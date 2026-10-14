#!/usr/bin/env python3
"""Build docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml from the records below, then check it.

Written by the COO for run 20261014-sot-yaml-review, after the four experts' review (experts/compare.md) and EJ's
"yes 1 and 2, use project owner". The record text is the Markdown's, split by clause where a requirement held more
than one level; links are taken from the text by pattern, never by hand. Checks: the file loads; every record has the
one shape; ids are unique; every one of the 46 requirement ids is present (whole or as clauses); every link resolves.
What the checks do not establish: that an agent follows the file better than the Markdown (not measured; EJ skipped
the test).

  build_requirements.py OUT.yaml
"""
import re
import sys
import textwrap

import yaml

PO = "project owner"

HEADER = {
    "what": "The requirements of the source-of-truth memory design. The design itself, and why, is "
            "SOURCE_OF_TRUTH.md beside this file.",
    "how_to_read": [
        "Each record is one requirement, or one clause of one (its id ends in a letter, and part_of names the "
        "requirement). Every record has the same keys.",
        "Read level first, then text. When a clause and its requirement seem to differ, text governs.",
        "fails_if is the case that breaks the record. check says who or what finds it.",
        "who_decides names who settles an open choice inside the record; none means the record leaves no choice "
        "open; unassigned means the choice is open and nobody is named yet.",
        "The records are grouped by what happens to a memory: it is written, it is kept true, and it is read.",
        "There are no fixed numbers: where a limit applies, it is a comparison that measurement decides.",
    ],
    "levels": {
        "MUST": "A gate. When it fails, the work it governs stops.",
        "SHOULD": "A default. It may be skipped with a written reason; it fails only when skipped without one.",
        "guidance": "Explanation or advice. Nothing to pass or fail.",
    },
    "checks": {
        "tool": "tools/memory_index.py, in write mode or with --check, fails it.",
        "git": "git history shows it.",
        "reviewer": "a person or agent reading the work judges it. The project owner names who reviews.",
        "secret scanner": "a scanner over entries/ finds it.",
        "none": "guidance: nothing to check.",
    },
    "roles": {
        "project owner": "The person who decides for the project: a mismatch between memory and code, a contested "
                         "supersession, and the open choices named in who_decides.",
    },
    "basis": {
        "v": "the vision, vision-statements/source-of-truth-memory-vision-statements.md",
        "d": "this design's text, SOURCE_OF_TRUTH.md (the section named)",
    },
    "retired_ids": "K2 and K3 are not used. Other text cites K4 to K6, so the numbers stay.",
}


def r(id, level, text, fails_if, check, who_decides="none", part_of=None):
    return {"id": id, "part_of": part_of, "level": level, "text": text, "fails_if": fails_if, "check": check,
            "who_decides": who_decides}


