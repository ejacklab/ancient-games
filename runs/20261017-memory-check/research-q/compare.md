# Six experts — how should memory-check work, before any code is written?

Question: `runs/20261017-memory-check/research-question.md`. Answers: `research-q/<expert>/answers/<expert>.md`.
This file compares the answers. It does not pick a winner and does not decide: the main agent decides.
Labels: *quoted* (an answer's own words), *my reading* (the comparer's reading), *not measured*.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | "Build an evidence report that distinguishes what was checked, what failed, and what remains unknown" (*quoted*) | "divide the checks strictly into static file inspections, git history inspections, and reviewer-only items, reuse `tools/memory_index.py` via a path-aware wrapper, and treat absent optional memories as not applicable" (*quoted*) | "a thin, read-only TypeScript layer that can give a final mechanical verdict on only 9 of the 20 `tool`/`git` records" (*quoted*) | "Check the 9 `tool` records by calling `tools/memory_index.py` and check 5 more from git history ... report the other 6 ... as **not checkable**" (*quoted*) | "a read-only runner over one named snapshot ... reports every clause it cannot decide as *needs a reviewer*, never as pass" (*quoted*) | "Build it in two slices ... (9 records), then the git-history checks (7 more). Four `git` records cannot be built" (*quoted*) |
| Main items used | #9, #7, #2, #13, #1, #3, #19, #18, #5 | #18, #14, #2, #3, #7, #13, #16 | #1, #19, #14, #3, #4, #13, #10, #6, #2, #8, #17, #16, #9, #11 | #14, #1, #6, #8, #2, #16, #19, #17, #5, #7, #18, #4, #3 | #1, #2, #3, #4, #5, #6, #7, #8, #9, #10 | — |
| Insights cited | — | — | — | — | `runs/20261016-four-experts-what-counts-as-change/insight.md#F-21e1586c`, `#F-d3132a7f`; `runs/20261016-integrate-r11-r13/insight.md#F-2cdebf3b`, `#F-969500fa` | — |

The item numbers are as each answer cites them (*quoted*); whether each item was applied correctly is *not measured*.

## Where they agree

- **The tool reports a result other than pass or fail for what it cannot decide.** Linus: "Missing evidence produces an
  incomplete result, never a pass"; 范蠡: reviewer items are "never report[ed] as pass or fail"; 孫子: "'not checked' for a
  stage that never ran"; 老子: "one `unknown` state, never folded into pass"; Dave: "*needs a reviewer*, never as pass";
  Dario: results for "partly checked", "guidance", "break found, reason not looked for" and "could not run" (*quoted*,
  all six). The names of the extra results differ (*my reading*; see disagreements).
