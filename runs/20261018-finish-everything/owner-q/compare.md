# Six experts — two choices that wait for the owner (Q1 owner-only questions at once; Q2 Claude Code's memory in memory-check F1)

Question: `runs/20261018-finish-everything/owner-question.md`. Five experts were asked in this run; 老子 (Laozi) was not
in the workflow's list, so there is no Laozi column and no Laozi answer (my reading of the step's expert list; the
check script still looks for a `lao-tzu` file, see Check).

| | Linus | 范蠡 | 孫子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|
| Q1 (one line) | (a), with an "answerability check" first | (a) | (a), gated by one line: "which trial would answer this, and why can it not?" | (a), with a reshaping step first and a "whose fact or value" line | (a), when the agent names who decides and shows no check could fail a wrong choice |
| Q2 (one line) | (a) provisionally; (b) if SoT makes it authoritative, (c) if disposable | (a); (c) if memory-check is only for the portable guideline spec | (a), on a separate "also found" line labelled *harness memory for this project*, never "agent memory"; (c) if only guideline-governed memory is in scope | (a), labelled "Claude Code's memory, not a location the guidelines name"; never (b); (c) if the vision limits locations | (a), present/absent only, no file names or contents |
| Main items used | #13, #19, #5, #7, #9, #10, #2, #4 | #3, #7, #14, #13, #4, #18, #5 | #1, #11, #4, #17, #8, #2, #13, #6, #20, #3, #16, #15 | #1, #5, #4, #10, #6, #7, #3, #2, #8, #9 | — |
| Insights cited | — | — | — | `runs/20261017-experts-speed-trial/insight.md#F-1ed514ad` (with F-1c81bc00); none for Q2 | — |

All table cells: *quoted* or close paraphrase of each answer's Answer section; the item lists are *my reading* of the
"my #N" references in each answer.

## Where they agree

- Q1: all five pick (a). *quoted* (each Answer section).
- Q1: four of five attach a gate so the class "no trial can answer it" cannot become an escape hatch — Linus's
  "answerability check", 孫子's one-line "which trial would answer this, and why can it not?", Dave's reshaping step
  plus "whose" line, Dario's "who decides … and what check would fail a wrong choice". 范蠡 names the same risk as a
  question instead of a gate ("Is there an objective, verifiable test…?"). *quoted*; the grouping is *my reading*.
- Q1: the shared reason is that a trial with no check that can fail it returns no information, so three trials only
  delay. Linus: "Repeating an action that cannot change the answer is not verification"; 孫子: "the 'none' case, paid
  for three times"; Dario: "each trial returns no information, and three of them only delay the question". *quoted*.
