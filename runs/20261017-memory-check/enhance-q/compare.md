# Six experts — what should memory-check v1 improve next?

Question: `runs/20261017-memory-check/enhance-question.md`. All six answered; all six usable. This file compares;
it does not pick a winner or decide. The main agent decides; EJ accepts or declines.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | Real-repo canary first; explicit "no project-memory/" output; hook only as an approved, reversible diff (*quoted*, his top three) | Real-repo calibration; package the hook diff for EJ; shallow-clone "could not run" (*quoted*, his top three) | One whole valid memory checked by hand (fixture if no real project); record the hook yes; name the working-tree/staged disagreement (*quoted*) | Mend `--warn` for "could not run" first; then the hook; say each absence once; then a real project (*quoted*) | Make the warning speak when a check did not finish (tool and hook command); then the hook yes; tell EJ the agent-memory folder mismatch (*quoted*) | `--warn` reports "could not run"; one real-project run; then the hook (*quoted*, his answer line; his ranked list puts the hook first by value) |
| Main items used | #13, #2, #18, #5, #7, #16, #4, #17, #11, #19 | #18, #4, #5, #3, #10, #14, #7 | #1, #4, #2, #3, #19, #6, #14, #8, #5 | #6, #2, #3, #18, #19, #1, #15, #8, #4, #10, #14, #7 | #1, #5, #3, #10, #8, #4, #6, #7, #9 | — |
| Insights cited | — | — | — | — | `runs/20261016-six-experts/insight.md#F-7f938bdf`, `runs/20261017-agent-lessons/insight.md#F-0969936e`, `runs/20261016-four-experts-what-counts-as-change/insight.md#F-d3132a7f`, `runs/20261016-time-monitor/insight.md#F-173e0190` | — |

## Where they agree

