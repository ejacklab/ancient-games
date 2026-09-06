"""§8 — the nine lints. Each is pure: `lint_x(input) -> list[Finding]`.

Inputs are ctx / return dicts / journal events / schema rows / a plan.
"""
from __future__ import annotations

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


# 6 ------------------------------------------------------------------------
def lint_corroboration_capped(plan: Plan, events: list[dict]) -> list[Finding]:
    """(a) any group's category-(a) dispatched agents > 3, structurally;
    (b) a capped claim with a re-plannable remedy has no recorded fix — recompute
        n_available against the journal first;
    (c) a gate-routed capped claim is not disclosed in the plan's exit line."""
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
def lint_hub_touched_without_tripwire(plan: Plan, events: list[dict] | None = None) -> list[Finding]:
    """any entry whose hub ≠ [] has no tripwire recorded for each hub element:
    D·4 must have named a tripwire command for it, and (when the journal is
    given) a `check_executed` event running that command must exist — AA3′:
    that event may double as a (c) source for an executable claim it falsifies."""
    ran = {ev["command"] for ev in (events or []) if ev.get("event") == "check_executed"}
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
def lint_downstream_consumer_check_unrecorded(plan: Plan, events: list[dict]) -> list[Finding]:
    """a stakes=1 ∧ hub=[] entry with no consumer_check event for its ref."""
    refs = [set(ev["ref"]) for ev in events if ev.get("event") == "consumer_check"]
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


def run_all_on_plan(plan: Plan, events: list[dict]) -> list[Finding]:
    """A's exit: every lint in §8 over the whole plan. The two table lints run
    against this package's own §5/§6 rows; the return-shaped lints run over
    every ingested `return` event in the journal."""
    from .schema import FIELDS, RETURN_CONTRACT

    out: list[Finding] = []
    for ev in events:
        if ev.get("event") == "return":
            fields = ev.get("fields", {})
            out += lint_claims_without_evidence(fields.get("CLAIMS", []) or [])
            out += lint_follow_on_without_disposition(fields.get("FOLLOW_ON", []) or [])
            if fields.get("TEMPLATE"):
                out += lint_evidence_after_verdict(fields["TEMPLATE"])
    out += lint_schema_field_without_escape_value(FIELDS)
    out += lint_return_field_without_escape_value(RETURN_CONTRACT)
    out += lint_corroboration_capped(plan, events)
    out += lint_hub_touched_without_tripwire(plan, events)
    out += lint_downstream_consumer_check_unrecorded(plan, events)
    return out
