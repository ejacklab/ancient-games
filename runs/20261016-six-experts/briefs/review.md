# Brief — review (read-only)

You review a change in this repository (the current folder is its root). Do not change any file. Your final message is
the review; it will be saved by the caller.

## The change
`runs/20261016-six-experts/review-diff.patch` — the diff of plan B (`runs/20261016-six-experts/plan.md`):
- the four-experts skill renamed six-experts; a new plain control seat "Dario" (brief `assets/brief-plain.md`);
- the expert Dave loads past insights before answering (`insight_load`, `--insights`), and `check` makes him cite them;
- Dave and Dario run on the same Claude model (`SEAT_MODEL`); two opencode experts never run at once (`waiting`);
- the guard's new `insight index` / `insight show` (`src/insight-index.ts`, SPEC "Round 11") with six categories as data
  (`data/insight-categories.yaml`) and a per-section `Category:` override.
Decisions behind it: `runs/20261016-six-experts/state.md` (D1–D3).

## Find defects
Code that does not do what the skill text, the plan or the SPEC says; a check that cannot fail; a crash path; text
from insight sections reaching the index (it must not); Dario's brief carrying anything beyond the question and the
answer's shape; Dave and Dario not getting the same model and tools; a way two opencode experts could still overlap;
a reference still pointing at the old four-experts name in live code.

## Return (no preamble)
`status: done`, then one numbered finding per defect — severity (high / medium / low), file:line (from the patch), what
is wrong, the input that shows it, the fix you suggest. End with "Checked and found nothing" for each area above where
that is true.
