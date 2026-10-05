# Build brief

You are implementing part of a fix specification. The spec is
`runs/20261004-bugfix-13/FIX_SPEC.md`. Implement **only the bugs assigned to you** below; another builder has the
rest, and duplicating their work will collide.

## Your scope

bug 3.1, 3.2, 3.3, 3.4, 3.5 — all in .claude/skills/workflow-design/scripts/readiness.py, with tests in tests/test_readiness.py

## How to work

1. Read the spec block for each of your bugs, and the code it names. The spec gives the intended behaviour, the
   edit and the test.
2. **Write the test first, and run it against the unmodified code.** It must FAIL. If it passes, your test is not
   testing the bug — fix the test, not the code, until it goes red. This is the discipline the whole exercise is
   about: a test that passes before the fix proves nothing.
3. Then make the edit and run the test again. It must pass.
4. Run the files' full test modules and the whole suite:
   `env -u NO_COLOR python3 -m pytest -q`
   Nothing else may break.
5. If the spec is wrong about something, say so in your reply rather than silently departing from it.

## Rules

- Touch **only** the files in your scope. Do not edit another builder's files, the spec, or the register.
- Do not weaken an existing test to make it pass. If an existing test asserts the buggy behaviour, that is expected
  — the spec names which ones must flip — and you update it to assert the corrected behaviour, saying so in your
  reply.
- Do not touch anything under `docs/research/` or `runs/` except to read.
- Keep the diff minimal. A fix that rewrites a function to change one condition is a worse fix than one that
  changes the condition.

## Reply with

Only: the bugs you fixed, the tests you added or flipped, and the exact command you ran to prove each test fails
before and passes after. If a test could not be made to fail first, say so plainly.
