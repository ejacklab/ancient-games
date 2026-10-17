# Six experts — where do lessons live, and how do they reach each agent?

Question: `runs/20261017-insight-placement/question.md`. All six answered; all six usable. Labels: *quoted* (from an
answer), *my reading* (the comparer's), *not measured*. This file decides nothing; the main agent decides.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Store (Q1) | `~/.agents/insights/all/` + one dir per agent type | `~/.agents/insights/` `all/` + one dir per engine | `~/.agents/lessons/`, private git repo, one file per lesson, `scope:` + `triggers:` | `~/.agents/lessons/` `all.md` + `<engine>.md`; main agent sole writer and reader | a `lessons` skill in this repo, one file per lesson, `agents:` + `trigger:`; private folder if private lessons | `~/.agents/insights/all.md` + one file per engine |
| One-type vs all | directories | directories | a field (`scope`) | files | a field (`agents`) | files |
| Project place (Q2) | versioned records with path coverage (SoT `covers`); comments only for local explanation | inline comment, or `lessons.md` in the code's folder | one `.agents/lessons.yaml` at repo root, glob → one line | `project-memory/entries/L-*.md` with `covers:`; "comment never" | a lessons file in the code's folder, keyed by path; names the test when the fix is a test | `covers:` entries in `project-memory/` |
| Engines (Q3) | main agent selects, embeds text in brief | main agent filters, `## Lessons` block in brief | selector command `lessons-for` fills "Lessons that bite here" | picked at node-design time into the brief | fixed-rule script fills brief's Lessons section | main agent matches triggers, puts few into brief |
| Main agent (Q3) | verified startup entry point + selection before work | guard alerts before writes | guard: SessionStart + PreToolUse Write/Edit, max two lines | no hook; lessons every node needs → one line in `AGENTS.md` | guard matches Write/Edit paths and Bash command words | guard hook on matching Write/Edit path |
| Main items used | #2 #5 #7 #9 #11 #13 #18 | #2 #3 #14 #16 #18 | #1 #2 #3 #5 #8 #10 #12 #13 #17 #19 | #1–#4 #6 #8 #9 #12 #13 #16 #18 #19 | #1–#10 | — |
| Insights cited | F-682702da | F-682702da | F-682702da, F-15cf1278, F-98c2c4c9, F-8243a18f, F-96578c5b | F-682702da | F-682702da, F-4981093a, F-d8221199, F-84636a96, F-2cc835e3, F-15cf1278, F-98c2c4c9, F-05a1b440, F-4cbb2f4b, F-2cdebf3b, F-b7c8635f | — |

(Table cells: *quoted* in substance from each "Recommended version"; the grouping into rows is *my reading*.)

## Where they agree

- **Engines get the lesson's text inside the brief, never a path to go read.** All six. *quoted* — Linus: "An external
  path alone cannot serve a worker limited to its brief"; Sun Tzu: "No engine is asked to fetch anything"; Lao Tzu:
  "Never: … 'go read it'"; Dario: "the lessons have to be copied into the brief"; Dave and Fan Li say the same.
- **Only the matching lessons go in, not the whole store.** All six (filter by engine type plus task/paths). *quoted* —
  Linus: "All-agents describes audience; it does not mean every lesson belongs in every brief."
- **The store is not read by opencode or agy; the main agent (or a script it runs) is the reader.** All six, from the
  question's facts. *my reading*.
- **A skill is not a reliable delivery channel, because it loads on a description match.** Linus, Sun Tzu, Lao Tzu,
  Dario say so outright; Dave keeps the skill only as the container and delivers by trigger, not by skill load.
  *my reading*.
- **The store lives outside this public repo** — five of six (all but Dave, who puts it here unless private lessons
  arrive). *quoted* — Sun Tzu: "this repo is public, so a store naming other projects' traps would be published."
- **The code map cannot hold anything today; a path key keeps the door open for it.** Linus, Fan Li, Sun Tzu, Lao Tzu,
  Dave, Dario. *my reading*.
- **When the fix became a check or test, the lesson shrinks to a pointer or leaves.** Sun Tzu ("the store keeps only a
  pointer"), Lao Tzu ("retired from the store"), Dave ("the test is the memory"). *quoted*.
- **A wrong or missing trigger fails silently; only a planted/replayed repeat tests delivery.** Linus, Sun Tzu, Lao Tzu,
  Dave, Dario. *quoted* — Dave: "A wrong trigger never fires, silently."

## Where they disagree (side by side, quoted; never averaged)

**Q1 — where the store sits**
- Five: user-global under `~/.agents/` (Linus, Fan Li, Dario `insights/`; Sun Tzu, Lao Tzu `lessons/`).
- Dave: "Keep the lessons in this repo as one skill linked into both skill roots … if lessons will be filed from EJ's
  private work projects, the lesson files cannot sit in this public repo." Reason given: "version history, commit-hash
  citations, links that already exist in both roots, and one copy."
- Within user-global: Sun Tzu "a private git repo"; Lao Tzu and Dario a plain home folder ("Not in git — no history"
  is Lao Tzu's own cost line).

**Q1 — how one-type is kept apart from all-agents**
- Directories: Linus, Fan Li — "prevents one engine from reading rules that apply only to another" (Fan Li).
- One file per scope: Lao Tzu, Dario — "An engine reads `all.md` plus its own file" (Dario).
- A field, one directory: Sun Tzu ("one copy kept whole beats copies per engine"), Dave ("One lesson can belong to two
  engines … Folders would need two copies").

**Q2 — what "kept with the code" means**
- SoT `covers:` entries: Linus, Lao Tzu, Dario — Lao Tzu: "already decided, and it is `covers:`".
- A file in the code's folder: Dave ("can be found by walking up from the edited path"), Fan Li (or a comment).
- One file at the repo root: Sun Tzu — "a file in the code's folder drifts and is invisible from the root".
- A comment at the line: Fan Li allows it ("encountered directly upon reading or editing the code"); Lao Tzu refuses it
  ("check first, entry second, comment never"); Linus "only for local explanations"; Dario "the weakest".

**Q3 — the main agent's delivery**
- Guard hook at the write: Fan Li, Sun Tzu, Dave, Dario. Dave adds Bash command words.
- No per-write hook: Lao Tzu — "A PreToolUse hook that injects on every Write/Edit is a weapon used constantly";
  instead lessons are picked at design time, and a lesson every node needs becomes a line in `AGENTS.md`.
- Linus — a "verified main-agent startup entry point" plus selection before work, and the guard fact is wrong today
  (see below).

**Q3 — who fills the brief's lessons**
- A fixed-rule script: Sun Tzu (`lessons-for --repo --paths --engine`), Dave ("a script with fixed rules and no LLM").
- The main agent: Linus, Fan Li, Lao Tzu, Dario. Fan Li makes it conditional: script-enforced if briefs are
  generated, a checklist if hand-written.

**When a lesson is filed**
- Sun Tzu: "I would file only the chosen fix and leave the rest in the run's `insight.md`."
- Dave: "deliver a lesson from the day it is written, marked 'open', not only after its fix is chosen" (2 of his 6
  repeats had unchosen fixes).
- Linus: record "decision status"; "EJ's recorded choice governs an adopted fix". Others silent.

**Noise cap**
- Sun Tzu: "at most two lines per push, one line per lesson."
- Lao Tzu: comparative only — "if the lesson block is ever longer than the rest of the brief, it is … a document that
  belongs in `AGENTS.md`"; "I do not invent a count".
- Linus, Dave: the number is EJ's or unmeasured. Dario: "more than a few per brief" as a looseness sign.

## A fact in the question that one expert found wrong

- Linus: "The supplied guard fact conflicts with checked-in code: installation registers PreToolUse for Bash … the
  handler returns immediately for other tools." *quoted*.
- Checked by the comparer by reading the code: `.claude/skills/workflow-design/guard/src/install.ts` lists
  `["PreToolUse", "Bash"]` and `["PostToolUse", "Bash|Write|Edit|MultiEdit"]`; `guard/src/hooks.ts` `handlePreToolUse`
  starts `if (payload.tool_name !== "Bash") return quiet();`. *my reading of the code* — so today the guard sees
  Write/Edit only after they run. Not tested by running a hook (*not measured*).
- Consequence, *my reading*: the main-agent hook delivery of Fan Li, Sun Tzu, Dave and Dario rests on the question's
  fact; it needs a new PreToolUse registration for Write/Edit/MultiEdit, not only a matcher. Sun Tzu cites guard
  `SPEC.md` M5 for the fact; the comparer did not check M5.

## What each added that the others did not

- **Linus:** the guard-fact conflict above; F-682702da's defect no longer exists ("the current exporter copies
  reference directories"), so a project record must keep the failure and the fix with dates, not teach a stale trap;
  ask which startup mechanism is actually loaded per harness. *quoted*.
- **范蠡:** inline comments as a valid project place; per-engine folders so an engine never reads another's rules; if
  EJ uses several machines, the store needs git to sync. *quoted*.
- **孫子:** start from the classes that already repeated the same day (F-15cf1278 → F-98c2c4c9, F-8243a18f → F-96578c5b),
  not all 56; a required `triggers:` field ("A lesson with no trigger is not filed yet"); `lessons-for` selector; the
  public/private answer is "the only answer that moves the store". *quoted*.
- **老子:** the drain — a lesson retires when a check enforces it, and the store's line count should fall while checks
  rise; a new `Seen on:` (engine) field, because `guard/src/insight.ts` has no engine field today ("nothing can be
  routed and everything would be universal"); one writer (the main agent); SoT already leaves agent memory to the home
  folder (`~/.claude/agent-memory/<name>/`), keyed by name, not type; `EXECUTOR_KINDS.md` records Codex not listing
  `~/.claude/skills` and agy's skill-dir reading as unknown. *quoted*.
- **Dave:** data — 6 repeats found by searching insight files; "none of the 6 repeats was caused by where a lesson was
  stored", "delivery decides more than location" (*quoted*; his sorting, n=6, no control, *not measured* beyond that);
  a paper replay predicting 5 of 6 would have fired; build order: brief part first, guard second; his own brief got the
  whole 56-line index because no category was named — the noise the owner names. *quoted*.
- **Dario:** each lesson carries a date and a recheck owner; a "split check" — read 10 stored lessons and count any that
  name a repo path (each is a failed split); asks whether `project-memory/` exists yet (Lao Tzu reports it does not).
  *quoted*.

## What they need to know (merged, each with its options)

1. **Are lessons public (part of the Ancient Games) or private — and will any come from EJ's private work projects?**
   (Sun Tzu, Dave, Dario, Linus, Fan Li) — (a) private user-global store under `~/.agents/`; (b) public, in this repo
   (a skill, or `agent-lessons/`); (c) split: matcher/skill in this repo, lesson files in a private home folder (Dave).
2. **One machine, or several / shared with someone?** (Fan Li, Lao Tzu, Dario, Linus) — (a) one machine: a plain home
   folder; (b) several or shared: a private git repo for the store.
3. **When is a lesson filed?** (Sun Tzu, Dave, Linus) — (a) only after EJ picks the fix; (b) from the day the insight is
   written, marked "open".
4. **May a lesson leave the store once a check enforces it?** (Lao Tzu; Sun Tzu and Dave lean the same way) — (a) yes:
   retire it, or keep only a pointer to the check/test; (b) no: lessons stay as advice, and noise is cut by selection
   alone.
5. **How does the main agent get a lesson?** (all) — (a) a guard hook at the write (needs PreToolUse registered for
   Write/Edit — not there today); (b) selection at design/brief time only, with near-universal lessons as one line in
   `AGENTS.md` (Lao Tzu); (c) a verified startup entry point plus selection before work (Linus).
6. **Who fills a brief's Lessons section?** (Fan Li, Sun Tzu, Dave vs Linus, Lao Tzu, Dario) — (a) a fixed-rule
   selector script; (b) the main agent by hand, against a checklist.
7. **How is one-type kept apart from all-agents?** — (a) directories; (b) one file per scope; (c) one field in each
   lesson file.
8. **What does "kept with the code" mean?** — (a) SoT `covers:` entries in `project-memory/` (not yet created);
   (b) a lessons file in the code's folder; (c) one path-keyed file at the repo root; (d) a comment at the line.
9. **Do the main agent's 60+ per-project memory files move into the store?** (Dave, Lao Tzu) — (a) only the tool/agent
   lessons move; (b) all move; (c) none move.
10. **Agent type or agent name?** (Lao Tzu, Dario) — (a) type, as decided; (b) reuse SoT's `~/.claude/agent-memory/<name>/`,
    keyed by name.
11. **Facts to probe, not to choose** (Lao Tzu, Dave, Dario): do opencode/agy read `~/.agents/skills`; do Codex/dsh run
    hooks at the moment of action; how much text a guard hook can add — (a) probe before building; (b) assume no and
    rely on the brief.
12. **How is noise judged?** (Linus, Dave, Sun Tzu, Lao Tzu) — (a) a fixed cap (Sun Tzu's two lines); (b) a comparison:
    lesson lines per brief against today's whole-index brief (Dave), or lesson block against the rest of the brief
    (Lao Tzu).

## Check

- Workflow check result: all six *check pass* (from the step's input). Each subfolder's `check.txt` lists five
  `FAIL <other>: no answer file` lines — one per expert not in that subfolder — and no line for its own expert.
  *my reading*: that is the expected shape when each expert runs in its own folder.
- Engines, from each `status.json` (exit 0, `ok: true`, no problem, no fallback recorded):
  Linus codex `gpt-6.1-sol` 88.5 s; 范蠡 agy `gemini-3.8-flash-medium` 122.7 s; 孫子 dsh `deepseek-flash` 112.5 s;
  老子 opencode `MiniMax-M3.1-Flash-Preview` 171.1 s (started 13:43, about 4 min after the others); Dave claude
  `claude-opus-5-5` 207.3 s; Dario claude `claude-sonnet-5-5` 40.2 s.
- 老子's answer file begins with three lines of engine narration ("I'll read that brief first." …) before the heading.
  *quoted*; harmless to the content.
- The check script was written by Claude. It checks that answers exist and that quotes match the lists; it does not
  establish that a rule was applied correctly, nor that the experts' readings of this repository are right. Only
  Linus's guard claim was re-read by the comparer (above).
- Five of six engines answered one brief with one fact list; agreement among them is not independent evidence.
  *my reading*.
