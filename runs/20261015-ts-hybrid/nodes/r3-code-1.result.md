---
node: r3-code
attempt: 1
engine: opencode
model: minimax-coding-plan/MiniMax-M3.1-Flash-Preview
status: partial
started: 2026-10-15T16:57:00Z
ended: 2026-10-15T18:34:00Z
evidence: runs/20261015-ts-hybrid/nodes/r3-code-1.evidence.txt
---

C1–C16, C18–C24 are implemented in `src/` and 793 of 796 tests pass; the three C17 tests abort in their own
precondition because the engine running this node is itself an `opencode run` process, so their behaviour is verified
by a stand-in-process probe instead (evidence, section 3).

- Files written:
  - `tools/harness-guard/src/traps.ts` — C2 (output flags and `>` read from unquoted words only, via the new
    `shellWords`), C18 (`<<` with or without a space before it), C19 (backticks split segments; `do/then/else/elif/!/{}`
    stripped as wrappers), C21 (redirect targets are not paths read; quoted words split on whitespace), C3/C4 (new
    exported `engineCallSite` + `folderBefore`: the folder a `cd` moved the call into, and whether the engine segment
    ends the command). `recognizeEngineCall` now delegates to it.
  - `tools/harness-guard/src/hooks.ts` — C1 (background calls write no record and no output), C2 (`input` is
    `"<engine> call"` plus the output file's basename), C3 (`payload.cwd`, then `cd`), C4 (a failing segment after the
    engine is not its exit), C9 (a touched register that no longer exists is skipped), C10 (the raise check needs a
    `last_assistant_message` string), C23 (the context line says the failure is already in the journal), C24 (the Stop
    block names `.harness-guard/insights/<name>.md` and `runs/<run>/insight.md`).
  - `tools/harness-guard/src/journal.ts` — C12 (`appendFailure` stores the record as given; only `writeEvidence` and
    `appendRecord` drop raw-content keys), C13 (evidence may be a file or a folder).
  - `tools/harness-guard/src/insight.ts` — C5 (every `*.md` under `.harness-guard/insights/`), C6 (blank lines skipped,
    indented continuations joined, list ends at an unindented non-item line), C7 (`Source:` decided by its first word).
  - `tools/harness-guard/src/register.ts` — C8: a list item that is not a mapping is an `R13-malformed` fail naming its
    list and index; `validateRegister`, `units` and `coverage` read only mapping entries, so no YAML shape throws.
  - `tools/harness-guard/src/doctor.ts` — C14 (health JSON that is not an object with a `findings` array is
    `ok: false`, `summary: "unexpected JSON"`), C16 (an opencode plugin file counts as installed when its text contains
    `harness-guard`).
  - `tools/harness-guard/src/install.ts` — C15: the opencode snippet prints the one-line plugin file
    (`export { default } from "<guardDir>/src/plugins/opencode.ts";`) and the plugins folders to put it in.
  - `tools/harness-guard/src/cli.ts` — C11 (a hook payload that is not JSON, or empty stdin, is one stderr line and
    exit 0), C17 (`running` drops only this process and its parent, by pid, read from `ps -eo pid=,args=`; the old
    text filter on `harness-guard` is gone).
  - `runs/20261015-ts-hybrid/nodes/r3-code-1.evidence.txt`, this file. Nothing under `test/`, `SPEC.md`,
    `src/types.ts`, `data/`, `package.json` or `tsconfig.json` was touched; nothing was committed.

- Check:
  - `cd tools/harness-guard && bun test` → `793 pass / 3 fail / 2533 expect() calls / Ran 796 tests across 9 files.`
    The three failures are the C17 block; each aborts inside the test's own `requireNoOtherOpencode()`
    (`test/round3.test.ts:841`: "C17 needs a machine with no other opencode run process"), because this node runs as
    `opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview …` (and its runlog.py wrapper line matches too).
    The precondition is reached before any assertion, so no change under `src/` can pass them here. Their three
    behaviours were reproduced with `ps` replaced by a stand-in that lists the guard's own process, its parent and one
    other process: (1) another process whose line contains `harness-guard` → `lint` exits 1 with
    `trap:opencode-parallel`, and the hook denies with the same rule; (2) with no other process → `lint` exits 0; (3)
    the CLI's own line and its parent's line both name an engine and are dropped → exit 0. Evidence, section 3.
  - `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` → no output, exit 0.
  - Baseline before the change, same commands: `684 pass, 112 fail` (the brief said 111; I measured 112).

- CONTRADICTS: none between a test and SPEC.md. One environment-only gap, reported for the COO:
  **C17 cannot be satisfied on the machine that runs this node.** `test/round3.test.ts:832-892` requires no other
  `opencode run` process, and the node's own engine is one, so the three C17 tests fail before reaching the guard.
  Test 3 would also fail on its assertion while this node runs (it expects `lint 'opencode run …'` to exit 0, while the
  node's engine line is a real concurrent `opencode run` that the parallel trap must count). C17 is implemented as
  SPEC.md says and verified out of band; the COO should re-run those three tests on a machine with no `opencode run`
  (or after this node has exited) to get the suite at 796/796. No type in `src/types.ts` had to change.