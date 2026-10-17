status: done

## Findings

My reading, supported by in-memory probes I wrote; these are not independent verification.

1. **P1 — Unreadable staging is treated as absent memory.** `memory_check/src/checks.ts:111` — breaks **C1, C2, R3, U3**. Input: a corrupt git index makes `git ls-files` fail. Memory requirements become “not applicable”; the command exits 0 without warnings. **Fix:** propagate snapshot-read errors as “could not run” before applying absence exemptions.

2. **P1 — Deleting all memory hides the deletion finding.** `memory_check/src/checks.ts:209` — breaks **U2 / SoT:K4.1**. Input: commit an entry, then stage deletion of all `project-memory/`. The detected deletion is discarded because memory is now absent, and exit is 0. This exposes a **C4–U2 conflict; U2 takes precedence**. **Fix:** retain historical deletion failures when current memory is absent.

3. **P1 — `--since` can hide staged changes to existing entries.** `memory_check/src/gitrequirements.ts:224` — breaks **C1 / SoT:K4.3**. Input: create an entry, commit an unrelated change, then stage a different `source` and run with `--since HEAD`. With no entry commits in that range, the check compares zero transitions and passes. **Fix:** compare staged content with HEAD even when the selected history contains no entry changes.

4. **P1 — Actual session-start hooks escape the cache check.** `memory_check/src/cachechecks.ts:76` — breaks **C6 / CACHES:Rd1**. Input: `.claude/settings.json` contains a `hooks.SessionStart` command of `cat project-memory/.cache/index.sqlite`. The check passes because the command line lacks its natural-language session-start phrase. **Fix:** recognize hook timing from the configuration structure.

5. **P1 — Cache instruction checks use the wrong snapshot.** `memory_check/src/cachechecks.ts:67` — breaks **C5, C6**. Input: stage an `AGENTS.md` instruction to open the cache at session start, then remove that instruction without staging. The check passes using working-tree text while the report claims staged content was checked. **Fix:** read tracked instruction content from staged blobs.

6. **P1 — Inactive entries bypass kind validation.** `tools/memory_index.py:167` — breaks **SoT:W1.1a / U2**. Input: a retired `D-17-10-abc123-2026-old.md` with `kind: fact` and a matching empty index. Python exits 0 with a warning; the TypeScript wrapper reports W1.1a passing. **Fix:** make invalid kinds and prefix mismatches errors in every status.

7. **P1 — Unborn HEAD bypasses staged entry validation.** `tools/memory_index.py:483` — breaks **SoT:W4.1b, W1.2a**. Input: before the first commit, stage an entry with `status: invalid` or no header, then run `--check`. It exits 0 without reading staging. **Fix:** inspect staged files when no revision is requested, regardless of HEAD’s existence.

8. **P1 — SHA-256 repositories are mistaken for empty memory.** `tools/memory_index.py:354` — breaks **SoT:K6.1a, K6.2**. Input: a git repository using SHA-256 with staged entries and an incorrect index. Every 64-character object id is rejected, so Python reports no memory and exits 0. **Fix:** accept the repository’s object-id format instead of requiring 40 characters.

9. **P1 — Markdown separators are mistaken for additional entries.** `memory_check/src/gitrequirements.ts:82` — breaks **U2, C1** by falsely failing **SoT:W6.1a**. Input: one valid entry whose body contains two `---` thematic separators after `**Why:**`. It is reported as multiple entries. **Fix:** distinguish another entry header from ordinary Markdown separators.

10. **P1 — Unreadable instructions receive a clean cache verdict.** `memory_check/src/cachechecks.ts:68` — breaks **C1, C2 / CACHES:Rd1**. Input: an existing `.claude/settings.json` that cannot be read. The exception is recorded as “unreadable,” but Rd1 passes. **Fix:** return “could not run” when an instruction file cannot be inspected.

11. **P1 — Regular files are reported as agent-memory directories.** `memory_check/src/locations.ts:68` — breaks **F1 / U1**. Input: the agent-memory parent contains only a regular `README.md` file. The report lists `agent memory README.md/` as present. **Fix:** enumerate directory children only, reporting absence when none exist.

12. **P2 — Entry-format warnings omit the affected filename.** `memory_check/src/warn.ts:12` — breaks **R2**. Input: an entry with `status: invalid`. Python supplies its bare filename, but the warning formatter recognizes only paths beginning `project-memory/entries/`, so the warning contains no filename. **Fix:** carry parsed entry paths into warning generation.

Checked and found nothing: guideline record enumeration and versioning; report section ordering; literal index fixtures; ordinary id, status and conflict-marker parsing.

Validation: **53 Python unit cases passed; 4 file-writing cases excluded**. Full suites were not run because they create files. No files were changed.