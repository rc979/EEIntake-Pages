#!/usr/bin/env python3
"""
Convert our exported chat Q&A HTML into a single narrative Markdown document.

Input: HTML produced by scripts/chats/extract_qa.py --out-html
Output: Markdown grouped by topic sections, with Q/A text copied verbatim.

Rules implemented (per user request):
- Omit Q&As whose question is "very long" and looks like a request for opinion on a long document.
- Q&As that don't match any topic bucket are listed at the end.

Two output modes:
- verbatim: reorganize only; copy Q/A text verbatim
- narrative: write a cohesive narrative section (paraphrasing allowed), then include a verbatim appendix
"""

from __future__ import annotations

import argparse
import html as _html
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _now_stamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _strip_tags(s: str) -> str:
    # Minimal tag stripper for our controlled HTML
    s = re.sub(r"<[^>]+>", "", s)
    return _html.unescape(s)


@dataclass
class QA:
    source: str
    chat_id: str
    chat_title: str
    category: Optional[str]
    url: Optional[str]
    qnum: str
    question: str
    answer: str


def _parse_chat_meta(meta_html: str) -> tuple[Optional[str], Optional[str]]:
    # Examples in our HTML:
    # Category: <code>EE</code> • Source: <a href="...">...</a>
    category = None
    url = None

    m = re.search(r"Category:\s*<code>(.*?)</code>", meta_html, flags=re.IGNORECASE | re.DOTALL)
    if m:
        category = _strip_tags(m.group(1)).strip()

    m = re.search(r'Source:\s*<a[^>]+href="([^"]+)"', meta_html, flags=re.IGNORECASE)
    if m:
        url = _html.unescape(m.group(1)).strip()

    return category, url


def _iter_qas_from_html(html_text: str) -> list[QA]:
    """
    Parse the specific structure produced by extract_qa.py:
      <h2 id="source-id">Chat Title</h2>
      <div class="chat-meta">...</div>
      <details class="qa">
        <summary><span class="qnum">Q1</span> QUESTION</summary>
        <div class="answer"><pre>ANSWER</pre></div>
      </details>
    """
    # Split into chat blocks by <h2 ...>
    h2_re = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.IGNORECASE | re.DOTALL)
    matches = list(h2_re.finditer(html_text))
    qas: list[QA] = []

    for i, m in enumerate(matches):
        anchor = _html.unescape(m.group(1))
        chat_title = _strip_tags(m.group(2)).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html_text)
        block = html_text[start:end]

        # anchor looks like "chatgpt-<id>" or "gemini-<id>"
        if "-" in anchor:
            source, chat_id = anchor.split("-", 1)
        else:
            source, chat_id = "unknown", anchor

        meta_match = re.search(r'<div class="chat-meta">(.*?)</div>', block, flags=re.IGNORECASE | re.DOTALL)
        category, url = (None, None)
        if meta_match:
            category, url = _parse_chat_meta(meta_match.group(1))

        # details blocks
        details_re = re.compile(
            r'<details class="qa">.*?<summary>(.*?)</summary>.*?<pre>(.*?)</pre>.*?</details>',
            re.IGNORECASE | re.DOTALL,
        )
        for d in details_re.finditer(block):
            summary_html = d.group(1)
            pre_html = d.group(2)

            # summary is: <span class="qnum">Q1</span> QUESTION
            qnum_m = re.search(r'<span class="qnum">(Q\d+)</span>', summary_html, flags=re.IGNORECASE)
            qnum = _strip_tags(qnum_m.group(1)).strip() if qnum_m else "Q?"

            # question is whatever remains after qnum span
            q_html = re.sub(r'<span class="qnum">.*?</span>', "", summary_html, flags=re.IGNORECASE | re.DOTALL)
            question = _strip_tags(q_html).strip()

            answer = _html.unescape(pre_html)
            # keep line breaks as-is; normalize trailing whitespace
            answer = answer.replace("\r\n", "\n").replace("\r", "\n").strip()

            qas.append(
                QA(
                    source=source.strip(),
                    chat_id=chat_id.strip(),
                    chat_title=chat_title,
                    category=category,
                    url=url,
                    qnum=qnum,
                    question=question.replace("\r\n", "\n").replace("\r", "\n").strip(),
                    answer=answer,
                )
            )

    return qas


def _is_long_doc_review_prompt(q: str) -> bool:
    """
    Heuristic for "very long question asking for opinion of a long document".
    We only omit when the question itself is long.
    """
    qn = q.strip()
    lines = qn.splitlines()
    if len(qn) >= 2000:
        return True
    if len(lines) >= 60 and len(qn) >= 1200:
        return True
    # common structure when a large document is pasted
    if len(qn) >= 1200 and (qn.count("```") >= 2 or re.search(r"^#{1,6}\s", qn, flags=re.MULTILINE)):
        return True
    if len(qn) >= 1200 and ("table of contents" in qn.lower() or "toc" in qn.lower()):
        return True
    return False


