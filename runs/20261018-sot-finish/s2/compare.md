# Six experts — approve or change the COO's wording in the memory design's requirements

Question: `runs/20261018-sot-finish/question-s2.md` (APPROVE or CHANGE, vote form). Compared by a Claude subagent
(the compare step); it decides nothing. The main agent decides; EJ accepts or overrules at the end.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | CHANGE: W5.2 text + fails_if, K5.1 fails_if, Rd5.2 check, W1.2a fails_if, K1.1 who_decides | CHANGE: K1.1 who_decides, K5.1 fails_if only | CHANGE: W5.2 text + fails_if + check, K5.1 text + fails_if, Rd5.2 check, K1.1 who_decides | CHANGE: W5.2 fails_if, K5.1 fails_if, Rd5.2 check, K1.1 who_decides | CHANGE: K5.1 text + fails_if + check, W1.2a fails_if, W5.2 fails_if, W6.1a text, Rd5.2 check, K1.1 who_decides | CHANGE: K5.1 text + fails_if, K1.1 who_decides, W5.2 fails_if, W6.1a text, W1.2a fails_if |
| Main items used | #18, #10, #7, #4 | #14, #2, #18, #5 | #1, #10, #16, #13, #4, #3 | #4, #8, #11, #15, #1, #19, #6, #2, #3 | #2, #9, #5, #4, #10 | — |
| Insights cited | — | — | — | — | `runs/20261016-four-experts-what-counts-as-change/insight.md#F-8243a18f`, `#F-336edcb0`, `#F-0f2fa841`, `#F-d8221199` | — |

All rows *quoted* (summarised to the records each answer names). Six of six answered CHANGE (*quoted*); no expert
lacks a usable answer.

## Per record: who changes what (my reading, counted from the answers)

| Record / field | Change | Stand | Not judged |
|---|---|---|---|
| K1.1 `who_decides` | all six, same words | — | — |
| K5.1 `fails_if` | all six, words differ (below) | — | — |
| K5.1 text | 孫子, Dave, Dario | Linus (unlisted), 范蠡, 老子 | — |
| K5.1 `check` | Dave | the other five (not named) | — |
| W5.2 `fails_if` | Linus, 孫子, 老子, Dave, Dario | 范蠡 | — |
| W5.2 text | Linus, 孫子 | 范蠡, 老子, Dave, Dario (not named) | — |
| W5.2 `check` | 孫子 | the others (Dave asks it as a question) | — |
| Rd5.2 `check` | Linus, 孫子, 老子, Dave | 范蠡 | Dario: approves as written, "if it does, apply it" |
| W1.2a `fails_if` | Linus, Dave, Dario | 范蠡, 孫子, 老子 | — |
| W6.1a text | Dave, Dario | Linus (unlisted), 范蠡, 孫子, 老子 | — |
| Rd1.1 | — | all six | — |
| W1.2b | — | five | Dario: "I was not shown W1.2b's text, so I cannot judge it" |
| K5.2 `who_decides` | — | all six | — |

Counts are *my reading*: "stand" includes an expert who did not name the record and said the rest stand (Linus:
*"Unlisted wording stands"*; 范蠡: *"The remaining records stand"*). A count is not a verdict: five of the six engines
got the same brief, and that brief carried Dave's 2026-10-15 findings as facts (see the check below).

## Where they agree

- **K1.1 `who_decides`** — all six give the same new words (*quoted*): *"the project owner, through the project's
  workflow: when work goes the other way"*. Reason, in two of their words: Dario *"A workflow is a document and cannot
  decide, so K1.1 must name a person"*; 孫子 *"a document cannot decide"* (*quoted*).
- **K5.1 `fails_if` must stop firing on an append** — all six replace "a journal file is edited after it is written"
  with a changed-or-removed-line test (*quoted*, words side by side under disagreements).
- **Rd1.1, W1.2b (five of six) and K5.2 `who_decides` stand** (*quoted*; Dario did not judge W1.2b).
- **W6.1a stands as a requirement** — no one removes or weakens its MUST; the two who change it only narrow the text
  to match its `fails_if` (*my reading*).

