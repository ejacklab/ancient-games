# 范蠡 (Fan Li) — Whether a procedure can always be a script and who decides

## Answer
A procedure cannot always be a script: it must only be scripted when its operational conditions and verification can be completely examined without human discretion, and must remain prose in `docs/` when conditions are unformed or require judgment. The agent authoring the procedure classifies it on the spot, and the project owner decides when classification is unclear or contested at the moment of review before it enters `AGENTS.md`.

## How I decided

1. **A procedure cannot always be a script.** Growth cannot be forced when conditions have not arrived, and completion cannot be forced when a matter has not run its course (my #3, `quoted`: 「時不至，不可彊生；事不究，不可彊成」). If a workflow is nascent, exploratory, or volatile, seeking by force to script it early brings misfortune and makes the outcome unknowable (my #7, `quoted`: 「彊索者不祥…王無蚤圖。夫吳，君王之吳也，王若蚤圖之，其事又將未可知也」). When underlying external tools and environments have not taken visible form, executing ahead of them causes failure and shared harm (my #9, `quoted`: 「逆節萌生。天地未形，而先為之征，其事是以不成，雜受其刑。王姑待之」).

2. **The kinds of procedures that cannot be scripts.** Regulating operational affairs goes with the ground (my #2, `quoted`: 「節事者與地」) — this is deterministic scripting. But steadying situations that involve human discretion, shifting policy, or interactive arbitration goes with people (my #2, `quoted`: 「定傾者與人」). Procedures depending on human-in-the-loop decisions, subjective trade-offs, or unformed external contracts cannot be grounded in scripts and belong in `docs/` (my reading).

3. **The test an agent can apply.** Examine the preparations (my #18, `quoted`: 「審備則可以戰乎？」王曰：「巧」). An agent tests: *Can the procedure's preconditions, execution steps, and verification all be examined and executed deterministically without human intervention?* If yes, the matter has run its course (my #3) and the agent must script it without slacking (my #4, `quoted`: 「得時無怠，時不再來，天予不取，反為之災」). If no, completion cannot be forced (my #3), so the agent must record it as prose in `docs/` (my reading).

4. **Who decides and at what moment.** Distribute responsibility by who is better at what (my #14, `quoted`: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也」). The authoring agent operates outside the borders on matters decided on the spot (立斷之事, my #14); therefore, the authoring agent applies the technical test initially while writing the procedure (my reading). However, repository standing assets and listings in `AGENTS.md` are domestic governance inside the borders (四封之內, my #14), which must not forget the state's standing rules (my #8, `quoted`: 「無忘國常」). When classification is unclear or contested, the project owner decides at the temple hall of review, before the script is registered in `AGENTS.md` (my #5, `quoted`: 「夫謀之廊廟，失之中原，其可乎？…天節固然，唯謀不遷」; my reading).

5. **What W3.6 should say.** W3.6 should read: *"A procedure lives in the repo as a script if its execution and verification can be examined and run deterministically, or as a page in `docs/` where they require human discretion. The authoring agent classifies it on the spot, and the project owner decides when unclear or contested during review before it is named in `AGENTS.md`."* (my reading, applying my #3, my #14, and my #18).

## What I need to know

1. If EJ intends for `AGENTS.md` to be edited directly by automated workers without owner review, then the owner's decision moment cannot be registration in `AGENTS.md`; it must occur during a post-hoc verification gate or pull-request check (conditional on EJ's workflow model).
2. If the repository contains procedures that are fully deterministic yet carry destructive or security-sensitive operational risk, then policy might forbid scripting despite passing the technical test (conditional on repository safety rules).
3. Otherwise: none.

## Costs and risks

- **Documentation decay:** Storing non-scriptable procedures as prose in `docs/` risks leaving them idle, which becomes a ladder to disorder as documentation drifts from reality (my #3, `quoted`: 「無曠其眾，以為亂梯」).
- **Premature automation:** Forcing uncertain, evolving tasks into rigid scripts causes brittle failures and forces everyone to share maintenance harm when interfaces break (my #7, `quoted`: 「彊索者不祥」; my #9, `quoted`: 「其事是以不成，雜受其刑」).
- **Harness inconsistency:** Allowing agents across different engines to decide on the spot risks diverging standards across the repository (my reading on my #14).
- **Bottleneck at the owner:** Escalating every unclear case to the project owner risks missing opportune windows if review is delayed (my #4, `quoted`: 「從時者，猶救火、追亡人也，蹶而趨之，唯恐弗及」).

## How we would know I was right

- **Deterministic execution:** 100% of the scripts registered in `AGENTS.md` run to completion and pass their verification checks without requiring human prompts or interactive intervention.
- **Clean dispute resolution:** In any pull request or task run where procedure placement is marked unclear, the authoring agent falls back to `docs/` with a logged rationale, and the project owner resolves the placement in a single review round without task blockage.
- **Zero premature script reverts:** No scripts added to the repository are reverted due to boundary changes that were already known to be unstable at authoring time.
