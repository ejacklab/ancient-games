# The 17 unjudged findings of run 20261017-memory-check-review (copied verbatim; only the reviews' Findings sections)

## Codex (C1–C12)

My reading, supported by in-memory probes I wrote; these are not independent verification.

C1. **P1 — Unreadable staging is treated as absent memory.** `memory_check/src/checks.ts:111` — breaks **C1, C2, R3, U3**. Input: a corrupt git index makes `git ls-files` fail. Memory requirements become “not applicable”; the command exits 0 without warnings. **Fix:** propagate snapshot-read errors as “could not run” before applying absence exemptions.

C2. **P1 — Deleting all memory hides the deletion finding.** `memory_check/src/checks.ts:209` — breaks **U2 / SoT:K4.1**. Input: commit an entry, then stage deletion of all `project-memory/`. The detected deletion is discarded because memory is now absent, and exit is 0. This exposes a **C4–U2 conflict; U2 takes precedence**. **Fix:** retain historical deletion failures when current memory is absent.

C3. **P1 — `--since` can hide staged changes to existing entries.** `memory_check/src/gitrequirements.ts:224` — breaks **C1 / SoT:K4.3**. Input: create an entry, commit an unrelated change, then stage a different `source` and run with `--since HEAD`. With no entry commits in that range, the check compares zero transitions and passes. **Fix:** compare staged content with HEAD even when the selected history contains no entry changes.

C4. **P1 — Actual session-start hooks escape the cache check.** `memory_check/src/cachechecks.ts:76` — breaks **C6 / CACHES:Rd1**. Input: `.claude/settings.json` contains a `hooks.SessionStart` command of `cat project-memory/.cache/index.sqlite`. The check passes because the command line lacks its natural-language session-start phrase. **Fix:** recognize hook timing from the configuration structure.

C5. **P1 — Cache instruction checks use the wrong snapshot.** `memory_check/src/cachechecks.ts:67` — breaks **C5, C6**. Input: stage an `AGENTS.md` instruction to open the cache at session start, then remove that instruction without staging. The check passes using working-tree text while the report claims staged content was checked. **Fix:** read tracked instruction content from staged blobs.

C6. **P1 — Inactive entries bypass kind validation.** `tools/memory_index.py:167` — breaks **SoT:W1.1a / U2**. Input: a retired `D-17-10-abc123-2026-old.md` with `kind: fact` and a matching empty index. Python exits 0 with a warning; the TypeScript wrapper reports W1.1a passing. **Fix:** make invalid kinds and prefix mismatches errors in every status.

C7. **P1 — Unborn HEAD bypasses staged entry validation.** `tools/memory_index.py:483` — breaks **SoT:W4.1b, W1.2a**. Input: before the first commit, stage an entry with `status: invalid` or no header, then run `--check`. It exits 0 without reading staging. **Fix:** inspect staged files when no revision is requested, regardless of HEAD’s existence.

C8. **P1 — SHA-256 repositories are mistaken for empty memory.** `tools/memory_index.py:354` — breaks **SoT:K6.1a, K6.2**. Input: a git repository using SHA-256 with staged entries and an incorrect index. Every 64-character object id is rejected, so Python reports no memory and exits 0. **Fix:** accept the repository’s object-id format instead of requiring 40 characters.

C9. **P1 — Markdown separators are mistaken for additional entries.** `memory_check/src/gitrequirements.ts:82` — breaks **U2, C1** by falsely failing **SoT:W6.1a**. Input: one valid entry whose body contains two `---` thematic separators after `**Why:**`. It is reported as multiple entries. **Fix:** distinguish another entry header from ordinary Markdown separators.

C10. **P1 — Unreadable instructions receive a clean cache verdict.** `memory_check/src/cachechecks.ts:68` — breaks **C1, C2 / CACHES:Rd1**. Input: an existing `.claude/settings.json` that cannot be read. The exception is recorded as “unreadable,” but Rd1 passes. **Fix:** return “could not run” when an instruction file cannot be inspected.

C11. **P1 — Regular files are reported as agent-memory directories.** `memory_check/src/locations.ts:68` — breaks **F1 / U1**. Input: the agent-memory parent contains only a regular `README.md` file. The report lists `agent memory README.md/` as present. **Fix:** enumerate directory children only, reporting absence when none exist.

