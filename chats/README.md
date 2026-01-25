# Chats export notes (ChatGPT + Gemini)

This folder is for **exported chat transcripts** (usually as `.json` / `.md`) that informed this project.

## ChatGPT: export all chats from a Project (web UI → DevTools)

### Goal

Download every conversation in a specific **ChatGPT Project** into a single JSON file, by:

- collecting all conversation IDs from the Project chat list
- fetching each conversation via the same internal endpoint the web app uses
- saving a combined `*.json` file locally

### What you need

- Access to the Project in the ChatGPT web app (`chatgpt.com`)
- Chrome/Edge DevTools Console access

### 1) Open the Project’s chat list and load *all* items

ChatGPT’s left-side chat list is often **virtualized** (only renders what’s visible).

- Open the Project page where it lists chats.
- **Scroll all the way down** until you’re confident all chats have rendered at least once.
  - If you don’t scroll, the export will only include the IDs that happened to be in the DOM.

### 2) Collect conversation IDs from the DOM

Run in DevTools Console:

```js
// Collect conversation IDs from links currently in the DOM.
// If the list is virtualized, scroll to load more, then rerun.
const ids = [...new Set(
  [...document.querySelectorAll('a[href]')]
    .map(a => a.getAttribute('href'))
    .map(h => h && h.match(/\/c\/([a-f0-9-]{20,})/i)?.[1])
    .filter(Boolean)
)];
console.log(ids.length, ids.slice(0, 10));
```

#### Important: this collector can include non-Project chats

The selector above scans **every** link on the page. ChatGPT pages often include links to:

- recent/unclassified chats
- other areas of the app

Those links can also contain `/c/<conversation-id>`, so your exported set may include chats **outside** the intended Project.

##### Scoped collector (recommended)

If you’re on a Project/GPT page whose URL includes `/g/.../c/...`, use this instead. It only captures links that begin with the current `/g/<slug>` prefix.

```js
// Collect ONLY chats under the current /g/... scope.
// Note: use a distinct variable name so you don't collide with an earlier `const ids`.
const gPath = location.pathname.match(/^\/g\/[^/]+/)?.[0];
if (!gPath) throw new Error("Not on a /g/... page.");

const projectIds = [...new Set(
  [...document.querySelectorAll(`a[href^="${gPath}/c/"], a[href^="https://chatgpt.com${gPath}/c/"]`)]
    .map(a => a.getAttribute("href"))
    .map(h => new URL(h, location.origin).pathname)
    .map(p => p.match(/\/c\/([^/?#]+)/)?.[1])
    .filter(Boolean)
)];

console.log({ gPath, count: projectIds.length, sample: projectIds.slice(0, 10) });
```

### 3) Bulk fetch + download JSON (uses your existing `ids`)

The `backend-api` call often requires an **Authorization Bearer token** (cookies alone can yield 404s).

Run in DevTools Console (after the `ids` snippet above):

```js
async function getToken() {
  const session = await fetch("/api/auth/session", { credentials: "include" }).then((r) => r.json());
  return session?.accessToken || session?.access_token || null;
}

async function fetchConversation(id, token) {
  const res = await fetch(`/backend-api/conversation/${id}`, {
    credentials: "include",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error(`Fetch failed ${res.status} for ${id}`);
  return await res.json();
}

async function mapPool(limit, items, fn) {
  const out = new Array(items.length);
  let i = 0;
  await Promise.all(
    Array.from({ length: limit }, async () => {
      while (i < items.length) {
        const idx = i++;
        out[idx] = await fn(items[idx]);
      }
    })
  );
  return out;
}

(async () => {
  if (typeof ids === "undefined" || !Array.isArray(ids) || ids.length === 0) {
    throw new Error("No global `ids` array found. Re-run the ID collector first.");
  }

  const token = await getToken();
  const data = await mapPool(3, ids, (id) => fetchConversation(id, token));

  const blob = new Blob([JSON.stringify({ exported_at: new Date().toISOString(), ids, data }, null, 2)], {
    type: "application/json",
  });

  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `chatgpt-project-export-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
})();
```

#### If you hit “Can't create duplicate variable: 'ids'” / readonly assignment errors

If you previously ran `const ids = ...` in the Console, you can’t redeclare or reassign it in the same page context.

- **Simplest**: reload the page, then rerun your scripts.
- **No reload**: use a different variable name (like `projectIds`) and export from that.

##### Bulk export using `projectIds` (scoped collector)

```js
async function getToken() {
  const session = await fetch("/api/auth/session", { credentials: "include" }).then((r) => r.json());
  return session?.accessToken || session?.access_token || null;
}