CATEGORIES = [
    ("Write — what goes in, and how", [
        ("W1", "The shape of an entry", "d: What will be put in", [
            r("W1.1a", "MUST", "Each entry is one file. The prefix is one letter per kind (W2): `D-` decision, `F-` "
              "fact, `L-` lesson, `O-` observation and `H-` hypothesis. It matches the entry's `kind`. There is no "
              "runbook prefix (W3.6). An entry's kind, and so its prefix, never changes. A changed kind (a hypothesis "
              "confirmed, an observation that turns out to be a fact) is a new entry that supersedes the old one "
              "(K4.1).",
              "a file's prefix is not one of the five or does not match its `kind`, `kind` holds any other value, or "
              "git shows an entry file renamed to a different prefix.", "tool; git", part_of="W1.1"),
            r("W1.1b", "MUST", "The `id` is `DD-MM-xxxxxx-YYYY`: the day, month and year the entry is written, six "
              "random lowercase letters and digits, for example `13-10-k3f7a2-2026`. Writers on different branches "
              "pick ids without coordinating, so an id is never \"the next free number\". No two entries share an id. "
              "An id never changes, so the file keeps its name.",
              "an id is not in the W1.1 form, two entries share an id, or git shows an entry file renamed to a "
              "different id.", "tool; git", part_of="W1.1"),
            r("W1.1c", "SHOULD", "The file is `project-memory/entries/<prefix>-<id>-<slug>.md`.",
              "an entry file has another folder or name, with no written reason.", "reviewer", part_of="W1.1"),
            r("W1.2a", "MUST", "The header starts on the file's first line, which is exactly `---`, and ends at the "
              "next line that is exactly `---`. Each field is one `key: value` line.",
              "a header is not between two `---` lines.", "tool", part_of="W1.2"),
            r("W1.2b", "SHOULD", "A field with several values (`covers`, the links, `changed:`) holds them on "
              "indented lines below its key. The keys are `id`, `kind`, `status`, `author`, `recorded` (the date "
              "recorded), `covers` (the code paths it is about), `source` (its source or evidence), `depends_on`, "
              "`supersedes`, `superseded_by` and `changed:`. A decision to build something, once its work is "
              "complete, also holds `done:` (W5.3).",
              "a field is missing or laid out otherwise, with no written reason.", "reviewer", part_of="W1.2"),
            r("W1.3a", "MUST", "The body follows the header: the claim, then a line starting with `**Why:**`. There "
              "is one claim per entry.",
              "an active entry has no claim or no `**Why:**` line, or a reviewer finds two claims in one entry.",
              "tool; reviewer", part_of="W1.3"),
            r("W1.3b", "SHOULD", "The claim is one or two sentences. A line starting with `**How to apply:**` follows "
              "the `**Why:**` line.",
              "the claim is longer, or the `**How to apply:**` line is missing or spelled otherwise, with no "
              "written reason.", "reviewer", part_of="W1.3"),
        ]),
        ("W2", "What each kind means", "v; d: What it is for", [
            r("W2.1a", "guidance", "A **decision** is a choice the code must follow, with the reason. A **fact** is a "
              "truth or outside constraint the code must respect, not something discovered afterwards.",
              "nothing: a definition.", "none", part_of="W2.1"),
            r("W2.1b", "SHOULD", "Decisions and facts are requirements: they are written before the code.",
              "a commit changes code under a new decision or fact with no entry in that commit or an earlier one, "
              "with no written reason.", "git", part_of="W2.1"),
            r("W2.2a", "guidance", "A **lesson** comes from a failure or a human correction. An **observation** "
              "records what was seen.", "nothing: a definition.", "none", part_of="W2.2"),
            r("W2.2b", "SHOULD", "A **hypothesis** is a guess, labelled as one.",
              "a guess is recorded under any kind but hypothesis, with no written reason.", "reviewer",
              part_of="W2.2"),
        ]),
        ("W3", "What never goes in", "v; d: What will not be put in", [
            r("W3.1", "SHOULD", "Nothing that can be read directly from the code, the tests or the commit log: what a "
              "function does, which test covers it, what a commit changed. The memory lives in git; the rule is about "
              "what an entry says.", "an entry holds such content, with no written reason.", "reviewer"),
            r("W3.2", "MUST", "No credentials or sensitive data.",
              "an entry holds a credential or sensitive data.", "secret scanner; reviewer"),
            r("W3.3a", "MUST", "Nothing from another agent's private state.",
              "an entry holds another agent's private state.", "reviewer", part_of="W3.3"),
            r("W3.3b", "SHOULD", "No raw transcripts.", "an entry holds a raw transcript, with no written reason.",
              "reviewer", part_of="W3.3"),
            r("W3.4", "SHOULD", "No work described as \"verified\" when it is only implemented.",
              "an entry calls work verified that was only implemented, with no written reason.", "reviewer"),
            r("W3.5a", "MUST", "No user memory (one person, across projects) and no agent memory (one agent name).",
              "the project holds user memory or agent memory.", "reviewer", part_of="W3.5"),
            r("W3.5b", "SHOULD", "User memory and agent memory live in the home folder.",
              "they live elsewhere, with no written reason.", "reviewer", part_of="W3.5"),
            r("W3.6", "SHOULD", "No copy of the project's existing documents (requirements, architecture in `docs/`) "
              "or of its procedures: an entry links to them. A procedure lives in the repo as a script, or as a page "
              "in `docs/` where it cannot be a script, and `AGENTS.md` names each script, one line each. A script is "
              "project work, not memory.",
              "an entry copies a document or a procedure's steps, with no written reason.", "reviewer",
              who_decides="unassigned: whether a procedure can be a script"),
        ]),
        ("W4", "Who writes, and the change log", "v: no owners, every change logged", [
            r("W4.1a", "guidance", "Anyone, agent or person, may create or change any entry, and `AGENTS.md` too. "
              "No entry has an owner, and no change needs approval.", "nothing: a permission.", "none",
              part_of="W4.1"),
            r("W4.1b", "MUST", "`status` is only `active`, `superseded` or `retired`.",
              "an entry's `status` is any other value.", "tool", part_of="W4.1"),
            r("W4.1c", "MUST", "The one exception to W4.1a is Rd5.3: a reader who finds a decision or fact out of step "
              "with the code reports it and does not settle it.",
              "as Rd5.3.", "reviewer", who_decides=PO, part_of="W4.1"),
            r("W4.2", "SHOULD", "Every change to an entry adds one line to its `changed:` log: the time, and who made "
              "it (the model ID for an agent, the name for a person). Earlier lines are never edited.",
              "git shows a change to an entry with no matching `changed:` line, or an earlier line edited, with no "
              "written reason.", "git"),
            r("W4.3", "guidance", "Files that are not entries (`state.md`, `journal/`, `AGENTS.md`) rely on git "
              "history.", "nothing: a statement of where history lives.", "none"),
        ]),
        ("W5", "When to write", "d: When to write", [
            r("W5.1", "SHOULD", "Written immediately: a decision or fact, before the code it governs; a human "
              "correction; and the state of unfinished work, before a handoff, an interruption or a context "
              "reduction.",
              "a commit changes code under a new decision with no entry in that commit or an earlier one, or a "
              "session ends without a human correction it received, with no written reason.", "git; reviewer"),
            r("W5.2", "SHOULD", "Written at the end of a task: other lessons, observations and hypotheses.",
              "a task ends with what it learned unwritten, with no written reason.", "reviewer"),
            r("W5.3a", "SHOULD", "A decision to build something is started when it is written. When the work is "
              "complete, whoever finishes it adds `done:` to the decision: the time, the result in one sentence, and "
              "the test results, or \"no tests\" said plainly. `done:` points to the evidence (`runs/<run-id>/` or the "
              "commit) rather than copying test output (W3.1). A standing rule, such as \"all timestamps are UTC\", "
              "is never complete and never gets `done:`.",
              "a finished task's decision has no `done:`, or a `done:` without a time, a result and test results or "
              "\"no tests\", with no written reason.", "reviewer", part_of="W5.3"),
            r("W5.3b", "MUST", "If the result differs from the decision, that is a mismatch for Rd5.3: it is "
              "reported, not settled in `done:`.",
              "a `done:` line settles a mismatch before the project owner has decided.", "reviewer",
              who_decides=PO, part_of="W5.3"),
        ]),
        ("W6", "Writers do not collide", "d: Changing entries", [
            r("W6.1a", "MUST", "Each new entry gets its own file. Agents never append to one shared file.",
              "an entry file holds more than one entry, or a commit adds an entry to an existing file.",
              "reviewer; git", part_of="W6.1"),
            r("W6.1b", "SHOULD", "Each journal, the task's or the project's, has one file per agent session.",
              "two agent sessions write to one journal file, with no written reason.", "git", part_of="W6.1"),
            r("W6.2", "SHOULD", "Each agent works on its own branch or worktree, so two edits to the same lines meet as "
              "a merge conflict, not a silent overwrite.",
              "an edit to an entry is lost without a conflict, with no written reason.", "git"),
            r("W6.3a", "MUST", "A claim is never rewritten (K4.3), so a merge conflict in an entry is only in the lines "
              "added to it. Whoever does the merge keeps both sides: both `changed:` lines, both links. Nobody "
              "chooses between two claims. Two entries that each supersede the same entry are reported in the task's "
              "`state.md` and to the project owner, as in Rd5.3.",
              "a merged entry is missing a `changed:` line or link that one side added, or two entries superseding "
              "one go unreported.", "git; reviewer", who_decides=PO, part_of="W6.3"),
            r("W6.3b", "SHOULD", "A conflict in `INDEX.md` is resolved by regenerating it (K6.3).",
              "as K6.3b.", "tool", part_of="W6.3"),
        ]),
    ]),
    ("Keep — memory stays true, and nothing is lost", [
        ("K1", "The decision or fact first, then the code", "v; d: What it is for", [
            r("K1.1", "SHOULD", "To change behaviour that a decision or fact governs, change the entry first, then the "
              "code. Work that has to go the other way is a matter for the project's workflow, not for memory.",
              "git shows a commit changing the behaviour a decision or fact governs, with no change to that entry in "
              "the same commit or an earlier one, with no written reason.", "git; reviewer",
              who_decides="the project's workflow: when work goes the other way"),
        ]),
        ("K4", "Never deleted, never expired by age", "v: nothing lost; d: What will not be put in", [
            r("K4.1", "MUST", "An entry is never deleted. It is marked `superseded` or `retired`, links to what "
              "replaced it (`superseded_by`), and keeps its old body.",
              "git shows an entry file deleted, or a `superseded` or `retired` entry with no link.", "git"),
            r("K4.2", "guidance", "Age alone never expires an entry. An entry is found out of date only when someone "
              "reads it and checks it against the code (Rd5).", "nothing: why there is no expiry.", "none"),
            r("K4.3", "MUST", "An entry's claim is never rewritten. A changed claim is a new entry that supersedes the "
              "old one. After an entry is first committed, it only gains a `changed:` line, a new `status`, the "
              "`superseded_by` link, and `done:` on a decision to build something (W5.3). This also keeps merge "
              "conflicts out of claims (W6.3).",
              "git shows an entry's claim changed after its first commit.", "git"),
        ]),
        ("K5", "The journal becomes entries", "v: nothing lost between sessions", [
            r("K5.1", "SHOULD", "Task and project memory each keep a journal: a task's in `work/<task-id>/journal/`, "
              "the project's in `journal/` for work not tied to a task. Both hold raw notes, one file per agent "
              "session, appended to and never edited. Agent and user memory keep no journal under this design.",
              "a journal file is edited after it is written, or raw notes are kept elsewhere, with no written "
              "reason.", "git"),
            r("K5.2", "SHOULD", "At the end of a task, and before a handoff or session end, an agent reads its task's "
              "journal (or the project journal) written since the last read, writes what is worth keeping as entries, "
              "and logs that read in the task's `state.md`. A session cut off before it can read loses nothing: the "
              "next read covers it.",
              "a task's `state.md` shows it complete or handed off with no journal-read log line, with no written "
              "reason.", "reviewer", who_decides="the agent doing the read: what is worth keeping"),
        ]),
        ("K6", "`INDEX.md` stays in step", "d: Where it is put; When to write", [
            r("K6.1a", "MUST", "`INDEX.md` is generated from `entries/`: one line per active entry, showing its id, "
              "kind and one-line claim.",
              "a commit's `INDEX.md` differs from what the tool builds from that commit's entries, or lists a "
              "superseded or retired entry as active.", "tool", part_of="K6.1"),
            r("K6.1b", "SHOULD", "`INDEX.md` is never edited by hand.",
              "`INDEX.md` is edited by hand, with no written reason.", "reviewer", part_of="K6.1"),
            r("K6.2", "MUST", "Whenever an entry is created or changed (any kind, any status change), `INDEX.md` is "
              "regenerated and committed in the same commit as the entry, so the next session, on any clone, sees it. "
              "`tools/memory_index.py` builds it; its `--check [<rev>]` compares the `INDEX.md` in the staging area, "
              "or in a commit, with what it builds from the entries there. Its requirements and design are in "
              "`docs/index-md/`.",
              "a commit's `INDEX.md` differs from what the tool builds from that commit's entries.", "tool"),
            r("K6.3a", "MUST", "When a merge conflicts, resolve the entry files first, with no conflict markers left "
              "in them.",
              "an entry holds a git conflict-marker line (`<<<<<<<` or `>>>>>>>`). In `INDEX.md`, the comparison in "
              "K6.2 catches it.", "tool", part_of="K6.3"),
            r("K6.3b", "SHOULD", "`INDEX.md` is never merged by hand: after the entry files, regenerate it and commit "
              "it with them.", "`INDEX.md` is merged by hand, with no written reason.", "reviewer", part_of="K6.3"),
        ]),
    ]),
    ("Read — the right memory reaches the agent at the right time", [
        ("Rd1", "Where it lives, and readable from a clone alone", "v: plain files; never a database or service", [
            r("Rd1.1", "SHOULD", "`AGENTS.md` sits at the repo root (`CLAUDE.md` only imports it). `project-memory/` "
              "holds `INDEX.md`, `entries/`, `work/<task-id>/` (with `state.md`, `evidence/` and `journal/`), "
              "`journal/`, and `.cache/`, which is optional and gitignored.",
              "these live elsewhere or are laid out otherwise, with no written reason.", "reviewer"),
            r("Rd1.2", "MUST", "With no network, no cache and no private agent store, a fresh clone can read "
              "`INDEX.md` and every entry.",
              "an entry exists only in a database, a cache or one agent's private memory.", "reviewer"),
        ]),
        ("Rd2", "Session start", "v: a fresh session carries on; d: When it will be used", [
            r("Rd2.1", "SHOULD", "At session start, an agent reads `AGENTS.md`, `INDEX.md`, the `work/` listing and "
              "its task's `state.md`. Agents skip optional reads, so these are loaded for the agent wherever its tool "
              "allows: an `@` import in `CLAUDE.md`, the tool's own loading of `AGENTS.md`, or a start hook for the "
              "task's `state.md`. Only where none of these exists does the first instruction in `AGENTS.md` ask the "
              "agent to read them.",
              "a start hook or instruction loads any memory file outside these four, or a session starts work on a "
              "task before the four have reached it, with no written reason.", "reviewer"),
            r("Rd2.2", "SHOULD", "Not at session start, but read later at its set time: the task and project journals "
              "(K5.2); `.cache/`, only through search (Rd4.2); entry bodies, `evidence/` and other tasks' `state.md`, "
              "on demand (Rd4).",
              "a session loads one of these at its start, with no written reason.", "reviewer"),
            r("Rd2.3a", "MUST", "Never loaded, at session start or at any later point: credentials; another agent's "
              "transcripts.", "a session loads either, at any point.", "reviewer", part_of="Rd2.3"),
            r("Rd2.3b", "SHOULD", "Never loaded, at session start or at any later point: superseded or retired "
              "entries, except by following a link (Rd4.4); the whole `project-memory/` tree at once; whole graph or "
              "code-map dumps; bulk issue or PR text.",
              "a session loads one of these, with no written reason. Following a link to a superseded or retired "
              "entry passes.", "reviewer", part_of="Rd2.3"),
        ]),
        ("Rd3", "`INDEX.md` fits every agent that reads it", "d: the size check; CACHES.md § Example numbers by case", [
            r("Rd3.1a", "MUST", "`INDEX.md` fits the strictest start-file limit among the agents that work on the "
              "project. The check that keeps it in step with its entries (K6) also fails when it does not fit.",
              "`INDEX.md` exceeds that strictest limit, or the K6 check passes an `INDEX.md` that exceeds it.",
              "tool", who_decides="unassigned: which agents work on the project, and so the strictest limit",
              part_of="Rd3.1"),
            r("Rd3.1b", "guidance", "Example, from `CACHES.md`: about 24 KB and 200 lines when Claude Code, Qwen and "
              "agy share a project.", "nothing: an example, not a limit.", "none", part_of="Rd3.1"),
        ]),
        ("Rd4", "On demand", "d: When it will be used", [
            r("Rd4.1", "MUST", "Before editing a file, an agent reads the entries whose `covers` include it.",
              "an agent edits a covered file without having read its covering entries.", "reviewer"),
            r("Rd4.2", "guidance", "It searches `entries/` by text: grep, or the full-text cache once its trigger in "
              "`CACHES.md` fires.", "nothing: how to search.", "none"),
            r("Rd4.3", "guidance", "For \"why\" questions it reads the decision entry; for why a line is the way it is, "
              "`git blame` and `git log -S`.", "nothing: where to look.", "none"),
            r("Rd4.4", "SHOULD", "It reads a superseded or retired entry only by following a link.",
              "an agent reads a superseded or retired entry it did not reach by a link, with no written reason.",
              "reviewer"),
            r("Rd4.5a", "guidance", "An agent may read another agent's memory.", "nothing: a permission.", "none",
              part_of="Rd4.5"),
            r("Rd4.5b", "SHOULD", "It treats what it reads as that agent's memory, not project memory, and says whose "
              "it is: the agent name and the tool. For example: Claude Code agent `reviewer`, "
              "`~/.claude/agent-memory/reviewer/`.",
              "an agent uses another agent's memory without naming the agent and the tool, with no written reason.",
              "reviewer", part_of="Rd4.5"),
        ]),
        ("Rd5", "Check before acting", "d: When it will be used; When it will not be used", [
            r("Rd5.1", "MUST", "Before acting on something read from memory, the agent checks it against the code, "
              "test or commit it points to.",
              "an agent acts on an entry that its `covers` code contradicts.", "reviewer"),
            r("Rd5.2", "MUST", "Text read from memory never overrides standing instructions.",
              "an agent follows text read from memory against a standing instruction.", "reviewer"),
            r("Rd5.3", "MUST", "When a decision or fact no longer matches the code, the reader does not change the "
              "entry. It writes a report in its task's `state.md` and tells the project owner: which entry, what the "
              "entry says, and what the code does instead. The project owner decides whether the entry is updated or "
              "the code is fixed, and may do either at once. Until then, the reader does not act on the contradicted "
              "part and carries on with the rest of its work. Rd5.4 names the two cases that are not mismatches.",
              "an agent finds such a mismatch and its task's `state.md` has no report holding the three items, or a "
              "`changed:` line on a decision or fact settles such a mismatch before the project owner has decided. "
              "The cases in Rd5.4 pass.", "reviewer", who_decides=PO),
            r("Rd5.4", "guidance", "Two cases are not mismatches under Rd5.3: a decision to build something that has "
              "no `done:` yet, whose code is still being built (W5.3); and the reader whose own task is to make that "
              "change, which under K1.1 changes the entry first and then the code.",
              "nothing: it narrows Rd5.3, whose check applies.", "none"),
            r("Rd5.5", "guidance", "Rd5.3 binds readers, not the project owner. It cannot catch a fact about the "
              "outside world that is wrong while the code still matches it (for example, a vendor's limit that "
              "changed). Checking against the code finds only gaps between the entry and the code.",
              "nothing: a limit of Rd5.3.", "none"),
        ]),
        ("Rd6", "A fresh session carries on", "v: how we know it works", [
            r("Rd6.1", "MUST", "A fresh session with only a clone of the repo and a task id names the task's next step "
              "from its `state.md`, and follows the recorded decisions without asking the project owner again.",
              "it asks a question that a decision entry or `state.md` already answers, on a real handoff. A Rd5.3 "
              "mismatch report is not such a question.", "reviewer"),
        ]),
    ]),
]