## Where they disagree (side by side, quoted; never averaged)

**1. K5.1 `fails_if` — the exact words** (all *quoted*)

| Expert | New `fails_if` |
|---|---|
| 范蠡, 孫子 | "a line already written is changed or removed, or raw notes are kept elsewhere, with no written reason." |
| 老子, Dario | "a line already written in a journal file is changed or removed, or raw notes are kept elsewhere, with no written reason." |
| Linus | "a line already written in a journal is changed or removed, or raw notes are kept elsewhere, with no written reason in the task's state.md." |
| Dave | "a commit changes or removes a line already written in a journal file, or raw notes are kept elsewhere, with no written reason." |

Differences (*my reading*): whether the line is scoped to a journal file; whether the reason's place is named
(Linus: `state.md`); whether the trigger is a commit (Dave).

**2. K5.1 text — change it or not**

- 孫子, Dave, Dario change it (*quoted*): 孫子/Dario *"appended to; a line already written is never changed or
  removed"*; Dave *"appended to; a line once written is never changed or removed."*
- 老子 leaves it (*quoted*): *"The record's own text — one file per session, appended to, never edited — already says
  this; only the fails_if was inverted."* Linus and 范蠡 do not name it.

**3. K5.1 `check`**

- Dave (*quoted*): `git` → *"git; reviewer"* — *"Git can see changed lines. Only a person reading can see notes kept
  somewhere else."*
- The other five leave `check: git` (not named; *my reading*).

**4. W5.2 — whether to change, and where the lesson is written**

| Expert | Position (*quoted*) |
|---|---|
| 范蠡 | no change named; "The remaining records stand" |
| Linus | text: "At the end of a task, record other lessons, observations and hypotheses, if any." fails_if: "a completed task has neither a written record of other lessons, observations and hypotheses, a statement that there are none to add, nor a written reason in the task's state.md for omitting the record." |
| 孫子 | text: "At the end of a task, the agent that did it records the task's other lessons, observations and hypotheses in the task's journal." fails_if: "the task's journal does not record the task's other lessons, observations or hypotheses, with no written reason." check: "reviewer; the K5.2 journal-read log line" |
| 老子 | fails_if: "a task ends with no end-of-task entry, with no written reason." — "the taking away happens later, at the entry" |
| Dave | fails_if: "a task ends with no lessons, observations or hypotheses written from it and no reason in its `state.md`; a written 'nothing new' is a reason." |
| Dario | fails_if: "a task ends with no lesson, observation or hypothesis written, and no written reason for none." |

