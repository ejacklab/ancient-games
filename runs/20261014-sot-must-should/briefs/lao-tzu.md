# Brief — 老子 (Laozi) answers one question

You are **老子 (Laozi)**, one of the experts EJ consults. You were built from a numbered list of 老子 (Laozi)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261014-sot-must-should/seats/lao-tzu-list.md` — the "## Final list" section; items are numbered 1–19.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261014-sot-must-should/seats/lao-tzu-identity.md` — the "## Who they are" section.

## The question

# Question: which source-of-truth memory requirements are MUST, which SHOULD, which guidance?

EJ, 2026-10-14: *"which source-of-truth requirements are MUST and which are SHOULD can let 4 experts decide"*.

## The task

Below are the core requirements of the project's Source-of-Truth memory design (`docs/memory-system/SOURCE_OF_TRUTH.md`,
confirmed by EJ 2026-10-12, amended 2026-10-13). Today none carries a level. Give **each numbered requirement**
(W1.1, W1.2, … Rd6.1) one level, with a one-line reason:

- **MUST** — a gate that stops work: when it fails, the commit, task or handoff does not go ahead.
- **SHOULD** — a default: it may be overridden, with the reason written down.
- **guidance** — explanation or advice; nothing fails when it is not followed.

Put your levels in a table in your Answer section: `| Id | Level | Reason (one line) |`, every id once.

## Facts you need

- RFC 2119 §6, quoted: imperatives *"must be used with care and sparingly… they MUST only be used where it is actually
  required… they must not be used to try to impose a particular method."* RFC 8174: the key words have their meaning
  *"only when they are in all capitals."*
- The project's requirement-check skill says: *"A safety bound earns MUST. A method does not."*
- EJ's design choices that stand: no owners and no human approval gate (W4.1); no fixed numbers, comparisons decided
  by measurement; "judged" checks are done by a reviewer reading, not a script.
- Only `tools/memory_index.py` exists today as tooling (it builds and checks `INDEX.md`, K6). There is no lint over
  `entries/` yet and no `project-memory/` folder in any product yet. No run has used this memory yet (n=0).
- Do not change any requirement's wording; only assign a level. If a requirement cannot get a level as written (two
  levels in one id), say so in its row and say which part gets which.

## The requirements, verbatim

### Write — what goes in, and how

**W1 — The shape of an entry** (d: What will be put in)
- **W1.1** Each entry is one file: `project-memory/entries/<prefix>-<id>-<slug>.md`. The prefix is one letter per
  kind (W2): `D-` decision, `F-` fact, `L-` lesson, `O-` observation and `H-` hypothesis. It matches the entry's
  `kind`. There is no runbook prefix (W3.6). An entry's kind, and so its prefix, never changes. A changed kind (a
  hypothesis confirmed, an observation that turns out to be a fact) is a new entry that supersedes the old one (K4.1;
  EJ, 2026-10-13). The `id` is `DD-MM-xxxxxx-YYYY`: the day, month and year the entry is written, six
  random lowercase letters and digits, for example `13-10-k3f7a2-2026` (EJ, 2026-10-13). Writers on different
  branches pick ids without coordinating, so an id is never "the next free number". An id never changes, so the file
  keeps its name.
- **W1.2** The header starts on the file's first line, which is exactly `---`, and ends at the next line that is
  exactly `---`. Each field is one `key: value` line; a field with several values (`covers`, the links, `changed:`)
  holds them on indented lines below its key. The keys are `id`, `kind`, `status`, `author`, `recorded` (the date
  recorded), `covers` (the code paths it is about), `source` (its source or evidence), `depends_on`, `supersedes`,
  `superseded_by` and `changed:`. A decision to build something, once its work is complete, also holds `done:` (W5.3).
- **W1.3** The body follows the header: the claim in one or two sentences, then a line starting with `**Why:**`, then a
  line starting with `**How to apply:**`. There is one claim per entry.
- **Fails if** a lint over `entries/` finds a header not between two `---` lines, a missing field or section, a section
  not spelled as in W1.3, an id not in the W1.1 form, two entries with the same id, or a file whose prefix is not one
  of the five or does not match its `kind`. It also fails if a reviewer finds two claims in one entry, or git shows an
  entry file renamed to a different prefix or id.

