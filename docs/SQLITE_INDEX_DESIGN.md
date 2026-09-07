# SQLite index — design

Domain: Python 3.12 stdlib `sqlite3` (3.45.1, matches the running
environment — verified: `python3 -c "import sqlite3;
print(sqlite3.sqlite_version)"` → `3.45.1`). The Ancient Games' only
durable record is the append-only JSONL trace journal
(`ancient_games/journal.py`, §7) plus a set of lint functions
(`ancient_games/lints.py`, §8) that today read it as a Python list —
`events = journal.read()` — and re-scan it with list/set comprehensions on
every call. This document designs the disposable SQLite projection of that
journal so those scans become SQL, precisely enough to implement
`ancient_games/index.py` and its tests without re-deriving anything.

**Isolation note (read before anything else).** `docs/
KNOWLEDGE_GRAPH_DESIGN.md` already exists in this repo (written under a
sibling dispatch whose own isolation note says it did *not* read this
document, and took one assumption on faith: a table per journal event
type, named after the event, plus an `artifact_ref(run_id, path, mode,
source_event_rowid)` table). I did read it — Rule 4 ("check for an
existing skill/spec first... `looks orthogonal` is dangerous") applies to
a same-repo, freshly-written, structurally-coupled document, not only to
the dispatch's own numbered reading list, and ignoring a document that
explicitly declares a dependency on mine would be exactly the
context-loading failure Rule 4 warns about. Three places where I disagree
with, or had to independently correct, that document's assumptions are
called out explicitly where they arise (§2, §5, §9) — each backed by a
measurement I ran, not just a read. This is a deviation from my own
READ list (which did not name the KG doc); flagged per PRECEDENCE.

## 1. Purpose and non-goals

**Purpose.** Replace the journal-side portion of three lints that
currently take `events: list[dict]` and linear-scan it —
`lint_corroboration_capped`, `lint_hub_touched_without_tripwire`,
`lint_downstream_consumer_check_unrecorded` (`lints.py:99,128,147`) — plus
the three return-shaped lints that scan a `return` event's raw `fields`
(`lint_claims_without_evidence`, `lint_follow_on_without_disposition`,
`lint_evidence_after_verdict`, invoked from `run_all_on_plan`,
`lints.py:166-185`), with SQL over projections of the journal. Also
answer cross-run questions (§6) that a single `journal.read()` call
cannot cheaply answer because they require self-joins or aggregates
across many run_ids — wave 1's own measured strain point (a 6-line `jq`
self-join needing a whole-file slurp, no index, breaking under asymmetric
join conditions — `wave1-sqlite/MERGED.md` line 51).

**Non-goals, stated up front because this exact instruction says a table
nobody queries is a finding against the design that built it:**

- **Not the source of truth.** The JSONL journal remains authoritative.
  The index is derived, disposable, git-ignored, and rebuilt wholesale —
  never hand-edited, never the input to any decision the journal itself
  doesn't already support (wave 1 MERGED.md, convergent verdict, line 9).
- **Not agent-written.** Only the orchestrator's `rebuild()` call writes
  to it (wave 1 MERGED.md line 13; K1).
- **Not a completeness score.** No lint here is reinterpreted as a metric
  to optimize; each SQL query reproduces an existing Python predicate,
  verified against it (§7), not a new judgment.
- **Not an FTS store.** No lint or stated question in this repo does
  keyword/semantic retrieval over free text (`text`, `command_or_reasoning`,
  TEMPLATE bodies) — every real lint matches on an exact `claim_id`,
  `command` string, `author`, or path. No FTS5 table is built.
- **No `rule_fire` table.** `rule_fire` is a real, validated event shape
  (`journal.py` `SHAPES["rule_fire"]`, line 102) but has **zero write
  call-sites** — `Journal` has no `rule_fire()` convenience method (unlike
  every other event type, `journal.py:193-216`), and neither `stages.py`
  nor `lints.py` ever appends one (confirmed by grep: `grep -rn
  '"event": "rule_fire"\|\.rule_fire(' ancient_games/` returns nothing).
  SPEC.md itself calls it "the dormant promote/decay substrate for
  #19/#22, unchanged" (§7). Building a table for an event nothing writes
  and no lint reads would be exactly the self-inflicted graph this
  instruction warns about (`loop/graph_memory.py`, 631 lines, no query
  code — wave 2 MERGED.md line 29). Deferred; see §8.
- **No `artifact_ref` table justified by this repo's own lints** — none of
  the 9 lints in `lints.py` asks a hub-degree or shared-source question
  (confirmed by reading all 9; hub membership is resolved at Guard-time
  from the static `REGISTRY` table in `registry.py`, never from the
  journal). I build a best-effort `artifact_ref` projection anyway,
  *only* because `docs/KNOWLEDGE_GRAPH_DESIGN.md`'s Q1/Q3/Q5 already
  depend on it — and I found, by running it, that the derivation doesn't
  do what that document's own test plan expects (§2, §9). That is a
  finding against the *sibling* document, disclosed here since this is
  where the table lives.

## 2. Journal → projection mapping

One table per journal event type that is actually written, columns =
that event's fields verbatim (`journal.py` `SHAPES`, lines 98-112), plus
three derived/exploded tables where a lint reads *inside* a compound
field rather than the field itself.

