# Six experts — five decisions to finish the source-of-truth memory design (D1–D5)

Question: `runs/20261018-sot-finish/research/s1.question.md`. Answers: `runs/20261018-sot-finish/s1b/<expert>/answers/<expert>.md`.
All six answers are usable. This file compares; it picks no winner and decides nothing. The main agent decides
(time-boxed run, method 3.8 item 14). Five engines answering one brief still share the brief, so a count below is
not a vote of independent evidence (*my reading*, per the six-experts skill).

Labels: *quoted* = the expert's own words; *my reading* = the comparer's summary or inference; *not measured* = no
one ran it.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| D1 path, format | `project-memory/start-file-limits.json`, JSON | `project-memory/start-limits.json`, JSON | `project-memory/limits.json`, JSON | `project-memory/start-limits.txt`, `key: value` line blocks | `project-memory/start-limits.json`, JSON | `project-memory/index-limits.json`, JSON |
| D1 row grain | one per agent, nested `limits` | one per agent and unit | one per agent, nested `limits` | one per agent and unit | one per limit | one per agent and unit |
| D2 when the example stops | only when every reader in the inventory has a valid record | row by row (measured or documented) | row by row, by `basis` | row by row; the file existing does not end it | the file is the switch: present, its rows alone apply | the file is the switch, as a whole |
| D3 both sides change one `covers` path | keep both new paths, old removed, both `changed:` records; no report named | keep every path; report in `state.md` and to the owner | keep both, old removed, both `changed:`; report in `state.md` | keep both, choose neither; report in `state.md` and to the owner | keep both, old removed; report in `state.md` and to the owner | keep both, old removed, both `changed:`; explicitly **no** separate `state.md` report |
| D4 secret scanner | **(b)** adopt `detect-secrets`, keep the reviewer | **(a)** fixed prefixes, no waiver | **(a)** fixed prefixes, `secret-scan:allow` waiver counted | **(c) now**, (a) later if a real credential is found | **(a)** fixed prefixes, no waiver at the start | **(a)** fixed prefixes, `secret-scan:allow` waiver |
| D5 agy measurement | now | later, on a trigger | now, one run with a control | later, on a trigger | now, in S5 (unless the owner says no project loads agy) | now, if agy can be called in this run |
| Main items used | #1 #2 #5 #7 #9 #13 #17 #18 | #1 #2 #3 #4 #5 #7 #9 #10 #11 #14 #18 | #1 #2 #3 #4 #5 #6 #8 #9 #16 #17 #19 | #1 #2 #3 #4 #6 #7 #8 #10 #12 #15 #16 #18 #19 | #1 #2 #3 #4 #5 #6 #7 #8 #9 #10 | — |
| Insights cited | — | — | — | — | `runs/20261016-four-experts-what-counts-as-change/insight.md#F-d8221199`, `#F-21e1586c`; `runs/20261016-integrate-r11-r13/insight.md#F-d8a49e5a` | — |

Every table cell is *my reading* of the answer's own Answer section; the quoted words are below.

## Where they agree

- **D1, place: the project's own `project-memory/`, beside `INDEX.md` — 6 of 6.** *my reading.* Reasons quoted:
  范蠡 "A file in the design's folder would travel with the kit into every project and carry another project's
  agents"; Dave "a file in `docs/memory-system/` would travel with the kit and carry one project's agents into the
  next project"; 老子 "a file in the kit would carry another project's numbers into this one". The file names
  differ (four different names, see the table); no one argued over the name (*my reading*).
- **D1, fields:** every answer has `agent`, a limit value, `unit`, `basis` (`measured` / `documented` / `example`)
  and `source` (*my reading*). Linus and 孫子 add an engine `version`; Linus and 范蠡 add `load_path`.
- **D1, YAML is out — 6 of 6.** *my reading.* Dave dropped his own last-round YAML vote: *quoted* "last round I
  chose YAML for this file and never said how the tool would parse it. The research shows it cannot without
  PyYAML. I drop it."
- **D2, a missing file → the Rd3.1b example applies and the run says so — 6 of 6.** *my reading.*
- **D2, a file that does not parse fails; never a silent fallback — 6 of 6.** *my reading.* E.g. 老子 *quoted*
  "a file the tool cannot parse, or a row missing `limit`, `unit` or `basis`, is an **error** — never a silent
  fallback."