**W2 — What each kind means** (v; d: What it is for)
- **W2.1** A **decision** is a choice the code must follow, with the reason. A **fact** is a truth or outside
  constraint the code must respect, not something discovered afterwards. Both are requirements: they are written
  before the code.
- **W2.2** A **lesson** comes from a failure or a human correction. An **observation** records what was seen. A
  **hypothesis** is a guess, labelled as one.
- **Fails if** `kind` holds any other value, or a guess is recorded under any kind but hypothesis.

**W3 — What never goes in** (v; d: What will not be put in)
- **W3.1** Nothing that can be read directly from the code, the tests or the commit log: what a function does, which
  test covers it, what a commit changed. The memory lives in git; the rule is about what an entry says.
- **W3.2** No credentials or sensitive data.
- **W3.3** No raw transcripts, and nothing from another agent's private state.
- **W3.4** No work described as "verified" when it is only implemented.
- **W3.5** No user memory (one person, across projects) and no agent memory (one agent name). Both live in the home
  folder.
- **W3.6** No copy of the project's existing documents (requirements, architecture in `docs/`) or of its procedures:
  an entry links to them. A procedure lives in the repo as a script, or as a page in `docs/` where it cannot be a
  script, and `AGENTS.md` names each script, one line each. A script is project work, not memory (EJ, 2026-10-13).
- **Fails if** a secret scanner finds a credential (W3.2). For W3.1 and W3.3–W3.6, a reviewer finds such content.
  Those are judged checks.

**W4 — Who writes, and the change log** (v: no owners, every change logged)
- **W4.1** Anyone, agent or person, may create or change any entry, and `AGENTS.md` too. There is no owner and no
  approval: `status` is only `active`, `superseded` or `retired`. The one exception is Rd5.3: a reader who finds a
  decision or fact out of step with the code reports it and does not settle it (EJ, 2026-10-12).
- **W4.2** Every change to an entry adds one line to its `changed:` log: the time, and who made it (the model ID for an
  agent, the name for a person). Earlier lines are never edited.
- **W4.3** Files that are not entries (`state.md`, `journal/`, `AGENTS.md`) rely on git history.
- **Fails if** git shows a change to an entry with no matching `changed:` line, or a `status` outside the three.

**W5 — When to write** (d: When to write)
- **W5.1** Written immediately: a decision or fact, before the code it governs; a human correction; and the state of
  unfinished work, before a handoff, an interruption or a context reduction.
- **W5.2** Written at the end of a task: other lessons, observations and hypotheses.
- **W5.3** A decision to build something is started when it is written. When the work is complete, whoever finishes it
  adds `done:` to the decision: the time, the result in one sentence, and the test results, or "no tests" said plainly.
  `done:` points to the evidence (`runs/<run-id>/` or the commit) rather than copying test output (W3.1). A standing
  rule, such as "all timestamps are UTC", is never complete and never gets `done:`. If the result differs from the
  decision, that is a mismatch for Rd5.3: it is reported, not settled in `done:`. (EJ, 2026-10-12; refined after four
  readers.)
- **Fails if** a commit changes code under a new decision with no entry in that commit or an earlier one. For a human
  correction, it fails if the session ends without one (judged). For W5.3, it fails if a reviewer of a finished task
  finds that its decision has no `done:`, or a `done:` without a time, a result and test results or "no tests"
  (judged; EJ, 2026-10-12).

**W6 — Writers do not collide** (d: Changing entries)
- **W6.1** Each new entry gets its own file. Agents never append to one shared file; each journal, the task's or the
  project's, has one file per agent session.
- **W6.2** Each agent works on its own branch or worktree, so two edits to the same lines meet as a merge conflict, not
  a silent overwrite.
- **W6.3** A claim is never rewritten (K4.3), so a merge conflict in an entry is only in the lines added to it. Whoever
  does the merge keeps both sides: both `changed:` lines, both links. Nobody chooses between two claims. Two entries
  that each supersede the same entry are reported in the task's `state.md` and to EJ, as in Rd5.3 (EJ, 2026-10-13). A
  conflict in `INDEX.md` is resolved by regenerating it (K6.3).
- **Fails if** an edit to an entry is lost without a conflict, or a merged entry is missing a `changed:` line or link
  that one side added.

### Keep — memory stays true, and nothing is lost

