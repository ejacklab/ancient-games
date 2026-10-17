# Six experts — where does memory-check belong in the workflow-design method?

Question: `runs/20261017-memory-check/placement-question.md`. All six answers usable. This file compares; it decides
nothing. Each line is labelled *quoted* (from an answer or a cited file), *my reading*, or *not measured*.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | 3.1, once before the run; fail stops the run for EJ's repair or waiver | 3.1, once before the run; fail stops only if the run depends on memory | 3.1, once; fail never stops the run, only the dependent pieces wait; the node that commits memory reruns it | 3.1, once; fail stops only if the task reads that memory; drop the 3.1 line if the hook is installed | 3.1 baseline, plus `--warn` at the stop of a node that writes `project-memory/`, trial first | 3.1, plus once at the end of a run if a node wrote memory; fail is a decision spot, run carries on |
| Main items used | #13, #5, #4, #7, #2, #3 | #18, #10, #3, #13, #14 | #1, #2, #4, #5, #6, #8, #12, #13, #15, #17 | #1, #6, #3, #17, #2, #8, #14, #19, #4 | #1, #5, #4, #6, #7, #8, #2, #10, #3, #9 | — |
| Insights cited | — | — | — | — | `runs/20261016-integrate-r11-r13/insight.md#F-8392b4ce`, `runs/20261015-long-session/insight.md#F-f09b058d`, `runs/20261015-long-session/insight.md#F-8712e9fc` | — |

(The one-line answers are *my reading*, condensed from each answer's "Answer" and "Recommendation".)

## Where they agree

- **Step 3.1 Readiness, before the run, beside `readiness.py` / `harness_health.py` / `doctor`; no new numbered
  step.** All six. *Quoted:* Linus "add no numbered step"; 范蠡 "never per node or as a new method step"; 孫子 "One
  line made checkable, not a new step"; 老子 "not a new step"; Dave "This adds no step"; Dario "Don't add a per-node
  step."
- **Not on every node.** All six. *Quoted:* 老子 "Per node multiplies one read-only check by the node count"; Dave "A
  node that writes no memory cannot break memory". (Three of them make an exception for a node that writes memory —
  see disagreement 2.)
- **pass and not applicable: carry on.** All six. No `project-memory/` is not a reason to create one: 孫子 "is not a
  failure (C4) and is not a reason to create it"; Dave "Do not add a piece to create `project-memory/`"; Dario "It
  must not trigger the 3.1 'Missing → research piece' row"; 老子 "Absence is information, not a failure"; 范蠡 "must
  not halt or force memory creation" (*quoted*).
- **The method must not rest on the session-start hook; the hook is EJ's separate yes.** Linus, 孫子, Dave, Dario
  (*quoted*: Dave "the method never relies on it"; Dario "the method can't depend on it"). 老子 agrees the hook waits
  for EJ's yes but draws a different conclusion (disagreement 5). 范蠡 does not address the hook (*my reading*).
