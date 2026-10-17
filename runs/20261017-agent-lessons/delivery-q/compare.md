# Six experts — deliver a lesson with the edit's result (A), or hold the first edit (B)?

Question: `runs/20261017-agent-lessons/delivery-question.md`. Answers: `delivery-q/<expert>/answers/<expert>.md`.
This file compares the answers. It does not decide anything: the main agent decides, provisionally, and EJ accepts or declines at the end.
Labels: *quoted* (from an answer), *my reading*, *not measured*.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | B, hold once per lesson per session, provisionally (*quoted*) | B, with the shown-mark written first and a "not forbidden, send it again" reason; switch to A if a live trial shows context arrives before the tool runs (*quoted*) | B, once per lesson per session; context only where nothing can be written (*quoted*) | B; switch to A if the docs confirm `additionalContext` arrives before the tool runs (*quoted*) | B, with a "not judged wrong" reason and a record of the denied and retried inputs; provisional until A, B and a no-lesson control are compared (*quoted*) | C: context only, never a hold, given at the Read before an edit and again at the edit; hold once as a per-lesson fallback (*quoted*) |
| Main items used | #2, #3, #5, #7, #9, #13, #18 | #3, #4, #5, #9, #10, #11, #12, #13, #18 | #1, #2, #3, #4, #5, #6, #8, #10, #12, #15, #16, #17 | #1, #2, #3, #4, #5, #6, #7, #8, #9, #10, #11, #13, #14, #16, #17, #18, #19 (says it does not use #12) | #1–#10 | — |
| Insights cited | — | — | — | — | `runs/20261016-four-experts-what-counts-as-change/insight.md#F-cc665076` | — |

## Where they agree

