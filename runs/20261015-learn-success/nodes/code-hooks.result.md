status: done

S1, S2 and S5 are in place: success lines, `rates`, the `rates` and `path new|check|parents` CLI commands, and the Stop path ask. All 49 round-5 hooks tests pass. 22 tests from earlier rounds now fail, because they require the journal to hold no record after a passing call, and S1 now writes a success line there (see CONTRADICTS).

## Files written (all under `.claude/skills/workflow-design/guard/`)

- `src/journal.ts`: `appendRecord` now accepts `SuccessRecord` (type union only; the same scrub as the other kinds).
- `src/rates.ts` (new): `rates(root, session|null)` counts success and failure records per (check, engine), using SPEC S2's mapping; `ratesMarkdown(rows)` prints a table of ids, engine names and counts only.
- `src/hooks.ts`:
  - S1: PostToolUse for Bash writes a `success` record for a clean engine call (`engine-call`, the engine name) or a green test run (`test-run`, the runner label). It writes nothing for background calls (C1), unknown paths (D3), interrupted runs or PostToolUseFailure, and prints no context line.
  - S5: `pathAsk` at Stop runs after the open-failure, raise and register checks. It blocks once when the session has a success and either no path file names the session, or a path file of the session has `great` and no valid `## great:` section. The block writes `raised` with `ids: ["path"]`. `handleStop` now takes `env`, so this record's time comes from `env.now()`.
- `src/cli.ts`: `rates [--session S]` (exit 0); `path new [--session S] [--out F]` (`--session` defaults to "none", the same default `fail` uses; a write outside the root exits 2); `path check <file>` (exit 1 on a fail finding; a `PathError` exits 2, the same way `register` treats `RegisterError`); `path parents <category>` (Markdown table). Usage text extended.

## Commands run (last lines)

- `cd .claude/skills/workflow-design/guard && bun test` → `1027 pass / 51 fail / Ran 1078 tests across 16 files.`
  - `test/round5-hooks.test.ts` (my part): **49 pass, 0 fail**.
  - `test/round5-insight.test.ts`: 37 pass, 0 fail.
  - `test/round5-paths.test.ts`: 38 pass, 29 fail. All 29 are S3 `checkPath` cases in `src/paths.ts`, another worker's file that was still being written. None of them use cli, hooks or rates.
  - Earlier rounds: 925 tests by my count, not the 922 the brief gives (1078 total − 49 − 37 − 67). Of these, 903 pass and 22 fail, all for the S1 reason below.
- `./node_modules/.bin/tsgo --noEmit -p .` → no output, `tsgo exit 0`.
- Hand check of the CLI in a temporary folder, with `SECRET-PLANT-7f3a9c` planted in a failure's input, actual and reason:
  - `rates` printed only check, engine and counts; exit 0.
  - `path new --out runs/r/success-path.yaml` wrote the file; exit 0.
  - `path check` on the new skeleton gave `R12.7-path-missing` ×3; exit 1.
  - `path parents test` printed an empty table; exit 0.
  - `path` with no subcommand exited 2; `--out /etc/x.yaml` exited 2.
  - The plant did not appear in any output.

## CONTRADICTS

1. **S1 vs the M5, C2 and D1 tests that already existed.** SPEC S1 says "PostToolUse for Bash writes one `success` record when … a recognised engine call's result check finds nothing … or … a test run neither fails nor shows a failure summary". Those older tests require the journal to hold nothing, or only `failure`/`raised` records, after exactly those calls:
   - `test/hooks.test.ts:240` and `:246`: `expect(readJournal(folder).records).toEqual([])`.
   - `test/round3.test.ts:250`: the same assertion.
   - `test/round4.test.ts`: `failures()` at line 61 asserts every record is `failure` or `raised`. This hits the 12 "D1 control: passing … stays quiet" cases (line 192), 6 "stdout … does not match" cases (line 197) and the "stderr alone" case.

   I followed SPEC (Round 5 is the later round). These 22 tests need updating to allow `success` records. I did not change them; tests are outside my Limits.
2. **S5's "blocks the same way, once" was ambiguous.** I first gave the great-section ask its own reason and its own raised id (`great:<file>`). `test/round5-hooks.test.ts:313` reads the SPEC line as the same reason and the same single `raised` id `["path"]`. That is a fair reading of the line, so I adopted it. The block reason is the path text plus one line naming the great section that is missing.

   Consequence (my reading, not measured): one ask per session covers both cases. If the plain path ask has already been raised, a great section that is missing later is not asked for.
3. **Two choices of mine that SPEC does not settle** (labelled as mine, not SPEC):
   - A test run counts as green only when **no** failure summary appears anywhere in its stdout. D1, by contrast, reads stdout only when the run owns it. The reason is that `pytest; echo done`, where pytest failed, must never write a success line.
   - Every path ask needs at least one success record in the session, following the S5 Fails-if line "a session with no successes is asked".
