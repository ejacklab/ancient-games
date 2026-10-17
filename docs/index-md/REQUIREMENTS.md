# INDEX.md generator — requirements

> **Status: draft, under review with EJ.** Written 2026-10-12 by the COO (Claude `claude-opus-5-5`). The builder
> builds against this version; a requirement marked *open* is not built until EJ settles it.
>
> **Sources.** Each requirement names one:
> - **(d)** `docs/memory-system/SOURCE_OF_TRUTH.md`, accepted by EJ;
> - **(p)** the proposal `runs/20261012-index-md-algorithm/proposals/claude.md`, by step;
> - **(r)** a fix from the blind reviews in `runs/20261012-index-md-algorithm/reviews/`, with the reviewer and problem
>   number;
> - **(v)** `VISION.md`.
>
> *Proposed* marks wording EJ has not decided. Every requirement has a **Fails if** check that some case breaks. There
> are no fixed numbers: where a limit applies, measurement decides it.
>
> **Categories (proposed):** **B — Build** (what goes in and what comes out), **C — Check** (how anyone tells the file
> is right), **G — Git** (when it runs, and how branches meet).

## B — Build: from entries to `INDEX.md`

**B1 — What it reads** (p step 1; r opencode 3, codex 7)
- **B1.1** Only files directly in `project-memory/entries/` whose name matches `^[DFLOH]-[^/]+\.md$`. No subfolders,
  no dotfiles, not `INDEX.md`. The five prefixes are those of W1.1.
- **B1.2** Write mode reads the working-tree content of the entry files git knows about (tracked or staged). An
  untracked entry file is an error that names the file and tells the writer to `git add` it.
- **B1.3** Check mode reads git objects only: the staging area by default, or a commit with `--check <rev>`. Paths
  are listed with `-z` and read through one `git cat-file --batch` call.
- **Fails if** an untracked entry gets a line, a file outside B1.1 gets a line, or a path with a space or a non-ASCII
  character is read wrongly in either mode.

**B2 — What it parses** (p steps 3–4; r opencode 5, 6, 8, 9; agy 6, 7)
- **B2.1** The header starts on line 1 with `---` and ends at the next line that is exactly `---`. Inside it, read
  only top-level `id:`, `kind:` and `status:` as `key: value`, stripping whitespace and surrounding quotes. The format
  is W1.2's.
- **B2.2** The claim is the body after the header, up to the first line that starts with `**Why:**`. Blank lines are
  dropped and runs of whitespace become one space. The spelling `**Why:**` is W1.3's.
- **B2.3** Every entry must have a readable header with an `id` in W1.1's form, `DD-MM-xxxxxx-YYYY` (two
  digits, two digits, six lowercase letters or digits, four digits), and a `status` of `active`, `superseded` or
  `retired`. No two entries share an `id`.
- **B2.4** An **active** entry must also have: a `kind` from the five (decision, fact, lesson, observation,
  hypothesis); a file prefix that matches its `kind`; a `**Why:**` line; and a non-empty claim.
- **B2.5** A problem in an inactive entry beyond B2.3, B2.7 and B2.8 is a warning, not an error, so one old entry cannot
  block every memory commit.
- **B2.6** A file that is not valid UTF-8 is reported as `<file>: <problem>`, not as a crash.
- **B2.7** No entry holds a line that starts with `<<<<<<<` or `>>>>>>>`, a git conflict marker (SoT K6.3). It is an
  error in every status.
