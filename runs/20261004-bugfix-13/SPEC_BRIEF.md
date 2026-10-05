# Spec brief — the 13 programming bugs

You are writing the **specification**, not the fix. Two builders implement from your spec; a verifier then tries to
prove their tests cannot fail. A vague spec becomes a vague fix and a test that passes both ways, so precision here
is the whole job.

## The bugs, and what "programming bug" means

`runs/20261004-defect-register.md` holds 45 issues. **13 are programming bugs** — the code does not do what the
design says — as opposed to *gaps* (the design never says) and *drift* (two documents disagree). Your scope is the
13, and nothing else:

| # | bug | file |
|---|---|---|
| 1.4 | `pattern` is parsed from every category row and used 0 times | `design_gate.py` |
| 1.5 | G2 reads `builds`/`touched_paths` from the design itself — half fixed, the self-reference remains | `design_gate.py` |
| 1.6 | loop rules fire only if a `loop` object already exists | `design_gate.py` |
| 2.5 | published accuracies had no denominator | already corrected in prose |
| 3.1 | `check_blueprint` can never fail: an existing dir is always VERIFIED | `readiness.py` |
| 3.2 | absent and empty directories report `verified` | `readiness.py` |
| 3.3 | "N sections" counts every `.md`, not the blueprint's sections | `readiness.py` |
| 3.4 | `--require` passes a tool that is UNKNOWN rather than MISSING | `readiness.py` |
| 3.5 | `rc == 0` with output counts as verified models; a non-object `model` raises `AttributeError` | `readiness.py` |
| 7.1 | dispatches readiness before method 3.0, skipping the restatement and tiny test | `intake.js` |
| 7.2 | its only baseline is a `git status` snapshot, not the test command and its output | `intake.js` |
| 7.3 | refuses any loop exit that does not mention "unclear" or "EJ" | `intake.js` |
| 7.4 | filed against the wrong file; the emitter was `corpus_check.py`/`test_task_types.py`, already fixed | — |

`3.1`, `3.2`, `3.3`, `3.4` and `3.5` are already marked PASS in the verifier's report at
`runs/20261004-domain-fix-review/VERIFICATION.md` — read its §1 table, which names the existing test that must flip
for each. **Those five are the ready set.** `1.4`, `1.5`, `1.6`, `7.1`, `7.2`, `7.3` are the ones whose checks the
verifier rejected; for those you must *design the check*, because that is what was missing.

## Read

- `runs/20261004-defect-register.md` §1, §2, §3, §7 — the bugs and the evidence each was found from.
- `runs/20261004-domain-fix-review/VERIFICATION.md` §1 — what the verifier already accepted and rejected.
- `runs/20261004-domain-fix-review/FIX_PLAN.md` §2–§3 — what the three experts proposed, including where they
  disagreed.
- The code: `.claude/skills/workflow-design/scripts/readiness.py`, `design_gate.py`, `.claude/workflows/intake.js`.
- The existing tests, so you reuse their style and helpers: `tests/test_readiness.py`, `tests/test_task_types.py`.

## Write `runs/20261004-bugfix-13/FIX_SPEC.md`

One block per bug, in register order:

```
### <id> — <one line>
- **Intended behaviour**: what must be true after the fix, stated so it could be false. Quote the method or the
  table line it comes from where one exists, with the file and line.
- **The edit**: the function and the condition to change. One or two sentences — precise enough that two builders
  make the same change, not so prescriptive that you are writing the code.
- **The test**: the file, the test name, and the assertion. It MUST fail against the current file and pass after
  the fix. Say which existing test flips, or that a new one is needed and what it asserts.
- **Risk**: what else this edit could break. Name the test that would catch it.
```

Then:

```
## Blocked, and why
Bugs that cannot be fixed without a decision EJ has not made, with the decision named. 7.2 depends on 5.1
(a DECISION, not a bug) — say so if that is what you find rather than inventing a fix.
```

```
## The order to build them in
Which bugs share a file and should be fixed together, and which must come first because another depends on it.
```

## Rules

- Write only `FIX_SPEC.md`. Change no code.
- **Do not specify a fix whose test would pass before the fix.** That is the defect the verifier is looking for, and
  a spec that asks for one is worse than no spec. If you cannot find a test that fails on the current code, say the
  bug is not yet checkable and put it under "Blocked".
- 13 blocks is the target. If two bugs are one change, say so and give one block.
