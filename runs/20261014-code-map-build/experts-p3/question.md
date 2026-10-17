Method 3.5 — before these pieces run as loops: are their checks real?

Asked of: Linus, 范蠡, 孫子, Dave (`--only linus,fan-li,sun-tzu,dave`). Answer **your own** question below, through
your rules, for each piece listed; the others answer theirs.

- **Linus:** could this check pass while the requested result is wrong, or while an existing user workflow breaks?
- **范蠡:** what bounds the attempts before the loop must exit, and how promptly must it close when the check passes?
- **孫子:** what is left to the worker's good character rather than to a check the worker cannot edit?
- **Dave:** what result would show this check can fail, and what is its control (old code, a plant, the baseline)?

In "Answer", give one line per piece id: loop-ready as written / strengthen the check (how) / not loop-ready (why).
Name a concrete failure the check would miss wherever you can; "looks fine" is not an answer.

Facts (filled in by the COO), per piece. You may read these files in the repository; do not read anything else.
Requirements: `runs/20261014-code-map-vision-relay/result-trimmed.md`. Interface: `runs/20261014-code-map-build/spec.md`.
Evaluator: `code_map/eval/` (its own notes: `code_map/eval/COVERAGE.md`, `code_map/eval/SPEC_QUESTIONS.md`).

- **P3 — build loop, one requirement per round**, in this order: R1, R2, A5, A2, A3, A1, L1, R3. Deliverable: the
  `code-map` tool in `code_map/src/` (TypeScript, Bun, `typescript` 5.8.2, reads opencode-style Effect services).
  - Each round:
    1. Codex (gpt-6.1-sol) writes failing `bun test` tests for the round's requirement in `code_map/test/<req>/`,
       from the requirements and spec; the COO freezes them (sha256).
    2. opencode (MiniMax-M3.1-Flash-Preview) writes `code_map/src/` until those tests pass, and the evaluator
       (`bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json`) reports the round's
       requirement MET, and no requirement MET in an earlier round becomes NOT MET.
    3. 孫子 (dsh) and 范蠡 (agy) review the diff and the evaluator report: APPROVE, or CHANGE tied to a requirement
       line.
  - check: run by the COO after each attempt — `bun test` (all frozen tests), `bunx tsgo --noEmit`, the evaluator,
    sha256 of the frozen tests and of `code_map/eval/` unchanged. Known to fail on: the evaluator caught 15 of 15
    COO plants (one broken canned answer each, on Codex's stub tool); the tests are not yet written, so not yet
    shown for them.
  - Known coupling (measured on the evaluator): R1's four cases run `map`, `chain`, `tests` and `callers` on a
    marker fixture and also check those answers' content; the evaluator's report marks R1 NOT MET when any of those
    answers is wrong, even with no marker created. A wrong answer anywhere also spills onto R1; an R1 or R3 fault
    marks every requirement NOT MET. So R1, the first round, cannot reach MET until map, chain, tests and callers
    are correct.
  - The evaluator's fixtures are 6 small projects, 37 cases; the opencode case files (from answer keys kept away
    from builders) are not written yet and are used from P4. A6 and L2 are not in P3.
  - Open rules set by the user, passed as flags with no default: `--tests`, `--fake-rule` (A3), `--siblings` (A1).
  - attempt limit: 3 per requirement · feedback on failure: the failing test names and output, the evaluator's
    NOT MET lines with expected against actual, the reviewers' CHANGE lines · exit: the requirement goes to EJ as
    blocked and the loop moves to the next requirement.
  - may change: `code_map/src/` (builder), `code_map/test/<req>/` (Codex, before the build only) · must not change:
    `code_map/eval/`, frozen tests during a build, `code_map/package.json`, `docs/`, `code_graph/`. No commits.
