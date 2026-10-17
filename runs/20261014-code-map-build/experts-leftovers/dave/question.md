Eight decisions for the `code-map` tool, a TypeScript tool that maps code for agents. The first target is the
opencode repository, where most calls go through Effect services. The owner gave a time box. So you decide now,
and the owner may overrule you later. For each decision, give your pick and one line of reason, based on the vision
and its use cases.

You may read only these paths in the repository:
- the requirements: `runs/20261014-code-map-vision-relay/result-trimmed.md` (the vision and its four uses, R1–R3,
  A1–A6, L1, L2);
- the tool's spec: `runs/20261014-code-map-build/spec.md`;
- the earlier wording rounds: `runs/20261014-code-map-build/experts-p3-wording-r2/compare.md` and the answers it
  names.

## Facts (filled in by the COO)

- The tool builds a link graph by type, and answers one question per command: `where`, `find`, `callers`,
  `callees`, `chain`, `tests`, `map`. The default depth is six levels each way.
- An earlier probe on opencode found 63 of 71 service tags resolve to one implementation, 7 to several and 1 to none.
  One call site has 20 implementations: 1 real one and 19 test fakes.
- In opencode most function bodies are written straight into a call: `Effect.fn("name")(function* () {...})`, or
  `Effect.gen(function* () {...})` passed as an argument.
- The spec already takes the user's rules as inputs, with no defaults: `--tests <glob>` (which files are test
  files), `--fake-rule count|exclude` (A3) and `--siblings <glob>` (A1). Decisions 6–8 pick the values the run uses
  on opencode, and what the requirement text says.

## The decisions

1. **Does a known link that the tool marks with a `dynamic` limit count as missing under A2?**
   - a. No, when a limit at its site names why. A2's line becomes "a known link within the depth is missing with no
     limit at its site naming why" (范蠡's wording).
   - b. Yes. The link is known, so marking it dynamic is a miss.
   - The COO's pick: a.
2. **Does going into a body written straight into a call add a level?**
   - a. No. The body is its own place, but entering it is not a step in the chain.
   - b. Yes. Each body is a level.
   - The COO's pick: a. Under b, the default six reaches about half as far on opencode, by the COO's reading; this is
     not measured.
3. **"Known" in A2.**
   - a. No definition (范蠡).
   - b. "established from repository source or type information" (Linus, 孫子).
   - c. A place is known when the code or description points to it; a link is known when the type checker
     establishes it (老子).
   - The COO's pick: c, because it settles decision 1 by itself.
4. **Does A5 add "a limit the interface requires for that command is part of the answer"?**
   - a. Yes (Linus, 老子).
   - b. No; "its limits" already covers it (范蠡, 孫子).
   - The COO's pick: b.
5. **Layout of A2's and A5's Fails-if lines.**
   - a. One line naming both actors (范蠡).
   - b. A tool line and an agent line (Linus, 孫子, 老子).
   - The COO's pick: b.
6. **A3's fake rule on opencode.** Does a test that swaps in a fake service reach the real function?
   - a. `exclude`: no. The test reaches the fake, so it is left out.
   - b. `count`: yes, it is counted.
   - c. Report both: the count without fakes, and the fake-path tests listed separately.
   - The COO's pick: a (Linus and 老子 in round P1: a test that swaps in a mock reaches the mock).
7. **A1's sibling rule on opencode.** Which files count as siblings?
   - a. The files under one folder that implement the same declared interface or service tag (Dave in P1).
   - b. Files that export the same member names, shown as candidates (老子 in P1).
   - c. One glob per group, given by the user per module: for example, `tool/*.ts` minus the registry.
   - The COO's pick: c, with a's rule used to choose the globs for the three opencode modules.
8. **What counts as a test file?**
   - a. A file under a `test/` or `__tests__` folder, or named `*.test.ts` or `*.spec.ts`.
   - b. Only what the user passes with `--tests`, with no default (the spec today).
   - The COO's pick: b in the tool, and a as the value the run passes on opencode.

## Rules for your answer

- In **Answer**, give a table: decision number · your pick (a, b, c or your own wording) · one-line reason.
- Do not invent facts. A fact you need and do not have goes under "What I need to know".
- Keep to the vision and its use cases. A requirement must not mislead, must not be split, and holds no invented
  numbers.
