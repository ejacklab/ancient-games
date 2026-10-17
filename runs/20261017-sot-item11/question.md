# Five open points in the memory design's requirements: decide each

The source-of-truth memory design is three files in `docs/memory-system/`: the prose `SOURCE_OF_TRUTH.md`, the
requirements `SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, and release notes. A review left five open points. For **each** of
A–E, give your choice and one or two sentences of wording if it changes the design. Do not invent numbers: a limit is
a comparison or a measured value with its source (the owner's rule, *recall*: house memory "comparisons, not
numbers").

## A. A merge, and a path one side removed

**Fact** (*read*: the YAML, record W6.3a, level MUST): *"Whoever does the merge keeps both sides: both `changed:`
lines, both links, and every `covers` path either side wrote."* Its `fails_if`: *"a merged entry is missing a
`changed:` line, link or `covers` path that one side added"*. **Fact** (*read*: record K4.3): after its first commit
an entry's `covers` *"may also be corrected, for example after a file is renamed, with a `changed:` line"*.
**Question:** if one branch removed or replaced a stale path and the other did not touch it, does the merge keep the
removal, or bring the stale path back? Which wording?

## B. What the kit carries

**Fact** (*read*: the YAML, key `kit`): *"These files travel together as one kit: SOURCE_OF_TRUTH.md, this file,
CACHES.md and vision-statements/ … `tools/` and `docs/index-md/` are relative to the repository root."* **Fact**
(*read*: the YAML, key `checks`): `tool` means *"tools/memory_index.py, in write mode or with --check, fails it"*;
about a dozen records use `check: tool`, and K6.2 names the tool and `docs/index-md/` (its requirements and design).
**Question:** should the kit include the tool and `docs/index-md/`, or should the design say the tool is installed
separately (and what a project without it does)?

## C. Where the measured limit is recorded

**Fact** (*read*: record Rd3.1a, MUST, `check: tool`): *"`INDEX.md` fits the strictest start-file limit among the
agents that work on the project. … Until the project owner records measured limits, the tool's limit is the example in
Rd3.1b: 200 lines and 24,000 bytes."* `who_decides`: the project owner (which agents work on the project). **Fact**
(*read*: `tools/memory_index.py:35-36`): `MAX_LINES = 200`, `MAX_BYTES = 24_000`, commented as "the design's example,
not a measurement". **Fact** (*read*: `docs/index-md/REQUIREMENTS.md` B4.1): the values "come from measuring the
readers' load paths. Until then they hold the design's example". So the numbers sit in three places: Rd3.1a, Rd3.1b
and the tool. **Question:** where, and in what form, does the project owner record the agents and their limits so the
tool can read them and a reviewer can see when the interim example stops applying? (For example a section of
`AGENTS.md`, a small config file, or the tool's constants — say which and why.)

## D. Which agents count

**Fact** (*read*: the YAML, group Rd3 title): *"`INDEX.md` fits every agent that reads it"*; the prose
(`SOURCE_OF_TRUTH.md:157`): *"the strictest start-file limit of the agents that read it"*. Record Rd3.1a: *"among the
agents that work on the project"*. **Question:** which set is right — agents that read `INDEX.md` at session start, or
all agents that work on the project — and which wording?

## E. Build the tool change, and measure the limits?

**Fact** (*read*: `docs/memory-system/CACHES.md`, table "The index read at session start", lines 489–497): documented
start-file limits per engine — Claude Code `MEMORY.md` "first 200 lines … or the first 25KB" (W-1); Codex `AGENTS.md`
up to 32 KiB (`project_doc_max_bytes`, W-2); agy 24,000 bytes per rule file and a 20,000-token budget, or 12,000
characters in other reports (W-4, a conflict); opencode no limit stated; dsh a 65,536-byte budget; Qwen Code 200 lines
or 25,000 bytes. The research below re-checks these. **Question:** should the tool be changed to read the limits from
where C records them (a code change with tests, in its own run), and should the limits be measured on the engines
(not only read from docs) — now, later, or not at all?

The research for this question is added below by the workflow before you are asked.