- **The tool must not write or fix memory, and must not judge the "needs a reviewer" items.** 范蠡, 孫子, 老子, Dave,
  Dario (*quoted*: 孫子 "The tool must not judge the 'needs a reviewer' items"; Dario "No agent edits memory to make
  it pass"). Linus says the same in substance: a pass "proves guideline compliance, not that memory is complete,
  current, or correctly interpreted" (*quoted*).
- **What becomes redundant: nothing fully; 3.1's row "There, but not verified | Add a small piece that checks it" is
  what the tool now does for memory structure.** 孫子, 老子, Dave, Dario cite that row (line 125, *quoted*); 范蠡 says
  "Automated verification replaces manual structure verification in step 3.1" (*quoted*); Linus says "Nothing
  currently named in the method becomes redundant" (*quoted*).
- **§4's per-node memory duties stay.** Linus, 孫子, 老子, Dave, Dario (*quoted*: 孫子 "the tool checks the
  repository's memory, not which entries a node reads or writes").
- **On this repo the result is near-empty and must stay quiet.** All six cite or reflect the smoke report's counts —
  "0 fail, 3 pass, 3 needs a reviewer, 72 not applicable, 0 could not run" (*quoted*,
  `nodes/smoke-report.md` line 128).
- **The test is a planted break on a fixture project with `project-memory/`.** Linus, 孫子, 老子, Dave, Dario
  (*my reading* of their "How we would know" sections); 范蠡 names outcomes over future runs instead.

## Where they disagree   (side by side, quoted; never averaged)

**1. A failing MUST before the run — what stops?**

| Position | Who | Their words (*quoted*) |
|---|---|---|
| Stop the whole run; EJ repairs or waives | Linus | "fail: stop the run and ask EJ to repair it or explicitly waive the failing MUSTs." |
| Stop the run only when the run's nodes use that memory; otherwise a note | 范蠡 | "if `fail`, stop and ask EJ only if the run depends on project memory, otherwise carry on with a note." |
| | 老子 | "stop and ask EJ … the stop is for a failing MUST whose memory the task's nodes receive through Context … a break nobody reads is a note." |
| Never stop the run; a decision spot for EJ (3.3), only the pieces that rely on that memory wait | 孫子 | "a decision spot in the 3.3 batch; provisional: carry on … and hold only the pieces that read or write that memory" |
| | Dave | "Report it; do not fix it … A node that reads the failing memory becomes an unclear spot (3.3) … Every other piece carries on" |
| | Dario | "it becomes an unclear spot of kind decision, in the one batch to EJ. The provisional assumption is to carry on with pieces that don't touch the failing entries." |

*My reading:* 范蠡/老子 and 孫子/Dave/Dario use the same test (does a node read the broken memory?) but differ on the
unit held — the run versus the dependent piece. Linus holds the run unconditionally.

**2. Is there a second moment after 3.1?**

| Position | Who | Their words (*quoted*) |
|---|---|---|
| 3.1 only | 范蠡 | "never per node" (no end-of-run run proposed — *my reading*) |
| | 老子 | "not at the end of the run … §4's per-node rule already says what an end-of-run check would say" |
| 3.1 only, unless the workflow changed memory | Linus | "Do not run it per node or at the end unless the workflow intentionally changed project memory." |
| Also at the node that commits / writes memory, inside that node's existing check | 孫子 | "only the node that commits memory runs it again, as its check" |
| | Dave | "only at the stop of a node that writes to `project-memory/`, run `--warn` again and compare it with that baseline … A MUST that newly fails there counts as a failed attempt." Trial on one product first; "drop it if it catches nothing." |
| Also once at the end of the run, if a node wrote memory | Dario | "Run it a second time at the end of a run (step 3.6 / skill step 8), and only if a node wrote memory entries." |

*Not measured:* none of the second-moment positions has run on real memory (Dave: "n=0").

**3. "needs a reviewer"**

| Position | Who | Their words (*quoted*) |
|---|---|---|
| Carry on with a note; never a gate | 范蠡 | "carry on with a note in `state.md`" |
| | 老子 | "carry on with a note … it must not be promoted into a gate" |
| | Dave | "Listed once for EJ in the readiness file. It never stops the run and is not asked again each run." |
| | Dario | "Carry on and list it in `state.md` and the final report. It is never counted as a pass." |
| Note by default; pause if EJ makes review blocking | Linus | "carry on with a visible 'unreviewed' note and reviewer task; if review is defined as blocking, pause instead." |
| The dependent piece waits for the reviewer | 孫子 | "a reviewer item a piece depends on holds that piece until the owner, or the person they name, judges it" |

**4. "could not run"**

| Position | Who | Their words (*quoted*) |
|---|---|---|
| Unknown; carry on with a note | 范蠡, 孫子, 老子, Dave, Dario | 孫子 "record 'unknown' with the reason … no stop"; Dave "Marked unknown … Carry on and say so." |
| Pause unless EJ accepts the gap | Linus | "continue only if EJ accepts the missing check as an exception; otherwise pause." |

**5. If EJ installs the session-start hook, does the 3.1 line stay?**

| Position | Who | Their words (*quoted*) |
|---|---|---|
| Drop the 3.1 line | 老子 | "If the hook is installed, 3.1's line duplicates it and my #1 says remove the line rather than keep both." |
| Keep the 3.1 line; the hook is extra | Linus | "it is an optional duplicate, not a substitute for canonical 3.1 readiness" |
| | 孫子 | "the method's placement stays 3.1, and the hook is how sessions outside a designed run get the same warning" |
| | Dave | "a session-start warning can be a day old when a run starts, so it cannot stand in for 3.1"; the hook is in `~/.claude/settings.json` only, while nodes may run on other engines |
| | Dario | "a hook warning is a reminder" (§4 lines 594–595) |

**6. What 3.1 runs and records**

| Position | Who | Their words (*quoted*) |
|---|---|---|
| `--warn`; the full report only when the warning is not empty | 老子 | "So 3.1 gets `--warn`, and the report only when the warning is not empty." |
| `--warn` | Linus | "Put `memory-check --warn` inside existing step 3.1" |
| The full report; the counts line and reviewer ids in readiness; read the states, never the exit code | 孫子 | "the **report** is the result, not the exit code … The readiness line must carry the counts and the reviewer ids; 'memory OK' is never written." |
| | Dave | "save the report in `runs/<id>/` as the memory baseline; read the states, never the exit code alone." |
| | Dario | "Write the tool's counts line to `state.md`." "Read the counts line, not the exit code" |
| Not specified | 范蠡 | — |

*My reading:* `--warn` prints only failing MUSTs and a missing `AGENTS.md` (`memory_check/REQUIREMENTS.md` R2,
*quoted*), so a 3.1 that runs `--warn` alone does not see the "needs a reviewer" or "could not run" states that Linus's
own state table acts on.

**7. A factual conflict: what exit code "could not run" gives.**
- Dave: "memory-check exits 1 both when a MUST fails and when a MUST could not run" (*quoted*).
- Dario: "REQUIREMENTS R3 says exit 0 for 'no MUST fails *or could not run*'" and "a script that trusts the exit code
  treats 'could not run' as a pass" (*quoted*).
- I read the code: `memory_check/src/checks.ts` `exitCodeOf` returns 1 when any MUST's verdict is `"fail"` or
  `"could not run"` (*my reading* of the code, read and not run). Dave's statement matches the code; Dario's
  reading of R3 does not. Both still conclude "read the states, not the exit code", so the placement does not change
  (*my reading*).

## What each added that the others did not

- **Linus** — record "the status, timestamp, checked repository revision, and exception decision" in the existing
  readiness progress line (*quoted*); fixtures for all five states, including a simulated could-not-run, because
  "the current repository cannot exercise the useful failure path" (*quoted*).
- **范蠡** — an explicit "strict repository-wide compliance" option, under which a fail stops every run (*quoted*,
  his only question); the risk that carrying on "risks propagating latent memory defects if downstream nodes
  unexpectedly touch unchecked files" (*quoted*).
- **孫子** — the snapshot argument: the tool reads the staged state (C5), so an end-of-run pass "can pass on the
  memory as it was, not as a node wrote it" (*quoted*); outside a git root the tool exits 2, so a plain directory is
  "skipped with a note, not counted as a fail" (*quoted*); `CACHES.md` gives its requirements no level, so a cache
  break never changes the exit code (*quoted*, smoke report line 129); a three-design review on the method's existing
  3.3 schedule, and "If after three designs it caught no break … keep the session-start hook only" (*quoted*).
- **老子** — the 3.1 line belongs in the **Information** bullet, not Tools (*quoted*); the tool checks "its own"
  copies of the guidelines and prints their versions, so the printed version belongs in the state file (*quoted*);
  a proposed change to the method's 3.3 line: a new check first looks for an existing step to absorb it (*quoted*).
  *My reading:* his "3.1's cost guard … no tool calls (`:89-90`)" cites the cost guard of step 3.0 — lines 89–90
  come before the `### 3.1 Readiness` heading.
- **Dave** — the baseline-and-compare design: a new fail is charged to a node only if it is on a file the node lists
  as written, because another session can change the staged state mid-run (*quoted*, insight F-8712e9fc); the
  session as the wrong unit (F-8392b4ce); the 3.6 stop part 2 "the baseline recorded in 3.1 still passes" as the
  existing check to carry it (*quoted*; line 373 checked — *my reading* that it matches); a pre-written trial with
  a null result reported and the part removed (*quoted*).
- **Dario** — a count of the guideline's `check:` lines: "of the 64 records about 33 are reviewer-only, 11 are
  'none', 14 are tool or git alone, and 6 mix tool or git with a reviewer" (*quoted*; *not measured* by me); the
  tension with §4 "a start hook carries only the four session-start reads" (*quoted*); a calibration measure — fails
  EJ confirms versus fails EJ overrules (*quoted*).

## What they need to know   (merged, each with its options)

1. **A failing MUST before a run — what does it hold?** (Linus, 范蠡, 孫子, 老子, Dario)
   - a. Stop the whole run; EJ repairs or waives (Linus).
   - b. Stop the run only if its nodes read that memory; otherwise a note (范蠡, 老子).
   - c. Never stop the run: a decision spot in the 3.3 batch, and only the pieces that read that memory wait (孫子, Dave, Dario).
   - d. Strict compliance: stop every run, whatever it reads (范蠡's named alternative).
2. **Is there a second moment after 3.1?** (Dave, Dario, 孫子)
   - a. 3.1 only (范蠡, 老子; Linus unless memory was changed on purpose).
   - b. Also at the stop of a node that writes or commits `project-memory/`, inside its existing check; Dave: trial on one product first, dropped if it catches nothing (孫子, Dave).
   - c. Also once at the end of the run if any node wrote memory (Dario).
3. **"needs a reviewer" — note or hold?** (Linus, 孫子)
   - a. Note, never a gate (范蠡, 老子, Dave, Dario).
   - b. Note by default; pause if EJ makes review blocking (Linus).
   - c. The piece that depends on that item waits until the owner or a reviewer they name judges it (孫子) — then: who is the reviewer?
4. **"could not run" — carry on or pause?** (Linus)
   - a. Unknown, carry on with a note (范蠡, 孫子, 老子, Dave, Dario).
   - b. Pause unless EJ accepts the gap (Linus).
5. **The session-start hook** (`settings-diff.md`, "Yes recorded: (not yet)").
   - a. Install it, and keep the 3.1 line as well (Linus, 孫子, Dave, Dario).
   - b. Install it, and drop the 3.1 line as a duplicate (老子).
   - c. Do not install it; 3.1 alone.
6. **What 3.1 runs and saves.**
   - a. `--warn` only; the full report only when the warning is not empty (老子; Linus names `--warn`).
   - b. The full report saved in `runs/<id>/`, the counts line and reviewer ids in readiness, states read rather than the exit code (孫子, Dave, Dario).
7. **Which of EJ's projects has `project-memory/` now, or will first?** (孫子, 老子, Dave, Dario)
   - a. None yet: write only the 3.1 line now; the rest waits (Dave).
   - b. A named project: run the planted-break test or the trial there before the method changes (老子, Dave).
   (*Not measured* beyond this repo: Dave's Glob over `~/dev` found no `project-memory/INDEX.md`; listing other projects was refused.)
8. **If 2b or 2c: do nodes stage or commit the entries they write before the check?** (孫子, Dario) The tool reads the staged state (C5).
   - a. Yes: the writing node's check is cheap and sees what it wrote.
   - b. No: a later check reads the old snapshot and must not run.
9. **If 2b: how is the trial judged?** (Dave) — a. a date; b. a set of runs. Fixed in writing before the trial.

Answered by the spec, not asked: 老子's "are the tool's guideline copies its own?" — `memory_check/REQUIREMENTS.md` C1
says "Which copy of the guidelines: the tool's own, with its version printed", and the smoke report prints them
(`SOURCE_OF_TRUTH_REQUIREMENTS.yaml 26226965112c, CACHES.md 8eef3b46f3f2`) (*quoted*).

## Check

- Each expert's `check.txt` (*quoted*): every subfolder's check prints `FAIL: 1 answers, 5 failure(s)`, and the five
  failures are the *other* five experts' "no answer file" — each subfolder holds one answer by design. No subfolder
  has a FAIL line for its own expert. The progress log records each as passing: e.g. "check-dario · done · dario
  answer passes check; other experts absent by design" (*quoted*, `nodes/placement-q.progress.md`).
- The check script was written by Claude. I did not read what it tests beyond its output above; it does not
  establish that an expert applied its rules correctly, nor that a cited line says what the expert says it does
  (*my reading*). Two cited lines I read myself: 老子's lines 89–90 belong to step 3.0's cost guard, not 3.1; Dario's
  reading of R3 conflicts with the code (disagreement 7).
- Engines, from each `status.json` (*quoted*):

| Expert | Engine | Model | Seconds | Exit | Fallback |
|---|---|---|---|---|---|
| Linus | mcode | minimax/MiniMax-M3.1-Flash-Preview | 48.1 | 0 | from codex: "codex has 19% left (20% or less)" |
| 范蠡 | agy | gemini-3.8-flash-medium | 100.1 | 0 | none |
| 孫子 | dsh | deepseek-flash (dsh headless profile) | 206.1 | 0 | none |
| 老子 | opencode | minimax-coding-plan/MiniMax-M3.1-Flash-Preview | 140.0 | 0 | none (started 18:51:55, after the others finished) |
| Dave | claude | claude-opus-5-5 | 296.1 | 0 | none |
| Dario | claude | claude-sonnet-5-5 | 124.1 | 0 | none |

- Linus and 老子 ran on the same model family (MiniMax-M3.1-Flash-Preview) through different engines, so their
  answers are less independent than six engines suggest (*my reading*). 老子's answer file begins with an engine
  line, "I'll read the brief first." (*quoted*).
- Dave reports he could not rerun `bun test` ("My own `bun test` was refused permission"); Dario did not rerun it
  either. "70 tests pass" rests on the brief (*quoted*; *not measured* here).
