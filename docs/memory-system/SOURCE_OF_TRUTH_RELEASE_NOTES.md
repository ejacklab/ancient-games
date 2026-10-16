# Source-of-Truth Memory Design — release notes

The history of `SOURCE_OF_TRUTH.md`: what changed, when, and who decided. The design itself holds only the product,
so an agent reading it carries no history it does not need (EJ, 2026-10-14). Newest first. The notes up to
2026-10-13 are the design's former status block and inline attributions, moved here unchanged.

## 2026-10-16

- **W3.6: when a procedure is a script, and who decides.** A procedure lives as a script with an external check;
  where a step cannot be a command with a checkable result (a person's action, or a choice that depends on judging
  what was seen) it is a page in `docs/` that names that step and calls scripts for the rest. The agent writing the
  procedure decides by trying the script first; the project owner decides if it is contested. Its `fails_if` adds a
  page that names no unscriptable step. `who_decides` was `unassigned`. Wording: Dave's, from one round of the four
  experts and Dave (`runs/20261016-w36-procedure-script/experts/compare.md`; all five agreed "not always" and on who
  decides); EJ: *"Yes apply them"*.
- **W3.6: a script that waits for a person is still a script** (an approval, a typed confirmation). The page is for an
  action a script cannot do or wait for, or a choice that depends on judging what was seen. EJ: *"Yes, a script
  paused still a script"*.

## 2026-10-15

Leftovers of the review, fixed in run `runs/20261015-sot-leftovers/` (EJ: *"fix the item 10 leftovers with a proper
designed workflows"*; decisions picked by EJ from the COO's options):
- **K4.3:** after its first commit an entry's `covers` may be corrected in place, with a `changed:` line, for example
  after a file is renamed; `source` and `depends_on` still change only by superseding the entry.
- **W6.3a:** a merge keeps every `covers` path either side wrote.
- **Rd3.1a:** the project owner decides which agents work on the project, and so the strictest `INDEX.md` limit;
  until the project owner records measured limits, the tool holds the example in Rd3.1b.
- **The kit:** the YAML's paths are relative to its own folder, and the design, the YAML, `CACHES.md` and
  `vision-statements/` travel together.
- **W6.3b** names `reviewer` as its check, as K6.3b does; a typo in the prose's "When to write" table.
- **From the blind review of these fixes:** a merge conflict in an entry is never in its claim, only in its `covers`
  and its added lines (W6.3a and the prose); the YAML's `kit` key says which paths are relative to its folder, which
  to the repository root, and which are the project's own; Rd3.1a states the interim limit itself, 200 lines and
  24,000 bytes, instead of only pointing at the guidance example.
- **From the review of those repairs:** a merge conflict can also sit in `status` and the links (W6.3a and the
  prose); a `covers` correction is not a mismatch under Rd5.3 (K4.3); Rd3.1a's `fails_if` names the interim numbers,
  and `how_to_read` says they hold only until the limit is measured.

Earlier the same day:

Fixes from the four experts' review of the finished design (`runs/20261015-sot-final-review/experts/compare.md`;
EJ: *"yes apply 1-5, project owner reviews"*):
- **Retiring without a replacement.** K4.1: a `superseded` entry links to what replaced it; a `retired` entry, which
  nothing replaces, gives its reason in its `changed:` line. Before, every retired entry needed a `superseded_by` link
  (4 of 5 experts; 老子 would keep the link).
- **Superseding, spelled out.** K1.1 says changing a claim means superseding the entry, and names the steps
  (5 of 5).
- **What a failed MUST stops:** what its `fails_if` names (the entry, the commit, the load or the action); the rest
  of the work goes on unless it depends on that (4 of 5).
- **W1.2:** "each field is one `key: value` line" moved from W1.2a (MUST) to W1.2b (SHOULD), where the indented
  multi-value layout is; W1.2a keeps only the `---` lines.
