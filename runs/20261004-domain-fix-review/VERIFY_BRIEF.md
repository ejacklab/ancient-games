# Verification brief — a blind re-read of the chair's plan

You are the **verifier**. You did not write the surveys and you did not write the plan. Your job is to find where the
plan is wrong, not to confirm it.

## Read

- `runs/20261004-defect-register.md` — the 45 issues in 8 areas, with the evidence each was found from.
- `runs/20261004-open-defects.md` — what is already fixed, partial or addressed.
- `runs/20261004-domain-fix-review/FIX_PLAN.md` — **the plan you are verifying.**
- The three surveys it reconciles: `surveys/areas-claude-opus-5-5.md`, `surveys/areas-minimax-m3.1-flash.md`,
  `surveys/areas-deepseek-v4-pro.md`.

## Check these, in order, and report only what FAILS

1. **Is every `DIRECT` checkable?** Take each fix the plan calls direct. Is there a named check, and is it a check
   that could actually fail — a test, a script, a mutation, a gate rule? A check that would pass either way is not a
   check.
2. **Is the plan faithful to the surveys?** For every issue, does the plan's `agreement` column match what the three
   surveys actually say? Spot-check at least the seven `3/3` rows and the three split rows by reading the surveys.
   The plan was written by an engine that also wrote one of the surveys; a quiet preference for its own is the
   failure mode to look for.
3. **Did anything get lost?** 45 issues exist. Are all 45 accounted for in the plan — in the direct set, or among
   the non-DIRECT verdicts with a blocking reason?
4. **Are the plan's three corrections true?** It claims (a) `7.4` was mis-filed in the register and its emitter was
   `tests/workflows/corpus_check.py:69`, already fixed; (b) the caps in `5.7` are enforced in `dispatch.py`, so the
   register's claim that they "exist only in the method" is wrong; (c) the SCHEMA verdict on `1.1`/`1.3`/`8.3`
   overstates the work because `intake.js`'s schema already carries `stop` and a baseline. Check each against the
   files. Say which are right and which are not.
5. **What did the plan miss?** Anything the register's own evidence implies that the plan does not address.

## Write `runs/20261004-domain-fix-review/VERIFICATION.md`

For each of the five checks: `PASS`, `FAIL` with the specific instance, or `CANNOT CHECK` with the reason. Then:

```
## The plan's weakest claim
The one thing in FIX_PLAN.md you would not act on without more evidence, and what would settle it.
```

```
## What I did not check
Be specific. A verification that claims to have checked everything is not credible.
```

## Rules

- Write only `VERIFICATION.md`. Change nothing else — not the plan, not the surveys, not the register.
- **Do not add findings of your own about the algorithm.** You are verifying the plan, not re-reviewing the
  algorithm. A new defect you notice goes in "what I did not check", not into a verdict.
- Your classical source, if you cite one at all, remains the four files in `docs/research/20261004-sunzi/`. This task
  is mostly arithmetic and reading; 孫子兵法 has little to say about it and you should not force it.
