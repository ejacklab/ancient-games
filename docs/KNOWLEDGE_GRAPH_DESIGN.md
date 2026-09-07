# Knowledge graph layer — design

Domain: software engineering. The Ancient Games is a rules-based
agent-orchestration framework (five algorithms: Gate, Guard, Corroborate,
Filter, Prove) whose only durable record of what happened is the
append-only JSONL trace journal (`ancient_games/journal.py`, §7). This
document designs the layer that answers cross-cutting provenance
questions over that journal — hub degree, shared-source independence,
transitive staleness, dispatch lineage, and "what does this recommendation
rest on" — without a graph engine, per wave 2's converged verdict
(`store-research/wave2-kg/MERGED.md`, three independent framings,
no conflicts).

## 1. Purpose and non-goals

**Purpose.** Answer, over the trace journal (and the sibling per-event-type
SQL index built alongside it), exactly the graph-shaped questions the
framework's own algorithms and lints ask:

1. Which artifacts are hubs, by degree (Guard, D·2/D·2′).
2. Did two claimed-independent corroborating sources actually share the
   same underlying evidence (Corroborate, B·1's independence assumption)?
3. Which dispatches/claims transitively rest on a fact later found stale
   (K6 — cross-run provenance, not answerable by any single stage)?
4. What did a task's plan actually dispatch, and what did each dispatch
   produce (dispatch lineage)?
5. What does a given claim/recommendation ultimately rest on, resolved
   down to exact evidence and artifacts (the evidence-KG skill's own
   lineage discipline, §6 below)?

**Non-goals, stated up front because this repo has a track record of
building graphs nobody queries** (`loop/graph_memory.py`, 631 lines, no
query code, `~/dev/seza/.ctxgraph/graph.db`, wired once, never touched
again — wave 2 MERGED.md, "In-house prior art"):

- **No graph engine.** No Kùzu, DuckDB PGQ, Oxigraph, CozoDB, NetworkX
  installed or invoked by default. The graph *is* SQL — a set of typed
  tables and one small materialized edge table, queried with `JOIN`,
  `GROUP BY`, and `WITH RECURSIVE` (wave 2 MERGED.md, convergent verdict).
- **No ontology.** PROV-flavored edge *names* are adopted as column
  values (`used`, `wasGeneratedBy`, `wasDerivedFrom`, `wasAttributedTo`)
  for readability and because they map cleanly onto entity/activity/agent
  — not as an RDF store, not for PROV-O interoperability (wave 2
  MERGED.md, "Provenance model": "Adopt the vocabulary, not the engine").
- **No node or edge type without a listed query.** Every type in §2 is
  justified in §3 by a specific query. Where a natural-seeming type
  (e.g. a standalone `Fact` node distinct from `Evidence`, or
  `actedOnBehalfOf` delegation edges) is *not* built, §2 says why, citing
  the absence of a query that needs it — this is the same test the
  dispatch itself applies to this design.
- **No whole-graph iterative computation** (PageRank, centrality,
  community detection). Nothing the framework asks today is
  centrality-shaped (K1). If that changes, §5 names the exact trigger.

## 2. Node and edge model

### Isolation note

Per this dispatch's NON_DELEGABLE clause, `docs/SQLITE_INDEX_DESIGN.md`
was not read. The only assumption taken from the dispatch about the
sibling relational index: **one table per journal event type, named after
the event, columns = the event's fields** (from `journal.py`'s
`SHAPES`/TypedDicts, i.e. tables `exit`, `dispatch`, `return`,
`rule_fire`, `check_executed`, `claim_recorded`, `consumer_check`, each
with implicit SQLite `rowid` plus the event's own `ts`/`run_id`/fields),
**plus `artifact_ref(run_id, path, mode, source_event_rowid)`** where
`mode ∈ {read, invoke, mutate}`. Everything below is built *on top of*
those tables, not instead of them. Queries 1 and 2 (§3) read the
per-event-type tables directly — no edge table needed. Queries 3 and 5
need a small materialized `edge` table, decided in §4.

### Node types (6), each traced to the journal field that produces it

| Node | Identity | Source event(s) / field(s) | Cited by |
|---|---|---|---|
| **Task** | `run_id` | The common `run_id` field every event carries (`journal.py` `validate_event`, lines 124–126). **Proxy, not a dedicated event** — see gap below. | Q4, Q5 |
| **Agent** | agent identifier string, incl. `"MAIN"` and the Z3′ sentinel `"none"` | `dispatch.agent_id`; `claim_recorded.author`; `claim_recorded.actor`; `return.agent_id` | Q2, Q4 |
| **Dispatch** | surrogate: `(run_id, agent_id, ts)` (no `dispatch_id` field exists — gap, noted) | `dispatch` event: `agent_id, role, framing, payload_fields, output_path` | Q4 |
| **Claim** | `claim_id` | `claim_recorded.claim_id`; `check_executed.claim_id` / `.falsifies` | Q2, Q3, Q5 |
| **Evidence** (doubles as "Fact" — see below) | check_executed row identity (rowid once loaded) | `check_executed` event: `claim_id, falsifies, mechanism, command, expected, observed, pre_fix_result, hub_integrity_for` | Q3, Q5 |
| **Artifact** | `path` | **Not re-derived here** — read from the sibling's `artifact_ref(run_id, path, mode, source_event_rowid)` table | Q1, Q3, Q5 |

**Why no separate `Fact` node.** K1/K6 talk about "a fact later found
stale" as if fact and evidence were distinct. They are not, in this
journal: the only place an observed value is recorded is
`check_executed.observed` (or `claim_recorded.text` for a judgment claim
with no command). Splitting "the check that ran" from "the fact it
established" would be two nodes with one query between them — exactly
the pattern this dispatch calls out as a self-inflicted graph. `Evidence`
plays both PROV roles (`activity` when queried as "what ran", `entity`
when queried as "what was found") off the same row.

**Why `Task = run_id` is a proxy, not a first-class node.** There is no
`task_declared` event. A task's boundary is recovered from the first
`exit{algorithm="C"}` row for a `run_id` onward. This mostly works
because one `Journal` instance (one `run_id`) is meant to back one task
— but `stages.gate()`'s own C·4 split (`ancient_games/stages.py` lines
103–114) recurses into `gate(Ctx(), sub, journal, registry)` **passing
the same `journal` object**, so a single `run_id` can contain several
nested Gate→Guard→Corroborate→Filter→Prove sub-plans (one per
`PLAN_NEEDED[]` group). `run_id`-scoping is exact for the eight spec
cases (§10, none of which exercises C·4) but is not exact in general.
This is disclosed, not fixed — no listed query (Q4 included) needs
sub-plan-level scoping today. See §9.