C12. **P2 — Entry-format warnings omit the affected filename.** `memory_check/src/warn.ts:12` — breaks **R2**. Input: an entry with `status: invalid`. Python supplies its bare filename, but the warning formatter recognizes only paths beginning `project-memory/entries/`, so the warning contains no filename. **Fix:** carry parsed entry paths into warning generation.


## agy (A1–A5)

A1. **[P1] Unborn HEAD skips staging area check — [tools/memory_index.py:483](tools/memory_index.py#L483).**
   - **Broken requirement / use case:** SoT:K6.1a, SoT:K6.2, U2 (*my reading*).
   - **Input that shows it:** An initial repository state where `HEAD` is unborn (e.g. a fresh `git init` before the first commit) with malformed entries or an unsynchronized `project-memory/INDEX.md` staged. Running `python3 tools/memory_index.py --check` outputs `"nothing to check: HEAD names no commit yet, so the staging area holds no snapshot"` and exits 0 instead of checking the staged snapshot and exiting 1.
   - **Fix:** Restrict `if head_is_unborn(repo):` so it only returns early when checking `rev` (or `rev == "HEAD"`), allowing staged checks (`rev is None`) to proceed to `snapshot_memory`.

A2. **[P1] Early return on index mismatch suppresses Rd3.1a size check — [tools/memory_index.py:499](tools/memory_index.py#L499).**
   - **Broken requirement / use case:** SoT:Rd3.1a, U2 (*my reading*).
   - **Input that shows it:** An active entry corpus whose generated index exceeds `MAX_LINES` (200) or `MAX_BYTES` (24,000) and whose staged `project-memory/INDEX.md` is simultaneously out of date (`current != rendered`). Running `python3 tools/memory_index.py --check` returns 1 immediately at line 502, never evaluating `over_limit(rendered)` at line 503, thereby failing to report that `INDEX.md` exceeds its limit.
   - **Fix:** Evaluate and record `over_limit(rendered)` before or alongside returning on `current != rendered`.

A3. **[P1] SessionStart harness hook opening cache is evaluated as allowed on-demand read — [memory_check/src/cachechecks.ts:38](memory_check/src/cachechecks.ts#L38).**
   - **Broken requirement / use case:** CACHES:Rd1, C6, U2 (*my reading*).
   - **Input that shows it:** A project with `.claude/settings.json` defining a `SessionStart` hook command opening the cache (e.g. `"hooks": { "SessionStart": [{ "matcher": ".*", "command": "cat project-memory/.cache/index.sqlite" }] }`). Because `checkRd1` evaluates each line in isolation against `SESSION_START` regex, the command line lacks startup keywords, setting `reading.atStart` to `false` and reporting `CACHES:Rd1` as `pass`.
   - **Fix:** Maintain `SessionStart` block context when parsing JSON/settings files rather than testing lines in isolation with `SESSION_START`.

A4. **[P1] Empty bullet in superseded_by passes as valid link — [memory_check/src/gitrequirements.ts:147](memory_check/src/gitrequirements.ts#L147).**
   - **Broken requirement / use case:** SoT:K4.1, U2, R3 (*my reading*).
   - **Input that shows it:** A staged entry with `status: superseded` and `superseded_by:\n  -` (an empty list bullet). In `parseEntry`, `entry.fields.get("superseded_by")?.full` is `"-"`, for which `linksNothing("-")` returns `false`, causing `checkHeader` to log no break and `runChecks` to return `needs a reviewer` (exit 0) instead of `fail` (exit 1).
   - **Fix:** Verify `itemsOf(entry, "superseded_by").length === 0` or include `"-"` in `linksNothing` empty forms.

A5. **[P2] Entry names with whitespace or non-ASCII characters are truncated in warnings — [memory_check/src/warn.ts:12](memory_check/src/warn.ts#L12).**
   - **Broken requirement / use case:** R2, U3 (*my reading*).
   - **Input that shows it:** An entry whose filename contains whitespace or non-ASCII characters (e.g. `project-memory/entries/D-17-10-abc123-2026-time check.md`) that triggers a failing MUST. `FILE_NAME` regex `[\w.\-]+` stops before the space, printing `files: project-memory/entries/D-17-10-abc123-2026-time` in `memory-check --warn`.
   - **Fix:** Update `FILE_NAME` regex to match valid entry paths containing spaces and UTF-8 characters up to `.md`.

