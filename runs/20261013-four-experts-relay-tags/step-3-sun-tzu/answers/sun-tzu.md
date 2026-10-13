# 孫子 (Sun Tzu) — one official set of research trust tags

## Answer

I made all four tags measure one thing — the evidence in hand for the exact claim — turned the selection rule into an ordered ladder, defined primary/secondary relative to the exact wording, and required a count over already-accepted findings before adoption; I kept the four names, the single canonical file, the no-upgrade rule, and the preservation of history. If EJ adopts this, `docs/RESEARCH_TAGS.md` (new) holds the one copy and every tag answers "what evidence do I actually have?" rather than "whose source is it?"

### The copy

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

## How I decided

1. **Kept** the four names (`verified`, `reported`, `unproven`, `unknown`) and `docs/RESEARCH_TAGS.md` as the one home. My #3 (`quoted`: 「凡用兵之法，全國為上，破國次之」) — keep the accepted set whole rather than break it — and my #12 (`quoted`: 「凡戰者，以正合，以奇勝」): run 2’s accepted set is the regular I engage with; the new selection rule is the irregular that wins.
2. **Changed** the selection rule from a loose list into an ordered ladder (split → assertion only → description of evidence → evidence in hand). My #1 (`quoted`: 「地生度，度生量，量生數，數生稱，稱生勝」) — the source itself gives an ordered chain, so the tag is the outcome of the same kind of chain — and my #16 (`quoted`: 「約束不明，申令不熟，將之罪也」): an order that will not decide the case is the general’s fault. This is the change that answers the five reviewers’ `reported`/`unproven` clash.
3. **Changed** all four definitions onto one measure, evidence in hand. My #10 (`quoted`: 「兵之勝，避實而擊虛」) — strike the empty: the weak point was two measures sharing one label, so I moved the measure and left the names.
4. **Added** the reading that primary/secondary are relative to the exact wording. My #19 (`quoted`: 「九地之變，屈伸之利，人情之理，不可不察也」) — name the ground, act as prescribed — and my #1: the exact claim is the unit that gets counted.
5. **Added** the pre-adoption reckoning over the accepted findings files. My #1 (`quoted`: 「多算勝，少算不勝，而況於無算乎？」) — reckon before you commit — and my #4 (`quoted`: 「知彼知己，百戰不殆」): know the other side (the recorded usage counts) and yourself (this proposal is `n=0`).
6. **Added** the line that definitions are fixed and EJ’s while defaults may bend with a written reason. My #13 (`quoted`: 「途有所不由，軍有所不擊，城有所不攻，地有所不爭，君命有所不受」): the field may decline a default, and not every road is taken.
7. **Changed** `unknown` and `unproven` so they cannot overlap: `unproven` = nothing beyond the assertion; `unknown` = evidence exists but cannot be obtained or assessed, or conflicts. My #16 and my #15 (`quoted`: 「凡此五者，將之過也，用兵之災也」) — examine the known faults instead of leaving them in the order.
8. **Kept** inferences and gaps as prose, and **added** “a search that found nothing is a gap, not a tag.” My #11 (`quoted`: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也」) — foreknowledge must come from a source that knows the situation; an empty search supplies none.
9. **Kept** history preservation and the no-upgrade rule; **removed** the restatement of the upgrade mechanics from the Old-files paragraph, since the selection rule already carries it. My #3 (whole over broken) and my #13 (not every road taken).
10. **Bounded** the work to one new file plus four edits and added the future-check line. My #13 and my #8 (`quoted`: 「故兵聞拙速，未睹巧之久也」) — value the quick, decisive move over a drawn-out one.
11. **Kept separate** the Explorer `read`/`ran` tags and the main agent’s `quoted`/`my reading`/`not measured` labels. My #19 — a different ground gets a different prescription, so the same words are not forced onto different work.

## What I need to know

- Is the accepted `20261011-agent-memory-graph` set (10 files) the right material for the pre-adoption reckoning, or is there another accepted findings set it should be run over? If EJ names a different set, the adoption test changes.
- What count replaces “multiple tasks show a settled pattern” — how many separate runs, and must the same friction recur in the same tag? Without a count, that trigger cannot be checked.
- Does EJ want source reliability recorded at all? If yes, it must be a separate prose field, because these four tags carry one measure.

## Costs and risks

- The one-measure design drops source reliability from the tag; where a source’s standing matters, it must be written in prose. (my #10, my #12)
- The ladder adds a step the researcher must walk, and no tag regex can check it; the check becomes semantic review. (my #16, my #8)
- Keeping the familiar names hides a changed meaning of `verified`; readers may still apply the old rule that reading any primary document sufficed. (my #3, my #16)
- Preserving history leaves old and new meanings side by side; a reader must know which definition an old run used. (my #3)
- The reckoning is itself a pass over ten files, and if it fails, adoption is blocked rather than rushed. (my #1, my #8)
- A future automated check, if EJ wants one, must read prose as well as table tags. (my #16)

## How we would know I was right

**My test, written by me (my reading); passing it checks consistency with this proposal, not the truth of the research.** Apply the copy to these five cases, then re-tag the ten accepted files:

1. A vendor blog says “our system is 60% faster,” no benchmark shown → two rows: `verified` that the vendor claims it, `unproven` that it is 60% faster.
2. A paper’s own reported benchmark numbers, read in the paper → `verified` for the claim and conditions those numbers state.
3. A claim only in a blog post about a paper, paper unread → `reported` if the post describes the paper’s evidence, `unproven` if it only repeats the claim.
4. A search for a named system that returned nothing → gap prose with query and places searched, no tag.
5. A conclusion drawn from two other findings → inference prose with premise IDs, no tag, no inherited `verified`.

**Observable result:** every one of the ten accepted rows lands on exactly one tag without argument, and in the next research tasks the tag column carries zero `INFERRED`/`GAP` and no accepted row is edited in place. This is `n=0` until EJ adopts it and the reckoning runs.
