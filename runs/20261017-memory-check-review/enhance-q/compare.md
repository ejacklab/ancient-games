# Six experts — after this round of review and fixes, what should the memory-check tools improve?

Question: `runs/20261017-memory-check-review/enhance-question.md`. Six of six answers usable (Dave after one rerun).
This file compares; it does not pick a winner or decide. The main agent decides.

Labels: *quoted* (an answer's own words), *my reading* (the comparer's), *not measured* (nobody here ran it).

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | *quoted* "Top one: prevent `--out` from overwriting memory." | *quoted* "Calibrate and verify `memory_check` against a real multi-branch repository containing `project-memory/` to validate readiness before declaring completion (U6 / `VISION.md:10`)." | *quoted* "refuse `--out` paths inside memory — a checker must not be able to overwrite what it checks." | *quoted* "one rule — a check that examined nothing is never a clean state — proved by a planted matrix of five states" | *quoted* "memory-check should never report \"could not look\" as absent or passing: \"not applicable\" needs the evidence of a read that worked, or the result is \"could not run\"." | *quoted* "make `memory_check` report `could not run`, not `pass`, whenever its own staged read and `memory_index.py` disagree about whether entries exist." |
| Rank 1 | `--out` guard incl. aliases (VISION:22) | real-repo / multi-branch calibration (U6, VISION:10) | `--out` guard (VISION:22, U5) | fail-open rule + 5-row planted matrix (U2, U3, C2, R3) | "not applicable" needs a successful read (VISION "never do", U2, U3) | guard: staged read vs tool's `noMemory`/`unbornHead` (U2, U3, VISION) |
| Rank 2 | file paths carried as data into warnings (U3, U2) | Python/TS boundary contract (VISION:26, U2) | fail-closed matrix over every input | one judge per clause at the `memory_index.py` seam, 9-row table (U2, C3, VISION:26) | full `project-memory/` deletion still fails K4.1 (U2; C4 changed under use-case-wins) | fault-injection test over every input (U2, VISION) |
| Rank 3 | none given | agent-memory location enumeration (U1, F1) | drop static "hook is not installed" line (`report.ts:101`) | take the self-asserted pass out of F2/F3 (U2, C2, VISION:23) | none — *quoted* "No third pick" | conditional: one real-project run, only if EJ names one |
| Main items used | #7, #2, #1, #3, #13, #9, #10, #5, #18 | #18, #14, #2, #3, #7, #5, #10 | #1, #2, #5, #17, #15, #6 | #6, #7, #8, #16, #2, #13 | #5, #10, #6, #7, #3, #4, #9, #8 | — |
| Insights cited | — | — | — | — | `runs/20261016-six-experts/insight.md#F-7f938bdf`, `runs/20261017-read-missing-false-hold/insight.md#F-cd340d9b`, `runs/20261015-long-session/insight.md#F-f09b058d` | — |
| Ran anything | yes — *quoted* "My in-memory probe intercepted an attempted overwrite" | no (read only, *my reading* of the answer) | yes — *quoted* "the index's sha256 changed and `git status --short` showed `M project-memory/INDEX.md`" | no | no — *quoted* "I read each line myself and ran none of them" | no — *quoted* "I did not run any probes" |
| Proposed pattern change | — | ask enhance only after `verify-r*` exits 0 | — | reproduce (P3) before judge (P2); a cross-citation carries its text | judge rerun once at `review-enhance.js:182`, then stop; enhance only when `findings.md` exists | — |

## Where they agree

- **All six: the review verdicts and fixes the question names do not exist.** *quoted* Dave "The question assumes a
  review round and fixes that did not happen"; Linus "`findings.md` and `fix-r*.result.md` were absent when
  checked"; 孫子, 老子 and Dario say the same with `nodes/review-enhance.progress.md:7`; 范蠡 asks it as his question 2
  and builds his pattern change on it. *my reading*, checked at 23:20: `runs/20261017-memory-check-review/` holds no
  `findings.md`, and `nodes/review-enhance.progress.md` ends at `judge-r1 · start` (23:11:34) with no done or fail
  line. So every answer rests on the two raw, unjudged reviews `review/r1-codex.md` (12) and `review/r1-agy.md` (5).
