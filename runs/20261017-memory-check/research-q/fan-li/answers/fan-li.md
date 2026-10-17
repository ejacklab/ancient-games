# 范蠡 (Fan Li) — How memory-check should work

## Answer
Before writing code, inspect the preparations: divide the checks strictly into static file inspections, git history inspections, and reviewer-only items, reuse `tools/memory_index.py` via a path-aware wrapper, and treat absent optional memories as not applicable rather than failures. If the session-start hook must be fast, run only file-level presence and index checks at startup while reserving full git-history traversals for on-demand reports.

## How I decided

1. **Examine the preparations first (my #18).** In 國語·吳語, when asked what makes it possible to fight, I asked: 「審備則可以戰乎？」王曰：「巧。」 (`quoted`). Before writing code, we examine what the requirements demand and what existing tools already defend. `tools/memory_index.py` already checks index generation, frontmatter delimiters, entry id formats, duplicate ids, active kinds, conflict markers, and index size bounds (`MAX_LINES = 200`, `MAX_BYTES = 24_000`). Building `memory-check` requires examining these defenses so we do not rebuild what already exists.

2. **Say who is better at what (my #14).** In 國語21:7, I said: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 (`quoted`). We must divide the requirements by who or what is equipped to check them, never assigning to an automated tool what requires human judgement:
   - **Checkable on files alone:** SOT requirements W1.1a (`kind` matches prefix), W1.1b (id format `DD-MM-xxxxxx-YYYY`, duplicate ids across files), W1.2a (`---` delimiters), W1.3a (active entry has claim and `**Why:**`), W4.1b (`status` value), K6.1a/K6.2 (`INDEX.md` byte match), K6.3a (no `<<<<<<<` or `>>>>>>>`), Rd3.1a (size limits), location discovery F1, and Rd1.1 (verifying `CLAUDE.md`, `AGENTS.md`, and start hooks do not open `.cache/`). In CACHES: B1/B1.1/B1.2 (cache forbidden if `project-memory/` absent or trigger not recorded in `runs/`), B4.1 (SQLite holds only active entries with `covers`), and K1.1/K1.2 (SQLite carries content hash and model id).
   - **Need git history or git staging:** SOT requirements W1.1a (git rename to different prefix), W1.1b (git rename to different id), W2.1b (code changed with no entry), W4.2 (entry edited without matching `changed:` line), W5.1 (code changed under new decision), W6.1a (commit adds entry to existing file), W6.1b (multiple sessions in one journal), W6.2 (lost edit in merge), W6.3a (missing merge lines), K1.1 (behavior changed without superseding entry), K4.1 (file deleted or missing `superseded_by`), K4.3 (claim/source/depends_on altered after first commit), and K5.1 (journal edited after initial commit). In CACHES: B2.2 (`git check-ignore project-memory/.cache` and clean `git status --short`).
   - **Need what the tool cannot see (reviewer or runtime engine):** Semantic judgement such as whether an entry holds "two claims" (W1.3a), whether a code change is "under a new decision" (W2.1b, W5.1, K1.1), secret scanning (W3.2), agent execution state (W3.3a, W3.4, W5.2, Rd4.1, Rd5.1–Rd5.3, Rd6.1), human decisions by EJ (CACHES B1.0, K3.3), and cache software runtime mechanics (CACHES B2.1, B3.1, B5.1, K2.1–K2.3, Rd3.1–Rd3.5). The tool must catalog these as needing a reviewer (U4) and never report them as pass or fail.

3. **Three kinds of state affairs, three things to go by (my #2).** In 國語21:3, I said: 「夫國家之事，有持盈，有定傾，有節事。」/「持盈者與天，定傾者與人，節事者與地。」 (`quoted`). In memory verification:
   - *Earth (files on disk):* The ground truth in the working directory.
   - *Heaven (git timeline and triggers):* Changes across commits, branching history, and time-based triggers.
   - *People (reviewer judgement):* Human intent, policy adherence, and semantic evaluation.
   Treating all checks as one homogeneous bucket creates confusion; keeping the three realms distinct ensures clarity.

4. **While the time has not come, do not force growth (my #3).** In 國語21:9, I said: 「時不至，不可彊生；事不究，不可彊成。」 (`quoted`). In this repository today, `project-memory/` does not exist (`ls project-memory` fails). Per C4, absent optional memory is not a failure, but `not applicable`. The docs are misleading where U3 and R2 fail if "a missing location" is not in the warning, because treating absent optional memory as a failure contradicts C4 and would flood session-start warnings. Only missing *required* memory (e.g. `AGENTS.md`) should fail.

5. **Do not plan early for unbuilt stores (my #7).** In 國語21:13, I said: 「有奪，有予，有不予，王無蚤圖。」 (`quoted`). The four docs are misleading in C1 by demanding checks for all `CACHES.md` Core requirements. Requirements B2.1, B3.1, B5.1, K2.1–K2.3, and Rd3.1–Rd3.5 are runtime properties of the cache search and rebuild tools, not static repository lint rules. Planning to test cache engine internals inside `memory-check` before any cache exists or before triggers B1.1/B1.2 fire forces things out of their proper time.

6. **Contention is the last of affairs (my #13).** In 國語21:5, I said: 「夫勇者，逆德也；兵者，凶器也；爭者，事之末也。」 (`quoted`). The tool must be purely read-only (F3, U5). It reads files and git, outputs to stdout or `--out`, and never alters project files, entries, or caches.

7. **Take a method that worked for the state to the household (my #16).** In 史記129:24, I said: 「計然之策七，越用其五而得意。既已施於國，吾欲用之家。」 (`quoted`). Apply the proven test patterns from `code_map/` and `tools/memory_index.py`:
   - Split the build into small, verifiable segments: location discovery (F1–F3), file checks (W1–W4, K6), git checks (K4, W4.2), cache checks (B1, B4.1, K1), reviewer cataloging (U4), and reporting/hook (R1–R3).
   - Test checks against fixtures with known planted defects (non-circular testing), where expected outcomes are fixed fixture contracts, not re-computed by the check under test.
   - Guard against `memory_index.py`'s limitation: it inspects the git staging area by default and lacks `--project <path>`. `memory-check` must invoke it with an explicit working directory and ensure unstaged working tree files are validated.

8. **Recommended Plan (my reading):**
   1. Build location discovery (`Find`: F1–F3; `AGENTS.md` required, `project-memory/` optional).
   2. Wrap `tools/memory_index.py` with cwd management for file checks (W1.1–W1.3, W4.1b, K6.1–K6.3, Rd3.1a).
   3. Implement git-history analyzer for revision checks (K4.1, K4.3, W4.2, B2.2).
   4. Build cache validator for SQLite tables (B1.1, B1.2, B4.1, K1.1, K1.2) when `.cache/` is present.
   5. Catalog reviewer requirements (U4) and map absent optional memory to not applicable (C4).
   6. Build Markdown reporter (R1) and session-start warning formatter (R2, R3).
   7. Validate all checks on fixture repositories with planted defects to avoid circularity.
   8. Benchmark session-start hook execution to guarantee sub-100ms startup latency.

## What I need to know
- If EJ intends `memory-check` to run on non-git directories or shallow clones, git history checks must degrade gracefully to `not applicable` rather than failing.
- If EJ requires git-history checks inside the session-start hook (R2), we must establish whether a startup timeout budget is enforced.

## Costs and risks
- **my #14 (Subprocess wrapper overhead):** Calling `tools/memory_index.py` as a Python subprocess incurs startup time (~30–50ms), risking session-start hook lag if called repeatedly.
- **my #18 (Preparation delay):** Clarifying the contradictions in U1/U3/C4 and resolving `memory_index.py` invocation constraints takes design alignment before writing code.
- **my #3 (Masking misnamed paths):** Marking absent optional locations as not applicable risks silently passing if a user misnames `project-memory/`.
- **my #7 (Deferred cache verification):** Deferring runtime cache behavioral checks leaves cache engine compliance unverified until the cache tooling itself is built.

## How we would know I was right
- Running `memory-check` on this repository today reports `AGENTS.md` and `CLAUDE.md` present, `project-memory/` absent (not applicable per C4), exits 0 with no warnings, and completes in under 50ms.
- Running `memory-check` against fixture repositories with planted defects catches 100% of planted violations without false passes, lists reviewer requirements under U4, and leaves `git status --short` completely untouched (U5).
