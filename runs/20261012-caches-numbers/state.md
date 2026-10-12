# State — 20261012-caches-numbers

## Challenge (verbatim)

> sees like each new session , you do the same review will ask the same old question again, sorry this is a memory
> architect design guide what we try to build here , so not logic for me to give you a number, and what you actually
> should do it to go sue web research find some solid examples or research data, put in example in what case the
> numebr can be what. an even better one you looks at the seza project, and research . for each agent type and
> difference conditions , shoudl be what number , give some use cases. make sense ?

## Vision and requirements (method 3.0)

- **Vision:** `docs/memory-system/vision-statements/caches-memory-vision-statements.md`, settled by EJ on 2026-10-12.
- **Requirements:** taken from EJ's message above, which is their source.
  1. Each trigger in `CACHES.md` (R5.1, R5.2, R5.3 and R8.2, plus the `INDEX.md` size it depends on) gets example
     numbers by case: agent type × condition.
  2. Every example number comes from web research (solid examples or research data, with a URL) or from a
     measurement of the SEZA project (with the command).
  3. There are use cases, with SEZA as the worked one.
  4. The triggers stay comparisons; the examples show what a comparison typically comes out at.

## Steps

| # | Node | Engine | Status | Output |
|---|---|---|---|---|
| 1a | SEZA: measure its real memory | Claude subagent (sonnet) | done | `nodes/seza.md` |
| 1b | Web: published numbers per agent type and condition | Claude subagent (sonnet), web | done | `nodes/web.md` |
| 1c | Web: effective context per model family | agy `gemini-3.1-pro-high`, plan | **failed** (headless denies shell and web) | `nodes/agy.md` |
| 1d | Web: search vs grep by size, code-graph pay-off, rebuild cost | opencode MiniMax M3.1, plan | done | `nodes/opencode.md` |
| 1e | SEZA use cases by agent type (an independent second look) | codex `gpt-6.1-sol` high, read-only | done | `nodes/codex.md` |
| 2 | Section "Example numbers by case" in `CACHES.md` | main session | done | `docs/memory-system/CACHES.md` § Example numbers by case |
| 3 | Check the example table against every node file | dsh (`deepseek-flash`) | todo | `nodes/dsh-check.md` |

## Log (append only)

- 2026-10-12 run created; 1a and 1b launched in parallel (independent, read-only, each writes its own file).
- 2026-10-12 EJ: "use your subagent, deepseek harness, agy, codex and opencode". Added 1c-1e (`launch.sh`, briefs in `briefs/`) and node 3 (dsh). agy has no shell in headless mode (run 20261012-caches-merge), so its slice is web-only.
- 2026-10-12 1a done (`nodes/seza.md`). At session start SEZA loads 58,427 B (~14.6K tokens est.), 7.3% of a 200K
  window. Its stores:
  - the Claude memory folder: 52 topic files, 167 KB, `MEMORY.md` 52 lines and 12 KB;
  - `project_memory`: a 9.08 MB journal and a 16.1 MB `graph.db`, of which 98 entities are non-inventory;
  - `.ctxgraph`: 1.1 MB, never queried by code (`usage_count` 0);
  - `factstore`: 0 facts;
  - 48 ADRs.
  On its own 5-question test (n=5), grep took 4-7 ms but printed between 361 B and 109,519 B (about 27K tokens).
  **Side effect, reported:** the first sqlite3 open of SEZA `.ctxgraph/graph.db` (WAL) touched `graph.db-shm`, whose
  mtime moved to 2026-10-12. The db content is unchanged (`graph.db` mtime still 2026-07-28). Later opens used
  `immutable=1`.
