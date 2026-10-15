status: done

Round 6 K2 and K3 are in place: UserPromptSubmit reminder, touched records for criteria files, the Stop criteria step,
UserPromptSubmit in the install snippet, `criteria new|score` in the CLI, and `measures.score` in the path skeleton —
1167/1167 tests pass and tsgo reports no errors.

## Files

- `.claude/skills/workflow-design/guard/src/hooks.ts`
  - `handleUserPromptSubmit`: asks once per session, using the SPEC text word for word. It records `raised`
    `ids: ["criteria"]` and says nothing if the session has already touched a criteria file. It never reads the prompt.
  - PostToolUse Write/Edit/MultiEdit: writes a `touched` record for a register **or** criteria file (`isCriteriaFile`).
  - `criteriaStep` runs in Stop after open-failure → raise → register and before `pathAsk`. For each criteria file this
    session touched that still exists:
    - If the file is unreadable, has a `checkCriteria` fail, or has unmarked ids, Stop blocks once per file state. The
      block gives only rule ids and K1's id/position messages, never item text.
    - One `criterion:<id>` failure is written per `met: false` item, once per session per id.
    - One `R12.7-criteria-late` failure is written per file when its first touch comes after the session's first
      success or failure record (records the criteria step itself wrote don't count).
- `.claude/skills/workflow-design/guard/src/install.ts`: `UserPromptSubmit` added to the event list (no matcher).
- `.claude/skills/workflow-design/guard/src/cli.ts`:
  - `criteria new [--session S] [--request TEXT] [--from-register FILE] [--out F]`: prints the K1 skeleton, or
    `fromRegister` written out with `Bun.YAML.stringify`, or writes it to a file. An `--out` outside the root gives exit 2.
  - `criteria score <file>`: prints `score: <met>/<total> (<percent>%)` and `unmarked: <ids>|none`. Exit 1 on a fail
    finding or unmarked ids; exit 2 on an unreadable file (same as `register`).
- `.claude/skills/workflow-design/guard/src/paths.ts`: `skeleton` adds `measures.score`, the mean percent of the
  session's scored criteria files rounded to one decimal. It is left out when no file is scored.

## Choices I made where SPEC leaves the detail open

1. **Where the criteria step sits:** after the register check and before the path ask. SPEC only says "after the
   open-failure and raise checks and before the path ask".
2. **"Once per file state":** a `raised` record with id `criteria-state:<relative path>:<first 16 hex of sha256 of the
   file bytes>`. It holds a hash, not the text. If the file changes, it can block again.
3. **Blocking on new failures:** when this Stop writes a criterion or late failure, the same Stop blocks with the
   standard insight reason rather than waiting for the next Stop.
4. **Late check runs on a bad file too:** it runs even when the file has problems or fails to load. The late record has
   `input` = the file's basename and `evidence` = its relative path, and "once per file" is keyed on that evidence path.
5. **Which files count for `measures.score`:**
   - A session's criteria files are the files it touched plus the files whose `session:` field names it.
   - A file counts as scored when it loads, has at least one item and has no unmarked items. If unmarked items were
     counted, they would count as "not met", which K1's Fails-if forbids.
6. **`criteria score` output:**
   - Findings print as `severity rule: message`. K1's messages name items by id or position only.
   - A null percent prints as `(n/a)`.

## Commands and last lines

- `cd .claude/skills/workflow-design/guard && bun test` → `1167 pass / 0 fail / 6130 expect() calls / Ran 1167 tests
  across 18 files.`
  - None of the 1078 earlier tests changed behaviour or failed. The existing install test checks that events are
    included, so the extra event doesn't break it.
  - Round 6 test files present when I finished, all passing: `test/round6-hooks.test.ts` 40, `test/round6-criteria.test.ts` 49.
- `./node_modules/.bin/tsgo --noEmit -p .` → no output, exit 0. No errors in my files or anyone else's.
- Manual CLI smoke test in a temporary git repo (deleted afterwards), with `SECRET-PLANT-7f3a9c` in the prompt, the
  criterion text and the register text. The plant did not appear in hook output, block reasons, `criteria score` output
  or `.harness-guard/`. It does appear in the criteria file that `criteria new --from-register` writes; that is
  expected, because SPEC names the request and the unit text as that file's content.
  - Results: `criteria score` on 2 met / 1 not met → `score: 2/3 (66.7%)`, exit 0. The reminder appeared once; the
    second prompt was quiet. Stop wrote `criterion:C2` and blocked. `path new` showed `score: 66.7`. `--out /tmp/...` →
    exit 2 and no file.

## Notes

- `SPEC.md` was changed in this worktree by someone else while I worked. Line 475 now reads "criteria written first
  leave a late record" (it was "no late"). My code behaves as the new line says.
- The reminder text has no `--session`, because SPEC's text has none. So a file created by that command has
  `session: none` in it. Stop and the path score still connect the file to its session through the touched record.

CONTRADICTS: none.
