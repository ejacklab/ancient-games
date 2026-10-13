# Brief — read two requirements, one round

You are one of four independent readers. You do not see the other readers' work.

## What you read

Two requirements in `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md` (a project-memory
design, accepted by its owner EJ; read the whole file for context):

- **W5.3** (under "Write", W5 "When to write") and its part of W5's **Fails if** line.
- **Rd5.3** (under "Read", Rd5 "Check before acting") and Rd5's **Fails if** line.

Also read the vision: `/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md`.

## Where the words came from

Both were written by the COO (Claude) on 2026-10-12, after EJ removed a drift-check script and a background subagent
from the design. EJ's own words:
- On W5.3: *"memory is very simple, when we put details says we decided to build soemthing. means it is a starting.
  when done, you put the time and results, test reuslt those into your memory, that means comeplte right?"* and, on
  its check: *"ok make it judged"*.
- On Rd5.3: the removed subagent rule was *"When a decision or fact no longer matches the code, the background
  subagent reports it to EJ and does not edit it"*. EJ agreed to it becoming "whoever reads a decision checks it
  against the code, and reports a mismatch" (*"ok remove both and update the doc"*).

Everything else in the two requirements is the COO's wording.

## Your task

For **each** of the two requirements:

1. Run the eight requirement-quality questions in `/home/smoke01/.agents/skills/requirement-check/SKILL.md` (read it).
   Say pass or FAIL for each, with one line why.
2. Find conflicts with the rest of the design. In particular, compare with W4.1 (anyone may change any entry),
   K1.1 (change the decision first, then the code), Rd5.1 and the vision. For each conflict, give a concrete case.
3. Find a concrete case that the requirement or its check gets wrong: it fails when it should pass, or passes when it
   should fail.
4. Mark anything the COO added beyond EJ's words that EJ should confirm.

Rules:
- Do not fill a gap with your own value. If a unit, a threshold or a rule is missing, write it as a question for EJ.
- If something is fine, say so. Do not invent problems.
- If a fix is obvious, give it in one line; do not rewrite the requirement.
- Read only; do not change any file.

## Output — one markdown report

```
# Reading W5.3 and Rd5.3 (<your engine name>)

## W5.3
| question | pass / FAIL | why |
(the eight)
Conflicts: …
Wrong case: …
COO additions for EJ to confirm: …

## Rd5.3
(same four parts)

## Questions for EJ
Numbered, one line each, only ones that change the requirement.
```

The launcher tells you your engine name and where the report goes.