TOPICS: list[tuple[str, list[str]]] = [
    (
        "EV charging: design, permitting, AHJ, utility, interconnection",
        [
            r"\bev\b",
            r"\bevse\b",
            r"charging",
            r"\bahj\b",
            r"permit",
            r"interconnection",
            r"pge|pg&e",
            r"utility",
            r"load calc|load calculation|nec",
            r"\bems\b",
            r"one-line|single[- ]line",
            r"panel|breaker|service upgrade",
            r"rule 21|rule 16",
        ],
    ),
    (
        "Workflow, automation, tooling, documentation systems",
        [
            r"\bworkflow\b",
            r"automation|automate",
            r"\bai\b|llm|rag|ocr",
            r"pipeline|artifact|dependency|traceability",
            r"github pages|publish|docs/|robots\.txt|noindex",
            r"script|python|repo|git",
        ],
    ),
    (
        "Engineering services business, pricing, market, careers",
        [
            r"fee|fees|\bcost\b|\bprice\b|\bquote\b|\brange\b|\$",
            r"market|demand|shortage",
            r"remote ee|stamping|pe license|principal",
            r"vc|pitch|persona|fundraising",
            r"revenue|timeline",
        ],
    ),
    (
        "Tax and legal",
        [
            r"\btax\b",
            r"home office",
            r"divorce|separation|support",
        ],
    ),
    (
        "Other technology / general topics",
        [
            r"nuclear|oklo",
            r"watch|iphone|apple",
            r"cyber|security|vciso",
        ],
    ),
]


def _topic_for(qa: QA) -> Optional[str]:
    text = f"{qa.question}\n\n{qa.answer}".lower()
    for topic, pats in TOPICS:
        for p in pats:
            if re.search(p, text, flags=re.IGNORECASE):
                return topic
    return None


_STOPWORDS = {
    "a",
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "he",
    "her",
    "here",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "itself",
    "just",
    "me",
    "more",
    "most",
    "my",
    "myself",
    "no",
    "nor",
    "not",
    "now",
    "of",
    "off",
    "on",
    "once",
    "only",
    "or",
    "other",
    "our",
    "ours",
    "ourselves",
    "out",
    "over",
    "own",
    "same",
    "she",
    "should",
    "so",
    "some",
    "such",
    "than",
    "that",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "us",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "whom",
    "why",
    "with",
    "would",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
}


