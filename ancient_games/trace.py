"""§10 — render a run's trace to markdown from journal events.

Stage exit lines come from `exit` events; the per-claim corroboration table
is rebuilt from the Corroborate exit line plus the journal's
`claim_recorded` / `check_executed` events; consumer checks and dispatches
are listed from their own events.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .journal import kind_overrides

_CLAIM_PART = re.compile(r"^(?P<claim>[^:]+): n=(?P<n>\d+)(?:/(?P<req>\d+))?(?P<rest>.*)$")


@dataclass
class ClaimRow:
    claim_id: str
    kind: str
    n_required: int
    n_available: int
    sources: list[str] = field(default_factory=list)
    remedy: str | None = None
    capped: bool = False


def parse_corroborate_line(line: str) -> list[ClaimRow]:
    body = line[len("Corroborate: "):].rstrip(".")
    rows = []
    for part in body.split("; "):
        if part.startswith("reconciled="):
            continue
        m = _CLAIM_PART.match(part.strip())
        if not m:
            continue
        rest = m.group("rest")
        remedy = None
        rm = re.search(r"remedy=([a-z-]+)", rest)
        if rm:
            remedy = rm.group(1)
        rows.append(ClaimRow(m.group("claim"), "?", int(m.group("req") or 1), int(m.group("n")),
                             remedy=remedy, capped="capped" in rest))
    return rows


def claim_rows(events: list[dict], run_id: str | None = None) -> list[ClaimRow]:
    if run_id is not None:
        events = [e for e in events if e.get("run_id") == run_id]
    rows: list[ClaimRow] = []
    for ev in events:
        if ev.get("event") == "exit" and ev.get("algorithm") == "B":
            rows.extend(parse_corroborate_line(ev["exit_line"]))
    for r in rows:
        for ev in events:
            if ev.get("claim_id") != r.claim_id:
                continue
            if ev["event"] == "claim_recorded":
                r.kind = ev["kind"] + (" (override)" if ev.get("kind_override") else "")
                cat = "(b)" if ev["author"] == "MAIN" else "(a)"
                r.sources.append(f"{cat} {ev['author']}: {ev['evidence_type']} {ev['evidence_ref']}"
                                 + (f" [{ev['framing']}]" if ev.get("framing") else ""))
            elif ev["event"] == "check_executed" and ev.get("falsifies") == r.claim_id:
                r.sources.append(f"(c) [{ev['mechanism']}] {ev['command']} expected={ev['expected']} observed={ev['observed']}"
                                 + (" pre_fix=FAIL" if ev.get("pre_fix_result") == "FAIL" else ""))
    return rows


def stage_exits(events: list[dict], run_id: str | None = None) -> list[str]:
    return [ev["exit_line"] for ev in events if ev.get("event") == "exit"
            and (run_id is None or ev.get("run_id") == run_id)]


def render_trace(events: list[dict], title: str = "Run trace", run_id: str | None = None) -> str:
    """The trace of ONE run. `run_id` names it; absent, the first event's run decides.
    A merged journal renders only the titled run's rows — the artifact a human audits
    must not mix another run's evidence into this run's corroboration table."""
    run_id = run_id if run_id is not None else next((ev.get("run_id") for ev in events), "run")
    events = [ev for ev in events if ev.get("run_id") == run_id]
    out = [f"# {title} — {run_id}", "", "## Stage exits", "```"]
    out += stage_exits(events)
    out += ["```", ""]
    rows = claim_rows(events)
    out += ["## Corroboration (per claim)", "| claim | kind | n_required | n_available | sources | remedy |",
            "|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| `{r.claim_id}` | {r.kind} | {r.n_required} | {r.n_available} | "
                   f"{'; '.join(r.sources) or 'none'} | {r.remedy or 'n/a (not capped)'} |")
    out.append("")
    out += ["## Claim kind overrides (D-KIND: author's `executable` over the rule's `judgment`)",
            "| claim | author | closed_world |", "|---|---|---|"]
    ov = kind_overrides(events, run_id)
    out += [f"| `{o['claim_id']}` | {o['author']} | {o['closed_world']} |" for o in ov] or ["| none | | |"]
    out.append("")
    out += ["## Consumer checks", "| ref | answer | command_or_reasoning |", "|---|---|---|"]
    for ev in events:
        if ev.get("event") == "consumer_check":
            out.append(f"| `{', '.join(ev['ref'])}` | {ev['answer']} | {ev['command_or_reasoning']} |")
    out.append("")
    dispatches = [ev for ev in events if ev.get("event") == "dispatch"]
    out += [f"## Dispatches ({len(dispatches)} agents)", "| agent | role | framing | output |", "|---|---|---|---|"]
    for ev in dispatches:
        out.append(f"| {ev['agent_id']} | {ev['role']} | {ev['framing']} | `{ev['output_path']}` |")
    out.append("")
    return "\n".join(out)


def consumer_check_refs(events: list[dict]) -> set[str]:
    return {r for ev in events if ev.get("event") == "consumer_check" for r in ev["ref"]}