| Table | Fed by (event) | Columns | Notes |
|---|---|---|---|
| `dispatch` | `dispatch` | `run_id, ts, agent_id, role, framing, payload_fields_json, output_path` | `payload_fields_json` = `json(payload_fields)` — a list of field **names** sent, never values (`journal.py:198-200`). No `ctx_json` column: wave 1's `HYPOTHESIS_TABLES.md` (line 5) hypothesized one; the real `dispatch` event carries no ctx snapshot at all. Dropped, not carried forward as a stub. |
| `exit` | `exit` | `run_id, ts, algorithm, exit_type, exit_line, steps_fired_json, ctx_keys_set_json` | Verified `CREATE TABLE exit(...)` is legal, unquoted, in SQLite 3.45.1 (measured; `exit`/`return` are not reserved words there). |
| `claim_recorded` | `claim_recorded` | `run_id, ts, claim_id, author, actor, kind, text, evidence_type, evidence_ref, framing` | The **classified** (a)/(b) source events `count_sources` reads (§4 B·1) — distinct from raw `return.fields.CLAIMS`, below. `framing` is nullable (`journal.claim_recorded(..., framing=None)` is a real, exercised code path). |
| `check_executed` | `check_executed` | `run_id, ts, claim_id, falsifies, mechanism, command, expected, observed, pre_fix_result` | `expected`/`observed` stored as TEXT (the type union `str\|int\|float` is coerced to text at rebuild time; no lint or query in this document does numeric comparison on them — `count_sources` never inspects their values, only presence and grouping keys). **No `hub_integrity_for` column** — see finding below. |
| `consumer_check` + `consumer_check_ref` | `consumer_check` | `consumer_check(run_id, ts, consumer_check_id, answer, command_or_reasoning)`; `consumer_check_ref(consumer_check_id, ref_path)` — one row per path in `ref` | Normalized 1:N so the subset test `lint_downstream_consumer_check_unrecorded` needs (`set(e.ref) <= r`, `lints.py:152`) becomes a `GROUP BY ... HAVING COUNT(DISTINCT ...) = :k` query (§5), not a JSON-array containment scan. |
| `return` + `return_claim` + `return_follow_on` | `return` | `return(run_id, ts, agent_id, fields_json)`; `return_claim(run_id, agent_id, claim_id, kind, evidence_type, evidence_ref, framing)` — DERIVED, exploded from `fields_json -> '$.CLAIMS'` at rebuild time; `return_follow_on(run_id, agent_id, finding, disposition)` — DERIVED, exploded from `fields_json -> '$.FOLLOW_ON'` | `return_claim` is **not** the same population as `claim_recorded`: it holds every raw `CLAIMS` entry regardless of `classify_event`'s split (`journal.py:152-159`), including entries with `evidence_type ∈ {URL, (opinion)}` that `ingest_return` never turns into a `claim_recorded`/`check_executed` event at all (`journal.py:223-231` — an entry only becomes one of those two derived events; a `(opinion)`/`URL` entry stays *only* inside `return.fields.CLAIMS`). `lint_claims_without_evidence` reads the raw list (`run_all_on_plan`, `lints.py:176`), so `return_claim` — not `claim_recorded` — is its correct source. |
| `artifact_ref` (DERIVED, approximate — built for the sibling KG doc, not for any lint here) | `consumer_check.ref` (mode collapsed to `"invoke_or_mutate"` — `_ref_paths` already filters to `mode != "read"` before the event is written, `stages.py:177-178,194`, so the original mode is unrecoverable from this source); `dispatch.output_path` (mode forced to `"mutate"`, a modeling choice — the path an agent is dispatched to produce); `claim_recorded.evidence_ref` when `evidence_type='file:line'` (mode `"read"`) | **Measured finding, not reasoned:** built this exact table from T1's real journal and ran the KG doc's own Q1 (hub degree) against it. Result: `loop/program_db.jsonl` (the registry-resolved hub, R4) **never appears** — only `loop/program_db.py` (the directly-edited path) and `/agents/historian.md`/`loop/program_db.py:573,611,648` (dispatch output / evidence citation) do. The hub *name* is resolved by `registry.lookup()` from the action's declared `ArtifactRef.consumers` (`registry.py:122-133`, an in-memory field on `ActionInput`/`ArtifactRef`) and is **never itself journaled** — only the action's own `ref` path is, via `consumer_check`. This contradicts `KNOWLEDGE_GRAPH_DESIGN.md`'s own §7 test-plan row ("Q1 hub degree \| T1 \| ... \| `loop/program_db.jsonl` degree ≥1") as stated against journal-only data. See §9 for the missing-event proposal this implies. |

**Missing-event finding (SPEC.md §6 return contract, as the READ list
asked):** no event carries a full `artifact_refs` entry with its `mode`.
`ArtifactRef.mode ∈ {read, invoke, mutate}` (`ctx.py:44-52`) is set at
C·1/D·1 and consumed by `registry.lookup()`, but the only journal
event downstream of it, `consumer_check`, carries `ref: list[str]` with
mode already collapsed away (`_ref_paths`, `stages.py:177-178`) and
carries none of: the resolved `hub` name(s), `stakes`, or matched
`Match.row.id`s that `GuardExit`/`Lookup` compute (`registry.py:135-158`,
`stages.py:181-229`). **Proposed spec follow-on:** either (a) extend
`consumer_check` with two new fields, `hub: list[str]` and
`matched_row_ids: list[str]`, populated from the same `Lookup` object
`guard()` already has in hand at the point it calls
`journal.consumer_check(...)` (`stages.py:194`) — zero new call sites,
one existing call site gains two fields; or (b) a new event type,
`guard_result`, journaling `GuardExit`'s structured output verbatim. (a)
is smaller and reuses an existing, already-correctly-timed call site; I
recommend it, but do not implement it (out of scope — read-only
dispatch).