- **Five of six (not Linus) name one class: an input that was not read, or could not be read, gives a clean
  verdict.** 孫子 #2, 老子 #1, Dave #1, Dario #1 and #2, 范蠡 #2 (the Python/TS seam) and the cases under his #1. They
  cite the same raw findings: `checks.ts:111`/`:212` (failed `git ls-files` → every SoT record "not applicable"),
  `cachechecks.ts:66-71` (unreadable settings → Rd1 pass), `memory_index.py:483` (unborn HEAD → exit 0 before the
  staging check), `memory_index.py:354` (SHA-256 ids). *my reading*: 老子, Dave and Dario make it their top one.
- **Three want one table-driven fault test over every input instead of one fix per finding**: 孫子 #2 (*quoted* "a
  table of every input the tool reads ... each with an injected read failure"), 老子 #1 (five rows), Dario #2 (one row
  per input). Dave asks for four fault fixtures built one at a time. *my reading*.
- **Two put the `--out` guard first, both for the same reason (the one irreversible action)**: Linus #1 and 孫子 #1,
  both citing `command.ts:118` and `VISION.md:22`, both having run a probe. 孫子 *quoted* "I put the irreversible action
  first"; Linus's check also covers aliases. No other expert mentions `--out`. *my reading*.
- **None repeats what the previous round applied**: 孫子, Dave and Dario each say so and name the applied items
  (could-not-run warning, unstaged count, Not applicable section, scoped hook). *quoted* / *my reading* that the
  others do not repeat them either.
- **Three warn the fail-closed rule can make noise in the session-start hook**: 老子 cost 1, Dave cost 1 (*quoted*
  "could make the tool cry wolf"), Dario (*quoted* "a wrong guard costs noise in the live hook"). 孫子 answers the same
  risk the other way (see below).

## Where they disagree (side by side, quoted; never averaged)

**1. What goes first.**

| Expert | Top pick | Their reason |
|---|---|---|
| Linus, 孫子 | `--out` guard | 孫子 *quoted* "A wrong verdict can be corrected; memory overwritten before it is committed cannot." |
| 老子, Dave, Dario | the fail-open class | 老子 *quoted* "that one shape is seven of the fourteen distinct defects this round found"; Dave *quoted* "Four of them have one cause: a read that fails is reported as \"nothing there\"" |
| 范蠡 | real-repository calibration | *quoted* "the tool has only been checked against synthetic single-commit fixtures" |

**2. A real project versus a fixture standing in for one.**
- 范蠡 *quoted*: "Run `memory-check` against either an active real project containing `project-memory/` or a
  synthesized multi-branch git fixture".
- Dario *quoted*: "If not, drop improvement 3 and do not build a stand-in. A fixture written to match the tool is not
  evidence."
- Dave: run the tool on a real project "before either pick" if EJ names one; 老子: *quoted* "None of my three
  improvements depends on it".

**3. Where the `memory_index.py` seam is fixed.**
- 老子 *quoted*: "one table names the single judge for each of the nine `tool` records"; it *quoted* "cannot be built
  before Q2 is answered".
- 范蠡 *quoted*: "Either `memory_index.py` must return structured error classifications or `memory_check` must
  explicitly check the clauses Python suppresses".
- Dario: a guard on the TypeScript side, in `checks.ts:237-264`.
- Dave *quoted*: "The fix loop does the better specific fixes, such as reading the staging area under an unborn HEAD
  and accepting 64-character ids."
- Linus *quoted*: "changing Python's entire output protocol would enlarge the work unnecessarily."

**4. Is a false "could not run" safe?**
- 孫子 *quoted*: "A false `could not run` is possible, but it is visible in the warning (U3) and exits 1, so it fails
  safe."
- 老子 *quoted*: "the wrong answer here is not a missed break, it is a session that starts with noise the owner cannot
  act on."