**K1 — The decision or fact first, then the code** (v; d: What it is for)
- **K1.1** To change behaviour that a decision or fact governs, change the entry first, then the code. Work that has to
  go the other way is a matter for the project's workflow, not for memory.
- **Fails if** git shows a commit changing the behaviour a decision or fact governs, with no change to that entry in the
  same commit or an earlier one (judged).

*K2 (the drift-check script) and K3 (the background subagent) were removed by EJ on 2026-10-12. Their numbers are not
reused, because other text cites K4–K6. A mismatch between a decision and the code is now caught when the decision is
read (Rd5).*

**K4 — Never deleted, never expired by age** (v: nothing lost; d: What will not be put in)
- **K4.1** An entry is never deleted. It is marked `superseded` or `retired`, links to what replaced it
  (`superseded_by`), and keeps its old body.
- **K4.2** Age alone never expires an entry. An entry is found out of date only when someone reads it and checks it
  against the code (Rd5).
- **K4.3** An entry's claim is never rewritten. A changed claim is a new entry that supersedes the old one. After an
  entry is first committed, it only gains a `changed:` line, a new `status`, the `superseded_by` link, and `done:` on a
  decision to build something (W5.3). This also keeps merge conflicts out of claims (W6.3; EJ, 2026-10-13).
- **Fails if** git shows an entry file deleted, a `superseded` or `retired` entry with no link, or an entry's claim
  changed after its first commit.

**K5 — The journal becomes entries** (v: nothing lost between sessions)
- **K5.1** Task and project memory each keep a journal: a task's in `work/<task-id>/journal/`, the project's in
  `journal/` for work not tied to a task. Both hold raw notes, one file per agent session, appended to and never
  edited. Agent and user memory keep no journal under this design (EJ, 2026-10-12).
- **K5.2** At the end of a task, and before a handoff or session end, an agent reads its task's journal (or the project
  journal) written since the last read, writes what is worth keeping as entries, and logs that read in the task's `state.md`. A session cut off
  before it can read loses nothing: the next read covers it (EJ, 2026-10-12: no separate milestones, the start and the
  end already cover them).
- **Fails if** a task's `state.md` shows it complete or handed off with no journal-read log line.

**K6 — `INDEX.md` stays in step** (d: Where it is put; When to write)
- **K6.1** `INDEX.md` is generated from `entries/`: one line per active entry, showing its id, kind and one-line
  claim. It is never edited by hand.
- **K6.2** Whenever an entry is created or changed (any kind, any status change), `INDEX.md` is regenerated and
  committed in the same commit as the entry, so the next session, on any clone, sees it. `tools/memory_index.py`
  builds it; its `--check [<rev>]` compares the `INDEX.md` in the staging area, or in a commit, with what it builds
  from the entries there. Its requirements and design are in `docs/index-md/`.
- **K6.3** `INDEX.md` is never merged by hand. When a merge conflicts, resolve the entry files first, with no conflict
  markers left in them, then regenerate `INDEX.md` and commit it with them.
- **Fails if** a commit's `INDEX.md` differs from what the tool builds from that commit's entries, or it lists a
  superseded or retired entry as active. It also fails if an entry or `INDEX.md` holds a git conflict-marker line
  (`<<<<<<<` or `>>>>>>>`); that part is judged, because the tool does not check for markers.

### Read — the right memory reaches the agent at the right time

**Rd1 — Where it lives, and readable from a clone alone** (v: plain files; never a database or service)
- **Rd1.1** `AGENTS.md` sits at the repo root (`CLAUDE.md` only imports it). `project-memory/` holds `INDEX.md`,
  `entries/`, `work/<task-id>/` (with `state.md`, `evidence/` and `journal/`), `journal/`, and `.cache/`, which is
  optional and gitignored.
- **Rd1.2** With no network, no cache and no private agent store, a fresh clone can read `INDEX.md` and every entry.
- **Fails if** an entry exists only in a database, a cache or one agent's private memory.