The split that changes the design (*my reading*): 孫子 puts the lesson in the **task's journal** (K5.1); 老子 puts it
in an **entry** (W6.1a's one-file-per-entry); Linus, Dave and Dario name no place. Whether "nothing new" counts:
Linus and Dave say yes explicitly; Dario's "no written reason for none" reads the same way (*my reading*).

**5. Rd5.2 `check`**

| Expert | Position (*quoted*) |
|---|---|
| 范蠡 | stands: "instructions established at court must never be overthrown by memory read on the spot (my #5)" |
| Linus | "reviewer; only on transcript audit" |
| 孫子 | "reviewer; only on audit" — "a MUST checked only from a transcript still gates, but late" |
| 老子 | "reviewer, on audit only" — "the guarantee is real only if audits actually happen" |
| Dave | "reviewer, on audit of the session's journal; test: a planted entry that contradicts a standing instruction is shown to be read, and is not followed" |
| Dario | "I approve it as written … Does the `check` vocabulary have such a value? If it does, apply it." |

What is audited also differs (*my reading*): Linus a transcript, Dave the session's journal plus a planted test,
孫子 and 老子 name no source. 范蠡's "stands" is about Rd5.2's rule; it does not answer whether its check can be
done (*my reading*).

**6. W1.2a `fails_if`**

- Linus (*quoted*): *"the file's first line is not exactly `---`, or the header does not end at the next line that is
  exactly `---`."*
- Dave, Dario (*quoted*): *"the file's first line is not exactly `---`, or no later line is exactly `---`."*
- 孫子, 老子 (*quoted*): stands — 孫子 *"W1.2a … pass"*; 老子 approves, with a question about a field line that is
  exactly `---`. 范蠡: not named.

**7. W6.1a text**

- Dave (*quoted*): *"Agents never add an entry to a file that already exists."* Cost he names: *"the sentence may also
  have been meant to stop agents appending to any shared file, to avoid merge conflicts. If so, the new words drop
  that, and it needs its own record."*
- Dario (*quoted*): *"Agents never append an entry to a file that already holds one."* — *"A hand-appended `INDEX.md`
  or a shared `state.md` would break it literally."*
- Linus, 范蠡, 孫子, 老子: stands. 孫子 raises a different clash instead (*quoted*): if "entry" includes journal session
  files, *"W6.1a's 'never append' clashes with K5.1's 'appended to', and W6.1a needs 'other than journal session
  files'."*

## What each added that the others did not

- **Linus** — W5.2 text with *"if any"* and a *"statement that there are none to add"* as a pass (*quoted*); names
  `state.md` as the place of the reason in K5.1's `fails_if` (*quoted*). *"What I need to know: None"* (*quoted*).
- **范蠡** — the only expert who leaves Rd5.2 and W5.2 untouched (*quoted*); asks whether the workflow should decide
  automatically, in which case K1.1 *"should name an automated tool check instead of the project owner"* (*quoted*).
- **孫子** — W5.2's `check` pointed at *"the K5.2 journal-read log line"* and its text naming *"the agent that did it"*
  and *"the task's journal"* (*quoted*); the W6.1a/K5.1 "entry" clash; whether `CLAUDE.md` only imports `AGENTS.md`
  (*quoted*).
- **老子** — W5.2 tied to an *"end-of-task entry"*; what triggers W5.2's check (*"task closed in `state.md`?"*); a
  stand-in when EJ is away; an escape for a header field that is exactly `---` (*quoted*). Notes *"I did not open the
  YAML"* (*quoted*). Its answer file begins with a stray line *"I'll read the brief first."* (*quoted*; harmless to the
  content, my reading).
- **Dave** — K5.1 `check` *"git; reviewer"*; a planted-entry test for Rd5.2 with a control that the plant was read;
  cites four insights; and flags his own limit (*quoted*): *"the K5.1, W5.2, Rd5.2 and K1.1 points repeat my
  2026-10-15 answer. That is the same rules applied twice, not independent confirmation. Each point is n=1."*
- **Dario** — could not judge W1.2b because its text was not in the brief (*quoted*); asks what "other" in W5.2
  points at, which texts count as "standing instructions", and where `project-memory/` lives (*quoted*).

## What they need to know (questions merged, each with its options)

