# Provisional decisions — leftovers run (time-boxed, 2026-10-17)

The COO made each decision provisionally from the six experts' answers in `experts-leftovers/`, under method 3.8
item 14 (EJ gave a time box). EJ may overrule any of them. The requirements document is not changed. The wording
below is a proposal for EJ, and the tests follow it.

| # | Question | Decision (COO, provisional) | Experts (all six) |
|---|---|---|---|
| 1 | Does a known link that the tool marks `dynamic` count as missing? | No, when a limit at its site names why. A limit that contradicts the code still fails. A2's line, proposed: "a known link within the depth is missing with no limit at its site naming why, or a shown link or a limit contradicts the code". So a call the type checker resolves, marked `dynamic` instead of linked, fails. | a: Dario, 孫子, Dave, 老子 (Dave added the "or a limit" clause; 老子 wants no words added). b: Linus, 范蠡. Dave's clause meets the concern behind b: a false `dynamic` label on a link the checker resolves still fails. |
| 2 | Does going into a body written straight into a call add a level? | No. Proposed sentence for A2 (范蠡): "Going into a body written straight into a call adds no level." | a: all six. |
| 3 | What does "known" mean? | "established from repository source or type information" | b: Linus, Dario, Dave. c: 孫子, 范蠡, 老子. A 3–3 tie. The COO picks b for two reasons. A key writer can establish it without the tool's own method (Dave). And decision 1's clause no longer needs c. |
| 4 | Does A5 add "a limit the interface requires for that command is part of the answer"? | No: "its limits" already covers it. Dave's check, which would switch this to yes: a planted copy that drops the limit "fake rule not set (A3)" must be caught by A5's line. | b: Dario, 孫子, Dave, 范蠡. a: Linus, 老子. |
| 5 | One Fails-if line naming both actors, or a tool line and an agent line? | A tool line and an agent line, inside one A2 and one A5. | b: all six. |
| 6 | A3's fake rule on opencode | This run passes no `--fake-rule` on opencode. Tests that pass through a fake go to `undecided`: they are listed, not counted, and the answer carries the limit "fake rule not set (A3)". | a: Linus, 孫子, 老子 (老子: exclude them, with one limit naming how many were left out). b: Dario. c: Dave, 范蠡. The decision keeps a's core: fake-path tests are not counted. It keeps 老子's: the answer says how many there are. It lists them, because of the over-marking Dave and 范蠡 point to in the spec: `throughFake` marks every path through a call site whose candidates include a fake. |
| 7 | A1's sibling rule on opencode | One glob per sibling group, given per module. The interface or service-tag rule chooses the globs and checks them: every file a glob matches implements that group's tag. | c: all six. |
| 8 | What counts as a test file? | The tool has no default; the user passes `--tests`. On opencode, the run passes files under `test/` or `__tests__`, or named `*.test.ts` or `*.spec.ts`. | b in the tool, a on opencode: all six. |
