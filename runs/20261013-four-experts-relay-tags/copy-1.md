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
