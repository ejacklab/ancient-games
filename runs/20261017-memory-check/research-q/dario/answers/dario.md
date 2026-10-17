# Answer — How memory-check should work before any code is written

## Answer
Build it in two slices: first the checks that read files and run `tools/memory_index.py` (9 records), then the git-history checks (7 more). Four `git` records cannot be built (W2.1b, W5.1, K1.1, W6.1b); ask EJ to mark them `reviewer`. Several doc gaps would make the tool give wrong or misleading answers, so settle those before building. Test with hand-declared planted-break fixtures, not with the tool's own output.

## How I decided
1. **Counting (I ran grep over the YAML).** 20 of the 64 records have `tool` or `git` in their `check`: 6 `tool`, 6 `git`, 2 `tool; git`, 1 `tool; reviewer`, 4 `git; reviewer`, 1 `reviewer; git`. The other 44 are `reviewer`, `none` or the secret scanner.
2. **Slice 1: files only, one snapshot, via `memory_index.py --check HEAD`.** I read the script (lines 148–203, 481–508) and did not run it. It covers W1.1a (prefix and kind), W1.1b (id form and duplicates), W1.2a, W1.3a (tool half), W4.1b, K6.1a, K6.2, K6.3a and Rd3.1a.
   - K4.1's "superseded with no `superseded_by`" needs the tool's own header reader. The script reads only `id`, `kind` and `status` (lines 104–124).
   - These slice 1 results cannot be taken straight from the script:
     - It exits 1 for every problem and prints no requirement ids, so the tool must map message text to ids.
     - It treats a kind/prefix mismatch in a superseded or retired entry as a warning only (lines 167–170), but W1.1a is a MUST with no status condition.
     - Check mode returns at the first entry error (lines 495–496), so K6.1a, K6.2 and Rd3.1a are *not evaluated* then, which is different from passing.
     - "Nothing to check" exits 0 (lines 484, 491), which is "not applicable", not a pass.
     - `--check` with no revision reads the staging area, not the working tree.
3. **Slice 2: git history, buildable.**
   - K4.1: `git log --diff-filter=D` finds a deleted entry.
   - W1.1a and W1.1b: rename detection finds a renamed entry file.
   - K4.3: compare claim, `source` and `depends_on` across commits; a changed `covers` needs a `changed:` line added in the same commit.
   - W4.2: each commit touching an entry adds exactly one `changed:` line and removes none. The "matching" time and author are not defined, so only count lines.
   - K5.1: a commit to a journal file that removes or edits lines.
   - W6.3a and W6.2: for each merge commit, check that every header line, link and `covers` path either side added survives. This is a proxy for W6.2; a general "lost edit" outside merges is not visible.
   - W6.1a: a commit that adds a top-level `id:` to an existing entry is a heuristic only.
4. **Not buildable.**
   - W2.1b, W5.1 and K1.1 need to know which code a commit changed "under" a decision. Git has no such link, and an uncovered change has no covering entry, so the check would be circular. The tool can only list commits that touched covered files as a hint.
   - W6.1b needs a session identity that git does not record, and no journal naming scheme is given.
   - W3.2 names a secret scanner that does not exist, and C1 has no rule for that check type.
   - So the 20 split as 9 in slice 1, 7 in slice 2 and 4 unbuildable.
5. **CACHES.**
   - The Core requirements have no level or `check` field, and "Fails if" sits per group. Someone has to assign them, and the tool "adds no rule of its own".
   - No cache or cache tool exists here (`ls project-memory` fails).
   - Checkable now: B2.2 (`git check-ignore project-memory/.cache`) and Rd1.1 (scan hook configs and `AGENTS.md`/`CLAUDE.md` for `.cache/`; this can miss indirect opens).
   - B1 and K3 ("a cache exists with no recorded comparison") need a place and format for the record, and none is named.
   - B4.1, K1.1 and K1.2 need a cache schema that is not defined anywhere I found.
   - B2.1, B3.1, B5.1, K2.x, Rd2.1 and Rd3.x describe how a cache tool behaves. They are not applicable until one exists.