- 2026-10-12 1b done (`nodes/web.md`, about 40 example rows, each labelled CONFIRMED/REPORTED/GAP):
  - Claude Code MEMORY.md: 200 lines or 25KB, re-verified;
  - Codex AGENTS.md: 32 KiB; Cursor: under 500 lines;
  - context windows: about 1M for current models;
  - BM25 overtakes grep at about 6,980 docs or 8.5M tokens (S-F4, full table);
  - BEAM: RAG beats long-context from 500K tokens;
  - CodeGraph: savings track cross-file reach, not file count.
  Gap: nothing found for a corpus of a few hundred short notes.
- 2026-10-12T10:41:50Z agy re-run (no-shell note): exit=0 0B
- 2026-10-12T10:42:02Z agy re-run also empty: headless denied "read_url" (web fetch). agy headless can run neither shell nor web without a permission change (agy settings.json allow-rule or --dangerously-skip-permissions); not done, EJ's call. agy is reassigned to an inline review of the drafted section (no tools needed).
- 2026-10-12T10:45:30Z agy exit=0 0B
- 2026-10-12T10:45:30Z opencode exit=0 26401B
- 2026-10-12T10:45:30Z codex exit=0 38983B
- 2026-10-12 1e codex done: per-agent SEZA start loads; Codex local window 500K (models cache); agy 20K-token rules
  budget; dsh 65,536-byte loader budget; Qwen 15% warning ratio; SEZA's real failures were a stale index and a
  missing graph. No SEZA file changed (timestamps checked).
- 2026-10-12 node 2 done: "Example numbers by case" written into `CACHES.md`, with sources W-*, OC, SZ, CX. One
  miscount fixed against `seza.md` (the full-text proxy ranked the right file first on 3 of 5, not 2).
- 2026-10-12 node 3 launched: dsh and agy review the section inline (`launch-review.sh`); the review copy carries one planted defect, whose location is kept out of every file they see.
- 2026-10-12T10:48:50Z review dsh exit=0 6425B
- 2026-10-12T10:48:50Z review agy exit=126 0B
- 2026-10-12 node 3, dsh: **REPAIR**, 7 findings (1 high, 2 medium, 4 low). The plant was R5.1's "3,980 docs, 8.5M
  tokens" (true 6,980, W-22) in `verify/section-review-copy.md`. dsh caught it as finding 2, quoting W-22's table, so
  this review can fail. The other 6 were verified by the main session against seza.md, codex.md and web.md and fixed
  in `CACHES.md`:
  - the R8.2 reading contradicted its own table;
  - `.ctxgraph` "queried by no code" overreached (CX: a query script exists, and a staging copy was queried);
  - the 52 topic files are 159,524 B, not 167,257;
  - the SEZA grep scopes were mixed up;
  - there are 7 tiers, not 9;
  - two vendor benchmarks were not labelled as vendor.
- 2026-10-12 agy's first review failed in the launcher: the 146 KB prompt was passed as one argument, over the
  128 KB per-argument limit ("Argument list too long"). That was the COO's error. agy was relaunched on the fixed
  section with a short prompt, reading the files itself.
- 2026-10-12T10:57:09Z agy re-review of the fixed section (reads the files itself): exit=0 6697B
- 2026-10-12 node 3, agy (reading the files itself, on the section after dsh's fixes): **REPAIR**, 4 findings (2
  medium, 2 low), all verified and fixed:
  - Qwen's hard index cap (200 lines or 25,000 B), with the 15% figure only advisory;
  - SEZA's FTS rebuilds were in-memory;
  - Opus's 93% at 256K is a reported figure (W-15);
  - the 2,013 files are SEZA's whole markdown corpus, not its memory.
  No new review after these fixes.
- 2026-10-12 committed without SEZA's raw material (EJ, option 1: SEZA is a private repo, and ancient-games is
  public). `.gitignore` keeps 7 files on disk only: `nodes/seza.md`, `nodes/codex.md` and their logs, the inline review
  prompt, and both review outputs. The review verdicts and findings are recorded above. `CACHES.md` keeps the SEZA
  numbers and one quote.
- 2026-10-12 EJ accepted `docs/memory-system/CACHES.md` ("yes I accept"), including R1–R9; its status line now says so.
