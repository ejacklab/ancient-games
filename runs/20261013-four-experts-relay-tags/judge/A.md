# Proposal A

I'd keep the four lower-case tags, `verified`, `reported`, `unproven` and `unknown`, and give them new definitions. Each tag should answer one question: how far along the chain of sources did the researcher get, and what was there? The single definition goes in `docs/workflow-templates/research-file.md`, and every other file points to it. `INFERRED` and `GAP` should stop being trust tags. An inference belongs in the answer and must cite the finding ids it rests on. A gap is an `unknown` row, plus a line in the Gaps section. The other two sets (`read`/`ran` for the explorer, and *quoted* / *my reading* / *not measured* for the main agent) stay separate.

**The proposed tags.** A researcher picks a tag by asking two questions in order. First: did I read the primary source? Second: does that source *show* the claim as I worded it, or does it only state it?

| Tag | One-line definition |
|---|---|
| `verified` | I read the primary source, and it shows the claim as worded. For a claim like "V states X", the statement itself is the evidence. For a claim like "X is true", the data, method, code or run must be shown. |
| `unproven` | I read the primary source, and it asserts the claim but shows no evidence for it. |
| `reported` | I saw the claim only in a secondary source that passes it on. I did not read the primary. |
| `unknown` | I looked and could not settle it: nothing was found, or the sources I read do not decide it. The Gaps section records what I searched and where. |

**When two tags seem to fit.** The claim is probably two claims, so split it into rows that each take one tag. For example, "Vendor V states its system is 60% faster" (`verified`) and "V's system is 60% faster" (`unproven`). If a row really cannot be split, it takes the weaker tag, in the order `verified` > `reported` > `unproven` > `unknown`. A tag is never raised later unless the primary source is read again. When sources disagree, write both rows; don't average them (house rule).

**Files that change** (one change, done all at once):
1. `docs/workflow-templates/research-file.md` holds the single copy: the four definitions, the two-question test, the rule for when two tags fit, and where inferences and gaps go. Through its link it is also what the skill reads.
2. `docs/TASK_TYPES.md`, the `research and reports` row. Replace "a CONFIRMED/INFERRED/GAP/UNPROVEN label" with "a label from `docs/workflow-templates/research-file.md`". I grepped `design_gate.py` and it does not parse that wording.
3. `docs/FEEDBACK_TEMPLATES.md`: rows 9 and 14, lines 47–49, 130 and 135.
   - `FACT` becomes one of the four tags.
   - `CONFIRMED` and `UNPROVEN` become the four tags.
   - `INFERRED` and `GAP` stay as kinds of line in the pass-back, not trust tags. `INFERRED` names the rows it follows from and can be no stronger than the weakest of them.
4. `.claude/agents/researcher.md`, lines 27, 38–40 and 49–50. Replace the copied definitions with a pointer. Fix the F7 example: it tags a vendor blog `reported` even though the blog *is* the primary source. Under the new definitions it becomes `verified` ("the vendor claims") or `unproven` (the performance claim itself).
5. `.claude/workflows/research-agent-memory.js`, lines 50 and 60–65. Keep the `LABELS` constant, but point its definition text to the template.
6. `skills/workflow-design/`: regenerate it with `tools/export_skills.py`; don't edit it by hand.
7. Not changed: the old `docs/research/*` findings files, and `runs/20261011-agent-memory-graph/check-findings.py`. Its tag list already matches.

**What the evidence-grading schemes say, and what applies here.**
- **The Admiralty code (NATO 6×6).** It rates the source A–F and the information 1–6 separately, and Wikipedia says *"Each descriptor is considered in isolation"*. Tag: `reported`. I read Wikipedia, not the NATO doctrine itself, which is not public.
  - What applies: reading a good source must not raise the claim's tag. The vendor's own page gives "V states X" as `verified`, but "X is true" stays `unproven`. Splitting rows does that job inside one column.
  - What does not apply yet: the second column for how reliable the source is.
  - Its "1 = confirmed by other sources" is cross-checking, and that is the referee's Corroborate stage, not a tag.
- **ICD 203 (US intelligence analysis standard).** It asks writers to *"Properly distinguish between underlying intelligence information and analysts' assumptions and judgements"*. Tag: `reported`. I read this on the ODNI objectivity page; the ICD 203 PDF downloaded but I could not extract its text. This is the reason `INFERRED` leaves the tag column: an inference is a judgement, not information.
- **GRADE (medical evidence grading).** It keeps how certain the evidence is apart from how strong the recommendation is, and its ratings start from the study design and move up or down from there. Tag: `reported`, from search summaries only. What applies: a tag grades a finding, never a decision. Decisions already go to `decisions.md`.
