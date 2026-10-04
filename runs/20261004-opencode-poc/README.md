# opencode + MiniMax-M3.1-Flash-Preview — what it is actually good at

POC run, 2026-10-04. Every claim below is a check that can fail (`check.py`), not an impression. **19/19 checks
pass.**

- **Tool:** `opencode` 1.18.34 (`/home/smoke01/.opencode/bin/opencode`)
- **Model:** `minimax-coding-plan/MiniMax-M3.1-Flash-Preview` — provider-namespaced, released 2026-09-27
- **Cost:** `cost: 0` under the coding plan; the account's other providers are separate
- **Catalog facts** (`~/.cache/opencode/models.json`): 1,000,000-token context, 512,000-token output, reasoning,
  tool calls, modalities in text + image + **video**

## How to call it (both traps verified, both silent)

```bash
opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build "<message>"
opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan  "<message>"   # read-only
```

1. **The message must come before any `--file=`.** `-f` is a greedy array option that swallows the next
   positional, so a file-first call makes opencode read the *prompt* as the attachment path and fail with
   `File not found: <the prompt>`. Verified both ways against a one-line file: message-first returned the secret,
   file-first did not.
2. **An attachment it cannot read makes it exit 1 even when the task succeeds.** See P4.
3. The answer is on **stdout**; the `> build · MiniMax-…` banner and all ANSI go to **stderr**, so stdout is clean.
   `--format json` emits one JSON event per line instead (see the cost note below).

The plain `minimax/` API-key provider **500s** on this id — its catalog stops at `MiniMax-M3`. The model is only
served under the `*-coding-plan` providers.

## The POCs

| # | What was tested | Check | Time | Result |
|---|---|---|---|---|
| P1 | Frontend: one self-contained HTML page, 6 requirements (3 ARIA tabs in vanilla JS, inline SVG bar chart, `prefers-color-scheme` dark mode, viewport meta, no network, < 12 KB) | 9 mechanical checks + rendered in Chrome | 29 s | **9/9**, 6,134 bytes |
| P2 | Long context: 787,839 chars (~197k tokens) of synthetic records with three access codes at 5%, 51% and 95% depth | all three codes + their sum | **14 s** | **4/4** — 481207, 739164, 205938, sum 1426309, all exact |
| P3 | Vision: a labelled bar chart PNG | read bar C and name the tallest | 5 s | **2/2** — `C = 83`, `HIGHEST = C` |
| P4 | Video: three frames counting 7, 14, 21 | the three numbers in order | 21 s | **1/1** — `7, 14, 21`, via a workaround (below) |
| P5 | Agentic: a repo whose pytest suite fails (`return out - 1`) | the tests pass afterwards | 20 s | **2/2** — found `calc.py:6`, removed it, 3 tests pass |
| P6 | Read-only enforcement: `--agent plan` asked to write a file | no file is created | 6 s | **1/1** — refused: *"plan mode is active, so this session is read-only"* |

Rendered evidence for P1: `p1_light.png`, `p1_dark.png` (the two themes differ across the whole canvas) and
`p1_datatab.png` (the Data tab, chart drawn by the page's own click handler). The page's prose computed the series
correctly — *"Total volume is 232 units, with channel C accounting for the largest share"* — 12+47+83+29+61 = 232.

## What it is measurably good at

1. **Frontend/UI from one prompt.** The strongest result. It produced a clean, coherent, self-contained page with
   correct ARIA tabs, a real SVG chart (gridlines, axis ticks, value labels, correct proportions), a dark theme and
   no external requests — in 29 seconds. This matches the marketing claim in the Chinese coverage, and here it is
   measured rather than asserted.
2. **Long-context retrieval, fast.** Three needles across 197k tokens, including the sum, in **14 seconds** and
   exactly right. This is the cheapest strong result in the set and the one most likely to change routing.
3. **Agentic fixing with real diagnosis.** P5 was not a description: it read, located the bug at a specific line,
   edited, and the objective check passed.
4. **Enforced read-only mode.** `--agent plan` refuses writes and says why — which is what the engine adapter needs
   for read-only nodes.

## Limits, all measured

- **Video is not readable.** The catalog advertises video input, but opencode's read path answers
  `Error: Cannot read binary file: …mp4`. What actually happened in P4 is the interesting part: the model ran
  `ffprobe`, then `ffmpeg -vsync 0` to extract frames to `/tmp/opencode/p4f/`, read the PNGs, and answered
  correctly. So video works *through the model's own tool use*, not through the interface.
- **It exits 1 when an attachment cannot be read — even on success.** P4 answered correctly and still returned 1,
  reproducibly 2/2. `dispatch.py` classifies a non-zero exit as an executor failure *before parsing stdout*, so a
  node that attaches such a file would be marked failed and rerun on a fallback. The engine adapter therefore
  emits no `-f` at all.
- **The chart's y-axis overshoots.** Ticks stop at 80 while the tallest bar is 83, so it breaks the top gridline.
  Small, but it is the kind of thing a careful reader notices.
- **No model id in the JSON events.** `--format json` gives `step_start` / `text` / `step_finish` and a
  `sessionID`, but nothing naming the model, so the engine-reported model check cannot be done on stdout. The
  banner on stderr carries it.
- **The online docs do not match this version.** The non-interactive-mode page describes `opencode -p "…"` with
  `-f` meaning *output-format*; 1.18.34 uses the `run` subcommand where `-f` means *file to attach*. Another
  instance of the bundled/stale-client trap, this time in documentation.

## Follow-up worth taking

`--format json`'s `step_finish` event carries real accounting:

```json
"tokens": {"total": 12382, "input": 5512, "output": 4, "reasoning": 0, "cache": {"write": 0, "read": 6866}},
"cost": 0
```

That is a **better cost source than any engine currently wired in** — the ledger's Actual cost column says "not
instrumented" for the DSH runs precisely because nothing reports this. opencode's sessions live in
`~/.local/share/opencode/opencode.db` (SQLite, which `harvest_run.py` could read with stdlib only). Not built
here; recorded because it closes a gap this project has been working around by hand.

## Reproducing

```bash
python3 make_inputs.py      # the ~197k-token record file, the chart, the video, the buggy repo
./run_poc.sh                # P1 and P6 (the rest need the flag order fixed, see run_poc_rest2.sh)
./run_poc_rest2.sh          # P2, P3, P4
python3 check.py            # 19 mechanical checks; exit 1 if any fails
```

`p2_records.txt` is not tracked (see `.gitignore`): it is 772 KB of generated filler and
`make_inputs.py` recreates it. Everything else here, including the failures, is committed.

`run_poc.sh` and `run_poc_rest.sh` are kept as they were run, including their failures: the first pass failed P2,
P3 and P4 on `-f` argument ordering, which is how that trap was found.
