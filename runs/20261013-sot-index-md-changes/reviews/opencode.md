I'll read the brief first.
# INDEX.md changes to the design (opencode)

Read: `SOURCE_OF_TRUTH.md` whole, its vision statements, `docs/index-md/REQUIREMENTS.md` and `DESIGN.md`, and as evidence `tools/memory_index.py`, `.githooks/pre-commit`, `tests/test_memory_index.py`, `docs/index-md/BACKLOG.md` and the limits table in `docs/memory-system/CACHES.md`. Labels: *[EJ]* his words, *[design]* already in the document, *[proposed]* mine.

One thing I found while reading, before any of the five: the merged script and the merged requirements no longer agree about the kinds. It is the "what could go wrong" below, and it touches change 5.

---

## 1. K6.2 and When to write

**Recommend: make it as proposed, and do not repeat the rule three times in the table** — one line after the table carries "any entry, any status", which is what makes the rule true.

**Why.** *[design]* K6.1 says the file "is never edited by hand", and `REQUIREMENTS.md` B3 makes it a pure function of `entries/` (B3.4: "If the result is byte-identical to the existing file, the file is not rewritten"). Once it is a pure result, the only moment it must be rebuilt is any change to any entry — so limiting it to decisions and facts buys nothing and leaves a lesson commit failing the project's own check. And the current wording cannot be carried out as written, because the tool needs the entry `git add`ed first (B1.2: "An untracked entry file is an error that names the file and tells the writer to `git add` it"), so "regenerated right after … is written" names a step that fails on a brand-new file.

**Exact text** — *[proposed]*:

`SOURCE_OF_TRUTH.md:296-297`, K6.2 and its Open line, become one bullet:

> - **K6.2** `INDEX.md` is regenerated and committed whenever any entry is created or changed — any kind, any `status` change — in the same commit as the entry, so the next session sees it. `tools/memory_index.py` builds it and the writer runs it; a committed pre-commit hook and the test suite check that the committed file matches the entries.

The Open line under it goes: it is answered by naming the tool and the checker, which is what K6 left open.

`SOURCE_OF_TRUTH.md:105`, the "Immediately" row of **When to write**, loses its trailing clause:

> | Immediately | Decisions and facts, before the code. A human correction. The state of unfinished work before a handoff, an interruption or a context reduction. |

One line after the table, *[proposed]*:

> **Any change to an entry.** `INDEX.md` is regenerated and committed in the same commit, whatever kind the entry is and whatever `status` it has (K6.2).

`SOURCE_OF_TRUTH.md:117`, **Still open**, drops `(K6)`:

> **Still open:** who resolves a git merge conflict (W6). Whether a changed decision is edited in place or superseded is proposed in K4.3.

**Fails if** *(proposed)* — the K6 check stays and gains one clause, which serves change 2 as well:

> **Fails if** regenerating `INDEX.md` changes it, meaning it was out of step, or it lists a superseded entry as active; or a commit or a merge leaves the committed `INDEX.md` different from what the committed entries build.

Two words I deliberately left out: the order of the commands. W3.6 says an entry links to a procedure and never repeats its steps, so K6.2 states the outcome (regenerated, same commit) and the script's own comment carries the steps.

---

## 2. K6.3, never hand-merge

**Recommend: make it, and narrow W6's Open to the part this work does not answer**, rather than closing it.

**Why.** *[design]* W6 leaves it open: "**Open:** who resolves a merge conflict" (`SOURCE_OF_TRUTH.md:259`), and K6.1 already says "never edited by hand" — which reads as *editing*, not as *choosing between two merged texts*. `docs/index-md/DESIGN.md` "Must not 1" is the reason the rule has teeth: "`union` silently re-adds a superseded entry's line". Once two branches both regenerated, the conflict is not in the index but in the entries, and the rule says so in one line. A merge conflict inside a decision entry is a different question — two writers chose differently, which K4.3 governs — and I will not answer it here.

**Exact text** — *[proposed]*, a new bullet after K6.2:

> - **K6.3** `INDEX.md` is never hand-merged, and never hand-edited to settle a conflict. When it conflicts, the merging writer resolves the entry files first, then regenerates `INDEX.md` and commits it. It merges as ordinary text.

`SOURCE_OF_TRUTH.md:259` becomes:

> - **Open:** who resolves a merge conflict inside an entry. A conflict in `INDEX.md` is settled by regenerating it (K6.3).

**Fails if:** the K6 clause quoted in change 1 — "a commit or a merge leaves the committed `INDEX.md` different from what the committed entries build" — is this requirement's check, and it is the one `REQUIREMENTS.md` G3.2 already has.

Not carried into the memory design: "no merge driver, no `merge=union`". That is a rule about this repo's config and already lives in `DESIGN.md` "Must not 1" and `VISION.md`. A mechanism that is not needed should not be written down as a rule against one.

---

## 3. Rd3.1, who checks the size

**Recommend: make it, and add one clause that says the number is still the design's example** — otherwise the requirement claims a strictest limit that nothing measures.

**Why.** *[design]* This repo has no build step; `REQUIREMENTS.md` C2 says so in its own heading: "**C2 — Tests** (r opencode 15, agy 3–4; replaces 'the build checks it' in Rd3.1)". And the check that exists runs two places, not one: `.githooks/pre-commit` and `tests/test_memory_index.py`, the latter being the guarantee — `REQUIREMENTS.md` G2.3: "The hook is a convenience, not the guarantee … the tests (C2) catch what it misses". The added clause is not tidying: `tools/memory_index.py:35-36` holds `MAX_LINES = 200`, `MAX_BYTES = 24_000`, whose comment says "These two numbers are the design's example, not a measurement", and the strictest reading in `CACHES.md` for agy is "12,000 characters in other reports" — a lower bar in a different unit that the check cannot see.

**Exact text** — *[proposed]*:

`SOURCE_OF_TRUTH.md:180`:

> `INDEX.md` must fit the strictest start-file limit of the agents that read it, and the script checks it; the tests run that check (Rd3).

`SOURCE_OF_TRUTH.md:332-333`, Rd3.1:

> - **Rd3.1** `INDEX.md` fits the strictest start-file limit among the agents that work on the project. `tools/memory_index.py --check` checks it, and `tests/test_memory_index.py` runs that check, so a committed index that does not fit fails the suite; a committed pre-commit hook checks it too. *Example*, from `CACHES.md`: about 24 KB and 200 lines when Claude Code, Qwen and agy share a project. The two constants the script compares against hold that example, not a measurement; the real values come from measuring the readers' load paths (`REQUIREMENTS.md` B4.1, open).

**Fails if** *[proposed]* — the existing check is kept, with the way it is caught:

> - **Fails if** `INDEX.md` exceeds that strictest limit, or the check passes an index that does. Nothing is ever cut, dropped or shortened to fit (B4.3).

---

## 4. W1.1, the id

**Recommend: make the uniqueness rule, leave the form open as proposed, and add one property the brief did not ask for — the id must not change when the entry is edited.**

**Why.** *[design]* The id is in the file name (`SOURCE_OF_TRUTH.md:194`, `project-memory/entries/<prefix>-<id>-<slug>.md`) and K4.3 proposes that a refined decision is edited in place. A form derived from the content — a hash of the claim, say — would then move the file name on every edit, which is the one thing K4.3 does not allow. The uniqueness rule itself is `REQUIREMENTS.md` G4.1, which is already requirement, not open: "It is never 'the next free number'".

**Exact text** — *[proposed]*, added to W1.1 after "An entry's kind, and so its prefix, never changes":

> An entry's `id` is unique across branches without coordination: never "the next free number", and never a value another writer may also pick. It does not change when the entry is edited, so the file keeps its name. *Proposed form, open for EJ* (`REQUIREMENTS.md` G4.1): the date it was written plus a short random suffix, for example `20261013-k3f7` — sortable, quotable, and two writers in the same second still differ.

**Fails if** *[proposed]* — added to W1's check:

> It also fails if two entries share an `id` (the script checks this), or if an entry's `id` changed while its file kept its name (judged).

---

## 5. W1.2 and W1.3, the format

**Recommend: make it as proposed, but fix the format only as far as the generator reads it**, and note that the `**Why:**` spelling is already correct in the design — the rule is what is missing, not the letters.

**Why.** *[design]* The design already writes the exact bytes the script looks for: `SOURCE_OF_TRUTH.md:202` reads "then **Why:**, then **How to apply:**", and `tools/memory_index.py:53` is `WHY = "**Why:**"` — the same eight characters. So a writer following this design today already produces a parseable entry; what the design never says is that the claim *ends* at the first such line, or how the header is delimited. The scope limit matters because the design has fields the generator ignores (`covers`, `changed:`, `done:`) with no agreed shape: `tools/memory_index.py:97-117` reads only `id`, `kind` and `status`, skipping indented lines and unknown keys. Writing a schema for `changed:` would invent a format nothing checks.

**Exact text** — *[proposed]*, W1.2 gains:

> *Proposed format:* the header starts on line 1 with `---` and ends at the next line that is exactly `---`. Inside it each field is a top-level `key: value` line, and a value may be wrapped in one pair of quotes. The index generator reads only `id`, `kind` and `status`; every other key is that entry's own text under that key and is left alone.

W1.3 gains:

> *Proposed format:* the claim is everything after the header up to the first line that starts with `**Why:**`. Blank lines are dropped and runs of whitespace become one space, which is how the claim reads on the index line.

**Fails if** *[proposed]* — added to W1's check:

> It also fails if the generator cannot read the header or find the claim — for example a `**Why:**` line that begins with a space, or written `**Why**:`.

---

## What could go wrong

The kind list is now six in the tool and five everywhere else, so change 5's text would be false in this repo and the check would not say so. `tools/memory_index.py:42-51` lists `ENTRY_NAME = re.compile(r"[DFLROH]-[^/]+\.md")` and `"R": "runbook"`; `tests/test_memory_index.py:405` asserts that `R-runbook.md` with `kind: runbook` gets an index line. The latest commit, `0c19b18` ("No runbooks: a procedure is a script or a `docs/` page", "Five prefixes D/F/L/O/H"), changed `REQUIREMENTS.md` B1.1 to `^[DFLOH]-` and B2.4 to the five kinds, and left the script and its tests at six. So `R-deploy.md`, `kind: runbook`, `status: active`, with a `**Why:**` and a claim, passes `--check`, gets a line in `INDEX.md`, and the only thing that fails is `W1.1`'s "prefix is one letter per kind" — which nothing mechanical checks. Write W1.2's "kind is one of the five" and drop `R` from the script and its test in the same change, or the design says one thing and the check enforces another.

Second, smaller, and not fixed by anything above: `INDEX.md` at 200 lines and 24,000 bytes can exceed agy's "12,000 characters" reading of its own rule, and the check measures bytes. Until someone measures the readers' load paths (B4.1, open), the size requirement is enforced against a number nobody chose.

## Questions for EJ

1. **The id form** — my W1.1 text leaves it open and proposes "date plus a short random suffix" (`20261013-k3f7`). If you would rather have something else, or rather have no example at all until it is used, tell me and the sentence changes. Do not leave it undecided for long: two writers will otherwise both pick the obvious thing.
2. **May the memory design name this repo's scripts?** My K6.2 and Rd3.1 name `tools/memory_index.py`, `.githooks/pre-commit` and `tests/test_memory_index.py`, which would be the first concrete script paths in `SOURCE_OF_TRUTH.md` — today it names only files the design itself owns (`AGENTS.md`, `state.md`, `project-memory/`), and W3.6 says "`AGENTS.md` names the project's scripts, one line each". If the design should stay free of repo mechanisms, both sentences become "regenerated and committed with the entry; `AGENTS.md` names what generates it" and "the script checks it and the test suite runs that check", with the names living only in `AGENTS.md` and `docs/index-md/`.