**Why the code import/call graph is *not* a second graph, decided.**
(Read #6, `frame-research-as-software-engineering.md`.) Software has an
import/call graph Guard *could* use for `hub`/`stakes` on a code change
(does editing file A transitively affect a registered hub via imports?).
Guard does not do this today: `registry.py`'s `direct_matches` /
`consumer_matches` match an action's *declared* `ArtifactRef.path` /
`.consumers` against hand-written registry rows (`dir`/`file`/`callable`/
`action` patterns) — a purely declarative lookup, never a graph
traversal. K4: this answered every hub question in T1/T2/T3 without any
import scan. **Decision: if a transitive-import hub question ever
arrives, its edges belong in the *same* `edge(src, dst, kind, run_id,
source_rowid)` table (§4) as a new `kind='imports'`, populated by a new
*producer* — an AST import scan or `import-linter`'s contract-check
output — not a new graph, not a new engine, and not a journal event
(import edges describe repo structure at a commit, not something an
agent did).** `source_event_rowid` would be `NULL` for these rows since
they don't originate from a journal event. This is not built now because
no listed query needs it (§9 names it as a follow-on, not a requirement).

### Edge kinds

PROV vocabulary used as edge-kind values in one table, not as an RDF
predicate set (wave 2 MERGED.md, "Provenance model").

| Edge kind | Direction (`src → dst`) | Derivation | Cited by |
|---|---|---|---|
| `wasAttributedTo` | Claim → Agent | `claim_recorded.author` (direct FK, no join needed) | Q2 |
| `wasGeneratedBy` | Claim → Dispatch (or → Task when `author="MAIN"`, since MAIN has no `dispatch` event) | join `claim_recorded.author = dispatch.agent_id` within the same `run_id` | Q4 |
| `wasGeneratedBy` | Evidence → Dispatch (or → Task) | **approximated** — `check_executed` carries no `agent_id` field (gap, unlike `claim_recorded.author`). Approximated by append-order adjacency to the nearest preceding `return` event in the same `run_id`, because `Journal.ingest_return` (`journal.py` lines 218–232) appends `check_executed`/`claim_recorded` rows immediately after the `return` row, in one call, in file order. **Proposed missing field: `check_executed.agent_id`**, would remove the approximation. | Q3, Q5 (attribution only; not needed for the recursive traversal itself) |
| `wasDerivedFrom` | Claim → Evidence | `check_executed.falsifies == claim.claim_id` (also `.claim_id`) | Q3, Q5 |
| `wasDerivedFrom` | Claim → Artifact | `claim_recorded.evidence_ref` when `evidence_type='file:line'` | Q5 |
| `used` | Evidence → Artifact | join on `artifact_ref.source_event_rowid = check_executed.rowid`, `mode IN ('read','invoke')` | Q3, Q5 |
| `wasGeneratedBy` | Artifact → Dispatch (or → Task) | `artifact_ref.mode='mutate'`, via `source_event_rowid` | Q1 (degree only counts these + `invoke`), Q3 |
| `verifies` (non-PROV, named for the spec's own dual-role rule) | Evidence → Artifact | `check_executed.hub_integrity_for` (V3.6 §7, AA3′ — "one event, two roles") — the same row already counted once under `used`; `verifies` is a second, distinct label on the identical row, per the spec's own instruction that this is "not a new event type... the same journaled event can satisfy both" requirements | Q3 (T1 worked example, §7 below) |

**`actor` is a node property, not an edge.** `claim_recorded.actor`
records *whose work the claim is about* (Z3′), not delegation. It is not
forced into `wasAttributedTo` (that is `author`) or `actedOnBehalfOf`
(that would claim agent-to-agent delegation, which is not what `actor`
means). Stored as a plain column on the Claim node; read directly by Q2.

**`actedOnBehalfOf` is not modeled.** No listed question needs
agent-to-agent delegation: every dispatch in this framework is
MAIN/orchestrator → one agent, never agent → agent (B·3, `stages.py`
lines 473–481, dispatches one file per source, no chaining). Per this
dispatch's own rule, an edge kind with no query is a finding against the
design, so it is left out and named here instead of built quietly.

**`artifact_ref` derivation, and a second gap.** The sibling table's rows
come from three places, per this dispatch's isolation note: (a)
`consumer_check.ref` (the list of non-read paths D·2 checked —
`stages.py` `_ref_paths`, lines 177–178: `[r.path for r in refs if
r.mode != "read"]`, `guard()` line 194); (b) `dispatch.output_path`
(`mode='mutate'`, the artifact the dispatch is meant to produce); (c)
`claim_recorded.evidence_ref` when `evidence_type='file:line'`
(`mode='read'`, citing evidence never mutates it). **Gap:** (a) collapses
`invoke` and `mutate` into "non-read" at the point `_ref_paths` is
called — `consumer_check` events do not carry per-path mode, so the
sibling table's `mode` column cannot always distinguish `invoke` from
`mutate` for consumer-check-derived rows from the journal alone.
Flagged, not fixed here (§9); it does not block Q1, which only needs
`mode != 'read'`.

## 3. Queries

One per framework question (K1) plus the two named in the TEMPLATE.
Tables assumed per §2's isolation note; `edge` is this document's own
materialized table, defined in §4.

### Q1 — Hub degree (Guard, D·2)

```sql
SELECT path AS artifact, COUNT(*) AS degree
FROM artifact_ref
WHERE mode IN ('invoke', 'mutate')
GROUP BY path
ORDER BY degree DESC;
```

No `edge` table needed — direct `GROUP BY` over the sibling's own table.
**Measured** (this document's own harness, `/tmp/.../scratchpad/kg-design/
_scratch_kg_measure.py`, deleted after use — see below): 3.65 ms over
20,000 synthetic `artifact_ref`-shaped rows, correctly surfacing an
injected hot path (`loop/program_db.jsonl`, 309 hits vs. a ~45-hit noise
floor) at the top. Consistent with wave 1's own MEASURED result for the
identical query shape (wave 2 MERGED.md, row 1 of the table).

### Q2 — Shared-source independence (Corroborate, B·1 self-join)

Replicates B·1 (a)'s self-exclusion (`stages.py` `_a_events`, lines
274–280, and Z3′'s `actor="none"` vacuous-inclusion rule), then asks the
graph question B·1 itself never asks: did two *counted* sources actually
cite the same underlying evidence?

```sql
SELECT a.claim_id, a.author AS agent_a, b.author AS agent_b,
       a.evidence_ref AS shared_evidence_ref
FROM claim_recorded a
JOIN claim_recorded b
  ON a.claim_id = b.claim_id
 AND a.rowid < b.rowid
 AND a.author <> b.author
WHERE (a.actor = 'none' OR a.author <> a.actor)
  AND (b.actor = 'none' OR b.author <> b.actor)
  AND a.evidence_ref = b.evidence_ref
  AND a.evidence_ref <> '';
```

**Measured:** 3.70 ms over 5,000 synthetic `claim_recorded` rows (1,000
distinct claims, 7 agents, 20% of rows sharing one of 3 "secretly common"
evidence refs) — 400 correctly-flagged pairs.

### Q3 — Transitive staleness (K6)

No event marks a claim "stale" directly (gap, disclosed — the framework
has no `superseded_by` field). **Operational definition used here:**
re-verification contradicts an earlier finding for the same claim.

**3a — detect a stale claim** (no recursion):

```sql
SELECT c1.claim_id, c1.rowid AS earlier, c2.rowid AS later,
       c1.observed AS old_value, c2.observed AS new_value
FROM check_executed c1
JOIN check_executed c2
  ON c1.claim_id = c2.claim_id AND c1.rowid < c2.rowid AND c1.observed <> c2.observed;
```

**3b — everything that transitively rests on the stale claim/evidence**,
over the materialized `edge` table (§4), walking `wasDerivedFrom` /
`used` / `wasGeneratedBy` backward from the stale node:

```sql
WITH RECURSIVE affected(node) AS (
  SELECT :stale_node                          -- e.g. 'claim:six-are-dead'
  UNION
  SELECT e.src FROM edge e JOIN affected a ON e.dst = a.node
   WHERE e.kind IN ('wasDerivedFrom', 'used', 'wasGeneratedBy')
)
SELECT * FROM affected WHERE node <> :stale_node;
```

**Cycle guard (the gotcha, verified against my own schema, not just
trusted from wave 2's report):** a 3-node cycle was injected
(`d9000→d9001→d9002→d9000`) into a synthetic edge set and queried two
ways:

- *Broken* — adding a `depth` column inside the recursive term (`reach(node,
  depth)`, `depth < 50` bound) defeats `UNION`'s row-level dedup because
  `(node, depth)` never repeats: **51 rows returned, not 3** — the query
  keeps re-walking the 3-node cycle up to the depth cap.
- *Fixed* — a plain `reach(node)` term with no depth column: `UNION`
  dedups on `node` alone and the cycle correctly terminates at exactly
  the 3 cycle members.

This reproduces wave 2's documented gotcha (MERGED.md, "Design rules for
the recursive CTE", item 1) as an independent, adversarial measurement
against this document's own query shape, not a re-assertion of the prior
finding. **Both directions of `edge` are indexed** (`ix_edge_src`,
`ix_edge_dst`) — required, per wave 2's own note that the 598 ms/400k-edge
number assumed indexes; unindexed is a scan.

**Measured (this harness):** 3.94 ms over 5,002 edges (a 5,000-node
chain); 89.06 ms over a 100,000-edge chain. Order-of-magnitude consistent
with wave 2's own MEASURED numbers for the same query shape (5.7 ms @ 2k
dispatches, 89 ms @ 20k, 598 ms @ 100k dispatches / 400k edges) — not
independently re-measured at the 100k-dispatch/400k-edge scale here;
cited from wave 2, not re-derived.

### Q4 — Dispatch lineage for a task

No recursion: dispatches don't dispatch dispatches (B·3 issues each
category-(a) source directly, `stages.py` `dispatch_source`, one file per
agent, no chaining).

```sql
SELECT d.agent_id, d.role, d.framing, d.output_path, d.ts,
       r.fields AS return_fields,
       (SELECT group_concat(cr.claim_id)
          FROM claim_recorded cr
         WHERE cr.run_id = d.run_id AND cr.author = d.agent_id) AS claims_authored
FROM dispatch d
LEFT JOIN return r ON r.run_id = d.run_id AND r.agent_id = d.agent_id
WHERE d.run_id = :run_id
ORDER BY d.ts;
```

**Caveat**, stated rather than solved: a C·4 group split shares one
`run_id` across several nested sub-plans (§2). This query returns every
dispatch under the `run_id`, not scoped to one sub-plan; no listed query
needs sub-plan scoping today (§9). **Not separately measured** — at K3's
real scale (fewer than ~60 events per run across T1/T2/T3), this is an
indexed equality join; reasoned to be sub-millisecond, not benchmarked,
because no case in this repo's actual traces approaches a scale where it
would matter.

### Q5 — "Which facts does this recommendation rest on"

Same shape as Q3b, opposite direction: from a claim, walk *outward* to
what it derives from, instead of inward to what depends on it.

```sql
WITH RECURSIVE rests_on(node) AS (
  SELECT 'claim:' || :claim_id
  UNION
  SELECT e.dst FROM edge e JOIN rests_on r ON e.src = r.node
   WHERE e.kind IN ('wasDerivedFrom', 'used')
)
SELECT * FROM rests_on WHERE node <> 'claim:' || :claim_id;
```

**Not separately re-measured** — structurally identical CTE to Q3b (same
table, same indexes, opposite edge direction); reasoned to have the same
cost profile, not independently benchmarked. Disclosed as reasoned, not
measured.

**Worked example against a real spec case** (V3.6 SPEC §10, T1,
`journal-untouched` claim): seeding `rests_on` at `claim:journal-untouched`
should return exactly `{evidence:check_executed#hash-compare,
evidence:check_executed#git-diff-scope, artifact:loop/program_db.jsonl}`
— matching §10's own table (`n_available=2`, two distinct mechanisms,
hub=`loop/program_db.jsonl`). See §7 for this run as a test case.

## 4. How it sits on the relational index

**Decision: a materialized `edge(src, dst, kind, run_id, source_rowid)`
table, not a view over the per-event-type tables — for Q3 and Q5 only.**
Q1 and Q2 read the per-event-type/`artifact_ref` tables directly; no
`edge` table involved for them (§3).

**Measured trade-off**, purpose-built for this decision: the same
recursive query, same result, run against (a) a `VIEW` that
`UNION ALL`s two heterogeneous source tables remapped to `(src, dst,
kind)`, vs. (b) a materialized copy of that view with `(src)`/`(dst)`
indexes, both over ~50,000 derived edges:

| Form | Time | Result |
|---|---|---|
| View (`UNION ALL` over 2 base tables, no index on the view) | 58.05 ms | 2 rows |
| Materialized + indexed | 0.07 ms | 2 rows |

Same query, same answer, ~800× apart. SQLite cannot maintain a
cross-table index on a `UNION ALL` view, so every recursive step re-scans
and re-unions the full underlying tables; the materialized table gets a
real B-tree on both `src` and `dst`, which is what wave 2's own
598 ms/400k-edge number assumed ("indexed both directions... without them
it's scans" — MERGED.md, cycle-guard rule 3).

**Rebuild = the index rebuild.** The journal is append-only and the
sibling's per-event-type tables are, per the isolation assumption, the
canonical rebuild target from the whole JSONL file. `edge` is rebuilt in
the same pass, as one more `INSERT ... SELECT` step after the
per-event-type tables are populated — not a second pipeline, no
incremental edge maintenance. This matches the evidence-KG skill's own
rule 9 verbatim: "Build a new graph from the whole corpus. Never
incrementally patch a production graph unless the importer proves exact
update and provenance-merge semantics" (`~/.codex/skills/
evidence-knowledge-graph/SKILL.md`, "Non-negotiable controls", item 9).
No importer here proves incremental-update correctness, so none is
attempted; a full rebuild from an append-only log at K3's scale (tens of
events per run) is cheap enough that incrementality buys nothing.

## 5. Flip conditions as tests

All three carried over unchanged from wave 2 MERGED.md (the "Conditions
that would flip the verdict" list) — stated here as things that could be
checked, not just watched for:

1. **A whole-graph iterative question arrives** (centrality, community
   detection, weighted transitive importance — "PageRank-shaped", K1).
   Test: a new query spec cannot be expressed as a `WITH RECURSIVE` term
   whose base case and recursive step both terminate in a bounded number
   of joins over the edge table (i.e. it needs a global fixed point over
   all edges, not a bounded traversal from a named seed). If such a query
   spec is proposed and this test fails, that is the trigger — not a
   vague sense that "the graph feels bigger now."
2. **Edge count or depth exceeds ~200,000 edges / depth 20,000** — two to
   three orders of magnitude above K3's real volume (fewer than ~60
   events per run). Test: `SELECT COUNT(*) FROM edge` run as part of the
   same rebuild step that populates `edge` (§4); if it exceeds 200,000,
   or the longest chain found by `Q3b`/`Q5`'s recursion exceeds depth
   20,000 (countable via a one-off `WITH RECURSIVE ... (node, depth)`
   probe — the depth-column-defeats-dedup gotcha from §3 is fine to
   invoke deliberately for a bounded, one-shot depth *measurement*, just
   never for correctness-critical traversal), fail loud and re-open this
   design.
3. **An external RDF / PROV-O interoperability requirement arrives** —
   i.e. something outside this framework needs to consume these edges as
   actual triples, not read them out of SQLite. Test: any accepted
   requirement whose acceptance criterion names RDF, SPARQL, or PROV-O
   export.

**First response if any of these flip: NetworkX over an exported edge
list** (`SELECT * FROM edge`), in-memory, one-shot — not a graph
database, not a rewrite of this design (wave 2 MERGED.md, "Follow-on").

## 6. Relationship to the evidence-knowledge-graph skill

`~/.codex/skills/evidence-knowledge-graph/SKILL.md` — EJ's in-house skill
— targets a different corpus (`knowledge/raw|reconciled|structured/`,
research reports turned into atomic sourced assertions) with a
staging/promotion ceremony (validate → stage → verify → atomically
replace production, with manifests and backups) built for a corpus that
is *authored*, not append-only-logged.

**Reused, deliberately:**
- The evidence-lineage discipline — "graph hit → structured record →
  exact source locator → authoritative source... never cite a graph hit
  as final proof" (SKILL.md, "Core rule"). This design's queries never
  return a bare graph node as an answer; every `Evidence`/`Claim`/
  `Artifact` result resolves to an exact `check_executed.command` /
  `claim_recorded.evidence_ref` / `artifact_ref.path`, i.e. a row a human
  or agent can go read.
- Rule 9 (rebuild from the whole corpus, never incrementally patch) —
  directly drives §4's rebuild-with-the-index decision.
- The graph-as-tables decision itself: `ctxgraph` is already "plain
  SQLite + FTS5 with a hand-rolled hop-limited BFS" (wave 2 MERGED.md).
  `WITH RECURSIVE` with a plain (non-depth) `UNION` term *is* a
  hop-limited BFS, expressed declaratively; nothing new is being
  invented, just applied to a different corpus.

**Not duplicated:**
- **No FTS5 / token search.** The skill's queries are keyword discovery
  over free-text research reports. Every query in §3 here is by exact ID
  or path (`claim_id`, `run_id`, `path`) — there is no natural-language
  retrieval need named by any framework question.
- **No embeddings / semantic layer.** Same reason — nothing here is
  "find claims like this one"; it's "resolve this exact provenance
  chain."
- **No staging/promotion/manifest ceremony.** The skill's corpus is
  hand-curated and promoted deliberately; this journal is a single
  append-only writer (`Journal`, one process) with no competing writers
  to reconcile and no "wrong" state to guard against beyond a full
  rebuild from the file.
- **No `--emit-same-as-edges` entity-identity layer.** Nothing here needs
  cross-corpus same-as resolution; `claim_id`/`run_id`/`path` are already
  the framework's own stable identifiers.

## 7. Test plan

Run each query against the eight spec cases' events (V3.6 SPEC §10: T1,
T2, T3, Case 1, Case 2, Case 3, (i), (ii)) as a table-driven test loading
each case's traced events into the schema.

| Query | Case | Input | Expected |
|---|---|---|---|
| Q1 hub degree | T1 | `guard()` mutate `loop/program_db.py` → R7∪R4 | `loop/program_db.jsonl` degree ≥1 (the D·2 hub hit) |
| Q1 hub degree | Case (ii) | R2 hub match | `eval/holdout_access.log` present with degree ≥1 |
| Q2 shared-source | T3 | 3 co-equal authors, `actor=none`, 3 distinct framings, no shared `evidence_ref` | 0 rows — genuinely independent, matches `SOURCES(n_available=3, ..., reconciliation="disagree")` |
| Q2 shared-source | T1 `six-are-dead` | MAIN's own `claim_recorded` (`author=actor=MAIN`) plus historian's | MAIN's row excluded by the `author≠actor` filter on both sides — same exclusion `count_sources`/`_a_events` already applies (§3) |
| Q3a detect stale | synthetic (no real case has one) | two `check_executed` rows, same `claim_id`, differing `observed` | 1 row flagged — **INSUFFICIENT_DATA note:** none of the 8 spec cases re-verifies a claim with a contradicting result; this branch is untested against real traces, only against synthetic data built for this purpose |
| Q3b transitive dependents | adversarial 3-node cycle (§3) | `d9000→d9001→d9002→d9000` | exactly 3 nodes, not 51 (cycle-guard regression test) |
| Q4 dispatch lineage | Case 3 | 2-pass V7 resume, `liquidity-module-coder` + docstring dispatch | both dispatches returned for the `run_id`, first-pass `CAPPED` claim and second-pass `SOURCES` claim both attributed to the same `agent_id` |
| Q5 rests-on | T1 `journal-untouched` | dual-role hash-compare event + git-diff-scope event | `{evidence:hash-compare, evidence:git-diff-scope, artifact:loop/program_db.jsonl}` — matches §10's own table exactly (worked in §3, Q5) |

**Cycle-guard test:** the §3/Q3b adversarial case, asserted as a
regression test: `assert len(result) == 3`, not `> 3`. Already run once
during design (§3); re-run as part of accepting this design, not
re-derived from scratch by the implementer.

**Graph-answer-differs-from-naive-grep case:** T1's `six-are-dead` claim.
`grep -c '"claim_id": "six-are-dead"' journal.jsonl` (or a token search
over the same journal) finds **2** `claim_recorded` hits — MAIN's own
scan and the historian's. The graph query (Q2, applying B·1 (a)'s
`author≠actor` exclusion) correctly reports **1** countable source,
matching the spec's own `CAPPED(..., delivered=1, remedy=
add-differently-framed-source)` verdict (§10, T1). A naive grep overcounts
by exactly the self-authored, self-judged claim that B·1 excludes by
design — this is the concrete case this dispatch's own rigor standard
asks for: a graph answer that is *not* reproducible by grep, because it
encodes a rule (self-exclusion), not just presence.

## 8. When to build it

**Trigger:** the first time a real framework run needs Q3 or Q5 across
more than one `run_id` — i.e. the first time a claim in one task cites,
as its evidence, an artifact a *different* task's dispatch produced. Q1
and Q2 are cheap enough (direct queries over tables the sibling index
already builds) that they cost nothing extra to wire in whenever the
per-event-type tables exist; only the `edge` table (§4) is genuinely
extra machinery, and it is only needed for cross-kind recursive
traversal (Q3, Q5).

**Not worth building today:** per K3, three real runs (T1, T2, T3)
produced fewer than ~60 events each, and no run has yet cited another
run's artifact as evidence. The value case here is explicitly
cross-run provenance (K3), which has not yet occurred in this repo's own
history — so `edge` has no real data to be built from yet. Building it
now would mean testing it exclusively against synthetic data (as this
document did), which is exactly the failure mode wave 2 flags in
`loop/graph_memory.py` and `.ctxgraph/graph.db`: correct and unused. The
per-event-type tables (Q1, Q2) are worth building whenever the sibling
index is built, since they cost nothing beyond it; `edge` (Q3, Q5) should
wait for the first real cross-run citation.

## 9. Open questions / spec follow-ons

1. **`check_executed` has no `agent_id`/actor field** (unlike
   `claim_recorded.author`). The `wasGeneratedBy(Evidence, Dispatch)`
   edge is approximated by append-order adjacency to the nearest
   preceding `return` event, which is correct for every case traced via
   `Journal.ingest_return` but not verified for a `check_executed` logged
   by a direct `journal.check_executed()` call outside that path (D·4's
   own hub-integrity tripwire, called by MAIN, not via `ingest_return` —
   T1's worked example, V3.6 SPEC §7). Proposed spec follow-on: add
   `check_executed.agent_id: str` (default `"MAIN"` for spine-run
   tripwires).
2. **`consumer_check.ref` does not carry per-path mode.** `_ref_paths`
   collapses `invoke`/`mutate` to "non-read" before the event is written
   (`stages.py` lines 177–178, 194), so the sibling `artifact_ref` table
   cannot recover the original per-path mode for consumer-check-derived
   rows. Does not block any query in §3 (Q1 only needs `mode != 'read'`),
   flagged for the sibling's own design in case it matters there.
3. **`Task = run_id` is not exact under a C·4 split** (§2). No listed
   query needs sub-plan scoping yet; if one arises, the natural fix is
   windowing dispatch/claim rows between consecutive `exit{algorithm='C'}`
   rowids within a `run_id`, not a new `task_id` field — noted, not
   designed, since nothing needs it.
4. **The code import/call graph** (§2) is deliberately not built. If
   Guard is ever asked "does this edit reach a hub transitively through
   imports," the follow-on is a `kind='imports'` addition to `edge`,
   populated by an AST import scan or `import-linter`'s contract JSON —
   same table, new producer, no new engine.
5. **Q3a's staleness detection is untested against real data** (§7) —
   none of the 8 spec cases re-verifies a claim with a contradicting
   result. This is `INSUFFICIENT_DATA`, not `NOT_DETECTED`: the mechanism
   is exercised only by synthetic input in this design's own harness.

## 10. Sources

- `/tmp/claude-1000/-home-smoke01-dev-seza/a1db3155-9529-49c3-b157-9a385a8c7b55/scratchpad/store-research/wave2-kg/MERGED.md` — binding wave-2 verdict (no engine, edge table + CTE, PROV vocabulary, measured CTE costs, cycle-guard gotchas, flip conditions).
- `/home/smoke01/dev/ancient-games/ancient_games/journal.py` — the seven event TypedDicts and `SHAPES`, `Journal.append`/`ingest_return`/`read_events`.
- `/home/smoke01/dev/ancient-games/ancient_games/stages.py` — `count_sources`, `_a_events`, `guard()`, `dispatch_source`, `corroborate()`.
- `/home/smoke01/dev/ancient-games/ancient_games/registry.py` — `direct_matches`, `consumer_matches`, `lookup` (D·2/D·2′ hub union, purely declarative, no import graph).
- `/home/smoke01/dev/ancient-games/ancient_games/ctx.py` — `ArtifactRef`, `CTX_META` (what each ctx property is set/consumed by).
- `/home/smoke01/dev/ancient-games/ancient_games/lints.py` — `lint_hub_touched_without_tripwire`, `lint_corroboration_capped` (what Guard/Corroborate actually check today).
- `/home/smoke01/dev/ancient-games/SPEC.md` — §2 ctx, §4 B·1/D·2′, §7 trace journal (dual-role rule, AA3′), §10 T1/T2/T3 worked traces used as test cases in §7.
- `/home/smoke01/.codex/skills/evidence-knowledge-graph/SKILL.md` — EJ's in-house KG skill; §6's reuse/non-duplication decisions.
- `/home/smoke01/.claude/projects/-home-smoke01-dev-seza/memory/frame-research-as-software-engineering.md` — the code-import-graph question this document reopens and answers in §2.
- This document's own measurements: `_scratch_kg_measure.py` and a second, unnamed inline script for the view-vs-materialized comparison (§4), both run under `/tmp/claude-1000/-home-smoke01-dev-seza/a1db3155-9529-49c3-b157-9a385a8c7b55/scratchpad/kg-design/`, **deleted after use, disclosed here** per this dispatch's NON_DELEGABLE clause. Raw numbers: hub degree 3.65 ms/20k rows; shared-source join 3.70 ms/5k rows; staleness chain 3.94 ms/5k edges, 89.06 ms/100k edges; cycle-guard broken=51 rows / fixed=3 rows; view=58.05 ms vs. materialized+indexed=0.07 ms over the same 50k-edge result.

### Deviation from the generic harness reminder

This session's harness reminder ("do your work through Bash wherever it
can accomplish the job... use dedicated tools only when Bash genuinely
cannot") is outranked by this dispatch's own `PRECEDENCE` clause. All
source reading was done with the `Read` tool (not `cat`/`sed`) and this
document was written with `Write` (not a heredoc), per the dispatch's own
instructions for a research/design task; only the ad hoc SQLite
measurements in §3/§4 were run through `Bash`, since that is what running
Python actually requires. Noted per the same clause's own requirement,
matching the pattern in `SPEC.md` §12 item 11.