def _keywords(qas: list[QA], limit: int = 18) -> list[str]:
    text = "\n".join([qa.question + "\n" + qa.answer for qa in qas]).lower()
    words = re.findall(r"[a-z0-9][a-z0-9&.+-]{1,}", text)
    counts: dict[str, int] = {}
    for w in words:
        if w in _STOPWORDS:
            continue
        if len(w) <= 2:
            continue
        counts[w] = counts.get(w, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [w for w, _ in ranked[:limit]]


def _render_md_verbatim(qas: list[QA], source_path: str, title: str) -> str:
    included: list[QA] = []
    omitted: int = 0
    for qa in qas:
        if _is_long_doc_review_prompt(qa.question):
            omitted += 1
            continue
        included.append(qa)

    # bucket by topic, preserve original order
    buckets: dict[str, list[QA]] = {t: [] for t, _ in TOPICS}
    other: list[QA] = []
    for qa in included:
        t = _topic_for(qa)
        if t is None:
            other.append(qa)
        else:
            buckets[t].append(qa)

    def md_escape_heading(s: str) -> str:
        return s.replace("\n", " ").strip()

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- Source HTML: `{source_path}`")
    lines.append(f"- Generated: `{_now_stamp()}`")
    lines.append(f"- Q&As included: `{len(included)}`")
    lines.append(f"- Q&As omitted (very long doc-review prompts): `{omitted}`")
    lines.append("")
    lines.append("This document reorganizes the extracted Q&As into topic sections. **Question and answer text is copied verbatim** from the source HTML.")
    lines.append("")

    def render_qa_block(qa: QA) -> None:
        meta_bits = [qa.source]
        if qa.category:
            meta_bits.append(f"category={qa.category}")
        meta_bits.append(f"chat={qa.chat_title}")
        if qa.url:
            meta_bits.append(qa.url)

        lines.append(f"#### {qa.qnum} ({', '.join(meta_bits)})")
        lines.append("")
        lines.append("```text")
        lines.append(qa.question)
        lines.append("```")
        lines.append("")
        lines.append("```text")
        lines.append(qa.answer)
        lines.append("```")
        lines.append("")

    for topic, _ in TOPICS:
        items = buckets.get(topic, [])
        if not items:
            continue
        lines.append(f"## {md_escape_heading(topic)}")
        lines.append("")
        for qa in items:
            render_qa_block(qa)

    if other:
        lines.append("## Unsorted (did not match any topic)")
        lines.append("")
        for qa in other:
            render_qa_block(qa)

    return "\n".join(lines).rstrip() + "\n"


def _render_md_narrative(qas: list[QA], source_path: str) -> str:
    """
    Narrative output: connective prose + verbatim Q&As embedded inline.
    """
    included: list[QA] = []
    omitted: int = 0
    for qa in qas:
        if _is_long_doc_review_prompt(qa.question):
            omitted += 1
            continue
        included.append(qa)

    # bucket by topic, preserve order
    buckets: dict[str, list[QA]] = {t: [] for t, _ in TOPICS}
    other: list[QA] = []
    for qa in included:
        t = _topic_for(qa)
        if t is None:
            other.append(qa)
        else:
            buckets[t].append(qa)

    # Narrative section: connective prose + embedded Q&As (verbatim)
    lines: list[str] = []
    lines.append("# Integrated narrative (verbatim Q&As embedded)")
    lines.append("")
    lines.append(f"- Source HTML: `{source_path}`")
    lines.append(f"- Generated: `{_now_stamp()}`")
    lines.append(f"- Q&As included: `{len(included)}`")
    lines.append(f"- Q&As omitted (very long doc-review prompts): `{omitted}`")
    lines.append("")
    lines.append(
        "This document integrates Q&As from ChatGPT and Gemini into a single narrative by grouping them into topical sections. "
        "Within each section, Q&As are included **verbatim** (no edits), with brief connective prose to keep the flow readable."
    )
    lines.append("")

    def render_qa(qa: QA) -> None:
        meta_bits = [qa.source]
        if qa.category:
            meta_bits.append(f"category={qa.category}")
        meta_bits.append(f"chat={qa.chat_title}")
        if qa.url:
            meta_bits.append(qa.url)

        lines.append(f"#### {qa.qnum} ({', '.join(meta_bits)})")
        lines.append("")
        lines.append("**Question (verbatim)**")
        lines.append("")
        lines.append("```text")
        lines.append(qa.question)
        lines.append("```")
        lines.append("")
        lines.append("**Answer (verbatim)**")
        lines.append("")
        lines.append("```text")
        lines.append(qa.answer)
        lines.append("```")
        lines.append("")

    def _chat_group_keywords(chat_items: list[QA]) -> list[str]:
        # Keywords biased toward questions + early answer text (avoid huge-answer overweight)
        text_parts: list[str] = []
        for x in chat_items:
            text_parts.append(x.question)
            text_parts.append(x.answer[:800])
        text = "\n".join(text_parts).lower()
        words = re.findall(r"[a-z0-9][a-z0-9&.+-]{1,}", text)
        counts: dict[str, int] = {}
        for w in words:
            if w in _STOPWORDS or len(w) <= 2:
                continue
            counts[w] = counts.get(w, 0) + 1
        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return [w for w, _ in ranked[:10]]

    def render_topic(topic: str, items: list[QA]) -> None:
        lines.append(f"## {topic}")
        lines.append("")
        lines.append(
            "This section groups together Q&As that belong to the same theme, even when they were asked across different chats. "
            "The short connective text is only for reading flow; the Q&As remain verbatim."
        )
        lines.append("")

        topic_kws = _keywords(items, limit=18)
        if topic_kws:
            lines.append("Thread keywords: " + ", ".join(f"`{k}`" for k in topic_kws[:12]) + ".")
            lines.append("")

        current_chat: Optional[str] = None
        current_items: list[QA] = []

        def flush_chat_group() -> None:
            nonlocal current_chat, current_items
            if not current_chat or not current_items:
                return
            lines.append(f"### {current_chat}")
            lines.append("")
            kws = _chat_group_keywords(current_items)
            if kws:
                lines.append(
                    "In this sub-thread, the questions cluster around: " + ", ".join(f"`{k}`" for k in kws[:8]) + "."
                )
                lines.append("")
            for qa2 in current_items:
                render_qa(qa2)
            current_items = []

        for qa in items:
            if qa.chat_title != current_chat:
                flush_chat_group()
                if current_chat is not None:
                    lines.append(
                        "Next, the conversation continues in a different chat thread while staying within the same topic."
                    )
                    lines.append("")
                current_chat = qa.chat_title
            current_items.append(qa)

        flush_chat_group()

    for topic, _ in TOPICS:
        items = buckets.get(topic, [])
        if not items:
            continue
        render_topic(topic, items)

    if other:
        lines.append("## Unsorted (did not fit a topic)")
        lines.append("")
        lines.append("Some Q&As did not match any topic bucket. They are listed verbatim below.")
        lines.append("")
        current_chat = None
        for qa in other:
            if qa.chat_title != current_chat:
                current_chat = qa.chat_title
                lines.append(f"### {current_chat}")
                lines.append("")
            render_qa(qa)

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-html", "-i", required=True, help="Path to chat-qa-all.html")
    ap.add_argument("--out-md", "-o", required=True, help="Path to write narrative markdown")
    ap.add_argument("--mode", choices=["verbatim", "narrative"], default="verbatim")
    args = ap.parse_args(argv)

    html_text = _read_text(Path(args.input_html).expanduser())
    qas = _iter_qas_from_html(html_text)
    if args.mode == "narrative":
        md = _render_md_narrative(qas, args.input_html)
    else:
        md = _render_md_verbatim(qas, args.input_html, title="Integrated Q&A narrative (verbatim)")
    _write_text(Path(args.out_md).expanduser(), md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv[1:]))

