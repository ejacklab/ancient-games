# Answer — what memory-check v1 should improve next

## Answer
Make `--warn` report a MUST that could not run, run the tool once on a real project, then install the session-start hook. The hook is the most valuable piece, but it should go in only after the other two. I found nothing in the code worth removing; I'd collapse the repeated "not applicable" lines in the report, but only after the real-project run.

**Top three:**
1. Install the session-start hook (U3), run from the git root with the bun cache off, after improvement 2 is done.
2. Make `--warn` say when a MUST could not run (U3 purpose, vision line "must not start work on memory that is … broken without being told"). EJ must widen U3's wording first.
3. Run the tool on one real project that has `project-memory/` (U1, U2). EJ must name the project.

## How I decided

1. **What I checked.**
   - I read `USE_CASES.md`, `VISION.md`, `REQUIREMENTS.md`, `design-decisions.md`, the review, `fix-2.result.md` and the smoke report.
   - I read `command.ts`, `cli.ts`, `warn.ts`, `report.ts`, `guidelines.ts` and the `exitCodeOf` function in `checks.ts`.
   - I diffed the tool's `guidelines/` copy against `docs/memory-system/`. Both files are identical today.
   - I could not re-run `bun test` because it needed approval, so "70 pass" is the brief's figure.
   - I measured no run times.
2. **U3 is the only one of the owner's three use cases that cannot be met today.** U1 and U2 have tests. U3 needs the hook, which is not built (`REQUIREMENTS.md` R2, `design-decisions.md` 15). The vision's second audience, "every agent starting a session", has nothing yet.
3. **The 55 acceptance tests were written from the spec, and review still found 14 defects.** By my reading of `review.codex.md`, nine of them made a real break read as a pass or clean result (findings 1, 2, 4, 5, 6, 7, 8, 9, 12). Finding 3 made it "not applicable". The reviewer says its own probes only confirm code paths (`review.codex.md:5`). So fixtures built from the same spec share its blind spots. The tool has never seen real memory: the smoke report has 6 of 8 locations absent and says "Not calibrated on a real project" (`smoke-report.md:127`). A search under `~/dev` found no `project-memory/` folder.
4. **One silent hole is visible in the code itself.**
   - `warn.ts:45-47` prints only MUSTs whose verdict is `fail`.
   - `checks.ts:178-181` makes a MUST that "could not run" exit 1.
   - Per `fix-2.result.md:29`, a `python3` that only prints a traceback makes every tool clause "could not run".
   - Reading the code, the warning for that case is empty, and an empty warning looks like "all clear". A shallow clone does the same to the history MUSTs (C5).
   - None of the `--warn` tests covers it; all of them plant a `fail`.
   - I did not run it, so this is my reading.

**Ranked improvements**

1. **Install the session-start hook.**
   - *Serves:* U3, and the vision's "warnings at the start of a session".
   - *Needed now because:* U3 cannot be met without it. The hook pattern already exists (`~/.claude/settings.json:89`, a `SessionStart` entry), so the diff is small.
   - *Design traps, all from the code:*
     - **Launch folder.** The tool requires the git root and returns exit 2 plus usage text from any subfolder (`command.ts:77-86`; test `acceptance.test.ts:45`). The hook command must resolve the root first and stay silent outside a git repository.
     - **Exit code.** R3 makes a failing MUST exit 1. I believe (*recall*) a non-zero `SessionStart` hook exit is treated as an error and its stdout is not injected. If that is right, the command needs a wrapper that always exits 0.
     - **Process count.** `cli.ts:17` re-spawns bun unless `BUN_RUNTIME_TRANSPILER_CACHE_PATH` is already `0`. If the hook command sets it, the second process is skipped with no code change.
   - *Done when:* see the first test under "How we would know I was right".
