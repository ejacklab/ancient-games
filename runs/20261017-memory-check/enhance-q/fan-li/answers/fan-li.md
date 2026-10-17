# 范蠡 (Fan Li) — What memory-check v1 should improve next

## Answer
Complete the planned defenses before inventing new ones: calibrate the tool against a real repository with `project-memory/` to examine its preparations on actual terrain, and package the session-start hook settings diff for EJ's approval so agents receive warnings at startup as promised. If no real repository is currently designated, enforce boundary handling for shallow Git clones, simplify heuristic cache instruction parsing into clean reviewer delegations, and stop at the boundary of v1 without planning early for unbuilt stores.

## How I decided

1. **Examine the preparations on real terrain (my #18).** In 國語·吳語, when asked what would make it possible to fight, I asked: 「審備則可以戰乎？」王曰：「巧。」 (`quoted`).
   - **Improvement 1 (Rank 1):** Calibrate and verify `memory-check` on a real repository containing active `project-memory/`.
   - **Use case / vision line:** Serves U6 ("Work on any project") and `memory_check/VISION.md` ("The project owner, who wants to know, without reading the guidelines, whether a project's memory follows them").
   - **Case showing it is needed now:** Fact: the tool passes 70 tests (55 acceptance, 15 review) across synthetic fixtures (`memory_check/test/acceptance.test.ts`, `review.test.ts`), but no real project with `project-memory/` has ever been checked (Source: `runs/20261017-memory-check/nodes/smoke-report.md:127`, `design-decisions.md:15`). Synthetic fixtures do not capture real-world Git branching, merge topologies, unstaged edge cases, or genuine entry writing styles.
   - **How to check it is done:** Point `memory-check --project <path>` at a real repository containing `project-memory/`; verify that the report generates with exit code 0 (or 1 on genuine breaks), outputs accurate evidence with line numbers and commit hashes, produces zero uncaught runtime exceptions, and leaves working-tree and Git status completely untouched (U5).

2. **Finish what was begun and follow the time (my #4).** In 國語21:21, I said: 「得時無怠，時不再來，天予不取，反為之災。」 (`quoted`).
   - **Improvement 2 (Rank 2):** Package the session-start hook installation diff for owner approval.
   - **Use case / vision line:** Serves U3 ("Be warned at the start of a session") and `memory_check/VISION.md` ("Every agent starting a session, which must not start work on memory that is missing, stale or broken without being told").
   - **Case showing it is needed now:** Fact: the session-start hook is not built yet because it needs the owner's yes to a harness settings diff (Source: `memory_check/REQUIREMENTS.md` R2, `runs/20261017-memory-check/design-decisions.md:8, 15`). The underlying command `--warn` is implemented and verified (Source: `runs/20261017-memory-check/nodes/fix-2.result.md:17`), but until the hook is packaged into a concrete settings diff and submitted to EJ, agents start sessions unwarned, leaving half the tool's vision unfulfilled.
   - **How to check it is done:** Prepare the harness settings diff (R12.3); when accepted by EJ, launch an agent session in a test workspace containing planted MUST failures; verify that the hook executes at startup, prints exactly one line per failing MUST or missing `AGENTS.md` with file names and ids only, opens no cache file, and outputs nothing on a clean repository.

3. **Keep the plan from shifting at the boundary (my #5).** In 國語21:23, I said: 「夫謀之廊廟，失之中原，其可乎？王姑勿許也。…贏縮轉化，後將悔之。天節固然，唯謀不遷。」 (`quoted`).
   - **Improvement 3 (Rank 3):** Explicitly detect shallow Git clones and report history-dependent requirements as "could not run" rather than false passes.
   - **Use case / vision line:** Serves U2 ("Know what breaks the guidelines") and `memory_check/VISION.md` ("Say a requirement passes without the evidence that shows it [will never do]").
   - **Case showing it is needed now:** Fact: `REQUIREMENTS.md` C5 explicitly dictates that "A shallow clone makes history checks 'could not run'" (Source: `memory_check/REQUIREMENTS.md` C5). In CI systems or shallow local clones (`git clone --depth`), history-dependent requirements (`SoT:K4.1`, `SoT:K4.3`, `SoT:W6.3a`) cannot inspect full parentage. If the tool evaluates truncated logs as complete history, it emits false passes.
   - **How to check it is done:** Run `memory-check` on a fixture repository cloned with `--depth 1`; verify that all history checks evaluate to "could not run" with shallow repository noted in the evidence, exit code reflects R3, and no history requirement is falsely marked pass.

4. **Measure input against constant limits (my #3).** In 國語21:9, I said: 「時不至，不可彊生；事不究，不可彊成。自若以處，以度天下，待其來者而正之，因時之所宜而定之。」 (`quoted`).
   - **Improvement 4 (Rank 4):** Validate CLI arguments for missing directories and non-Git paths with explicit usage error exit code 2.
   - **Use case / vision line:** Serves U6 ("Work on any project — a path that does not exist is an error, not an empty report") and `memory_check/REQUIREMENTS.md` F2/R3.
   - **Case showing it is needed now:** Fact: F2 requires `--project <path>` to be the root of a Git repository and fails if a non-Git path is checked instead of being a usage error (Source: `memory_check/REQUIREMENTS.md` F2, R3).
   - **How to check it is done:** Execute `memory-check --project /nonexistent/path` and `memory-check --project <non-git-dir>`; verify that the tool immediately prints a usage error to stderr and exits with code 2, without generating a report file or claiming zero memory exists.

5. **Stop at Heaven's limit and enforce the operational bound (my #10).** In 國語21:25, I said: 「臣聞古之善用兵者，贏縮以為常，四時以為紀，無過天極，究數而止。」 (`quoted`).
   - **Improvement 5 (Rank 5):** Benchmark and latency-bound session-start warning execution.
   - **Use case / vision line:** Serves U3 ("Be warned at the start of a session").
   - **Case showing it is needed now:** Fact: U3 wins over a narrower hook, requiring every check to run to produce the warning lines (Source: `memory_check/REQUIREMENTS.md` R2). Invoking `tools/memory_index.py` as a Python subprocess plus Git staging inspections adds startup latency. If startup overhead exceeds agent tolerance, the hook will be abandoned.
   - **How to check it is done:** Benchmark `memory-check --warn` across 20 invocations on this repository and a 50-entry fixture; verify that median execution time stays strictly under 100ms.

6. **What to remove or simplify: say who is better at what, and do not plan early (my #14, my #7).**
   - In 國語21:7, I said: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 (`quoted`). In 國語21:13, I said: 「未可也。蠡聞之，上帝不考，時反是守，彊索者不祥。…有奪，有予，有不予，王無蚤圖。」 (`quoted`).
   - **What to simplify/remove:** Simplify natural-language heuristic parsing in `cachechecks.ts` (`checkRd1`) and remove any speculative expansion into unbuilt cache stores.
   - **Reasoning:** Fact: Codex review finding 10 (`runs/20261017-memory-check/nodes/review.codex.md:25`, `fix-2.result.md:16`) demonstrated that trying to parse English prose with regexes to determine whether an instruction opens a cache file at startup generates fragile and unsupported verdicts. Discerning English intent in instructions belongs to the human reviewer (U4), not a regex heuristic. Furthermore, `project-memory/.cache/` does not exist in this project or standard projects today (Source: `runs/20261017-memory-check/nodes/smoke-report.md:16, 100-111`). Attempting to implement checks for SQLite tables (B4.1, K1.1) before the cache engines exist violates "do not plan early" (my #7). Keep CACHES v1 strictly limited to B2.2 (Git ignored) and delegate any non-obvious natural-language instruction directly to "needs a reviewer" (U4).

7. **Improving the workflow pattern (my reading):**
   - *Proposed change to the pattern:* Classify run questions by decision authority (my #14).
   - In EJ's workflow pattern, "A question goes to EJ only after three failed trials on it or once the time is used up." When a question concerns mechanical code or test failures, three trials are proper. But when a question requires owner consent, harness configuration approval (R12.3), or external repository assets (design-decisions.md 15), automated trials cannot solve it. Running three automated trials on an owner authority gate wastes time. Authority and permission questions should go directly to EJ without waiting for three failed automated trials.

8. **Top three in three lines (my reading):**
   1. Calibrate and verify `memory-check` on a real repository containing active `project-memory/` (U6, my #18).
   2. Package and submit the session-start hook configuration diff for EJ's approval (U3, my #4).
   3. Detect shallow Git clones and report incomplete history as "could not run" rather than false passes (U2, my #5).

## What I need to know
- Which repository containing genuine `project-memory/` does EJ designate for calibration (design-decisions.md 15)? If none is available, we must conditionally synthesize a multi-branch Git fixture containing real merges and historical edits to simulate terrain.
- Does EJ approve installing the session-start hook into their harness configuration (REQUIREMENTS.md R2)? If yes, we prepare the diff immediately; if no, `--warn` remains an on-demand command and U3 is deferred.

## Costs and risks
- **my #18 (Calibrating on real terrain):** Running on a real repository risks exposing unforeseen edge cases in Git history or ambiguous guideline phrasing, requiring time to triage whether discrepancies stem from the tool or the guidelines.
- **my #4 (Completing the hook diff):** Installing a session-start hook risks introducing noticeable startup latency if Python subprocess execution (`tools/memory_index.py`) degrades as entries scale.
- **my #5 (Enforcing shallow clone limits):** Marking shallow clone history as "could not run" will cause automated CI environments with default shallow checkouts to exit 1 (R3), requiring CI pipelines to explicitly configure full clone depth or `--since`.
- **my #14 (Simplifying heuristic parsing):** Delegating ambiguous natural-language instructions to "needs a reviewer" increases the count of items requiring EJ's manual review in the report.

## How we would know I was right
- Running `memory-check --project <real-project>` on an active project with `project-memory/` completes without unhandled errors, correctly classifies staged versus committed entries, and outputs clean Markdown with no raw entry text leaks.
- The session-start hook triggers reliably on session launch, executes in under 100ms, outputs exactly one line per failing MUST or missing `AGENTS.md` when broken, and outputs zero lines when clean.
- Running `memory-check` in a Git repository cloned with `--depth 1` marks history-dependent requirements (`SoT:K4.1`, `SoT:K4.3`, `SoT:W6.3a`) as "could not run" citing shallow history, with zero false passes.
