status: done

XB4 of the guard SPEC's Round 20 (after the Codex review) and the memory-check findings 1, 2 and 3 are implemented;
every written test for them passes and nothing else changed.

## Pieces

- **f1** — `memory_check/src/cachechecks.ts`, `checkRd1`, the SessionStart-hook branch: a hook command is read without
  the prose negation rule, so `cat project-memory/.cache/index.sqlite || echo not found` is a break, not an
  instruction never to read a cache. The line-by-line prose scan keeps its negation rule.
- **f2** — `memory_check/src/entry.ts`, `headerDelimiters` and `parseEntry`: a pair of `---` lines is a header block
  when the lines between it hold a top-level `id:`, `kind:` or `status:` key (the keys `tools/memory_index.py` reads
  there), a pair that closes no header is stepped over and the scan goes on, and `idLines` collects the `id:` line of
  every header block, so W6.1a names the second `id:` line.
- **f3** — `memory_check/src/warn.ts`, `FILE_NAME`: it also matches `project-memory/entries/<name>.md` in the evidence,
  so a staged or committed deletion's warning names the file it deleted. Staged entries are still matched whole
  first, so a name with a space in it is named whole as before (C12, A5).
- **xb4** — `.claude/workflows/crossed-build-check.js`, `testRun`: a test command runs as
  `timeout <N> bash -c '<test_cmd>'` with its single quotes written `'\''`, so the limit bounds a compound command
  whole; XB2's background form wraps the same string.

## The three commands' last lines

- `cd memory_check && bun test` — `Ran 101 tests across 6 files. [14.27s]` (0 fail; `review3.test.ts` 4 pass)
- `cd .claude/skills/workflow-design/guard && bun test` — `Ran 1560 tests across 40 files. [16.48s]` (0 fail)
- `node tests/workflows/crossed_build_check_harness.mjs` — `all passed`

Both `tsgo --noEmit -p .` runs (memory_check and the guard) are clean.

## CONTRADICTS

none