- **The hook needs EJ's yes and nothing else is blocking it as a diff.** All six. Linus: "prepare the session-start hook only as an owner-approved reversible change"; 范蠡: "package the session-start hook settings diff for EJ's approval"; 孫子: "Record the yes to the session-hook diff already written"; 老子: "blocked on one word, not on work"; Dave: "ask for EJ's yes to the hook, because that is U3's only unmet acceptance"; Dario: "Install the session-start hook (U3)". (*quoted*)
- **The tool has never met a real `project-memory/`, and that matters.** All six name it. Linus and 范蠡 rank a real-repo run first; 孫子 ranks a whole valid memory first (real or fixture); 老子 puts it fourth and conditional; Dario third; Dave would stop check-logic work until one exists rather than build a stand-in. (*quoted* positions; ranking is *my reading* of each list)
- **No module to remove.** Linus: "Remove or simplify no modules yet"; Dave: "Nothing in the code to remove"; Dario: "Nothing to remove. Every module serves U1–U6"; 孫子 proposes no code removal beyond two static report lines; 老子 refuses to add, removes nothing from code. 范蠡 alone proposes a code simplification (`checkRd1`, below). (*quoted*)
- **No new checks.** 孫子: "No new checks"; 老子: "no new requirement"; Dave: "Stop check-logic work until real memory exists"; 范蠡: keep CACHES v1 to B2.2. (*quoted*)
- **Collapse the repeated "not applicable" rows** — 孫子 (#4), 老子 (#3), Dave (7a), Dario (simplify). Each keeps every id listed; 老子 and 孫子 each add a test that every id still appears exactly once. Linus and 范蠡 do not raise it. (*quoted* / *my reading* of who omits it)
- **The hook will print a line in every git project without `AGENTS.md`.** 孫子, 老子, Dave and Dario each name this cost; Dave counts 3 of 6 repos under `~/dev`. (*quoted*; Dave's count *not measured* by me)

## Where they disagree (side by side, quoted; never averaged)

**1. What comes first.**

| Expert | First item (*quoted*) |
|---|---|
| Linus | "Validate on one real repository with `project-memory/`." |
| 范蠡 | "Calibrate and verify `memory-check` on a real repository containing active `project-memory/`." |
| 孫子 | "Put one whole valid memory through the tool and check every verdict by hand; a fixture will do until a real project is named." |
| 老子 | "Fix that first" — the `--warn` hole for a MUST that could not run. |
| Dave | "Make the warning speak when a check did not finish." |
| Dario | Answer line: "Make `--warn` report a MUST that could not run, run the tool once on a real project, then install the session-start hook"; top three line 1: "Install the session-start hook (U3) … after improvement 2 is done." |

*My reading:* three put calibration first (Linus, 范蠡, 孫子), three put the could-not-run warning first or before the
hook (老子, Dave, Dario). Dario's top-three list is ordered by value, his answer line by sequence; they are not the same order.

**2. The `--warn` silence on "could not run".** 老子, Dave and Dario name it (`warn.ts:46` filters `verdict === "fail"`
only). *My check:* `memory_check/src/warn.ts:46` reads `.filter((result) => result.id !== "F1" && result.level === "MUST" && result.verdict === "fail")` — confirmed in the file; the predicted empty output is *not measured* (nobody ran it).
Linus, 范蠡 and 孫子 do not raise it. Linus raises a nearby but different silence: "emit a deterministic result such as
`skipped: no project-memory/`" for an absent target. (*quoted*)

**3. Whether the hook command itself must change.** Dave: "if the tool exits non-zero with no output, print one line
such as 'memory-check did not finish'" and an inner time limit. 老子: the `2>/dev/null || true` "swallows exit 2 as well
as 1 … that promise and R2's 'nothing else' are in tension, and the owner should settle which wins." 孫子: "`|| true`
makes a timeout look like 'nothing to warn'" (a cost, no change proposed). Dario: "the command needs a wrapper that
always exits 0" (*recall* about SessionStart exit codes). 范蠡 and Linus: no change to the command. (*quoted*)
*My reading:* Dave and Dario pull in opposite directions on exit status — Dave wants the failure made visible, Dario
wants it always exit 0 so stdout is injected; both could hold together, but neither says so.

**4. If no real project exists.**

| Expert | Position (*quoted*) |
|---|---|
| Linus | Conditional on a use case requiring it: "If none does, this improvement is ineligible." |
| 范蠡 | "we must conditionally synthesize a multi-branch Git fixture containing real merges and historical edits to simulate terrain." |
| 孫子 | "a fixture is the fallback, not the goal"; "the calibration proves consistency, not correctness." |
| 老子 | "if no project is named, skip it rather than widen the fixtures (a fixture written to match the tool is not evidence)"; "v1 is finished". |
| Dave | "Do no more check-logic work until a real project has `project-memory/`"; "its first full report is the calibration." |
| Dario | "If there is none … I would delay the hook, since it would have little to warn about beyond a missing `AGENTS.md`." |

**5. Collapse the report now or later.** 老子 and 孫子: now (老子 measured 72 lines, 80.7% of 21,173 bytes, 2 distinct
reasons; target under 9 KB; 孫子 target ≤ 120 lines on a valid-memory report). Dario: "wait for improvement 3". Dave:
"this is EJ's call and ranks low" because the acceptance suite was written by another engine (T1). (*quoted*; figures
*not measured* by me)

**6. Hook scope.** 孫子: "If EJ wants that only in projects that have adopted memory, the hook needs a scope condition
before the yes." Dave: "the same entry can go first into a single project's `.claude/settings.json`." Dario: "Should the
hook be global, like the guard hooks, or per project?" Linus, 范蠡, 老子: global as diffed. (*quoted*)

## What each added that the others did not

- **Linus** — an explicit target-absent result under `--warn` ("skipped: no project-memory/"), distinct from a clean
  check (*quoted*); a pattern change: "make evaluation briefs source-complete and outcome-based" (*quoted*). He states
  "`USE_CASES.md` and `VISION.md` were not supplied, every use-case mapping below is conditional" (*quoted*). *My check:*
  his pasted brief (`linus/briefs/linus.pasted.md`, 659 lines) holds no U3 text — the mcode fallback had no file reads,
  so his use-case mapping is conditional by construction, not by choice.
- **范蠡** — shallow-clone detection (rank 3) and usage error exit 2 for missing / non-git paths (rank 4) (*quoted*).
  *My check:* both are already built and tested — `memory_check/test/acceptance.test.ts:108-110` ("C5/R3: shallow
  history could not run exits 1") and `:45` (missing / subdirectory / notgit → status 2). So these two items describe
  done work (*my reading*). Also: a hook latency bound "median execution time stays strictly under 100ms" (*quoted* —
  a threshold he set himself, not given by EJ); simplify `checkRd1` prose parsing into "needs a reviewer" (*quoted*);
  a pattern change: authority questions go to EJ without three automated trials (*quoted*).
- **孫子** — the working-tree vs staged-state disagreement (presence from `git ls-files --cached`, `checks.ts:99-100`;
  F1 from `existsSync`, `locations.ts:74-77`) with a probe: an unstaged valid entry gives F1 "present", every SoT record
  "not applicable", exit 0, empty `--warn` (*quoted*; probe *not measured* by me); a byte-for-byte test pinning the
  bundled guidelines to `docs/memory-system/` (*quoted*); remove the two static status lines at `report.ts:75-76`
  (*quoted*); his probe counts on the one-entry fixture: 9 pass, 44 needs a reviewer, 22 not applicable (*quoted*).
- **老子** — the counts line: "3 + 3 + 72 = 78 against 'Records: 64 … 11'" in `smoke-report.md:128` (*quoted*; not
  checked by me); a proposed R2 amendment text: "`fail` **or** `could not run` of a MUST, plus a missing `AGENTS.md`, and
  nothing else" (*quoted*, labelled his reading). His answer file begins with a stray line "I'll read the brief first."
  (*quoted*, engine chatter).
- **Dave** — the agent-memory location mismatch: `SOURCE_OF_TRUTH.md:23–24` names `~/.claude/agent-memory/<name>/`,
  absent here, while `~/.claude/projects/*/memory/MEMORY.md` exists 7 times; the report says agent memory "absent"
  (*quoted*); no `project-memory/INDEX.md` anywhere under `~/dev` (*quoted*; Dario reports the same search); written
  predictions P1–P3 before any run (*quoted*); a pattern change: list the tool's real inputs from file names before
  ranking (*quoted*, n=1); a cost model for K4.3, about N × (3 + 2c) git calls (*quoted*, his reading).
- **Dario** — hook design traps: the tool needs the git root (exit 2 from a subfolder); a non-zero SessionStart exit may
  drop stdout (*recall*); setting `BUN_RUNTIME_TRANSPILER_CACHE_PATH=0` in the hook skips the second bun process
  (*quoted*); keep `--since` but do not extend it, "it produced review finding 6" (*quoted*); a count that 9 of the 14
  review findings made a real break read as a pass (*quoted*, his reading).

## What they need to know (the questions, merged, for EJ)

1. **Is there a real project with `project-memory/` the tool may run on — and may its contents be read in this session?**
   (Linus, 范蠡, 孫子, 老子, Dave, Dario.) Options: (a) yes, EJ names it — calibration becomes one run there;
   (b) none — build a multi-entry fixture as a stand-in (范蠡, 孫子); (c) none — skip calibration, freeze check logic,
   and treat v1 as finished until one exists (老子, Dave); (d) none — delay the hook too (Dario).
2. **Does a MUST that could not run belong in the session-start warning?** U3's fails-if says the warning holds nothing
   else. (老子, Dave, Dario.) Options: (a) yes — widen U3 / amend R2 to "`fail` or `could not run` of a MUST, plus a
   missing `AGENTS.md`"; (b) no — the silent case stays, and the owner knows it is there.
3. **What does the hook do when the tool itself fails (crash, usage error, timeout)?** (老子, Dave, Dario.) Options:
   (a) stay silent, as the diff's `2>/dev/null || true` does now; (b) print one "memory-check did not finish" line under
   an inner time limit (Dave; the limit's value is EJ's or the main agent's); (c) always exit 0 through a wrapper so
   stdout is shown (Dario, resting on *recall*).
4. **Global hook or scoped?** (孫子, Dave, Dario.) Options: (a) global in `~/.claude/settings.json` as diffed — a line in
   every git project without `AGENTS.md`; (b) one project's `.claude/settings.json` first; (c) global with a condition
   so it speaks only where `project-memory/` exists.
5. **Is `~/.claude/projects/<slug>/memory/` agent memory under the guidelines?** (Dave.) Options: (a) yes — F1 lists it,
   with a fixture test; (b) no, outside on purpose — a one-line note; (c) a guideline change, reported not fixed here.
6. **Does "missing" in `VISION.md:11` include memory written but not staged, or staged but deleted?** (孫子.) Options:
   (a) yes — a line in the warning too (changes U3 and R2); (b) no — a note in the report is the whole fix.
7. **Should an absent `project-memory/` print an explicit "skipped" result rather than nothing?** (Linus.) Options:
   (a) yes — distinct output for absent, clean, warnings, failure; (b) no — silence is the contract.

## Check

- `check` result per expert, as given to this step: linus pass, fan-li pass, sun-tzu pass, lao-tzu pass, dave pass,
  dario pass. Each subfolder's `check.txt` prints "FAIL: 1 answers, 5 failure(s)" — the five failures are the other
  experts' answer files, absent from that subfolder; no line names a failure for the folder's own expert (*my reading*
  of the six `check.txt` files).
- Engines (from each `status.json`): Linus — **mcode**, `minimax/MiniMax-M3.1-Flash-Preview`, **fallback from codex**
  ("codex has 19% left (20% or less)"), 72.1 s; 范蠡 — agy, `gemini-3.8-flash-medium`, 220.2 s; 孫子 — dsh,
  `deepseek-flash (dsh headless profile)`, 316.3 s; 老子 — opencode, `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`,
  92.1 s, started 18:41 after the others; Dave — claude, `claude-opus-5-5`, 450.4 s; Dario — claude,
  `claude-sonnet-5-5`, 192.1 s. All exit 0, `ok: true`. (*quoted*)
- Linus and 老子 ran on the same model family (MiniMax M3.1 Flash) through different harnesses; Dave and Dario both on
  Claude. (*my reading* — their agreement is less independent than six engines suggest.)
- The check script was written by Claude. It checks citations and that an answer file exists; it does **not** establish
  that a rule was applied correctly or that the advice is good.
- Two expert claims I checked in the repository: the `warn.ts:46` filter (confirmed) and 范蠡's items 3 and 4 (already
  tested, `acceptance.test.ts:45`, `:108-110`). Everything else — the probes by 孫子, 老子's byte counts, Dave's globs,
  Dario's search — is *not measured* by me. Dave and Dario each say they could not run the tool or `bun test`.
