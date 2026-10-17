# Experts — keep or remove `--mark P` on `deadline wait`

Question: `runs/20261017-workflows/mark-question.md`. Asked in this run: Linus, 孫子 Sun Tzu, Dave and Dario. 范蠡 Fan Li
and 老子 Laozi were not in this run's list. They have no subfolder and no answer, and nothing below speaks for them.
The main agent decides; this file does not.

| | Linus | 孫子 Sun Tzu | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|
| Answer (one line) | Remove, provisionally; restore if a real workflow needs it (*quoted*: "provisionally remove `--mark P`, keeping `deadline wait` for the deadline itself") | Keep; remove only if the owner meant every percentage trigger (*quoted*: "Keep `--mark P` ... on the reason as given, keep it") | Remove, provisionally; becomes keep + a suite test if the report is due before the deadline (*quoted*: "Remove `--mark P` (reading A), provisionally") | Remove, provisionally, and make `--mark` a loud usage error (*quoted*: "Remove `--mark P` (reading A), provisionally") |
| Main items used | #13, #2, #3, #5, #7, #18 (*quoted*) | #1, #17, #6, #5, #10, #8 (*quoted*) | #1, #5, #4, #6 (dropped by #7), #8, #2, #3, #9, #10 (*quoted*) | — |
| Insights cited | — | — | `runs/20261016-time-monitor/insight.md#F-a03fa5b3`, `#F-173e0190` (*quoted*) | — |

## Where they agree

- **No run has used `--mark`.** All four rest on the brief's grep. Dave and Dario widened the search and found
  nothing more. Dave: "No run has ever used it as its timer" (*quoted*); Dario: "*measured*, but only for this
  repository" (*quoted*).
- **The decision is provisional and the evidence is thin.** Linus: "Removal is justified provisionally"; Sun Tzu:
  "The evidence is thin in both directions"; Dave: "How sure I am: low either way"; Dario: "This is provisional" (all
  *quoted*).
- **Each names what would change its answer, and for all four that is a real need for an early wake.** Linus: "A
  demonstrated workflow that removal prevents would be evidence to reverse my recommendation"; Sun Tzu: "wrong if two
  consecutive time-boxed runs need no pre-deadline timer at all"; Dave: an idle agent "woken only at time-up, and the
  owner calls the late report a problem"; Dario: "If agents repeatedly work out seconds by hand, or a report is lost to
  an idle wait, that argues for putting `--mark` back" (all *quoted*).
- **No suite test passes `--mark`.** Sun Tzu, Dave and Dario say so; Dave and Dario name the only `deadline wait` test,
  `round10-deadline.test.ts:190`, which runs with no flag (*quoted*). Linus does not address tests (*my reading*).
- **An early wake only helps an agent that makes no calls.** Sun Tzu: "a long call leaves the agent blind until it
  ends"; Dave: "A timer only helps an agent that is idle"; Dario, labelled recall: "useful when the agent is idle
  waiting on workers" (all *quoted*). Linus does not raise it (*my reading*).
- **Three of four advise removal and one advises keeping** (*my reading*). Vote counts settle nothing: all four
  answered the same brief.

## Where they disagree   (side by side, quoted; never averaged)

**Does the owner's reason ("not able to well predict, specific when exploring solutions") cover a percent the agent
picks?**

| Linus | Sun Tzu | Dave | Dario |
|---|---|---|---|
| "removing reminders alone does not establish that this timer violates EJ's decision" | "The defect is the **fixed** percentage, not the percentage. A number the agent chooses at the moment it starts the wait is the agent's own prediction" | "`--mark P` is also a fixed percent, chosen in advance. The agent chooses it, rather than the guard firing it ... But the number has the same weakness." | "this objection is about picking a percent of the deadline, not about who picks it. EJ did not say that, so it is *my reading*." |

**Is `--mark` a leftover of the removed marks?**

| Linus | Sun Tzu | Dave | Dario |
|---|---|---|---|
| not addressed (*my reading*) | "The `wait` branch ... never reads the marks field"; commit `07b67a9` left `wait [--mark P]` in place, so "it is not code the removal forgot to sweep" | "added in the same build as `--marks 50,80,100`" but "the code never read the deadline's list of marks", so "it did not *only* serve them" | `method.md` line 551, edited after the decision, says "a timer that returns at the deadline"; "Removing the flag makes everything match the newer text" |

**Is a plain `sleep` an adequate substitute?**

| Linus | Sun Tzu | Dave | Dario |
|---|---|---|---|
| refers to "the accepted clock behavior and existing timer approach" without judging it (*my reading*) | "it moves it to a plain `sleep` interval the agent computes, where the guard cannot see it and no status line is printed" | "a `sleep` whose length the agent works out by hand, which is the kind of failure `F-a03fa5b3` recorded" | "the plain `sleep` the time-monitor run used already does that" |

**Which choice is easier to reverse?**

| Linus | Sun Tzu | Dave | Dario |
|---|---|---|---|
| "Restoration takes work" | "Keeping can be removed later on evidence; removing cannot be tested" | "Neither choice is hard to undo" | "reversibility doesn't decide" |

**What the zero grep shows**

| Linus | Sun Tzu | Dave | Dario |
|---|---|---|---|
| "It does not establish absence of callers elsewhere" | "the measured zero ... measures the **whole timer path**, not the flag. It cannot decide between A and B." | "No uses is still a result ... confirms the removal" (for the next run) | the decision "rests on zero uses in one repository" |

## What each added that the others did not

