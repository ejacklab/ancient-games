# Question

This is a relay. Earlier experts have written and improved a proposal, one at a time; you are step 5 of 5. Improve
the **same copy**: keep what is right, change what is wrong, add what is missing, remove what is more than needed.

The repo has several different sets of trust tags for research findings. They should be one set. The copy proposes
which set is official, where it lives, what each tag means, the rule for when two tags seem to fit, which files
change, and what happens to old files.

In your `## Answer` section: one or two sentences on what you changed, then a heading `### The copy` containing the
**complete** improved proposal — not a diff, not a list of edits. Under `## How I decided`, list each change as kept /
changed / added / removed, with the item that drove it. Do not search the web; work from the copy and the facts below.

# The current copy

**Status:** Proposal for EJ's decision; not measured (`n=0`). These are proposed SHOULD defaults, with any departure explained by the researcher. The definitions themselves are EJ's; a default may bend in a hard case with a written reason, but a definition may not. Track operational friction during initial use, but do not alter canonical definitions on an `n=1` basis; evaluate adjustments only after the same friction recurs across separate tasks. **Adoption waits on one reckoning:** re-tag the 143 rows of the five findings files in `runs/20261011-agent-memory-graph-r2/verify/sections/` (run 2 is the accepted run; run 1 was blocked at Sections and its five section findings files are not in the repo), writing each row's tag down before looking at its old one. A row that splits into two claims is the rule working, not the rule failing. The rule is not ready only if a row, after splitting, still stands between two tags — `reported` and `unproven` above all. Report the result as a number: how many of the 143 rows moved, and in which direction. This is a first tagging under the new rule, not an upgrade of old labels, so rows may move either way. Do not argue the number.

**Scope:** The researcher assigns one tag to each research finding. The tag describes the evidence available to the researcher for the finding's exact wording; it is neither a confidence score nor a declaration of universal truth. **Primary and secondary are relative to that exact wording, not to the source's reputation:** one document is primary evidence for the claim that it says what it says, and secondary for a claim about the world that it only reports. That is why the same blog can carry `verified` for one row and no support at all for the next.

**The four tags.** Each names one measure: the evidence in hand for the exact claim. The four are parallel answers to one question, not rungs of a ladder; their order is not their strength, and a fifth tag — source rank, say — is not added.

| Tag | Definition |
|---|---|
| `verified` | The supporting evidence itself — the primary document's own measurements, data, or wording — was inspected, and directly supports the exact claim within its stated scope, and the row shows what was inspected. Merely reading an assertion does not qualify. |
| `reported` | An account describes supporting evidence for the exact claim and points at it — a named benchmark, a citation, a method, figures — but that evidence has not been inspected. An account that only repeats the assertion, however it is attributed, is `unproven`. |
| `unproven` | The claim is asserted, and nothing beyond the assertion is present or described; the cited material offers no supporting evidence. |
| `unknown` | Supporting evidence exists but cannot be obtained or brought to bear on the claim, or the evidence conflicts and is unresolved. One tag serves both; the reason goes in the row, not in the vocabulary. |

**When two tags seem to fit:** First check whether the row contains two claims. Split a statement about what a source says from a statement about whether that assertion holds, then tag each claim separately, each with its own citation of the same passage.

For one claim, ask one question: what evidence is in hand for that exact wording? Source rank does not substitute for evidence, whether the asserting document is primary or secondary. What is in hand is one of four things:

- nothing beyond the assertion → `unproven`
- an account that points at evidence you have not inspected → `reported`
- the evidence itself, inspected and directly supporting the claim → `verified`
- evidence you cannot obtain or bring to bear, or that conflicts and is unresolved → `unknown`, and state the unresolved point

Write the finding so that one row fits; if you cannot, it is two findings. **Never upgrade a label in place.** A finding's label is fixed once assigned; when later investigation inspects primary evidence, record a new finding referencing the original rather than editing the earlier record.

**The row must show what was inspected.** A `verified` row carries in the row — not in a footnote — the wording, figure, or file:line that was inspected. If a reader cannot see from the claim and its row what was looked at, the row is two findings, or it is not `verified`.

