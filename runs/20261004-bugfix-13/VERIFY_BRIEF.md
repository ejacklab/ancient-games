# Verify brief — prove each new test can actually fail

Two builders just implemented 9 programming bugs from `runs/20261004-bugfix-13/FIX_SPEC.md`. You are the verifier.
Your job is **not** to check whether the code looks right. It is to prove, one test at a time, that the test fails
when the fix is absent — because a test that passes either way is the exact defect this whole day has been about,
and a previous verifier found 7 of 13 proposed checks were of that kind.

## The method, and why not `git stash`

**`git stash` with no arguments reverts the new tests too**, and then you cannot run them. Stash the *source file*
only, keeping the tests:

```
git stash push -- .claude/skills/workflow-design/scripts/readiness.py
env -u NO_COLOR python3 -m pytest -q <the test the spec names>     # MUST FAIL
git stash pop
env -u NO_COLOR python3 -m pytest -q <the same test>               # MUST PASS
```

Do that once per bug, against the file that bug lives in. The spec names the test for each. Where a test is new,
confirm it is present before you stash and after you pop.

## What to write

`runs/20261004-bugfix-13/VERIFICATION.md`, with:

**1. The sabotage table.** One row per bug:

```
| bug | the test | fails without the fix? | passes with it? | how you reverted |
```

`fails without the fix?` is `YES`, `NO — passes either way` (the verdict that matters), or `COULD NOT RUN` with the
reason. A `NO` is a finding, not a formality: report it and say what the test would have to assert instead.

**2. The full suite**, before and after each pop: the command and the pass/fail count. Nothing else may break.

**3. The bugs that were not built** — `1.5` and `7.2` are Blocked, `2.5` and `7.4` were already fixed. Confirm from
the spec that each is genuinely out of scope, or say which is not.

**4. Any test that asserts the buggy behaviour was flipped rather than deleted.** A builder may update an existing
test that encoded the bug — the spec names the ones that must flip — but deleting an assertion to make a suite green
is the failure to look for. Diff the test files and say what changed.

```
## What I could not verify
Be specific. You cannot prove a negative by assertion.
```

## Rules

- **Change no source file.** Stash and pop only; leave the tree exactly as you found it. If a pop conflicts, stop and
  report rather than resolving it yourself.
- Do not fix anything you find, however small. Report it.
- Do not run anything that needs the network.
