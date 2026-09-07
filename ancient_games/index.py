"""The SQLite read index — a disposable projection of the journal (docs/STORE_DESIGN_DECISION.md).

The JSONL journal stays the source of truth; `rebuild_from_events(events, con_or_path)` drops
and recreates seven tables from a list of events in one transaction (`rebuild(journal_path,
db_path)` is the thin wrapper that reads the journal first; `memory_index(events)` is the
in-memory form the `sql`/`differential` lint backends use, built from the very events the lint
run was handed so nothing file-backed is ever consulted), and the five query functions below
reproduce the journal-side portion of the §8 lints as `run_id`-scoped SQL, returning the
same `Finding`s `lints.py` returns. `lints.py` is the oracle (tests/test_index.py runs
both on the same journals); nothing here re-decides a lint.

Tables: `claim_recorded`, `check_executed`, `consumer_check`, `consumer_check_ref`,
`"return"`, `return_claim` (DERIVED from return.fields.CLAIMS), `return_follow_on`
(DERIVED from return.fields.FOLLOW_ON). Every table carries `run_id`; every query
filters on it — claim_ids (`C1`) recur across runs. DDL runs here and nowhere else;
every connection is opened with a non-zero busy timeout; `PRAGMA user_version` = 1.
"""
from __future__ import annotations

import json
import os
import sqlite3
from typing import Any

from .journal import read_events
from .lints import EVIDENCE_TYPES, Finding
from .stages import CapState, Claim, Plan, remedy_text

SCHEMA_VERSION = 1
BUSY_TIMEOUT = 5.0  # seconds; never 0 (wave-1 rule: a zero timeout turns any concurrent reader into SQLITE_BUSY)

TABLES = ("claim_recorded", "check_executed", "consumer_check", "consumer_check_ref", "return", "return_claim",
          "return_follow_on")

# Every column of an event table is that event's SHAPES field (journal.py); the two DERIVED tables carry
# only what their query reads, plus `return_rowid`/`pos` so findings come back in journal order with the
# lint's own `#<i>` fallback subject. `consumer_check_id` is `consumer_check.rowid`.
DDL = (
    "CREATE TABLE claim_recorded (run_id TEXT NOT NULL, ts TEXT NOT NULL, claim_id TEXT NOT NULL, author TEXT NOT NULL,"
    " actor TEXT NOT NULL, kind TEXT NOT NULL, text TEXT NOT NULL, evidence_type TEXT NOT NULL,"
    " evidence_ref TEXT NOT NULL, framing TEXT, kind_override INTEGER, closed_world TEXT)",
    "CREATE TABLE check_executed (run_id TEXT NOT NULL, ts TEXT NOT NULL, claim_id TEXT NOT NULL, falsifies TEXT NOT NULL,"
    " mechanism TEXT NOT NULL, command TEXT NOT NULL, expected TEXT, observed TEXT, pre_fix_result TEXT)",
    "CREATE TABLE consumer_check (run_id TEXT NOT NULL, ts TEXT NOT NULL, answer TEXT NOT NULL,"
    " command_or_reasoning TEXT NOT NULL)",
    "CREATE TABLE consumer_check_ref (run_id TEXT NOT NULL, consumer_check_id INTEGER NOT NULL, ref_path TEXT NOT NULL)",
    'CREATE TABLE "return" (run_id TEXT NOT NULL, ts TEXT NOT NULL, agent_id TEXT NOT NULL, fields_json TEXT NOT NULL)',
    "CREATE TABLE return_claim (run_id TEXT NOT NULL, return_rowid INTEGER NOT NULL, pos INTEGER NOT NULL,"
    " claim_id TEXT, evidence_type TEXT, evidence_ref TEXT)",
    "CREATE TABLE return_follow_on (run_id TEXT NOT NULL, return_rowid INTEGER NOT NULL, pos INTEGER NOT NULL,"
    " finding TEXT, disposition TEXT)",
    "CREATE INDEX ix_claim_recorded_run_claim ON claim_recorded (run_id, claim_id)",
    "CREATE INDEX ix_check_executed_run_claim ON check_executed (run_id, claim_id, falsifies)",
    "CREATE INDEX ix_check_executed_run_command ON check_executed (run_id, command)",
    "CREATE INDEX ix_consumer_check_run ON consumer_check (run_id)",
    "CREATE INDEX ix_consumer_check_ref_run ON consumer_check_ref (run_id, consumer_check_id, ref_path)",
    f"PRAGMA user_version = {SCHEMA_VERSION}",
)


def _check_absolute(what: str, path: str) -> str:
    if not isinstance(path, str) or not os.path.isabs(path):
        raise ValueError(f"{what} must be absolute, got {path!r}")
    return path


