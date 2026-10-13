# Linus Torvalds — Where I help in EJ’s workflow

## Answer

**My reading:** Given concrete artifacts, my strongest placements are **3.2 write the algorithm**, **3.5 check the loops**, and **3.3 examine unclear decisions**; the size and reliability of that help are **not measured**. The main agent should ask me, respectively: *Does this algorithm follow the data and solve the immediate problem without unnecessary machinery?*; *Could this check pass while the requested result is wrong or an existing user workflow breaks?*; and *Which choices depend on missing technical facts, and what would make a mistaken choice reversible?*

## How I decided

1. **3.2 — Review the algorithm through its data.**  
   My #9 puts data structures and their relationships before code; my #10 looks for representations that remove special cases; my #13 challenges design that serves no immediate need. **My reading:** given the algorithm, inputs, outputs and state format, I can identify concrete mismatches and suggest simpler alternatives. This also supports reviewing the contracts in 3.6. I cannot establish that a proposed simplification works without execution evidence.

2. **3.5 — Challenge what the check establishes.**  
   My #2 asks for implementation evidence. My #1 and my #3 distinguish preserving users’ working outcomes from merely satisfying documents or tests. My #18 adds quantified benefits and explicit costs, but is labelled `attributed` kernel guidance, not demonstrated personal wording. **My reading:** compare the proposed check with the requested outcome and supplied examples of existing use. A useful contribution is a concrete failure the check would miss—not another declaration that the design looks sound.

3. **3.3 — Expose decisions made without the details.**  
   My #4 and my #6 defer technical judgment to those who know the details; my #5 examines whether damage can actually be undone; my #7 keeps advice preliminary. **My reading:** I can identify missing evidence, distinguish a reversible experiment from a lasting commitment, and frame the question for the person with the needed knowledge. This advises EJ’s decision without taking it over.

## What I need to know

None to identify these placements. For a concrete consultation:

- What immediate outcome, algorithm and data formats are being reviewed?
- Which existing user workflows must continue working, and what evidence covers them?
- What alternatives, constraints and rollback consequences are known?

If those facts are absent, I can identify gaps; I cannot reliably choose the implementation or certify its checks.

## Costs and risks

- **Algorithm review — my #9, my #10, my #13:** simplifying around today’s need may overlook a supplied future requirement. Moving these software rules into agent workflow design is **my reading**, not measured evidence.
- **Check review — my #1, my #2, my #3:** representative user cases cost effort to obtain. Reviewing a check cannot prove that execution passed or that unrepresented users are protected.
- **Decision review — my #4–my #7:** obtaining missing facts can delay work. A code rollback may still leave lost time or damaged trust; my #5 explicitly recognises that limit.
- **Unreliable placement — 3.0 deciding EJ’s purpose:** my #6 warns that ability in one area does not transfer automatically; my #13 supplies no basis for inventing their vision.
- **Unreliable placement — 3.4 choosing exact engines, budgets or concurrency:** my rules provide no comparative measurements. My #2 and attributed my #18 support demanding evidence, not manufacturing numbers.

## How we would know I was right

**My proposed test, not measured:** compare reviews with and without this consultation on the same supplied artifacts. Have a reviewer other than me check each finding against the artifact and subsequent execution: confirmed defects found, unsupported objections, user breakage prevented, and added review cost.

That reviewer’s check would test my contributions on those cases. It would not establish general reliability or “huge” benefit without repeated results.