- **W2.1b, W5.1 and K1.1 cannot be decided from git, despite their `git` label.** All six say so (*quoted*: Linus "It
  cannot determine generally whether a code change embodies a new decision"; 范蠡 lists them under "Need what the tool
  cannot see"; 孫子, 老子, Dave and Dario list them as reviewer or not buildable).
- **`memory_index.py --check` reads the staging area or a commit, not the working tree.** Linus, 范蠡, 孫子, Dave, Dario
  (*quoted*). 老子 adds only that it takes no path and runs on the cwd's git root (*quoted*). So the report must name its
  snapshot — Linus, 孫子, Dave say this outright (*quoted*).
- **Reuse `memory_index.py` (C3) rather than rewrite it.** All six (*quoted*). How much it covers is disputed (below).
- **SHOULD records with "with no written reason" cannot be failed by a tool.** Linus, 孫子, 老子, Dave, Dario (*quoted*);
  老子 calls it "the largest gap in the four docs" (*quoted*). 范蠡 does not raise it (*my reading*).
- **Records that mix a mechanical and a reviewer check have no result rule today.** Linus, 孫子, 老子, Dave, Dario
  (*quoted*). 孫子 and Dave give the same rule: a mechanical fail is a fail; otherwise any human half means needs a
  reviewer (*quoted*).
- **CACHES Core requirements have no `check` field (and no levels), and most of them are runtime behaviour.** Linus,
  孫子, Dave, Dario (*quoted*); 范蠡 agrees on the runtime half only (B2.1, B3.1, B5.1, K2, Rd3) (*quoted*).
- **"Required location" (C4, R2) has no source in the guidelines; this repo has no `project-memory/`.** All six raise
  the absent-memory case (*quoted*); what to do about it is disputed (below).
- **U5's `git status --short` is too weak; hash the whole tree, ignored files included.** Linus, 孫子, Dave, Dario
  (*quoted*). 孫子, Dave and Dario add `GIT_OPTIONAL_LOCKS=0` on git calls (*quoted*).
- **F1 needs a home-folder override so tests do not touch the real home; U1's "user memory" has no path in the
  guidelines.** Linus, 孫子, Dave, Dario (*quoted*).
- **Tests: the expected answer is written before the check, by hand or by another route, never computed by the check.**
  All six (*quoted*). Dave and Dario add a sabotage step: remove or force-pass each check and a test must go red
  (*quoted*); 孫子 a "mutation check" that flips one expected row (*quoted*).
- **Build in small pieces, hook last, hook installed only on EJ's yes to the settings diff.** All six (*quoted*).

## Where they disagree (side by side, quoted; never averaged)

**1. How much of the `tool` records `memory_index.py` already covers.**
- 老子: "All 9 `tool` records are already built. The tool adds no entry check at all." (*quoted*)
- 范蠡: lists W1.1a among the delegated file checks and does not name a gap in it (*my reading*).
- Linus: "The existing checker ignores names outside its recognised entry-name pattern and treats some inactive-entry
  content defects as warnings. W1.1a has broader MUST failure conditions." (*quoted*)
- 孫子: "W1.1a's 'prefix is not one of the five' is silently passed." (*quoted*)
- Dave: "Under C3 as written, a planted `X-foo.md`, or a superseded entry with `kind: foo`, gets W1.1a = pass." He cites
  `tests/test_memory_index.py:136-145`, which asserts exit 0 for `X-hidden.md` (*quoted*).
- Dario: "treat the '(warning)' kind/prefix lines as W1.1a fails." (*quoted*)
- Who checked it: Dave and 孫子 cite code lines and Dave a test; none ran `memory_index.py` (Dario: "I did not run
  `memory_index.py`"; Dave's prediction run is proposed, not done) (*quoted*). The claim is *not measured* by a run.

**2. How the 20 `tool`/`git` records split.**
- 孫子: "9 MUSTs a tool can settle finally; 4 MUSTs where a mechanical fail is final but a pass still needs a person; 7
  tool/git SHOULDs that can only signal" (*quoted*).
- 老子: 9 by `memory_index.py`, "5 more are decidable from git history", "6 of the 20 cannot be decided by any tool"
  (*quoted*).
- Dave: "14 of the 20 `tool`/`git` records can be decided at least in part. Five (W2.1b, W5.1, K1.1, W6.1b, W6.2) carry
  a `git` label that git history cannot back up" (*quoted*).
- Dario: "9 in slice 1, 7 in slice 2 and 4 unbuildable" (W2.1b, W5.1, K1.1, W6.1b) (*quoted*).
- Linus: no count; per-group table, with W6.1b "cannot identify distinct agent sessions" and W6.2 "No detected loss
  cannot certify compliance" (*quoted*).
- 范蠡: lists W6.1b and W6.2 under "Need git history" (*quoted*).
- On W6.1b and W6.2: 老子 and 范蠡 treat them as git-checkable (老子: W6.2 "at a **merge** commit"; W6.1b with K5.1 as
  "never edited after it is written"); Linus, 孫子, Dave, Dario say git cannot see them (*quoted*).

**3. What to do when `project-memory/` (or another location) is absent.**
- 范蠡: absent optional memory is "not applicable"; on this repo the tool "exits 0 with no warnings"; "Only missing
  *required* memory (e.g. `AGENTS.md`) should fail" (*quoted*).
- 孫子: "Make a missing `project-memory/` a warned missing location ... not a requirement failure" (*quoted*).
- 老子: "R3 makes 'no memory at all' a silent pass ... The owner must name the required-when-absent list" (*quoted*).
- Dave: "None of the 64 records has a MUST requiring any location to exist ... C4's example 'AGENTS.md is required'
  would be a rule the tool invents"; default: the warning carries only failing MUSTs (*quoted*).
- Dario: default "`AGENTS.md` always; the rest only once `project-memory/` exists in HEAD" (*quoted*).
- Linus: "report absence as an observed fact; leave its unresolved severity open"; also U3 says "every missing
  location" where R2 says "missing required locations" (*quoted*).

**4. CACHES in the first version.**
- 范蠡: file-checkable now: "B1/B1.1/B1.2 ... B4.1 (SQLite holds only active entries with `covers`), and K1.1/K1.2
  (SQLite carries content hash and model id)" (*quoted*).
- 孫子: "keep `CACHES.md` out of mechanical checking until it has levels, a `check` field and a cache schema"; B2.2 is a
  signal (*quoted*).
- Dave: "Only B2.2 (`git check-ignore`) and Rd1 ... can be read"; B4 and K1 "need the index opened and its schema
  known, and no doc fixes a schema" (*quoted*).
- Dario: "only B2.2 and Rd1.1 now. Everything else is 'not applicable: no cache tool'" (*quoted*).
- Linus: inspect "supported formats"; rebuild and query trials "belong in disposable fixtures" (*quoted*).

**5. The expected `INDEX.md` in test fixtures.**
- 孫子: "generated **once** by `memory_index.py` write mode (a different code path from `--check`), stored in the
  fixture" (*quoted*).
- Dave: the baseline has "an `INDEX.md` built by memory_index.py" (*quoted*).
- Linus: "Do not generate expected indexes with the production renderer. Handwrite tiny expected indexes." (*quoted*)
- 老子: "a **literal byte string** written in the test" (*quoted*).
- Dario: "`INDEX.md` must be literal bytes, never produced by the script's write mode" (*quoted*).

**6. Who writes the expected answers.**
- Dave: "Another engine writes it before the check exists, and it stays out of the builder's files" (*quoted*).
- Dario: "Have an engine other than the code's author write or review the mutation table" (*quoted*).
- Linus: "The worker writes each expectation ... a second reader checks it before seeing implementation output"
  (*quoted*).
- 孫子 and 老子: hand-written from `fails_if` before the check exists; no second author named (*my reading*).

**7. U2's "exactly that requirement".**
- Linus, 孫子, Dario: impossible as written; use an expected *set* per fixture (*quoted*).
- 老子 point 12: K6.1a and K6.2 "the report must cite both ids on one result"; yet in "How we would know": "Count of
  failing ids per fixture must be 1" (*quoted*; the two read as in tension — *my reading*).
- Dave: keeps "Each plant makes exactly its own id fail" by adding a "*not reached (blocked by <id>)*" result
  (*quoted*).

**8. What the session-start hook may read.**
- 老子: "the hook runs locations + `memory_index.py --check` + index size only, and the body checks (W1.3a) belong to the
  command" — R2 conflicts with Rd1.1/Rd2.3b (*quoted*).
- Dave: "never open a file inside `.cache/` (listing the folder is fine), and it must print ids, never claims"; whether
  history MUSTs go in the hook is "a measured comparison" (*quoted*).
- Linus: "the startup path inspects permitted files and location metadata; full cache-content checks run on demand"
  (*quoted*).
- 孫子: "The warning uses HEAD only; the full report checks history on demand" (*quoted*).
- 范蠡: "run only file-level presence and index checks at startup", and "Benchmark ... to guarantee sub-100ms startup
  latency" (*quoted*). The 100 ms and 50 ms figures are not in the question or the four docs (*my reading*).

**9. The four undecidable `git` records: edit the YAML or not.**
- Dario: "ask EJ to mark them `reviewer`" in the YAML (*quoted*).
- 孫子: "Report the kit problems to EJ, do not edit the kit"; "I will not edit the kit to relabel W2.1b/W5.1/K1.1"
  (*quoted*).
- Dave: "Report the YAML's overstated `tool`/`git` labels to EJ" (*quoted*).
- 老子: report as an observation for the owner, not a fix (*quoted*, on the reviewer-labelled records).

## What each added that the others did not

- **Linus:** the vision's stale-memory promise "exceeds structural checks" — "A fresh index or matching cache hash does
  not establish that an entry still agrees with code" (*quoted*); Rd3.1a's limits are interim constants with no input for
  owner-measured limits (*quoted*; Dario also notes the hardcoded limits); U3 "every missing location" vs R2 "required"
  (*quoted*); C1 runs the requirement-check eight and fails four (who decides, weak words, basis, links) (*quoted*).
- **范蠡:** three realms — files (earth), git (heaven), reviewer (people) (*quoted*); startup time budgets 100 ms / 50 ms
  (*quoted*; numbers not given by EJ, *my reading*); non-git directories and shallow clones degrade to not applicable
  (*quoted*).
- **孫子:** 64 records under 46 base ids, 25 MUST / 28 SHOULD / 11 guidance, and the "46 requirements" in
  `SOURCE_OF_TRUTH.md:160` is the base-id count (*quoted*; *not measured* by the comparer); which copy of the guidelines
  governs another project (`--guidelines`) (*quoted*); `--project` must be the git root (*quoted*); a `--warn` mode
  (*quoted*); `Bun.YAML.parse` "verified: Bun 1.4.3 parses it" (*quoted*); split owner questions into decision questions
  and trial questions (*quoted*).
- **老子:** five records mechanically decidable but labelled `reviewer` (W1.1c, W1.2b, K6.1b, K6.3b, Rd1.1) (*quoted*);
  a tool-level error with no requirement id ("not known to git") needs a place in R1 (*quoted*); publish a known-empty
  baseline on this repo and build "at least one fixture whose memory is real, not authored by the checker" (*quoted*);
  rebases leave W6.2/W6.3a unseen — report "merges-only" (*quoted*).
- **Dave:** id collisions — `K1.1`, `Rd1.1`, `Rd2.1` mean different things in the two guidelines; prefix ids `SoT:` /
  `CACHES:` (*quoted*; Dario raises the same, see below); shallow-clone detection with
  `git rev-parse --is-shallow-repository` (*quoted*); a control arm — `memory_index.py` alone must pass the W1.1a
  plants that memory-check fails (*quoted*); one cheap prediction run before building (*quoted*); four insights applied
  (*quoted*); a thymus analogy, labelled *recall* and not deciding (*quoted*).
- **Dario:** also id collisions, plus "The YAML's `retired_ids` says K2 and K3 are unused, but CACHES uses them" and
  `memory_index.py` comments cite a third id set (*quoted*); a past MUST break "fails forever" with no baseline or waiver
  (*quoted*); C1 lumps `none` guidance with `reviewer` (*quoted*; Linus also says `none` is guidance); a session-start
  hook reaches Claude Code only, labelled *recall* (*quoted*); TypeScript needs a YAML parser and depends on `python3`
  (*quoted*; 孫子 says Bun parses YAML natively); the report headline counts checked / partly / reviewer / guidance
  (*quoted*).

**Who stands alone:** 老子 alone says `memory_index.py` already covers all 9 `tool` records with no gap; 范蠡 alone says
absent `project-memory/` gives exit 0 with no warning on this repo and gives startup time numbers, and alone treats
CACHES B1.1/B4.1/K1.1/K1.2 as file-checkable now; Dario alone asks EJ to edit the YAML labels; Linus alone raises the
stale-memory promise in the vision; 孫子 alone raises which guidelines copy governs (*my reading*, from the sections
above).

## What they need to know (the questions, merged, for EJ — each with its options)

1. **Which snapshot do the report and the warning describe?** (Linus, 孫子, Dave, Dario)
   - a. HEAD for the warning; `--staged` / `--rev` / history for the report (孫子's default).
   - b. HEAD plus the staging area, read from git objects only, named in the first line (Dave's default).
   - c. The current files (working tree) — needs an agreed read-only extension of `memory_index.py` (Linus).
2. **Which locations are required, and what does absent `project-memory/` produce?** (all six)
   - a. `AGENTS.md` required; absent `project-memory/` is not applicable, no warning (范蠡).
   - b. Absent `project-memory/` is a warned missing location, not a failure (孫子).
   - c. No location is required by the guidelines; the warning carries only failing MUSTs; requiring one is a guideline
     change (Dave).
   - d. `AGENTS.md` always; the rest only once `project-memory/` exists in HEAD (Dario).
   - e. Report absence as an observed fact; leave its severity open (Linus).
   - Also: U3 says "every missing location", R2 says "missing required" — which wins? (Linus)
3. **May `memory_index.py` change?** (孫子, Dave, Dario; Linus as an option)
   - a. Yes: `--check --json` with record ids and stages, fail non-`[DFLOH]` files and a wrong kind in any status; C3
     stands as written.
   - b. No: memory-check parses its stderr, pinned by contract tests, and checks the missed W1.1a clauses itself; C3 is
     narrowed.
4. **Which extra result states (and exit codes) are allowed beyond R1's four?** (all six)
   - a. One `unknown` state, distinct from not applicable (老子).
   - b. *not reached (blocked by <id>)* and *needs a reviewer* (Dave).
   - c. partly checked / guidance / break found, reason not looked for / could not run (Dario).
   - d. Incomplete check plus an operational-error exit (Linus); a non-zero exit for an unverified MUST, never 0 (孫子).
   - e. May the warning carry a "could not run" line, which U3 forbids today? (Dario: default yes)
5. **How are mixed-check records and SHOULD findings reported?** (Linus, 孫子, 老子, Dave, Dario)
   - a. A mechanical fail is a fail; otherwise needs a reviewer; only then pass (孫子, Dave).
   - b. Give the "written reason" a place and a bound so the tool can look; otherwise give up the check (老子 — "Where is
     a written reason written, and how is it matched to the entry it excuses?").
   - c. Report SHOULD breaks as signals / findings only (孫子, Dave, Dario).
6. **The `git` records git cannot back (W2.1b, W5.1, K1.1; W6.1b, W6.2 disputed):**
   - a. EJ edits the YAML to `reviewer` (Dario).
   - b. Report to EJ, leave the YAML; the tool lists them as needs a reviewer (孫子, Dave).
   - c. The tool lists commits touching covered files as hints only (Dario).
7. **CACHES in v1?** (Linus, 范蠡, 孫子, Dave, Dario)
   - a. Out of mechanical checking until it has levels, a `check` field and a cache schema (孫子).
   - b. Only B2.2 and Rd1 now; the rest not applicable / needs a reviewer (Dave, Dario).
   - c. Also B1.1, B1.2, B4.1, K1.1, K1.2 as file checks when `.cache/` exists (范蠡).
   - d. Inspect supported formats only; behaviour trials in disposable fixtures (Linus).
   - And who assigns CACHES levels and checks (Dave, Dario).
8. **What may the session-start hook run?** (Linus, 范蠡, 孫子, 老子, Dave)
   - a. Locations + `memory_index.py --check` + index size; body checks in the command only (老子).
   - b. Never open `.cache/`, print ids not claims; history MUSTs in or out decided by a measured comparison (Dave).
   - c. HEAD only; history on demand (孫子); file presence and index checks only (范蠡).
   - And which harness and settings path (Linus, 孫子; Dario notes hook reach is Claude Code only, *recall*).
9. **History scope.** (老子, Dave, Dario, Linus)
   - a. Every commit touching `project-memory/` (Dave's default).
   - b. Since the first commit touching `project-memory/`, with `--since`, range printed (Dario's default).
   - c. A parameter, measured on a synthetic 1,000-commit fixture first (老子).
   - And: may a past MUST break be acknowledged (Dario); a shallow clone gives "not applicable: history incomplete"
     (Dave).
10. **Which copy of the guidelines governs another project?** (孫子; Dario)
    - a. The tool's own copy via `--guidelines`, version printed, the target's copy reported as data (孫子's default).
    - b. The checked project's own `docs/memory-system/` (孫子's alternative).
11. **Must `--project` be a git root?** (孫子; Dario on non-git projects)
    - a. Yes; a subdirectory or non-git path is a usage error (孫子's default).
    - b. Define subdirectory and non-git behaviour; never report the parent (孫子, Dario).
12. **Ids from two guidelines: prefix them (`SoT:K1.1`, `CACHES:K1.1`)?** (Dave, Dario) — yes / keep bare ids.
13. **Expected `INDEX.md` in fixtures:** literal bytes written by hand (Linus, 老子, Dario) / generated once by
    `memory_index.py` write mode and frozen (孫子, Dave).
14. **Who writes the expected answers:** another engine (Dave, Dario) / the worker plus a second reader before output
    (Linus) / the builder by hand before the check (孫子, 老子).
15. **Is there a real project with `project-memory/` (with merges) to calibrate against?** (Dave, 老子) — yes, name it /
    no, fixtures only, reported as such.
16. **Pattern change: a question that trials cannot answer goes to EJ at once, not after three failed trials.** (孫子,
    老子, Dave — each labels it a proposed change) — adopt / keep the three-trial rule.

## Check

- **Results (given to this step, and in each `check.txt`):** all six have a usable answer and the check passed for
  their own file. Each `check.txt` was run in that expert's own subfolder and lists the five *other* experts as
  "FAIL ...: no answer file", ending "FAIL: 1 answers, 5 failure(s)"; no line names the expert whose folder it is
  (*quoted*). The progress log calls those five "absent by design" (*quoted*). Reading this as a pass for the expert's
  own file is *my reading*.
- **"After one rerun":** `nodes/research-q.progress.md` shows the first check for linus, fan-li, sun-tzu, dave and dario
  ran at 17:24 before any answer existed and crashed (folder missing); each expert then ran once and was checked again
  (*quoted*). Each `status.json` records one run (*quoted*). 老子 had no failed first check in the log (*quoted*).
- **Engines (from each `status.json`, *quoted*):** Linus — codex, `gpt-6.1-sol`, 124 s; 范蠡 — agy,
  `gemini-3.8-flash-medium`, 215 s; 孫子 — dsh, `deepseek-flash (dsh headless profile)`, 335 s; 老子 — opencode,
  `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, 78 s; Dave — claude, `claude-opus-5-5`, 453 s; Dario — claude,
  `claude-sonnet-5-5`, 297 s. All exit 0, `ok: true`, `problem` empty. No fallback is recorded in any `status.json`
  (*quoted*): Linus ran on Codex, not mcode; 范蠡 ran on agy, not Claude.
- **Small defect:** 老子's answer file starts with a stray line, "I'll read the brief first." (*quoted*).
- **Logs:** 范蠡's, Dave's and Dario's logs are empty (0 lines) (*quoted*, `wc -l`).
- **What the check does not establish:** the check script was written by Claude. It checks that the answer file
  exists and its citations are well formed. It does not establish that an expert applied a rule correctly, that a cited
  line says what the expert says it does, or that any count is right. The counts quoted above (20, 64, 46, 9/4/7,
  14 of 20, 9/7/4) are the experts' own; the comparer did not recount them (*not measured*). No expert ran
  `memory_index.py`; the claims about what it misses rest on reading its code (and, for Dave, its test) (*quoted*).
