# Brief P2 — build the ancients page (opencode)

Repo: /home/smoke01/dev/ancient-games. You may create/edit ONLY: `site/ancients/build.py`,
`site/ancients/templates/`, `site/ancients/dist/`, `site/ancients/Makefile`. Do NOT edit `site/ancients/tests/`,
`site/ancients/content/`, `site/ancients/tools/`, `site/ancients/docs/`, or anything outside `site/ancients/`.

## Read first
- `site/ancients/docs/blueprint/02-requirements.md`, `07-ui-ux.md` (**the DOM contract — the tests use exactly these
  selectors**), `08-non-functional.md`, `06-data-model.md`.
- `site/ancients/content/ancients.json` — the data (4 persons; items with title, kind, kind_tag, rule, words, source,
  label, from; `who.markdown`). Fields are Markdown.
- `site/ancients/templates/kindle-reference.html` (a copy of the kindle-page skill template) — the Kindle look to reuse: its theme colour variables
  (white, sepia, green, black), fonts (Literata, Georgia, Sans, Hyperlegible, with the CJK fallbacks), sizes,
  spacing/margins/alignment choices, and its settings-in-localStorage approach (wrapped in try/catch). Copy what you
  need into `templates/`; do not edit the skill.

## Template — what to build
1. `build.py`: reads `content/ancients.json`, renders every Markdown field to HTML at build time with markdown-it-py
   (`MarkdownIt("commonmark", {"html": False, "typographer": True}).enable(["table","strikethrough"])`), and writes ONE
   self-contained `dist/index.html` (CSS and JS inline; only Google Fonts loaded from outside). Title "The Ancient
   Games — Four Seats", `lang="en"`.
2. Layout (07-ui-ux.md): `#people` is a horizontal row, `display:flex`, `overflow-x:auto`,
   `scroll-snap-type:x mandatory`, `overscroll-behavior-x:contain`, scrollbar hidden. Four
   `section.person[data-person=id]`, each `flex:0 0 100%`, `scroll-snap-align:start`, `scroll-snap-stop:always`,
   `height:100dvh`, `overflow-y:auto` (each panel scrolls vertically on its own), padding so text never touches the
   screen edges (Android's edge-back gesture lives there).
3. Each panel: `.person-name` (h1), `.kinds` (e.g. "3 mindsets · 15 decision rules" — counted from kind_tag; say
   "1 algorithm" singular), `.who` (the bio; under it a small muted note: "From the first research round; its Chinese
   quotes were checked, its other facts were not re-checked."), then every item as
   `.item[data-n]` with `.kind` (a small tag: kind_tag), the title, `.rule`, `.words` (styled like a quote), `.source`
   and `.label` (small, muted), and at the end of the panel `.pct` showing that person's % read (update on scroll).
4. Fixed quiet header (Kindle style, small, muted): `#person-name`, `#person-pos` ("n / 4"), `#dots` with
   `button[data-goto=0..3]`, and an `#aa` button ("Aa") that opens `#menu`. Menu buttons carry
   `data-setting` (font, size, leading, margin, align, theme) and `data-value`; a Done button closes it.
5. Remember in localStorage (try/catch): settings, the current person index, and each panel's scroll offset; restore
   all on load (after `document.fonts.ready`). Default settings: theme sepia, font literata, size 18, leading normal,
   margin normal, align justify.
6. No text wider than its panel: tables `display:block; overflow-x:auto`, `pre` wraps, long words break.
7. `Makefile` targets: `content` (`python3 tools/extract_content.py && python3 tools/check_content.py`), `build`
   (`python3 build.py`), `test` (`python3 tests/test_mobile.py`), `all: content build test` (default).

## Example
A panel, shortened:
```html
<section class="person" data-person="fan-li"><h1 class="person-name">范蠡 (Fan Li)</h1>
<p class="kinds">3 mindsets · 15 decision rules</p><div class="who">…</div>
<article class="item" data-n="1"><span class="kind">decision rule</span><h3>Keep to the time…</h3>
<div class="rule">…</div><blockquote class="words">…</blockquote><p class="source">…</p><p class="label">quoted</p></article>
… <p class="pct">0%</p></section>
```

## Standard — how it is judged
`python3 build.py` exits 0 and writes `dist/index.html`; then `python3 tests/test_mobile.py` must print all PASS (the
tests may not exist yet when you start — if `tests/test_mobile.py` exists, run it with `python3` (not `-I`) and fix
the page until it passes; never edit the tests). End your answer with the last test run's output, or say that the
tests did not exist yet.
