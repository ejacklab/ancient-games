"""§2 — the ctx object.

Every property is set by a named algorithm step and consumed by a named
field, step, or lint. `validate()` raises if the dataclass carries a
property the metadata table says no stage sets or nothing consumes — "an
unset property is a lint in itself: a field whose `when` depends on it can
never fire" (V3_1_SPEC §2).
"""
from __future__ import annotations

import re
from dataclasses import MISSING, dataclass, field, fields
from typing import Any

ROLES = ("coder", "researcher", "tester", "MAIN")
EXECUTION_STATUSES = ("main_executes", "hard_blocked", "mixed", "dispatched")
REVERSIBILITIES = ("git-revertible", "restorable", "irreversible")
CLAIM_KINDS = ("executable", "judgment")
# D-KIND (docs/ABLATION_2.md): a claim whose text asserts an absence or a universal negative is an
# open-world claim — `judgment` by rule unless the author states why the check space is closed
# (`closed_world`). Word-bounded, case-insensitive; a floor, not a proof. The one place the list lives.
ABSENCE_PATTERNS = ("dead", "unused", "no references?", "never", "nothing calls", "not reachable", "no callers?",
                    "unreferenced")
_ABSENCE_RE = re.compile(r"\b(?:" + "|".join(ABSENCE_PATTERNS) + r")\b", re.IGNORECASE)


def kind_by_rule(text: str) -> str | None:
    """`judgment` when `text` matches an absence/universal-negative pattern, else None (author's kind stands)."""
    return "judgment" if _ABSENCE_RE.search(text or "") else None


REMEDIES = (
    "add-claim-specific-check",
    "add-differently-framed-source",
    "gate-checkpoint",
    "gate-owner",
)
GATE_REASONS = (
    "stakes-2-checkpoint",
    "stakes-3-owner",
    "governance-gated",
    "corroboration-capped",
)
MODES = ("read", "invoke", "mutate")
DIFFICULTIES = ("LOW", "MED", "HIGH", "UNKNOWN")  # AA2′; UNKNOWN is the escape value
MECHANISMS = ("interpreter-import", "pytest-fail-first", "suite-count", "git-diff-scope", "hash-compare", "adversarial-case")


@dataclass(frozen=True)
class ArtifactRef:
    """One `artifact_refs` entry (§2, S2).

    `consumers` and `external_state` are the per-instance declarations D·2
    reads: the registry never infers a downstream consumer from code (D6),
    and R9's external-system entity is "declared per instance" (§3).
    """

    path: str
    mode: str
    verb: str | None = None
    consumers: tuple[str, ...] = ()
    external_state: str | None = None

    def __post_init__(self) -> None:
        if self.mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}, got {self.mode!r}")


@dataclass(frozen=True)
class GateReason:
    """One `gate_reason` entry: who gates, why, and (for a capped claim) which claim."""

    who: str  # "human(checkpoint)" | "owner(<name>)"
    reason: str  # one of GATE_REASONS
    claim_id: str | None = None

    def __post_init__(self) -> None:
        if self.reason not in GATE_REASONS:
            raise ValueError(f"reason must be one of {GATE_REASONS}, got {self.reason!r}")


@dataclass(frozen=True)
class CappedClaim:
    """One `corroboration_capped` entry (§2, X1′ adds `remedy`)."""

    claim_id: str
    kind: str
    capped_from: int
    mandated: int
    delivered: int
    remedy: str
    detail: str | None = None  # the framing (judgment) or mechanism (executable) the remedy names (DECISIONS.md #21)

    def __post_init__(self) -> None:
        if self.kind not in CLAIM_KINDS:
            raise ValueError(f"kind must be one of {CLAIM_KINDS}")
        if self.remedy not in REMEDIES:
            raise ValueError(f"remedy must be one of {REMEDIES}, got {self.remedy!r}")