6. **Doc gaps that give wrong answers, most serious first.**
   - **Id collision.** CACHES K1.1, Rd1.1 and Rd3.1 mean different things from SoT K1.1, Rd1.1 and Rd3.1a. The YAML's `retired_ids` says K2 and K3 are unused, but CACHES uses them. `memory_index.py` comments cite a third set (B1.1, B2.3, G4.2). "By id" in C1, R1 and U2 would merge or overwrite requirements. Namespace them (`SoT:K1.1`, `CACHES:K1.1`).
   - **Mixed checks.** The 6 records that combine `tool` or `git` with `reviewer` have no result: R1's four results have no "tool part passed, reviewer part open". C1 also puts `none` (11 guidance records) with `reviewer`, so U4's list would say guidance needs a reviewer.
   - **SHOULD breaks.** Every SHOULD ends "with no written reason", and the tool can find the break but not the reason. A SHOULD "fail" may really be a pass.
   - **No history scope.** A past MUST break (a deleted entry) fails forever, and U3 then warns forever. No baseline or waiver exists, and the tool may not write one.
   - **Duplicate records.** K6.1a and K6.2 have the same `fails_if`, so U2's "exactly that requirement" cannot hold. A single fixture with many planted breaks also hides K6 and Rd3.1a because of the script's early return, so U2 needs one fixture per break.
   - **C3 vs U2.** C3 says report the script's result, but the script's warnings let a failing W1.1a MUST show as passing. The use case wins, so treat the "(warning)" kind/prefix lines as W1.1a fails.
   - **"Required location" is undefined.** R2, C4 and U3 use it, but no MUST says `AGENTS.md` is required (Rd1.1 is a SHOULD with a `reviewer` check). This repo has no `project-memory/`, so U3 would print a missing-location line at every session start.
   - **U1 and user memory.** U1 says the guidelines place user memory outside the repo, but they name only `~/.claude/agent-memory/<name>/`. Reading the home folder needs a `--home` override, because `AGENTS.md` forbids tests on the real home.
   - **Other projects (U6).** The YAML and `memory_index.py` do not exist in another project. They must come from the tool's own repo. A non-git project, or a project folder that is not the git root, must not turn the script's git error into a K6 failure.
   - **Tool cannot run.** Nothing says how a crash or a missing `python3` or `git` is shown. Silence looks like "all clear", and U3 forbids any non-failure line, so a "could not run" line is not allowed today. R3 has no exit code for it.
   - **Hook reach.** A session-start hook reaches Claude Code only (*recall*), but the vision says "every agent".
   - **U5 test.** `git status --short` misses ignored files such as `.cache/`, and git's own index refresh. Use a hash of the whole tree and `GIT_OPTIONAL_LOCKS=0`, as `memory_index.py` line 288 does.
   - **Rd3.1a limits.** The script hardcodes 200 lines and 24,000 bytes (lines 35–36). No place is named where the owner records measured limits.
7. **Build pieces, each tested on its own fixture.**
   1. Catalog loader.
   2. Report, warning and exit code (pure functions).
   3. Locator (F1/F2, with `--home` and `--project`).
   4. `memory_index.py` adapter.
   5. K4.1's `superseded_by` check.
   6. CLI and hook (show the settings diff only).
   7. One history check per piece in slice 2.
   8. B2.2 and Rd1.1.
8. **Tests without circularity.**
   - **Oracle for the catalog.** `sot-requirements.txt` was made by another route, so the loader's 64 ids, levels and checks must equal it line for line.
   - **Mutation fixtures.** Use one clean, hand-written base project. `INDEX.md` must be literal bytes, never produced by the script's write mode. Apply one planted break per fixture. The set of requirement ids that should fail is written by hand before the check exists, and the check must fail first. Also assert that every other record still passes.
   - **Git fixtures.** A builder script uses plain `git` commands and logs each break it plants. That log is the expected answer, and the checker shares no parsing code with the builder.
   - **Adapter tests.** Use recorded real outputs of `memory_index.py` to test the message-to-id mapping, plus a live call on two fixtures: a clean one, and one where `INDEX.md` was hand-edited with `sed`.
   - **Sabotage.** Force each check to always pass; at least one test must go red.
   - **Read-only.** Compare a hash of the whole tree before and after a run.
   - **Who writes the tests.** The repo's `crossed-build-check` skill has an engine other than the code's author write them.

