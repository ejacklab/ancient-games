# 孫子 (Sun Tzu) — which memory checks can be built, and how

## Answer
Build v1 as a thin, read-only TypeScript layer that can give a final mechanical verdict on only 9 of the 20 `tool`/`git` records — delegate the index and entry-format side to `tools/memory_index.py --check`, own the git-history checks, let 4 split MUSTs fail but never pass without a person, and treat the 7 `tool`/`git` SHOULDs as signals, because their "written reason" escape is not machine-readable. Patch C1, C3, C4 and U2 before code, and keep `CACHES.md` out of mechanical checking until it has levels, a `check` field and a cache schema.

## How I decided

**1. I counted before committing (my #1).** The YAML is 64 records under 46 base ids: 25 MUST, 28 SHOULD, 11 guidance. Twenty records carry `tool` or `git`; the other 44 are 33 `reviewer` and 11 `none`. The "46 requirements" in `SOURCE_OF_TRUTH.md:160` is the base-id count, not the record count C1 asks for (`REQUIREMENTS.md:23-27`). My #1 says the reckoning comes first — 「多算勝，少算不勝，而況於無算乎？」 (quoted, my #1) — and the count already shows the tool cannot honestly promise the whole matrix.

**2. I named each record's ground and matched force to it (my #19, my #14).** The YAML's own level rule changes the arithmetic: a SHOULD fails only when skipped with no written reason, and the reason may live in `state.md` or the commit message (YAML lines 31-33). A tool can find the signal but cannot read every possible reason, so a `tool`/`git` SHOULD can only be reported as a signal for a reviewer — never as a final fail. That leaves:

- **9 MUSTs** a tool can settle finally;
- **4 MUSTs** where a mechanical fail is final but a pass still needs a person;
- **7 tool/git SHOULDs** that can only signal;
- **33 reviewer records and 11 guidance records.**

| Record (level) | What the tool can establish | Verdict |
|---|---|---|
| W1.1a MUST | prefix/kind on every file in `entries/`; renamed prefix from git | final, but needs an own scan for files `memory_index.py` ignores |
| W1.1b MUST | id form, duplicate ids; renamed id from git | final |
| W1.2a MUST | header between two `---` lines | final (delegate) |
| W1.3a MUST | claim and `**Why:**` (tool); two claims (person) | can fail; needs reviewer to pass |
| W4.1b MUST | `status` is one of three values | final (delegate) |
| W6.1a MUST | a second header block added to an entry (git signal); two entries in one file (person) | can fail on the signal; needs reviewer to pass |
| W6.3a MUST | merge missing a parent's `changed:` line, link or `covers` path (git signal); unreported double supersession (person) | can fail on the signal; needs reviewer to pass |
| K4.1 MUST | deleted entry (git); missing `superseded_by` (file); retired reason (person) | can fail; needs reviewer to pass |
| K4.3 MUST | claim/`source`/`depends_on` rewritten after first commit; `covers` changed with no `changed:` line | final (own git) |
| K6.1a MUST | `INDEX.md` equals what entries build | final (delegate) |
| K6.2 MUST | the same, at each commit | final (delegate `--check <rev>`) |
| K6.3a MUST | conflict markers in entries | final (delegate) |
| Rd3.1a MUST | index ≤ 200 lines / 24,000 bytes | final (delegate) |
| W2.1b SHOULD | a code commit and an entry in it; not that the decision was "new" | signal → reviewer |
| W4.2 SHOULD | a `changed:` line added per commit; earlier lines untouched; not whether a reason exists | signal → reviewer |
| W5.1 SHOULD | nothing about sessions or human corrections | reviewer |
| W6.1b SHOULD | journals have no session-naming rule | reviewer |
| W6.2 SHOULD | lost edits need branch archaeology | reviewer |
| K1.1 SHOULD | "behaviour governed by a decision" is semantic | reviewer |
| K5.1 SHOULD | journal lines edited (git signal); raw notes elsewhere (person) | signal → reviewer |

This is my reading of the `fails_if` lines with the YAML's level rule applied, not a count of the `check` field. The five records whose `check` says `git` but whose `fails_if` needs judgement — W2.1b, W5.1, W6.1b, W6.2, K1.1 — are all SHOULDs, which is why none can be a mechanical pass.

**3. I put the index and entry-format checks under the tool that already owns them (my #3).** `memory_index.py --check` already covers W1.2a, W4.1b, K6.1a, K6.2, K6.3a and Rd3.1a (`memory_index.py:104-203, 481-508`), and C3 is right that re-implementing it would be worse. But it cannot be the sole checker for all entry-format records:
- Files whose prefix is not one of `[DFLOH]` are not entries to it, so they are never parsed (`memory_index.py:43, 306-313`) — W1.1a's "prefix is not one of the five" is silently passed.
- Kind/prefix problems in a *superseded or retired* entry are downgraded to warnings (`memory_index.py:167-170`), but W1.1a is a MUST for every entry, not only active ones.
- Its output is per-file prose with no record id, and it fails on things no record names ("not known to git", non-UTF-8 filename; `memory_index.py:156-157, 200-202`), so C2/R1's per-id evidence cannot come from it as it stands.
- It stops at the first stage: entry errors mean the index was never compared, and a stale index means the size was never measured (`memory_index.py:495-506`). K6.1a/K6.2/K6.3a/Rd3.1a must then be reported as **not checked**, not as pass or fail.

Either `memory_index.py` gains `--check --json` with record ids and stage information, or C3 must name the ids it delegates and say how "not checked" and unattributed failures are reported. I recommend the JSON contract; the alternative is parsing stderr, which pins the wrapper to prose that can change.

**4. I checked `CACHES.md` on its own ground (my #4).** Its Core requirements have no levels and no `check` field at all (`CACHES.md:310-469`), so C1's "a requirement whose check is tool or git" and R1's "its level" have nothing to read. Of the whole section, only B2.2's `git check-ignore` is fully static (`CACHES.md:379-383`); even its "rebuild adds nothing to `git status`" half needs a rebuild, so it is a signal. B4.1/K1.1/K1.2 need a cache schema the document does not give — it names an FTS5 table with `kind` and `covers`, but no table name or hash/model-id columns (`CACHES.md:196, 391-412`) — so a checker would hard-code the cache implementation. Rd1.1 is a grep-level sign at best. B1.1/B1.2/B2.1/B3.1/B5.1/K2/K3/Rd2/Rd3.2-3.5 are benchmarks, runtime fallbacks or EJ's recorded decision. In v1, CACHES is reviewer/runtime; B2.2 is a signal.

**5. I refused the checks that cannot see their target (my #13, my #10).** I will not build a check whose evidence is a reviewer's judgement but whose result says "pass", and I will not edit the kit to relabel W2.1b/W5.1/K1.1 (AGENTS.md `memory_check/AGENTS.md:6-8` says report, not fix). 「君命有所不受。」 (quoted, my #13) — a command that cannot produce a verdict is not accepted. The price is a report that looks mostly "needs reviewer"; the alternative is a clean-looking report with no evidence.

**6. I wrote the harm column before the benefit column (my #6).** These are the four docs' problems that would make the tool give a wrong answer or promise a check that cannot be built — 「不盡知用兵之害者，則不能盡知用兵之利也。」 (quoted, my #6):

| Where | What is wrong | What to write instead |
|---|---|---|
| C1 + R1 (`REQUIREMENTS.md:23-27, 44-47`) | CACHES has no `level` or `check`; most of its `Fails if` lines are runtime/benchmark. C1 also makes every tool/git SHOULD a tool verdict, but a SHOULD may be skipped with a reason (YAML:31-33). | Give CACHES levels and checks or exclude it from v1; say a tool/git SHOULD can only signal; state the record basis (64 records / 46 ids). |
| C3 (`REQUIREMENTS.md:32-35`) | `--check` prints prose, not ids; it ignores non-`[DFLOH]` files and only warns about kind/prefix in inactive entries; it fails on things no record names; it stops before the index/size stage on an earlier error. | `--check --json` with record ids and stage, or name the delegated ids and add a "not checked" result for the stages it never reached. |
| U2 (`USE_CASES.md:15-20`) | "exactly that requirement" is impossible with a generated index: a broken entry cannot have a valid `INDEX.md`, because write mode refuses to write when entries have errors (`memory_index.py:453-455`), so every entry break also touches K6.2. | An expected failure set per fixture, not exactly one; each mechanical record gets at least one fixture where it is in the set. |
| C4 + R2 (`REQUIREMENTS.md:37-40, 49-52`) | An absent `project-memory/` is "not applicable" and produces an empty warning; no record requires project memory to exist; which locations are "required when absent" is undefined beyond `AGENTS.md`. This repo has no `project-memory/` today (brief line 36), so a run would look clean. | Make a missing `project-memory/` a warned missing location; list required vs optional locations; decide whether its absence is a requirement failure at all. |
| F1 + U1 (`REQUIREMENTS.md:9-13`, `USE_CASES.md:6-13`) | F1 lists `work/` but not `work/<task>/state.md`, `evidence/`, `journal/` (`SOURCE_OF_TRUTH.md:112-118`); U1 promises user memory but the guidelines give no user-memory path (`SOURCE_OF_TRUTH.md:17-25`); `MEMORY.md` and topic files (`CACHES.md:489-513`) blur what counts as agent memory. | Enumerate the layout exactly; drop user memory or name its path; say which agent-memory files are listed. |
| C1 + R1 (`REQUIREMENTS.md:23-27, 44-47`) | No rule for a record with two checks (`tool; reviewer`, `git; reviewer`, `secret scanner; reviewer`). A "pass" can hide an unread reviewer half. | Precedence: any mechanical fail = fail; otherwise any human half = needs reviewer; only then pass. |
| R3 + R2 (`REQUIREMENTS.md:54-55, 49-52`) | No exit code for "a check could not run"; no warning-only command; no settings file named for the hook. | A non-zero code for unverified (never 0); a `--warn` mode; name the settings path and show the diff before installing. |
| F2 + U6 (`REQUIREMENTS.md:15-17`, `USE_CASES.md:40-44`) | `--project` may be any path, but `memory_index.py` always acts on the git root (`memory_index.py:316-318`); a subdirectory or non-git project checks the parent or errors. | Require the git root, or define subdirectory and non-git behaviour; never report the parent as the requested project. |
| U5 (`USE_CASES.md:35-38`) | `git status --short` cannot see writes into ignored `.cache/` or into `.git/index`, while F3 says "any file". | A content hash of every path, including ignored ones, before and after. |
| AGENTS + F1 (`memory_check/AGENTS.md:11-15`) | Tests may not touch the real home and F1 gives no override; static `fixtures/` cannot hold git history; "a test per Fails if" includes reviewer-only checks. | `--home`; scenario builders that construct repos; tests only for checks the tool owns. |

**7. I fixed the invariants before the features (my #2).** Making yourself unbeatable first — 「先為不可勝，以待敵之可勝。」 (quoted, my #2) — means: read-only (`GIT_OPTIONAL_LOCKS=0` on every git call, because git may write `.git/index`), one declared snapshot per run, evidence for every result, the precedence rule above, N/A only for an absent location, "not checked" for a stage that never ran, and a non-zero exit when a MUST cannot be verified. The warning uses HEAD only; the full report checks history on demand. Both print the snapshot in the first line.

**8. I split the build into pieces with a ground and a sign (my #8, my #17).**

1. `kit`: load the YAML with `Bun.YAML.parse` (verified: Bun 1.4.3 parses it) and the CACHES ids; classify each record. Test the literal counts 64/46/25/28/11 and the 9/4/7 split.
2. `locations`: F1/U1/F2, `--project` and `--home`; fixtures with every location present, one absent, a project outside this repo, and a nonexistent path.
3. `delegate`: run `memory_index.py --check` at HEAD/staged/`<rev>` with `cwd=project`, `GIT_OPTIONAL_LOCKS=0`; map stage and message to ids or JSON; report "not checked" when it stopped early; own scan for non-`[DFLOH]` files and inactive-entry kind mismatches (W1.1a).
4. `git-history`: rename to a new prefix/id (W1.1a/b), `changed:` line and earlier-line edits (W4.2), deletion and `superseded_by` (K4.1), claim/`source`/`depends_on` rewrite (K4.3), journal line edits (K5.1), merge-parent signal (W6.3a), second-header signal (W6.1a).
5. `report` + `warn`: precedence, evidence, MUSTs first, CACHES and reviewer records listed by id, `--warn` exact output.
6. `cli` + hook: flags, exit codes, dry-run settings diff, install only with `--yes`; no settings change without the owner's approval.
7. `read-only` + `any-project`: tree hash unchanged; U6 outside repo; non-git and subdirectory errors.

**9. I made the tests non-circular (my #16, my #9).** Orders clear before enforced; the fixture sets the ground, so the test need not chase the checker:

- Each fixture's expected failure set is hand-written from its `fails_if` before the check exists, and the test reads that file — never computes the expectation from the checker.
- The committed `INDEX.md` bytes are generated **once** by `memory_index.py` write mode (a different code path from `--check`), stored in the fixture, and never regenerated during the test.
- Every piece has a clean negative control (a checker that always fails is caught) and a planted break (one that always passes is caught).
- Git scenarios record their own operations (`git mv`, the commit message, the planted line) and the expected verdict is written from that narrative, not from `git log` output the checker reads.
- Evidence is asserted to the planted file:line, not merely to the id.
- The read-only test hashes every path including ignored ones; the mutation check flips one expected row and requires the suite to fail.

## What I need to know

1. **Which copy of the guidelines governs?** If the checked project's own `docs/memory-system/` governs, then U6 shrinks to projects that carry the kit, and a stale copy changes the verdict. If the tool's canonical copy governs, it must print the kit version. My default: `--guidelines` defaulting to the tool's own copy, with the target's copy reported as data.
2. **May `memory_index.py` gain `--check --json`?** If yes, one contract with ids and stages. If no, I either parse its stderr and pin that prose with tests, or C3 is narrowed and the wrapper owns the format checks — which duplicates the checker.
3. **Which snapshot is the warning about?** If HEAD-only, uncommitted memory is not warned about; if the working tree, K6 cannot be judged until the entry is staged. My default: HEAD for the warning, `--staged`/`--rev`/history for the report.
4. **Is CACHES in v1?** If yes, it needs levels, a `check` field and a cache schema first — EJ owns those documents, and I will report rather than edit them. If no, CACHES is listed as not mechanically checkable and the "two guidelines" promise is only half met.
5. **Is a missing `project-memory/` a failure, a warned missing location, or N/A?** This decides whether a run on this repo is silent. My default: warned missing location, not a requirement failure, because no record makes project memory itself required.
6. **Must `--project` be a git root?** My default: yes; a subdirectory or non-git path is a usage error, because `memory_index.py` resolves to the repo root and would otherwise report the wrong project.

**Proposed change to the pattern.** Split "a question to EJ" into *decision questions* (an owner-only fact that no amount of work can settle: which kit, CACHES scope, failure-vs-warning) and *trial questions* (things three attempts can settle). Send decision questions up before code; keep the three-trial rule for trial questions. It changes the escalation rule, not the time-box — my #11, foreknowledge comes from people, not from more attempts.

## Costs and risks

- **Delegation has a second contract (my #3).** One checker is kept, but the wrapper depends on `memory_index.py`'s stage behaviour and prose; if `--json` is refused, the mapping is brittle. Price: one more contract to maintain.
- **HEAD-only warning (my #8).** Old drift in history is not seen at session start. Price: the full report must be run deliberately, and it is slower.
- **The honest reviewer list (my #6, my #11).** The report will look mostly "needs reviewer" — 33 records plus the human halves — and EJ may stop reading it. Price: no fake passes.
- **CACHES out of v1 (my #13).** The vision promises two guidelines; v1 serves one. Price: an incomplete tool, or more document work before code.
- **Heuristic git signals (my #10).** Merge, second-header and journal checks can false-fail legitimate history; they must stay reviewer signals, not MUST failures. Price: W6.1a/W6.3a/K4.1 stay partly unverified.
- **Read-only through git (my #2).** Git itself may write `.git/index`; every call needs `GIT_OPTIONAL_LOCKS=0`, and the test must hash `.git`. Price: one more invariant to defend.
- **The hook (my #16).** A wrong settings path prints nowhere. Price: installation stays a manual owner step with a shown diff.

## How we would know I was right

- On a clean fixture and on this repo, **zero false passes**: every "pass" has an id, a file:line or command output, and no unread reviewer half.
- On 10 hand-planted breaks — one per mechanical check — the reported set equals the hand-written expected set; on the clean copy, every result is pass or N/A. Flipping one expected row makes the suite fail.
- The content hash of every path, including ignored ones, is identical before and after a run except for the report; `git status --short` is also identical.
- EJ's hand audit of three projects (this repo, a project with memory, a project without) finds no requirement the tool called passing that the audit finds failing; on this repo, the report names `project-memory/` as missing and lists CACHES and the reviewer records as such rather than passing them.

## Recommended plan

1. Patch `memory_check/{VISION,USE_CASES,REQUIREMENTS,AGENTS}.md` per the table: C1 levels/checks and SHOULD signals, C3 `--json` or named ids plus a "not checked" result, C4/R2 missing memory, U2 expected sets, R3 unverified exit, R2 `--warn` and the settings path, F1 layout/`--home`, F2 git root, U5 tree hash, AGENTS test scope.
2. Report the kit problems to EJ, do not edit the kit: CACHES needs levels, a `check` field and a cache schema before any CACHES check is mechanical; W2.1b/W5.1/K1.1's `git` label is judgement.
3. Piece 1 `kit` loader/classifier; test the literal 64/46/25/28/11 and the 20-record 9/4/7 split.
4. Piece 2 `locations` (`--project`, `--home`); fixtures all-present, one-absent, outside-repo, nonexistent.
5. Piece 3 `delegate` (`--check` HEAD/staged/`<rev>`, `GIT_OPTIONAL_LOCKS=0`, "not checked" on early stop, W1.1a own scan; `--json` if approved).
6. Piece 4 `git-history` (rename, `changed:`, deletion, claim rewrite, journal edits) on scenario repos, each verdict written before the check.
7. Piece 5 `report`+`warn` (precedence, evidence, MUSTs first, exact warning); Piece 6 CLI/exit/hook dry-run; Piece 7 read-only tree hash and U6.
8. Tests first: hand-written expected sets, write-mode INDEX golden, clean control, mutation check; stop when the 9 final records and 4 partial ones each have a fail fixture and a clean fixture, with no false pass.
