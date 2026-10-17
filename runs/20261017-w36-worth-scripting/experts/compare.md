# Six experts — May a procedure a script could do stay a page because it runs rarely, and who decides?

Question: `runs/20261017-w36-worth-scripting/research/experts.question.md`. Answers: `experts/<id>/answers/<id>.md`.
All six answers are usable. No one is listed as missing. Written by the compare step (Claude). It picks no winner and
decides nothing; the main agent decides.

Labels: *quoted* (an answer's own words), *my reading* (this step's summary), *not measured*.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line, *my reading*) | Yes, when build + check + keep cost exceeds the effort and error saved over expected use; writer decides **before building**, records it in `state.md`; owner if contested | Yes, **only until it is used again**, and only as a page of exact commands with expected results; the **next follower** decides on that run; owner if contested | Yes, when the whole-form comparison over expected runs favours the page; writer decides the clear case; owner decides **close, missing-facts or contested** cases; comparison **on the page** | Yes, when `state.md` names both sides of the comparison, no number for either; agent writes it; **owner decides what the saving is worth**, and contested cases | Yes, after trying the script, with the comparison **on the page**; writer decides at writing; **next follower re-decides**, trying the script first; owner if contested | Yes, on a written comparison, not rarity; writer decides at writing **and again each time the page is followed**; owner if contested |
| Main items used | #13, #18, #3, #7, #4, #6, #14, #5, #11 | #1, #3, #7, #4, #18, #14 | #1, #5, #6, #2, #4, #10, #8, #14, #11, #17, #13, #16, #15 | #2, #6, #7, #13, #17, #9, #18, #1, #8, #4, #14, #3 | #1, #5, #4, #2, #3, #8, #6, #7, #9, #10 | — |
| Insights cited | — | — | — | — | `runs/20261016-integrate-r11-r13/insight.md#F-2cdebf3b` (+ `#F-b7c8635f`); `runs/20261016-four-experts-what-counts-as-change/insight.md#F-8243a18f, F-96578c5b` | — |

## Where they agree

- **Rarity alone is not the reason; the test is a comparison** (all six). *Quoted*: Linus "rarity alone does not
  establish that"; 范蠡 "Being run rarely is not a reason on its own"; 孫子 "not because it runs rarely"; 老子 "rarity
  alone never decides either side"; Dave "running rarely is not the test"; Dario "'it runs rarely' by itself is not
  that reason".
- **No number** (all six). Each cites research A9 (no measured break-even) or the owner's "comparisons, not numbers"
  rule (*my reading*). 孫子 allows a break-even run count only as "an output of the terms, never an input threshold"
  (*quoted*).
- **Both sides of the comparison carry keep and error cost, not build cost against zero** (all six, *my reading*):
  a rarely-run script rots (B10, B11) and a rarely-run page drifts and its follower is out of practice (C16, C18,
  C19). Every answer cites that pair.