For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim — the announcement's wording is the evidence for what it says. The performance claim itself is `unproven` if the announcement supplies no measurements.

`verified` does not imply independent replication. State whose evidence was inspected and the conditions it covers. A vendor's benchmark cannot establish performance outside its tested conditions.

**Other finding types:** `INFERRED` and `GAP` stop being alternatives in the trust-label field. Write researcher deductions as inference prose identifying their premise finding IDs and reasoning. Write unsuccessful searches as gap prose identifying the question, query, and places searched. A search that found nothing is a gap, not a tag: do not record absence as though it were evidence. An inference does not inherit `verified` from its premises; failure to find evidence does not establish that something does not exist. An inference or a gap is not a row in the findings table; it is prose, and it carries no trust tag.

When sources disagree, retain separate findings with their citations and tags. Describe the disagreement explicitly; do not average it away. An unresolved overall conclusion is `unknown`.

**One definition:** [RESEARCH_TAGS.md](file:///home/smoke01/dev/ancient-games/docs/RESEARCH_TAGS.md) is to be created as the single copy; it will hold these definitions, the selection rule, the examples, the historical-reading guidance, and two dates: the date it takes effect, and the date before which files carry the older meanings. That is the only new file. Other active documents link to it rather than restating the definitions. Only EJ changes the definitions.

**Files to change if EJ adopts the proposal:**

- `docs/RESEARCH_TAGS.md`: create it with the contents above.
- [research-file.md](file:///home/smoke01/dev/ancient-games/docs/workflow-templates/research-file.md): replace its local definitions with the canonical link; retain the findings table and clarify that bare primary assertions do not qualify for `verified`. Also change the digest's **Confidence** line, which currently counts by the old three labels — and the local list there already omits `unproven`, which is itself an argument for one copy.
- [TASK_TYPES.md](file:///home/smoke01/dev/ancient-games/docs/TASK_TYPES.md): replace `CONFIRMED/INFERRED/GAP/UNPROVEN` in the research check with the canonical link; preserve its citation requirements.
- [FEEDBACK_TEMPLATES.md](file:///home/smoke01/dev/ancient-games/docs/FEEDBACK_TEMPLATES.md): make both research and web-search summaries carry the finding's original ID and canonical tag. Keep inference, gap, and disagreement explanations as prose.
- [.claude/agents/researcher.md](file:///home/smoke01/dev/ancient-games/.claude/agents/researcher.md): update the draft to reference the canonical definition before adoption.

Only these change in the first pass; no historical run folder is edited, and the re-tag produces a count, not an edit. Any future findings check must accept the canonical four tags, must not demand a tag where inference or gap prose is written, and must fail a row that is neither tagged nor written as named prose — that blank middle is the failure that matters. Explorer's `read`/`ran` and the main agent's `quoted`/`my reading`/`not measured` stay separate: they measure what was done to the repo, and how a conclusion is handed to EJ, not the evidence in hand for a claim. There is nothing there to merge.

**Old files:** Preserve completed findings and their original labels. In particular, leave `runs/20261011-agent-memory-graph/check-findings.py` where it is, in the run-1 folder, and do not edit it; its `LABELS` tuple is a spelling check, and the canonical file, not the script, holds the meaning. Preserve run 2's five findings files unchanged, with their 2026-10-11 tags.

Do not automatically translate historical `FACT`, `CONFIRMED`, or even `verified` into the new meanings; read them under their original definitions. When reusing a historical finding, assess its evidence against the new definition and create a current finding referencing the original. Pass-back summaries retain existing tags; new evidence follows the no-upgrade rule above. The re-tag's numbers live in the canonical file's historical section, not in the run folders.

**Price:** Keeping the names requires readers to unlearn the older loose definition of `verified` (where reading any primary document sufficed). One measure means source reliability is not recorded separately; if it matters, it belongs in prose. Centralization requires working links, and preserving history means old and current meanings coexist across repository runs. The regex cost is close to already paid: across the 143 accepted rows the Label column carries only the four tags — 94 `verified`, 44 `reported`, 3 `unproven`, 2 `unknown` — and the gap and inference material is already prose under a `## Gaps` heading. What is genuinely new is the cost of the split: rows will lengthen, and the re-tag will show how many `verified` rows cannot show what was inspected.

# Facts (all read from the repo by the main agent on 2026-10-13)

## Where tags are defined today

1. `docs/workflow-templates/research-file.md` (written 2026-10-02, commit 7b66107) — the form the researcher fills in
   (FINDINGS.md table: id | Finding | Label | Source). Quoted:
   > `verified` = the primary file or document was read; `reported` = a secondary source; `unknown` = not settled.
   > Never upgrade a label. When sources disagree, give both rows.
2. `docs/TASK_TYPES.md` row `research and reports` (2026-10-02, commit bf6a6f8) — the table of task kinds with their
   check. Quoted: "every finding carries both-side citations and a CONFIRMED/INFERRED/GAP/UNPROVEN label; missing
   proof never reads as PASS".
3. `docs/FEEDBACK_TEMPLATES.md` — the short summary a worker passes back to the main agent (proposed, n=0):
   - `web search` pass-back: `FACT` / `INFERRED` / `GAP` lines plus a `Disputed:` line. Quoted:
     "INFERRED <claim> — <why it follows from the FACT lines>"; "GAP <asked fact> — not found; searched: <query, where>".
   - `research and reports` pass-back: `CONFIRMED | INFERRED | GAP | UNPROVEN`. Quoted: "`INFERRED` names the
     `CONFIRMED` rows it follows from; `GAP` names the query run and where."
4. `runs/20261011-agent-memory-graph/check-findings.py` (2026-10-11, uncommitted, written by Claude for one run) —
   a script that fails a findings file whose row has no year, no URL/file:line, or a tag outside
   `("verified", "reported", "unknown", "unproven")`. The research workflow of that run defined:
   "verified = the primary document was read; reported = a secondary source; unknown = not settled; unproven =
   claimed without evidence."
5. A draft Claude Code researcher subagent (`.claude/agents/researcher.md`, 2026-10-13, not yet adopted) copies the
   four lower-case tags.

## Related tag sets with a different job (not research findings — say if they should stay separate)

- Explorer (reads repo code): every behaviour claim is `read` (inferred from reading) or `ran` (confirmed by running).
- The main agent's conclusions to EJ: *quoted* (with id), *my reading*, or *not measured* (CLAUDE.md, 2026-10-11).

## How the tags are actually used (counts of tag words in existing findings files)

- 2026-10-02 mods-plugins: verified 49, reported 21, unknown 11, gap 2, confirmed 1
- 2026-10-02 whale-dolphin-hunting: reported 140, verified 42, unknown 24, inferred 5, unproven 5, disputed 3, fact 1
- 2026-10-02 workflow-feedback: verified 43, reported 27, unknown 8, gap 5, fact 2, confirmed 2
- 2026-10-03 jev: reported 23, unknown 2, verified 1
- 2026-10-05 requirement-statements: verified 13, gap 2, confirmed 2, fact 1
- 2026-10-11 agent-memory-graph runs 1 and 2 (10 files): only verified / reported / unknown / unproven; unproven used
  3 times in total. Run 2 was accepted by EJ.
(Counts are word counts over the whole file, so a few may be prose, not tags.)

## The problems already raised by an earlier review (2026-10-13, five reviewers)

- `reported` says *who* the source is (secondary); `unproven` says *whether evidence was shown*. Two different
  measures on one label. Example: a vendor blog says "our system is 60% faster" with no benchmark harness — it is
  both `reported`-ish and `unproven`, and nothing says which wins.
- One reviewer: the narrow claim "the vendor says X" is `verified` (the primary was read); the performance claim
  itself is not established.
- `INFERRED` (a conclusion drawn from other findings) and `GAP` (looked for, not found) are different kinds of thing
  from source-trust tags.
- House rules: one copy of a definition, others point to it; a label is never upgraded; when sources disagree give
  both rows, never average; EJ decides — you advise.