- **B2.8** No entry holds a known credential (SoT W3.2). A known credential is text that matches one of these
  fixed-prefix forms: an AWS access key id (`AKIA`, `ASIA`, `ABIA` or `ACCA`, then 16 of `A`–`Z` and `2`–`7`); a
  `-----BEGIN … PRIVATE KEY-----` line followed by a key body of 64 or more characters before its `-----END` line; a
  GitHub token (`ghp_`, `gho_`, `ghu_`, `ghs_` or `ghr_`, then 36 letters or digits; or `github_pat_` then 82 letters,
  digits or `_`); a GitLab token (`glpat-` then 20 letters, digits, `-` or `_`); a Slack token (`xoxb-`, `xoxp-` or
  `xoxe-`, then a run of digits); an Anthropic key (`sk-ant-api03-`); a Google API key (`AIza` then 35 letters,
  digits, `-` or `_`). It is an error in every status, in both modes, reported as `<file>: possible credential
  (<kind>) on line <n>`, without printing the matched text. There is no entropy or keyword rule and no waiver: an
  example key in an entry is shortened so it no longer matches. Everything else W3.2 covers stays the reviewer's.
- **Fails if** a malformed active entry gets a line, a prefix/kind mismatch passes, a duplicate id passes, a retired
  entry broken beyond B2.3, B2.7 and B2.8 stops the build, or any input ends in a traceback; an id not in W1.1's form
  passes, an entry with a conflict-marker line passes, or an entry holding a known credential passes, or a report
  prints the matched credential.

**B3 — What it writes** (p steps 2, 5, 6; r codex 6, opencode 7, agy 8)
- **B3.1** One line per active entry, sorted by file name in code-point order:
  `- [<id>](entries/<percent-encoded file name>) <kind>: <claim>`. Superseded and retired entries get no line.
- **B3.2** A fixed head: the title `# Project memory index`, then a comment saying the file is generated, must not be
  edited, and naming the command that rebuilds it. With no active entries, the list is the line `(no active entries)`.
- **B3.3** UTF-8, LF line endings, one newline at the end. No date, time, count, host name or locale-dependent order.
- **B3.4** If the result is byte-identical to the existing file, the file is not rewritten. A missing `INDEX.md` is
  written.
- **Fails if** two runs over the same entries, on two machines or with two locales, give different bytes; a
  superseded entry gets a line; or a file name with a space or `#` gives a link that does not resolve.

**B4 — Size** (d Rd3.1; p steps 7–8, 14; r agy 2, opencode 13, 16, codex 10–12)
- **B4.1** The index must fit the strictest start-file limit of the agents whose session start loads it (SoT Rd3.1a).
  The project owner records those limits in `project-memory/start-limits.json`: a JSON object whose `limits` is a
  list of rows, one per agent and unit, each with `agent` (a name), `unit` (`lines`, `bytes` or `characters`),
  `limit` (a whole number above 0), `basis` (`measured`, `documented` or `example`) and `source` (where the figure
  comes from). For each unit, the smallest `limit` among its rows applies; a unit with no row keeps the example.
  With no file, the script uses the example: `MAX_LINES` (200) and `MAX_BYTES` (24,000), constants marked in the code
  as the design's example. Lines are counted as now, bytes as UTF-8 bytes, characters as Unicode code points.
- **B4.2** Every run prints the size against each limit that applies, as `INDEX.md: <lines>/<l> lines, <bytes>/<b>
  bytes` followed by `, <characters>/<c> characters` when a `characters` limit applies, and on the next line where the
  limits came from: `limits: project-memory/start-limits.json` or `limits: the design's example (no
  project-memory/start-limits.json)`.
- **B4.5** A limits file that is not valid UTF-8 JSON, or is not an object with a non-empty `limits` list, or has a
  row missing a field, a field of the wrong type, an unknown `unit` or `basis`, or a `limit` that is not a whole number
  above 0, is an error in both modes, reported as `project-memory/start-limits.json: <problem>`; nothing is written
  and the script never falls back to the example silently. In check mode the file is read from the same snapshot as
  the entries (the staging area, or the commit named), never from the working tree.
- **B4.3** Nothing is ever cut to fit. Over the limit, write mode still writes the whole file, prints a warning and
  exits 0. Check mode fails.
- **B4.4** Any change that brings the index back under the limit makes the check pass. No approval is needed (d W4.1).
- **Fails if** a line is dropped or shortened to fit; `--check` passes an index over any limit that applies; a row
  in the limits file is ignored, or a bad limits file passes or falls back to the example; or check mode reads the
  limits file from the working tree.