@dataclass
class Ctx:
    # C-set
    role: str = "MAIN"
    count: int = 0
    execution_status: str | None = None
    stop_criterion: str | None = None
    time_box: str | None = None
    difficulty: str = "UNKNOWN"  # AA2′: LOW | MED | HIGH, escape UNKNOWN
    capability: list[str] = field(default_factory=list)  # AA2′: escape []
    actor: dict[str, str] = field(default_factory=dict)  # action_id -> agent-id | MAIN | none (Z3′)
    dispatch_count: int = 0  # plan-wide category-(a) dispatches so far (Z1′); cap_state = (dispatch_count, CAP=3)
    governance_gated: str = "none"
    known_facts: list[tuple[str, str, str, str]] = field(default_factory=list)
    stale_claims: list[tuple[str, str]] = field(default_factory=list)
    prior_findings: list[str] = field(default_factory=list)
    tools_required: list[str] = field(default_factory=list)
    standing_clauses: str = ""
    env_policy: str = ""
    # C·1 / D·1
    artifact_refs: list[ArtifactRef] = field(default_factory=list)
    # D-set
    reversibility: str | None = None
    hub: list[str] = field(default_factory=list)
    stakes: int | None = None
    tripwire: dict[str, str] = field(default_factory=dict)  # hub element -> command
    write_boundary: list[str] = field(default_factory=list)
    gate_reason: list[GateReason] = field(default_factory=list)
    # B-set
    n_sources: dict[str, int] = field(default_factory=dict)
    corroboration_capped: list[CappedClaim] = field(default_factory=list)
    claim_kind: dict[str, str] = field(default_factory=dict)
    framing: str | None = None
    siblings: list[str] = field(default_factory=list)
    # E-set
    scope_items: list[str] = field(default_factory=list)
    closure: str = "floor"
    authoritative_doc: str = "none"
    adds_tests: bool = False
    touches_shared_files: bool = False
    verify_cmds: list[tuple[str, str]] = field(default_factory=list)
    template_version: str = ""

    def validate(self) -> None:
        """Raise ValueError on a property no stage sets or nothing consumes,
        or on a value outside its declared enum."""
        names = {f.name for f in fields(self)}
        for name in names:
            meta = CTX_META.get(name)
            if meta is None:
                raise ValueError(f"ctx property {name!r} has no set-by/consumed-by entry")
            set_by, consumed_by = meta
            if not set_by:
                raise ValueError(f"ctx property {name!r} is set by no stage")
            if not consumed_by:
                raise ValueError(f"ctx property {name!r} is referenced by no field")
        for name in CTX_META:
            if name not in names:
                raise ValueError(f"CTX_META names {name!r}, which is not a ctx property")
        if self.difficulty not in DIFFICULTIES:
            raise ValueError(f"difficulty {self.difficulty!r} not in {DIFFICULTIES}")
        if self.dispatch_count < 0:
            raise ValueError("dispatch_count must be non-negative")
        if self.role not in ROLES:
            raise ValueError(f"role {self.role!r} not in {ROLES}")
        if self.execution_status is not None and self.execution_status not in EXECUTION_STATUSES:
            raise ValueError(f"execution_status {self.execution_status!r} not in {EXECUTION_STATUSES}")
        if self.reversibility is not None and self.reversibility not in REVERSIBILITIES:
            raise ValueError(f"reversibility {self.reversibility!r} not in {REVERSIBILITIES}")
        if self.stakes is not None and self.stakes not in (1, 2, 3):
            raise ValueError(f"stakes {self.stakes!r} not in (1, 2, 3)")
        if not 0 <= self.count <= 3:
            raise ValueError(f"count {self.count!r} outside 0..3")
        if self.closure not in ("floor", "exhaustive"):
            raise ValueError(f"closure {self.closure!r} not in (floor, exhaustive)")
        for cid, kind in self.claim_kind.items():
            if kind not in CLAIM_KINDS:
                raise ValueError(f"claim_kind[{cid!r}]={kind!r} not in {CLAIM_KINDS}")
        for e in self.hub:
            if e not in self.tripwire and self.stakes is not None and self.stakes >= 2:
                # D·4 names one tripwire per hub element; a gap here is what the
                # hub-touched-without-tripwire lint catches, so only warn via lint.
                pass

    def keys_set(self) -> list[str]:
        """Names of properties holding a non-default value (for `ctx_keys_set`)."""
        out = []
        for f in fields(self):
            v = getattr(self, f.name)
            default = f.default if f.default_factory is MISSING else f.default_factory()  # type: ignore[misc]
            if v != default:
                out.append(f.name)
        return out

    def as_dict(self) -> dict[str, Any]:
        return {f.name: getattr(self, f.name) for f in fields(self)}


