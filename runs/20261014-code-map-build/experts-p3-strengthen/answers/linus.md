# Linus Torvalds — Checks that can still pass wrong answers

## Answer

**My reading:** keep the COO’s proposal, but strengthen it to check complete relationships, relevant limits and surplus output. I reproduced two false passes in the current evaluator; the proposed cases alone would not eliminate their underlying causes.

**A5**

All changes below serve A5’s existing Fails-if line.

- **Keep evidence checks; add connected evidence.** Exercise `callers`, `callees`, nested `chain` links and test paths. Require the expected caller, call site and target on the **same link**, rather than accepting their locations anywhere in the answer. Plant missing and substituted evidence. **My #9. Cost:** more explicit answer keys.
- **Keep named-limit cases; check their meaning.** Use not-found and a service answer affected by absent `--tests`. Check the expected reason, explanatory text and location where applicable. An unrelated limit elsewhere must not satisfy the case. Keep a valid `limits: []` control where no limit applies. **My #2. Cost:** maintaining expectations for when classification actually changes an answer.
- **Keep section checks; close the ambiguity exception.** Exercise link commands and preserve candidate-only answers for ambiguous names. The [current contract](/home/smoke01/dev/ancient-games/code_map/eval/contract.ts:83) already rejects command-inappropriate top-level sections; strengthen that mechanism rather than duplicate it. Also reject unrelated content hidden inside an otherwise permitted payload. **My #10. Cost:** defining the permitted answer content precisely.
- **Keep text checks; cut the blanket exclusion of unasked places.** A callee’s implementation, declaration and call site may legitimately be outside the place named in the question. Check required answer facts, evidence and limits, and reject unrelated definitions or map material. Do not rely only on required substrings. **My #3. Cost:** text checks need semantic expectations without freezing incidental formatting.
- **Keep held-out execution; add A5-specific fault attribution.** Generate the new cases into the held-out copy, including relocated text expectations and case-specific test patterns. For each failure mode, demonstrate that its mutation makes **A5** NOT MET. **My #2. Cost:** mutation runs and generator verification.

**Wording proposal for the owner — my reading:** the confirmed failures already violate A5; they do not require weaker or broader wording. To settle its scope boundary, propose:

*A specific answer contains the requested result, its supporting evidence, applicable limits and any candidates needed to resolve ambiguity. It excludes unrelated definitions, links, flows and tables, whether they appear in another section or inside the requested payload. This applies to JSON and default text output.*

Price: the owner must accept the boundary; a checker cannot establish their intended meaning of a dump.

**A2**

- **Keep anonymous-body cases; require traversal through them.** Tie these to the missing-known-link Fails-if line. Put known links beyond the callback or property arrow, at level 2 or deeper, in both directions. Finding the callback when queried directly is insufficient. **My #3. Cost:** expected paths depend on an agreed callback model.
- **Keep the actual `Effect.fn` service shape.** Under the same line, check callers, callees and a chain passing through the constant. Preserve the private real-code failures as external checks; write a public reproduction without copying protected source. **My #13. Cost:** the reproduction may omit a relevant detail, so it cannot replace the private check.
- **Add false-target and surplus-link checks.** Tie these to the shown-link-contradicts-code part of that line. Assert complete expected edges and reject fabricated edges, including on dynamic or unresolved cases. **My #9. Cost:** independent expected relationships require more work than location inclusion checks.
- **Add a longer-path-first shared-node case.** Tie it to both missing-known-link and repeated-function lines. For depth 3, use `root → a → shared → leaf` and `root → shared → leaf → tail`, visiting `a` first. `tail` remains within depth through the shorter route and must survive deduplication. Reverse sibling order and check again; include an upward counterpart. **My #9. Cost:** traversal may need to retain the greatest remaining depth for each function.
- **Keep a directly failing case for every A2 line.** Cover finding a known place, complete ambiguity candidates, omitted or contradictory links, missing kind/location, and repeated functions with valid references. Freeze the new shapes before the builder starts A2. Candidate selection and naming by the agent remain explicitly NOT CHECKED until the agent check. **My #2 and my #1. Cost:** additional fixtures and fault runs.