ORIGINAL_IDS = ("W1.1 W1.2 W1.3 W2.1 W2.2 W3.1 W3.2 W3.3 W3.4 W3.5 W3.6 W4.1 W4.2 W4.3 W5.1 W5.2 W5.3 W6.1 W6.2 "
                "W6.3 K1.1 K4.1 K4.2 K4.3 K5.1 K5.2 K6.1 K6.2 K6.3 Rd1.1 Rd1.2 Rd2.1 Rd2.2 Rd2.3 Rd3.1 Rd4.1 Rd4.2 "
                "Rd4.3 Rd4.4 Rd4.5 Rd5.1 Rd5.2 Rd5.3 Rd5.4 Rd5.5 Rd6.1").split()
REF = re.compile(r"\b((?:W|K|Rd)\d(?:\.\d[a-c]?)?)\b")
LEVELS = {"MUST", "SHOULD", "guidance"}
CHECKS = {"tool", "git", "reviewer", "secret scanner", "none"}


def links(rec, known):
    found = []
    for ref in REF.findall(rec["text"] + " " + rec["fails_if"]):
        if ref in (rec["id"], rec["part_of"]) or ref in found:
            continue
        found.append(ref)
    bad = [x for x in found if x not in known]
    assert not bad, (rec["id"], bad)
    return found