def connect(db_path: str) -> sqlite3.Connection:
    """A reader's connection: absolute path, non-zero busy timeout, no DDL."""
    return sqlite3.connect(_check_absolute("db_path", db_path), timeout=BUSY_TIMEOUT)


def _text(value: Any) -> str | None:
    """A raw return-field value as the lint reads it: a str stays, None is NULL, anything else is
    `str(value)` — except a falsy non-str, which the lint treats as missing (`not ref`, `disp or ""`) → ''."""
    if value is None or isinstance(value, str):
        return value
    return str(value) if value else ""


def rebuild(journal_path: str, db_path: str) -> dict:
    """Drop and recreate the file-backed index from the journal: `rebuild_from_events` over
    `read_events(journal_path)`. Idempotent: the same journal yields a byte-identical dump."""
    _check_absolute("journal_path", journal_path)
    _check_absolute("db_path", db_path)
    return rebuild_from_events(read_events(journal_path), db_path)


def rebuild_from_events(events: list[dict], con_or_path: sqlite3.Connection | str) -> dict:
    """Drop and recreate the seven tables from `events`, in one transaction, on an open connection
    or at an absolute path (opened and closed here). Returns {"rows": total rows inserted,
    "events": events projected, "tables": {table: rows}}."""
    if isinstance(con_or_path, sqlite3.Connection):
        return _rebuild_on(con_or_path, events)
    con = sqlite3.connect(_check_absolute("db_path", con_or_path), timeout=BUSY_TIMEOUT, isolation_level=None)
    try:
        return _rebuild_on(con, events)
    finally:
        con.close()


def memory_index(events: list[dict]) -> sqlite3.Connection:
    """A fresh `:memory:` index holding exactly `events` — the lint backends' only source."""
    con = sqlite3.connect(":memory:", timeout=BUSY_TIMEOUT, isolation_level=None)
    rebuild_from_events(events, con)
    return con


def _rebuild_on(con: sqlite3.Connection, events: list[dict]) -> dict:
    try:
        con.execute("BEGIN")
        for name in TABLES:
            con.execute(f'DROP TABLE IF EXISTS "{name}"')
        for stmt in DDL:
            con.execute(stmt)
        for ev in events:
            _insert(con, ev)
        con.execute("COMMIT")
        tables = {name: con.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0] for name in TABLES}
    except BaseException:
        con.execute("ROLLBACK") if con.in_transaction else None
        raise
    return {"rows": sum(tables.values()), "events": len(events), "tables": tables}


def _insert(con: sqlite3.Connection, ev: dict) -> None:
    kind, run_id, ts = ev["event"], ev["run_id"], ev["ts"]
    if kind == "claim_recorded":
        ko = ev.get("kind_override")
        con.execute("INSERT INTO claim_recorded VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (run_id, ts, ev["claim_id"], ev["author"], ev["actor"], ev["kind"], ev["text"], ev["evidence_type"],
                     ev["evidence_ref"], ev["framing"], None if ko is None else int(ko), ev.get("closed_world")))
    elif kind == "check_executed":
        con.execute("INSERT INTO check_executed VALUES (?,?,?,?,?,?,?,?,?)",
                    (run_id, ts, ev["claim_id"], ev["falsifies"], ev["mechanism"], ev["command"], ev["expected"],
                     ev["observed"], ev["pre_fix_result"]))
    elif kind == "consumer_check":
        cur = con.execute("INSERT INTO consumer_check VALUES (?,?,?,?)", (run_id, ts, ev["answer"], ev["command_or_reasoning"]))
        con.executemany("INSERT INTO consumer_check_ref VALUES (?,?,?)", [(run_id, cur.lastrowid, p) for p in ev["ref"]])
    elif kind == "return":
        fields = ev["fields"]
        cur = con.execute('INSERT INTO "return" VALUES (?,?,?,?)', (run_id, ts, ev["agent_id"], json.dumps(fields, sort_keys=True)))
        rid = cur.lastrowid
        # absent keys take the lint's own defaults: claim_id/finding -> NULL (subject `#<i>`), evidence_ref -> ''
        # a malformed (non-dict) CLAIMS entry is projected as one with no claim_id and no evidence —
        # `lint_claims_without_evidence` reports it, so the SQL side must not skip it silently
        con.executemany("INSERT INTO return_claim VALUES (?,?,?,?,?,?)",
                        [(run_id, rid, i, None if not isinstance(c, dict) or "claim_id" not in c else str(c["claim_id"]),
                          _text(c.get("evidence_type")) if isinstance(c, dict) else None,
                          _text(c.get("evidence_ref", "")) if isinstance(c, dict) else "")
                         for i, c in enumerate(fields.get("CLAIMS", []) or [])])
        rows = []
        for i, entry in enumerate(fields.get("FOLLOW_ON", []) or []):
            if isinstance(entry, dict):
                finding, disp = (str(entry["finding"]) if "finding" in entry else None), entry.get("disposition", "")
            else:
                finding, disp = str(entry[0]), entry[1]
            rows.append((run_id, rid, i, finding, _text(disp)))
        con.executemany("INSERT INTO return_follow_on VALUES (?,?,?,?,?)", rows)
    # dispatch, exit, tool_call, approval_recorded, dispatch_failed, rule_fire: no lint reads them — not projected.