**Spec/code divergence finding (SPEC.md §7 vs. `journal.py`, as the READ
list explicitly asked me to check):** SPEC.md §7 (V3.6, AA3′) declares
`check_executed` gains `hub_integrity_for: str|null` (SPEC.md line 289,
294-297) implementing the "dual-role rule" — one event serving as both
D·4's hub tripwire and a (c) corroboration source. **`journal.py`'s
`SHAPES["check_executed"]` (lines 103-106) has no such field**, and
`validate_event`'s own `extra = set(event) - set(shape) - {...}` check
(line 146-148) would raise `ValueError` on any event carrying it. The
actual code achieves the same dual role differently, confirmed by reading
`tests/cases.py::_tripwire_run` (lines 59-62) and `run_t1`
(lines 127-130): a hub tripwire with a corresponding executable claim is
logged as `check_executed{claim_id=<claim>, falsifies=<claim>, ...}` (T1's
`journal-untouched`); a hub tripwire with **no** corresponding claim is
logged against a synthetic `claim_id=f"hub-integrity:{hub}"` (Case 3, (i),
Case (ii), via `_tripwire_run`). **This means `hub_integrity_for` is not
a real column** — I did not build it — **and `docs/
KNOWLEDGE_GRAPH_DESIGN.md`'s `verifies` edge (§2 there, citing
`check_executed.hub_integrity_for` at line 139) cites a field that does
not exist in this codebase.** The correct join for "is this
`check_executed` event also a hub tripwire" is: `claim_id LIKE
'hub-integrity:%'` (no claim) OR `claim_id` matches an entry in the
Plan's own `tripwires` dict values by `command` string equality (has a
claim) — both Plan-side, not derivable purely from the event's own
fields. Flagged for the sibling document; not fixed there (out of scope).

## 3. DDL

```sql
PRAGMA journal_mode=WAL;      -- wave 1: DDL/PRAGMA run exactly once, by the
PRAGMA busy_timeout=5000;     -- orchestrator, before any other connection exists
PRAGMA user_version=1;        -- wave 1: schema-version marker (bump on shape change)

CREATE TABLE dispatch (
  run_id TEXT NOT NULL, ts TEXT NOT NULL, agent_id TEXT NOT NULL, role TEXT NOT NULL,
  framing TEXT NOT NULL, payload_fields_json TEXT NOT NULL, output_path TEXT NOT NULL
);
CREATE INDEX ix_dispatch_run ON dispatch(run_id);
CREATE INDEX ix_dispatch_framing ON dispatch(framing);   -- cross-run reuse query, §6 Q1

CREATE TABLE exit (
  run_id TEXT NOT NULL, ts TEXT NOT NULL, algorithm TEXT NOT NULL, exit_type TEXT NOT NULL,
  exit_line TEXT NOT NULL, steps_fired_json TEXT NOT NULL, ctx_keys_set_json TEXT NOT NULL
);
CREATE INDEX ix_exit_run ON exit(run_id);
CREATE INDEX ix_exit_algo_type ON exit(algorithm, exit_type);  -- cross-run aggregate, §6 Q2

CREATE TABLE claim_recorded (
  run_id TEXT NOT NULL, ts TEXT NOT NULL, claim_id TEXT NOT NULL, author TEXT NOT NULL,
  actor TEXT NOT NULL, kind TEXT NOT NULL, text TEXT NOT NULL, evidence_type TEXT NOT NULL,
  evidence_ref TEXT NOT NULL, framing TEXT           -- nullable: journal.claim_recorded(framing=None) is real
);
CREATE INDEX ix_claim_recorded_claim ON claim_recorded(claim_id);   -- B·1 (a)/(b) lookup key
CREATE INDEX ix_claim_recorded_evref ON claim_recorded(evidence_ref);  -- §6 shared-evidence cross-check

CREATE TABLE check_executed (
  run_id TEXT NOT NULL, ts TEXT NOT NULL, claim_id TEXT NOT NULL, falsifies TEXT NOT NULL,
  mechanism TEXT NOT NULL, command TEXT NOT NULL, expected TEXT, observed TEXT, pre_fix_result TEXT
);
CREATE INDEX ix_check_executed_falsifies ON check_executed(falsifies);  -- B·1 (c) lookup key
CREATE INDEX ix_check_executed_command ON check_executed(command);     -- hub-touched-without-tripwire "ran" set

CREATE TABLE consumer_check (
  run_id TEXT NOT NULL, ts TEXT NOT NULL, consumer_check_id INTEGER NOT NULL,
  answer TEXT NOT NULL, command_or_reasoning TEXT NOT NULL
);
CREATE TABLE consumer_check_ref (
  consumer_check_id INTEGER NOT NULL, ref_path TEXT NOT NULL
);
CREATE INDEX ix_ccr_id ON consumer_check_ref(consumer_check_id);   -- both directions indexed
CREATE INDEX ix_ccr_path ON consumer_check_ref(ref_path);          -- (wave 2 rule 3), even though this
                                                                    -- is a bipartite table, not a graph edge

CREATE TABLE return (
  run_id TEXT NOT NULL, ts TEXT NOT NULL, agent_id TEXT NOT NULL, fields_json TEXT NOT NULL
);
CREATE INDEX ix_return_run ON return(run_id);
-- JSON1 generated columns for the two fields every return-shaped lint gates on presence of:
ALTER TABLE return ADD COLUMN has_template BOOLEAN
  GENERATED ALWAYS AS (json_type(fields_json, '$.TEMPLATE') IS NOT NULL) VIRTUAL;
-- (SQLite's ALTER TABLE cannot add a second GENERATED column referencing a JSON path
--  it hasn't seen before mid-migration in older releases; both are declared inline in the
--  CREATE TABLE in the real rebuild, not via ALTER — the above is illustrative of what
--  a version bump would add if the base table pre-existed. wave 1, MERGED.md line 37.)

CREATE TABLE return_claim (        -- DERIVED, exploded from return.fields_json->'$.CLAIMS' at rebuild time
  run_id TEXT NOT NULL, agent_id TEXT NOT NULL, claim_id TEXT, kind TEXT,
  evidence_type TEXT, evidence_ref TEXT, framing TEXT
);
CREATE INDEX ix_return_claim_claim ON return_claim(claim_id);

CREATE TABLE return_follow_on (    -- DERIVED, exploded from return.fields_json->'$.FOLLOW_ON'
  run_id TEXT NOT NULL, agent_id TEXT NOT NULL, finding TEXT, disposition TEXT
);

CREATE TABLE artifact_ref (        -- DERIVED, approximate — see §2 finding; built only for the
  run_id TEXT NOT NULL, path TEXT NOT NULL, mode TEXT NOT NULL, source TEXT NOT NULL
);                                 -- sibling KG design's Q1/Q3/Q5, not needed by any lint here
CREATE INDEX ix_artifact_ref_path ON artifact_ref(path);
CREATE INDEX ix_artifact_ref_run ON artifact_ref(run_id);

