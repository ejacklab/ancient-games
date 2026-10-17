# 范蠡 (Fan Li) — Strengthen A5 and A2 checks

## Answer
Before closing A5, its defensive preparations must be completed so its own Fails-if lines fire rather than borrowing coverage from other requirements; before starting A2, prepare tests only for the service-held `Effect.fn` constants and anonymous bodies that failed on real code, while removing agent duties from tool checks. If the project owner accepts wording updates now, clarify A5's dump prohibition and excise agent candidate-naming from A2's tool contract.

### A5
- **Keep** (tied to *without its evidence*): Add an A5 case on a link command (`callers`/`callees`/`chain`/`tests`) asserting that a link's `site` is present, failing under A5 if missing.
- **Keep** (tied to *without its … limits*): Add A5 cases verifying that required limits are present and populated, specifically for `where <missing>` (`not-found`) and commands run without `--tests` (`no test-file pattern given`), charged to A5.
- **Keep** (tied to *a whole map is produced unasked*): Add an A5 case asserting that link and lookup commands do not attach unrequested sections, specifically asserting that `map` and unasked `definitions` are absent from `callers`/`callees`/`chain`/`tests`.
- **Keep** (tied to *an answer comes only inside a dump*): Add an A5 check on default text output asserting that it returns only the targeted answer and not extraneous definitions or whole-repository dumps.
- **Keep** (held-out execution): Ensure all added bundled A5 cases are generated into the held-out copy.
- **Cut**: Any check attempting to evaluate whether the agent asked before requesting a map; interactive agent behavior belongs to P6 and must not block closing tool round A5.
- **Add** (tied to *without its evidence*): Assert that non-link query commands (`where`, `find`) do not emit fabricated link evidence fields, and link commands include valid `via` and `resolution` fields alongside their sites.
- **Wording proposal for A5**:
  - *Current*: `Fails if: an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked.`
  - *Proposed*: `Fails if: an answer comes inside a dump or with unasked sections, lacks its evidence or limits, or a whole map is produced unasked.`
  - *Rationale*: "Only inside a dump" allows a tool to pass if it produces the correct answer accompanied by an extraneous dump; adding "or with unasked sections" catches payload piggybacking where the extra payload is not a complete map.

### A2
- **Keep** (tied to *a known link within the depth is missing*): Add cases traversing chains through anonymous bodies (`Effect.gen` generator callbacks, object-property arrows) at depth 2 or deeper, both up and down.
- **Keep** (tied to *a known link within the depth is missing*): Add cases for `callers` and `callees` of a step function held in an `Effect.fn` constant and reached via service lookup.
- **Keep** (tied to all A2 Fails-if lines): Ensure each of the five A2 Fails-if lines has at least one bundled case charged directly to A2 in the evaluator.
- **Keep** (frozen tests): Include these real-code shapes in Codex's frozen tests for round A2.
- **Cut**: Broad combinatorial permutations of arbitrary anonymous depths or hypothetical framework structures not seen in the target codebase; do not over-build before the round begins.
- **Add** (tied to *an ambiguous match is treated as certain, or a candidate not built is not named*): Split the evaluator assertion so the tool check evaluates only that the tool marks ambiguous matches as `ambiguous: true` with candidates; mark the second clause ("a candidate not built is not named") as pending P6.
- **Wording proposal for A2**:
  - *Current*: `When more than one place matches, the tool flags the match as ambiguous; the agent picks the place that fits the question best, builds its chain, and names every other candidate it did not build. ... Fails if: an ambiguous match is treated as certain, or a candidate not built is not named;`
  - *Proposed*: `When more than one place matches, the tool flags the match as ambiguous and lists all candidates. Fails if: a known place is not found; an ambiguous match is treated as certain or omits candidates; a known link within the depth is missing, or a shown link contradicts the code; a link lacks its kind or location; a function reached twice is shown twice.` (Move agent candidate selection and naming to the agent workflow contract in P6).
  - *Rationale*: A static tool evaluator cannot inspect an agent's conversational explanation; leaving an agent requirement inside the tool's Fails-if line forces the evaluator to report A2 permanently incomplete or uncheckable.

