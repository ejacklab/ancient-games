"""§8 — the nine lints. Each is pure: `lint_x(input) -> list[Finding]`.

Inputs are ctx / return dicts / journal events / schema rows / a plan.

`run_all_on_plan` has three backends (`BACKENDS`), chosen by its `backend` kwarg or, when that
is None, by `$AG_LINT_BACKEND` (default `python`):
  python        — the lints below, the permanent oracle;
  sql           — the five journal-backed lints answered by `index.py`'s queries over a `:memory:`
                  index built from the very `events` passed in (never a file); the other lints
                  stay Python in every mode;
  differential  — both, compared lint by lint; any disagreement raises `LintBackendDivergence`
                  (never a silent preference) and agreement returns the Python result.
SQL is never the oracle: when the two disagree the SQL is wrong until shown otherwise.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Iterable

from .schema import TEMPLATE_TRAILING
from .stages import CapState, Claim, Plan, count_sources, remedy_text

EVIDENCE_TYPES = ("command", "file:line", "URL", "(opinion)")
DISPOSITION_RE = re.compile(r"^(fixed|new-task|dismissed:\S.*|escalated:\S+)$")  # V3.5 §4 E·3 four-value enum


@dataclass(frozen=True)
class Finding:
    lint: str
    subject: str
    message: str


# 1 ------------------------------------------------------------------------
def lint_claims_without_evidence(claims: Iterable[dict[str, Any]]) -> list[Finding]:
    """any CLAIMS entry lacking command | file:line | URL | (opinion)."""
    out = []
    for i, c in enumerate(claims):
        et = c.get("evidence_type")
        ref = c.get("evidence_ref", "")
        cid = str(c.get("claim_id", f"#{i}"))
        if et not in EVIDENCE_TYPES or (et != "(opinion)" and not ref):
            out.append(Finding("claims-without-evidence", cid, f"claim {cid} lacks command|file:line|URL|(opinion)"))
    return out


# 2 ------------------------------------------------------------------------
def lint_follow_on_without_disposition(follow_on: Iterable[Any]) -> list[Finding]:
    """any FOLLOW_ON entry not tagged fixed | new-task | dismissed:reason | escalated:owner."""
    out = []
    for i, entry in enumerate(follow_on):
        if isinstance(entry, dict):
            finding, disp = entry.get("finding", f"#{i}"), entry.get("disposition", "")
        else:
            finding, disp = entry[0], entry[1]
        if not DISPOSITION_RE.match(str(disp or "")):
            out.append(Finding("follow-on-without-disposition", str(finding),
                               f"follow-on {finding!r} has disposition {disp!r}, not fixed|new-task|dismissed:reason|escalated:owner"))
    return out


# 3 ------------------------------------------------------------------------
def lint_scope_delta_missing(return_fields: dict[str, Any], dispatch: dict[str, Any]) -> list[Finding]:
    """SCOPE was sent but SCOPE_DELTA is absent (not even an explicit-empty)."""
    if "SCOPE" in dispatch and "SCOPE_DELTA" not in return_fields:
        return [Finding("scope-delta-missing-when-SCOPE-present", "SCOPE_DELTA", "SCOPE sent but SCOPE_DELTA absent")]
    return []


# 4 / 9 --------------------------------------------------------------------
def _escape_rows(lint: str, rows: Iterable[Any]) -> list[Finding]:
    out = []
    for r in rows:
        row = r.as_row() if hasattr(r, "as_row") else r
        val = str(row.get("escape_value", "") or "").strip()
        if not val or val == "—":
            out.append(Finding(lint, row.get("field", "?"), f"{row.get('field', '?')} has an empty escape_value cell"))
    return out


def lint_schema_field_without_escape_value(rows: Iterable[Any]) -> list[Finding]:
    """§5 CORE/CONDITIONAL: a required field's row has an empty escape_value cell."""
    return _escape_rows("schema-field-without-escape-value", rows)


def lint_return_field_without_escape_value(rows: Iterable[Any]) -> list[Finding]:
    """§6 return contract: a required return field's row has an empty escape_value cell."""
    return _escape_rows("return-field-without-escape-value", rows)


# 5 ------------------------------------------------------------------------
def lint_evidence_after_verdict(template_text: str) -> list[Finding]:
    """## Verdict before ## Findings, or any heading other than
    ## Not established / ## Follow-on after ## Verdict."""
    headings = [ln.strip() for ln in template_text.splitlines() if ln.startswith("## ")]
    out = []
    if "## Verdict" in headings and "## Findings" in headings:
        if headings.index("## Verdict") < headings.index("## Findings"):
            out.append(Finding("evidence-after-verdict", "## Findings", "## Verdict appears before ## Findings"))
    if "## Verdict" in headings:
        for h in headings[headings.index("## Verdict") + 1:]:
            if h not in TEMPLATE_TRAILING:
                out.append(Finding("evidence-after-verdict", h, f"{h} appears after ## Verdict"))
    return out