## C — Check: how anyone tells the file is right

**C1 — The check mode** (d K6; p step 9)
- **C1.1** `python3 tools/memory_index.py --check [<rev>]` rebuilds the index from the snapshot (B1.3) and compares it
  byte for byte with the snapshot's `INDEX.md`.
- **C1.2** It passes (exit 0) only when the entries are valid, the bytes are equal, and the size is within the limits.
  Otherwise it exits 1, says what failed, prints a unified diff when the bytes differ, and prints the fix: stage the
  entries, run the script, stage `INDEX.md`.
- **C1.3** A snapshot with no `project-memory/`, or an unborn `HEAD`, passes with "nothing to check".
- **C1.4** It writes nothing.
- **Fails if** a hand edit to `INDEX.md` passes, a stale `INDEX.md` passes, or check mode changes any file.

**C2 — Tests** (r opencode 15, agy 3–4; replaces "the build checks it" in Rd3.1)
- **C2.1** `tests/test_memory_index.py` runs under the repo's `pytest`
  (`env -u NO_COLOR python3 -m pytest -q`).
- **C2.2** It holds at least these tests:
  - golden bytes for a fixed set of sample entries;
  - running twice changes nothing;
  - the check rejects a hand-edited `INDEX.md`;
  - the check rejects a superseded entry listed as active;
  - `--check HEAD` passes on this repo itself.
- **Fails if** any of these cases passes when it should fail, or the test file does not run under the repo's `pytest`.

## G — Git: when it runs, and how branches meet

**G1 — Who runs it** (p step 10; d K6.2)
- **G1.1** Whoever creates or changes any entry file runs the script, of every kind and for every status change, and
  commits `INDEX.md` in the same commit as the entry.
- **G1.2** This is written as an instruction where agents read it: `CLAUDE.md` today, because `AGENTS.md` only points
  there (r opencode 11), and `AGENTS.md` after the move in Rd1.1.
- **Fails if** a commit changes an entry and not the `INDEX.md` it implies (caught by C1 at the next check).

**G2 — The hook** (p step 11; r opencode 10, codex 3)
- **G2.1** One committed hook, `.githooks/pre-commit`, runs `--check` when the staged change touches
  `project-memory/` or `tools/memory_index.py`. `.githooks/pre-merge-commit` only calls it.
- **G2.2** It is switched on once per clone with `git config core.hooksPath .githooks`.
- **G2.3** The hook is a convenience, not the guarantee. Rebase, cherry-pick, fast-forward and `--no-verify` skip it;
  the tests (C2) catch what it misses (r codex 1–2, opencode 1–2, agy 3).
- **Fails if** a commit through the hook leaves a wrong `INDEX.md`, or a change to the script alone skips the check.

**G3 — Merging** (p step 13; d W6, K6.3)
- **G3.1** `INDEX.md` merges as normal text. There is no `merge=union`, no `merge=binary` and no custom merge driver.
- **G3.2** When `INDEX.md` conflicts, nobody edits it. Resolve the entry files first, then run the script, stage
  `INDEX.md` and commit.
- **Fails if** a merged `INDEX.md` differs from what the script builds from the merged entries.

**G4 — Ids across branches** (p must-not 5; d W1.1)
- **G4.1** An entry's `id` is unique without coordination between branches. It is never "the next free number". Its
  form is W1.1's: `DD-MM-xxxxxx-YYYY` (EJ, 2026-10-13).
- **G4.2** The script rejects a duplicate id and an id not in W1.1's form (B2.3); it does not choose an id.
- **Fails if** two branches can each create the same id and the clash shows only after a merge.

## Open, for EJ

1. **The categories B / C / G** are proposed.
2. **B4:** which agents and load paths read `INDEX.md`; bytes or characters.

*The design changes these requirements implied in `SOURCE_OF_TRUTH.md` were made on 2026-10-13 (K6.2, K6.3, Rd3.1, W1.1–W1.3; run `runs/20261013-sot-index-md-changes/`).*
