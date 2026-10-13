# Linus Torvalds — One set of research tags

## Answer

**My reading:** Keep `verified`, `reported`, `unknown`, and `unproven`, but define them against the exact claim and its supporting evidence; put their single definition in `docs/RESEARCH_TAGS.md`. This preserves familiar names while fixing their overlap, at the cost of changing what qualifies as `verified`.

### The copy

**Status:** Proposal for EJ’s decision; not measured (`n=0`). These are proposed SHOULD defaults, with any departure explained by the researcher. Revisit them after the first research task using them.

**Scope:** The researcher assigns one tag to each research finding. The tag describes the evidence available for the finding’s exact wording; it is neither a confidence score nor a declaration of universal truth.

| Tag | Definition |
|---|---|
| `verified` | The researcher inspected primary evidence that directly supports the exact claim within its stated scope; merely reading an assertion does not qualify. |
| `reported` | A secondary account describes supporting evidence for the exact claim, but the researcher has not inspected that primary evidence. |
| `unproven` | The claim is asserted, but inspection of the cited material finds no supporting evidence beyond assertion. |
| `unknown` | The question remains unresolved because evidence is unavailable, its bearing on the claim cannot be assessed, or conflicting evidence has not been resolved. |

**When two tags seem to fit:** First check whether the row contains two claims. Split a statement about what a source says from a statement about whether that assertion holds.

For a single claim:

- A bare assertion is `unproven`, whether its source is primary or secondary. Source identity does not override missing evidence.
- An account of supporting evidence is `reported` until that evidence is inspected. If inspection directly supports the claim, a new finding can be `verified`.
- If evidence cannot be assessed, or the conclusion remains unresolved, use `unknown` and state the unresolved point.

For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim. The performance claim itself is `unproven` if the announcement provides no supporting measurements. A secondary account describing an identified benchmark is `reported` until the benchmark is inspected.

`verified` does not imply independent replication. State whose evidence was inspected and the conditions it covers. A vendor’s benchmark cannot establish performance outside its tested conditions.

**Other finding types:** `INFERRED` and `GAP` stop being alternatives in the trust-label field. Write researcher deductions as inference prose identifying their premise finding IDs and reasoning. Write unsuccessful searches as gap prose identifying the question, query, and places searched. An inference does not inherit `verified` from its premises; failure to find evidence does not establish that something does not exist.

When sources disagree, retain separate findings with their citations and tags. Describe the disagreement explicitly; do not average it away. An unresolved overall conclusion is `unknown`.

**One definition:** `docs/RESEARCH_TAGS.md` contains these definitions, selection rules, examples, and historical-reading guidance. Other active documents link to it rather than restating the definitions.

**Files to change if EJ adopts the proposal:**

- `docs/workflow-templates/research-file.md`: replace its local definitions with the canonical link; retain the findings table.
- `docs/TASK_TYPES.md`: replace `CONFIRMED/INFERRED/GAP/UNPROVEN` in the research check with the canonical link; preserve its citation requirements.
- `docs/FEEDBACK_TEMPLATES.md`: make both research and web-search summaries carry the finding’s original ID and canonical tag. Keep inference, gap, and disagreement explanations as prose.
- `.claude/agents/researcher.md`: update the draft to reference the canonical definition before adoption.

Explorer’s `read`/`ran` tags stay separate because they distinguish code inspection from execution. The main agent’s `quoted`/`my reading`/`not measured` labels stay separate because they describe how conclusions are presented to EJ.

**Old files:** Preserve completed findings and their original labels. In particular, preserve `runs/20261011-agent-memory-graph/check-findings.py` as the historical check for that run; its accepted spelling list does not become the new semantic authority.

Do not automatically translate historical `FACT`, `CONFIRMED`, or even `verified` into the new meanings. Read them under their original definitions. When reusing a historical finding, assess its evidence against the new definition and create a current finding referencing the original. Pass-back summaries retain existing tags without upgrading them; additional evidence produces a new finding while preserving the earlier record.

**Price:** Keeping the names requires readers to notice the definition change. Centralization requires working links, separating deductions adds explanation, and preserving history means old and current meanings coexist.

## How I decided

1. **My #9:** Start with the data. A finding is an exact claim attached to evidence. Source identity and evidential support cannot substitute for one another. **My reading:** Tag that relationship, rather than the reputation of the source.

2. **My #2:** Require evidence for the claimed behavior. Reading a performance assertion establishes that it was asserted. **My reading:** It does not establish the performance; this is why `unproven` takes precedence over source identity.

3. **My #10:** Remove the recurring special case. **My reading:** Separate the source-statement claim from the underlying claim, so a vendor assertion follows the same rules as any other finding.

4. **My #13:** Solve the immediate problem without redesigning every labeling system. **My reading:** Retain the four familiar spellings, centralize their definitions, and leave labels with different jobs separate.

5. **My #1, my #3, and my #5:** Apply the regression and reversibility rules by analogy to research consumers. **My reading:** Preserve historical findings and checks instead of silently changing the meaning of work already accepted by EJ.

6. **My #11 and my #18:** Make the proposal understandable as a lasting, self-contained record, including its costs. Item #18 is **attributed** documentation guidance, not established as Linus’s own words.

7. **My reading — requirement check:** For the proposal’s individual rules: **source — pass** (this proposal); **one thing — pass** (separate tagging, forwarding, and historical-reuse rules); **unit — pass** (one finding’s exact claim); **can it fail — pass** (examples below); **weak words — pass** (selection conditions stated); **level — pass** (SHOULD defaults); **basis — pass** (`n=0`, revisit specified); **links — pass** (proposed relationships stated explicitly). This is my assessment, not independent validation.

## What I need to know

None for this first proposal. The supplied facts support a recommendation; EJ’s adoption decision remains theirs.

## Costs and risks

- **My #7:** Familiar names can conceal changed meanings. In particular, readers may still mistake `verified` for independently reproduced.
- **My #9:** Judging whether evidence supports the exact claim requires human review. A tag whitelist cannot do that.
- **My #13:** A central document adds link maintenance; separating inference and search gaps makes summaries longer.
- **My #5 and my #11:** Preserving history avoids silent reinterpretation but requires readers to consult the definition used by an old run.
- **My #18, attributed:** No reduction in errors or review time has been measured. The proposal promises clearer decisions, not a quantified productivity gain.

## How we would know I was right

Use these cases in the first research task:

- Vendor assertion without measurements: the assertion’s existence is `verified`; its performance claim is `unproven`.
- Secondary account describing an identified study: its substantive finding is `reported`.
- Inspected primary measurements: `verified` only for the claim and conditions those measurements support.
- Missing evidence or unresolved conflicting results: `unknown`, with the missing point or disagreement recorded.
- Researcher deduction: explicit inference with premise IDs; unsuccessful search: explicit gap with search details.
- Empty, `TBD`, `—`, or `0` in the label field: invalid.
- Historical finding passed through a summary: retains its original label and provenance.

**My reading:** The proposal earns support if another reviewer can apply it without inventing a precedence rule, and the resulting summaries preserve the evidence limits. These cases are written by me; passing them would check consistency with the proposal, not independently establish the truth of the research or prove that this is the best tag set.