def block(key, text, pad):
    lines = textwrap.wrap(text, 118 - len(pad) - 2, break_long_words=False, break_on_hyphens=False)
    return [f"{pad}{key}: >-"] + [f"{pad}  {line}" for line in lines]


def plain(value):
    return yaml.safe_dump(value, width=1000, allow_unicode=True).strip().removesuffix("\n...")


def emit():
    recs = [x for _, groups in CATEGORIES for _, _, _, rs in groups for x in rs]
    ids = [x["id"] for x in recs]
    assert len(ids) == len(set(ids)), "duplicate id"
    group_ids = [g for _, groups in CATEGORIES for g, _, _, _ in groups]
    known = set(ids) | set(ORIGINAL_IDS) | set(group_ids)
    covered = {x["part_of"] or x["id"] for x in recs}
    assert covered == set(ORIGINAL_IDS), set(ORIGINAL_IDS) ^ covered
    out = ["# Source-of-Truth Memory — requirements", ""]
    for key, value in HEADER.items():
        if isinstance(value, str):
            out += block(key, value, "")
        elif isinstance(value, list):
            out.append(f"{key}:")
            for item in value:
                lines = textwrap.wrap(item, 114, break_long_words=False, break_on_hyphens=False)
                out.append(f"  - >-")
                out += [f"    {line}" for line in lines]
        else:
            out.append(f"{key}:")
            for k, v in value.items():
                out += block(plain(k), v, "  ")
        out.append("")
    out.append("categories:")
    for title, groups in CATEGORIES:
        out += [f"  - title: {plain(title)}", "    groups:"]
        for gid, gtitle, basis, rs in groups:
            out += [f"      - id: {gid}", f"        title: {plain(gtitle)}", f"        basis: {plain(basis)}",
                    "        requirements:"]
            for x in rs:
                assert x["level"] in LEVELS, x["id"]
                assert all(c.strip() in CHECKS for c in x["check"].split(";")), x["id"]
                assert (x["check"] == "none") == (x["level"] == "guidance"), x["id"]
                out.append(f"          - id: {x['id']}")
                out.append(f"            part_of: {x['part_of'] or 'none'}")
                out.append(f"            level: {x['level']}")
                out += block("text", x["text"], "            ")
                out += block("fails_if", x["fails_if"], "            ")
                out.append(f"            check: {x['check']}")
                out.append(f"            who_decides: {plain(x['who_decides'])}")
                ls = links(x, known)
                out.append(f"            links: [{', '.join(ls)}]")
    return "\n".join(out) + "\n", len(recs)


def main():
    text, n = emit()
    open(sys.argv[1], "w", encoding="utf-8").write(text)
    data = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
    keys = {"id", "part_of", "level", "text", "fails_if", "check", "who_decides", "links"}
    recs = [x for c in data["categories"] for g in c["groups"] for x in g["requirements"]]
    assert all(set(x) == keys for x in recs), "one shape"
    assert all(isinstance(x["level"], str) for x in recs), "level is one word"
    print(f"{n} records from 46 requirements; loads; one shape; ids unique; all 46 covered; links resolve")


main()