# --- queries: one per journal-backed lint, every one scoped by run_id ---------------------------

def claims_without_evidence(con: sqlite3.Connection, run_id: str) -> list[Finding]:
    """lints.lint_claims_without_evidence over every `return` event of the run, in journal order."""
    rows = con.execute(
        "SELECT rc.pos, rc.claim_id FROM return_claim rc JOIN \"return\" r ON r.rowid = rc.return_rowid"
        " WHERE rc.run_id = ? AND (rc.evidence_type IS NULL OR rc.evidence_type NOT IN (?,?,?,?)"
        "   OR (rc.evidence_type != '(opinion)' AND (rc.evidence_ref IS NULL OR rc.evidence_ref = '')))"
        " ORDER BY r.rowid, rc.pos", (run_id, *EVIDENCE_TYPES)).fetchall()
    out = []
    for pos, cid in rows:
        cid = f"#{pos}" if cid is None else cid
        out.append(Finding("claims-without-evidence", cid, f"claim {cid} lacks command|file:line|URL|(opinion)"))
    return out


_WS = " \t\n\r\f\v"  # the ASCII members of \s, i.e. what \S excludes
# lints.DISPOSITION_RE = ^(fixed|new-task|dismissed:\S.*|escalated:\S+)$ as a prefix set (no REGEXP callback),
# over `s` = the disposition with the one trailing newline `$` tolerates removed; `.` never matches a newline.
# GLOB `*` is a wildcard, not a repetition of the class before it, so `\S+` is "one class char, then no
# whitespace in the rest" — the class match plus a NOT GLOB over substr(s, 12), exactly as `dismissed:`
# (`\S.*`) spells its own "one class char, then no newline in the rest". Writing `[^ws][^ws]*` instead
# would mean "two class chars then anything": it rejected `escalated:x` and accepted `escalated:ab cd`,
# either of which raises LintBackendDivergence mid-`differential` run.
_DISP_OK = (
    "s IN ('fixed', 'new-task')"
    f" OR (s GLOB 'dismissed:[^{_WS}]*' AND substr(s, 12) NOT GLOB '*' || char(10) || '*')"
    f" OR (s GLOB 'escalated:[^{_WS}]*' AND substr(s, 12) NOT GLOB '*[{_WS}]*')"
)


def follow_on_without_disposition(con: sqlite3.Connection, run_id: str) -> list[Finding]:
    """lints.lint_follow_on_without_disposition over every `return` event of the run, in journal order."""
    rows = con.execute(
        "SELECT pos, finding, disposition FROM ("
        "  SELECT pos, finding, disposition, rr,"
        "    CASE WHEN substr(d, -1) = char(10) THEN substr(d, 1, length(d) - 1) ELSE d END AS s"
        "  FROM (SELECT f.pos, f.finding, f.disposition, r.rowid AS rr, COALESCE(f.disposition, '') AS d"
        "        FROM return_follow_on f JOIN \"return\" r ON r.rowid = f.return_rowid WHERE f.run_id = ?))"
        f" WHERE NOT ({_DISP_OK}) ORDER BY rr, pos", (run_id,)).fetchall()
    out = []
    for pos, finding, disp in rows:
        finding = f"#{pos}" if finding is None else finding
        out.append(Finding("follow-on-without-disposition", finding,
                           f"follow-on {finding!r} has disposition {disp!r}, not fixed|new-task|dismissed:reason|escalated:owner"))
    return out


