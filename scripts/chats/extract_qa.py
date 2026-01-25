#!/usr/bin/env python3
"""
Extract Q/A pairs from ChatGPT + Gemini exported JSON files.

Supported inputs:
- ChatGPT single conversation JSON from /backend-api/conversation/<id>
- ChatGPT bundle JSON produced by our DevTools exporter ({ ids: [...], data: [conversationJson...] })
- Gemini category export JSON produced by our DevTools exporter ({ category, chats: [{..., data: { panel_text }}] })

Outputs:
- JSONL file of Q/A pairs
- Optional per-chat Markdown files
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from html import escape as _html_escape
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _slugify(s: str, max_len: int = 80) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s.-]+", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = s.strip("-")
    return (s[:max_len] or "chat")


def _now_stamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")


def _epoch_to_iso(ts: Optional[float]) -> Optional[str]:
    if ts is None:
        return None
    try:
        return datetime.utcfromtimestamp(float(ts)).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


@dataclass
class Turn:
    role: str  # "user" | "assistant"
    text: str
    create_time: Optional[float]  # epoch seconds (ChatGPT), else None
    # ChatGPT-only flags (best-effort). Gemini exports do not provide these.
    is_user_system_message: bool = False
    is_visually_hidden_from_conversation: bool = False


@dataclass
class Chat:
    source: str  # "chatgpt" | "gemini"
    id: str  # conversation id or app id
    title: str
    url: Optional[str]
    category: Optional[str]
    turns: list[Turn]


def _extract_chatgpt_content_text(content: dict[str, Any]) -> str:
    """
    ChatGPT message content can be:
    - {"content_type":"text","parts":[...]}
    - {"content_type":"multimodal_text","parts":[...]}
    - other types; we best-effort.
    """
    parts = content.get("parts")
    if isinstance(parts, list):
        return "\n".join(str(p) for p in parts if p is not None).strip()
    # fallback
    text = content.get("text")
    if isinstance(text, str):
        return text.strip()
    return ""


def _extract_chatgpt_linear_turns(conv: dict[str, Any]) -> list[Turn]:
    mapping = conv.get("mapping") or {}
    current = conv.get("current_node")
    out_rev: list[Turn] = []

    while current and current in mapping:
        node = mapping[current] or {}
        msg = node.get("message")
        if isinstance(msg, dict):
            role = (msg.get("author") or {}).get("role")
            if role in ("user", "assistant"):
                meta = msg.get("metadata") or {}
                content = msg.get("content") or {}
                text = _extract_chatgpt_content_text(content)
                if text:
                    ct = msg.get("create_time")
                    try:
                        ct_f = float(ct) if ct is not None else None
                    except Exception:
                        ct_f = None
                    out_rev.append(
                        Turn(
                            role=role,
                            text=text,
                            create_time=ct_f,
                            is_user_system_message=bool(meta.get("is_user_system_message")),
                            is_visually_hidden_from_conversation=bool(meta.get("is_visually_hidden_from_conversation")),
                        )
                    )
        current = node.get("parent")

    # we walked backwards from current_node
    out_rev.reverse()
    return out_rev


def _chatgpt_chat_from_json(obj: dict[str, Any]) -> Chat:
    conv_id = str(obj.get("conversation_id") or obj.get("id") or "unknown")
    title = str(obj.get("title") or conv_id)
    turns = _extract_chatgpt_linear_turns(obj)
    return Chat(
        source="chatgpt",
        id=conv_id,
        title=title,
        url=None,
        category=None,
        turns=turns,
    )


def _trim_gemini_header(panel_text: str) -> str:
    t = panel_text.strip()
    marker = "Conversation with Gemini"
    idx = t.find(marker)
    if idx == -1:
        return t
    after = t[idx + len(marker) :]
    return after.strip()


def _gemini_guess_pairs(panel_text: str) -> list[tuple[str, str]]:
    """
    Best-effort parsing of Gemini panel_text into (question, answer) pairs.

    We rely on the 'Show thinking' marker which appears between a user prompt and Gemini's response.
    """
    t = _trim_gemini_header(panel_text)
    sep = "\n\nShow thinking\n\n"
    if sep not in t:
        # Nothing to split; return as one big blob as "assistant"
        return []

    chunks = t.split(sep)
    # chunks[0] ends with user1; each subsequent chunk i contains assistant_{i} + user_{i+1} (except last)
    user1 = chunks[0].strip()

    def tail_user_text(s: str) -> str:
        # take last 1-2 paragraphs as "next user prompt"
        paras = [p.strip() for p in s.strip().split("\n\n") if p.strip()]
        if not paras:
            return ""
        tail = paras[-1]
        # sometimes the prompt includes a filename/format + prompt; allow 2 paras if short
        if len(paras) >= 2 and (len(tail) < 240 and len(paras[-2]) < 240):
            tail = paras[-2] + "\n\n" + paras[-1]
        return tail.strip()

    pairs: list[tuple[str, str]] = []
    prev_q = user1

    for i in range(1, len(chunks)):
        chunk = chunks[i].strip()
        if not chunk:
            continue

        if i < len(chunks) - 1:
            next_q = tail_user_text(chunk)
            a = chunk
            if next_q and a.endswith(next_q):
                a = a[: -len(next_q)].rstrip()
            pairs.append((prev_q, a.strip()))
            prev_q = next_q.strip()
        else:
            # last chunk: assistant_last (plus possible footer)
            a = chunk.strip()
            # common footer line(s)
            a = re.sub(r"\n\nFast\n\nGemini can make mistakes, so double-check it\s*$", "", a, flags=re.IGNORECASE)
            pairs.append((prev_q, a.strip()))

    # drop empty questions (can happen if heuristic fails)
    pairs = [(q, a) for (q, a) in pairs if q.strip() and a.strip()]
    return pairs


def _gemini_chats_from_json(obj: dict[str, Any]) -> list[Chat]:
    category = obj.get("category")
    chats = obj.get("chats") or []
    out: list[Chat] = []

    for c in chats:
        if not isinstance(c, dict):
            continue
        url = c.get("url")
        app_id = None
        if isinstance(url, str):
            m = re.search(r"/app/([a-z0-9]+)\b", url, re.IGNORECASE)
            app_id = m.group(1) if m else None
        app_id = app_id or _slugify(str(c.get("parsed_title") or c.get("sidebar_title") or "chat"))

        title = str(c.get("sidebar_title") or c.get("parsed_title") or app_id)
        data = c.get("data") or {}
        panel_text = data.get("panel_text") if isinstance(data, dict) else None
        if not isinstance(panel_text, str) or not panel_text.strip():
            continue

        pairs = _gemini_guess_pairs(panel_text)
        # represent as turns in user/assistant alternating
        turns: list[Turn] = []
        for q, a in pairs:
            turns.append(Turn(role="user", text=q, create_time=None))
            turns.append(Turn(role="assistant", text=a, create_time=None))

        out.append(
            Chat(
                source="gemini",
                id=str(app_id),
                title=title,
                url=str(url) if isinstance(url, str) else None,
                category=str(category) if category is not None else None,
                turns=turns,
            )
        )

    return out


def _detect_and_load_chats(path: Path) -> list[Chat]:
    obj = _read_json(path)
    if not isinstance(obj, dict):
        raise ValueError("Top-level JSON must be an object.")

    # ChatGPT bundle
    if isinstance(obj.get("data"), list) and isinstance(obj.get("ids"), list):
        chats: list[Chat] = []
        for item in obj["data"]:
            if isinstance(item, dict) and item.get("mapping"):
                chats.append(_chatgpt_chat_from_json(item))
        return chats

    # ChatGPT single conversation
    if obj.get("mapping") and isinstance(obj.get("mapping"), dict):
        return [_chatgpt_chat_from_json(obj)]

    # Gemini category export
    if isinstance(obj.get("chats"), list) and any(isinstance(x, dict) and "data" in x for x in obj["chats"]):
        return _gemini_chats_from_json(obj)

    raise ValueError("Unrecognized export format.")


def _to_qa_pairs(chat: Chat) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    pending_q: Optional[str] = None
    pending_q_ts: Optional[float] = None
    pending_q_is_user_system: bool = False
    pending_q_is_hidden: bool = False
    idx = 0
    for turn in chat.turns:
        if turn.role == "user":
            pending_q = turn.text.strip()
            pending_q_ts = turn.create_time
            pending_q_is_user_system = turn.is_user_system_message
            pending_q_is_hidden = turn.is_visually_hidden_from_conversation
        elif turn.role == "assistant" and pending_q:
            idx += 1
            a_ts = turn.create_time
            pairs.append(
                {
                    "source": chat.source,
                    "category": chat.category,
                    "chat_id": chat.id,
                    "title": chat.title,
                    "url": chat.url,
                    "turn_index": idx,
                    "question": pending_q,
                    "answer": turn.text.strip(),
                    "question_create_time": pending_q_ts,
                    "question_create_time_iso": _epoch_to_iso(pending_q_ts),
                    "answer_create_time": a_ts,
                    "answer_create_time_iso": _epoch_to_iso(a_ts),
                    "question_is_user_system_message": bool(pending_q_is_user_system),
                    "question_is_visually_hidden_from_conversation": bool(pending_q_is_hidden),
                }
            )
            pending_q = None
            pending_q_ts = None
    return pairs


def _render_chat_markdown(chat: Chat, qa_pairs: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append(f"# {chat.title}")
    if chat.url:
        lines.append("")
        lines.append(f"- Source: {chat.url}")
    else:
        lines.append("")
        lines.append(f"- Source id: `{chat.id}`")
    if chat.category:
        lines.append(f"- Category: `{chat.category}`")
    lines.append("")

    for p in qa_pairs:
        lines.append(f"## Q{p['turn_index']}")
        if p.get("question_create_time_iso"):
            lines.append("")
            lines.append(f"- Timestamp: `{p['question_create_time_iso']}`")
        lines.append("")
        lines.append(p["question"])
        lines.append("")
        lines.append(f"## A{p['turn_index']}")
        if p.get("answer_create_time_iso"):
            lines.append("")
            lines.append(f"- Timestamp: `{p['answer_create_time_iso']}`")
        lines.append("")
        lines.append(p["answer"])
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _render_all_html(chats: list[Chat], pairs: list[dict[str, Any]], title: str) -> str:
    """
    Render a single HTML document with all chats.

    Each Q/A is rendered as a <details> element:
    - Question visible in <summary>
    - Answer hidden until expanded
    """
    # group pairs by chat_id (and source) preserving order
    by_chat: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for p in pairs:
        key = (str(p.get("source")), str(p.get("chat_id")))
        by_chat.setdefault(key, []).append(p)

    def h(s: Any) -> str:
        return _html_escape("" if s is None else str(s), quote=True)

    def pre_block(text: str) -> str:
        # preserve formatting without needing markdown parsing
        return f"<pre>{h(text)}</pre>"

    chat_sections: list[str] = []
    toc_items: list[str] = []

    for chat in chats:
        key = (chat.source, chat.id)
        chat_pairs = by_chat.get(key, [])
        anchor = f"{chat.source}-{chat.id}"
        toc_label = chat.title
        if chat.category:
            toc_label = f"{chat.category} — {toc_label}"
        toc_items.append(f'<li><a href="#{h(anchor)}">{h(toc_label)}</a> <span class="meta">({h(chat.source)}, {len(chat_pairs)} Q&A)</span></li>')

        header_bits = [f'<h2 id="{h(anchor)}">{h(chat.title)}</h2>']
        meta: list[str] = []
        if chat.category:
            meta.append(f'Category: <code>{h(chat.category)}</code>')
        if chat.url:
            meta.append(f'Source: <a href="{h(chat.url)}" target="_blank" rel="noreferrer">{h(chat.url)}</a>')
        else:
            meta.append(f'Chat id: <code>{h(chat.id)}</code>')
        header_bits.append(f'<div class="chat-meta">{" • ".join(meta)}</div>')

        qa_bits: list[str] = []
        for p in chat_pairs:
            q = str(p.get("question") or "").strip()
            a = str(p.get("answer") or "").strip()
            idx = p.get("turn_index")
            qts = p.get("question_create_time_iso")
            ats = p.get("answer_create_time_iso")
            ts_label = f" [{h(qts)}]" if qts else ""
            ans_ts = f'<div class="ts">Answer timestamp: <code>{h(ats)}</code></div>' if ats else ""
            badge = ""
            if p.get("question_is_user_system_message") or p.get("question_is_visually_hidden_from_conversation"):
                badge = ' <span class="badge">hidden/system</span>'
            qa_bits.append(
                "\n".join(
                    [
                        '<details class="qa">',
                        f'  <summary><span class="qnum">Q{h(idx)}</span>{ts_label}{badge} {h(q)}</summary>',
                        f'  <div class="answer">{ans_ts}{pre_block(a)}</div>',
                        "</details>",
                    ]
                )
            )

        if not qa_bits:
            qa_bits.append('<div class="empty">No Q/A pairs were extracted for this chat.</div>')

        chat_sections.append("\n".join(header_bits + qa_bits))

    css = """
    :root { color-scheme: light dark; }
    body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji"; margin: 24px; line-height: 1.35; }
    h1 { margin: 0 0 8px 0; }
    .sub { color: #666; font-size: 14px; margin-bottom: 18px; }
    .toc { padding: 12px 14px; border: 1px solid #ddd; border-radius: 10px; background: rgba(0,0,0,0.02); }
    .toc ul { margin: 8px 0 0 18px; }
    .toc li { margin: 6px 0; }
    .meta { color: #777; font-size: 12px; margin-left: 6px; }
    h2 { margin-top: 28px; border-top: 1px solid #eee; padding-top: 18px; }
    .chat-meta { color: #666; font-size: 13px; margin: 6px 0 12px 0; }
    details.qa { border: 1px solid #e5e5e5; border-radius: 10px; padding: 10px 12px; margin: 10px 0; background: rgba(0,0,0,0.015); }
    details.qa[open] { background: rgba(0,0,0,0.03); }
    summary { cursor: pointer; }
    summary::-webkit-details-marker { display: none; }
    summary::before { content: "▸"; display: inline-block; width: 1em; }
    details[open] summary::before { content: "▾"; }
    .qnum { font-weight: 700; margin-right: 8px; }
    .badge { display: inline-block; margin: 0 8px 0 6px; padding: 1px 6px; border-radius: 999px; border: 1px solid #ccc; font-size: 11px; color: #666; vertical-align: 1px; }
    .answer { margin-top: 10px; }
    .ts { color: #777; font-size: 12px; margin: 2px 0 10px 0; }
    pre { white-space: pre-wrap; word-wrap: break-word; margin: 0; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: 13px; }
    .empty { color: #777; font-style: italic; margin: 10px 0 0 0; }
    """.strip()

    doc = "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '  <meta charset="utf-8" />',
            '  <meta name="viewport" content="width=device-width, initial-scale=1" />',
            f"  <title>{h(title)}</title>",
            f"  <style>{css}</style>",
            "</head>",
            "<body>",
            f"  <h1>{h(title)}</h1>",
            f'  <div class="sub">Generated {_now_stamp()} • Chats: {len(chats)} • Q&amp;A pairs: {len(pairs)}</div>',
            '  <div class="toc"><strong>Chats</strong><ul>',
            *[f"    {x}" for x in toc_items],
            "  </ul></div>",
            *chat_sections,
            "</body>",
            "</html>",
        ]
    )
    return doc


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", action="append", required=True, help="Path to export JSON (repeatable).")
    ap.add_argument("--out-jsonl", default=None, help="Write Q/A pairs to this JSONL file (default: stdout).")
    ap.add_argument("--out-md-dir", default=None, help="Write per-chat markdown files to this directory.")
    ap.add_argument("--out-html", default=None, help="Write a single HTML file with all chats/Q&A.")
    args = ap.parse_args(argv)

    all_pairs: list[dict[str, Any]] = []
    all_chats: list[Chat] = []

    for p in args.input:
        chats = _detect_and_load_chats(Path(p).expanduser())
        all_chats.extend(chats)

    for chat in all_chats:
        pairs = _to_qa_pairs(chat)
        all_pairs.extend(pairs)

        if args.out_md_dir:
            out_dir = Path(args.out_md_dir).expanduser()
            fname = f"{chat.source}-{_slugify(chat.title)}-{chat.id}.md"
            _write_text(out_dir / fname, _render_chat_markdown(chat, pairs))

    if args.out_html:
        html_title = "Chat Q&A Export"
        if len(args.input) == 1:
            html_title = Path(args.input[0]).name
        _write_text(Path(args.out_html).expanduser(), _render_all_html(all_chats, all_pairs, html_title))

    out_lines = [json.dumps(p, ensure_ascii=False) for p in all_pairs]
    out_text = "\n".join(out_lines) + ("\n" if out_lines else "")
    if args.out_jsonl:
        _write_text(Path(args.out_jsonl).expanduser(), out_text)
    else:
        sys.stdout.write(out_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

