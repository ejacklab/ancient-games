# 范蠡 (Fan Li) — Unifying research trust tags

## Answer
I kept the four trust tags, the separation of deductions and search gaps into prose, and the strict preservation of historical run files; I moved the house rule that a label is never upgraded into the active selection rules, and removed the invitation to rewrite canonical definitions after an isolated trial (`n=1`). If EJ adopts this, the canonical definition in [RESEARCH_TAGS.md](file:///home/smoke01/dev/ancient-games/docs/RESEARCH_TAGS.md) anchors research trust across active workflows while leaving existing history undisturbed.

### The copy

**Status:** Proposal for EJ’s decision; not measured (`n=0`). These are proposed SHOULD defaults, with any departure explained by the researcher. Track operational friction during initial use, but do not alter canonical definitions on an `n=1` basis; evaluate adjustments only after multiple tasks show a settled pattern.

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
- **Never upgrade a label in place.** A finding's label is fixed once assigned. When additional investigation inspects primary evidence, record a new finding referencing the original rather than editing the earlier record.

For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim. The performance claim itself is `unproven` if the announcement provides no supporting measurements. A secondary account describing an identified benchmark is `reported` until the benchmark is inspected.

`verified` does not imply independent replication. State whose evidence was inspected and the conditions it covers. A vendor’s benchmark cannot establish performance outside its tested conditions.

**Other finding types:** `INFERRED` and `GAP` stop being alternatives in the trust-label field. Write researcher deductions as inference prose identifying their premise finding IDs and reasoning. Write unsuccessful searches as gap prose identifying the question, query, and places searched. An inference does not inherit `verified` from its premises; failure to find evidence does not establish that something does not exist.

When sources disagree, retain separate findings with their citations and tags. Describe the disagreement explicitly; do not average it away. An unresolved overall conclusion is `unknown`.

**One definition:** [RESEARCH_TAGS.md](file:///home/smoke01/dev/ancient-games/docs/RESEARCH_TAGS.md) contains these definitions, selection rules, examples, and historical-reading guidance. Other active documents link to it rather than restating the definitions.

**Files to change if EJ adopts the proposal:**

- [research-file.md](file:///home/smoke01/dev/ancient-games/docs/workflow-templates/research-file.md): replace its local definitions with the canonical link; retain the findings table and clarify that bare primary assertions do not qualify for `verified`.
- [TASK_TYPES.md](file:///home/smoke01/dev/ancient-games/docs/TASK_TYPES.md): replace `CONFIRMED/INFERRED/GAP/UNPROVEN` in the research check with the canonical link; preserve its citation requirements.
- [FEEDBACK_TEMPLATES.md](file:///home/smoke01/dev/ancient-games/docs/FEEDBACK_TEMPLATES.md): make both research and web-search summaries carry the finding’s original ID and canonical tag. Keep inference, gap, and disagreement explanations as prose.
- [.claude/agents/researcher.md](file:///home/smoke01/dev/ancient-games/.claude/agents/researcher.md): update the draft to reference the canonical definition before adoption.

Explorer’s `read`/`ran` tags stay separate because they distinguish code inspection from execution. The main agent’s `quoted`/`my reading`/`not measured` labels stay separate because they describe how conclusions are presented to EJ.

**Old files:** Preserve completed findings and their original labels. In particular, preserve `runs/20261011-agent-memory-graph/check-findings.py` as the historical check for that run; its accepted spelling list does not become the new semantic authority.

Do not automatically translate historical `FACT`, `CONFIRMED`, or even `verified` into the new meanings. Read them under their original definitions. When reusing a historical finding, assess its evidence against the new definition and create a current finding referencing the original. Pass-back summaries retain existing tags without upgrading them; additional evidence produces a new finding while preserving the earlier record.

**Price:** Keeping the names requires readers to unlearn the older loose definition of `verified` (where reading any primary document sufficed). Centralization requires working links, separating deductions into prose removes simple column regex checks and requires semantic review, and preserving history means old and current meanings coexist across repository runs.

## How I decided

1. **Kept** the four core trust tags (`verified`, `reported`, `unproven`, `unknown`) and their evidentiary boundaries. Driven by my #18 (`quoted`: 「審備則可以戰乎？」王曰：「巧。」) and my #2 (`quoted`: 「持盈者與天，定傾者與人，節事者與地。」). Each tag examines defensive preparations and grounds the finding in concrete evidence rather than subjective confidence.
2. **Kept** the principle that source identity does not override missing evidence (a bare assertion is `unproven`). Driven by my #18 and my #1 (`quoted`: 「夫人事必將與天地相參，然後乃可以成功。」). A claim cannot stand merely on the speaker's status without matching empirical evidence.
3. **Changed** the revisit trigger in Status: removed the clause inviting immediate modification after a single task (`n=1`), changing it to observation of friction across multiple runs. Driven by my #3 (`quoted`: 「時不至，不可彊生；事不究，不可彊成。自若以處，以度天下，待其來者而正之，因時之所宜而定之。」) and my #7 (`quoted`: 「未可也。蠡聞之，上帝不考，時反是守，彊索者不祥。…有奪，有予，有不予，王無蚤圖。」). Changing standards on `n=1` forces completion before matters mature and schemes prematurely.
4. **Added** the house rule "Never upgrade a label in place" directly into the core selection rules, rather than leaving it buried only in the historical files section. Driven by my #5 (`quoted`: 「夫謀之廊廟，失之中原，其可乎？王姑勿許也。…贏縮轉化，後將悔之。天節固然，唯謀不遷。」) and my #11 (`quoted`: 「死生因天地之刑，天因人，聖人因天；人自生之，天地形之，聖人因而成之。是故戰勝而不報，取地而不反…」). A finding assigned at a given evidentiary state is fixed ground; fresh evidence produces a new finding rather than retroactively shifting the historical entry.
5. **Kept** moving `INFERRED` and `GAP` out of trust labels into prose explanations. Driven by my #14 (`quoted`: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」) and my #9 (`quoted`: 「逆節萌生。天地未形，而先為之征，其事是以不成，雜受其刑。王姑待之。」). Trust tags measure source evidence, while deductions measure researcher reasoning and gaps measure search perimeters. Conflating them confuses tools, and treating an unlocated item as proven absence acts before form has appeared.
6. **Kept** the separation of Explorer tags (`read`/`ran`) and main agent presentation labels (`quoted`/`my reading`/`not measured`). Driven by my #14 (`quoted`: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」). Code inspection, external research, and reporting in the council chamber have different scopes and must not be forced into one vocabulary.
7. **Kept** preserving historical files, scripts, and past runs without retroactive translation. Driven by my #5 (`quoted`: 「天節固然，唯謀不遷。」) and my #11 (`quoted`: 「取地而不反」). Previous commitments stand on their own terms.
8. **Added** explicit acknowledgment in the price section of the cognitive cost of redefining `verified` and the tooling impact of moving inferences to prose. Driven by my #17 (`quoted`: 「前日吾所爲欲遣少子，固爲其能棄財故也。而長者不能，故卒以殺其弟，事之理也，無足悲者。」) and my #4 (`quoted`: 「得時不成，天有還形。天節不遠，五年復反，小凶則近，大凶則遠。」). Every operational choice has an inescapable cost rooted in the logic of things; obscuring that cost invites failure.
9. **Kept** [RESEARCH_TAGS.md](file:///home/smoke01/dev/ancient-games/docs/RESEARCH_TAGS.md) as the single canonical home for definitions. Driven by my #16 (`quoted`: 「計然之策七，越用其五而得意。既已施於國，吾欲用之家。」) and my #2 (`quoted`: 「節事者與地。」). Applying a unified policy systematically avoids divergent local rules.

## What I need to know
- Whether EJ requires an automated validation script (analogous to the old `check-findings.py`) to enforce the new tags across future runs, or if manual inspection by the intake verifier is sufficient. If automated enforcement is desired, the validator must be designed to parse table tags and prose blocks together rather than checking a single column.

## Costs and risks
1. **Cognitive reversion risk:** Under previous templates, reading a primary file earned `verified` automatically. Under the new definition, reading a bare claim in a primary document earns only `unproven` for the substance. Researchers accustomed to the old convention will risk mislabelling bare claims unless explicitly checked. (From my #17: 「事之理也」).
2. **Verification overhead:** Moving `INFERRED` and `GAP` to prose eliminates single-column regex filtering and requires semantic review or structured prose parsing. (From my #18: 「審備則可以戰乎？」).
3. **Friction impatience:** Initial runs under stricter tag rules may feel slower or encounter edge cases, tempting workers to modify definitions before sufficient data accumulates. (From my #3: 「時不至，不可彊生；事不究，不可彊成」 and my #7: 「王無蚤圖」).

## How we would know I was right
In the next two research tasks executed under this proposal:
1. Every row in the findings table carries strictly one of the four canonical tags (`verified`, `reported`, `unproven`, `unknown`), with zero instances of `INFERRED` or `GAP` in the table column.
2. In cases where primary vendor literature makes performance claims without verifiable measurement data, the substantive claim is tagged `unproven` (with the narrow claim that the vendor made the assertion tagged `verified`).
3. In subsequent reviews or extended research runs, zero existing findings rows are edited in place when primary evidence is later unearthed; each appears as an independent finding citing the earlier ID.
4. Historical run checks and scripts continue to execute against their respective past folders without errors.