**5. The file names in warnings (`warn.ts`).**
- Linus rank 2: *quoted* "a bare Python filename disappears, while a path containing spaces and Chinese characters is
  truncated."
- Dario *quoted*: "It is small and is the fix loop's to take."

**6. The third slot.** Linus and Dave give none (Dave *quoted* "the owner asked for less work"); 范蠡 the agent-memory
location; 孫子 the static hook line; 老子 F2/F3; Dario a conditional real run. No two agree. *my reading*.

**7. Changing the workflow itself.** Three different changes, none shared:
- 范蠡 *quoted*: "sequence the enhance consultation strictly after `verify-r*` exits 0".
- Dave *quoted*: "`review-enhance.js:182` records a problem and reruns the judge once. If the judge still returns
  nothing, the run stops."
- 老子 *quoted*: "Move P3 before P2, so a finding enters the judge only after a test fails on HEAD for its reason".

## What each added that the others did not

- **Linus**: `--out` aliases to memory files, not just the literal path; carry file paths as data from each finding
  producer to `warn.ts:48`, not parsed from prose — with his own probe of the bare-name and space/Unicode cases.
  *quoted* / *not measured* by me.
- **范蠡**: `locations.ts:68-71` lists regular files under `~/.claude/agent-memory/` as directory locations, and Claude
  Code's real memory lives in `~/.claude/projects/*/memory/MEMORY.md`; a calibration fixture with merges, unborn HEAD
  and SHA-256 history. *quoted*.
- **孫子**: `report.ts:101` still prints "The session-start hook is not installed" though `settings-diff.md:38` and
  commit `7f1f67a` record it applied; the previous round's 孫子 proposed removing it and it was not applied. The only
  expert who measured the `--out` overwrite on a git fixture. *quoted*.
- **老子**: F2 and F3 are hard-coded `verdict: "pass"` at `checks.ts:145-160` with no command output, a pass with no
  evidence that *quoted* "both reviews missed"; `design.md:7` Q2 ("`memory_index.py` is in scope for fixes") and
  `REQUIREMENTS.md:43` C3 ("never changes `memory_index.py`") contradict; agy's review cites a "finding 8" whose text is
  not in Codex's file; `indextool.ts:126` drops every `(warning)` line, so a retired entry with a wrong `kind` gives
  SoT:W1.1a pass. *quoted*.
- **Dave**: `r1-codex.md:9` — staging the deletion of all of `project-memory/` makes K4.1 "not applicable", exit 0 —
  and the C4 change under the use-case-wins rule; *quoted* "EJ does not need to rule on it". `review-enhance.js:182`
  `if (!usable(j)) break` records no problem; *quoted* "The judge step returned 26 s after it started" (*not measured*
  by me: the progress log has no judge end line). The cited insights. *quoted*.
- **Dario**: `checks.ts:262` uses the unborn-HEAD note only for `AFTER_ENTRIES` clauses, so a staged `status: bogus`
  entry probably passes W4.1b; `tests/test_memory_index.py:774-785` tests only `--check HEAD`; the fault test should be
  written by another engine than the fixer (`crossed-build-check`). *quoted*.

## What they need to know (questions merged, each with its options)