async function fetchConversation(id, token) {
  const res = await fetch(`/backend-api/conversation/${id}`, {
    credentials: "include",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error(`Fetch failed ${res.status} for ${id}`);
  return await res.json();
}

async function mapPool(limit, items, fn) {
  const out = new Array(items.length);
  let i = 0;
  await Promise.all(
    Array.from({ length: limit }, async () => {
      while (i < items.length) {
        const idx = i++;
        out[idx] = await fn(items[idx]);
      }
    })
  );
  return out;
}

(async () => {
  if (typeof projectIds === "undefined" || !Array.isArray(projectIds) || projectIds.length === 0) {
    throw new Error("No `projectIds` array found. Run the scoped collector first.");
  }

  const token = await getToken();
  const data = await mapPool(3, projectIds, (id) => fetchConversation(id, token));

  const blob = new Blob(
    [JSON.stringify({ exported_at: new Date().toISOString(), ids: projectIds, data }, null, 2)],
    { type: "application/json" }
  );

  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `chatgpt-project-export-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
})();
```

### 4) Save the downloaded file into this repo

- Put the downloaded JSON into `chats/` (this folder).
- Recommended naming:
  - `chatgpt-project-EEProject-YYYY-MM-DD.json`

## Gemini (gemini.google.com): export by Category prefix (DevTools)

### Convention used

Chat titles are prefixed with a category before a dash:

- `Category-This Is the Chat title`

This allows exporting chats grouped by category (one file per category).

### Verified working method (one paste → exports all categories except `EE`)

Notes:

- **Open History sidebar** and scroll it until all chats are loaded (Gemini history is often virtualized).
- The script will **click through chats** while exporting (it can feel “creepy”).
- The browser may prompt to **allow multiple downloads** (one JSON per category).
- The export is DOM-based; the reliable payload is **`panel_text`** (full visible transcript).

Paste this in DevTools Console while on `gemini.google.com`:

```js
(async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const cleanText = (s) =>
    (s || "").replace(/\u00a0/g, " ").replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();

  function* walk(node) {
    if (!node) return;
    yield node;
    const sr = node.shadowRoot;
    if (sr) yield* walk(sr);
    for (const child of node.children || []) yield* walk(child);
  }

  function parseCategory(title) {
    const t = cleanText(title);
    const i = t.indexOf("-");
    if (i <= 0) return null;
    const category = cleanText(t.slice(0, i));
    const rest = cleanText(t.slice(i + 1));
    if (!category || !rest) return null;
    return { category, title: rest, full: t };
  }

  function collectHistoryItems() {
    const out = [];
    const seen = new Set();

    for (const node of walk(document.documentElement)) {
      const tag = node.tagName;
      const role = node.getAttribute?.("role");
      const isClickable =
        tag === "A" || tag === "BUTTON" || role === "link" || role === "menuitem" || role === "option";
      if (!isClickable) continue;

      const text = cleanText(node.innerText || node.textContent);
      if (!text || text.length > 140) continue;

      const parsed = parseCategory(text);
      if (!parsed) continue;

      const href = node.getAttribute?.("href") || null;
      const key = `${parsed.full}||${href || ""}`;
      if (seen.has(key)) continue;
      seen.add(key);

      out.push({ node, href, ...parsed });
    }
    return out;
  }

  function findMainLikeRoot() {
    const mains = [];
    for (const node of walk(document.documentElement)) {
      if (!node?.tagName) continue;
      const role = node.getAttribute?.("role");
      if (node.tagName === "MAIN" || role === "main") mains.push(node);
    }
    mains.sort((a, b) => cleanText(b.innerText).length - cleanText(a.innerText).length);
    return mains[0] || document.body;
  }

  function findBestScroller(root) {
    const scrollables = [];
    for (const node of walk(root)) {
      if (!(node instanceof HTMLElement)) continue;
      const sh = node.scrollHeight || 0;
      const ch = node.clientHeight || 0;
      if (sh > ch + 200) scrollables.push(node);
    }
    scrollables.sort((a, b) => (b.scrollHeight - b.clientHeight) - (a.scrollHeight - a.clientHeight));
    return scrollables[0] || null;
  }

  async function autoLoadOlderTurns(root, maxSteps = 35) {
    const scroller = findBestScroller(root);
    if (!scroller) return;

    // go bottom first
    scroller.scrollTop = scroller.scrollHeight;
    await sleep(600);

    // then top-until-stable to load older turns
    let lastH = -1;
    for (let i = 0; i < maxSteps; i++) {
      scroller.scrollTop = 0;
      await sleep(900);
      const h = scroller.scrollHeight;
      if (h === lastH) break;
      lastH = h;
    }

    // back to bottom
    scroller.scrollTop = scroller.scrollHeight;
    await sleep(300);
  }

  async function waitForChatReady(prevUrl, timeoutMs = 20000) {
    const start = Date.now();
    while (Date.now() - start < timeoutMs) {
      if (location.href !== prevUrl) return true;
      const root = findMainLikeRoot();
      if (cleanText(root.innerText).length > 50) return true;
      await sleep(250);
    }
    return false;
  }

  function downloadJson(filename, obj) {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  async function exportByCategory(categories, { delayMs = 1200 } = {}) {
    const items = collectHistoryItems();
    if (!items.length) throw new Error("Found 0 Category-Title items. Open History sidebar and scroll it to load chats.");

    const groups = new Map();
    for (const it of items) {
      if (!categories.includes(it.category)) continue;
      if (!groups.has(it.category)) groups.set(it.category, []);
      groups.get(it.category).push(it);
    }

    const seenAppIds = new Set();

    for (const [category, chats] of groups.entries()) {
      const exportedChats = [];

      for (const chat of chats) {
        const prevUrl = location.href;
        chat.node.click();
        await sleep(delayMs);
        await waitForChatReady(prevUrl);

        const appId = location.pathname.match(/\/app\/([a-z0-9]+)\b/i)?.[1] || null;
        if (appId && seenAppIds.has(appId)) continue;
        if (appId) seenAppIds.add(appId);

        const root = findMainLikeRoot();
        await autoLoadOlderTurns(root);

        exportedChats.push({
          sidebar_title: chat.full,
          parsed_title: chat.title,
          url: location.href,
          data: {
            exported_at: new Date().toISOString(),
            url: location.href,
            title: document.title || "Gemini chat",
            panel_text: cleanText(root.innerText),
          },
        });

        await sleep(200);
      }

      const safeCategory = category.replace(/[^\w.-]+/g, "_");
      downloadJson(`gemini-category-${safeCategory}-${new Date().toISOString().slice(0, 10)}.json`, {
        exported_at: new Date().toISOString(),
        category,
        chat_count: exportedChats.length,
        chats: exportedChats,
      });

      await sleep(800);
    }
  }

  // ---- run: all categories except EE ----
  const allItems = collectHistoryItems();
  const allCategories = [...new Set(allItems.map((x) => x.category))].filter(Boolean);
  const categories = allCategories.filter((c) => c !== "EE");

  console.log("Found categories:", allCategories);
  console.log("Exporting categories:", categories);

  await exportByCategory(categories, { delayMs: 1200 });

  console.log("Done.");
})();
```

### Verification spot-check (recommended)

For each exported category, open 1–2 exported chat URLs, scroll to the very top, and confirm the first prompt matches the start of `panel_text`. In testing, this validated that the export captured the full chat history.

### Alternatives (official)

- **Few chats**: use Gemini’s in-product **Share & export → Export to Docs**, then save/copy the doc content here.
- **Many chats**: use **Google Takeout** for Gemini Apps data, then filter by chat title(s).

## Post-processing exports (ChatGPT + Gemini) into Q&As

This repo includes scripts that convert the exported JSON files into:

- **HTML**: one page with a TOC, each Q visible, answer collapsed/expandable
- **JSONL**: one Q/A per line (useful for downstream processing)
- **Markdown**: per-chat Q/A files
- **Integrated Markdown**: topic-grouped narrative documents built from the HTML export

### Where exports should live

Do **not** commit raw exports to GitHub; they can contain sensitive content.

- `chats/.gitignore` ignores `*.json`, `*.zip`, and `*.html` within `chats/`.

In practice we kept the raw exports under `~/Downloads/EEProject-Chats/` and generated derived views next to them.

### 1) Extract Q/A pairs from export JSON

Script: `scripts/chats/extract_qa.py`

#### Gemini category export → Q/A

Input is the DevTools-exported Gemini JSON (contains `panel_text` per chat).

```bash
python3 "scripts/chats/extract_qa.py" \
  -i "$HOME/Downloads/EEProject-Chats/gemini-category-EE-2026-01-24-3.json" \
  --out-jsonl "$HOME/Downloads/EEProject-Chats/gemini-category-EE-2026-01-24-3.qa.jsonl" \
  --out-md-dir "$HOME/Downloads/EEProject-Chats/gemini-category-EE-2026-01-24-3.qa-md"
```

Notes:

- Gemini Q/A extraction is **best-effort** and relies on `Show thinking` markers inside `panel_text`.

#### ChatGPT Project export → Q/A

Input is the DevTools-exported ChatGPT JSON bundle.

```bash
python3 "scripts/chats/extract_qa.py" \
  -i "$HOME/Downloads/EEProject-Chats/chatgpt-project-export-2026-01-24.json" \
  --out-jsonl "$HOME/Downloads/EEProject-Chats/chatgpt-project-export-2026-01-24.qa.jsonl" \
  --out-md-dir "$HOME/Downloads/EEProject-Chats/chatgpt-project-export-2026-01-24.qa-md"
```

Notes:

- ChatGPT per-message `create_time` is preserved and attached to each extracted Q/A as:
  - `question_create_time_iso` / `answer_create_time_iso` (UTC)

### 2) Create HTML viewers (answers collapsed; click to expand)

These are convenient for browsing everything quickly.

#### Combined (ChatGPT + Gemini)

```bash
python3 "scripts/chats/extract_qa.py" \
  -i "$HOME/Downloads/EEProject-Chats/chatgpt-project-export-2026-01-24.json" \
  -i "$HOME/Downloads/EEProject-Chats/gemini-category-EE-2026-01-24-3.json" \
  --out-html "$HOME/Downloads/EEProject-Chats/chat-qa-all.html"
```

#### ChatGPT-only

```bash
python3 "scripts/chats/extract_qa.py" \
  -i "$HOME/Downloads/EEProject-Chats/chatgpt-project-export-2026-01-24.json" \
  --out-html "$HOME/Downloads/EEProject-Chats/chat-qa-chatgpt.html"
```

#### Gemini-only

```bash
python3 "scripts/chats/extract_qa.py" \
  -i "$HOME/Downloads/EEProject-Chats/gemini-category-EE-2026-01-24-3.json" \
  --out-html "$HOME/Downloads/EEProject-Chats/chat-qa-gemini.html"
```

### 3) “Original custom instructions no longer available” in ChatGPT exports

ChatGPT’s export JSON sometimes includes messages like:

- `Original custom instructions no longer available`

These appear as `author.role: "user"` but are tagged as hidden/system metadata:

- `metadata.is_user_system_message: true`
- `metadata.is_visually_hidden_from_conversation: true`

We **do not skip any messages**; instead the HTML marks these entries with a `hidden/system` badge so you can recognize them without altering their text.

### 4) Build topic-grouped Markdown from the HTML export

Script: `scripts/chats/html_to_narrative_md.py`

#### Verbatim topic grouping

```bash
python3 "scripts/chats/html_to_narrative_md.py" \
  -i "$HOME/Downloads/EEProject-Chats/chat-qa-all.html" \
  -o "chats/chat-qa-all.narrative.md" \
  --mode verbatim
```

#### Integrated narrative (connective prose + verbatim Q&As inline)

```bash
python3 "scripts/chats/html_to_narrative_md.py" \
  -i "$HOME/Downloads/EEProject-Chats/chat-qa-all.html" \
  -o "chats/chat-qa-all.integrated.md" \
  --mode narrative
```

Notes:

- Very long “doc review” prompts can be omitted by heuristic (see script); everything else is included.
- Q&As that don’t match any topic bucket are placed under **Unsorted** at the end.

## Google AI Studio (aistudio.google.com): export options (high level)

- The most practical approach is usually a **browser exporter extension** that downloads the current conversation as JSON/Markdown.

