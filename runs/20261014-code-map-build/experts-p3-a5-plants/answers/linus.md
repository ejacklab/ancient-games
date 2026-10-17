# Linus Torvalds — Do the A5 plants justify closure?

## Answer

- **limits-dropped — enough for the exercised failures:** users lose relevant qualifications; explicit limit assertions catch that loss, although the evaluator attributes it to other requirements. **My #3.**
- **where-inside-dump — enough:** unrelated definitions bury a specific answer; matching the requested result exactly catches the actual scope failure. **My #3.**
- **site-dropped — enough:** call relationships lose their call-site evidence; location checks reject the missing evidence for the right reason. **My #2 and #3.**
- **callers-unasked-map — enough:** a caller question produces an unrequested repository dump; the frozen test rejects the extra section correctly, despite the evaluator reporting other requirement failures. **My #3.**
- **not-found-limit-dropped — not enough:** the empty-result message still explains the analysis’s limit. Rejecting the missing `not-found` record establishes an L1 contract failure, but does not alone demonstrate a user-visible A5 failure. **My #3; my reading.**

**STRENGTHEN:** have the COO extend default-text checks to reject unrequested output and verify each answer’s evidence and applicable limits; add independently chosen held-out questions exercising those failures across commands. These address A5’s dump, missing-evidence and missing-limits conditions. Keep the agent’s unasked-map behaviour explicitly pending P6.

## How I decided

1. **My #3 — judge what breaks for the user.** A failing test is evidence to examine, not the definition of broken behaviour. In particular, the fifth plant retains this meaning in rendered output: nothing found by static analysis does not establish that nothing exists. Its missing record and its remaining explanation must be distinguished.

2. **My #2 — inspect the actual checks.** Codex wrote the thirteen [frozen A5 tests](/home/smoke01/dev/ancient-games/code_map/test/a5/one-question-one-answer.test.ts); all request JSON. They check focused sections, locations and several concrete limits. Codex’s [evaluator](/home/smoke01/dev/ancient-games/code_map/eval/run.ts) validates JSON structure, but its sole bundled default-text case only requires a name and location to appear. It does not reject additional text.

3. **My #2 and #7 — demonstrate the gap and limit the claim.** I ran an in-memory probe against the existing matcher. Both a focused answer and that answer with an unrelated map appended produced **zero mismatches**. I constructed this probe; it demonstrates the matcher’s blind spot, not a complete mutated-tool run.

   A concrete escaping fault is: preserve JSON output, but append a repository map to every specific default-text answer. The frozen A5 tests remain unaffected. Bundled and renamed held-out text checks retain their required substrings. The same evaluator cannot distinguish the added output in private text cases either: its text assertions check presence, without a prohibition on extra content.

   **My reading:** this fault preserves the automated content verdicts while visibly violating A5. A complete implementation would still need to finish within existing runtime limits and pass type checking. Whether human reviewers would catch it is **not measured**.

4. **My #7 — do not overstate independence.** The COO’s [plant report](/home/smoke01/dev/ancient-games/runs/20261014-code-map-build/evidence/p3-a5-src-plants.txt) reports every plant caught by both bundled and held-out evaluation. Therefore **none is caught only by checks the builder can read**. However, renaming identifiers and shifting lines preserves the questions and their checking logic. It does not repair the text-output blind spot.

   The private set distinguishes only `site-dropped` from its existing A1/A2 failures. Its silence about the other plants does not establish that those behaviours work.

5. **My #13 — strengthen the immediate weak point.** The plants are useful, though several remove information globally. A smaller diagnostic fault would suppress just the fake-rule qualification in default-text `tests` output while preserving the result and JSON. Another would append one unrelated definition to an otherwise correct answer. These test whether the checks notice a quiet loss of qualification or focus.

6. **My reading — requirement quality.** Read with the interface, A5 passes **who decides, one thing, unit, can it fail, weak words, level, basis and links**: it concerns one answer, the command establishes requested scope, and concrete failures are identifiable. The weakness is its verification. Behaviour outside the exercised checks remains dependent on implementation judgment and review; agent decisions about requesting whole maps belong to P6.

## What I need to know

Do the two reviewers inspect default-text scope, evidence and limits, and has P6 checked the agent’s map requests? If so, that supplies evidence beyond these plants; otherwise those parts remain unestablished.

## Costs and risks

- **My #13:** additional text and independently chosen cases cost authoring effort and runtime. Check meaning and scope; exact whitespace comparisons would make harmless formatting changes expensive.
- **My #18 — attributed:** report the additional checking time and failures found. Neither was measured here.
- **My #7:** stronger checks reduce the demonstrated gaps; they do not establish correctness on every repository.

## How we would know I was right

The current text check accepts an appended map; the strengthened check rejects it specifically for unrequested output. It also rejects the quiet missing-qualification fault, while accepting the unchanged answer in both formats. The COO’s independent cases and reviewers then establish which A5 behaviours were actually exercised, with P6’s result reported separately.