- Five of six choose B (Linus, 范蠡, 孫子, 老子, Dave) and Dario chooses C. *Quoted* (each answer's Choice line). *My reading:* this is not a vote. All six had the same brief, and three of them ran on Claude (范蠡 as a fallback, Dave, Dario).
- On A, the lesson for the first match probably reaches the agent only after the first edit has run. All six say so. *Quoted:* Dario, "the first match of a lesson therefore arrives after the edit it was meant to guide"; Dave, "the edit is already written when PreToolUse fires … A can only affect the next step"; 孫子, "A is learn-after-the-edit"; 老子, "Option A is 亂後"; 范蠡, "the first edit already holds the mistake"; Linus, "A can deliver the lesson after the first relevant action". Whether context is shown before the tool runs is *not measured*.
- B costs one denied call and one retry per lesson per session, and a hold also fires on a call that was already correct. All six say so (*quoted*: Linus, "A correct action can therefore be interrupted"; Dario, "including when the agent was already doing it right").
- B rests on a deny path the run has already used; A rests on a timing the docs do not settle. 范蠡 #18, 孫子 #2/#4/#17, 老子 #8 and Linus #13 say this. *Quoted:* 孫子, "B is safe under either ground; A is safe under only one."
- If context turns out to arrive before the tool runs, A is better. 范蠡, 孫子 and 老子 say this outright, and Linus says "If A produces the same useful outcomes with fewer interruptions, prefer A" (*quoted*).
- The "shown" mark must be written before the deny returns, or the retry is held again and the agent loops. Linus ("record their delivery before returning the denial"), 范蠡 ("Loop risk") and 老子 ("the one thing that can make B worse than A") say this (*quoted*).
- B is wrong if retries mostly repeat the denied call unchanged, or if mistakes do not fall while turns rise. Linus, 孫子, 老子 and Dave say this (*quoted*). The proposed check is a planted-repeat replay against a control. All six propose some version of it, and none was run (*not measured*).
- Nobody can see what B costs or achieves unless something records it, because a deny writes no journal record. Linus, 范蠡, 孫子, Dave and Dario raise this. 老子 disagrees (see below).

## Where they disagree (side by side, quoted; never averaged)

**1. Hold, or deliver earlier by context**

| B (Linus, 范蠡, 孫子, 老子, Dave) | C (Dario) |
|---|---|
| 孫子: "Make the call unable to run before the lesson, then let it run" | Dario: "Use context and never hold. Return `additionalContext` for a matching Write/Edit/MultiEdit and also for the Read that comes before it, so the lesson normally arrives before the first edit without a denied call." |
| Dave: "The key condition holds for B and fails for A on the first call" | Dario: "Those blocked-but-correct calls are noise, which is the opposite of the owner's aim." |

**2. Which calls a lesson may hold**

| Expert | Position (*quoted*) |
|---|---|
| 范蠡 | "I keep B for Bash too, and treat false holds as noise to measure." |
| Dave | "Bash. The logic is the same." |
| 孫子 | "hold only state-changing calls … hold writes, attach on reads"; "If not [able to tell], hold on Write/Edit/MultiEdit only and attach for Bash." |
| 老子 | "if a deny on Write has not run, use B and treat the first session's holds as the test, or (if EJ wants a proven path first) hold only on a matching Bash call." |
| Dario | "Is any lesson about a mistake that cannot be cheaply undone … Those few should be held (B); the others should not." |
| Linus | No split by call type (my reading). |

**3. What the deny reason says**

| Expert | Position (*quoted*) |
|---|---|
| 范蠡 | "the deny reason says the call is not forbidden: send it again, changed if the lesson applies." |
| Dave | "the call was not judged wrong and can be retried unchanged if the lesson does not apply." |
| 孫子 | "the reason must be the lesson, or the hold must not fire"; "the reason carries no lecture beyond the lesson"; "The reason must end with the retry path." |
| 老子 | "keep the reason to the matched lesson and the path, one line." |

*My reading:* 范蠡 and Dave add a sentence telling the agent it may retry. 孫子 asks for nothing beyond the lesson except the retry path. 老子 asks for one line.

**4. A record of each hold**

| Expert | Position (*quoted*) |
|---|---|
| Dave | "a delivery record that keeps both the denied input and the retried input" — "(session, lesson id, tool, path, time, denied input, retried input)." |
| 孫子 | "have each hold write one journal line — lesson id, matched path or command word, and whether the retry differed." |
| Linus | "The delivery state is separate from the execution journal." |
| Dario | "The noise comparison needs a 'lesson shown (id, session)' record in any case." |
| 老子 | "build the smallest thing that works: no severity ranking, no lesson scoring, no second hold, no new journal type." |

**5. Test inside this run, or leave it to the owner**

| Expert | Position (*quoted*) |
|---|---|
| Dave | "The test costs less than this debate … nine runs fit well inside 3 hours", if R12.3 allows a temporary `--settings` file in the run folder. |
| Linus | "Only a later authorized live trial can establish agent behavior." |
| 范蠡 | Offline tests on `handlePreToolUse` "now"; the planted-repeat at "the owner's live trial (R12.3)". |
| 孫子 | "there is no probe now." |
| 老子 | "treat the first session's holds as the test." |

**6. Several lessons matching one call**

| Expert | Position (*quoted*) |
|---|---|
| Linus | "return all newly matching lessons together." |
| 孫子 | Raises it as a question: "Once per lesson would put several blocked calls in a row." |
| Others | Not raised. |

## What each added that the others did not

- **Linus.** He ran the decision through the requirement check, and all eight checks pass for the delivery event. "The outcome claim, *fewer mistakes with less noise*, remains incomplete" (*quoted*). He also notes that "journal silence cannot establish low noise" (*quoted*).
- **范蠡**
  - The plan already allows the mechanism to change. He cites §6 piece 1: "If it cannot, section 3's first bullet changes" (*quoted*; plan line 56, verified by grep).
  - B changes piece 4, "(no deny, context only)" (*quoted*; plan line 59, verified). The owner should know this when they approve piece 5.
  - A held Write re-sends the whole file.
  - The agent may get round a hold by writing through Bash.
  - Proposed change to the pattern: a "trials for the owner" list in the end-of-run report (*quoted*).
- **孫子**
  - Hold calls that change state; give context on read-only calls.
  - Measure "repeated code and testing mistakes per 100 edits" and the share of holds whose retried call differs.
  - The agent may stall and wait to ask EJ, who is not asked until the time ends.
  - Question: "Does a denied edit leave the agent's intended content intact".
- **老子**
  - Routing risk: "The agent changes the path, the file name or the command word until nothing matches. This is the largest risk of B" (*quoted*).
  - Proposed change to the pattern: decide by the premise the run has already exercised, and write that premise into the state entry.
  - Question: has a deny ever fired on Write/Edit/MultiEdit?
- **Dave**
  - A code fact: the hook reads `tool_input`, so "the edit is already written when PreToolUse fires" (*quoted*).
  - Existing data: in long-session arm C, each run hit one deny and the median was 102 s against 83 s. That is n=3, one model, and Stop blocks are included (*quoted*; matches `runs/20261015-long-session/results.md` lines 26–27, verified).
  - Insight F-cc665076: a hold denies a correct call by design.
  - A three-arm headless test (no lesson, A, B), with its prediction written before any result.
  - Question: are lessons mostly about the content of the call (which favours B) or about what to do after the result (A is enough)?
- **Dario**
  - Option C: deliver at the Read before the edit. It rests on "*recall*: Claude Code refuses an Edit on a file not yet read" (*quoted*).
  - The plan's §3 wording "before the edit runs" is wrong for context-only delivery. Plan line 31–32 does read "adds one context line per match before the edit runs" (verified).
  - Compaction: a lesson shown once and then compacted away is not shown again.
  - A subagent could use up the main agent's once-per-session flag.

## What they need to know (merged, each with its options)

1. **Is `additionalContext` shown before the tool runs, and how do we find out?** All six ask this.
   - (a) Run a headless three-arm test now, if R12.3 allows a temporary settings file (Dave).
   - (b) Leave it to the owner's live trial at the end. B stays provisional (Linus, 范蠡, 孫子, 老子).
2. **Does R12.3 cover a temporary `--settings` file in the run folder, used only for a headless test?** (Dave)
   - (a) Yes: run the test before B is final.
   - (b) No: B stays provisional and untested, and the live delivery records become the test.
3. **Which calls may a lesson hold?**
   - (a) Every matched call: Write/Edit/MultiEdit and Bash (范蠡, Dave).
   - (b) Only calls that change state; context on read-only ones (孫子).
   - (c) Write/Edit/MultiEdit only; context for Bash (孫子's fallback).
   - (d) Bash only, until a deny on Write has run (老子's alternative).
   - (e) Only lessons about mistakes that cannot be cheaply undone; context for the rest (Dario).
4. **What does the deny reason say?**
   - (a) "Not forbidden: send it again, changed if the lesson applies" (范蠡).
   - (b) "Not judged wrong; retry unchanged if the lesson does not apply" (Dave).
   - (c) The lesson only, ending with the retry path (孫子).
   - (d) One line: the lesson and the path (老子).
5. **Several lessons on one call.**
   - (a) One deny carrying every new lesson (Linus).
   - (b) One deny per lesson. 孫子 warns this puts several blocked calls in a row.
6. **Is there a cap on `permissionDecisionReason`?** Only the 10,000-character cap on `additionalContext` is known. (范蠡, 孫子)
   - (a) The whole lesson fits: send it.
   - (b) It does not fit: send a pointer plus one guaranteed read. 孫子 calls this "a design change".
7. **What is recorded per hold?**
   - (a) Session, lesson id, tool, path, time, denied input and retried input (Dave).
   - (b) One journal line: lesson id, matched path or command word, and whether the retry differed (孫子).
   - (c) A "lesson shown (id, session)" record (Dario).
   - (d) No new journal type (老子).
8. **Is the shown-mark written before the deny returns, and keyed by a session id that stays the same across the retry?** (范蠡, 老子, Linus)
   - (a) Write the mark first, in a store of its own.
   - (b) Do not ship B until this is shown.
   - *My reading:* the working tree's `lessonLines` already calls `takeUnshown(root, sessionOf(payload), …)` on the context path. Whether that would serve a deny path is *not measured*.
9. **Do subagents' calls fire this hook under the same session?** (范蠡 and Dario, both *recall*)
   - (a) Limit holds to the main agent if the payload allows it.
   - (b) Accept that a subagent may use up the flag.
10. **What are the lessons mostly about?** (Dave)
    - (a) The content of the call: B.
    - (b) What to do after the result: A is enough.
11. **Does Claude Code require a Read before an Edit or an overwriting Write?** (Dario, *recall*)
    - (a) Yes: delivering at the Read reaches most edits.
    - (b) No: delivering at the Read misses some edits.
12. **How much friction counts as noise?** (Linus, 老子)
    - (a) A blocked call counts as loudly as a context line.
    - (b) It counts for less.
    - Linus: "That tradeoff remains theirs; I would not invent a threshold" (*quoted*).

## Check

| Expert | Engine / model (status.json) | Fallback | Check |
|---|---|---|---|
| Linus | codex / gpt-6.1-sol, 80.5 s, exit 0 | — | pass |
| 范蠡 | claude / claude-opus-5-5, 120.6 s, exit 0 | from agy (gemini-3.8-flash-medium): "agy failed: empty answer" | pass |
| 孫子 | dsh / deepseek-flash (dsh headless profile), 112.6 s, exit 0 | — | pass |
| 老子 | opencode / minimax-coding-plan/MiniMax-M3.1-Flash-Preview, 60.3 s, exit 0 | — | **fail**: "Chinese not found in its list: 一件事不夠取天下 (no close passage in the list)"; "Chinese not found in its list: 及其有不 (nearest in the list: 及其有事, 1 character(s) differ)" |
| Dave | claude / claude-opus-5-5, 197.0 s, exit 0 | — | pass |
| Dario | claude / claude-sonnet-5-5, 90.5 s, exit 0 | — | pass |

- **What the check covers.** The check script was written by Claude. It confirms only that each quoted Chinese passage appears in that expert's list. It does not establish that a rule was applied correctly, and it does not check the English facts.
- **Every expert gave a usable answer.** None was filled in.
- **The check.txt files.** Each expert's `check.txt` also lists "no answer file" for the other five, because each folder holds one answer. The per-expert results above are the workflow's, as given in this step's brief. *My reading.*
- **老子's answer**
  - It has a corrupted character in step 7 (`及其有不��`), at the passage the check flagged.
  - Its first line is engine chatter: "I'll read the brief first."
  - Its #18 and #19 passages are marked "attributed", as are 孫子's two #16 uses.
- **Facts I verified (by grep or sed, this step)**
  - 范蠡's plan quotes: §5 line 51, §6 piece 1 line 56, piece 4 line 59.
  - Dario's §3 wording: lines 31–32.
  - Dave's long-session figures: results.md lines 26–27.
- **The code moved during the run.** `guard/src/hooks.ts` in the working tree was modified at 15:01:03, after the answers were written (14:56–15:01). It now has `lessonLines` (lines 109–131), and `handlePreToolUse` returns lesson context for non-Bash calls (line 143). That is A, already wired for Write/Edit/MultiEdit and Bash, uncommitted, from another session. So Dave's and Dario's "`hooks.ts:106` returns quiet for anything but Bash" describes an earlier state of the file. *My reading* from the timestamps; which version each expert read is *not measured*.
- **Nothing was run live.** No answer's prediction was tested (*not measured*).