## How I decided
1. **Closing A5 requires finishing what was begun, not declaring victory on hollow preparations.** (my #4: 「得時不成，天有還形。天節不遠，五年復反，小凶則近，大凶則遠。」 `quoted`; my #18: 「審備則可以戰乎？」 `quoted`; my #3: 「事不究，不可彊成」 `quoted`). Attempt 1 passed, but four of five planted defects failed to trigger A5's own line. Closing A5 now would claim completion before the matter has run its course. Adding the five checks examines defensive preparations so A5 closes on its own evidence.
2. **Do what is timely for A5 now; prepare A2 before its start without rushing ahead.** (my #1: 「夫聖人隨時以行，是謂守時。天時不作，弗為人客；人事不起，弗為之始。」 `quoted`; my #3: 「時不至，不可彊生」 `quoted`). A5 is at the end of its round; finishing its checks is the immediate task. A2 is before its round; preparing tests against known failures is necessary preparation, but building code ahead of the round is premature.
3. **Restrain check expansion to what real code requires, using minimal force.** (my #11: 「用力甚少而名聲章明」 `quoted`; my #10: 「無過天極，究數而止」 `quoted`). For A2, the two failures found in the private opencode core set are concrete (`Effect.fn` constants reached through services and anonymous `Effect.gen` bodies). We keep checks strictly to these demonstrated shapes. Adding speculative depths or artificial framework cases violates stopping when the measure is met (my #10).
4. **Separate the tool's craft from the agent's governance.** (my #14: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 `quoted`). The tool evaluator checks code artifacts (JSON shapes, exit codes, links, limits). Naming unbuilt candidates belongs to the agent's interaction (P6). Blurring them makes the tool's check fail or remain uncheckable.
5. **Hold firmly to the established contract without shifting.** (my #5: 「天節固然，唯謀不遷。」 `quoted`). The requirements and Fails-if lines are the temple plan. The evaluator's job is to ensure every Fails-if line has teeth, rather than inventing new requirements or dropping existing commitments.
6. **Address the questions posed to the other perspectives.** (my reading):
   - *Linus (failures passing strengthened checks)*: If a tool appends extra fields outside the checked schema or dumps definitions into stdout, JSON-focused checks will pass while A5 is violated. For A2, if a chain silently truncates at a non-generator closure returning an Effect and emits no limit, it passes unless depth checks assert the target leaf.
   - *孫子 (builder-readable checks)*: Checks in frozen tests and bundled cases can be memorized by the builder. This is covered only because the held-out generator relocates lines and renames identifiers, and because the private opencode set verifies real-world generalization.
   - *老子 (excessive proposals)*: Massive synthetic chain hierarchies are more than needed. A small check asserting property ownership on answer objects and checking text output line counts does far more.
7. **Correct the wording loopholes that defeat verification.** (my #2: 「夫國家之事，有持盈，有定傾，有節事。」 `quoted`; my reading). In A5, "only inside a dump" allows answers accompanied by dumps to pass. In A2, conflating agent candidate reporting with tool call-chain generation makes the requirement uncheckable by static evaluation. Proposing these adjustments to the project owner aligns rules with reality.

## What I need to know
1. If the project owner permits updating requirement text before P6:
   - *If yes*: apply the proposed wording changes to A5 and A2 immediately, removing agent duties from the tool specification.
   - *If no*: retain the existing requirement text and maintain `A2 (agent part): NOT CHECKED` in the evaluator report.
2. The actual nesting depth of anonymous generator functions in the target opencode modules (`packages/core/src/session`, etc.):
   - *If nesting exceeds depth 2 in production code*: extend A2 fixture cases to depth 3.
   - *If nesting in production code is at most depth 2*: stop at depth 2 to avoid unneeded test complexity.
3. Whether default text output is consumed primarily by agents or humans:
   - *If agents*: enforce strict token minimization and exact line count checks.
   - *If humans*: allow standard human-readable whitespace and headers.

## Costs and risks
1. **Risk of rejecting A5 attempt 1**: Adding four strict check categories to A5 and running them against attempt 1 code may cause attempt 1 to fail, forcing attempt 2 of 3 and consuming builder time and tokens. (From my #4: 「得時無怠，時不再來」 `quoted` — finishing must not mean slacking, but delay risks missing the window).
2. **Cost of over-constraining A2 before round start**: Introducing Effect and anonymous chain fixtures into bundled and frozen tests before round A2 begins risks over-constraining the builder's internal representation. (From my #7: 「王無蚤圖...王若蚤圖之，其事又將未可知也」 `quoted` — planning too early or forcing growth when the time has not come brings unnecessary friction).
3. **Risk of generator leakage on held-out cases**: If the held-out generator fails to transform anonymous functions and service wrappers cleanly, the builder may overfit to bundled cases while failing the private set. (From my #18: 「審備則可以戰乎？」 `quoted` — unexamined preparations leave the tool vulnerable).
4. **Governance friction from requirement edits**: Proposing wording changes to A2 and A5 requires review and agreement from the project owner, risking process delay. (From my #14: 「四封之內，百姓之事，蠡不如種也」 `quoted`).

## How we would know I was right
1. When the five COO plants (`runs/20261014-code-map-build/evidence/p3-a5-src-plants.txt`) are re-run against the evaluator with the strengthened A5 checks, A5's own line reports **NOT MET** for `where-inside-dump`, `callers-unasked-map`, `site-dropped`, and `not-found-limit-dropped`, rather than only 1 of 5.
2. In round A2, the bundled fixture cases replicate the failures previously observed on the private real-code set (`Effect.fn` constants and anonymous generator bodies), and once the builder satisfies these bundled cases, the private opencode core set turns **MET**.
3. The evaluator report eliminates `NOT CHECKED` markers on tool-evaluated requirements once agent candidate-naming is moved to P6.
