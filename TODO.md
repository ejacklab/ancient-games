# TODO

## Encode method 3.0 (understand the challenge) in intake.js

Added to the method 2026-10-01 (six whys + categorization added the same day); `intake.js` still embeds the
challenge verbatim and never asks for a restatement. Agreed shape (not scheduled):

- the step-1 readiness agent also writes the restatement (objective, in scope, out of scope, the six whys,
  categories inferred per `docs/TASK_TYPES.md`) into the `runs/<runId>/state.md` Restatement block;
- one `restatement` field in its structured output, and one fixed yes/no check in script code: it names an
  objective, an in-scope and an out-of-scope; a challenge that allows two readings stops at step 1 as an unclear
  spot of kind decision; the category is validated against the TASK_TYPES table and the facts (G2's shape);
- optionally run the design JSON through `.claude/skills/workflow-design/scripts/design_gate.py` at the check
  phase instead of re-implementing its rules;
- no new agent and no new loop;
- a sabotage case in `tests/workflows/intake_harness.mjs`: an empty or one-sided restatement must fail the check;
- then drop "Not yet encoded in `intake.js`" from `docs/WORKFLOW_DESIGN_METHOD.md` §3.0 and the n=0 row note in
  `docs/WORKFLOW_DESIGN_DIAGRAM.md` §6.

## Dispatcher layer (adopted and built 2026-10-03)

EJ adopted a friend's design idea: a layer, not the COO, spawns and supervises agents, so the method's prose rules
become code that cannot be skipped. It would join the scripts already built — `runlog.py` (two timers, events),
`validate_result.py` (pass-back), `harvest_run.py` (feedback), `quote_check.py` (explorer) — and enforce the caps
(5 roles per run, 3 at once) and the model check. (The executor-failure retry on a fallback was removed
2026-10-05: a failed engine blocks the node and reports.) Ancient Games (a
referee that decides how many agents and journals every decision) is the natural home. The COO keeps planning and
algorithm design. Design written 2026-10-03: `docs/DISPATCHER_DESIGN.md`. Built the same day as
`scripts/dispatch.py` (steps 1–4); open: a live canary per engine adapter, the first real run, and EJ's two
remaining decisions (§8).

## Guard: the read-missing hold blocks a correct `grep … > F; cat F`

A live bug: the guard's hooks run from this repo's source in every Claude Code session. Round 13's rule N3
(`.claude/skills/workflow-design/guard/SPEC.md`, `missingReads` in `guard/src/traps.ts`) skips an earlier segment
whole when its command is itself a reader (`cat`, `head`, `grep`, `sed`), so the `> F` of `grep … > F` is not counted
as making F, and a later `cat F` in the same command is denied although F will exist by then. Seen 2026-10-17
(F-cc665076; the command is in `runs/20261016-four-experts-what-counts-as-change/read-missing-false-hold.txt`).

**Fixed 2026-10-17** (run `runs/20261017-read-missing-false-hold/`, decided provisionally from the six experts in a
60-minute box; EJ accepts or declines): N3 now counts an earlier, finished segment's stdout redirect (`>`, `>>`, `&>`,
`&>>`) as making exactly that file, whatever its command word, when the file's folder exists. Still open from it:

- **A `cd` after `&&` is never seen as unknowable** (found by Dave, confirmed in the run's `cd-after-and.txt`):
  `mkdir -p a && cd $D && cat missing.md` is held, though N2 says a read after an unknowable `cd` is not checked. Each
  piece after `&&` in `coarsePieces` starts with `& `, so `unknownCdBefore` sees `&`, not `cd`. The same function
  feeds engine calls' `cwdKnown`. A false hold of its own, and a second cause of F-cc665076's.
- **N3's older text match lets reads through** (measured by 老子): `echo F; cat F` runs (an earlier segment only names
  F), and `grep x a >| other/linus.md; cat linus.md` runs (`>|` is split at its `|`, and the base name matches). All
  past holds were measured with this match, so a change needs its own replay.
- **`2> f`, `1> f` and `>& f` are not counted** as making `f`, though the shell creates it (Linus and Dave would
  count `2>`; 0 of 1,873 past commands need it). The next step if one is seen held: a `writes` field in `shellWords`.
- **The new exemption's known misses** (the dsh review, `runs/20261017-read-missing-false-hold/review-answers.md`),
  each rare and written into SPEC N3: a writer in a `|&` pipeline (`tokenize` splits `|&`), a writer in a pipeline
  sent to the background (only the last segment is marked), and a target the shell cannot write (`f/`, `absent/../f`,
  a parent that is a file — the folder is tested after `path.resolve` and not as a directory). Each fix needs its
  own crossed tests.
- **Two pins test less than their names say:** the `||` and probe pins in both `round13-reader-writes-*.test.ts`
  files have their own writer, so those exemptions are never exercised there.
