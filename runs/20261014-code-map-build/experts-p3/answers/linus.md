# Linus Torvalds — Can P3 pass with wrong results?

## Answer

**P3 — not loop-ready as written:** the evaluator command is incomplete, R1 depends on later features, and the answer checks accept concrete false claims. Strengthen the semantic checks before freezing them, separate R1’s execution check from answer correctness, and preserve user workflows explicitly; the price is additional checker work before building starts.

## How I decided

1. **My #2 — inspect the executable check.** The brief’s evaluator command omits `--out`. I called its argument parser with those arguments; it rejects them before evaluation. Supply the required output destination. Evidence: [run.ts](/home/smoke01/dev/ancient-games/code_map/eval/run.ts:12).

2. **My #19 (`attributed`) — each increment needs a check it can satisfy independently.** My reading: the stated R1 coupling defeats the one-requirement-per-round sequence. A safe reader with unfinished chains or test discovery cannot finish R1, although its execution behavior is correct. Separate marker execution observations from semantic answer checks, retaining both in the full suite. This costs evaluator changes and means an R1 pass establishes safe reading only.

3. **My #2 and my #9 — check the claimed relationships, rather than merely their shape.** P2 Codex wrote the evaluator independently of the future builder. I exercised its matcher and validator with unchanged canned answers and then mutated answers in memory:

   | Plant | Result |
   |---|---|
   | Replace a sibling cell’s source text with `return value + 999;` | Accepted |
   | Replace a nested flow return with `return 999;` | Accepted |
   | Start the requested chain from `level8`, which calls nothing | Accepted |
   | Put a test-path call site on the leaf’s return statement | Accepted |
   | Attach an unsolicited six-level chain to a `where` answer | Accepted |

   Every case sharing each mutated command also accepted it. The unchanged answers passed all 37 answer checks; a wrong test count produced two mismatches as a control. **My reading:** these are demonstrated holes in the answer checks. My probes do not establish runtime safety, future tool correctness, or whether the unwritten frozen tests will catch them.

4. **My #9 — strengthen the checks where the relationships are missing.** Validate sibling text and nested flow text against their source locations; verify chain roots and parent-to-child connections; verify test-path call sites and endpoints; reject answer sections unrelated to the requested command. These repairs target the five demonstrated failures in [contract.ts](/home/smoke01/dev/ancient-games/code_map/eval/contract.ts:65) and [matcher.ts](/home/smoke01/dev/ancient-games/code_map/eval/matcher.ts:56). Their cost is additional expected evidence and validation logic. Location plausibility alone is insufficient.

5. **My #1 and my #3 — preserve users’ results.** Earlier requirements remaining MET protects only behavior those checks exercise. The bundled cases always supply test patterns and request JSON, so they do not establish correct behavior without `--tests` or in default text mode. Freeze regression cases for those specified workflows and any existing user workflows before accepting changes. If an existing baseline exists, replay its inputs and compare useful results. Real opencode checks arrive in P4, so P3 passing fixtures cannot establish correctness on opencode.

6. **My #7 — keep uncertainty visible.** The evaluator’s own notes say network isolation cannot detect a caught connection attempt, and snapshots miss writes outside the observed trees. Nevertheless, its bounded R3 observations can report MET. **My reading:** that status cannot establish the entire privacy requirement. Separately check the protected paths and git boundary, and retain explicit unchecked scope. Likewise, A2 candidate selection, A3 asking the user, and A5 user intent remain P6 checks. Evidence: [SPEC_QUESTIONS.md](/home/smoke01/dev/ancient-games/code_map/eval/SPEC_QUESTIONS.md).

## What I need to know

- Which existing user workflows, if any, have a last working baseline? If none exist, the regression baseline is the accepted interface and accumulated checked examples.
- For R3, which private paths and git boundary are protected, and is P3 intended to accept only the bounded tool checks or the whole privacy promise? The current evaluator establishes only the former.

## Costs and risks

- **My #19 (`attributed`):** separating R1 checks costs setup work; its narrower pass must not imply later features work.
- **My #18 (`attributed`):** source-backed semantic checks require more answer-key maintenance and can become brittle if they prescribe incidental formatting.
- **My #1 and my #3:** workflow replay adds verification time; omitted workflows remain exposed to regressions.
- **My #7:** honest unchecked privacy scope may prevent an unconditional R3 pass.
- **My #2:** new tests still need demonstrated failures; freezing their hashes preserves them but does not establish their quality.

## How we would know I was right

The strengthened checks reject each of the five plants while accepting the unchanged controls. A safe implementation with unfinished later features passes R1’s execution check; executing the marker fails it. Frozen round tests reject a wrong implementation before accepting the repair, and later changes preserve the recorded user workflows. P4 then tests the real opencode cases; fixture success alone remains insufficient.