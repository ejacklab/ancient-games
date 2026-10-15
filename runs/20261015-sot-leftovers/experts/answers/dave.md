# Dave — the unknowns in the item-10 leftovers: smallest test, prediction, stop

## Answer
Only one spot, U4, is of kind *unknown*, and I agree it stays out of this run (backlog). If EJ ever brings it in, the smallest test is a sentinel-file read on one engine (agy) with a control file. For the four decisions (U1, U2, U3, U5) I run no test, because EJ decides them. Two of them can use data that already exists, though: one shell command is already enough to inform U1, and U5's only guard is the COO's path check, which has to be shown able to fail. I raise two new spots, N1 (the test baseline is compared by count) and N2 (the review rests on a single plant). Both cost almost nothing to fix.

| id | Kind | My verdict |
|---|---|---|
| U4 | unknown | Out of scope, backlog. Experiment if brought in: below. Prediction: below. Stop: one run per file size on one engine. Repeats (n) are EJ's call and left open. |
| U1 | decision | EJ decides. Existing data (my #5): in this repo's git history (293 commits, 2026-09-07 to today) there is **1 rename** (`R100 .claude/skills/workflow-design/scripts/code_graph.py → code_graph/code_graph.py`, 2026-10-07) and **1 deletion**, against 2,882 files added. So in this repo a stale `covers` path would be rare. That does **not** show the rate in other projects, and the design is meant for any project. n=1 repo. |
| U2 | decision | EJ decides. No experiment applies. |
| U3 | decision | EJ decides. My reading: while U4 is unmeasured, keeping the example limit is the small, reversible choice (my #8). Building limits-from-a-file before anyone has a measured limit to put in that file adds machinery with nothing to feed it. |
| U5 | decision | EJ decides. Fact checked: the YAML build script's "links resolve" covers **requirement ids only**. `links()` matches `REF` patterns in `text` and `fails_if` against known ids (`build_requirements.py:352-360`) and never checks a file path. So the COO's path check is the **only** guard on L3. It must be shown to fail on a path broken on purpose before P2. The design already plans this, and it must happen, not be assumed. |
| N1 (new) | unknown | Does the test baseline stay stable while another session edits skills? (git status shows `.claude/skills/requirement-check/SKILL.md` and `skills/requirement-check/SKILL.md` modified.) Experiment: at P2 start, run `env -u NO_COLOR python3 -m pytest -q` and record the **id** of the failing test, not just "1 failing". Do the same at P4 and compare by id. Prediction: the same single id, 993 passed. Stop: one run at each end. If they differ, look at the diff outside the three design files before calling the baseline changed. |
| N2 (new) | unknown | Does one planted contradiction found by P3 show the review is sound? It shows the reviewer found **one** contradiction of the planted kind. That is n=1, and the COO wrote both the edits and the plant. Whether to add a second plant or a control run is EJ's call, and the threshold is left open. |

## How I decided
1. My #1: for each spot I first asked what observation would settle it. Only U4 and my N1/N2 can be settled by observation. U1, U2, U3 and U5 are settled by EJ's choice, so for those I offer data, not an experiment.
2. My #5: before proposing anything new, I looked for data already in hand. For U1, git history is a free proxy for how often a `covers` path goes stale. I ran it: 1 rename and 1 deletion in 293 commits. It shows rarity *here*. It does not show other projects' rates or whether a stale path ever misleads an agent. No `entries/` folder exists yet, so there is no direct data on stale `covers`.
3. My #2: the rename count and the build script read cost less than debating them, so I ran them instead of guessing. The second one turned up the U5 fact: the build script never checks file paths.
4. My #3, for U4 if it is brought in: the prediction is written now, before any run. Metric: which sentinels the engine reports. Expected (my reading, n=0): agy reports a sentinel placed at about 13,000 bytes, which follows the 24,000-bytes-per-rule-file reading in `CACHES.md` (CX, official page), and misses one at about 25,000 bytes. If it misses the 13,000-byte sentinel, the "12,000 characters" report (W-4) wins. The stop date is EJ's.
5. My #4: the U4 experiment needs a control. Give the same sentinels in a file well under any limit (e.g. 2,000 bytes). If the engine misses sentinels there, the method is broken, not the limit, and the run says nothing about limits. For N2, the leftovers L1–L5 are known positives in the **pre-edit** text, so a reviewer run on the old text is a natural control. I leave to EJ whether that run is worth its cost.
6. My #8: the U4 experiment uses one engine and a temporary file outside the design, so it is reversible and changes nothing in this run's scope. Spreading it to other engines comes only after it works on one. For U3, the same rule favours keeping the example.
7. My #6 and #7: I looked for a living-system parallel to U1, where a claim never changes but its labels may. A genome's sequence is fixed while its epigenetic marks change. The key condition differs: an epigenetic mark changes *how* the sequence is used, while a `covers` path changes *what the claim is about*. So I dropped the analogy. It adds no test.
8. My #9 and #10: the U1 data is reported as a weak result (n=1 repo, a proxy rather than the thing itself). The same goes for N2: one found plant is a hint, not a proof.

## What I need to know
- U1: will EJ judge from this repo's rate, or do they want the rate in a code-heavy project? If the latter, the git command can be run on another repo EJ names. Under EJ's private-work-code rule, that is only with EJ's permission and only on a repo they choose.
- U4: is it brought into any run at all, and with how many repeats per size? That is EJ's threshold and is left open.
- N2: is one plant enough for EJ, or do they want a second plant or the pre-edit control run? If one is enough, P3 stays as designed.
- U5: will the design files always travel together into another project? If not, relative paths to `CACHES.md` will dangle there, and the path check in *this* repo cannot see that.

## Costs and risks
- U1 data (my #5, #10): cost already paid, one command. Risk: reading "rare here" as "rare everywhere". A code repo with frequent refactors could be quite different.
- U3 keep-the-example (my #8): costs nothing now. Risk: the example (200 lines / 24,000 bytes) is above agy's possible 12,000-character limit (W-4), so `INDEX.md` could pass the tool and still be cut off for agy until U4 is measured.
- U4 experiment (my #3, #4): about two engine calls and two small temp files. Risk: agy headless traps (soft-denied reads give exit 0 and empty output), so an empty reply must count as a failed run, not as "saw nothing". Also, one engine's result says nothing about Claude Code, Qwen or the others.
- U5 path check (my #2): costs one deliberate wrong path and one run. Risk if skipped: L3 passes on a check that cannot fail, because the build script will pass whatever the paths say.
- N1 (my #4): about one pytest run more than planned. Risk if skipped: another session's skill edit changes the failing test, the count still reads "1 failing", and the baseline looks unchanged when it is not.
- N2 (my #10): a second plant or control costs one more reviewer run (about 40–80k tokens, *not measured*, from the design). Risk if skipped: one found plant gets reported as "the review is sound".

## How we would know I was right
- U5: before P2, the path check fails on a deliberately broken path, and after the L3 edit it passes on the real ones. If it passes on the broken path, my verdict on how much it matters holds and the check must be rewritten.
- N1: the failing test id recorded at P2 start and at P4 is the same. If it differs, the by-id comparison caught what a count would have missed.
- U4, if run: the agy sentinel results match or contradict the prediction written in step 4 above, and the control file's sentinels are all reported. Either result is reported with the same weight (my #9).
- U1: if EJ allows U1's change, then once a project builds up entries, the count of `changed:` lines touching `covers`, compared with whole-entry supersessions done only to fix a path, shows whether the cost I estimated from this repo held.
