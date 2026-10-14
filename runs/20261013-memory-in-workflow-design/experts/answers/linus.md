# Linus Torvalds — Should workflows specify memory use?

## Answer

**My reading: partly**—agents have memory mechanisms, but reliable decisions about reading, writing and keeping memory across these engines are not established. **Yes**—make one change to §4: replace its project-memory prescription with a reference to EJ’s accepted design and an explicit memory contract in each node’s existing fields.

## How I decided

1. **My #2 and my #7: separate capability from demonstrated reliability.** Report §1 describes mechanisms; §2 and §7 leave their practical quality unmeasured. Codex generates memories in the background when enabled, so this is not simply the working model independently deciding what to remember. The current [OpenAI documentation](https://learn.chatgpt.com/docs/customization/memories) confirms that distinction. My answer is *partly*, rather than a claim that every current agent manages memory poorly.

2. **My #2: the evidence supports making delivery deliberate, with limits.** Responding to report §5/O1: Vercel’s experiment concerns discovery of a documentation skill and index, not every kind of memory. [VibeMemBench](https://arxiv.org/abs/2609.23570) also selected tasks where injected experience had already helped a reference solver. **My reading:** these results justify testing deliberate delivery; they do not establish that loading more memory universally improves work.

3. **My #9 and my #10: fit memory into the existing flow of information.** Responding to report §4: Context, Contract, Evidence and State already describe inputs, outputs and checks. Memory can use those fields. The report also identifies conflicting layouts; the brief establishes `SOURCE_OF_TRUTH.md` as accepted, so my recommendation references that policy instead of maintaining another prescription.

   **Proposed replacement in §4, my reading:** For task and project memory, the workflow designer **SHOULD** specify each node’s memory inputs, delivery mechanism and timing, required outputs and write timing, and checks in its existing Context, Contract and State fields, following the accepted [Write, Keep and Read policy](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md).

4. **My #13 and my #5: start with that change and keep it reversible.** Responding to report §5/O3–O5: an additional evaluator, automatic expiry or per-engine memory controls would each need evidence of a problem they solve. EJ’s accepted design already specifies checking before use, preserving superseded claims, and reporting contradictions. **My reading:** connecting that policy to node contracts is the immediate need.

5. **My reading: check the proposed requirement.** It passes **source** (my proposal), **one thing** (declaring a node’s memory contract), **unit** (each node), **can it fail** (missing delivery timing or output check), **weak words** (named contract contents), **level** (SHOULD), **basis** (a proposal, n=0, reviewed after the test below), and **links** (the existing node fields and accepted policy). Its performance benefit remains **not measured**. EJ’s ranking of memory and information is also **not measured**; this recommendation does not depend on that ranking.

## What I need to know

What additional token cost or elapsed time would EJ accept for fewer missed decisions and better handoffs? That answer determines whether the proposed change earns its ongoing cost.

## Costs and risks

- **My #18, attributed:** more brief preparation, input tokens and checking time. The amount is **not measured**.
- **My #7:** delivering memory does not establish that the agent understood or followed it.
- **My #9, my reading:** memory selection must respect the existing information boundaries; a verifier could otherwise receive the worker’s reasoning through stored notes.
- **My #5:** the method paragraph is reversible, but time already spent preparing unnecessary contracts is not recovered.

## How we would know I was right

**Proposed test—written by me, applying my #2, my #3 and my #18 (attributed):** compare the current method with the explicit contract on matched repository tasks, keeping the engine, model and memory settings fixed.

Include a fresh-session handoff, a relevant prior decision, and an entry contradicted by current code. Observe whether the agent resumes the correct next step, follows the decision, reports the contradiction under Rd5.3, and returns the required records. Measure task outcomes, memory mistakes, tokens and elapsed time.

The change earns its place if it improves those outcomes within EJ’s accepted cost. Contract completeness alone would not establish that.