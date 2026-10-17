# Dave — how memory-check should work, before any code

## Answer
Build memory-check as a read-only runner over one named snapshot. It hands to `memory_index.py --check` only the clauses that script actually catches, checks the other file and git clauses itself, and reports every clause it cannot decide as *needs a reviewer*, never as pass. That covers every SHOULD's "with no written reason", every "under a new decision", and all of CACHES today. Before any code, change C3: as written it forces a false pass on W1.1a, which U2 forbids. Then test every check against two things: a clean control fixture, and a plant manifest that another engine writes before the check exists.

## How I decided

1. **What would change my mind (my #1).** Question 1 depends on one fact: does `memory_index.py --check` catch what the YAML's `check: tool` says it does? The YAML defines `tool` as exactly that script (`SOURCE_OF_TRUTH_REQUIREMENTS.yaml:37-39`). If it catches every `tool` clause, C3 is right as written. If not, C3 has to change. I looked at the code and tests instead of arguing it (my #2, my #5).

2. **What is already measured (my #5).** Each fact below was checked in the file named:
   - `tests/test_memory_index.py:136-145` puts `X-hidden.md` in `entries/` and asserts that `--check` exits 0. So a file "whose prefix is not one of the five" (W1.1a's fails_if) is skipped, not failed (`memory_index.py:306-313`).
   - `memory_index.py:159-170`: a wrong `kind` in a superseded or retired entry is only a *warning*, and the exit stays 0. W1.1a's fails_if does not say "active".
   - `memory_index.py:494-506`: if any entry has an error, it returns 1 *before* it compares `INDEX.md` (K6.1a, K6.2) and before the size check (Rd3.1a). If the index does not match, it returns before the size check.
   - `memory_index.py:483-492`: with no `project-memory/`, or a HEAD with no commits, it exits **0** and prints "nothing to check".
   - `--check` reads the staging area or a commit, never the working tree. Write mode writes `INDEX.md` (`memory_index.py:447-465`, `481`).
   - `parse_header` reads only `id`, `kind` and `status` (`memory_index.py:104-124`). It never checks `supersedes`, `superseded_by`, `covers` or `changed:`.
   - What this does not show: this repo has no `project-memory/`, so nothing is known about real histories, merges or speed.

3. **Question 1: which records a tool can check.** This is my reading of each fails_if line, with no runs behind it (my #10).

   | How it can be decided | Records (clauses) |
   |---|---|
   | Files, by `memory_index.py --check` | W1.1b (id form, duplicate ids); W1.2a; W1.3a (active entry with no claim or no `**Why:**`); W4.1b; K6.3a; K6.1a, K6.2 and Rd3.1a for one snapshot |
   | Files, but `memory_index.py` misses them, so memory-check checks them itself | W1.1a: a file with a wrong prefix, and a wrong `kind` in an inactive entry; K4.1: a `superseded` entry with no `superseded_by`; W6.3a: two entries that supersede the same one (the finding only) |
   | Git history, mechanical | W1.1a/W1.1b renames (`git log -M --diff-filter=R`); K4.1 deletes (`--diff-filter=D`); K4.3 claim, `source` or `depends_on` changed, or `covers` changed with no `changed:` line; K6.1a/K6.2 for each commit (`--check <rev>` on every commit that touches `project-memory/`); W6.3a: a merged entry missing a `changed:` line, link or `covers` path that one side added (merge commit against both parents); W4.2 and the first clause of K5.1 (findings only, because they are SHOULDs) |
   | Needs something the tool cannot see | W2.1b, W5.1, K1.1: whether a commit "changes code under a new decision" (the missing decision is in no file). W6.1b: git records no session identity. W6.2: a silent overwrite on one branch looks like a deliberate edit. W5.1 "a correction it received": that needs transcripts, which Rd2.3a forbids loading. K5.1 "raw notes kept elsewhere". W3.2: its own check text says no secret scanner exists. Every SHOULD's "with no written reason". The reviewer half of W1.3a, W6.1a, W6.3a and K4.1 |
   | CACHES B1–Rd3 | Only B2.2 (`git check-ignore`) and Rd1 (a start hook or instruction opening `.cache/`, which a grep of the project's hook config and AGENTS.md/CLAUDE.md can find, direct mentions only) can be read. B2.1, B3, B5, K2, Rd2 and Rd3 need the cache's own rebuild or query to run, which writes files (breaking F3) or breaks things on purpose. B4 and K1 need the index opened and its schema known, and no doc fixes a schema. B1 and K3 need run records that only a reviewer can judge. Today all of them are *not applicable*: there is no `.cache/`. |

   So 14 of the 20 `tool`/`git` records can be decided at least in part. Five (W2.1b, W5.1, K1.1, W6.1b, W6.2) carry a `git` label that git history cannot back up, and W6.1a gives only candidates (my reading).

4. **Question 2: what would make the tool answer wrongly.** I list these first because a failure is a result (my #9).
   - **a. C3 forces a false pass, which conflicts with U2, and the use case wins.** Under C3 as written, a planted `X-foo.md`, or a superseded entry with `kind: foo`, gets W1.1a = pass. U2's fails-if names exactly this case: "a MUST that fails is shown as passing". Fix: C3 hands over only *the clauses memory_index.py checks*, and memory-check checks the rest itself. The YAML's `check: tool` on W1.1a claims more than the script does. That goes to EJ as a report; the YAML is not edited here (AGENTS.md).
   - **b. One exit code stands for eight ids.** memory_index.py gives one exit code and plain-text stderr lines. It stops before K6.2 and Rd3.1a when an entry fails, and exit 0 also means "nothing to check".
     - R1 allows four results. It needs a fifth, *not reached (blocked by <id>)*. Without it, one planted entry error also shows K6.2 failing, and U2's "exactly that requirement" fails.
     - Mapping stderr text to ids depends on the wording of the messages (insight F-2cdebf3b).
   - **c. No snapshot is named.** `--check` sees the staging area or a commit, while F1 looks at the working tree, and write mode would break F3. A broken entry that is not staged would be reported as passing. The report must say which snapshot it describes; that is EJ's choice.
   - **d. CACHES has no `check` field.** C1 says "who decides: the guidelines' check field", but for B1–Rd3 there is no field to read. Classifying them would mean the tool adds its own rule, which the vision forbids.
   - **e. Ids collide.** `K1.1`, `Rd1.1` and `Rd2.1` exist in both guidelines with different meanings (YAML lines 477, 631, 657; CACHES.md lines 407, 443, 451). A report listing "per requirement its id" (R1) is ambiguous. Ids need their source, e.g. `SoT:K1.1` and `CACHES:K1.1`.
   - **f. Mixed checks and SHOULDs have no rule.** C1 separates pure `tool`/`git` records from `reviewer`/`none` ones. But W1.3a, W5.1, W6.1a, W6.3a, K1.1 and K4.1 are both kinds, and W3.2 is "secret scanner; reviewer". If passing the mechanical clause makes the whole record pass, U4 fails: the report "looks complete when it is not".
     - Proposed: a mechanical fail is a fail; a mechanical pass is *needs a reviewer* for the rest.
     - The same goes for a git SHOULD finding. It fails only when there is no written reason, and the tool cannot judge a reason, so it is *needs a reviewer*, with the commit as evidence.
   - **g. "Missing required location" has no source.** None of the 64 records has a MUST requiring any location to exist; Rd1.1, the layout, is SHOULD and reviewer. C4's example "AGENTS.md is required" would be a rule the tool invents. Until EJ names the required locations, R2's second kind of warning line has nothing to fire on.
   - **h. The hook can break the rules it checks.** CACHES Rd1 fails if "a start hook or instruction opens any file under `project-memory/.cache/`" (CACHES.md:447). SoT Rd2.1 fails if a start hook loads a memory file outside the four it names. In hook mode the tool must never open a file inside `.cache/` (listing the folder is fine), and it must print ids, never claims (my reading: what counts is what reaches the session).
   - **i. Git history can be silently short.** On a shallow clone every git check sees fewer commits and passes. The tool should detect this with `git rev-parse --is-shallow-repository` and report the git checks as *not applicable: history incomplete*. Default range: every commit that touches `project-memory/`.
   - **j. U5's test is weaker than F3.** `git status --short` never shows a write to the gitignored `.cache/`, to `.git/index` or to the home folder. The test should compare a hash of the whole fixture tree, including ignored files and the fake home. memory-check's own git calls need `GIT_OPTIONAL_LOCKS=0`, as `memory_index.py:286-288` sets.
   - **k. F1 cannot be tested as written.** It reads `~/.claude/agent-memory/`, and AGENTS.md forbids tests that touch the real home folder. F1 needs an option for the home path. U1's "user memory ... outside the repo" has no path in the guidelines (SOURCE_OF_TRUTH.md:23-25 names only agent memory), so the tool lists only what the guidelines name.

5. **Question 3: the build, in order, smallest first (my #8).** Each piece is tested on a fixture.
   - P1: requirement loader. It reads 64 SoT records and 11 CACHES groups, with ids prefixed by their source.
   - P2: fixture kit. A clean baseline git repo with entries of every kind and status, an `INDEX.md` built by memory_index.py, a journal, an ignored `.cache/` and a fake home, plus a `plant(path, line, replacement)` helper.
   - P3: find (F1, F2, U1, U6).
   - P4: memory_index adapter. It covers the C3 clauses, maps stderr lines to ids, reports *not reached*, and turns "nothing to check" into *not applicable*.
   - P5: memory-check's own file checks (the W1.1a gaps, K4.1 `superseded_by`, W6.3a double supersede).
   - P6: git checks (renames, deletes, K4.3, K6.2 per commit, merges, shallow clones).
   - P7: report, warning and exit code (R1–R3, U3, U4).
   - P8: proof that the run writes nothing (F3, U5).
   - P9: the hook. Its settings diff goes to EJ, and it is installed only on their yes.

   P1–P5 work on one snapshot and cover U1, U2 and U4 without history. P6 is the expensive part, so it comes after a timing measurement.

6. **Test answers worked out another way, so the tests are not circular (my #3, my #4).**
   - *Prediction first (my #3).* A plant manifest, one row per decidable clause: the id, the file and the line replaced. Another engine writes it before the check exists, and it stays out of the builder's files (the house rule on planted controls; the `crossed-build-check` workflow does this). The expected answer is the manifest, not a re-run of the check.
   - *The control (my #4).* The clean baseline must report no fail, and no pass without evidence. Each plant must change its own id and no other id. That catches a check that fires too broadly as well as one that misses.
   - *A second control arm (my #4).* Run `memory_index.py --check` alone on the same plants; that is the current way. It must pass the W1.1a plants, and memory-check must fail them.
   - *Independent references.* The loader's list of ids, levels and checks is compared with `runs/20261017-memory-check/sot-requirements.txt`, which the main agent made in Python. The TypeScript claim parser that K4.3 needs is compared with the claims memory_index.py writes into `INDEX.md` for active entries (`memory_index.py:245-246`). Git checks are compared with the fixture script's own log of what it did ("commit 3 renames D-…"), not with git read back by the same code.
   - *Each plant fails for its own reason* (insight F-21e1586c). Each plant asserts that the line it replaces appears exactly once, and each test asserts that the failing id is the planted one. Earlier, a plant placed at the start of a file passed for the wrong reason.
   - *The tests can fail.* Remove each check function in turn; at least one test must go red. The guard did this before: in `runs/20261015-long-session/r4-mutants.txt`, each removed fix made 4 to 36 tests fail.
   - *A red run's exit must reach what reads it* (insights F-d3132a7f, F-969500fa). Twice, a red run's failure was lost because a `;` or `| grep` followed it. The same trap applies to memory-check reading memory_index.py's exit 0 as a pass (point 4b).

7. **How nature solves it (my #6, my #7; this is *recall* and does not decide).** The thymus removes T cells that attack the body's own tissue before releasing them; detectors are tested against "self" first. What is the same: a detector must fire on a break and stay silent on healthy memory, and the clean baseline plays the part of "self". What is different: the body makes detectors at random and in huge numbers, while each check here is written from one fails_if line. Only the selection step carries over. That step is already the clean control in point 6, which rests on my #4, not on the analogy.

8. **Insights used.**
   - `runs/20261016-four-experts-what-counts-as-change/insight.md#F-21e1586c`: led to the `plant()` helper and the assertion that the failing id is the planted one.
   - `runs/20261016-integrate-r11-r13/insight.md#F-2cdebf3b`: each reader of a contract written in prose checked a different subset. It led to a contract test in P4 that pins memory_index.py's messages, or a structured output if EJ allows a change to memory_index.py.
   - `runs/20261016-four-experts-what-counts-as-change/insight.md#F-d3132a7f` and `runs/20261016-integrate-r11-r13/insight.md#F-969500fa`: an exit code read from a command that did not own it. They led to point 4b (exit 0 is not a pass) and the red-run rule.
   - No category was named, so I chose `check` from the index, plus one `instruction` record (F-2cdebf3b).

9. ***Proposed change to the pattern.*** Some questions have answers that only EJ holds: the required locations, which snapshot, a change to another tool. These should go to EJ at the start, while the pieces that do not depend on them are built. Three trials cannot answer them, and the house rule forbids filling them with my own value. The change: "after three failed trials" becomes "after three failed trials, or at once when trials cannot answer it". Cost: EJ is asked earlier and more often.

## What I need to know
1. **Which memory locations are required (R2, C4)?** If none, the warning carries only failing MUSTs; that is the provisional default, since the guidelines name none. If EJ wants AGENTS.md or others required, that is a new rule that belongs in the guidelines, not in the tool.
2. **Which snapshot do the report and the warning describe?** The choices are HEAD, the staging area (what memory_index.py checks), or the working tree (which nothing reads without writing today). If HEAD plus staging area, which is the provisional default, the tool reads git objects only and says so in its first line.
3. **May memory_index.py change?** The changes would be: fail files in `entries/` whose names do not start with D, F, L, O or H; fail a wrong kind in any status; give per-id output. If yes, C3 stands as written and P4 gets simpler. If no, which is the provisional default, C3 is changed and memory-check checks those clauses itself.
4. **Who classifies the CACHES requirements, which have no `check` field?** Until someone does, all of them are *needs a reviewer*, and *not applicable* while there is no `.cache/`.
5. **Is there a real project with `project-memory/` and a history with merges?** If not, every result comes from fixtures only, with no real-world runs.
6. **Should the start-hook warning include the git-history MUSTs?** These are K4.1, K4.3, W6.3a and K6.2 per commit, and they may make the hook slower than the start hooks that already run. If they are left out, U3 misses failures found in history. If they are kept, every session pays the time. This is a measured comparison, not a number to set now.

## Costs and risks
- **Two parsers can disagree (my #4).** Changing C3 (point 4a) puts a Python parser and a TypeScript parser over the same entries. They can disagree about a claim and make K4.3 fail where memory_index.py sees no change. The `INDEX.md` cross-check covers active entries only.
- **Engine time and harder debugging (my #3).** A plant manifest from another engine costs engine time. A failing check is also harder to debug, because the builder cannot see the plants; that is the point.
- **The baseline could be wrong (my #4, my #7).** We write the baseline fixture ourselves. If it breaks a requirement nobody noticed, every result is measured against a wrong "self". A second engine should review it.
- **A longer reviewer list (my #9).** Reporting mixed and SHOULD findings as *needs a reviewer* gives EJ more to read. The report looks less finished than one that passes them; that is the price of being honest.
- **Early versions cannot see history failures (my #8).** Building the history checks last (P6) means the first versions' warning cannot show K4.1, K4.3 or W6.3a failures. The report must list them as *not built*, never as pass.
- **The contract test breaks when messages change (my #10).** Pinning memory_index.py's stderr text means the test breaks whenever a message is reworded. Until it is pinned, the mapping from messages to ids is a guess.
- **History-check speed is unmeasured (my #2).** Running `--check <rev>` per commit starts one Python process per commit. Measure before choosing.
- **How sure I am (my #10).** The table in point 3 is my reading of the fails_if text, with no runs behind it. Only the memory_index.py facts in point 2 are verified, by its code and its own test.

## How we would know I was right
- **One cheap run first (my #2).** In a fixture, run `memory_index.py --check` with (a) an `entries/X-foo.md` file and (b) a superseded entry with `kind: foo`. My prediction, written now (my #3): exit 0 for both. Exit 1 for either means point 4a is wrong for that clause, and C3 stands for it.
- **One plant, one failure.** The baseline gives no fail. Each plant makes exactly its own id fail, with the planted file named (U2's minimum acceptance). Count misses and extra fails, and report both (my #9).
- **The control arm.** memory_index.py alone passes the W1.1a plants; memory-check fails them.
- **Removed checks.** Removing any one check makes at least one test fail.
- **On this repo.** Every SoT and CACHES requirement comes out *not applicable* (no `project-memory/`, no `.cache/`), and AGENTS.md and CLAUDE.md are listed as present. Any "pass" here is a false pass.
- **Writes nothing.** A hash of the whole fixture, including ignored files, `.git/index` and the fake home, is the same before and after a run.
- **Hook time.** Measure it on fixture histories of growing size and compare it with the start hooks that already run. My prediction: it grows with the number of commits that touch `project-memory/` (because K6.2 runs per commit).

## Recommended plan
1. Decide the four questions provisionally with the defaults above, and send them to EJ now; do not wait for three failed trials.
2. Change C3 so it hands over only what memory_index.py checks. Add the *not reached* result, source-prefixed ids, and the rule that mixed checks and SHOULDs go to *needs a reviewer*. Report the YAML's overstated `tool`/`git` labels to EJ.
3. Have another engine write the plant manifest and the clean baseline before any check code exists.
4. Build P1–P5 on one snapshot. Every plant fails only its own id, and the memory_index.py-only control arm is green.
5. Measure how long the history checks take, then build P6 (git checks and shallow-clone detection).
6. Build P7–P8 (report, warning, exit code, whole-tree proof that nothing is written); removing any check turns a test red.
7. Show EJ the hook's settings diff and install it only on their yes.
8. Run on this repo (expect everything *not applicable*) and on any real project EJ names.
