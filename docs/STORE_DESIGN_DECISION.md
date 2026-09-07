# Store layer — decision after three-lens review (2026-09-07)

Inputs: `SQLITE_INDEX_DESIGN.md`, `KNOWLEDGE_GRAPH_DESIGN.md`, and three isolated reviews (simplicity, correctness, integration — session scratchpad `ancient-games-experiment/store-design-reviews/`). Merge rule, fixed before the reviews ran: correctness vetoes a simplicity cut that breaks a lint; integration decides spec/event changes. Ranking criterion: simple yet effective.

## Decision

*Built 2026-09-08 as `ancient_games/index.py` (`f9e131e`): 7 tables, 5 run_id-scoped queries, differential-tested against the Python lints on 10 real ablation journals (50 comparisons, 0 mismatches) plus the 8 spec cases, and on a merged multi-run DB with colliding claim ids. Rebuild ≈ 8 ms/journal.*

**Build the minimal SQLite index. Defer the graph layer entirely. One spec edit, zero journal changes.**

The three reviews converged from different evidence: simplicity found that only 6 lints are wired and they read only 4 event types; integration found that only 1 of 25 algorithm steps (B·1) plus A's lint run reads anything back; correctness found that every graph query and two index queries were wrong or unrunnable on real data. Nothing in the deferred set has a reader today. The repo has already built two graphs nobody queried; this decision does not build a third.

## What gets built — `ancient_games/index.py`

**Tables (7), every column ← a journal event field, `run_id` on every table:**
`claim_recorded` · `check_executed` · `consumer_check` · `consumer_check_ref(run_id, …)` · `return` · `return_claim` (DERIVED, exploded from `return.fields`) · `return_follow_on` (DERIVED)

**Not built, and why:** `dispatch`, `exit` — journaled, no lint reads them · `rule_fire` — no writer, no reader · `artifact_ref` — its only readers were the graph queries · `edge` + PROV kinds + recursive CTE — no reader; unbuildable as specified (3 of 7 kinds depend on a column no DDL defines) · FTS — no lint needs text search.

**Indexes (5):** the ones the six queries use, as listed in the SQLite doc §3, each with `run_id` leading.

**Queries (6 lints → SQL), with the correctness fixes applied:**
1. `claims-without-evidence`
2. `follow-on-without-disposition` (needs a registered `REGEXP`, or a `LIKE`/prefix set for the enum — choose the prefix set; simpler, no callback)
3. `corroboration-capped` — category (b) count in SQL; (a)/(c) stay in Python because they read `Plan` fields never journaled (integration confirmed). **Every query filters `run_id`.** framing counted as `COUNT(DISTINCT framing) + (COUNT(*) > COUNT(framing))` — **not** `COALESCE(framing,'')`, which would merge `None` and `''` into one bucket where Python's set semantics keep them distinct (corrected during implementation, `f9e131e`); `mechanism` is NOT NULL so needs no coalesce. Identical-`command` dedup before mechanism dedup.
4. `hub-touched-without-tripwire` — the "ran" set from `check_executed`, scoped by `run_id`
5. `downstream-consumer-check-unrecorded` — subset test scoped by `run_id`; empty-`ref` is vacuously true (match the Python)
6. `evidence-after-verdict` — **stays Python.** Markdown heading order is not a SQL question; the `has_template` column it would need is not in the DDL and is not worth adding.

**Rebuild:** `rebuild(journal_path, db_path)` — both absolute (relative raises); drop-and-recreate in one transaction; DDL runs once here and nowhere else; `PRAGMA user_version = 1`; `PRAGMA journal_mode = WAL` optional; every connection opened with a non-zero timeout; the orchestrator is the only writer. Idempotent (confirmed by two-rebuild dump comparison). Measured 66 ms / 1k events, 651 ms / 100k. Trigger: on demand before a lint run; no incremental mode.

## Spec and code changes (integration's rulings)
- `SPEC.md` §7: **drop `check_executed.hub_integrity_for`** — the spec drifted; the code never had it and achieves the dual role via `claim_id`/`falsifies`. One edit.
- `journal.py`: **no change.**
- `lints.py`: wire `lint_scope_delta_missing` into `run_all_on_plan` — pre-existing gap, unrelated to the store. **Done 2026-09-08 (`d149a57`)**: wired in §8 order, run-scoped, Python in every backend; no case file changed because no journaled dispatch carries a `SCOPE` payload field, so it is live but not yet triggered by real data.
- Rejected (no reader): extend `consumer_check` with the resolved hub; add `check_executed.agent_id`; fix `artifact_ref` mode collapse.

## Tests — the oracle is the Python lint, never a re-derivation
- Differential: each SQL lint == its Python lint on the eight spec cases' events.
- **Multi-run:** merge two cases' journals with a colliding `claim_id` into one DB; every query must still equal the per-run Python result. This is the case correctness built that the design missed.
- Rebuild twice → byte-identical dump. Relative path → `ValueError`. Vacuous-true consumer check.
- A FAIL input per lint.
- **Backends (built):** `lints.run_all_on_plan(..., backend=python|sql|differential)`, default `$AG_LINT_BACKEND` → `python`. The `sql` backend builds a `:memory:` index from the events it is handed (`index.rebuild_from_events`) — no file is ever consulted, so nothing can be stale. `differential` runs both and raises `lints.LintBackendDivergence` on any per-lint disagreement; `tests/conftest.py` sets the whole suite to `differential`, so every case test exercises both implementations. `prove`/`run_lint` take `backend` and journal it in `result_summary`. Python stays the oracle; a divergence is a SQL bug until the Python is shown wrong, and then it is reported, never edited to match.

## Deferred — with the trigger and the corrections already known
The graph layer (edge table, PROV kinds, transitive-staleness CTE, hub-degree, shared-source join) is deferred until **a lint or algorithm step asks a question on real cross-run data that a join cannot answer.** When that happens, `KNOWLEDGE_GRAPH_DESIGN.md` is the starting point with these corrections applied first: Q1 filter `mode != 'read'` (not `IN ('invoke','mutate')`); Q4 column is `fields_json`; `artifact_ref` needs `source_event_rowid INTEGER` (not `source TEXT`) before `used`/`wasGeneratedBy(Artifact, Dispatch)` can exist; drop `verifies` as a materialized edge kind; the T1 and Case (ii) hub-degree test rows are wrong because Guard never journals the resolved hub — that gap (integration's REJECT of the `consumer_check` extension) must be reopened *only* when a reader exists. The cycle-guard rule and the materialized-over-views measurement (58 ms vs 0.07 ms) stand.

## What simple-yet-effective gives up today
Cross-run provenance questions ("which claims across all runs rest on fact X") and hub degree from history. Neither has been asked in three real runs. The `run_id` on every table is what keeps them cheap to add.