- **Linus:** checked keeping the flag against requirement-check: it passes six of the eight and fails "can it
  fail" (no acceptance criterion) and "basis" (no demonstrated benefit) (*quoted*, summarised). He also asks for a
  search for callers outside the run files (Dario asks the same).
- **Sun Tzu:**
  - The time-monitor run set its timer for 11:17 against an 11:22 deadline, "B's use case, done without the flag"
    (*quoted*).
  - A proposed change to the pattern: set the timer at the start with `deadline wait --mark` and record it in the
    state's start line (*quoted*, summarised).
  - The wording conflict, "T5 says 'no marks' while T3 documents `wait [--mark P]`" (*quoted*).
  - The unit mismatch: the recorded intent was minutes ("five minutes before"), and the flag takes a percent
    (*quoted*, summarised).
  - A two-minute-deadline `--mark 50` test (*quoted*, summarised).
  - Two questions no one else asked: does `deadline wait` itself stay, and does a timer's output reach an agent that
    makes no call?
- **Dave:**
  - `--mark` has run once, in the time-monitor reviewer's own check (`review.log:4432–4444`): "it works. But the
    reviewer wrote that check, it is n=1" (*quoted*).
  - The accepted time-up line (`SPEC.md:559–560`) and the method's "leaves time for the report"
    (`WORKFLOW_DESIGN_METHOD.md:543`) "read differently" (*quoted*).
  - A replacement option: a wake a set number of minutes before the deadline, with the number chosen by the owner
    (*quoted*, summarised).
  - The exported `skills/workflow-design/` is "a directory, not a link", so removal touches a second copy
    (*quoted*).
  - The only expert who cited insights; `F-a03fa5b3` is what made his answer conditional (*quoted*, summarised).
- **Dario:**
  - Removal "must make `--mark` a loud usage error, or it breaks the 'fail loud' rule", because `flagValue`
    (`cli.ts:70-76`) ignores flags it was not asked for (*quoted*). Dave notes the same silent fall-through but makes
    the rejection optional ("would close it, at the price of one line and one test", *quoted*).
  - The time-monitor review (`review.result.md` item 10) already asked for an explicit `--mark` test, and none
    exists (*quoted*, summarised).
  - "Keeping leaves a trap": a later reader "may take it as a sanctioned reminder and rebuild what the owner
    declined" (*quoted*).

## What they need to know   (merged, each with its options)

1. **Did the owner's decision cover every percentage trigger, including one the agent starts itself, or only the
   automatic reminders?** Sun Tzu asks it; Dave and Dario answer it each in their own reading.
   - Only the automatic reminders: keep `--mark` (Sun Tzu).
   - Every percentage trigger: remove it (Sun Tzu's condition; Dario's reading).
2. **Is the report due before the deadline or after the time-up line?** Dave asks it; Dario asks the same thing as
   "Does EJ want agents to schedule their own wake-ups before the deadline?"
   - After, as the accepted time-up line says: remove `--mark`.
   - Before: keep `--mark` and add a suite test.
   - Before: replace it with a wake a set number of minutes before the deadline, with the number chosen by the owner
     (Dave).
   - Before: remove it and document the `sleep` recipe (Dario).
3. **If it is removed, should `deadline wait --mark N` fail loudly or be ignored silently?** Dario says it must
   fail; Dave says rejecting it is optional.
   - Make it a usage error (exit 2), with one test.
   - Leave it ignored: it then waits to 100% without complaint.
4. **Does anything outside the searched run files call `deadline wait --mark`?** Linus and Dario ask it.
   - Yes: keep that workflow working, or give it a replacement, before removal.
   - No: removal goes ahead.
5. **Does a background timer's output reach the agent when it fires, without the agent making a call?** Sun Tzu
   asks it.
   - Yes: an early wake has value.
   - No: an early wake buys nothing until the next call, and the case for keeping weakens.
6. **Is `deadline wait` itself staying?** Sun Tzu asks it.
   - It stays: this decision stands alone.
   - It is retired in favour of plain `sleep`: `--mark` goes with the branch, which is a larger decision than this
     one.
7. **How often does an agent sit idle past the point where its report needed to start?** Dave, Dario and Linus all
   ask a form of it; none of them measured it.
   - Measure it over the next time-boxed runs (each expert proposes a version of this).
   - Treat zero records found so far as enough.

## Check

- **Check results (as given by the caller):** linus pass, sun-tzu pass, dave pass, dario pass; all four answers
  usable (*quoted* from the task).
- **Engines (from each `status.json`, *quoted*):**
  - linus: codex `gpt-6.1-sol`, exit 0, 40.3 s.
  - sun-tzu: dsh `deepseek-flash (dsh headless profile)`, exit 0, 218.4 s.
  - dave: claude `claude-opus-5-5`, exit 0, 200.1 s.
  - dario: claude `claude-sonnet-5-5`, exit 0, 107.1 s.
  - Every `problem` field is empty, so no fallback is recorded.
- **Not asked:** Fan Li and Laozi were not in this run's list. They have no folder, status or answer.
- **What the check does not establish:** the check script was written by Claude. It does not establish that any
  expert applied its rules correctly, or that its readings of the code are right (*my reading*).
- **Not verified by me:**
  - The experts' file and line citations, such as `cli.ts:70-76`, `cli.ts:221-227`, `SPEC.md:559–560`,
    `method.md` line 551, `review.log:4432–4444` and commit `07b67a9` (*not measured*).
  - Where two experts give the same citation (Dave and Dario on `cli.ts:70-76` and `round10-deadline.test.ts:190`),
    they still read the same files on one brief, so the agreement is not independent (*my reading*).