2. **Say in the warning when a MUST could not run.**
   - *Serves:* U3's purpose ("told … what is missing or failing") and the vision.
   - *Needed now because:* step 4. The fix is one line per reason, for example "3 MUSTs could not run: python3 crashed".
   - *Conflict:* U3's "Fails if … the warning holds anything else" forbids it, and a use case wins over a requirement. So EJ widens U3 first. I am not guessing the wording.
   - *Done when:* a fixture with a crashing `python3` stub gives a non-empty `--warn`. Write the red test first, as `AGENTS.md` asks.
3. **Run on one real project with `project-memory/`, then fix what shows.**
   - *Serves:* U1 and U2. U2's "Fails if" is a wrong pass or fail, which fixtures can only partly show.
   - *Needed now because:* steps 3 and 4. The hook would run this tool at every session start.
   - *Done when:* every result on that project is read by EJ, and each one they disagree with becomes a test and a fix, or a written spec point.

**Remove or simplify**

- **Nothing to remove.** Every module serves U1–U6. `--home` is needed for the F1 agent-memory location and for tests. I would keep `--since` because C5 gives it to the owner, but I would not extend it. No use case names it, and it produced review finding 6.
- **Collapse repeated results in the report.**
  - *Serves:* U1 and the vision's "tells the user what is there".
  - *Case:* in the smoke report, 72 of 78 results carry the same ~230-character reason. The three passes and three reviewer items sit among about 100 boilerplate lines.
  - *Change:* group identical "not applicable" results into one line that still lists every id. R1 allows this, because its fail condition is a *missing* id.
  - *Timing:* wait for improvement 3. A real project will show whether the reviewer list, about 45 items by my count of the YAML, is the bigger problem.
- **Not proposed.**
  - A guideline-drift check on the bundled copy: no case yet, since the copies are identical.
  - Removing the second bun process: the hook can skip it by setting the variable.

## What I need to know
1. **Which real project can the tool run on?** `design-decisions.md` 15 says none is known. If there is none, improvement 3 cannot happen. The tool then stays proven on fixtures only, and I would delay the hook, since it would have little to warn about beyond a missing `AGENTS.md`.
2. **Should the hook be global, like the guard hooks, or per project?** Global means every project without an `AGENTS.md` gets the "AGENTS.md is missing" line at every session start.
3. **Does EJ accept widening U3 to include "a MUST could not run"?** If not, the silent hole stays, and the owner should know it is there.
4. **Is the calibration project one EJ is willing to have read in this session?** EJ's rule on private work code says to ask first.

## Costs and risks
- **Hook time is unmeasured.** R2 requires all checks to run in the hook, history included. `design-decisions.md` 8 had a narrower hook, but R2 reversed it because U3 wins. Git work grows with the commits that touch `project-memory/`. If it is slow, the narrower hook is the fallback, and that is EJ's call.
- **A global hook adds a line to sessions in projects that have no `AGENTS.md`.** This is U3 as written, but EJ may not want it everywhere.
- **Widening U3 adds output to every session start.** Group it as one line per reason, not per MUST.
- **A real project will likely find defects.** Each one costs an engine run plus a test.
- **My points rest on code reading and the brief's figures.** The hook exit-code behaviour is *recall*. I ran and timed nothing.

## How we would know I was right
- **Hook (1).** Take a fixture with one planted MUST break and run the exact command from the settings diff, from the root and from a subfolder. Pass means exactly one line per failing MUST, the same run on a clean fixture is empty on stdout and stderr, and the hook exits 0. A real session start should show the line. Compare wall time against the existing guard `SessionStart` hook; no threshold is invented.
- **Warning (2).** The new test fails on today's code and passes after. A fixture whose `python3` crashes, or a shallow clone, gives a non-empty `--warn`.
- **Calibration (3).** Count the results EJ disagrees with on the real project. Zero is also a result, because it means the fixtures were enough and the hook is safe to install. If it finds some, each becomes a failing test first.
- **Overall.** After a few weeks of the hook running, EJ reviews the warnings it printed. Mostly true warnings and no session where a broken memory started silently means this ranking was right.
