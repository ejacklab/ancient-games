# Findings — case A: requirements not clear
Produced 2026-10-03 by a research agent. Question asked: how best to handle building a feature when the requirements are NOT clear, for one developer (EJ) directing AI coding agents (a main Claude session as leader; Codex, agy and qwen as tool agents) — what makes this case different, what goes wrong in practice, and which practices handle it well, both established software-engineering practice and what is known in 2025–2026 about doing it with agents.

Label rules: *verified* = I read the primary page or paper myself (raw fetch, not a summarizing tool); for arXiv papers "verified" means the abstract, plus the body where the row says so. *reported* = secondary source or search summary. Vendor documentation is verified only for "the tool does X", never for "X works"; no recommendation below rests on a vendor row alone.

| id | Finding | Label | Source |
|---|---|---|---|
| A1 | NaPiRE survey of 228 companies in 10 countries: "Incomplete and/or hidden requirements" is the most cited RE problem overall (109 of 228, 48%) and the only problem in the top 3 in every cluster. "Underspecified requirements that are too abstract" (33%) and "Moving targets" (33%) follow. The 21-problem list also includes "Stakeholders with difficulties in separating requirements from known solution designs" and "Gold plating (implementation of features without corresponding requirements)". | verified (body read) | https://arxiv.org/html/1611.10288 |
| A2 | The XY problem: the person wants X, believes Y is the way to it, and asks for help with Y; time is wasted until it emerges that X was the real need and Y was not a suitable route. The advice is to always give the broader picture with the specific ask. | verified | https://xyproblem.info/ |
| A3 | A critique of "5 whys" (Card, BMJ Quality & Safety 2017) says its popularity rests on no evidence of effectiveness and that it forces users down a single causal pathway to a single root cause. | reported (search summary; PubMed fetch returned no abstract text) | https://pubmed.ncbi.nlm.nih.gov/27590189/ |
| A4 | INVEST (Bill Wake): a story is *Testable* — writing it carries the promise "I understand what I want well enough that I could write a test for it"; if the customer does not know how to test it, the story is not clear enough or not valuable. *Estimable* depends on understanding; when it is not, split off a time-boxed "spike" to learn enough. *Negotiable*: details are co-created during development, not a contract. XP's spike: a very simple program that addresses only the question under examination; "most spikes are not good enough to keep, so expect to throw it away"; its goal is reducing risk or making an estimate reliable. | verified | https://xp123.com/invest-in-good-stories-and-smart-tasks/ ; http://www.extremeprogramming.org/rules/spike.html |
| A5 | Example Mapping (Matt Wynne, Cucumber): story card, rules (blue), examples (green), questions nobody present can answer (red), captured and moved past. A table covered in red means "still a lot to learn"; many blue means the story should be sliced. Time-box about 25 minutes for a well-understood story; if it cannot be done, the story is too big or too uncertain — slice it or send the product person to do homework. A thumb vote decides readiness; minor open questions may be resolved during the work. Obvious rules need no examples. | verified | https://cucumber.io/blog/bdd/example-mapping-introduction/ |
| A6 | Fowler on Specification by Example: examples are usually much easier to come up with than pre/post-conditions, "particularly for the non-nerds"; stating behaviour once as examples and once as code gives a double-check whose value comes from the two sides being written differently; checking a design against examples is easy, unlike against formal specs. It "can't be the only requirements technique you use". | verified | https://martinfowler.com/bliki/SpecificationByExample.html |
| A7 | Mike Cohn on Definition of Ready: a DoR is a gate; rules requiring something be 100% done before work starts turn it into a stage-gate (waterfall) process. He does not recommend a DoR for most teams; where used, avoid "100% done" rules and prefer guidelines, e.g. replace "detailed mock-ups of all new screens before start" with a conditional, partial version. | verified | https://www.mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready |
| A8 | User story mapping (Jeff Patton): a flat backlog is a poor explanation of what a system does; the map keeps the whole product in view; the stories placed highest describe the smallest end-to-end system, the "walking skeleton", which he builds first. | verified | https://jpattonassociates.com/the-new-backlog/ |
| A9 | Impact mapping (Adzic): puts deliverables in the context of the impacts they are meant to achieve, visualises the underlying assumptions so they can be tested, and is meant to stop scope creep, over-engineered solutions and "unrealistic projects ... before they cost too much". | verified (the method's own site; benefit claims are the author's) | https://www.impactmapping.org/about.html |
| A10 | Ambig-SWE (ICLR 2026; underspecified SWE-bench Verified): interaction recovers up to 74% over non-interactive runs on underspecified inputs, but "LLMs default to non-interactive behavior without explicit encouragement", and even when encouraged they struggle to tell underspecified from well-specified tasks; prompt engineering gives limited, model-dependent improvement. Only Claude Sonnet 4 / 3.5 reached notable detection accuracy (89% / 84%). Models rarely recover if they do not engage within the first turns. | verified (body read) | https://arxiv.org/abs/2502.13069 ; https://arxiv.org/html/2502.13069 |
| A11 | Same paper: Qwen 3 Coder showed "complete non-responsiveness to interaction prompts (100% FNR)". The most effective questions are "specific, actionable, and task-level"; vague questions or questions about implementation details recoverable from the codebase add little. Limitation: the simulated user may be more cooperative than real users. | verified (body read) | https://arxiv.org/html/2502.13069 |
| A12 | "Ask or Assume?" (2026): a scaffold that decouples underspecification detection from code execution (separate agents) reaches 69.4% resolve rate on underspecified SWE-bench Verified, beats a single-agent setup and closes the gap to fully specified instructions; it asks little on simple tasks and more on complex ones. | verified (abstract) | https://arxiv.org/abs/2603.26233 |
| A13 | UnderSpecBench (2026), Claude Code, Codex and OpenCode on DevOps tasks with varied intent clarity, target certainty and blast radius: "underspecification does not mainly make agents fail; it makes them guess"; 55.8–67.8% of runs violate at least one action boundary; blast-radius cues barely reduce the urge to act. | verified (abstract) | https://arxiv.org/abs/2607.02294 |
| A14 | ClarifyCodeBench (2026): strong code generation does not imply good requirement clarification; more reasoning raises code correctness but barely improves ambiguity detection; clarification quality "degrades sharply as the density of ambiguities increases". | verified (abstract) | https://arxiv.org/abs/2607.00711 |
| A15 | CLARITI (2026): effective clarification has two properties — task relevance (the information predicts success) and user answerability (the user can realistically provide it); a module trained on these matched GPT-5's resolution rate on underspecified issues with 41% fewer questions. | verified (abstract) | https://arxiv.org/abs/2604.14624 |
| A16 | "Beyond Code Generation" (2025): code LLMs by default deliver one point solution that "obscures the larger space of possible alternatives"; an IDE that surfaces alternative problem framings and tracks implicit decisions made by the programmer or the LLM helped users explore, but users struggled with information overload and keeping up with LLM-originated changes. | verified (abstract) | https://arxiv.org/abs/2503.06911 |
| A17 | GitHub Spec Kit `specify` command (tool behaviour): make informed guesses and record them in an Assumptions section; at most 3 `[NEEDS CLARIFICATION]` markers, only where the choice changes scope/UX, has several reasonable readings and no reasonable default; priority scope > security/privacy > UX > technical; questions are presented together, each with suggested answers; spec checklist requires no markers left, testable requirements, measurable technology-agnostic success criteria. | verified (tool template; no evidence of effect) | https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/specify.md |
| A18 | Spec Kit `clarify` command (tool behaviour): scans the spec against a fixed taxonomy (scope, domain/data, UX flow, non-functional, integrations, edge cases, constraints, terminology, completion signals, vague adjectives) marking Clear/Partial/Missing; at most 5 questions ranked by impact × uncertainty; each multiple-choice (2–5 options) or ≤5-word answer, with a recommended option and a "why it matters" line; asked one at a time; each Q→A logged in a Clarifications section and applied to the spec at once. Skipping it is allowed (e.g. a spike) but must warn that rework risk rises. | verified (tool template; no evidence of effect) | https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/clarify.md |
| A19 | Spec Kit "assess" extension (tool behaviour): intake → research (supporting *and opposing* evidence) → define (users, problem, goals, non-goals, success metrics, cost of doing nothing) → shape (concept-level options) → decide, ending go / needs-clarification / kill; "stopping is a successful outcome"; touches no source code. | verified (tool docs; no evidence of effect) | https://github.github.io/spec-kit/guides/assessment.html |
| A20 | Kiro (tool behaviour): requirements in EARS form ("WHEN <condition> THE SYSTEM SHALL <behaviour>"); two variants — Requirements-First (you know the behaviour) and Design-First (you have an architecture or must explore feasibility first); feature specs are "not ideal for exploratory coding without clear goals". An "Analyze Requirements" step reasons across the whole requirement set for contradictions, ambiguous words ("large files", "fast"), conflicting constraints, unstated assumptions and missing edge cases, and turns them into questions with suggested fixes. | verified (vendor docs; no evidence of effect) | https://kiro.dev/docs/specs/feature-specs/ ; https://kiro.dev/docs/specs/analyze-requirements/ |
| A21 | Böckeler (Thoughtworks) trying Kiro, spec-kit and Tessl: distinguishes spec-first / spec-anchored / spec-as-source; Kiro turned a small bug into 4 user stories with 16 acceptance criteria ("a sledgehammer to crack a nut"); spec review was tedious ("I'd rather review code than all these markdown files"); agents both ignored spec notes (re-generated existing classes as new) and over-followed them; she is "very skeptical that lots of up-front spec design is a good idea" and favours small iterative steps. | verified | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html |
| A22 | Claude Code best practices (vendor docs): for larger features, have Claude interview you with the AskUserQuestion tool ("don't ask obvious questions, dig into the hard parts"), write SPEC.md, then implement in a fresh session; the most useful specs name files and interfaces, state what is out of scope, and end with an end-to-end verification step. Skip planning when the diff fits in one sentence. | verified (vendor docs; no evidence of effect) | https://code.claude.com/docs/en/best-practices.md |
| A23 | "Are delayed issues harder to resolve?" (171 projects, 2006–2014): no consistent evidence that issues cost more to fix later; the delayed-issue effect "might be an historical relic that occurs intermittently". | verified (abstract) | https://arxiv.org/abs/1609.04886 |
| A24 | Practitioner report: treat an AI-generated prototype as an "executable requirements draft"; the code is throwaway (code-and-fix, missing error handling, possible security flaws); an agent then extracts actors, use cases, rules, scenarios, failure modes and edge cases from it, the result is aligned with stakeholders, and only then is the real system built. Speed claims (3–10×) are the author's own. | reported (single practitioner blog) | https://dev.to/valentineshi-dev/ai-prototype-as-an-executable-requirements-draft-k73 |
| A25 | "Prototyping with Prompts" (CHI'25, 39 professionals): generative-AI prototyping is fast and iterative, but a named challenge is "overfitting the design to specific example content". | verified (abstract) | https://arxiv.org/abs/2402.17721 |

## What makes this case different

- **The truth is not written anywhere yet.** In B the oracle is the old system, in C the existing code plus a stated
  requirement, in D a blueprint EJ is expected to be able to write. In A the requirement exists only partly, in EJ's
  head, and part of it does not exist until EJ reacts to something concrete. So the lead-in is *discovery*, not
  extraction or confirmation (A1: "hidden" requirements; A4: Negotiable — details co-created).
- **The ask may be a solution, not the need.** The most common failure has a name on both sides: the XY problem (A2)
  and NaPiRE's "stakeholders who cannot separate requirements from known solution designs" (A1). Case A is where why
  #1 of method 3.0 does real work.
- **The failure is invisible to the build loop.** Steps 3–5 of the pipeline (dev ∥ tester, review, fix loop) check
  the build against the accepted criteria. If the criteria are wrong, every check passes and the feature is still
  wrong — validation risk, not verification risk. Only EJ can catch it.
- **Agents make it worse by default.** Tool agents guess rather than ask (A10, A13), cannot reliably tell when a task
  is underspecified (A10, A14), and some do not ask at all (A11: Qwen 3 Coder). A tool agent handed an unclear brief
  will return plausible code built on silent decisions (A16).
- **"Done" for the lead-in is EJ's acceptance, not a script.** Its stop condition is a human check, so its cost is
  EJ's attention — which makes the number and shape of questions, and the size of the spec to review, the main design
  levers (A15, A18, A21).

## What goes wrong

1. **Building the stated solution instead of the need** (A1, A2). The build is correct and useless.
2. **Silent guessing by agents** (A10, A13, A16). The dev agent fills gaps with defaults EJ never saw; the blind
   tester, reading the same gaps, may guess *differently* — which surfaces as a test failure that is really an
   unasked question.
3. **Too many or poor questions.** Long question lists, questions about things the agent could find in the code, or
   questions EJ cannot answer cost attention and get rubber-stamped (A11, A15). Clarification quality also drops as
   the number of ambiguities rises (A14), so a very vague feature gets the worst questions exactly when it needs the
   best.
4. **Spec bloat.** Agent-drafted requirements inflate (4 stories / 16 criteria for a small bug), review becomes the
   bottleneck, and the agents still do not follow all of it (A21).
5. **Untestable criteria accepted.** Words like "fast", "robust", "large" pass review and leave the tester without an
   oracle (A4 Testable; A18 vague-adjective scan; A20 Analyze).
6. **Gate turns into waterfall.** "Nothing builds until everything is settled" stalls when some answers only come
   from seeing something work (A7). The evidence that late fixes are always far costlier is weaker than folklore says
   (A23), which weakens the case for settling *everything* up front.
7. **Prototype misuse.** A throwaway prototype gets promoted to product (A24: it lacks error handling and may be
   insecure), or EJ's answers overfit to the prototype's example content (A25), or the prototype's own implicit
   decisions are accepted unseen (A16).
8. **Single-path whys.** Asking "why" in one chain converges on one story too early (A3, reported only).

## Recommended handling for EJ's method (each point citing finding ids; mark anything that is your inference)

Concrete changes to the case-A lead-in in `docs/TASK_TYPES.md` (Lead-in by case, row A):

1. **Add, first: a one-screen problem statement EJ accepts before any question batch** — the need behind the ask
   (why #1), who it is for, non-goals, how EJ would know it worked, and the cost of not doing it — with **"stop / not
   now" as an allowed, successful exit**. Today the row starts at "one batch of questions"; this puts the XY guard and
   the kill option ahead of R-blocks. (A1, A2, A9, A19; the form follows A19's define step. *Inference*: that this
   fits as part of blueprint section 1/2 rather than a new artifact.)
2. **Tighten the question batch: at most 5 questions, ranked by impact × uncertainty; each multiple-choice or a
   few-word answer with the COO's recommended option and one "why it matters" line; only questions EJ can actually
   answer — anything recoverable from the code or the web becomes a research piece, not a question.** Everything not
   asked is written as an explicit *Assumptions* list attached to the R-blocks, so EJ accepts it with them. The row's
   "each with a provisional answer" already matches; the cap, the filter and the assumptions list are the additions.
   (A11, A15, A17, A18; non-vendor support from A10/A11/A15 — the vendor rows only show the same shape is in use.)
3. **Make examples mandatory, prototypes conditional.** Replace "Examples or a throwaway prototype may help EJ
   decide" with: (a) every R-block carries at least one concrete example (input → expected result) alongside its
   criteria; a criterion EJ cannot state as an example or test is a question, not a criterion (already the blueprint
   template's rule — make the lead-in enforce it); (b) a prototype is built only for a question EJ cannot answer in
   words (flow, look, feel), time-boxed, outside the product tree, deleted after use; the COO then lists the
   requirements *and the implicit decisions* the prototype embodies and EJ accepts that list — never the prototype.
   (A4, A5, A6, A16, A24, A25. *Inference*: the specific placement outside the product tree and the deletion rule.)
4. **Add a COO consistency pass over the drafted R-blocks before EJ sees them** — contradictions between
   requirements, vague adjectives, unstated assumptions, missing edge/error cases — turned into the (capped) question
   batch rather than shown as a report. (A18, A20 as the pattern; A14 as the reason it should be a separate, deliberate
   step. *Inference*: run it by the COO, not a tool agent, given A11.)
5. **Reorder for very unclear features: settle the walking skeleton first.** When the question batch hits the cap with
   high-impact questions still open (or many "red cards"), do not try to settle the whole feature: settle R-blocks for
   the thinnest end-to-end slice, run the unchanged steps 3–5 on it, show EJ the working slice, and let that drive the
   next R-blocks. The "no piece builds until settled" rule stays — but per slice, not per feature. (A5, A7, A8, A23.
   *Inference*, and it changes how many times the pipeline runs per feature — see Decision.)
6. **Put a "stop on unclear" clause in every tool-agent brief (dev and tester).** A tool agent that meets a gap
   returns `UNCLEAR: <question> / <the guess it would make>` instead of guessing; the COO answers from the R-blocks or
   adds it to the next EJ batch. Do not rely on Codex/qwen to ask unprompted; for qwen, expect it not to ask at all.
   Detection stays with the COO as its own step. (A10, A11, A12, A13.)
7. **Keep the R-block set small and record the answers.** If the draft exceeds a size limit (EJ to set; *inference*),
   slice the feature instead of reviewing a long spec; log each Q→A under the R-blocks (or `decisions.md`) so the
   tester's oracle traces back to EJ's own words. (A5 "many blue cards → slice", A18 Clarifications log, A21 bloat.)

Kept as is (supported): the tester's oracle being the accepted criteria, written blind from them — with examples
added (point 3) this is Fowler's double-check (A6); and the COO, not a tool agent, owning the lead-in (A10–A12).

## Gaps

- **No study of the setting itself** — one developer directing several agents through a written method. All agent
  evidence is from benchmarks with *simulated* users who may be more cooperative than EJ (A11), on mostly older
  models (Sonnet 4, Qwen 3 Coder, GPT-5); nothing on Codex GPT-6-sol or agy. Unknown whether A10/A11 still hold.
- **Batch versus one-at-a-time questions: unknown.** Spec Kit itself does both (`specify` batches up to 3, `clarify`
  asks 5 one at a time; A17, A18). No evidence found on which costs a single owner less attention.
- **AI prototypes as an elicitation tool:** only a practitioner report (A24) and one adjacent CHI study (A25); no
  controlled evidence that it improves the requirements.
- **Spec-driven tools' effect on outcomes:** no controlled evaluation found; the tool rows (A17–A20, A22) show
  practice, not benefit, and one experienced practitioner is sceptical (A21).
- **Not read in primary form:** the 5-whys critique (A3, PubMed blocked), Adzic's *Specification by Example* book
  (only its page), the original EARS paper. Story mapping and impact mapping are read from their authors' sites, not
  from independent evaluations.
- **The walking-skeleton reorder (point 5) is my inference** and interacts with the pipeline's fixed rounds and the
  join check; it is n=0 like the rest of the row.
