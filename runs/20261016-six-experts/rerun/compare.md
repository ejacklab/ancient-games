# Dave, two category schemes — the same question, the same model (n=1 each)

Question: `../trial-question.md` (what a pre-flight check should verify in a brief). Dave on claude-opus-5-5 both times,
run through the runner. The only difference is the category scheme and the categories named.

| | Today's 6 (`guard/data/insight-categories.yaml`) | Linus's 4 + 2 flags (`insight-categories-4plus2.yaml`) |
|---|---|---|
| Categories named | spec, tool | instruction, tool |
| Sections loaded | 32.8 KB | 44.0 KB |
| Seconds | 502 | 433 |
| Answer size | 15.0 KB | 12.7 KB |
| Distinct insight ids cited | 13 | 13 |
| Shared ids | 10 of 13 (`F-7f938bdf`, `F-4cbb2f4b`, `F-05a1b440`, `F-173e0190`, `F-84636a96`, …) | same 10 |
| Only this one | `F-485505f6`, `F-60cad515`, `F-c60edad6` | `F-08cf4cc3`, `F-90389583`, `F-f09b058d` |
| `check` | pass (0 Dave failures) | pass (0 Dave failures) |
| The answer (quoted) | three rules: the engine's mode can't write a result file; a file outside the repo going to opencode; bigger than the engine has passed before (mcode) — each `proposed` until a replay over past briefs | two checks: outside the repo for opencode; missing, empty or not UTF-8 — shadow mode first, blocking only once "its false fails are fewer than the opencode answers it saves"; size and engine readiness left out |
| What Dave said about the named categories (quoted) | "The named categories (spec, tool) missed runs/20261016-integrate-r11-r13/insight…" | "The named categories (instruction, tool) missed the most relevant records: F-7f938bdf, F-08cf4cc3 and F-f09b058d are filed under **check**." |

## Reading (my reading; n=1 each, not judged blind)
- **The core didn't change.** Both put the same rule first: a path outside the repo going to opencode (`F-7f938bdf`).
  Both cite 13 ids, 10 of them shared.
- **Both schemes missed something, and Dave caught it both times.** Under 6, the `own-work` record of the refused
  file. Under 4 + 2, three `check` records, including `F-7f938bdf` itself, whose writer filed its Source as `check`.
  The "(c) both" picking (Dave also reads the index) is what saved both runs. Neither scheme made the named categories
  enough on their own.
- **The answers differ where the evidence differs.** The 4 + 2 Dave loaded more `instruction` sections and came out
  stricter: two checks, shadow mode first, and no size rule, because "this repo's own past files show those checks
  would either fail briefs that worked or catch no failure we have measured". The 6-category Dave kept a size rule for
  mcode. Which is better is **not judged**.
- **Cost:** 4 + 2 loaded 34% more text and finished 14% faster. One run each, so time differences are noise-level.

## What it does not show
Two runs, one question, one model, no blind judge. It shows the two schemes lead to the same core rule and the same
amount of insight use. It does not show that either one gives better answers.