- **Smaller:** a skipped SHOULD's reason is written in the task's `state.md` (with no task, the commit message); the
  secret scanner is marked as not existing yet; where the prose and the YAML differ, the YAML's level governs; a
  split requirement has no text of its own, its clauses are the requirement.
- **Who reviews:** the project owner reviews the judged checks (`check: reviewer`), or names someone who does (EJ).

## 2026-10-14

- **Requirements moved to `SOURCE_OF_TRUTH_REQUIREMENTS.yaml`.** The design keeps its prose and points to the YAML
  (EJ: *"we can have this doc point to a YAML file"*; *"yes 1 and 2"*). Layout from the four experts' review
  (`runs/20261014-sot-yaml-review/experts/compare.md`): a requirement holding clauses at different levels is split
  into clause records (W1.1a, W1.1b, …; `part_of` names the requirement); every record has one `level`, its own
  `fails_if`, a `check` (tool, git, reviewer, secret scanner, none), `who_decides`, and `links` taken from its text.
  64 records from the 46 requirements. Levels: the four experts' two rounds, EJ's id-form MUST, the COO's six
  (`runs/20261014-sot-must-should/round2/compare.md`).
- **Wording new in the YAML** (not moved from the Markdown; written by the COO):
  - `fails_if` for the requirements no group check covered: W5.2, W6.1a, K5.1, Rd1.1, Rd5.2.
  - A SHOULD's `fails_if` ends "with no written reason", and the header says a SHOULD fails only when skipped without
    one. This settles the group checks that failed a SHOULD (W1, W2, W4, K1).
  - W1.2 is split: the `---` header lines are MUST (the tool fails an entry without them); the field layout and the
    key list stay SHOULD.
  - W1.1b adds "No two entries share an id" from W1's check. Rd5.3 names Rd5.4's two cases, and its check lets them
    pass. Rd2.3b's check lets a superseded entry reached by a link pass.
  - `who_decides`: the project owner on W4.1c, W5.3b, W6.3a and Rd5.3; the agent doing the read on K5.2; the
    project's workflow on K1.1; `unassigned` on W3.6 (whether a procedure can be a script) and Rd3.1a (which agents
    work on the project).
- **"EJ" became "the project owner".** The design is for any project (EJ: *"use project owner"*). The design's "Who
  it is for" defines the role. "There are no owners" became "Entries have no owners".

- **History moved out of the design.** The status block, the revision notes, the dated "(EJ, …)" attributions and
  quotes, and the note on K2 and K3 moved here. Two orphan phrases were dropped: "EJ decides the questions listed as
  not decided" (there is no such list) and "*proposed* marks wording EJ has not decided" (nothing is proposed). EJ:
  *"I don't think we should have those logs or status at the starting of the file … then you can create another
  release note"*.
- **K6.3's Fails if.** The tool now checks an entry for conflict-marker lines (`docs/index-md/` B2.7), so "that part
  is judged, because the tool does not check for markers" became "In an entry, the tool's check catches it
  (`docs/index-md/` B2.7); in `INDEX.md`, the comparison in K6.2 does." Run `runs/20261014-memory-index-cleanup/`;
  merged by EJ (*"merge into master and push"*).

## 2026-10-13