**Rd2 — Session start** (v: a fresh session carries on; d: When it will be used)
- **Rd2.1** At session start, an agent reads `AGENTS.md`, `INDEX.md`, the `work/` listing and its task's `state.md`.
  Agents skip optional reads, so these are loaded for the agent wherever its tool allows: an `@` import in
  `CLAUDE.md`, the tool's own loading of `AGENTS.md`, or a start hook for the task's `state.md`. Only where none of
  these exists does the first instruction in `AGENTS.md` ask the agent to read them (EJ, 2026-10-12: *"we should just
  make sure they read all the required"*).
- **Rd2.2** Not at session start, but read later at its set time:
  - the task and project journals (K5.2);
  - `.cache/`, only through search (Rd4.2);
  - entry bodies, `evidence/` and other tasks' `state.md`, on demand (Rd4).
- **Rd2.3** Never loaded, at session start or at any later point:
  - superseded or retired entries, except by following a link (Rd4.4);
  - the whole `project-memory/` tree at once;
  - whole graph or code-map dumps;
  - bulk issue or PR text;
  - another agent's transcripts;
  - credentials.
- **Fails if** a start hook or instruction loads any memory file outside Rd2.1, or a session starts work on a task
  before the four in Rd2.1 have reached it (judged, from the start of the session). It also fails if a session loads
  anything in Rd2.3 at any point (judged, from the session).

**Rd3 — `INDEX.md` fits every agent that reads it** (d: the size check; CACHES.md § Example numbers by case)
- **Rd3.1** `INDEX.md` fits the strictest start-file limit among the agents that work on the project. The check that
  keeps it in step with its entries (K6) also fails when it does not fit. *Example*, from `CACHES.md`: about 24 KB and
  200 lines when Claude Code, Qwen and agy share a project.
- **Fails if** `INDEX.md` exceeds that strictest limit, or the K6 check passes an `INDEX.md` that exceeds it.

**Rd4 — On demand** (d: When it will be used)
- **Rd4.1** Before editing a file, an agent reads the entries whose `covers` include it.
- **Rd4.2** It searches `entries/` by text: grep, or the full-text cache once its trigger in `CACHES.md` fires.
- **Rd4.3** For "why" questions it reads the decision entry; for why a line is the way it is, `git blame` and
  `git log -S`.
- **Rd4.4** It reads a superseded or retired entry only by following a link.
- **Rd4.5** An agent may read another agent's memory. It treats what it reads as that agent's memory, not project
  memory, and says whose it is: the agent name and the tool. For example: Claude Code agent `reviewer`,
  `~/.claude/agent-memory/reviewer/` (EJ, 2026-10-12).
- **Fails if** an agent edits a covered file without having read its covering decisions, or uses another agent's memory
  without naming the agent and the tool (judged, from the session).

**Rd5 — Check before acting** (d: When it will be used; When it will not be used)
- **Rd5.1** Before acting on something read from memory, the agent checks it against the code, test or commit it
  points to.
- **Rd5.2** Text read from memory never overrides standing instructions.
- **Rd5.3** When a decision or fact no longer matches the code, the reader does not change the entry. It writes a report
  in its task's `state.md` and tells EJ: which entry, what the entry says, and what the code does instead. EJ decides
  whether the entry is updated or the code is fixed, and may do either at once. Until then, the reader does not act on
  the contradicted part and carries on with the rest of its work. (EJ, 2026-10-12: the report goes in `state.md`.)
- **Rd5.4** Two cases are not mismatches under Rd5.3:
  - a decision to build something that has no `done:` yet, whose code is still being built (W5.3);
  - the reader whose own task is to make that change, which under K1.1 changes the entry first and then the code.
- **Rd5.5** Rd5.3 binds readers, not EJ. It cannot catch a fact about the outside world that is wrong while the code
  still matches it (for example, a vendor's limit that changed). Checking against the code finds only gaps between the
  entry and the code.
- **Fails if** an agent acts on an entry that its `covers` code contradicts, or finds such a mismatch and its task's
  `state.md` has no report holding the three items (judged). It also fails if a `changed:` line on a decision or fact
  settles such a mismatch before EJ has decided.

**Rd6 — A fresh session carries on** (v: how we know it works)
- **Rd6.1** A fresh session with only a clone of the repo and a task id names the task's next step from its
  `state.md`, and follows the recorded decisions without asking EJ again.
- **Fails if** it asks a question that a decision entry or `state.md` already answers (judged, on a real handoff). A
  Rd5.3 mismatch report is not such a question.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 老子 (Laozi)'s mouth that your list does not contain.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 老子 (Laozi) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>