def in_run(events: list[dict], run_id: str | None) -> list[dict]:
    """`events` scoped to one run when `run_id` is given; the whole list when it is None.
    claim_ids (`C1`) and commands recur across runs, so a merged journal read unscoped
    counts another run's sources and checks as this run's."""
    if run_id is None:
        return events
    return [ev for ev in events if ev.get("run_id") == run_id]


# 6 ------------------------------------------------------------------------
def lint_corroboration_capped(plan: Plan, events: list[dict], run_id: str | None = None) -> list[Finding]:
    """(a) any group's category-(a) dispatched agents > 3, structurally;
    (b) a capped claim with a re-plannable remedy has no recorded fix — recompute
        n_available against the journal first;
    (c) a gate-routed capped claim is not disclosed in the plan's exit line.
    `run_id` scopes the journal read in (b) to that run (`in_run`)."""
    events = in_run(events, run_id)
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
                n, _ = count_sources(claim, events, CapState(e.dispatched_total), [])
                if n < cap.mandated:
                    out.append(Finding("corroboration-capped", cap.claim_id,
                                       "RETURN_TO_PLANNER: " + remedy_text(cap.remedy, cap.claim_id, cap.detail)))
            else:
                disclosed = ("corroboration-capped" in plan.exit_line and cap.claim_id in plan.exit_line)
                if not disclosed:
                    out.append(Finding("corroboration-capped", cap.claim_id,
                                       f"capped claim {cap.claim_id} (remedy={cap.remedy}) not disclosed in the exit line"))
    return out


# 7 ------------------------------------------------------------------------
def lint_hub_touched_without_tripwire(plan: Plan, events: list[dict] | None = None,
                                      run_id: str | None = None) -> list[Finding]:
    """any entry whose hub ≠ [] has no tripwire recorded for each hub element:
    D·4 must have named a tripwire command for it, and (when the journal is
    given) a `check_executed` event running that command must exist — AA3′:
    that event may double as a (c) source for an executable claim it falsifies.
    `run_id` scopes the `check_executed` events considered to that run (`in_run`)."""
    ran = {ev["command"] for ev in in_run(events or [], run_id) if ev.get("event") == "check_executed"}
    out = []
    for e in plan.entries:
        for h in e.hub:
            cmd = e.tripwires.get(h)
            if not cmd:
                out.append(Finding("hub-touched-without-tripwire", e.name, f"{e.name}: hub element {h} has no tripwire"))
            elif events is not None and cmd not in ran:
                out.append(Finding("hub-touched-without-tripwire", e.name,
                                   f"{e.name}: no check_executed event ran the tripwire for {h} ({cmd})"))
    return out


# 8 ------------------------------------------------------------------------
def lint_downstream_consumer_check_unrecorded(plan: Plan, events: list[dict], run_id: str | None = None) -> list[Finding]:
    """a stakes=1 ∧ hub=[] entry with no consumer_check event for its ref.
    `run_id` scopes the `consumer_check` events considered to that run (`in_run`)."""
    refs = [set(ev["ref"]) for ev in in_run(events, run_id) if ev.get("event") == "consumer_check"]
    out = []
    for e in plan.entries:
        if e.stakes == 1 and not e.hub and not any(set(e.ref) <= r for r in refs):
            out.append(Finding("downstream-consumer-check-unrecorded", e.name,
                               f"{e.name}: no consumer_check event for ref {e.ref!r}"))
    return out


# ---------------------------------------------------------------------------
LINTS = (
    "claims-without-evidence", "follow-on-without-disposition", "scope-delta-missing-when-SCOPE-present",
    "schema-field-without-escape-value", "evidence-after-verdict", "corroboration-capped",
    "hub-touched-without-tripwire", "downstream-consumer-check-unrecorded", "return-field-without-escape-value",
)


BACKENDS = ("python", "sql", "differential")
ENV_BACKEND = "AG_LINT_BACKEND"
SQL_LINTS = ("claims-without-evidence", "follow-on-without-disposition", "corroboration-capped",
             "hub-touched-without-tripwire", "downstream-consumer-check-unrecorded")


class LintBackendDivergence(AssertionError):
    """The python and sql backends disagreed on one lint. Carries both lists; the Python one is the oracle."""

    def __init__(self, lint: str, python: list[Finding], sql: list[Finding], run_id: str):
        self.lint, self.python, self.sql, self.run_id = lint, list(python), list(sql), run_id
        super().__init__(f"lint backend divergence on {lint!r} (run_id={run_id!r}):"
                         f"\n  python (oracle): {self.python!r}\n  sql:             {self.sql!r}")


def default_backend() -> str:
    """`$AG_LINT_BACKEND`, or `python` when unset/empty; any other value is a ValueError."""
    return check_backend(os.environ.get(ENV_BACKEND) or "python")


def check_backend(backend: str) -> str:
    if backend not in BACKENDS:
        raise ValueError(f"lint backend must be one of {BACKENDS}, got {backend!r}")
    return backend