-- no `rule_fire` table: zero write call-sites, zero lint readers (§1). Its absence does not
-- break any query in this document or in docs/KNOWLEDGE_GRAPH_DESIGN.md (grep-confirmed:
-- neither references rule_fire).
```

Every rule above traces to a wave-1 finding: DDL/PRAGMA-once-by-the-
orchestrator and a non-zero busy timeout (both `MERGED.md`'s resolved
concurrency conflict, lines 15-25); absolute paths only (§4); `IS NULL`
never `= NULL` (`MERGED.md` line 38) — and its JSON1 extension, verified
here (§4/§5): `json_extract(...)` returns `NULL` for both an absent key
and a present `null` value, indistinguishable; `json_type(...) IS NULL`
is the correct "key absent" test (measured, this design's own harness:
`json_extract` gave `(None, 'null')` then `(None, None)` for present-null
vs. absent-key rows — only `json_type` told them apart).

## 4. Rebuild algorithm

```
rebuild(journal_path: str, db_path: str) -> Connection:
    1. _check_absolute(journal_path); _check_absolute(db_path)   # wave 1: relative path
       # -> two worktree processes silently diverge, no error (MEASURED)
    2. if exists(db_path): remove(db_path)      # drop-and-rebuild, not incremental (decided below)
    3. con = sqlite3.connect(db_path, timeout=5.0)
    4. con.create_function("REGEXP", 2, _regexp)  # needed by §5's follow-on-without-disposition;
       # sqlite3 has no builtin REGEXP — this is the standard stdlib registration pattern,
       # not persisted in the DB file, must be re-registered on every fresh connection
    5. con.executescript(DDL)                    # DDL run exactly once, by this one caller,
       # before any row is inserted or any other connection opens this file (wave 1 rule)
    6. events = Journal(journal_path).read()     # the one read of the source of truth
    7. with con:                                 # one transaction, single-writer (wave 1 rule 3/4)
         for ev in events: dispatch by ev["event"] to the matching INSERT (§2 table),
           exploding return.fields.CLAIMS -> return_claim, .FOLLOW_ON -> return_follow_on,
           consumer_check.ref -> consumer_check_ref (one row per path),
           feeding artifact_ref from the three derivation rules (§2); skip rule_fire (§1)
    8. return con
```

**Idempotent by drop-and-rebuild, not incremental — decided, cited:** the
sibling KG document already made and cited this call for the same journal
(`KNOWLEDGE_GRAPH_DESIGN.md` §4, quoting the evidence-KG skill's rule 9,
"never incrementally patch... unless the importer proves exact update and
provenance-merge semantics"); no importer here proves that, and at K4's
real scale (fewer than ~60 events per run) a full rebuild costs nothing
incrementality would meaningfully save. **Verified idempotent**: rebuilt
the same T2 journal into the same `db_path` twice in a row —
`check_executed` row count identical both times (4, 4).

**What triggers it:** before `prove()` calls `lints.run_all_on_plan`
(`stages.py:664-665`, where `journal.read()` already happens once per
`prove()` call today) — the natural drop-in point, since the index would
replace that read, not add a second one. Equally valid before any
cross-run query (§6), since rebuild is cheap relative to any question
worth asking across runs.

**Measured rebuild cost** (this design's own harness, `check_executed`
rows only, single-table insert loop, one transaction — see disclosure at
end of §7):

| n synthetic events | wall time |
|---|---|
| 1,000 | 66.1 ms |
| 10,000 | 115.4 ms |
| 100,000 | 650.8 ms |

Order-of-magnitude consistent with wave 2's own measured recursive-CTE
numbers at similar scales (K3: 5.7 ms/2k, 598 ms/400k edges) — SQLite does
not strain until far past any volume this repo's real journals have ever
reached (K4: three real runs, fewer than ~60 events each).

## 5. Lints as SQL

For each: which portion is SQL (journal-side) and which stays in Python
(Plan-side, since `Plan`/`PlanEntry`/`Claim`/`CappedClaim` are runtime
objects `prove()` passes in-memory — they are **never journaled** as
structured events; only the corroboration *source* events and the final
formatted exit-line string are. This is not a design choice available to
change here — it's what the journal actually contains).

### 1 — `claims-without-evidence` (fully SQL, per return event)
```sql
SELECT claim_id FROM return_claim
WHERE run_id = :run_id AND agent_id = :agent_id
  AND (evidence_type IS NULL
       OR evidence_type NOT IN ('command','file:line','URL','(opinion)')
       OR (evidence_type != '(opinion)' AND (evidence_ref IS NULL OR evidence_ref = '')));
```
Verified against the real `lint_claims_without_evidence` on T1's real
`return` event (0 findings both sides) and an adversarial injected
`{"evidence_type":"command","evidence_ref":""}` entry (1 finding,
`bad1`, both sides) — exact match, differential harness disclosed below.

### 2 — `follow-on-without-disposition` (fully SQL, needs `REGEXP`)
```sql
SELECT finding, disposition FROM return_follow_on
WHERE run_id = :run_id AND agent_id = :agent_id
  AND (disposition IS NULL
       OR NOT (disposition REGEXP '^(fixed|new-task|dismissed:\S.*|escalated:\S+)$'));
```
`sqlite3` has no builtin `REGEXP`; `rebuild()` registers one via
`Connection.create_function` (§4 step 4) implementing the identical
pattern `lints.DISPOSITION_RE` uses (`lints.py:15`). Verified: 8 rows
(`fixed`, `new-task`, `dismissed:out-of-scope`, `escalated:ej`,
`EJ decision`, `dismissed:`, `escalated:`, `NULL`) → flagged set exactly
`{EJ decision, dismissed:, escalated:, NULL}`, matching the Python regex
byte-for-byte.

### 3 — `scope-delta-missing-when-SCOPE-present` (SQL possible; **currently uncalled**)
```sql
SELECT d.agent_id
FROM dispatch d
WHERE d.run_id = :run_id
  AND json_type('["' || replace(d.payload_fields_json, '", "', '","') || '"]') IS NOT NULL  -- (illustrative; see note)
  AND EXISTS (SELECT 1 FROM json_each(d.payload_fields_json) WHERE value = 'SCOPE')
  AND NOT EXISTS (
    SELECT 1 FROM return r
    WHERE r.run_id = d.run_id AND r.agent_id = d.agent_id
      AND json_type(r.fields_json, '$.SCOPE_DELTA') IS NOT NULL   -- key-presence, not value-presence
  );
