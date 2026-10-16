# Dave — what a pre-flight check on a brief should verify

## Answer
Check only two things for now. First, for any file going to opencode, fail it if any path in it points to an existing file outside the working directory. Second, fail it if the file is missing, empty or not UTF-8. Run the check in shadow mode inside `six_experts.py run` first, and let it block only once its false fails are fewer than the opencode answers it saves. Everything else stays out: template sections, placeholder text, a wording lint, size, and engine readiness. This repo's own past files show those checks would either fail briefs that worked or catch no failure we have measured.

## How I decided
1. **my #1.** What would change my mind is an item that fails more past files that worked than files that failed, when replayed on this repo's runs. So I measured that before ranking anything.
2. **my #5.** Data already there:
   - There are 67 question files, 397 briefs and 65 `status.json` files (each with its engine and `ok` per expert).
   - `six_experts.py:208` already refuses an empty question.
   - `six_experts.py:214–215` only *warns* when the output folder is outside the working directory. Nothing looks at paths inside the question.
   - `run_node.sh` already caught missing briefs (runs/20261015-ts-hybrid/insight.md#F-08cf4cc3).
   - `codex_left()` (`six_experts.py:94`, `:248`) already covers one engine's quota.
3. **my #2.** I ran a small experiment instead of arguing: read-only greps over `runs/`.
   - **Outside paths.** Eight expert runs name a `~/` path in their question: sot-must-should, its round2, sot-yaml-review, sot-final-review, harness-health, ts-hybrid/experts-spots, four-experts-what-counts-as-change, and six-experts/experts-q1q2.
     - Only one run lost opencode answers to a refused file: experts-q1q2, two seats (runs/20261016-six-experts/insight.md#F-7f938bdf). sot-final-review's opencode seat also failed, but for missing sections, and its log has no rejection.
     - **"Fail any outside mention"** would have stopped all 8 runs, 7 of them wrongly.
     - **"Fail an outside path that is an existing file"** would have stopped 3: harness-health and ts-hybrid (both name `~/.claude/settings.json` as the subject, with the facts written into the question, and opencode answered), plus experts-q1q2. That is 1 right and 2 wrong.
     - The other five name only directories (`~/.claude/`, `~/.claude/agent-memory/reviewer/`). Treating these as directories is *my reading* of how the paths are written; I did not check them on disk.
   - **Template sections.** None of the 397 briefs contains the node-brief template's placeholder text. 79 worker briefs carry some of the six template headings I searched for (Task, Example, Standard, Pieces and progress, Limits, Write the result to). None has all six, and most have three or four. A section check would fail every one of them.
4. **my #6.** How nature solves it: in the thymus, T-cells that react to the body's own molecules are removed before they are released. The mechanism to borrow: before a check may block, run each rule against files whose runs succeeded, and drop or narrow any rule that fires on them. Step 3 was that screen. It removed the section check and narrowed the path check from "any mention" to "an existing file". The biology is recall and only supplies the mechanism; the decision rests on step 3.
5. **my #7.** Does the analogy fit?
   - Same: a detector must not attack "self", a false alarm is costly, and a self set exists (`status.json` labels each answer).
   - Different: our past files include failures, so "self" has to be the files whose runs answered, labelled by outcome. And we have tens of runs, not millions of molecules, so the screen only bounds false fails on past writing styles.
   - The key condition, a labelled known-good set, holds for expert questions. For worker briefs it is weaker. I keep the analogy.
6. **my #10.** Ranking, with evidence size:
   1. **Outside-repo existing files, for files going to opencode.**
      - *What it looks for:* path-like words (in backticks or not, containing `/`, starting with `/`, `~`, `./` or a top-level folder name), skipping URLs.
      - *How a script can tell:* expand `~`, resolve against the working directory, and fail if the result is outside it and `is_file()`. A word containing `$` or a backtick is skipped and logged, not failed: the guard learned that unexpandable paths cause false fails (runs/20261015-long-session/insight.md#F-f09b058d).
      - *What to check:* the brief as built, because that is what the engine reads, not only the question.
      - *Failure it prevents:* opencode silently rejects the read, exits 0 and gives an empty answer (F-7f938bdf). `docs/EXECUTOR_KINDS.md:80–83` shows the same mechanism for `/tmp` writes.
      - *Evidence:* one loss (n=1, two seats); the narrowed rule was right 1 time in 3 in the replay. A hint, not a law.
   2. **The file exists, is not empty and decodes as UTF-8.** The script stats and reads it. It prevents an engine starting on a missing or empty brief (F-08cf4cc3: missing briefs for m4/m5-tests, n=2). It only adds value where no runner already does this, i.e. the hand-run CLI calls in `docs/EXECUTOR_KINDS.md`.
   - **Record, don't fail, during the trial:**
     - Paths inside the repo that do not exist at hand-off. Past files cannot test this, because files have moved since. It shares item 1's parsing.
     - The size in bytes of the brief plus the files it names, per engine. Only mcode has a measured ceiling: 9 KB answered, 44 KB and up stalled (runs/20261016-four-experts-what-counts-as-change/insight.md#F-e69dfb66). mcode is not in the rotation.
7. **Deliberately not verify** (my #5, my #9):
   - **Template sections and placeholders.** Step 3 shows this would fail all 79 worker briefs and catch nothing in 397. The failures it seems to address were about content inside a section that was present: a missing example row (runs/20261016-integrate-r11-r13/insight.md#F-4cbb2f4b) and the result written last (runs/20261015-ts-hybrid/insight.md#F-cf7d58f7). A presence check passes both.
   - **The literal-plus-instruction lint** (runs/20261016-integrate-r11-r13/insight.md#F-05a1b440, option 2). Two hits, one author, one run, in a spec, and never replayed.
   - **Engine readiness** (quota, login, command shape). It is not in the file; it belongs in a canary step before the run (runs/20261016-four-experts-what-counts-as-change/insight.md#F-2cc835e3, runs/20261016-time-monitor/insight.md#F-173e0190, runs/20261015-ts-hybrid/insight.md#F-3b8bdcec).
   - **Fixed template text** (the quote rule, the Chinese-script rule, the answer headings). It is the same on every call, so one unit test in the runner covers it (runs/20261016-time-monitor/insight.md#F-84636a96 — its fix is already in the brief text).
   - **Judgement** (is it one deliverable, is it clear, is the standard right). A script cannot tell, so its pass would mean nothing. *My reading.*
   - **SHOULD rules**, such as evidence living under `runs/<id>/`. A pass/fail check would turn a SHOULD into a MUST. *My reading.*
8. **Time cost.** *My reading, not measured:* parsing a few-KB file and stat-ing a few paths takes milliseconds. Engine calls take 20–220 s (F-e69dfb66: 20, 181, 220 s; F-173e0190: 52 s). So the real price is false fails, and "pays for itself" means fewer false fails than answers saved.
9. **my #8.** Start on one path: `six_experts.py run`, in shadow mode, writing its verdict as a progress line and to `status.json` without blocking anything. Then let it block. Then extend it to `run_node.sh` / `dispatch.py` for worker briefs.
10. **Why a check rather than a rule.** F-7f938bdf (why 4): memory already said "copy inputs in", and the question still named the plan file. runs/20261016-four-experts-what-counts-as-change/insight.md#F-4981093a (why 4): a memory rule was outrun within an hour.
    - *Proposed change to the pattern:* when a written rule has already failed to stop a trap, its fix becomes a check at the moment of action, not a second rule. This changes how insight options are chosen: for a repeat, the check option comes before the rule option.
    - *Proposed change to the pattern:* before a new check may block, replay it on past files in the run folders and count how many files that worked it would fail. That is the reverse of a sabotage test, which only proves it catches bad files. Step 3 shows what this buys.
11. **Insight categories.** The named categories (instruction, tool) missed the most relevant records: F-7f938bdf, F-08cf4cc3 and F-f09b058d are filed under **check**. I read them in their own files.

## What I need to know
- **Do agy and dsh refuse files outside their working directory, like opencode?** Past runs don't say: their questions named outside files the engine never had to read. If yes, item 1 covers them too. One canary call per engine, reading a file under `~/`, settles it (my #2).
- **Is there a list of paths that must never reach a non-Claude engine (private work code)?** If yes, a check that a brief bound for Codex, opencode, dsh or agy names none of them ranks first, because that miss cannot be undone (*my reading*). I was not given such a list.
- **Which use case or vision line does this serve?** I was not given one. If "an engine call either answers or fails loudly" exists, item 1 serves it. If no line fits, the pattern says drop it.
- **Are worker-brief outcomes recorded in one place, like `status.json` is for experts?** If not, the replay cannot screen worker-brief rules, and their trial has to run forward only.

## Costs and risks
- **False fails from item 1** (my #4, my #10): 2 of the 3 replayed runs it would have stopped got their answers anyway. Each false fail costs a rewrite or copying the file in. A 1-in-3 hit rate from 8 runs is a hint, not a law.
- **Misses by item 1** (my #9): a pointer written without a slash, or built with `$`, gets through. The loss then shows up after the call, as it does today (`answer_ok`), and must be logged as a miss of the check.
- **Upkeep of the engine table behind item 1** (*my reading*): a wrong entry means false fails or misses. Its home would be `docs/EXECUTOR_KINDS.md`.
- **Item 2 adds little** where a runner already does it (my #5).
- **The shadow trial delays the benefit** (my #8): a loss during the window is still caught after the call, at the cost of a rerun (about 3–4 minutes per opencode seat, using F-e69dfb66's timings).
- **Leaving out the section check** (my #9): a brief with no example still goes out. The defence stays the test-writer/coder crossing, which caught F-4cbb2f4b and F-05a1b440 only after both engines had run — one repair loop each.
- **The check must change nothing**, but its runtime can still write under HOME (runs/20261016-integrate-r11-r13/insight.md#F-90389583: bun's cache). It needs one test in an empty HOME.
- **Who wrote the replay check** (my #10): the numbers come from greps I wrote myself. They count path mentions, headings and `status.json` `ok` values. They do not show why each opencode answer passed, whether each worker node succeeded, or that the five directory paths really are directories on disk. I also tried a fuller scripted scan; it was refused for approval, so the counts come from grep only.

## How we would know I was right
- **Write the prediction first** (my #3), in the run folder, before switching it on:
  - Metric A: opencode answers lost to a refused outside file (`status.json` not ok, plus "auto-rejecting" in that seat's log).
  - Metric B: false fails, meaning files the check failed that got their answers when sent anyway.
  - Prediction: A falls to zero, and B stays at or below the replay's rate (2 of the 8 runs that named an outside path).
  - The stop date is set by the main agent at the start.
- **Control** (my #4): the replay is the "current way" arm. The check must fail `runs/20261016-six-experts/experts-q1q2/question.md` and pass the other seven. For sabotage, take a copy of a passing question with one `~/` file pointer added, and an empty brief: each must fail on exactly its own item.
- **When to block:** once B is lower than A in the shadow window. That is a comparison, with no number fixed up front.
- **What would change my mind** (my #1, my #9):
  - If shadow fails land mostly on files opencode never tried to read (no "auto-rejecting" line), narrow item 1 further, or move the fix into the runner as copying inputs in.
  - If no opencode answer is lost during the window while false fails happen, drop item 1 and report the null result with the same weight as a success.