- Q2: all five pick (a), present or absent only. *quoted*.
- Q2: all five reject (b) because the folder does not follow the guidelines' entry format and would produce false
  failures (Linus "false failures from format mismatch"; 范蠡 "creating artificial failures"; 孫子 "would produce false
  failures"; Dave "Never (b)"; Dario "rule out (b)"). *quoted*.
- Q2: four of five name (c) as the fallback if the owner reads memory-check's scope as only the locations the
  guidelines name (范蠡, 孫子, Dave, Dario's "(c) gets stronger"); Linus ties (c) instead to the folder being
  "generated or disposable harness state". *quoted*; grouping *my reading*.
- Q2: path fragility (how Claude Code encodes `.`, `_`, worktrees, subfolders) is raised by Dave and Dario; coupling to
  Claude Code's internal paths / drift by 范蠡, Dave and Dario. *quoted*.

## Where they disagree (side by side, quoted; never averaged)

- **Q2 — is the folder "agent memory"?**
  - Linus: "A repository-specific store used by Claude Code is relevant agent memory even when its implementation path
    belongs to the harness." *quoted*
  - 孫子: "the answer to the title is **no, it is not agent memory**" — it is "project memory in the harness's keeping".
    *quoted*
  - Dave: "By the guidelines' own definitions it is not agent memory (my reading), so the answer to the question's title
    is no." *quoted*
  - Dario: does not rule; argues "it is the harness's memory, not the project's" "does not separate the two cases
    cleanly", because Claude Code's subagent memory also lives at `~/.claude/agent-memory/<name>/` ("recall, not
    verified here"). *quoted*
  - 范蠡: does not rule on the label; treats it as "real assets" to be measured. *my reading*
- **Q2 — who settles the classification?**
  - Linus: "let the source-of-truth owner settle classification". *quoted*
  - Dave: "a question for the source-of-truth design, sent there as a request, not decided inside memory-check".
    *quoted*
  - 孫子: settles it now from `SOURCE_OF_TRUTH.md:20,24` ("The guidelines' own definition decides it"). *quoted*
- **Q2 — what the report line shows.**
  - 孫子: "path, present or absent, a count, no pass or fail" on an "also found" line. *quoted*
  - Dario: "present or absent only … no file names or contents in the report". *quoted* (no count mentioned)
  - Dave: "one row, present or absent, with no check and no warning line". *quoted*
  - Linus: inventory "as present or absent". *quoted*
- **Q1 — what "at once" means outside a time-boxed run.**
  - 孫子: "into the next batch of 3.3, not a separate summons". *quoted*
  - 范蠡: "in an untimed run they go to EJ immediately". *quoted*
  - Dave and Dario: little gain inside a time-boxed run; Dave says the main fix is the Fails-if line (`:591-593`) that
    forbids listing early; Dario: "In an untimed run the gain is larger". *quoted*
- **Q1 — are the question's three examples really owner-only?**
  - Dario: "'Which location a requirement names' is settled by reading the guidelines … 'Whether a real project exists'
    is settled by looking, unless the project exists only in the owner's world." *quoted*
  - 孫子: the examples "are not in the ground to be measured. They are held by a person." *quoted*
- **Q2 — file count (a fact, not a view).** 孫子 and Dave: 48 files; Dario: "49 `.md` files including `MEMORY.md`
  (verified: counted)". *quoted*. I counted 48 files, 48 `.md`, today (my run of `find`; not independent of the
  folder changing between counts — *my reading*).

## What each added that the others did not

- **Linus:** Q2 order — add the path to the inventory first, keep any conformance policy as "a separately testable
  change"; fixtures for canonical/native × present/absent; flags that the brief's count and schema were unchecked
  ("do not decide from unchecked recall"). *quoted / my reading*
- **范蠡:** the risk of workers idling or "shirk[ing] effort" by classing solvable problems as untriable (「無曠其眾，以為亂梯」);
  harness coupling as ongoing maintenance for an external tool. *quoted*
- **孫子:** the label is part of the pick (a durable mislabel, #16); privacy — `MEMORY.md` opens with personal facts, so
  count only, no names; precedent — opencode, Codex, agy also keep state ("one adapter per harness"); charter creep
  makes runs incomparable on the same count; a pre-registered three-run test with falsifier ("a question sent at once
  that a trial could have answered"); checked `~/.claude/agent-memory` does not exist. *quoted*
- **Dave:** the reshaping step (turn a threshold into a comparison) from insight F-1ed514ad and EJ's "how can I give you
  a number?"; the 3.8 item 14 Fails-if (`:591-593`) currently makes early asking a failure; the 20261017-memory-check
  run already behaved as (a) (items 2 and 15), so (a) vs (b) gave the same outcome there, n=1; the row is evidence the
  W3.5b reviewer needs; the `CACHES.md:489-512` example already names this `MEMORY.md`. *quoted*
- **Dario:** two of the three examples are answerable by reading or looking; F1's "Who decides: the guidelines" and its
  Fails-if must be rewritten once the folder is added; a sentinel-string test that no content leaks into the report;
  `--home` must redirect the path; never looked at run ledgers for whether the three-trial rule ever burned trials on
  an owner-only question (not measured). *quoted*

## What they need to know (merged, for the owner — each with its options)

1. **Q1 — who judges that "no trial can answer it", and against what?** (Linus, 范蠡, 孫子, Dario)
   Options: (i) the main agent alone, writing the one-line reason (which trial / which check was looked for and why it
   cannot work); (ii) the agent's line plus a second reader (experts or reviewer) who can contest it; (iii) a closed
   list of owner-only kinds (location named by a requirement, existence of an outside project, owner-set value).
2. **Q1 — what "at once" means outside a time-boxed run.** (孫子, 范蠡)
   Options: (i) into the next 3.3 batch of questions; (ii) a separate ask to the owner immediately; (iii) extend 3.8
   item 14's provisional route to every run.
3. **Q1 — where "listed for the owner" is written, and does the owner read it mid-run?** (Dave)
   Options: (i) the state file at the moment of decision; (ii) the end report only.
4. **Q1 — add the reshaping step before a question is listed?** (Dave)
   Options: (i) yes — try a comparison/structure instead of a number first; (ii) no — the gate line alone.
5. **Q2 — memory-check's scope.** (all five)
   Options: (i) only the locations the guidelines name → (c); (ii) all memory a project has / that an agent will load →
   (a); (iii) the source-of-truth design is asked to place the folder in a scope first, and F1 follows it (then (b) if
   it gives the folder a format).
6. **Q2 — the label on the line.** (孫子, Dave, Linus)
   Options: (i) "harness memory for this project" / "not a location the guidelines name" on a separate line; (ii)
   listed as agent memory.
7. **Q2 — what the line may show.** (孫子, Dario)
   Options: (i) present/absent only; (ii) present/absent plus a file count; (iii) file names. 孫子 and Dario warn that
   names would put personal facts in the report.
8. **Q2 — only Claude Code, or every harness?** (孫子, Dario)
   Options: (i) Claude Code only, with a stated reason; (ii) a list of harness memory locations (opencode, Codex, agy).
9. **Q2 — is the folder authoritative, generated, or disposable?** (Linus) Options: (i) authoritative → (b) later;
   (ii) generated/disposable → (c); (iii) unknown → (a) for now.
10. **Q2 — path encoding:** how Claude Code names the folder for `.`, `_`, worktrees, subfolder sessions (Dave, Dario).
    Not an owner choice: settled by a fixture test (*my reading*).

## Check

- Per-expert result as given to this step: linus pass, fan-li pass, sun-tzu pass, dave pass, dario pass. *quoted* (the
  step's task text).
- Each `owner-q/<expert>/check.txt` ends `FAIL: 1 answers, 5 failure(s)`, and every FAIL line is another expert's "no
  answer file" (including `lao-tzu`, not asked in this run). No file has a FAIL line for its own expert; the "pass" is
  the check nodes' reading of that (`nodes/owner-q.progress.md`). *quoted / my reading*
- Engines from each `status.json` *quoted*:
  - Linus: mcode, `minimax/MiniMax-M3.1-Flash-Preview`, **fallback from codex** ("codex has 1% left (20% or less)"),
    56 s, exit 0.
  - 范蠡: agy, `gemini-3.8-flash-medium`, 162 s, exit 0, no fallback.
  - 孫子: dsh, `deepseek-flash (dsh headless profile)`, 130 s, exit 0, no fallback.
  - Dave: claude, `claude-opus-5-5`, 444 s, exit 0, no fallback.
  - Dario: claude, `claude-sonnet-5-5`, 66 s, exit 0, no fallback.
- 老子 (Laozi): not asked in this run; no answer. *my reading* of the step's list.
- The check script was written by Claude. It checks the answer files' form and citations; it does not establish that
  any expert applied a rule correctly, nor that the files and line numbers the experts cite say what they claim.
  *not measured*
- All five answers share one question and two run on Claude (Dave, Dario); the five-of-five agreement on both picks is not
  five independent votes. *my reading*
- No winner is picked here; the main agent decides.
