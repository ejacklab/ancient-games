# bridge — the evaluator's verdict reaches the guard (guard SPEC Round 19, V1–V5)

**status:** done

**one sentence:** `evaluation ingest <verdict.json> --run DIR [--session S]` turns each FAIL requirement into one
`found_by: evaluator` failure whose evidence holds the id and its group's FAIL repros, writes one line per UNKNOWN to
`DIR/evaluator-notes.md`, writes nothing for a PASS, records a verdict's bytes once, and says so in one line — so the
stop that ends the run asks for an insight of the FAIL (checked: `insight --session s1` lists it open).

**files changed**

- `.claude/skills/workflow-design/guard/src/evaluation.ts` (new, 216 lines) — `ingestVerdict(root, file, run, session, now)`,
  `EvaluationError`, `IngestResult`. Uses `appendFailure` / `newFailureId` / `writeEvidence` from `src/journal.ts`; the
  root comes from `guardRoot` in `cli.ts`, as `fail` does. A case joins a requirement's group when the case id is the
  group's name or starts with `<group>-`.
- `.claude/skills/workflow-design/guard/src/cli.ts` (+25 lines, no deletions) — `evaluationCommand`, the `evaluation`
  case in `run`, one USAGE line.
- `runs/20261017-evaluator-wiring/nodes/bridge.progress.md` (this run's progress), this file.

**the two commands' last lines**

- `cd .claude/skills/workflow-design/guard && bun test` → exit 0 — last line: `Ran 1524 tests across 37 files. [22.78s]`
  (0 fail; the 7 round19 tests included: `7 pass 0 fail`).
- `./node_modules/.bin/tsgo --noEmit -p .` → exit 0, no output (0 lines). Last line: none — the command prints nothing
  when it is clean.

**CONTRADICTS**

1. **The group→case join is not written down anywhere.** The SPEC says the evidence holds "the repro of every FAIL case
   of its group", and `tools/evaluator/verdict.py:256` joins a requirement to its cases by `case.case.startswith(group +
   "-F")`. The round19 test's fixture writes its FAIL case as `G1-c1` for group `G1` — no `F` — so the writer's own rule
   matches nothing there and V1's evidence assertion could not hold. I matched the prefix `<group>-` (which also covers
   the writer's `G1-F1`) and read that as the intended join; **EJ may want `verdict.py` and the SPEC to name the same
   prefix rule.** n=1 (one writer read, one fixture).
2. **Where the once-per-verdict key lives — my choice, not the SPEC's.** The brief says "once-per-verdict by a hash of
   the file's bytes" but the SPEC does not say where the hash is kept. `src/types.ts` is fixed, so no new journal record
   kind was available; the hashes go in a new guard-state file `.harness-guard/evaluations.jsonl` (one line per ingest:
   time, session, sha256 hex, file, run, counts), read back with M2's rule that a bad line is skipped and never thrown.
   The consequence to know: the key is the hash alone, so the **same bytes ingested under a second `--run` or a second
   `--session` records nothing** (verified by hand). No test covers the cross-run case.
3. **Two cases the SPEC does not name, where I had to choose.** (a) A requirement row with no `id` would make
   `validateFailure` reject the record (empty `input`), which the CLI would turn into exit 2; I put it in V4's existing
   `could not run` note class instead, so an unusable verdict is still exit 1 and no failure. (b) A FAIL requirement
   with an empty `reason` uses the SPEC's default `"the evaluator judged it FAIL"` (otherwise `validateFailure` rejects
   it); an **UNKNOWN** with an empty `reason` gets the line `- <id> · UNKNOWN` with no text invented for it. Both
   verified by hand, not by a test.
4. **`PASS` is counted as "neither FAIL nor UNKNOWN".** The SPEC's V5 line wants a PASS count but the fixture and the
   writer only ever write PASS/FAIL/UNKNOWN, so a third verdict value would be reported as a pass. Not contradicted by
   any source; a judgement.
5. **`--run` outside the root is a usage error (exit 2, nothing written).** The SPEC does not say; this follows
   `expect.ts`'s `declareRed` and `criteria new --out`, so the owner's notes cannot be written outside the project.

**checked beyond the tests** (scratch roots in `/tmp`, deleted): a FAIL with an empty reason is recorded with the
default reason rather than crashing `validateFailure`; a 210-char repro lands in the evidence as `[228 chars]` (the
guard's no-raw-content rule in `writeEvidence`) and the record stays valid; a second, different verdict file with the
same requirement id records a second failure (the hash is the key, not the id); the same bytes re-ingested under another
session records nothing and the UNKNOWN line stays single; `--run /tmp/elsewhere` exits 2 and creates nothing.

**not done / not verified:** `harness: "none"` and `engine: "none"` on the evaluator's records — honest (the CLI is not
a harness) but the SPEC does not name them. The real `verdict.json` from `build/evaluator` was not run through the
command; the fixture in the round19 test and one hand-written verdict were.