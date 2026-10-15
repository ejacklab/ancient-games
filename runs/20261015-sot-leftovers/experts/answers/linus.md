# Linus Torvalds — Missing facts and reversible choices

## Answer

My reading: keep this a small document repair, distinguish policy decisions from missing measurements, and make each change independently reversible.

- **U1:** support correcting `covers` conditionally; do not assume changing `source` or `depends_on` always preserves the claim.
- **U2:** recommend the project owner as decider; EJ must confirm.
- **U3:** recommend keeping the example limits and deferring the tool build; this records an implementation gap rather than proving Rd3.1a satisfied.
- **U4:** defer measurements as scoped; retain the uncertainty explicitly.
- **U5:** support design-relative paths if the referenced files accompany the design.
- **N1 — Metadata merges:** resolve the conflict U1 would introduce with W6.3a.
- **N2 — Reviewer context:** give P3 EJ’s accepted decisions, while withholding the worker’s reasoning.
- **N3 — Final review coverage:** include the release-note edit and any subsequent repairs in the reviewed result.

## How I decided

1. **U1 and N1 — my #9, my #3, my #5.** Start with what the fields mean and who consumes them. Correcting a renamed file’s `covers` path can preserve the claim. Replacing its evidence or dependencies can change why the claim is justified, even when its wording stays identical. The missing fact is whether existing readers or checks rely on those fields remaining unchanged.

   There is also a concrete linked requirement: W6.3a assumes conflicts occur only in added lines and directs the merger to keep both sides. If U1 permits replacing metadata values, two branches can make competing corrections; retaining both can preserve a stale or contradictory value. **My reading:** U1 needs a corresponding examination of W6.3a, not just K4.3 and its prose repetition.

   For reversibility, retain the original values in git and the required change log, demonstrate the proposed correction on a disposable example, and avoid migrating existing entries before EJ settles the policy. Price: checking consumers and merge behavior takes additional review.

2. **U2, U3 and U4 — my #4, my #2, my #13.** Choosing which agents belong to a project is an ownership decision. Discovering their effective limits is technical work. Naming the owner answers the first; it does not supply the second.

   Requirement-check of Rd3.1a: **pass** — one thing, can it fail, weak words, level, basis as a design objective, links as stated; **FAIL/open** — who decides, and unit because the operative limits and their comparable units have not been supplied. Separately, the current example values are not evidence that its tool check enforces the objective.

   My recommendation is conditional: if EJ accepts recording that gap, retain the existing tool and defer measurements and configuration work. Keep Rd3.1a’s target distinct from the implementation’s example cutoff. Price: actual compatibility remains unverified.

3. **U5 — my #9, my #2, my #5.** A relative path specifies where to look; it does not supply the referenced file. The missing fact is what accompanies this design when another project adopts it.

   If the design travels with its vision file and `CACHES.md`, design-relative references are a small repair. Check resolution from a relocated copy outside the original repository. If those files do not travel with it, EJ needs to decide the dependency arrangement. Price: the first option carries supporting documents; the second leaves a distribution decision open.

4. **N2 — my #11; my #18, whose words are labelled `attributed`.** The workflow says P3 judges P2 against P1’s decisions, but its listed context does not explicitly provide those decisions. Withhold the COO’s reasoning; provide the accepted rules and acceptance criteria. Otherwise the reviewer can mistake a deliberate decision for a defect. Price: preparing a concise, neutral decision record.

5. **N3 and rollback — my #5, my #12; my #19, labelled `attributed`.** P3 checks the release note, but P4 adds its entry and may repair findings afterward. Review evidence therefore may describe an earlier result. Review the final changed material before acceptance.

   Also, `git diff` displays changes; it does not undo them. Preserve the starting state and separable patches so a mistaken repair can be reversed without removing unrelated work. Price: an additional review of later edits and modest patch bookkeeping.

## What I need to know

- **U1/N1:** Does EJ intend only corrections that preserve meaning, or also changes to evidence and dependencies? Who settles competing metadata corrections?
- **U2:** Does EJ confirm the project owner chooses the participating agents?
- **U3/U4:** Does EJ accept closing L5 as a recorded decision with the measurement and implementation gap still open?
- **U5:** Which supporting files accompany the design into another project?

## Costs and risks

- **U1/N1 — my #9, my #5:** broader metadata mutability makes repairs easier but introduces semantic and merge conflicts.
- **U2–U4 — my #2, my #13:** deferral saves implementation work while leaving engine compatibility unmeasured.
- **U5 — my #9:** portability requires an explicit dependency arrangement.
- **N2/N3 — my #11, my #19 (`attributed`):** complete review context and final-edit coverage cost preparation and review time.
- **Rollback — my #5, my #12:** reverting text cannot automatically undo decisions another project has already acted on.

## How we would know I was right

The final documents agree with EJ’s recorded decisions; a renamed-path example preserves the claim and history; competing metadata corrections receive the intended resolution; references resolve after relocation; and the final reviewed diff includes the release note and repairs.

The COO-authored structural and path checks support their stated checks only. Finding the planted contradiction demonstrates detection of that contradiction. Neither establishes that the example limits fit every participating engine; that remains **not measured**.