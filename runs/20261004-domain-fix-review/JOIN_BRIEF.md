# Join brief — the chair reconciles three expert surveys

You are the **chair** of this review. Three 孫子兵法 and game-strategy experts surveyed the algorithm's 45 open issues
independently and blind; you now reconcile them into one file. You did not write any of the three, and you must not
treat any of them as privileged — **including the one from your own engine.**

## Read

- `runs/20261004-defect-register.md` — the 45 issues in 8 areas. The ground truth for what exists.
- `runs/20261004-open-defects.md` — what is already fixed, partial or addressed. **Do not put a fixed item on the
  fix list.** Two are marked FIXED and one ADDRESSED; an expert that proposes one of those has made an error you
  should catch rather than inherit.
- `runs/20261004-domain-fix-review/surveys/areas-claude-opus-5-5.md`
- `runs/20261004-domain-fix-review/surveys/areas-minimax-m3.1-flash.md`
- `runs/20261004-domain-fix-review/surveys/areas-deepseek-v4-pro.md`

All three passed `areas-survey.py`: 8 areas, 45 ids each, verdicts from the fixed vocabulary. Their *judgement*
is not checked by anything — that is your job.

## Write `runs/20261004-domain-fix-review/FIX_PLAN.md`

**1. The consensus table.** One row per issue that any expert called DIRECT:

```
| issue | claude | minimax | deepseek | agreement | the fix, and the check that proves it |
```

`agreement` is `3/3`, `2/3` or `1/3`. Compute it; do not take it from anywhere else.

**2. The direct fix set.** Split into `3/3` and `2/3`. For each, one sentence: the file to edit, and the check that
would prove it. If two experts name *different* checks for the same fix, say so — that is a disagreement about the
fix, not about the verdict.

**3. The three where nobody agreed.** `5.2`, `6.4`, `8.1` — all three experts gave different verdicts. For each, say
which verdict you think is right and why. This is the part only a chair can do.

**4. The verdicts that are not DIRECT**, grouped by verdict, as a list of ids with the blocking reason. `SCHEMA` must
name the field; `DECISION` must name the choice EJ faces; `DOC` must name both files that disagree.

**5. What the three experts agreed on that I should be suspicious of.** Consensus is not evidence — if all three
said the same thing for the same weak reason, or all three missed something the register's own evidence implies, say
so. This section may be short; it may not be empty.

## Rules

- Write only `FIX_PLAN.md`. Nothing else.
- Do not add a 46th issue. The scope is the register's 45.
- A `DIRECT` with no named check becomes a `LATER` in your table, and you say you demoted it.
- Your classical source remains the four files in `docs/research/20261004-sunzi/`; cite only lines there, with their
  Basis. You may also write without classical citation at all — this is a reconciliation, and 孫子兵法 has nothing to
  say about, for example, which file holds a field name.
