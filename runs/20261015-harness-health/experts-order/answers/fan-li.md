# 范蠡 (Fan Li) — order of vision, requirements, and use cases

## Answer
If creating a new system, the order should be vision first, requirements second, and use cases third as a bounded loop that tests preparations against fixed units and stops when the count is exhausted (my #18, my #10); if steadying or repairing an existing system already running in the field, use cases first holds to measure ground reality before codifying rules (my #2, my #3, my #11). The loop is closed when fixed behavioral unit coverage reaches the target count (my #10), while the overarching plan does not shift (my #5).

## How I decided

1. **State affairs divide into three, and the plan made in the council must not be lost in the field (my #2, my #5).**
   In my #2, state affairs divide into three: keeping the full accords with Heaven, steadying the tilting accords with people, and regulating affairs accords with Earth (`quoted`: 「夫國家之事，有持盈，有定傾，有節事。」/「持盈者與天，定傾者與人，節事者與地。」). My reading: Vision accords with Heaven (enduring purpose and safety bounds); Requirements accord with People (human contracts, obligations, and definitions of failure); Use cases accord with Earth (concrete ground conditions and operational scenarios). In my #5, I warned: "To plan it in the temple hall and lose it on the central plain — can that be right? ... Heaven's rhythm is like that; only the plan does not move" (`quoted`: 「夫謀之廊廟，失之中原，其可乎？…天節固然，唯謀不遷。」). When embarking on new work, designing without a settled vision is marching onto the plain without a temple plan.

2. **Do not plan early, and do not campaign before form has appeared (my #7, my #9).**
   In my #7, I cautioned: "Do not plan early... if you plan for it early, the matter will again be unknowable" (`quoted`: 「王無蚤圖。夫吳，君王之吳也，王若蚤圖之，其事又將未可知也。」). In my #9, I warned that campaigning ahead of visible form causes failure: "Rebellion against order is sprouting. Heaven and Earth have not yet taken visible form, and to campaign ahead of it — that is why the affair does not succeed, and all together suffer the harm. For now, wait" (`quoted`: 「逆節萌生。天地未形，而先為之征，其事是以不成，雜受其刑。王姑待之。」). My reading: When a feature is brand-new, brainstorming exhaustive use cases before the vision and core requirement bounds exist is planning early and campaigning before form has settled. As seen in the trial, ungrounded generation produced cases that contradicted settled decisions.

3. **The recommended order and the closing of the loop (my #10, my #18).**
   For new work, the order I recommend is **Vision → Requirements → Use cases**.
   This is not a rigid one-way line; advance and retreat turn into each other: "Those of old who used troops well took advance and retreat as their constant and the four seasons as their rule; they did not pass Heaven's limit, and stopped when the count was exhausted" (`quoted`, my #10: 「臣聞古之善用兵者，贏縮以為常，四時以為紀，無過天極，究數而止。」). Use cases examine defensive preparations before the army moves (`quoted`, my #18: 「審備則可以戰乎？」). When use cases reveal gaps in requirements (such as clauses lacking a "fails if" or untested rules), they loop back to revise the requirement.
   What closes the loop: You do not loop endlessly; you stop when the count is exhausted (my #10: 「究數而止」). Here, the loop closes when the agreed count is met: 80% coverage of fixed behavioral units by consequence, verified against planted failures. Throughout revisions, the vision remains the invariant temple plan (my #5: 「唯謀不遷」).

4. **Where EJ's "use cases first" holds and where it breaks (my #3, my #11, my #7).**
   - **Where it holds:** When steadying what is tilting (my #2) or working with an already operating system where people are actively acting: "People bring it about themselves, Heaven and Earth give it form, the sage goes by that and completes it" (`quoted`, my #11: 「人自生之，天地形之，聖人因而成之。」).
     *Concrete case:* Refactoring an existing system (such as the project-memory cache) or addressing production bugs. Here, caller traffic and bug reports exist on the ground. Waiting and taking the measure of the world (`quoted`, my #3: 「自若以處，以度天下，待其來者而正之，因時之所宜而定之。」) by collecting concrete use cases first allows EJ to discover what the system actually does before formalizing requirements and vision.
   - **Where it breaks:** When creating an unprecedented capability or product from scratch.
     *Concrete case:* Designing a novel autonomous agent harness or data engine with no predecessor. If use cases are generated before setting the vision ("who it is for, problem it solves, what it will not do"), an AI prompted to brainstorm all scenarios generates speculative noise and contradictions (my #7: 「王若蚤圖之，其事又將未可知也」).

5. **Who writes each of the three (my #6, my #14).**
   In my #14, tasks go to whoever is better at them, stating weaknesses openly (`quoted`: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」). In my #6, roles are distinct: "You act by your law; I act by my intent" (`quoted`: 「君行制，臣行意。」). Every artifact has one maker:
   - **Vision:** Written by EJ alone (the ruler's intent and negative boundaries). An agent may only record what EJ has stated.
   - **Requirements:** Drafted by the worker/architect (agent or engineer) from EJ's vision, with EJ deciding open choices (my #14).
   - **Use cases:** Seeded by EJ from real experience; expanded by AI engines generating scenario candidates that attach strictly to fixed units (my #14, my #18).

6. **The check each must pass before building the next (my #3, my #18).**
   - **Vision check:** Must define who it is for, the problem it solves, what it will not do, and how we know it works. Fails if any part is missing or contains agent-invented scope. *Planted check:* A vision missing the negative boundary ("what it will not do") must be flagged and rejected by the validator.
   - **Requirements check:** Must pass the eight requirement dimensions (who decides, one thing, unit, can it fail, weak words, level, basis, links). Each requirement must specify MUST/SHOULD, observable "fails if" conditions, and fixed behavioral units. *Planted check:* A clause without a "fails if" (as found in today's trial) must fail validation.
   - **Use cases check:** Must examine the preparations (my #18). Each case must attach to an established unit without inflating the denominator, must not contradict settled decisions, must reach the 80% consequence coverage target, and historical tests must prove they can fail on a planted bug before being credited as evidence.

## What I need to know

1. If the upcoming work is greenfield development, vision must come first (my #5, my #7); if it is refactoring or fixing an existing live codebase, use cases first holds (my #2, my #11).
2. Who determines the consequence criteria used to select which 20% of units may be skipped (EJ or the worker; my #14).

## Costs and risks

- **Delay from waiting for form (my #3, my #9):** Requiring vision and requirements before use cases means waiting until boundaries are settled, which prevents immediate trial-and-error exploration on the ground.
- **Risk of infinite revision loop (my #10):** Allowing use cases to trigger requirement revisions risks churn unless the stopping limit (80% unit count) is strictly respected.
- **Bottleneck on the ruler (my #6, my #14):** Confining vision and open decisions to EJ means work halts if EJ is not present to settle questions.
- **Bounded blindness (my #18):** Restricting AI cases to fixed units prevents denominator gaming, but risks ignoring emergent edge cases that lie outside the conceived behavioral units.

## How we would know I was right

A comparative trial on two new tasks:
1. Under **Vision → Requirements → Use cases** (bounded loop to 80% unit coverage): zero contradictory cases are produced, 100% of generated cases attach to defined units, and discovered gaps in requirement text ("fails if" omissions) are patched without shifting the core vision.
2. Under **Use cases first** on a greenfield task: generated cases exhibit contradictions with established architecture decisions, cases float unattached to fixed units, and the requirement requires major restarts before implementation can be designed.
