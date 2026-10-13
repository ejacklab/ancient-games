# Brief P3 — mobile tests for the ancients page (Codex)

Repo: /home/smoke01/dev/ancient-games. You may create/edit ONLY `site/ancients/tests/` (and screenshots under
`runs/20261013-ancients-page/shots/`). Do not touch anything else. The page does not exist yet — write the tests from
the requirements, not from an implementation.

## Read
- `site/ancients/docs/blueprint/02-requirements.md` (R1–R6, ids), `07-ui-ux.md` (the DOM contract — use exactly
  these selectors), `08-non-functional.md` (N1, N2), `06-data-model.md`.
- `site/ancients/content/ancients.json` (the data the page must show).

## Template — what to write
`site/ancients/tests/test_mobile.py`, a plain Python 3 script (Playwright sync API, already installed: run it with
`python3`, not `python3 -I`):
- `python3 test_mobile.py [--url URL] [--shots DIR]`; default URL = `file://<repo>/site/ancients/dist/index.html`,
  default shots dir = `<repo>/runs/20261013-ancients-page/shots`.
- Device (N1): Chromium, viewport 412×915, device_scale_factor 3.5, is_mobile=True, has_touch=True, an Android Chrome
  user agent.
- One test function per criterion: R1.1, R1.2, R1.3, R2.1, R2.2, R2.3, R3.1, R3.2, R4.1, R4.2, R4.3, R4.4, R5.1, N2.
  Each prints exactly one line `PASS <id> <short note>` or `FAIL <id> <reason with the observed value>`; a test that
  throws is a FAIL with the exception text. Last line: `SUMMARY <passed>/<total>`. Exit 0 only if all pass.
- Swipes must be real touch scrolling so CSS scroll-snap is exercised: use a CDP session
  (`context.new_cdp_session(page)`) and `Input.synthesizeScrollGesture` with `gestureSourceType: "touch"`
  (horizontal: x from 80% to 20% of the width at half the height; vertical: inside the current panel). After a
  gesture, wait until scroll positions stop changing before you assert.
- "Current person" = the `section.person` whose left edge is at the `#people` scroll position (±2 px), and
  `#person-pos` reads "n / 4".
- R1.2/R5.1: compare each `.item[data-n]`'s `.words`, `.rule` text with the JSON after reducing both to letters,
  digits and CJK characters only (Markdown is rendered to HTML, so punctuation and markup differ).
- R4.2: pick sepia→black via `#menu [data-setting="theme"][data-value="black"]`, go to person 3, scroll it down,
  reload, then assert theme black, person 3, and its scroll offset restored (±40 px).
- R4.3: for every `section.person`, `scrollWidth <= clientWidth + 1`.
- N2: record every request; any host other than `fonts.googleapis.com`, `fonts.gstatic.com` (or a `file:` URL) is a
  FAIL; `document.cookie` must be empty.
- Save a screenshot per person (`person-<n>.png`) and one of the open menu.

## Example (one test's shape)
```python
def test_R2_2(page):
    name = page.locator("#person-name").inner_text().strip()
    pos = page.locator("#person-pos").inner_text().strip()
    ok = name.startswith("范蠡") and pos == "1 / 4"
    return ok, f"name={name!r} pos={pos!r}"
```

## Standard — how it is judged
Then create `site/ancients/tests/fixtures/empty.html` (a blank HTML page) and run the script against it with
`--url file://…/fixtures/empty.html`. **Every test must FAIL** there (that is the red baseline). Put that run's full
output in your final message. If the browser cannot launch in your sandbox, say so plainly — never fake a result.