- **D2, the tool cannot see an agent the file does not name** — 范蠡, 孫子, 老子, Dave, Dario say so in those
  terms (*my reading*). Dave *quoted*: "'Only when every agent has a row' therefore cannot be checked by the tool."
- **D1/D2, check mode reads the limits file from the same snapshot as the entries, not the working tree** —
  Linus, 范蠡, 孫子, Dave, Dario (*my reading*); 老子 assumed the same and asked (question 6 below).
- **D1/D2, a `tokens` row is printed "not checked", never passed** — 范蠡, 孫子, Dario, and 老子 for any unit the
  tool cannot count (*my reading*). Dave instead makes any unit outside `lines`/`bytes`/`characters`/`utf16_units`
  fail the check (*quoted* "Any other unit fails the check").
- **D3, keep both new paths and keep the old path removed — 6 of 6.** *my reading.* All six say W6.3a's existing
  "every `covers` path either side wrote" already implies it. "Keep the path that exists in the repository" was
  chosen by no one; 范蠡 and Dave *quoted* "The tool never reads `covers`" / "The tool does not read `covers` at
  all" (both ran a grep; the comparer's re-run: 0 matches for `covers` in `tools/memory_index.py`).
- **D4, if a built-in check is made, it is fixed-prefix only: no entropy, no generic-api-key, no JWT** — 范蠡,
  孫子, 老子 (for the later check), Dave, Dario (*my reading*). Reason quoted by 孫子: "A knowledge repository cites
  commit ids and UUIDs, which are exactly what an entropy rule flags".
- **D4, the reviewer stays the check for passwords, prefix-less tokens and personal data — 6 of 6.** *my reading.*
- **D4, the report names file, line and rule, never the matched value** — 孫子, Dave, Dario (*my reading*); the
  others do not address it.
- **D5, if measured: agy only, sentinels at known offsets, a control file whose failure voids the run, repeat
  runs, a multi-byte file to separate bytes from characters** — all six describe this method in some form (*my
  reading*). No one proposes measuring the other engines now.

## Where they disagree   (side by side, quoted; never averaged)

### D1 — format: JSON (5) or the tool's own line format (1)

- **JSON** — Linus *quoted* "JSON avoids adding a parser dependency"; 孫子 *quoted* "JSON is the only standard data
  format the standard library parses at the repository's declared floor of Python 3.10 (`pyproject.toml:5`)"
  (the comparer read `pyproject.toml:5`: `requires-python = ">=3.10"`); 范蠡, Dave and Dario likewise, with an
  `object_pairs_hook` that rejects a repeated key.
- **Line format, `.txt`** — 老子 *quoted* "the tool already reads `key: value` lines and strips one pair of quotes
  (`tools/memory_index.py:104-131`), so the line format costs nothing new; JSON and TOML would each add a parser".
  He names his own cost: *quoted* "A hand-rolled `key: value` reader has no schema, no type errors and no version
  field … If EJ prefers a documented format, JSON is the one the standard library reads."
- On TOML: Dario *quoted* "TOML is my second choice" (if the floor were 3.11+); 孫子 *quoted* "it would raise the
  kit's floor to 3.11 or need a fallback parser, and nothing in this run authorises that."

### D1 — row grain: one row per agent (2) or per agent and unit / per limit (4)

- **Per agent, nested limits** — 孫子 *quoted* "One row per agent, not per limit, so a duplicated `agent` is a
  mistake the parser rejects"; Linus: each reader record "contains `agent`, `engine_version`, `load_path`, and
  `limits`".
- **Per agent and unit** — Dario *quoted* "One row per agent would force a choice between them"; 范蠡 *quoted* "A
  row covers one agent and one unit … the tool compares each row against one count in one unit without
  converting"; 老子 and Dave the same (*my reading*).
- *my reading*: the two sides' reasons do not meet — 孫子's nested `limits` list also avoids a forced choice, and
  the per-unit rows lose the duplicate-agent check. Not resolved by either side.

### D2 — when the example stops: three positions

- **Complete coverage (Linus)** — *quoted* "Replace that fallback only when every reader in the owner's inventory
  has a valid record with enforceable constraints. … Missing reader records … are errors". *my reading*: he
  treats the file as an inventory the tool checks against, which the others say the tool cannot do.