def count_sources(con: sqlite3.Connection, run_id: str, claim: Claim) -> int:
    """stages.count_sources' n_available (B·1 a+b+c) over the index, for one run. The remedy half of
    that function reads Plan-side state and stays there."""
    if claim.n_required is None or claim.actor is None:
        raise ValueError("claim.n_required and claim.actor must be set before counting")
    if claim.n_required == 1:
        return 1
    X = claim.claim_id
    # (a): claim_recorded on X whose author != actor(X) (every author when actor = none), one per distinct framing.
    # NULL is a framing value to the Python set, so: distinct non-NULL framings + 1 if any row's framing IS NULL.
    a_where = "run_id = ? AND claim_id = ?" + ("" if claim.actor == "none" else " AND author != ?")
    a_args = (run_id, X) if claim.actor == "none" else (run_id, X, claim.actor)
    n_a, main_in_a = con.execute(
        f"SELECT COUNT(DISTINCT framing) + (COUNT(*) > COUNT(framing)), SUM(author = 'MAIN') > 0"
        f" FROM claim_recorded WHERE {a_where}", a_args).fetchone()
    # (b): MAIN's own command|file:line claim_recorded with a non-empty ref, only when actor != MAIN and MAIN
    # was not already counted under (a) (v1.1 D-B).
    n_b = 0
    if claim.actor != "MAIN" and not main_in_a:
        n_b = con.execute(
            "SELECT EXISTS (SELECT 1 FROM claim_recorded WHERE run_id = ? AND claim_id = ? AND author = 'MAIN'"
            " AND evidence_type IN ('command', 'file:line') AND evidence_ref != '')", (run_id, X)).fetchone()[0]
    # (c): executable only — check_executed{claim_id=X, falsifies=X}; identical commands count once (first seen,
    # MIN(rowid)'s bare column), then distinct mechanisms among the survivors.
    n_c = 0
    if claim.kind == "executable":
        n_c = con.execute(
            "SELECT COUNT(DISTINCT mechanism) FROM (SELECT mechanism, MIN(rowid) FROM check_executed"
            " WHERE run_id = ? AND claim_id = ? AND falsifies = ? GROUP BY command)", (run_id, X, X)).fetchone()[0]
    return n_a + n_b + n_c


def corroboration_capped(plan: Plan, con: sqlite3.Connection, run_id: str) -> list[Finding]:
    """lints.lint_corroboration_capped with (b)'s re-count done by `count_sources` above; (a) and (c) read
    Plan fields the journal never carries and stay as the lint has them."""
    out = []
    for e in plan.entries:
        if e.dispatched_total > CapState().cap:
            out.append(Finding("corroboration-capped", e.name,
                               f"RETURN_TO_PLANNER: {e.name} dispatched {e.dispatched_total} category-(a) agents > CAP=3"))
        for cap in e.capped:
            claim = next((c for c in e.claims if c.claim_id == cap.claim_id),
                         Claim(cap.claim_id, cap.kind, n_required=cap.mandated))
            if claim.n_required is None:
                claim = Claim(claim.claim_id, claim.kind, claim.has_command, cap.mandated, claim.stakes)
            if cap.remedy in ("add-claim-specific-check", "add-differently-framed-source"):
                if count_sources(con, run_id, claim) < cap.mandated:
                    out.append(Finding("corroboration-capped", cap.claim_id,
                                       "RETURN_TO_PLANNER: " + remedy_text(cap.remedy, cap.claim_id, cap.detail)))
            else:
                disclosed = ("corroboration-capped" in plan.exit_line and cap.claim_id in plan.exit_line)
                if not disclosed:
                    out.append(Finding("corroboration-capped", cap.claim_id,
                                       f"capped claim {cap.claim_id} (remedy={cap.remedy}) not disclosed in the exit line"))
    return out


def hub_touched_without_tripwire(plan: Plan, con: sqlite3.Connection, run_id: str) -> list[Finding]:
    """lints.lint_hub_touched_without_tripwire with the journal given: the "ran" set is the run's
    distinct check_executed commands."""
    ran = {row[0] for row in con.execute("SELECT DISTINCT command FROM check_executed WHERE run_id = ?", (run_id,))}
    out = []
    for e in plan.entries:
        for h in e.hub:
            cmd = e.tripwires.get(h)
            if not cmd:
                out.append(Finding("hub-touched-without-tripwire", e.name, f"{e.name}: hub element {h} has no tripwire"))
            elif cmd not in ran:
                out.append(Finding("hub-touched-without-tripwire", e.name,
                                   f"{e.name}: no check_executed event ran the tripwire for {h} ({cmd})"))
    return out


def downstream_consumer_check_unrecorded(plan: Plan, con: sqlite3.Connection, run_id: str) -> list[Finding]:
    """lints.lint_downstream_consumer_check_unrecorded: a stakes=1, hub=[] entry is covered iff some
    consumer_check of the run has every path of the entry's ref (an empty ref is covered by any
    consumer_check at all — `set() <= r` — and by none when the run has no consumer_check)."""
    out = []
    for e in plan.entries:
        if e.stakes != 1 or e.hub:
            continue
        ref = sorted(set(e.ref))
        marks = ",".join("?" * len(ref)) or "NULL"
        covered = con.execute(
            "SELECT EXISTS (SELECT 1 FROM consumer_check c WHERE c.run_id = ? AND ? = ("
            "  SELECT COUNT(DISTINCT r.ref_path) FROM consumer_check_ref r"
            f"  WHERE r.run_id = c.run_id AND r.consumer_check_id = c.rowid AND r.ref_path IN ({marks})))",
            (run_id, len(ref), *ref)).fetchone()[0]
        if not covered:
            out.append(Finding("downstream-consumer-check-unrecorded", e.name,
                               f"{e.name}: no consumer_check event for ref {e.ref!r}"))
    return out