# property -> (set by, consumed by), from V3_1_SPEC §2 with the V3.2/V3.3 rows.
# `difficulty` and `capability` are AA2′'s two rows (V3.6); `actor`/`dispatch_count` are V3.5 §2.
CTX_META: dict[str, tuple[str, str]] = {
    "role": ("C·2", "schema DISPATCH"),
    "count": ("C·3 / C·4", "schema (payload gate)"),
    "execution_status": ("C·3; D·5 override", "schema (Gate/Guard exit lines)"),
    "stop_criterion": ("C·5", "schema STOP"),
    "time_box": ("C·5", "schema STOP"),
    "difficulty": ("C·2", "C·3 (F1 decision tree), C exit line"),
    "capability": ("C·2", "C·3 (F1 decision tree), schema role selection, D·4 tool grants"),
    "actor": ("C·3/C·4, or D at execution_status=main_executes", "B·1 self-exclusion, journal claim_recorded.actor"),
    "dispatch_count": ("C·3/C·4; B·1 on RETURN_TO_PLANNER-triggered dispatch", "B·1 cap_state"),
    "artifact_refs": ("C·1, D·1", "C·1 routing, D·2, registry, lints"),
    "governance_gated": ("C·2", "B·1, E·5, A"),
    "reversibility": ("D·3", "schema HUB_INTEGRITY/fallback shape"),
    "hub": ("D·2", "schema WRITE_BOUNDARY/HUB_INTEGRITY, lints"),
    "stakes": ("D·2", "B·1 n_required, D·5 gate rule"),
    "tripwire": ("D·4", "schema HUB_INTEGRITY, lint hub-touched-without-tripwire"),
    "n_sources": ("B·1", "schema FRAMING, TEMPLATE"),
    "corroboration_capped": ("B·1", "lint corroboration-capped, HUMAN_GATE, A"),
    "claim_kind": ("B·1", "B·1, lint corroboration-capped"),
    "framing": ("B·2", "schema FRAMING"),
    "siblings": ("B·3", "schema READ_SCOPE.deny"),
    "scope_items": ("E·4", "schema SCOPE"),
    "closure": ("E·4", "schema SCOPE"),
    "authoritative_doc": ("E·4", "schema RECONCILE_AGAINST"),
    "known_facts": ("C·1", "schema KNOWN_FACTS"),
    "stale_claims": ("C·1", "schema VERIFY_NOT_CITE"),
    "prior_findings": ("C·1", "schema PRIOR_FINDINGS"),
    "adds_tests": ("E·4", "schema NEW_TEST_PROOF"),
    "touches_shared_files": ("E·4", "schema INTERFACE_MAP/ISOLATION"),
    "tools_required": ("C·2", "schema TOOLING_FALLBACK"),
    "verify_cmds": ("E·4", "schema VERIFY/ACCEPTANCE_GATE"),
    "standing_clauses": ("C·2", "schema STANDING_INSTRUCTIONS"),
    "write_boundary": ("D·2, D·4", "schema WRITE_BOUNDARY"),
    "gate_reason": ("D·5, E·5/A", "schema HUMAN_GATE"),
    "env_policy": ("orchestrator constant, C·2", "CORE ENV_POLICY"),
    "template_version": ("E·5", "schema TEMPLATE.version, journal"),
}