def _run_id_of(events: list[dict], run_id: str | None) -> str:
    """The run the SQL queries scope to: the caller's, else the one run in `events` (or '' when empty)."""
    if run_id is not None:
        return run_id
    ids = {e.get("run_id") for e in events}
    if len(ids) > 1:
        raise ValueError(f"sql lint backend needs run_id= for a multi-run event list, got run_ids {sorted(map(str, ids))}")
    return ids.pop() if ids else ""


def _python_journal_lints(plan: Plan, events: list[dict], run_id: str | None) -> dict[str, list[Finding]]:
    out: dict[str, list[Finding]] = {name: [] for name in SQL_LINTS}
    for ev in in_run(events, run_id):
        if ev.get("event") == "return":
            fields = ev.get("fields", {})
            out["claims-without-evidence"] += lint_claims_without_evidence(fields.get("CLAIMS", []) or [])
            out["follow-on-without-disposition"] += lint_follow_on_without_disposition(fields.get("FOLLOW_ON", []) or [])
    out["corroboration-capped"] = lint_corroboration_capped(plan, events, run_id)
    out["hub-touched-without-tripwire"] = lint_hub_touched_without_tripwire(plan, events, run_id)
    out["downstream-consumer-check-unrecorded"] = lint_downstream_consumer_check_unrecorded(plan, events, run_id)
    return out


def _sql_journal_lints(plan: Plan, events: list[dict], run_id: str) -> dict[str, list[Finding]]:
    from . import index  # lazy: index imports Finding from here

    con = index.memory_index(events)
    try:
        return {"claims-without-evidence": index.claims_without_evidence(con, run_id),
                "follow-on-without-disposition": index.follow_on_without_disposition(con, run_id),
                "corroboration-capped": index.corroboration_capped(plan, con, run_id),
                "hub-touched-without-tripwire": index.hub_touched_without_tripwire(plan, con, run_id),
                "downstream-consumer-check-unrecorded": index.downstream_consumer_check_unrecorded(plan, con, run_id)}
    finally:
        con.close()


def run_all_on_plan(plan: Plan, events: list[dict], *, backend: str | None = None,
                    run_id: str | None = None) -> list[Finding]:
    """A's exit: every lint in §8 over the whole plan. The two table lints run
    against this package's own §5/§6 rows; the return-shaped lints run over
    every ingested `return` event in the journal.

    `backend` (see the module docstring): `python` keeps the findings in journal order, the
    per-return lints interleaved event by event; `sql` reports the two per-return lints
    run-wide (claims, then follow-ons) before the template lint; `differential` raises on any
    per-lint disagreement and otherwise returns exactly the `python` list. `run_id` is the run every
    journal-reading lint scopes to (`in_run` for the Python lints, the `WHERE run_id` of the SQL
    queries); when it is None the Python lints read every event they are given and the SQL side
    takes the one run in `events` (a multi-run list then needs it)."""
    from .schema import FIELDS, RETURN_CONTRACT

    backend = check_backend(backend) if backend is not None else default_backend()
    if backend != "python":
        run_id = _run_id_of(events, run_id)
    out: list[Finding] = []
    if backend == "python" or backend == "differential":
        for ev in in_run(events, run_id):
            if ev.get("event") == "return":
                fields = ev.get("fields", {})
                out += lint_claims_without_evidence(fields.get("CLAIMS", []) or [])
                out += lint_follow_on_without_disposition(fields.get("FOLLOW_ON", []) or [])
                if fields.get("TEMPLATE"):
                    out += lint_evidence_after_verdict(fields["TEMPLATE"])
        out += lint_schema_field_without_escape_value(FIELDS)
        out += lint_return_field_without_escape_value(RETURN_CONTRACT)
        out += lint_corroboration_capped(plan, events, run_id)
        out += lint_hub_touched_without_tripwire(plan, events, run_id)
        out += lint_downstream_consumer_check_unrecorded(plan, events, run_id)
        if backend == "differential":
            python, sql = _python_journal_lints(plan, events, run_id), _sql_journal_lints(plan, events, run_id)
            for name in SQL_LINTS:
                if python[name] != sql[name]:
                    raise LintBackendDivergence(name, python[name], sql[name], run_id)
        return out
    sql = _sql_journal_lints(plan, events, run_id)
    out += sql["claims-without-evidence"]
    out += sql["follow-on-without-disposition"]
    for ev in in_run(events, run_id):
        if ev.get("event") == "return" and ev.get("fields", {}).get("TEMPLATE"):
            out += lint_evidence_after_verdict(ev["fields"]["TEMPLATE"])
    out += lint_schema_field_without_escape_value(FIELDS)
    out += lint_return_field_without_escape_value(RETURN_CONTRACT)
    out += sql["corroboration-capped"]
    out += sql["hub-touched-without-tripwire"]
    out += sql["downstream-consumer-check-unrecorded"]
    return out
