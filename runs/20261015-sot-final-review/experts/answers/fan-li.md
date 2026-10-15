# 范蠡 (Fan Li) — Review of the source-of-truth memory design

## Answer
An agent will stumble on three contradictions between the prose and the YAML: K4.1 forbids retiring entries without replacement, K1.1 suggests editing entries in place while K4.3 forbids rewriting claims, and two open choices remain unassigned. The design should assign those choices, allow retirement without a successor, clarify that K1.1 requires creating a superseding entry, specify default reviewers, and halt only the work governed by a failed MUST.

## How I decided

1. **Question 1 (Will an agent follow it?):** Under my #18, examining defensive preparations (「審備則可以戰乎？」 — "If the preparations are examined, can we then fight?", `quoted`), an agent will fail or stall at three specific flaws:
   - K4.1 requires every `superseded` or `retired` entry to have a `superseded_by` link. An entry retired because a feature or constraint is simply dead has nothing to link to; an agent will either invent a false link or fail the check.
   - K1.1 tells the agent to "change the entry first, then the code", which invites directly editing the existing file, directly colliding with K4.3's rule that claims are never rewritten.
   - Leaving `who_decides: unassigned` on W3.6 and Rd3.1a leaves the agent without an authority when it hits those forks.

2. **Question 2 (The wording the COO wrote):**
   - *`fails_if` additions:* For W5.2, change it (my reading). "Fails if a task ends with what it learned unwritten" cannot be evaluated objectively; change it to check whether the task journal was processed or logged as reviewed under K5.2. For W6.1a, keep it: preventing multiple entries per file is concrete and checkable in git (my #18). For K5.1, change it: keep the rule that a journal file is never edited after writing, but drop "raw notes are kept elsewhere", which git cannot detect (my reading). For Rd1.1 and Rd5.2, keep both: layout verification and enforcing that memory never overrides standing instructions uphold foundational boundaries (my #2, 「持盈者與天，定傾者與人，節事者與地」 — "Keeping the full goes with Heaven; steadying the tilting goes with people; regulating affairs goes with Earth", `quoted`).
   - *Ending SHOULD `fails_if` with "with no written reason":* Keep it. Regulating affairs requires explicit boundaries; allowing exceptions only with recorded reasons ensures deviations leave an audit trail rather than failing silently (my #2; my #10, 「無過天極，究數而止」 — "they did not pass Heaven's limit, and stopped when the count was exhausted", `quoted`).
   - *Splitting W1.2:* Keep it. Separating the hard tool barrier (`---` delimiters as MUST) from field layout (SHOULD) respects the division between automated syntax and human readability (my #14).
   - *Additions to W1.1b, Rd5.3, Rd2.3b:* Keep all three. Disallowing duplicate IDs stops branch collisions, and explicitly passing the exceptions in Rd5.4 and Rd2.3b avoids false alarms (my #18).
   - *`who_decides` assignments:* Keep the project owner on W4.1c, W5.3b, W6.3a, and Rd5.3 (temple-level decisions belong to the sovereign). Keep the reading agent on K5.2 (the worker on the ground judges what was observed; my #14). Keep the workflow on K1.1. Change `unassigned` on W3.6 and Rd3.1a (see step 4).
   - *Header keys:* Keep them. They establish the constant framework of the requirements (my #2).

3. **Question 3 (Who reviews the judged checks?):** Under my #14 (「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 — "Inside the four borders, the people's affairs: I am not as good as 種. Outside the four borders, dealing with enemy states, matters decided on the spot: 種 is not as good as I", `quoted`) and my #3 (「無曠其眾，以為亂梯」 — "Do not leave the people idle — that becomes a ladder to disorder", `quoted`), leaving reviewer unassigned produces inaction. The design should state clear defaults based on jurisdiction:
   - For internal task work: the default reviewer is the task's automated verifier or the reviewing agent checking the branch.
   - For systemic disputes (mismatches under Rd5.3, contested supersessions, merge conflicts under W6.3a): the reviewer is the project owner.

4. **Question 4 (The two open `who_decides`):** Under my #14 and my #3, neither should remain unassigned:
   - For Rd3.1a (which agents work on the project, and so the strictest limit): The project owner decides. Selecting the workforce across the repo is a sovereign decision beyond the scope of a single task.
   - For W3.6 (whether a procedure can be a script): The author of the procedure decides on the spot (with the project owner resolving disputes), because the author tests directly whether the steps can run deterministically without human intervention.

5. **Question 5(a) (Retiring an entry with nothing replacing it):** Under my #6 (「蜚鳥盡，良弓藏；狡兔死，走狗烹。」 — "When the flying birds are gone, the good bow is put away; when the cunning hare is dead, the hunting dog is cooked", `quoted`) and my #10 (「無過天極，究數而止」, `quoted`), when an outside constraint or abandoned feature ends, the matter has run its course. Forcing a `superseded_by` link forces an artificial connection where none exists (my #3, 「時不至，不可彊生；事不究，不可彊成」 — "When the time has not come, growth cannot be forced; when the matter has not run its course, completion cannot be forced", `quoted`). The design must allow an entry to be marked `retired` with `superseded_by: none` and the reason recorded in `changed:`.

6. **Question 5(b) (Clarity of supersession in K1.1 vs K4.3):** Under my #5 (「夫謀之廊廟，失之中原，其可乎？…天節固然，唯謀不遷。」 — "To plan it in the temple hall and lose it on the central plain — can that be right? … Advance and retreat change into each other; later you would regret it. Heaven's rhythm is like that; only the plan does not move", `quoted`) and my #18, the wording in K1.1 is not clear enough. Saying "change the entry first" directly invites editing the existing file. K1.1 must explicitly state: "create and commit the superseding entry (or status change) first, then the code."

7. **Question 5(c) (What work stops when a MUST fails):** Under my #12 (「彼來從我，固守勿與…宜為人主，安徐而重固」 — "If they come at us, hold firm and do not engage… A side fit to be the host is calm, slow, heavy and firm", `quoted`) and my #3 (「自若以處，以度天下，待其來者而正之」 — "Stay as you are and take the measure of the world; wait for what comes and set it right", `quoted`), only the specific work governed by the failed record stops. Halting the entire session over an isolated failure abandons the overall plan. The agent must hold firm on the blocked action, report it, and carry on with independent work, exactly as prescribed in Rd5.3.

## What I need to know
- Whether EJ intends for project repositories to mandate human review for pull requests, or if automated verifiers and CI tools are expected to be the sole gating reviewers for agent work. If automated CI is the sole gate, all checks marked `reviewer` will be advisory unless backed by automated linting or gating scripts.

## Costs and risks
- Defaulting task review to automated or peer agents risks missed defects if the inspecting agent lacks sufficient context (from my #14).
- Permitting entries to be retired without a `superseded_by` link risks losing historical context if the author writes an inadequate explanation in `changed:` (from my #6 and my #18).
- Allowing an agent to continue independent work when a MUST fails risks wasted effort if the blocked requirement turns out to undermine the entire task (from my #12 and my #3).
- Giving procedure authors the discretion to decide whether a procedure can be scripted risks the accumulation of manual markdown runbooks when an author is reluctant to write scripts (from my #14 and my #3).

## How we would know I was right
- A test run where an agent is instructed to retire an obsolete constraint and update an existing architectural decision: the agent creates a superseding entry without modifying the old entry's claim, marks the dead constraint retired with no replacement without failing validation, and proceeds with independent code changes without stalling on unassigned decision fields.