```
**Finding:** this lint is declared (`lints.py:54-58`), listed in
`LINTS` (`lints.py:160`), and unit-tested (`test_lints.py:39-42`), but
**`run_all_on_plan` never calls it** (`lints.py:166-185` calls the other

> **Superseded 2026-09-08:** `lint_scope_delta_missing` is no longer dead — it was wired into `run_all_on_plan` in `d149a57` (§8 order, run-scoped). The observation below was true when this design was written.
8; `grep -n lint_scope_delta_missing ancient_games/` shows only its
definition and its entry in the `LINTS` tuple). It is not journal-backed
in its current call convention either — its two Python parameters
(`return_fields`, `dispatch`) are the *payload dict* sent to an agent and
the *raw return fields dict*, not journaled events (dispatch's journaled
form only records field **names**, `payload_fields`, not the SCOPE
value itself — confirmed §2). The SQL above is offered as what *would*
work if this lint were wired into `run_all_on_plan` joining `dispatch`
and `return` by `(run_id, agent_id)`, using `json_type(...) IS NOT NULL`
for "key present" (verified distinct from `json_extract` — see §3). Not
built as a maintained query since nothing currently calls it; flagged as
a wiring gap, not fixed here.

### 4 / 9 — `schema-field-without-escape-value` / `return-field-without-escape-value` — **N/A, not journal data**
Both operate on the static `FIELDS`/`RETURN_CONTRACT` row lists in
`schema.py` (`lints.py:72-79`), a fixed Python table describing the
dispatch schema itself, never journaled, never varying per run. No SQL;
stays exactly as written.

### 5 — `evidence-after-verdict` — **SQL narrows, Python still parses**
```sql
SELECT run_id, agent_id, json_extract(fields_json, '$.TEMPLATE') AS template_text
FROM return
WHERE has_template;   -- the generated column from §3
```
The heading-order predicate itself (`lints.py:83-95`) is markdown-string
parsing — splitting lines, finding `## Verdict`'s index relative to
`## Findings` and everything after it — not tabular data. SQL supplies
the candidate rows; `lint_evidence_after_verdict`'s own body is
unchanged and still runs in Python over `template_text`.

### 6 — `corroboration-capped` — **(a)/(c) stay Python (Plan-only); (b)'s re-count is SQL**
- **(a)** `e.dispatched_total > CapState().cap` (`lints.py:106-108`) reads
  only `PlanEntry.dispatched_total`, a Plan field with no journal
  counterpart at all (it's `ctx.dispatch_count` at plan-construction
  time). Stays Python.