## What I need to know
- **Required locations.** Which locations count as required, and what "memory adopted" means. Default: `AGENTS.md` always; the rest only once `project-memory/` exists in HEAD.
- **History scope.** How far back git checks look, and whether a historical MUST break may be acknowledged. Default: since the first commit touching `project-memory/`, with `--since` to override, and the range printed as evidence.
- **Output from `memory_index.py`.** May it gain an id-tagged `--json` output? That is a small change to a tool that has tests. Without it, the adapter parses prose.
- **The four unbuildable records.** May the YAML mark W2.1b, W5.1, K1.1 and W6.1b as `reviewer`? Only EJ edits the YAML, and the tool must not.
- **CACHES levels and checks.** Who assigns a level and check to each CACHES requirement, and whether the *proposed* ones count. Default: none of them, until assigned.
- **Warning content.** Whether the warning may include a "could not run" line (U3 forbids it today). Default: yes.

## Costs and risks
- **False comfort.** Only 9 of 64 records are fully or mostly checked now. A silent hook would suggest healthy memory, so the report headline must say "N checked, M partly, rest need a reviewer or are guidance".
- **Brittle mapping.** Parsing the script's messages can break silently if they change. Golden-capture tests help; id-tagged output would remove the problem.
- **Two header parsers** (the script's and the tool's) can disagree. If the script rejects an entry's header, the tool's own checks skip that entry and say so.
- **Slice 2 is most of the work.** It needs seven history checks and a git fixture builder. It may also be slow at session start: measure with a 1,000-commit fixture (*recall*: hooks have time limits).
- **No real memory to test on.** The `changed:` and `done:` formats are only loosely specified, so fixtures could encode a wrong guess.
- **Python and YAML.** A TypeScript tool depends on `python3`, and neither `code_map` nor the guard lists a YAML parser. Adding one is a small decision.
- **Not run.** I counted records by grep and read the script and the four docs. I did not run `memory_index.py`.

## How we would know I was right
- The loader's output equals `sot-requirements.txt` exactly, and the report holds every record exactly once (R1).
- In slice 1, each mutation fixture fails exactly the ids declared in advance, the clean base passes all, and every sabotage mutant turns a test red.
- The "unbuildable" claim is falsifiable. If someone can build two repos that differ only in what W2.1b's check could see, one clean and one with a planted break, and a rule separates them, I was wrong about that record.
- The first run on a real `project-memory/` gives the same results as a person reading the 9 slice-1 records.
- The tree-hash read-only test passes after every run, on a fixture and on this repo.

**Recommended plan**
1. Get EJ's answers to the six questions above, starting with required locations and the history baseline, and have EJ edit the YAML for the four unbuildable records.
2. Fix the docs: namespaced ids, results for "partly checked", "guidance", "break found, reason not looked for" and "could not run", and one fixture per planted break in U2.
3. Slice 1 in this order: catalog loader (oracle: `sot-requirements.txt`), report/warning/exit code, locator, `memory_index.py` adapter, K4.1's `superseded_by` check, CLI, hook diff for EJ's yes.
4. Slice 2: one history check per piece (K4.1 deletion, K4.3, W4.2, K5.1, W6.3a with W6.2, W6.1a, rename halves of W1.1a/b), each on a git fixture whose builder logs its own planted breaks.
5. CACHES: only B2.2 and Rd1.1 now. Everything else is "not applicable: no cache tool" until a cache and its schema exist.
6. Tests: a hand-written clean base, one planted break per fixture, expected failing ids declared before the check, a sabotage mutant per check, and a tree-hash read-only test.
7. Have an engine other than the code's author write or review the mutation table.
8. The report headline states how many of the 64 records are checked, how many partly, and how many are left to a reviewer or are guidance.
