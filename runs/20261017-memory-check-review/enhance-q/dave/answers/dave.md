# Dave — what memory-check should improve after this round

## Answer
The question assumes a review round and fixes that did not happen. `findings.md` and `nodes/fix-r*.result.md` do not exist. The judge step returned 26 s after it started, and the experts were asked right away, so I have 17 unjudged raw findings, not verdicts.

From those, my top improvement is for memory-check to stop reporting "could not look" as "absent" or "pass". A "not applicable" result should need the same evidence as a pass: a read that worked. Second, a project that deletes its whole `project-memory/` should still fail K4.1. Everything else belongs to the fix loop, not to an enhancement.

## How I decided
1. **Use the data that exists first (my #5).** I read the run folder.
   - `runs/20261017-memory-check-review/nodes/review-enhance.progress.md` logs `judge-r1 · start` at 23:11:34 and no done line.
   - `nodes/enhance-q.progress.md` starts the experts at 23:12:00.
   - `review-enhance.js:182` reads `if (!usable(j)) break` and records no problem.
   - So there are no verdicts and no fixes. What does exist: `review/r1-codex.md` (12 findings) and `review/r1-agy.md` (5 findings), about 14 once duplicates are merged. They show where the reviewers looked; they do not show which findings are real. Each finding is n=1, unjudged and unreproduced (my #10).
2. **I grouped the raw findings by cause, not one by one** (my reading). Four of them have one cause: a read that fails is reported as "nothing there". I read each line myself and ran none of them:
   - `r1-codex.md:7`: in `checks.ts:111`, a git error goes into a note, the staged paths come back empty, and `checks.ts:212` then makes every SoT record "not applicable".
   - `r1-codex.md:25`: in `cachechecks.ts:67-69`, an unreadable file is skipped with `continue` and records no break, so Rd1 can pass.
   - `r1-codex.md:21`: in `memory_index.py:354`, `is_object_id` accepts only 40-character ids, so a SHA-256 repository looks like a repository with no memory.
   - `r1-codex.md:19`, the same as `r1-agy.md:192`: in `memory_index.py:483-485`, an unborn HEAD returns 0 before the staging area is read.
3. **Each improvement is tied to a vision line or use case,** as the question requires (my reading).
   - The first group serves the VISION line "Say a requirement passes without the evidence that shows it" (under "never do").
   - It also serves U2's fails-if, "a MUST that fails is shown as passing", and U3's "a MUST that fails or could not run … is not in the warning".
   - It is not a repeat of the last round. That round put could-not-run MUSTs into the warning (`runs/20261017-memory-check/report.md`, Enhance row). These four cases never become "could not run" in the first place, so they get past that fix.
4. **Ask how nature solves it (my #6), and check that the analogy fits (my #7).**
   - Vestibular nerves fire all the time at rest, so a silent nerve reads as damage, not as "no motion". This biology is *recall*.
   - What is the same: the reader must tell "nothing there" from "the sensor is broken".
   - What is different: a nerve signals continuously, while the tool gives one result per run.
   - The key condition, a positive signal every time, can still be met. C2 already requires evidence for every pass. The mechanism I borrow is to require the same for "not applicable": the command and its successful, empty output. Without that evidence, the result is "could not run".
5. **The second improvement comes from a conflict between a spec line and a use case** (my reading).
   - `r1-codex.md:9`: commit an entry, then stage the deletion of all of `project-memory/`. `checks.ts:212` then makes K4.1 "not applicable", so the deletion is never reported and the run exits 0.
   - REQUIREMENTS C4 says absent memory is "not applicable". U2 says a failing MUST must not show as passing.
   - `USE_CASES.md` says "A use case wins over a requirement that conflicts with it". So C4 changes, and the change is flagged. EJ does not need to rule on it: C4's "Who decides" is the guidelines, and K4.1 is a MUST.
6. **No third pick** (my reading, and the owner asked for less work). The remaining raw findings, such as Rd1 reading hooks by their structure (`r1-codex.md:13`, `r1-agy.md:202`), are plain bugs. The judge would accept them without the experts ranking anything.
7. **Write the prediction down first (my #3), always run a control (my #4).** Both are under "How we would know I was right".
8. **Insights used:**
   - `runs/20261016-six-experts/insight.md#F-7f938bdf`: an engine exited 0 with an empty answer, and the empty answer was read as "nothing". Its option 2 is to make a rejection visible instead of empty. This made improvement 1 my top pick, because the tool has the same class of failure.
   - `runs/20261017-read-missing-false-hold/insight.md#F-cd340d9b`: `| tail -5` hid bun's exit code, so failing runs were recorded as successes. Same class; it also backs the pattern change below.
   - `runs/20261015-long-session/insight.md#F-f09b058d`: the opposite failure, a path the check could not resolve treated as a missing file, which gave a false failure. This shaped the first cost below and the control.
   - No category was named; I chose check and tool from the index.
9. ***Proposed change to the pattern*, the workflow (my #9: report what failed).**
   - What failed: the judge returned without writing `findings.md`, and the run went straight to Enhance with nothing to enhance from. This is the same class of failure as improvement 1, inside the workflow itself. It also repeats the last run's failure, "the experts' first ask ran before its question file existed" (`runs/20261017-memory-check/report.md`).
   - What would change: `review-enhance.js:182` records a problem and reruns the judge once. If the judge still returns nothing, the run stops.
   - Enhance starts only when `findings.md` exists, as `design.md:65` already says: "A workflow step starts only after the files it reads exist".
   - I did not read why the judge returned. Whether it failed or dropped all 17 findings is not in the files I read.

## What I need to know
- **Will the main agent rerun the judge and the fix loop before building picks?**
  - If yes, improvement 1 shrinks to the floor rule plus one fault test per read path. The fix loop does the better specific fixes, such as reading the staging area under an unborn HEAD and accepting 64-character ids.
  - If no, improvement 1 is itself the fix for those four cases.
- **Is there a real project with `project-memory/`?** I found none: a Glob for `~/dev/*/project-memory/INDEX.md` returned nothing. This is still open for EJ from the last round (`runs/20261017-memory-check/report.md`, "Open for EJ"). If they name one, run the tool there before either pick (my #5). That run is the calibration.

## Costs and risks
- **Improvement 1 could make the tool cry wolf** (from `F-f09b058d` and my #4). A rule that is too wide turns harmless edge cases into "could not run", the warning gets noisy, and the hook speaks more often. To keep it honest, each could-not-run carries the error text, and the control below must stay unchanged.
- **Improvement 1 costs about four fault fixtures** (my #8). Build the `git ls-files` one first, check it, then add the rest. Making a file unreadable may not work on WSL or as root (*recall*).
- **Improvement 2 changes a spec line,** C4 in `memory_check/REQUIREMENTS.md`, under the use-case-wins rule, and the change must be flagged. The history checks would also run on repositories with no current memory, so more git calls. The last round's cost model, about N × (3 + 2c) git calls, is labelled "his reading" in `runs/20261017-memory-check/enhance-q/compare.md:96`.
- **Improvement 2 may still be silent at session start** (*not checked*, my reading). The last round made the hook speak only where `project-memory/` exists. If that test looks at the working tree, a full deletion still prints no warning.
- **The evidence is thin** (my #10). Every case is one reviewer's claim, and I read the code without running it.
- **The two reviewers are less independent than two engines suggest.** `r1-agy.md:55-56` quotes the earlier run's Codex review (`runs/20261017-memory-check/nodes/review.codex.md`).
- **The pattern change costs one more judge call** when the judge fails, and nothing on the tool.

## How we would know I was right
I wrote these predictions before any run (my #3). The stop date is the end of this run's time box.
1. The four fault tests from improvement 1 are red on HEAD: each exits 0 where 1 is required.
2. The deletion fixture from improvement 2 is red on HEAD: K4.1 shows "not applicable" and the run exits 0.
3. After the fix:
   - Each fault test gives "could not run" with the error, exits 1, and prints one `--warn` line.
   - The deletion fixture fails K4.1, names the deleted file, and exits 1.
   - A repository that never had `project-memory/` still gives "not applicable" and exits 0.
4. Control (my #4): the baseline (74 bun tests, 465 pytest, tsgo clean) and this repo's smoke report stay unchanged.
5. A second review round finds no new case of an error reported as absent.

**I am wrong if:**
- Any of the four is already green on HEAD. That finding was not real; drop it and report it (my #9).
- The control changes.

**Top one:** memory-check should never report "could not look" as absent or passing: "not applicable" needs the evidence of a read that worked, or the result is "could not run".