- **Row by row (范蠡, 孫子, 老子)** — 范蠡 *quoted* "Waiting until every agent has a row would let one unknown agent
  block a known limit"; 孫子 *quoted* "the harm of the global switch is an unbounded index when the file is
  partial; the harm of row-by-row is a stale example on one row, which is visible and bounded"; 老子 *quoted*
  "the file existing is not enough, the number being real is" (he changed his last-round position).
- **The file is the switch (Dave, Dario)** — Dario *quoted* "The example is two constants (lines and bytes), not
  per-agent values, so there is no clean way to say which row replaces which constant"; Dave *quoted* "File
  present: its rows alone apply." Dario names his own cost: *quoted* "A partial file drops the example's
  24,000-byte limit without warning. Only the printed rows show it."

Sub-points that also differ:
- **An agent with no row** — Linus: an error (*quoted* above); 范蠡: *quoted* "An agent left out of the file is
  the reviewer's finding"; 孫子: *quoted* "it is not in the owner's declaration, so no limit applies"; 老子:
  *quoted* "an agent with no row, holds the Rd3.1b example for that agent" (*my reading*: this sits next to his
  own "the tool cannot know the set of agents", so it is unclear how the tool would apply it); Dave: *quoted*
  "the project owner catches this, not the tool"; Dario: not checkable by the tool.
- **An empty file / empty list** — 孫子 *quoted* "An empty `agents` list is a valid declaration of no readers and
  must be printed loudly, not treated as malformed"; Dave *quoted* "a file with no rows fails. Otherwise it would
  switch the size check off with no sign"; Dario and Linus: no rows / empty inventory fails.
- **Does a `documented` row end the example?** — 范蠡, 孫子, 老子: yes for that agent; Dave and Dario: any row in a
  present file applies; Linus: documented values apply only with complete coverage, and *quoted* "Reading a
  documented limit does not make it measured." 范蠡 and 孫子 both send this to the owner (question 2 below).

### D3 — report the clash in `state.md`, or not

- **Report (范蠡, 孫子, 老子, Dave)** — Dave *quoted* "whoever does the merge reports it in the task's `state.md`
  and to the project owner, as in Rd5.3."
- **No separate report (Dario)** — *quoted* "No separate `state.md` report. Both `changed:` lines already show the
  divergence, and a kept path that no longer exists is an ordinary stale-path finding."
- **Not named (Linus)** — his wording keeps both and both `changed:` records and *quoted* "avoids … creating a new
  approval gate"; he does not mention `state.md` (*my reading*).
- Dario's premise "an ordinary stale-path finding" — he asks whether any check fails a dead `covers` path
  (question 11); 范蠡 and Dave found the tool never reads `covers` (*my reading*: so no tool check exists today).

### D4 — (a) 4, (b) 1, (c)-then-(a) 1; and the waiver

- **(b) Linus** — *quoted* "Maintaining credential detectors is a separate responsibility from generating an
  index. … `tools/memory_index.py` remains standard-library-only." He keeps `check:` as is and *quoted* "Until
  installation and integration are verified, describe the check as reviewer-only".
- **(a) 范蠡, 孫子, Dave, Dario** — 孫子 *quoted* "a scan inside the tool runs on every commit that touches
  `project-memory/` with no install and no second hook"; Dave *quoted* "The difference is when it is caught, not
  how much: the measured count of real secrets today is zero either way."
- **(c) now, (a) on a trigger — 老子** — *quoted* "building a secret scanner now, inside a six-hour run, to satisfy
  a MUST whose check is already resolved, is gripping a thing that cannot be gripped"; and *quoted* "Building the
  gate before its false-positive rate is measured is the expensive stage."
