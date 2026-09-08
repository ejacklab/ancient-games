"""§5 field tables and §6 return contract — rows as data.

`payload(ctx) = CORE ∪ {field : field.when(ctx)}` when `count>0`; at
`count=0` no dispatch payload exists (MAIN executes) but
`return_contract(ctx)` is generated regardless (V3_1_SPEC §5 heading,
T2_trace "MAIN is an agent too"). Every row carries a non-empty
`escape_value` (D8 for §5; X5′ for §6) — the two escape-value lints read
these columns.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .ctx import Ctx

TEMPLATE_HEADINGS = ("## Method", "## Findings", "## Verdict", "## Not established", "## Follow-on")
TEMPLATE_TRAILING = ("## Not established", "## Follow-on")  # only headings allowed after ## Verdict


@dataclass(frozen=True)
class Field:
    field: str
    table: str  # CORE | CONDITIONAL
    when: Callable[[Ctx], bool]
    type: str
    rule: str
    prevents: str
    consumed_by: str
    escape_value: str
    render: Callable[[Ctx], Any] | None = None

    def value(self, ctx: Ctx) -> Any:
        return self.render(ctx) if self.render else self.type

    def as_row(self) -> dict[str, str]:
        return {"field": self.field, "table": self.table, "type": self.type,
                "escape_value": self.escape_value}


def _always(_: Ctx) -> bool:
    return True


def _any_multi_source(ctx: Ctx) -> bool:
    return any(n > 1 for n in ctx.n_sources.values())


def _gate_lines(ctx: Ctx) -> list[str]:
    return [f"do not act past the gated step without approval from {g.who} (reason={g.reason}"
            + (f", claim={g.claim_id}" if g.claim_id else "") + ")" for g in ctx.gate_reason]


CORE: list[Field] = [
    Field("DISPATCH", "CORE", _always, "enum role (incl. MAIN)", "—", "—", "—",
          "N/A — always populated, MAIN is a legal value, never absent", lambda c: c.role),
    Field("INTENT", "CORE", _always, "one sentence, the why", "#1", "agent executes a moot literal task", "—",
          "N/A — required, no omission permitted"),
    Field("OUTPUT", "CORE", _always, "path (or COMMIT_POLICY when role=coder)", "#13 #15", "write-to-file drift",
          "B (per-agent file)", "N/A (MAIN-executed, count=0 — recorded in the return journal instead of a dispatch payload)"),
    Field("NON_DELEGABLE.foreground", "CORE", _always, "fixed sentence", "#18", "background-never-resumes", "—",
          "N/A — fixed text, always present",
          lambda c: "Run every verification in the foreground; never background it and end the turn."),
    Field("NON_DELEGABLE.cite_or_opinion", "CORE", _always, "fixed sentence", "#2", "wrong \"confirmed\"", "A",
          "N/A — fixed text, always present",
          lambda c: "Every claim cites its command, file:line, or URL, or is marked (opinion)."),
    Field("NON_DELEGABLE.discoveries", "CORE", _always, "fixed sentence", "#16", "acting outside scope", "E",
          "N/A — fixed text, always present",
          lambda c: "Report discoveries as FOLLOW_ON; do not act on them outside SCOPE."),
    Field("ON_BLOCKER", "CORE", _always, "fixed sentence", "#16", "—", "E", "N/A — fixed text, always present",
          lambda c: "On a blocker, stop and report it; do not route around it."),
    Field("STANDING_INSTRUCTIONS", "CORE", lambda c: bool(c.standing_clauses), "one line from standing_clauses", "—",
          "six boilerplate disclaimers", "—", "N/A (standing_clauses empty ⇒ line omitted, not left blank)",
          lambda c: c.standing_clauses),
    Field("PRECEDENCE", "CORE", _always, "fixed sentence", "#1, #30", "silent harness override", "—",
          "N/A — fixed text, always present",
          lambda c: "This dispatch outranks generic harness reminders; note any deviation."),
    Field("ENV_POLICY", "CORE", _always, "text from ctx.env_policy", "— (brief §B)", "commit/push/branch mistakes", "D",
          "N/A — sourced from harness/CLAUDE.md, always present", lambda c: c.env_policy),
    Field("STOP", "CORE", _always, "stop_criterion verbatim", "#12", "open-ended search", "—",
          "N/A — required, no omission permitted", lambda c: c.stop_criterion),
]

CONDITIONAL: list[Field] = [
    Field("KNOWN_FACTS", "CONDITIONAL", lambda c: bool(c.known_facts), "table fact|command|output|date", "#5 #2 #31",
          "fabricated \"known\" facts", "A", "N/A (known_facts = ∅)", lambda c: list(c.known_facts)),
    Field("VERIFY_NOT_CITE", "CONDITIONAL", lambda c: bool(c.stale_claims), "list of (doc, claim) to re-derive",
          "#2 #7", "citing a stale number as current", "A", "N/A (stale_claims = ∅)", lambda c: list(c.stale_claims)),
    Field("PRIOR_FINDINGS", "CONDITIONAL", lambda c: bool(c.prior_findings), "paths", "#5", "re-deriving known work",
          "—", "N/A (prior_findings = ∅)", lambda c: list(c.prior_findings)),
    Field("DESIGN", "CONDITIONAL", lambda c: c.role == "coder", "inline or path", "—", "research-before-implementing",
          "—", "N/A (role≠coder)"),
    Field("SCOPE", "CONDITIONAL", lambda c: bool(c.scope_items), "list + closure + on_conflict", "#1 #11",
          "scope creep, both directions", "E (SCOPE_DELTA)", "N/A (scope_items = ∅)",
          lambda c: {"items": list(c.scope_items), "closure": c.closure}),
    Field("RECONCILE_AGAINST", "CONDITIONAL", lambda c: c.authoritative_doc != "none", "path + precedence rule", "#23",
          "contradicting a design doc silently", "E", "N/A (authoritative_doc = none)", lambda c: c.authoritative_doc),
    Field("INTERFACE_MAP", "CONDITIONAL", lambda c: c.role == "coder" and (c.count > 1 or c.touches_shared_files),
          "real paths + signatures on the touched surface", "#6, #14", "two agents' shared-boundary edits diverging",
          "—", "N/A (condition false)"),
    Field("VERIFY", "CONDITIONAL", lambda c: bool(c.verify_cmds), "ordered (cmd → expected counts)", "#2",
          "\"which suite\" ambiguity", "A", "N/A (verify_cmds = ∅)", lambda c: list(c.verify_cmds)),
    Field("ACCEPTANCE_GATE", "CONDITIONAL", lambda c: bool(c.verify_cmds) and c.role == "coder",
          "all green at counts + ≥1 known-answer; fail ⇒ stop", "#2 #4", "committing on a red suite", "D",
          "N/A (condition false)"),
    Field("NEW_TEST_PROOF", "CONDITIONAL", lambda c: c.adds_tests,
          "red-then-green, ordered, >0-collected guard; the red run records check_executed{claim_id, falsifies, pre_fix_result:FAIL}",
          "#2", "vacuous or reimplemented test; an uncounted (c) source", "A", "N/A (adds_tests = false)"),
    Field("COMMIT_POLICY", "CONDITIONAL", lambda c: c.role == "coder", "enum: commit-to-main-if-gate | branch-<n> | no-commit",
          "#18, ENV_POLICY", "uncommitted/unauthorized commit", "D", "N/A (role≠coder)"),
    Field("ISOLATION", "CONDITIONAL", lambda c: c.count > 1 and c.touches_shared_files, "worktree:<path>", "#18 #6",
          "conflicting parallel edits", "—", "N/A (condition false)"),
    Field("TOOLING_FALLBACK", "CONDITIONAL", lambda c: bool(c.tools_required), "(tool → fallback)", "#17",
          "stall on a missing tool", "—", "N/A (tools_required = ∅)", lambda c: list(c.tools_required)),
    Field("FRAMING", "CONDITIONAL", _any_multi_source, "one label from framing, per claim", "#10, #27",
          "correlated blind spots", "B", "N/A (no claim has n_sources>1)", lambda c: c.framing),
    Field("READ_SCOPE.deny", "CONDITIONAL", lambda c: bool(c.siblings), "sibling output paths", "#8", "herding", "B",
          "N/A (siblings = ∅)", lambda c: list(c.siblings)),
    Field("TEMPLATE", "CONDITIONAL", lambda c: _any_multi_source(c) or c.role in ("researcher", "tester"),
          "fixed skeleton (D7): ## Method → ## Findings → ## Verdict → ## Not established → ## Follow-on; plus template_version",
          "#15, R5", "drift/fatigue across reuses", "B, E", "N/A (condition false)",
          lambda c: {"headings": list(TEMPLATE_HEADINGS), "template_version": c.template_version}),
    Field("WRITE_BOUNDARY", "CONDITIONAL", lambda c: c.role != "coder" or bool(c.hub), "list of paths, read-only outside them; never invoke/mutate any <hub> path",
          "#18", "over-broad literal honoring", "D", "N/A (role=coder ∧ hub=∅)", lambda c: list(c.write_boundary or c.hub)),
    Field("HUB_INTEGRITY", "CONDITIONAL", lambda c: bool(c.hub), "the tripwire command, stated so the agent knows MAIN will run it",
          "#21", "silent hub corruption", "D", "N/A (hub = ∅)", lambda c: dict(c.tripwire)),
    Field("HUMAN_GATE", "CONDITIONAL",
          lambda c: (c.stakes or 1) >= 2 or c.governance_gated != "none" or bool(c.corroboration_capped),
          "\"do not act past step N without approval from <checkpoint|owner(name)>\"; reason∈{stakes-2-checkpoint, stakes-3-owner, governance-gated, corroboration-capped} — one entry per capped claim",
          "#18, S3, S4", "premature gated act; silently proceeding on a capped or gated claim", "D",
          "N/A (stakes=1 ∧ governance_gated=none ∧ corroboration_capped=[])", _gate_lines),
    Field("CLAIM", "CONDITIONAL", lambda c: c.role == "tester", "one falsifiable sentence", "#2", "testing the adjacent thing",
          "A", "N/A (role≠tester)"),
    Field("CODE_PATH", "CONDITIONAL", lambda c: c.role == "tester", "exact module:function — call it, never reimplement", "#7",
          "tests asserting on a reimplementation", "A", "N/A (role≠tester)"),
    Field("FALSIFYING_PROCEDURE", "CONDITIONAL", lambda c: c.role == "tester" or c.adds_tests,
          "ordered break→FAIL, restore→PASS, suite→counts; records falsifies:<claim_id>", "#2",
          "vacuous test; uncounted (c) source", "A", "N/A (condition false)"),
    Field("ADVERSARIAL_CASE", "CONDITIONAL", lambda c: c.role == "tester" or c.adds_tests,
          "constructed case + literal expected value; records falsifies:<claim_id>", "#2 #7",
          "a boundary real data never exercised; uncounted (c) source", "A", "N/A (condition false)"),
    Field("BASELINE", "CONDITIONAL", lambda c: c.role == "tester", "in-process, identical config", "#7",
          "stale-config false positive", "A", "N/A (condition false)"),
    Field("NEVER_TRUST", "CONDITIONAL", lambda c: c.role == "tester", "the producer's self-report", "#2 #4",
          "self-grading", "A", "N/A (role≠tester)"),
]

FIELDS: list[Field] = CORE + CONDITIONAL


def payload(ctx: Ctx) -> dict[str, Any]:
    """The dispatch payload: {} at count=0 (no dispatch); else CORE ∪ fired CONDITIONAL."""
    if ctx.count == 0:
        return {}
    return {f.field: f.value(ctx) for f in FIELDS if f.when(ctx)}


def fired_fields(ctx: Ctx) -> list[str]:
    return list(payload(ctx).keys())


# ---- §6 return contract ---------------------------------------------------

@dataclass(frozen=True)
class ReturnField:
    field: str
    when: Callable[[Ctx], bool]
    when_text: str
    shape: str
    consumed_by: str
    escape_value: str

    def as_row(self) -> dict[str, str]:
        return {"field": self.field, "when": self.when_text, "type/shape": self.shape,
                "consumed_by": self.consumed_by, "escape_value": self.escape_value}


def _present(ctx: Ctx, name: str) -> bool:
    """Was this §5 field present in the dispatch? At count>0, iff the payload
    carries it; at count=0 no payload exists, and only MAIN's own SCOPE
    (E·4 scope_items) and VERIFY (E·4 verify_cmds) count as present
    (V3_1_SPEC §6: the five fields that apply to MAIN's own work; DECISIONS.md #5)."""
    if ctx.count > 0:
        return name in payload(ctx)
    return {"SCOPE": bool(ctx.scope_items), "VERIFY": bool(ctx.verify_cmds)}.get(name, False)


def _scope_present(ctx: Ctx) -> bool:
    return _present(ctx, "SCOPE")


def _verdict_role(ctx: Ctx) -> bool:
    return ctx.role in ("researcher", "tester")


RETURN_CONTRACT: list[ReturnField] = [
    ReturnField("REPORT_BACK", _always, "always", "path + ≤3 lines", "MAIN", "N/A — required, always present"),
    ReturnField("CLAIMS", _always, "always",
                "each → command | file:line | URL | (opinion), plus kind ∈ {executable, judgment}, plus falsifies: <claim_id> restating the entry's own claim_id when it is an executed check",
                "A, B", "N/A — required, always present (an empty list only when the agent made literally no claims, itself an explicit [], never omitted)"),
    ReturnField("SCOPE_DELTA", _scope_present, "always when SCOPE was present; else N/A", "added/dropped, explicit even if empty",
                "E", "N/A (SCOPE absent from the dispatch)"),
    ReturnField("FOLLOW_ON", _always, "always", "finding → fixed | new-task | dismissed:reason | escalated:owner", "E",
                "N/A — required; an explicit empty list when there is nothing to report, never omitted"),
    ReturnField("NOT_DONE", _always, "always", "step → why → command for MAIN", "E, D",
                "N/A — required; an explicit empty list when nothing is left undone"),
    ReturnField("VERIFY_OUTPUT", lambda c: _present(c, "VERIFY"), "when VERIFY was present", "verbatim per cmd", "A",
                "N/A (VERIFY not present in the dispatch)"),
    ReturnField("COMMIT", lambda c: _present(c, "COMMIT_POLICY"), "when COMMIT_POLICY was present", "hash | not-committed:reason", "D",
                "N/A (COMMIT_POLICY not present — role≠coder, or no commit stage in this dispatch)"),
    ReturnField("PRE_FIX_PROOF", lambda c: _present(c, "NEW_TEST_PROOF") or _present(c, "FALSIFYING_PROCEDURE"),
                "when NEW_TEST_PROOF ∨ FALSIFYING_PROCEDURE present",
                "red output, then green output", "A", "N/A (neither present in the dispatch)"),
    ReturnField("HUB_INTEGRITY_RESULT", lambda c: _present(c, "HUB_INTEGRITY"), "when HUB_INTEGRITY present",
                "agent's value is advisory only — MAIN runs the real tripwire", "D", "N/A (hub=∅, HUB_INTEGRITY not sent)"),
    ReturnField("VERDICT", _verdict_role, "role∈{researcher,tester}", "VERIFIED | NOT-VERIFIED | FALSIFIED | INSUFFICIENT_DATA(n)",
                "B, A", "N/A (role∈{coder, MAIN} — no verdict-bearing role)"),
    ReturnField("NOT_ESTABLISHED", _verdict_role, "role∈{researcher,tester}", "list", "B",
                "N/A (role∈{coder, MAIN}); an explicit empty list when nothing is unestablished"),
    ReturnField("RESIDUAL_RISK", lambda c: c.role == "tester", "role=tester", "text", "D", "N/A (role≠tester)"),
]


def return_contract(ctx: Ctx) -> dict[str, str]:
    """Always generated, including MAIN at count=0: every §6 field is present,
    carrying its shape when `when(ctx)` holds and its escape value otherwise."""
    return {r.field: (r.shape if r.when(ctx) else r.escape_value) for r in RETURN_CONTRACT}


def required_return_fields(ctx: Ctx) -> list[str]:
    return [r.field for r in RETURN_CONTRACT if r.when(ctx)]