- **Runbooks removed (item 8).** The runbook kind and the `R-` prefix are removed. A procedure lives in the repo as a
  script, or as a page in `docs/` where it cannot be a script, and `AGENTS.md` names the project's scripts. An entry
  links to a procedure and never repeats its steps (EJ: *"it is weird to have script inside the memory, if we buidlign
  a script should be a project already"*; readers' round `runs/20261012-sot-item8-runbooks/`). W3.6: "A script is
  project work, not memory" (EJ, 2026-10-13).
- **Prefixes (item 9).** `O-` observation and `H-` hypothesis are confirmed, so each of the five kinds has one prefix
  letter that matches its `kind`. A changed kind becomes a new entry that supersedes the old one, so a file's prefix
  never changes (EJ: *"a changed kind becomes a new superseding entry"*; readers' round
  `runs/20261013-sot-item9-prefixes/`). W1.1.
- **From the `INDEX.md` work.** `INDEX.md` is regenerated after any entry change and committed with it, and is never
  hand-merged (K6.2, K6.3); the size is part of that one check (Rd3.1); an entry id is `DD-MM-xxxxxx-YYYY` (W1.1; EJ:
  *"id form yes DD-MM-"random 6 digit + char " - YYYY"*); the header and section format is fixed (W1.2, W1.3). The
  design names the tool, in K6 only, and the header keys `recorded` and `source` (EJ: *"the design can suggest the
  name and user accept"*). A claim is never rewritten: a changed claim is a new superseding entry (K4.3), so whoever
  merges keeps both sides of a conflict in an entry and nobody chooses between claims (W6.3; EJ: *"yes write the first
  one, impact later"*). Two entries that each supersede the same entry are reported as in Rd5.3 (W6.3). An impact level
  for entries is left for later. Readers' round: `runs/20261013-sot-index-md-changes/`.

## 2026-10-12

- **Accepted.** EJ: *"yes I accept the source of truth design"*, with its vision and its Write / Keep / Read
  requirements. Vision: `vision-statements/source-of-truth-memory-vision-statements.md`.
- **Core requirements confirmed.** EJ, on reading them: *"this is amazing and a lot easy to read"*, taken as
  confirmation. Grouped by what happens to a memory (EJ: *"yes go ahead with write keep read"*).
- **Drift check and background subagent removed** (EJ: *"ok remove both and update the doc"*). K2 (the drift-check
  script) and K3 (the background subagent) were removed; their numbers are not reused, because other text cites
  K4–K6. A mismatch between a decision and the code is now caught when the decision is read (Rd5). A decision to
  build something is started when it is written and complete when its time, result and test results are added (EJ).
  Whoever reads a decision or fact checks it against the code before acting on it, and reports a mismatch in the
  task's `state.md`.
- **W5.3 and Rd5.3–Rd5.5 refined** after a four-reader round (`runs/20261012-sot-w53-rd53-read/`; EJ: *"state.md for
  the report, apply all the proposed fixes"*). Rd5.3: the report goes in `state.md` (EJ). W4.1's exception for Rd5.3
  (EJ). W5.3's Fails if for `done:` (EJ).
- **Memory by scope (item 7).** Memory has four scopes: task, project, agent and user (EJ). Task and project memory
  keep a journal; agent and user memory keep none (K5.1, EJ). A task's journal is `work/<task-id>/journal/` (EJ:
  *"create task folder, the subfolder inside"*). An agent may read another agent's memory if it knows and says whose
  it is (Rd4.5; EJ: *"agent can read another agent memory but they must know that is another agent memory, what agent
  what tools"*). Rd2.2 is split into "not at session start" (Rd2.2) and "never" (Rd2.3), after a four-reader round
  (`runs/20261012-sot-item7-scopes/`).
- **Session start** (Rd2.1; EJ: *"we should just make sure they read all the required"*). **The journal read** (K5.2;
  EJ: no separate milestones, the start and the end already cover them).
- **Revised with EJ** from the first version, written on 2026-10-11 by `opencode` from
  `runs/20261011-project-memory-engines/RECOMMENDATION.md`. Sources, citations and review history:
  `runs/20261011-source-of-truth-design/` (the full annotated version is `DESIGN-detailed-2026-10-12.md`) and
  `runs/20261012-memory-update-timing/notes.md`.

## Where the design differs from the recommendation — EJ's decisions

No owners and no human approval gate (anyone may change any entry, and every change is logged); decisions and facts
come before the code; a *fact* means a constraint the code must respect, not something discovered afterwards; no
drift-check script and no background subagent.

## Not proven

The timing split (what is written immediately and what later) is design judgement, not measured. Where the
recommendation's engines disagreed (session-start reads, one file per writer, SQLite, how often to write), this design
follows the majority.