1. **Does the YAML's `check` field accept a qualifier such as "on audit only"?** (孫子, 老子, Dave, Dario)
   - a. Yes → write it in `check` (Linus/孫子/老子/Dave wordings above).
   - b. No, closed vocabulary → keep `check: reviewer` and write "only on audit" into Rd5.2's text or beside it (孫子,
     Dave); or add a new value (老子).
   - c. Leave Rd5.2 as written (范蠡; Dario's answer if the vocabulary has no such value).
2. **Who writes `INDEX.md` (and does any shared file get appended by hand)?** (Dave, Dario)
   - a. A tool generates it, and no two agents write one `state.md` → W6.1a's current text is true; the change is
     optional.
   - b. Agents append to it by hand → W6.1a's current text breaks Rd1.1's own layout; take Dave's or Dario's wording.
3. **Does "entry" in W6.1a include journal session files?** (孫子)
   - a. No → no clash; W6.1a stands.
   - b. Yes or unclear → add "other than journal session files" to W6.1a.
4. **Where is the W5.2 lesson written?** (from the disagreement; 孫子 and 老子 differ, Dave asks about K5.2's log)
   - a. In the task's journal, checked through the K5.2 journal-read log line (孫子).
   - b. As an end-of-task entry (老子).
   - c. Unnamed: something written or a reason in `state.md` (Linus, Dave, Dario).
   - d. No change (范蠡).
   - Sub-question (Dave): does K5.2 already log every journal read? Yes → W5.2's check can point at that line.
   - Sub-question (老子): what marks the moment W5.2 fires — the task closed in `state.md`, or something else?
   - Sub-question (Dario): what does "other" in "other lessons" point at? An earlier W5 record → the W5.2 text stands.
5. **K1.1 — who decides, and when EJ is away?** (范蠡, 老子, Dave)
   - a. The project owner through the workflow (all six's words).
   - b. A role the workflow already names (Dave: *"name that role instead"*).
   - c. An automated tool check, if the workflow is meant to decide by itself (范蠡).
   - Sub-question (老子): is a stand-in named when EJ is away? No → the new words can leave a decision unmade.
6. **Rd1.1 layout** (孫子, Dave, Dario)
   - Does `CLAUDE.md` only import `AGENTS.md`? Yes → stands; no → 孫子's *"`AGENTS.md` and `CLAUDE.md` at the repo
     root, one importing the other"*.
   - Does an extra folder under `project-memory/` count as "laid out otherwise"? No → stands (Dave's reading); yes →
     the `fails_if` must say so.
   - Is `project-memory/` at the repo root? Yes → stands; no → Rd1.1 needs the path (Dario).
7. **W1.2a: may a header field hold a line that is exactly `---`?** (老子)
   - a. No → stands (or take the Linus / Dave–Dario `fails_if`).
   - b. Yes → the record must name the escape.
8. **Rd5.2: which texts are "standing instructions"?** (Dario) — options given: `AGENTS.md`, the task brief, or both.
9. **W1.2b's text** was not in the brief (Dario) — not judged by Dario; the other five judged it from the brief's
   description only (*my reading*).

## Check

- **Check results** (from the workflow, *quoted*): all six *usable; check pass*. No rerun; each expert's
  `status.json` has `"ok": true`, `"exit": 0`, `"problem": ""`.
- **What the check files say** (*quoted*): every `s2/<expert>/check.txt` ends *"FAIL: 1 answers, 5 failure(s)"*; each
  of the five failures is *"no answer file"* for another expert, because each subfolder holds one answer. No line
  names the expert of that folder. The workflow counts only that expert's lines (`experts-decide.js`, *read*), so
  "pass" means: the answer file exists and has every section. Form: `vote` in all six.
- **Engines and fallback** (*quoted* from each `status.json`): Linus `codex` / `gpt-6.1-sol` (38 s); 范蠡 `agy` /
  `gemini-3.8-flash-medium` (148 s); 孫子 `dsh` / `deepseek-flash (dsh headless profile)` (106 s); 老子 `opencode` /
  `MiniMax-M3.1-Flash-Preview` (34 s; started 05:11:33, after the others — one start in the progress log, so not a
  rerun); Dave `claude` / `claude-opus-5-5` (136 s); Dario `claude` / `claude-sonnet-5-5` (68 s). No fallback recorded
  (no mcode for Linus, no Claude for 范蠡).
- **What the check does not establish** (*my reading*): the check script (`.claude/skills/six-experts/scripts/six_experts.py`)
  was written by Claude. It shows the sections exist; it does not show that an expert applied its cited items
  correctly, that a cited item number says what the answer claims, or that Dave's insight ids carry the meaning he
  gives them. *Not measured* here.
- **Shared-brief caveat** (*my reading*): the brief gave Dave's 2026-10-15 findings on K5.1, W5.2, Rd5.2 and K1.1 as
  facts. Linus cites it three times (*"following the supplied Dave Q2 finding"*, *quoted*), and Dave says his own
  points *"repeat my 2026-10-15 answer"* (*quoted*). The six-way agreement on K1.1 and K5.1 is agreement with a fact
  in the brief, not six independent findings.