- **The project owner decides a contested case** (all six, *quoted* in each answer's text or proposed W3.6 sentence).
- **The agent, not the owner, makes the routine call** (all six, *my reading*), with the differences on *when* and
  *what else goes to the owner* listed below.
- **Choosing "script" does not end the cost; an unexercised script fails when needed** (孫子, 老子, Dave, Dario, 范蠡
  as a risk; Linus as "rarely exercised scripts can become fragile") (*my reading*). Only 孫子 and 老子 put the
  exercise schedule *inside* the comparison; the others flag it as outside the question.
- **The reviewer can check that a comparison is written, not that it is right** (Linus, 孫子, 老子, Dave, Dario, 范蠡)
  (*my reading*; e.g. Dave *quoted*: "The reviewer can check that the reason is a comparison, not that it is right").

## Where they disagree (side by side, quoted; never averaged)

### 1. When the decision is made

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| "the agent writing the procedure decides before building the script" | "The next agent who follows that page decides, during that run"; the writer "decides only 'page for now'. That needs no comparison" | "at the moment of writing, or at the first revision of a page that predates the rule" | "The agent writing the procedure writes that comparison and the page" (at writing; "the `state.md` line must carry a date to be re-read") | "The agent decides at the time of writing. Whoever follows the page next makes the comparison again" | "when it writes the page and again each time it follows the page" |

### 2. Does the writer try the script first (W3.6's current text) for this exception?

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| No: "records the comparison … rather than first trying the script" | Not at writing; the repeat-run agent "scripts it on that run, or writes … why" | Yes, as a probe: "the try is a probe that stops when the build is priced" | Not stated (*my reading*) | Yes: "after trying the script … the try shows this" | Yes: "by W3.6, has already tried the script first" |

### 3. What goes to the owner besides a contest

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| Only contests: "the project owner decides if contested" | Contests, and "any value no run can show, such as 'this must work the first time it is needed'" | "where the comparison is close, or its facts are missing, the project owner decides"; meanwhile the page stays provisional — "a real shift from W3.6's current script default; say it" | "the project owner decides what the saving is worth, and decides it wherever it is contested" | Contests; plus irreversible procedures (a question): "a page instead of a script for one of those goes to the owner before it stays" | Only contests: "the owner decides if it is contested" |

### 4. Where the written reason lives

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| "in the task's `state.md` (or the commit message when there is no task)" | "in the task's `state.md`" | "The comparison and the facts behind it are written on the page", with "a one-line skip record in `state.md` pointing to it" | "the task's `state.md` names both sides" | "writes on the page why" — "a *proposed change* to where this one SHOULD's reason lives" | Left out of the sentence: "I would put one line on the page, but that conflicts with the levels text, so EJ should say" |

### 5. `fails_if`

| Linus | 范蠡 | 孫子 | 老子 | Dave | Dario |
|---|---|---|---|---|---|
| No change: "a scriptable page with no written exception reason fails the existing SHOULD rule" | "a page for a procedure a script could do is followed again with neither a script nor that written comparison" | "must tell the two page kinds apart — a page kept because a step cannot be scripted names that step; a page kept because the script costs more names the comparison and its terms" | "…or a procedure page names no step a script cannot do and no `state.md` comparison naming both sides, with no written reason" | "'with no written reason' becomes 'with no written comparison'" | No change proposed; the reviewer "can fail a reason that says only 'rare'" |

### 6. What the page must be

- 范蠡 alone requires a form: "only if the page gives each step as an exact command with the result to expect"
  (*quoted*); "A prose page has no preparations to examine".
- 老子: the page "must still name what it is for and what the script could not hold, or it is only a summary"
  (*quoted*).
- 孫子: middle forms (exact commands, partial script, do-nothing script) "are ways of building it, not a third choice"
  (*quoted*). Linus: compare "the smallest useful script, including partial automation" with the page (*quoted*).
- Dave and Dario set no form; Dario notes the clause "does not name" the middle forms (*quoted*).

### 7. Emergency, first-time-must-work, or irreversible procedures

- 老子: "Conditional: emergency-only ⇒ exercise, do not merely script" — keep the page and exercise it, or script
  and exercise on a schedule (*quoted*).
- 范蠡: for such procedures "'may wait until it comes round again' is wrong"; script on a schedule or drilled page —
  "Which one is the owner's call" (*quoted*).
- Dave: irreversible → owner before the page stays (*quoted*, posed as a question).
- 孫子: inside the comparison — "a rare but dangerous step can still justify a script when the page's error cost is
  high" (*quoted*).
- Linus: inside the comparison — "A yearly recovery procedure might justify automation because a mistake is costly"
  (*quoted*, labelled by him as conditional, not measured).
- Dario: assumed it counts like any other cost; asks whether EJ wants "a separate rule" (*quoted*).

## What each added that the others did not

- **Linus**: drop "try the script first" for this exception, decide before building (*my reading*); "an unknown input
  is not zero" (*quoted*); commit message as the record when there is no task (*quoted*).
- **范蠡**: the trigger is observed, not forecast — "The test is not 'will it run often?' … The test is 'has it come
  round again?', which can be observed" (*quoted*); the page must be exact commands with expected results; a planted
  stale-command test (*quoted*: "Give an agent an existing page containing one stale command"); asks whether a run's
  `state.md` records which page it followed.
- **孫子**: the cost table (once / keep over H / each run / errors) with common writing cost cancelled; each term a
  range, "if the sign of the difference is the same at both ends of the range, the case is clear; if it changes, the
  case is close" (*quoted*); a person's approval gate cancels on both sides and is not a page argument; pre-rule pages
  decided at first revision; the unit question (whose time); flags that W3.6 now bundles four things and "the cleaner
  fix is to split it, but only the owner changes the spec" (*quoted*).
- **老子**: the owner holds the *value* half of every decision, not only contests (*my reading*); savings "counted only
  over runs on ground that stays still" in the sentence itself (*quoted*); a change to the experts' answer format —
  one comparison sentence in a common shape, each half marked owner-or-agent (*quoted*, step 10). Note: his answer
  file opens with a stray line, "I'll read the brief first." (*quoted*; engine noise, not content).
- **Dave**: a falsification test — pages followed again versus scripts run again, as a control; "If pages followed
  again show no more missed or out-of-date steps than the control scripts show breaks, I was wrong" (*quoted*); a
  failed "will not run again" prediction is recorded as a failed prediction; two repo insights, labelled n=1–2 and by
  analogy; asks whether a reason on the page breaks the "product docs, no history" rule.
- **Dario**: asks who follows the pages — agents, EJ or both — since skill erosion (C18) is about people (*quoted*);
  "Build cost is certain and now, while keep cost is uncertain and later. 'Not worth it' will be over-chosen"
  (*quoted*).

## What they need to know (questions merged, each with its options)

1. **When is the page-or-script decision made?**
   - a. At writing only (Linus; 老子 with a dated `state.md` line).
   - b. At writing, and again by the next follower of the page (Dave; Dario: each time it is followed).
   - c. Writer only says "page for now"; the decision is made on the next run that follows it (范蠡).
   - d. At writing, or at the first revision of a page older than the rule (孫子).
2. **Does the writer still try the script first for this exception?**
   - a. Yes — the try prices the build (Dave, 孫子 as a probe, Dario).
   - b. No — decide and record before building (Linus).
   - c. Not at writing; at the repeat run (范蠡).
3. **What goes to the owner besides a contest?**
   - a. Nothing else (Linus, Dario).
   - b. Close cases and cases with missing facts; the page stays provisional meanwhile, which makes the page the
     default in close cases (孫子).
   - c. The value of the saving, always (老子).
   - d. Values no run can show / irreversible procedures (范蠡, Dave).
4. **Where does the written comparison live?** (the `levels` key puts a SHOULD reason in `state.md`)
   - a. In the task's `state.md` (Linus — or the commit message; 范蠡; 老子).
   - b. On the page (Dave).
   - c. On the page, with a one-line pointer in `state.md` (孫子).
   - d. EJ to say (Dario).
5. **How are emergency, first-time-must-work or irreversible procedures handled?**
   - a. Inside the same comparison, through a high error cost (孫子, Linus).
   - b. They must be exercised: a drilled page or a scheduled script; the owner picks which (老子, 范蠡).
   - c. The owner decides before such a page stays (Dave).
   - d. A separate rule defaulting them to scripts (Dario, offered as an option).
6. **What does `fails_if` say?**
   - a. Unchanged (Linus, Dario).
   - b. "no written reason" → "no written comparison" (Dave).
   - c. Fails when no comparison naming both sides is written (老子).
   - d. Fails when the page is followed again with neither a script nor the comparison (范蠡).
   - e. Tells the two page kinds apart: the unscriptable step named, or the comparison and its terms named (孫子).
7. **Must a page kept on cost have a set form?**
   - a. No set form (Linus, 孫子, Dave, Dario).
   - b. Exact commands, each with the result to expect (范蠡).
   - c. It names what it is for and what the script could not hold (老子).
8. **Whose time is the unit of the comparison?** (孫子)
   - a. The writer's task time plus the owner's review time (孫子's assumption).
   - b. Agent time priced at zero — then, per 孫子, "the page exception will almost never fire" (*quoted*).
9. **Does anything run this repo's scripts on a schedule or in CI?** (老子, Dario; 孫子 puts the schedule in the keep
   term)
   - a. Yes — the keep side is as assumed.
   - b. No — the keep side is heavier, which tilts toward pages (老子, Dario).
10. **Who follows these pages?** (Dario)
    - a. Mostly agents — harm is mostly drift and misreading; tilts toward page.
    - b. Mostly EJ — skill erosion applies; tilts toward script.
    - c. Both.
11. **Are one-off or throwaway procedures settled once as a class?** (孫子)
    - a. Yes — the owner states "no scripts for throwaway tasks" as a value.
    - b. No — the comparison handles each one.
12. **Does a run's `state.md` record which procedure page it followed?** (范蠡)
    - a. Yes — the reviewer can check the repeat-run rule.
    - b. No — the added text must also require that log line.
13. **Is a reason on a `docs/` page "history" under the owner's product-docs rule?** (Dave)
    - a. No, it is a current reason — it may sit on the page.
    - b. Yes — it goes back to `state.md`, and the next follower will not see it.
14. **Who is W3.6's reviewer and the owner, and are they reachable when a procedure is written?** (老子)
    - a. The owner, reachable — decisions as proposed.
    - b. Not reachable then — the agent writes the comparison and the open question in `state.md`; the owner rules
       later.

*My reading*: the questions above are as the experts posed them; several (8, 9, 10, 12, 14) are facts the main agent
may be able to read in the repo rather than ask.

## Check

- **Check results** (*quoted* from the task and each `check.txt`): linus pass; fan-li pass; sun-tzu pass; lao-tzu
  pass after one rerun (first run: "lao-tzu answer missing 5 required sections", `nodes/experts.progress.md`); dave
  pass; dario pass. Each `check.txt` was run inside that expert's own subfolder, so its five "no answer file" lines
  are the other experts, expected, and none names its own expert (*my reading*).
- **Engines** (from each `status.json`, *quoted*):
  - Linus — codex, gpt-6.1-sol, 44 s, exit 0.
  - 范蠡 — claude, claude-opus-5-5, 182 s, exit 0; **fallback from agy**, reason "task needs web".
  - 孫子 — dsh, deepseek-flash (dsh headless profile), 256 s, exit 0.
  - 老子 — opencode, minimax-coding-plan/MiniMax-M3.1-Flash-Preview, 50 s, exit 0 (the rerun; status shows only it).
  - Dave — claude, claude-opus-5-5, 236 s, exit 0.
  - Dario — claude, claude-sonnet-5-5, 72 s, exit 0.
- **Three of six answers ran on Claude** (范蠡 by fallback, Dave, Dario), and all six shared one brief and one research
  section (*my reading*); agreement among them is not independent evidence.
- **What the check does not establish**: the check script was written by Claude; it checks that an answer file exists
  with its required sections and citations, and does not establish that any expert applied a rule correctly or that a
  quoted line says what it is cited for (*not measured*).
- **Not verified here**: this step did not re-open the research sources or the experts' cited files (`linus.md:19`,
  the YAML line numbers, the insight ids) (*not measured*).