1. **Which round-1 findings were accepted, and did any fixes land?** (all six)
   - The judge is rerun and the fix loop runs first; the enhance picks shrink to the general rule and its test (Dave,
     Dario, 孫子).
   - Enhance goes ahead on the raw reviews; the picks themselves are the fix for the fail-open cases (Dave's "if no").
   - Fixing and verifying round 1 comes before any enhancement (范蠡: *quoted* "takes absolute priority").
2. **Is there a real project with `project-memory/` to run on?** (范蠡, Dave, Dario, 老子)
   - EJ names one: one read-only run there, every verdict hand-checked.
   - None: build a multi-branch fixture instead (范蠡).
   - None: drop it, no stand-in (Dario).
3. **Is `memory_index.py` in scope to change, given C3 says never?** (老子; bears on 范蠡 #2 and Dario #1)
   - Yes: the seam's fixes go into the Python tool, and C3's line is changed and flagged.
   - No: the fixes stay on the TypeScript side (Dario's guard, 范蠡's second option).
   - *my reading*: the relayed request for this run says "memory_index.py in scope", and `design.md:7` Q2 says the same;
     `REQUIREMENTS.md:43` C3 still says the opposite. Whether that request also amends C3 is for the main agent.
4. **Is a `(warning)` from `memory_index.py` a break for SoT:W1.1a (a retired entry whose `kind` contradicts its
   prefix)?** (老子)
   - Yes, in every status (老子's reading).
   - No: an inactive entry's kind is no clause's business.
5. **Does a test's name count as F3's evidence under C2?** (老子)
   - Yes: the report cites the test.
   - No: F3 leaves the report.
   - No: F3 stays and prints a command and its output.
6. **May `--out` ever point inside `project-memory/` or at an instruction file?** (孫子, Linus)
   - No: usage error, exit 2, bytes unchanged (both).
   - Yes: then it is a separate command with its own risk (孫子).
7. **Should the report say whether the session-start hook is installed?** (孫子)
   - Drop the line (his proposal).
   - Compute it, which adds a read of the harness settings outside the project.
8. **Which agent-memory location does F1 report?** (范蠡; Dario calls it EJ's)
   - Add `~/.claude/projects/*/memory/MEMORY.md`, amending F1.
   - Keep `~/.claude/agent-memory/<name>/` per SOURCE_OF_TRUTH and only stop listing regular files.
9. **Change the workflow?** (three separate proposals, not one)
   - Enhance only after `verify-r*` exits 0 (范蠡).
   - Rerun a judge that returns nothing once, then stop; enhance only when `findings.md` exists (Dave).
   - Reproduce before judging (老子).
   - None of them.
10. **A fact to check before Dario's guard, not a choice**: does `memory_check`'s staged-entry read use the same
    `[DFLOH]-*.md` filter as `memory_index.py`? If it does, the guard is safe as written; if not, align the filter
    first, or the guard gives false could-not-run results. (Dario; *not measured*.)

## Check

- **Results**, from the workflow and each `check.txt` (*quoted*): linus pass, 范蠡 pass, 孫子 pass, 老子 pass, Dave pass
  after one rerun, Dario pass. Each `check.txt` ends `FAIL: 1 answers, 5 failure(s)`; all five FAIL lines name the
  *other* experts with "no answer file", because each check ran in that expert's own subfolder. No FAIL line names the
  expert whose folder it is (*my reading*, from all six files).
- **Engines** (each `status.json`): Linus `codex` / `gpt-6.1-sol` (not the mcode fallback); 范蠡 `agy` /
  `gemini-3.8-flash-medium` (not the Claude fallback); 孫子 `dsh` / `deepseek-flash (dsh headless profile)`; 老子
  `opencode` / `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`; Dave `claude` / `claude-opus-5-5`; Dario `claude` /
  `claude-sonnet-5-5`. All exit 0.
- **Dave's rerun**: the first call ended `claude exit 1` at 23:12:35 and its check failed (*quoted* "5 missing
  sections, no citations"); the rerun started 23:12:58 and passed. `status.json` holds only the rerun.
- **Other things seen** (*my reading*): 老子's answer file opens with a stray line, "I'll read the brief first.",
  before its heading. 老子 started at 23:17:39, about five minutes after the others; the progress log gives no reason.
  agy's review (`review/r1-agy.md`) began with leaked thought text citing Codex's review (`review-enhance.progress.md`),
  which 老子 and Dave both note weakens the two reviews' independence.
- **What the check does not establish**: the check script was written by Claude. It confirms the answers' shape and
  that their citations resolve; it does not establish that any expert applied its rules correctly, nor that any code
  claim is true. The only behaviour measured in these answers is Linus's in-memory probe and 孫子's fixture run, both by
  the experts themselves; the comparer reproduced none of them (*not measured*).