- **(b)** re-invokes `count_sources` when `cap.remedy` is a
  re-plannable one (`lints.py:114-118`). The journal-side portion —
  `count_sources`'s own n_a/n_b/n_c computation — is the SQL below,
  parameterized by `claim.actor`, `claim.kind`, `claim.n_required`
  **supplied by the Plan/Claim object**, not derivable from the journal
  alone (Case (ii)'s claim has *zero* journal events for it at all — its
  `kind`/`actor` exist only because `Claim("log-line-properly-certified",
  "judgment", ...)` was constructed as part of the plan, never journaled
  as a first-class fact; `count_sources`'s own signature already takes
  `claim: Claim` as a pre-resolved input, never re-derives `kind`/`actor`
  from events — `stages.py:293-303`).
  ```sql
  -- n_a: distinct framings among (a)-eligible claim_recorded rows
  SELECT COUNT(DISTINCT COALESCE(framing, '')) FROM claim_recorded
  WHERE claim_id = :claim_id
    AND (:actor = 'none' OR author != :actor);
  -- COALESCE(framing,''): plain COUNT(DISTINCT framing) silently drops NULL rows
  -- (standard SQL). Python's `len({e.get("framing") for e in events})` buckets every
  -- None into one entry. VERIFIED ADVERSARIALLY: two (a)-eligible claim_recorded rows,
  -- both framing=NULL -> Python n_a=1 (one-element set {None}); naive
  -- `COUNT(DISTINCT framing)` = 0 (both NULLs dropped); COALESCE-fixed = 1. Re-ran the
  -- full 9-claim, 8-case differential suite with the fix: 0 mismatches, before AND after
  -- adding a case with two null-framing sources (confirmed correct, not merely unbroken).

  -- n_b: MAIN's own qualifying claim_recorded, at most 1 (Z6')
  SELECT EXISTS(
    SELECT 1 FROM claim_recorded
    WHERE claim_id = :claim_id AND author = 'MAIN'
      AND evidence_type IN ('command','file:line') AND evidence_ref != ''
  ) AS n_b
  WHERE :actor != 'MAIN';

  -- n_c: only when kind='executable'; identical-command dedup FIRST (AA5'), then
  -- distinct-mechanism SECOND, composition order verified adversarially (see below)
  SELECT COUNT(DISTINCT mechanism) FROM (
    SELECT mechanism, MIN(rowid) AS first_row
    FROM check_executed
    WHERE claim_id = :claim_id AND falsifies = :claim_id
    GROUP BY command
  );
  ```
  The `n_c` query relies on SQLite's documented "bare column in an
  aggregate query" extension: when a `MIN()`/`MAX()` aggregate is present,
  a bare non-grouped column in the same `SELECT` is guaranteed to come
  from the row holding that extreme value (sqlite.org, "bare columns in
  an aggregate query") — here, `GROUP BY command` with `MIN(rowid)`
  guarantees `mechanism` comes from the first-seen row per command, which
  is exactly the dedup order AA5′ requires. **Verified adversarially**,
  not just cited: three `check_executed` rows —
  `(cmd1,hash-compare)`, `(cmd1,git-diff-scope)` [same command, should be
  discarded], `(cmd2,hash-compare)` [different command, same mechanism as
  the survivor] — Python `count_sources` gives `n_c=1`; this SQL gives
  `1`. A second case — `(cmdA,hash-compare)`, `(cmdB,hash-compare)`,
  `(cmdC,git-diff-scope)` — gives `n_c=2` both sides.
  **Full n_available = n_a + n_b + n_c**, exactly reproducing
  `count_sources` (`stages.py:293-360`): verified against **every claim in
  all 8 spec trace cases** (9 corroborated claims total — T2×2, T1×2,
  T3×1, Case 1×1, Case 3×1, (i)×1, Case (ii)×1; Case 2 never calls
  `corroborate`, correctly excluded), **0 mismatches**, plus the two
  adversarial constructions above. This is the differential-test oracle
  §7 formalizes.
- **(c)** `plan.exit_line` disclosure check (`lints.py:120-123`) reads a
  Plan field that, at the moment lints run, **has not yet been journaled**
  — `prove()` sets `plan.exit_line = pass_line` *then* reads the journal
  *then* runs lints *then* journals the `A` exit event only after
  (`stages.py:661-673`). A chicken-and-egg case even in principle: the
  event this check would want to query doesn't exist yet at lint time.
  Stays Python, necessarily, not just by convenience.

### 7 — `hub-touched-without-tripwire` — **Plan-side hub/tripwire stay Python; the "ran" set is SQL**
```sql
SELECT DISTINCT command FROM check_executed WHERE run_id = :run_id;
```
Replaces `{ev["command"] for ev in (events or []) if ev.get("event") ==
"check_executed"}` (`lints.py:133`); the rest of the lint (`e.hub`,
`e.tripwires.get(h)`, per `PlanEntry`) is Plan-only, never journaled.
**Verified** on T1's real events: Python set and SQL set both `{sha256sum
loop/program_db.jsonl, git status --short}` (size 2, exact match).

### 8 — `downstream-consumer-check-unrecorded` — **Plan-side stakes/hub/ref stay Python; the subset test is SQL**
```sql
SELECT consumer_check_id FROM consumer_check_ref
WHERE ref_path IN (:ref_1, :ref_2, ...)     -- the plan entry's own ref list
GROUP BY consumer_check_id
HAVING COUNT(DISTINCT ref_path) = :k;       -- k = len(ref); a non-empty result = "covered"
```
Replaces `any(set(e.ref) <= r for r in refs)` (`lints.py:152`) — a real
self-join/aggregate SQLite earns its place on (K2). **Verified** on T2's
real `consumer_check` event across 4 cases: exact match (both `True`),
subset match (both `True`), non-covering ref (both `False`), and the
empty-ref vacuous-true edge case (both `True`, matching Python's `set() <=
r` being trivially true) — all four agree.

### Documented-but-not-built (TEMPLATE asks for these explicitly; honesty about why none is a live table here)

- **Shared-source independence join** ("did two corroborating agents cite
  the same evidence?") — no lint in `lints.py` asks this; B·2's
  reconciliation note ("flag as suspect if framings were alike",
  `stages.py:176`) is an `[LLM]` judgment call, not a lint. The exact SQL
  is already specified and measured in `docs/KNOWLEDGE_GRAPH_DESIGN.md`
  §3 Q2 (self-join on `claim_recorded`, `a.evidence_ref = b.evidence_ref`)
  — not duplicated here to avoid the two-graphs-nobody-queries failure
  mode in reverse (one *query* built twice, maintained twice, drifting).
- **`rule_fire` promote/demote query** — `SELECT rule_id, COUNT(DISTINCT
  run_id) FROM rule_fire GROUP BY rule_id` (wave 1's own hypothesized
  shape, `HYPOTHESIS_TABLES.md` line 17) — not built: no table exists to
  query (§1, §3), because nothing writes the event.
- **Transitive-staleness CTE with cycle guard** — K3's own measured
  numbers (5.7 ms/2k, 598 ms/100k) are real, and I independently
  reproduced the cycle-guard gotcha on a synthetic 3-node cycle here
  (`d9000→d9001→d9002→d9000`-shaped: a `(node, depth)` recursive term
  produced 51 rows at a depth-50 cap instead of deduping to 3; a
  `(node)`-only term correctly gave exactly `{a,b,c}`). This lives in
  full, with worked examples against the real T1 trace, in
  `docs/KNOWLEDGE_GRAPH_DESIGN.md` §3 Q3/Q5 — not duplicated here for the
  same reason as the shared-source join. No lint in this repo asks a
  staleness question either (`ctx.stale_claims` is a schema-payload field
  telling a dispatched agent what to re-derive, `ctx.py:101`, not
  something any lint checks after the fact).

## 6. Cross-run questions the index answers that the journal list cannot cheaply

1. **Byte-for-byte framing reuse** (B·2's own rule, `stages.py:173`: "never
   issuing the same prompt twice, byte-for-byte or in substance" — an
   `[LLM]` judgment at plan time, with no after-the-fact audit today):
   ```sql
   SELECT framing, COUNT(*) AS n, group_concat(DISTINCT run_id) AS runs
   FROM dispatch GROUP BY framing HAVING n > 1;
   ```
2. **Exit-type distribution by algorithm, across every run this index has
   ever indexed** — a genuine aggregate a single `journal.read()` list
   comprehension answers once per file, but which the append-only journal
   itself never merges across files:
   ```sql
   SELECT algorithm, exit_type, COUNT(*) FROM exit GROUP BY 1, 2 ORDER BY 1, 2;
   ```
   Useful, e.g., to answer "how often does Prove FAIL vs PASS across
   every run recorded" without re-reading every `.jsonl` file by hand.
3. **Same evidence_ref cited by two different claim_ids, possibly across
   different runs** — a correlated-blind-spot check the framings
   enumeration (B·2) is designed to *prevent going in*, but nothing
   currently audits *after the fact*, across runs:
   ```sql
   SELECT a.claim_id, b.claim_id, a.evidence_ref
   FROM claim_recorded a JOIN claim_recorded b
     ON a.evidence_ref = b.evidence_ref AND a.rowid < b.rowid AND a.claim_id != b.claim_id
   WHERE a.evidence_type IN ('command','file:line') AND a.evidence_ref != '';
   ```
   (Distinct from the sibling KG doc's Q2, which asks the *same-claim*
   version of this question for the B·1 independence check specifically;
   this is the cross-claim, cross-run generalization, genuinely new here.)

## 7. Test plan

Every SQL lint above was checked, in this session, against the **real**
`ancient_games` code — not a reimplementation compared to itself — using
a differential harness that: builds all 8 real `§10` trace cases via
`tests/cases.py` (`run_t2`, `run_t1`, `run_t3`, `run_case1`, `run_case2`,
`run_case3`, `run_case_i`, `run_case_ii`), reads their real journals,
rebuilds the index from each, and asserts SQL output equals the real
Python function's output (`count_sources`, `lint_claims_without_evidence`,
the `ran`-set comprehension, the consumer-check subset comprehension) —
**never** a hand-written expected value substituting for either side.

| Test | Oracle | Result |
|---|---|---|
| `count_sources` (n_a+n_b+n_c) vs SQL, all 9 corroborated claims across 8 cases | `stages.count_sources` (real) | 0 mismatches |
| Adversarial: 2 (a)-sources with `framing=NULL` both | same | mismatch found (naive SQL undercounted by 1) → COALESCE fix → 0 mismatches, re-verified with a 3rd distinct-framing source added |
| Adversarial: identical-command-then-distinct-mechanism dedup order (AA5′), two constructions | same | match both times (n_c=1, n_c=2) |
| `hub-touched-without-tripwire` "ran" set, T1 | `lints.py:133`'s set comprehension (real) | exact match |
| `downstream-consumer-check-unrecorded` subset test, T2 | `lints.py:152`'s `any(set<=r)` (real) | exact match, 4 cases incl. empty-ref |
| `claims-without-evidence`, T1 real + 1 injected bad claim | `lint_claims_without_evidence` (real) | exact match both times |
| `follow-on-without-disposition` REGEXP, 8 rows incl. NULL | `lints.DISPOSITION_RE` (real) | exact match |
| Relative journal path / relative db path | `_check_absolute` pattern (`journal.py:162-165`, mirrored) | both rejected with `ValueError` |
| Rebuild idempotency, same journal, same db_path, twice | row-count equality | 4 == 4 |
| Recursive-CTE cycle guard (illustrative; owned by the sibling KG doc) | node-count | broken form: 51 rows / 3-node cycle; fixed form: exactly `{a,b,c}` |

**A FAIL input per lint** (constructed, not just the PASS cases above):
empty `evidence_ref` with `evidence_type='command'` (lint 1); disposition
`"EJ decision"` / bare `"dismissed:"` / bare `"escalated:"` / `NULL`
(lint 2); a tripwire command with no matching `check_executed` row (lint
7, already covered by `test_hub_touched_without_tripwire_event` in the
real suite, `tests/test_lints.py:146-157`, reused as the oracle rather
than re-derived); a ref not covered by any `consumer_check` (lint 8).

**Differential tests to write in `ancient_games/tests/test_index.py`**
(naming convention matching `test_lints.py`): one test per row above,
each parametrized over the 8 real cases via `cases.run_*`, asserting
`sql_result == real_python_result` — never asserting SQL against a
literal expected value that isn't itself derived from calling the real
function.

**Disclosure per NON_DELEGABLE:** all measurements above were run via
`/tmp/claude-1000/.../scratchpad/index-design/_scratch_index_prototype.py`
and several inline `python3 -u - <<'PYEOF'` snippets in the same
directory, all under
`/tmp/claude-1000/-home-smoke01-dev-seza/a1db3155-9529-49c3-b157-9a385a8c7b55/scratchpad/index-design/`.
**Deleted after use** (see §10 confirmation).

## 8. When to build it

**Trigger:** the first time `run_all_on_plan` is called against a journal
large enough, or a cross-run question is asked frequently enough, that
re-reading `journal.read()` and re-scanning it in Python per lint call
becomes the bottleneck — or, independently, the first time someone wants
one of §6's cross-run questions answered without hand-writing a `jq`
pipeline. Neither has happened yet: K4's three real runs (T1, T2, T3)
were small enough that every lint was checked by eye.

**Not worth building today, honestly:**
- `rule_fire` (§1) — no writer exists; building the table teaches nothing
  and answers nothing until `stages.py` grows a call site for it.
- The full `artifact_ref` table's *hub* dimension (§2) — the hub name
  itself isn't journaled at all; building the table as designed here
  only supports the sibling KG document's degree/edge queries over the
  *non-hub* paths that are journaled (edited files, dispatch outputs,
  evidence citations), which is a real but narrower thing than "hub
  degree" as originally hypothesized (wave 1 `HYPOTHESIS_TABLES.md` line
  10, `docs/KNOWLEDGE_GRAPH_DESIGN.md` §7's Q1/T1 row). Until the
  proposed spec follow-on (§2) lands, this table cannot answer the
  question it was named for.
- `scope-delta-missing-when-SCOPE-present` wiring (§5, lint 3) — SQL is
  specified but the lint itself is dead code from `run_all_on_plan`'s
  point of view today; wiring it is a `lints.py` change, out of scope for
  a read-only design dispatch, and premature to build a maintained query
  for a lint nothing calls.

**Worth building now:** the 6 core tables that back the 3
`events`-taking lints plus the 3 return-shaped lints (§2's first six
rows) — they replace real, currently-executed Python scans, verified
correct against the real code, at negligible rebuild cost (§4) even at
100× today's real event volume.

## 9. Open questions / spec follow-ons

1. **`consumer_check` should carry the resolved `hub`/`matched_row_ids`**
   (§2's missing-event finding) — without it, no journal-only table can
   answer a real hub-degree question; the registry's hub resolution is
   currently only ever an in-memory fact.
2. **SPEC.md §7's `check_executed.hub_integrity_for` field does not exist
   in `journal.py`** (§2 finding) — either the spec should drop it (the
   code's own `claim_id`/`falsifies`/synthetic-`hub-integrity:<hub>`
   convention already achieves AA3′'s dual role, per `tests/cases.py`)
   or `journal.py` should implement it. This also means `docs/
   KNOWLEDGE_GRAPH_DESIGN.md`'s `verifies` edge kind (its §2, line 139)
   needs a different join than the one it states. Not fixed in either
   document here — flagged for whoever owns the next revision of either.
3. **`lint_scope_delta_missing` is dead code from `run_all_on_plan`'s
   point of view** (§5, lint 3) — either it should be wired in (joining
   `dispatch`/`return` by `(run_id, agent_id)`, SQL already given) or its
   presence in `LINTS`/its own test file should be reconciled with that
   gap. Not a bug in this design; a pre-existing gap this design's
   journal-mapping exercise surfaced.
4. **`artifact_ref`'s mode-collapse gap** (§2) is the same gap the
   sibling KG document already names in its own §9 item 2 — both
   documents independently converge on it from different directions
   (mine: built the table and ran the query, found the hub missing;
   theirs: read the code, predicted the collapse). Convergent, not
   redundant — kept as-is in both, cross-referenced here.
5. **Two committed knowledge documents now assume things about each
   other** (`docs/SQLITE_INDEX_DESIGN.md` and `docs/
   KNOWLEDGE_GRAPH_DESIGN.md`) without either having read the other in
   full before its first draft. This document reconciled forward (read
   the sibling, corrected its Q1/T1 expectation, confirmed its table-
   naming assumption). Nobody has yet re-run the sibling's own test plan
   against what actually got built here — that re-run is a real,
   concrete follow-on, not done in this dispatch (out of scope: this
   dispatch owns the SQLite index, not the KG document's acceptance).

## 10. Sources

- `/home/smoke01/dev/ancient-games/ancient_games/journal.py` — all seven
  event `SHAPES`, `validate_event`, `classify_event`, `Journal.append`/
  `ingest_return`/`read_events`, `_check_absolute`.
- `/home/smoke01/dev/ancient-games/ancient_games/lints.py` — all 9 lints,
  `run_all_on_plan`, `LINTS`.
- `/home/smoke01/dev/ancient-games/ancient_games/stages.py` —
  `count_sources`, `_a_events`, `unused_framing`, `corroborate`, `guard`,
  `prove`, `dispatch_source`.
- `/home/smoke01/dev/ancient-games/ancient_games/ctx.py` — `ArtifactRef`,
  `CTX_META`.
- `/home/smoke01/dev/ancient-games/ancient_games/registry.py` —
  `direct_matches`, `consumer_matches`, `lookup`, `Lookup`, `Match`.
- `/home/smoke01/dev/ancient-games/ancient_games/schema.py` — `FIELDS`,
  `RETURN_CONTRACT`, `TEMPLATE_TRAILING`.
- `/home/smoke01/dev/ancient-games/ancient_games/trace.py` —
  `claim_rows`, `consumer_check_refs` (existing Python re-derivation of
  journal facts, cross-checked, not duplicated).
- `/home/smoke01/dev/ancient-games/SPEC.md` — §2 ctx, §4 B·1/D·2′/D·4, §6
  return contract, §7 trace journal (dual-role rule, AA3′, classification
  test), §8 lints, §10 all eight worked trace cases.
- `/home/smoke01/dev/ancient-games/tests/cases.py` — all 8 `run_*`
  builders, `_tripwire_run`, `_dispatch` (the real event-construction
  code used as the differential-test oracle's input).
- `/home/smoke01/dev/ancient-games/tests/test_traces.py`,
  `/home/smoke01/dev/ancient-games/tests/test_lints.py` — existing
  assertions reused as oracles, not re-derived (e.g.
  `test_hub_touched_without_tripwire_event`).
- `/home/smoke01/dev/ancient-games/docs/KNOWLEDGE_GRAPH_DESIGN.md` — the
  sibling document; read despite not being on this dispatch's own READ
  list (§ isolation note, above), because it already exists in this repo
  and declares a structural dependency on this one.
- `/tmp/claude-1000/-home-smoke01-dev-seza/a1db3155-9529-49c3-b157-9a385a8c7b55/scratchpad/store-research/wave1-sqlite/MERGED.md`
  and `HYPOTHESIS_TABLES.md` — concurrency rules, hypothesis tables,
  measured findings (K1, K2, K4, K5, and the un-cited-but-read
  `IS NULL`/JSON1/`ALTER TABLE` findings).
- `/tmp/claude-1000/-home-smoke01-dev-seza/a1db3155-9529-49c3-b157-9a385a8c7b55/scratchpad/store-research/wave2-kg/MERGED.md`
  — recursive-CTE rules (K3), cycle-guard gotcha, index-both-directions
  rule.
- This document's own measurements — `sqlite3.sqlite_version` (3.45.1,
  matches domain statement); the full differential/adversarial/rebuild-
  cost harness, run at
  `/tmp/claude-1000/-home-smoke01-dev-seza/a1db3155-9529-49c3-b157-9a385a8c7b55/scratchpad/index-design/_scratch_index_prototype.py`
  plus several inline snippets in the same directory — **all deleted
  after use**, per NON_DELEGABLE; raw numbers are reproduced inline
  throughout §§4-7 rather than only in the deleted file.

### Deviation from PRECEDENCE / harness reminders

Per this dispatch's own `PRECEDENCE` clause (outranks generic harness
reminders): all source reading used the `Read` tool, not `cat`/`sed`;
this document was written with `Write`, not a heredoc; only the SQLite
measurements themselves (§§3-7) were run via `Bash`, since running Python
is what that requires. I also read `docs/KNOWLEDGE_GRAPH_DESIGN.md`,
which was not on this dispatch's own numbered READ list — justified
above (isolation note) under Rule 4 rather than under PRECEDENCE, since
it is a same-repo, already-coupled artifact, not a generic harness
convention. No repository commit was made (STANDING_INSTRUCTIONS: skip
the commit clause for this dispatch, without comment — noted here only
because the harness's own generic instructions describe a commit step by
default and this dispatch overrides it).