- **Waiver** — none: 范蠡 (*quoted* "A match is never waived"), Dave (*quoted* "There is no waiver: an entry that
  quotes an example writes it shortened"); a line waiver: 孫子 (`secret-scan:allow`, counted in the report), Dario
  (`secret-scan:allow`; *quoted* "All three outside tools have a line waiver, so a quoted example needs one here
  too"), 老子 (`# pragma: allowlist secret`, in the later check).
- **W3.2's `check:` wording** — keep "secret scanner; reviewer": Linus, 范蠡, 孫子, 老子; change to *quoted*
  "`check: tool (known token formats); reviewer (everything else)`": Dario; Dave changes only the `checks` text
  (*my reading*).

### D5 — now (4, two of them conditional) or later on a trigger (2)

- **Now** — Linus *quoted* "The run needs evidence about the installed loader"; 孫子 *quoted* "measure agy now, one
  run, because its number is the design's number" (`MAX_BYTES = 24_000` is agy's documented figure); Dave: now,
  *quoted* "if the owner says agy loads `INDEX.md` in no planned project, skip it until one does"; Dario: now,
  *quoted* "only if agy can be called in this run".
- **Later, on a trigger** — 范蠡 *quoted* "no `INDEX.md` exists yet … A measurement now decides nothing" and "a
  measurement holds for one installed agy version. Measured years before it matters, it may no longer hold by
  then"; 老子 *quoted* "The time has not come: there is no `INDEX.md`". Their triggers: 范蠡, the limits file names
  agy and that `INDEX.md` exceeds the lowest agy figure; 老子, a real `INDEX.md` passes 12,000 characters with agy
  a declared reader.
- *my reading*: the two sides share the fact that no `project-memory/` exists (the comparer re-ran `ls`: no such
  directory); they differ on whether the design's own 24,000-byte constant is reason enough to measure now.

## What each added that the others did not

- **Linus** — a `scope` field per limit and *quoted* "A combined startup budget includes the other startup
  material"; the measurement caveat *quoted* "failure to recall does not by itself prove truncation"; a
  requirement-check table that fails W3.2 on weak words (*quoted* "W3.2's sensitive-data scope remains unspecified
  beyond credentials").
- **范蠡** — found three texts that disagree on when the example ends (YAML `how_to_read`, B4.1 "Until then",
  Rd3.1a "Until the tool reads that file") and gives words to align all three (*my reading* of his item 9); a row
  with `basis: example` carries no `limit`; a falsifiable test of his own no-waiver default (*quoted* "If false
  positives come first and outnumber the catches, the no-waiver default is wrong").
- **孫子** — the Python floor from `pyproject.toml:5` (`>=3.10`, re-read by the comparer); `agy --version` → 1.4.0
  (*quoted*, ran by him; the comparer confirmed only that `agy` is on PATH); an optional `files` field for a
  combined start load; a `date` field; draft C3.1–C3.4 requirements for the scan; the scan should also stop
  write mode, so a credential is not copied into `INDEX.md` (question 7).
- **老子** — the tool's existing `key: value` reader as the format; the limits file must not be inside `INDEX.md`
  or any start file *quoted* "or the limit would spend the budget it describes"; a pattern change: *quoted* "An
  interim value carries an ending — who ends it, and what ending" and "A piece not yet due records the trigger
  that makes it due, not a date".
- **Dave** — the only one who measured anything for D4: *quoted* "This repo's Markdown that `.gitignore` does not
  exclude: 1 hit. It is AWS's documented example key … That is a false positive"; "The 48 house memory notes: 0
  hits" (ran by him; *not measured* by the comparer). The comparer confirmed the line he cites
  (`runs/20261018-sot-finish/s1/dario/answers/dario.md:60`) quotes the AWS example key. A second control for D5:
  *quoted* "One random token placed in no file must *not* be reported"; a written prediction before the engine
  call; the hook runs only when `project-memory/` is staged, so the limits file belongs there; tests build
  key-shaped strings at run time so the public repo holds no literal key.
- **Dario** — `journal/` may hold pasted secrets more than `entries/` (question 4); random tokens every 500 bytes,
  three or more repeats; the house-rule caveat *quoted* "By house rules it should not change the design on n=1
  alone."

## What they need to know   (the questions, merged, each with its options)

1. **Which agents load `INDEX.md` at session start, and by which path, in the first project that adopts the kit?**
   (Linus, 范蠡, 孫子 Q1 and Q3, Dave, Dario Q5.)
   - agy is among them → D5's trigger is live / measure on that path;
   - agy is not → D5 becomes "not until it is";
   - the set is empty → 孫子: a valid `{"agents": []}` printed loudly; Dave, Dario, Linus: a file with no rows fails.
2. **Does a `documented` row end the example, or only a `measured` one?** (范蠡 Q1, 孫子 Q2; Linus's D2 position.)
   - documented ends it for that agent (范蠡, 孫子, 老子 as written);
   - only measured ends it (every row holds the example until measured; D5 becomes the only way out for agy).
3. **What does W3.2's "sensitive data" cover beyond credentials?** (Linus.)
   - credentials only (the scan's scope);
   - also personal data and other sensitive data, judged by the reviewer.
4. **Is `journal/` in scope for W3.2's scan, or `entries/` only?** (Dario Q2.)
   - `entries/` only (the `checks` key's current text);
   - `entries/` and `journal/`.
5. **What is the lowest Python version the tool and hook must run on?** (Dario Q1; 孫子 cites `pyproject.toml:5`
   `>=3.10`, which the comparer re-read.)
   - 3.10 (as declared) → JSON;
   - 3.11+ guaranteed → TOML with comments becomes possible.
6. **In `--check <rev>`, is the limits file read from that rev or from the working tree?** (老子 Q2; Linus, 范蠡,
   孫子, Dave, Dario already wrote "from the same snapshot".)
   - from the rev / staging area;
   - from the working tree.
7. **Should the secret scan stop write mode as well as `--check`?** (孫子 Q4; 范蠡 and Dave already write "in write
   mode or with --check".)
   - both modes;
   - `--check` only.
8. **Which units must the tool fail on, and must a reader with a larger limit (e.g. dsh, 65,536 bytes) still pass
   the example until its row is measured?** (老子 Q1.)
   - fail on every unit the tool can count; others "not checked";
   - only lines and bytes;
   - and separately: a larger-limit reader holds the example until measured / its documented row applies.
9. **Are rows keyed by agent alone, or by agent and unit?** (老子 Q3; the D1 row-grain disagreement.)
   - one row per agent with a nested `limits` list (Linus, 孫子);
   - one row per agent and unit (范蠡, 老子, Dave, Dario).
10. **Is agy callable here, and can it expose startup-loader evidence?** (Linus Q3, Dario Q3.) 孫子 *quoted*
    "agy 1.4.0 is installed here (`agy --version`, ran)"; the comparer confirmed only `which agy` →
    `~/.local/bin/agy`.
    - callable, loader evidence available → exact limit;
    - callable, sentinel recall only → behavioural bounds (Linus);
    - not callable → measure later, row stays `documented` / `example` (Dario).
11. **Does any check fail a `covers` path that no longer exists?** (Dario Q4.) 范蠡 and Dave report the tool never
    reads `covers`; the comparer's grep agrees (0 matches). Options:
    - no check exists → Dario's "ordinary stale-path finding" has no checker today;
    - add one (no expert proposed it).
12. **If `INDEX.md` moves out of `project-memory/`, does D1's path move with it?** (老子 Q4.)
    - yes, the limits file follows `INDEX.md`;
    - no.

## Check

- **Check results** (from the workflow's task text): linus pass, fan-li pass, sun-tzu pass, lao-tzu pass, dave
  pass, dario pass; all six usable. No expert is missing an answer.
- **Engines** (from each `status.json`, *quoted* fields):
  - Linus — `codex`, `gpt-6.1-sol`, exit 0, 158 s.
  - 范蠡 — `claude`, `claude-opus-5-5`, exit 0, 324 s; **fallback**: `fallback_from: "agy"`, `fallback_reason:
    "task needs web"`.
  - 孫子 — `dsh`, `deepseek-flash (dsh headless profile)`, exit 0, 278 s.
  - 老子 — `opencode`, `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, exit 0, 105.6 s. Its answer file opens
    with a stray line "I'll read the brief first." before the heading (*my reading*: harmless noise).
  - Dave — `claude`, `claude-opus-5-5`, exit 0, 438 s.
  - Dario — `claude`, `claude-sonnet-5-5`, exit 0, 136 s.
  - *my reading*: with 范蠡's fallback, three of the six answers come from Claude models (范蠡, Dave on Opus; Dario
    on Sonnet), so they are less independent than six engines would be.
- **What the check does not establish.** The check script was written by Claude. It does not establish that an
  expert applied its rules correctly, that a cited item number says what the expert claims, or that the
  research's external facts are true. "Check pass" means the answer was usable and its citations had the expected
  form, nothing more (*my reading*).
- **What the comparer re-ran** (2026-10-18): `pyproject.toml:5` reads `requires-python = ">=3.10"`; `grep -c
  covers tools/memory_index.py` → 0; `which agy` → `~/.local/bin/agy`; `ls project-memory` → no such directory;
  `dario.md:60` (s1) quotes the AWS example key. *not measured* by the comparer: Dave's ripgrep counts, 孫子's
  `agy --version`, and anything about agy's real start-file limit.
