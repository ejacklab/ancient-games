# Four experts and Dave — one official set of research trust tags

Asked 2026-10-13. Question: `question.md`. Answers: `answers/<id>.md`. Compared by the main agent (Claude); lines
labelled *quoted*, *my reading* or *verified* (I re-read what it rests on).

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Tags | `observed / reported / inferred / unknown` | `verified / unproven / reported / unknown` | `verified / reported / inferred / unknown` | `shown / reported / inferred / absent` | two columns — Read: `primary / secondary`; Backing: `confirmed / shown / claimed / unknown` |
| Columns | one tag, plus primary/secondary noted beside it | one | one | one | two |
| Home | new `docs/RESEARCH_FINDING_LABELS.md` | `research-file.md` | new `docs/EVIDENCE_LABELS.md` (or the template) | `research-file.md` | `research-file.md` |
| `unproven` | becomes a written limitation on a `reported` row | kept: primary read, no evidence shown | folded into `unknown` | folded into `reported` | renamed `claimed` |
| `INFERRED` | a tag | not a tag: goes in the answer, cites ids | a tag | a tag | not a tag: its own list |
| `GAP` | → `unknown` | → `unknown` + Gaps line | → `unknown` | → `absent` | its own list |
| Old files | leave as they are | leave as they are | retag them | leave; a read-map for old words | leave; a read-map for old words |
| Main items | #9 #10 #2 #7 #13 | #5 #14 #12 #3 #7 #18 | #1 #11 #12 #16 #6 | #1 #6 #4 #14 #17 | #1 #5 #6 #7 #3 #4 #8 |

## Where they agree

1. **One copy, everything else points to it.** All five.
2. **Split the vendor-blog case into two claims.** All five: "the vendor says X" is one finding (first-hand), "X is
   true" is another (not backed). The tie is a sign the row holds two claims.
3. **Source and information are separate questions.** All five cite the Admiralty code: *"Each descriptor is
   considered in isolation"* (*quoted* from Wikipedia by Dave, 范蠡, 孫子; Linus via WADA guidance).
4. **Keep the explorer's `read`/`ran` and the main agent's *quoted / my reading / not measured* separate** — they
   tag different things made by different people. All five.
5. **`Disputed` is not a tag**: disagreement stays as two rows. All who mention it.
6. **Do not import a source-reliability grade (A–F)**: the repo has no track record per source. Dave, 范蠡, 孫子.
7. **Test it before spreading it**: two blind labellers tag the same ~30 rows under the old and new definitions; the
   new set should agree more. Dave, 范蠡, Linus, 孫子 (老子: the worked vendor case).

## The evidence the problem is real (verified)

`docs/research/20261011-agent-memory-graph-r2/INDEX.md:255–256`: the same Zep paper's numbers are `verified` in s2-F2
and `reported` in s5-F18; Mem0's are `verified` in s1-F3 and `reported` in s4-F19 and s5-F17. The index's own reason:
*"The two sections applied different label conventions."* Found by Dave.

## Where they disagree

**A. One column or two.** Four say one tag, and split the row when two fit. Dave: two columns, *"each axis answers
only one question, so a tag from one axis never competes with a tag from the other"*. 范蠡 against a second
column now: *"A 6×6 grid now would be forcing growth before its time."*

**B. Keep `verified`, or rename.** 范蠡 and 孫子 keep it (continuity with ~hundreds of uses). Linus (`observed`) and
老子 (`shown`) rename. 范蠡 names the risk of keeping it: *"`verified` can still be read as 'true'."*

**C. What happens to "claimed with no evidence" (`unproven`).** 范蠡 keeps it as a tag; Dave keeps it as `claimed`;
Linus and 老子 move it into `reported` with a note; 孫子 into `unknown`. 老子's cost: *"The alarm word disappears."*

**D. Is `inferred` a tag?** Linus, 孫子, 老子: yes. 范蠡 and Dave: no — an inference is a judgement, not a finding
(范蠡 *quoting* ICD 203: *"Properly distinguish between underlying intelligence information and analysts'
assumptions and judgements"*).

**E. Retag old files?** 孫子 yes; the other four no.

## What each added

- **Linus** — the tag describes *how the researcher supports the exact claim*, *"not a ranking of truth or source reputation"*.
- **范蠡** — the two-question test, in order: did I read the primary? does it *show* the claim or only state it?
- **孫子** — the checker should read its tag list from the one definition file, so the rule is enforced, not remembered.
- **老子** — GRADE *"discourages 'modified GRADE approaches'"*: one system, used as published, is the point.
- **Dave** — the measured collision in the accepted run (above), and the fallback if the test fails: keep the four
  tags and add a one-line tie-break.

## What they need to know (merged, for EJ)

1. One tag column, or two (where the source came from + what backs the claim)?
2. Keep the word `verified`, or rename it?
3. Should "claimed but no evidence shown" keep its own tag?
4. Is an inference a tagged finding, or does it belong in the answer?
5. Old findings files: leave them, or retag?
6. (Dave) Does `confirmed` need a real re-run, or is an independent second source enough?

## Check

- `four_experts.py check` → `PASS: 5 answers, 0 failure(s)`; `--sabotage` → 2 failures. Written by Claude; checks
  structure and citations only, not whether the advice is good.
- Engines: Linus codex, 孫子 dsh, 老子 opencode (from `status.json`); 范蠡 and Dave as Claude subagents with web,
  saved by the main agent.
- Slips noticed (*my reading*): 孫子 calls `inferred` one of *"the repo's existing four labels"* — it is not in the
  lower-case set; and says nothing from run 2 disappears while folding `unproven` into `unknown`. 老子's file starts
  with a stray "I'll read the brief first."
