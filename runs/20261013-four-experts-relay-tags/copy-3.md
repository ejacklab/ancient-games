**Status:** Proposal for EJ’s decision; not measured (`n=0`). These are proposed SHOULD defaults, with any departure explained by the researcher. The definitions themselves are EJ’s; a default may bend in a hard case with a written reason, but a definition may not. Track operational friction during initial use, but do not alter canonical definitions on an `n=1` basis; evaluate adjustments only after the same friction recurs across separate tasks. **Adoption waits on one reckoning:** re-tag the ten accepted `20261011-agent-memory-graph` findings files with the selection rule below, writing each row’s tag down before looking at its old one. If any row will not land on exactly one tag without argument, the rule is not yet ready to be the one copy.

**Scope:** The researcher assigns one tag to each research finding. The tag describes the evidence available to the researcher for the finding’s exact wording; it is neither a confidence score nor a declaration of universal truth. **Primary and secondary are relative to that exact wording, not to the source’s reputation:** one document is primary evidence for the claim that it says what it says, and secondary for a claim about the world that it only reports. That is why the same blog can carry `verified` for one row and no support at all for the next.

**The four tags.** Each names one measure: the evidence in hand for the exact claim.

| Tag | Definition |
|---|---|
| `verified` | The supporting evidence itself — the primary document’s own measurements, data, or wording — was inspected and directly supports the exact claim within its stated scope; merely reading an assertion does not qualify. |
| `reported` | An account describes supporting evidence for the exact claim, but that evidence has not been inspected. |
| `unproven` | The claim is asserted, and nothing beyond the assertion is present or described; the cited material offers no supporting evidence. |
| `unknown` | Supporting evidence exists but cannot be obtained or brought to bear on the claim, or the evidence conflicts and is unresolved. |

**When two tags seem to fit:** First check whether the row contains two claims. Split a statement about what a source says from a statement about whether that assertion holds, then tag each claim separately.

For one claim, ask what evidence is in hand for that exact wording; the first answer that applies is the tag:

- Only the assertion, with nothing described past it → `unproven`. This holds whether the asserting document is primary or secondary; source rank does not substitute for evidence.
- An account that describes supporting evidence you have not inspected → `reported`. If you then inspect that evidence and it directly supports the claim, a new finding can be `verified`.
- The supporting evidence itself, inspected and directly supporting the claim → `verified`.
- Evidence that exists but cannot be obtained or assessed, or that conflicts and is unresolved → `unknown`, and state the unresolved point.

Write the finding so that one row fits; if you cannot, it is two findings. **Never upgrade a label in place.** A finding’s label is fixed once assigned; when later investigation inspects primary evidence, record a new finding referencing the original rather than editing the earlier record.

For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim — the announcement’s wording is the evidence for what it says. The performance claim itself is `unproven` if the announcement supplies no measurements. A paper’s own reported benchmark numbers, read in the paper, are the supporting evidence itself: `verified` for the claim and conditions those numbers state. A blog post that describes an identified benchmark is `reported` until the benchmark is inspected; a blog post that only repeats a claim, with no description of evidence behind it, is `unproven`.

`verified` does not imply independent replication. State whose evidence was inspected and the conditions it covers. A vendor’s benchmark cannot establish performance outside its tested conditions.

**Other finding types:** `INFERRED` and `GAP` stop being alternatives in the trust-label field. Write researcher deductions as inference prose identifying their premise finding IDs and reasoning. Write unsuccessful searches as gap prose identifying the question, query, and places searched. A search that found nothing is a gap, not a tag: do not record absence as though it were evidence. An inference does not inherit `verified` from its premises; failure to find evidence does not establish that something does not exist.

When sources disagree, retain separate findings with their citations and tags. Describe the disagreement explicitly; do not average it away. An unresolved overall conclusion is `unknown`.

**One definition:** [RESEARCH_TAGS.md](file:///home/smoke01/dev/ancient-games/docs/RESEARCH_TAGS.md) is to be created as the single copy; it will hold these definitions, the selection rule, the examples, and the historical-reading guidance. That is the only new file. Other active documents link to it rather than restating the definitions. Only EJ changes the definitions.

**Files to change if EJ adopts the proposal:**

- `docs/RESEARCH_TAGS.md`: create it with the contents above.
- [research-file.md](file:///home/smoke01/dev/ancient-games/docs/workflow-templates/research-file.md): replace its local definitions with the canonical link; retain the findings table and clarify that bare primary assertions do not qualify for `verified`.
- [TASK_TYPES.md](file:///home/smoke01/dev/ancient-games/docs/TASK_TYPES.md): replace `CONFIRMED/INFERRED/GAP/UNPROVEN` in the research check with the canonical link; preserve its citation requirements.
- [FEEDBACK_TEMPLATES.md](file:///home/smoke01/dev/ancient-games/docs/FEEDBACK_TEMPLATES.md): make both research and web-search summaries carry the finding’s original ID and canonical tag. Keep inference, gap, and disagreement explanations as prose.
- [.claude/agents/researcher.md](file:///home/smoke01/dev/ancient-games/.claude/agents/researcher.md): update the draft to reference the canonical definition before adoption.

Only these change in the first pass; no historical run folder is edited. Any future findings check must accept the canonical four tags and must not demand a tag where inference or gap prose is written.

Explorer’s `read`/`ran` tags stay separate because they distinguish code inspection from execution. The main agent’s `quoted`/`my reading`/`not measured` labels stay separate because they describe how conclusions are presented to EJ.

**Old files:** Preserve completed findings and their original labels. In particular, preserve `runs/20261011-agent-memory-graph/check-findings.py` as the historical check for that run; its accepted spelling list does not become the new semantic authority.

Do not automatically translate historical `FACT`, `CONFIRMED`, or even `verified` into the new meanings; read them under their original definitions. When reusing a historical finding, assess its evidence against the new definition and create a current finding referencing the original. Pass-back summaries retain existing tags; new evidence follows the no-upgrade rule above.

**Price:** Keeping the names requires readers to unlearn the older loose definition of `verified` (where reading any primary document sufficed). One measure means source reliability is not recorded separately; if it matters, it belongs in prose. Centralization requires working links, separating deductions into prose removes simple column regex checks and requires semantic review, and preserving history means old and current meanings coexist across repository runs.