**Wording proposal for the owner — conditional, my reading:**

*If depth means shortest call distance, state: The place is level 0; each call link adds one level. Every known link reachable within the selected depth is included regardless of traversal order. Reaching a function again produces a reference without losing links reachable through a shorter path.*

The owner also needs to settle whether an inline callback is a separate chain place or belongs to its enclosing function. Checks can catch violations of either policy; they cannot choose the intended policy. Price: that choice may change expected levels and existing answers.

## How I decided

1. **My #2 — test the alleged protection.** I ran two in-memory probes against Codex’s existing evaluator:
   - A5’s default-text expectation accepted the required name and location followed by an unrelated repository dump.
   - A2’s computed-member case accepted a fabricated implementation link from `obj[key]()` to `chain/logic.ts:3`, while retaining its dynamic limit.

   Both returned zero mismatches. I wrote these probes. They establish evaluator gaps, not that the builder emits either answer.

2. **My #9 — check relationships, not bags of locations.** The [source checker](/home/smoke01/dev/ancient-games/code_map/eval/source.ts:43) checks that a call exists at the stated site and enclosing function. That does not establish that its target is the implementation claimed. Adding more syntax shapes without stronger edge expectations leaves this false pass available.

3. **My #3 — judge the resulting chain.** The snapshot’s traversal stops expansion at an already-seen function. My reading of [that traversal](/home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p3/review-a5/a1/src/commands.ts:334) is that a longer route encountered first can suppress work available through a later, shorter route. This finding is from inspection; I did not run the proposed graph against the tool.

4. **My #7 — distinguish coverage from independence.** Renaming identifiers and shifting lines preserves the bundled graph’s structure and its expected answers. Held-out execution tests adaptation to those transformations; it does not independently validate the answer key or cover a missing graph shape.

5. **My reading — requirement-quality check.** With the accepted spec and brief included:

   | Criterion | A5 | A2 |
   |---|---|---|
   | Who decides | FAIL: precise surplus-content boundary | FAIL: callback ownership and shared-node depth interpretation |
   | One thing | Pass: answering a specific question | Pass: locating and reporting its chain |
   | Unit | Pass: no missing numerical unit | Pass: depth counts levels |
   | Can it fail | Pass: remove evidence or append a dump | Pass: omit a known link |
   | Weak words | FAIL: dump boundary needs agreement | FAIL: callback/place boundary needs agreement |
   | Level | Pass: accepted round gate | Pass: accepted round gate |
   | Basis | Pass: owner’s accepted requirement | Pass: owner’s accepted requirement |
   | Links | Pass: explicit interface mapping | Pass: explicit interface mapping |

   The questions below leave those choices with the owner.

## What I need to know

- Does the owner accept the proposed A5 content boundary, allowing supporting locations while excluding unrelated material?
- For A2, do inline callbacks count as separate places and levels, and does depth mean shortest call distance?

If these choices are already recorded in an allowed source, use that decision instead of introducing another.

## Costs and risks

- **My #13:** finish A5’s checks and rerun its existing gate before closing its tool round. An A5 NOT MET result becomes attempt 2 under the stated process. A2 implementation repairs belong in A2; freeze its strengthened checks before that round starts.
- **My #18:** stronger keys cost authoring and review time. Runtime and maintenance costs are **not measured**.
- **My #7:** public tests remain visible to the builder. Hidden renamed copies offer limited variation; the private real-code cases provide different evidence, but their sufficiency is not established.
- **My #1:** retain earlier-round checks. A repair that restores one chain while losing existing results is unfinished.

## How we would know I was right

The strengthened evaluator rejects each demonstrated bad answer under its own requirement while accepting the corresponding valid answer. It also rejects missing evidence, misplaced limits, unrelated text, fabricated targets and lost depth-bounded links.

For A2, reversing sibling order preserves the reachable links and valid references. The two private `Effect.fn` cases pass after the A2 repair, with earlier requirements preserved.

These observations would support the strengthened checks on the exercised cases. They would not prove correctness on every TypeScript program.