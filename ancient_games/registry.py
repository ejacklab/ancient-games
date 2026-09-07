"""§3 — the registry: rows as data, D6 matching, D2/D2′ specificity and hub union.

Matching semantics (D6): `dir` rows are directory-prefix matches; `file`
rows are exact-path matches; `callable` rows match the fully-qualified
import path an action declares with `mode=invoke`; `action` rows match the
action's declared `verb`. R9 has no key at all — it is declared per
instance via `ArtifactRef.external_state`.

Same-ref specificity (D2): when more than one row matches the identical
ref, the most specific wins and the generic match is suppressed.

Hub union (D2′): `hub = (same-ref survivors with hub?=yes) ∪ (registered
downstream-consumer matches with hub?=yes)`; `stakes = max` over every
matched row in both sets, `hub?` notwithstanding; default 1 if nothing
matches.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .ctx import ArtifactRef

CAP = 3


@dataclass(frozen=True)
class Row:
    id: str
    pattern: tuple[str, ...]  # matchable keys; () for verb-/instance-keyed rows
    kind: str  # dir | file | callable | action
    verb: str | None
    stakes: int
    hub: bool
    gate: str  # none | checkpoint | owner
    owner: str | None
    note: str
    hub_name: str | None = None  # name a matched hub element carries; None -> pattern / per instance


REGISTRY: list[Row] = [
    Row("R1", ("eval/protocol.json",), "file", None, 3, True, "owner", "ej",
        "Owner-gated protocol governing the sealed-holdout decision; read is exempt (S2)."),
    Row("R2", ("eval/holdout_access.log",), "file", None, 3, True, "owner", "ej",
        "Access ledger for the one-shot decision; any invoke(append)/mutate is part of the audit trail."),
    Row("R3", ("eval.partitions.load_holdout",), "callable", None, 3, True, "owner", "ej",
        "The sealed loader itself; invoke is the one-shot unseal act."),
    Row("R4", ("loop/program_db.jsonl",), "file", None, 2, True, "checkpoint", None,
        "Append-only event journal; frequently a consumer match (D2′), not a direct one."),
    Row("R5", ("eval/ledger.jsonl",), "file", None, 2, True, "checkpoint", None,
        "Permanent trial-count record; not effectively VCS-revertible."),
    Row("R6", (), "action", "commit", 2, True, "checkpoint", None,
        "Any commit to the default branch; matched by verb regardless of diff content.",
        hub_name="default-branch-history"),
    Row("R7", ("engine/", "runner.py", "config.py", "eval/", "loop/"), "dir", None, 2, False, "checkpoint", None,
        "Production/scoring-path surface edits; hub?=no (D2′); gate enforced at the commit (R6)."),
    Row("R8", ("research/", "tests/", "scratchpad"), "dir", None, 1, False, "none", None,
        "Disposable/exploratory surface."),
    Row("R9", (), "action", None, 3, True, "owner", "ej",
        "External system state reached indirectly through a mutated in-repo constant; declared per instance."),
]

_SPECIFICITY = {"dir": 1, "file": 2, "callable": 2, "action": 3}


def row_by_id(rid: str, registry: Iterable[Row] = REGISTRY) -> Row:
    for r in registry:
        if r.id == rid:
            return r
    raise KeyError(rid)


@dataclass(frozen=True)
class Match:
    row: Row
    ref: str
    hub_element: str | None  # name the hub carries if row.hub, else None
    via: str  # "direct" | "consumer"


def _matches_key(row: Row, ref: ArtifactRef) -> bool:
    if row.kind == "dir":
        return any(ref.path == p or ref.path.startswith(p) for p in row.pattern)
    if row.kind == "file":
        return ref.path in row.pattern
    if row.kind == "callable":
        return ref.mode == "invoke" and ref.path in row.pattern
    if row.kind == "action":
        if row.verb is not None:
            return ref.verb == row.verb
        return ref.external_state is not None  # R9: per-instance declaration
    return False


def _hub_element(row: Row, ref: ArtifactRef) -> str | None:
    if not row.hub:
        return None
    if row.hub_name:
        return row.hub_name
    if row.kind == "action" and row.verb is None:
        return ref.external_state
    if row.kind in ("file", "callable"):
        return ref.path
    return None


def direct_matches(ref: ArtifactRef, registry: Iterable[Row] = REGISTRY) -> list[Match]:
    """All rows matching this one ref, then same-ref specificity suppression (D2)."""
    if ref.mode == "read":
        return []  # reads are never gated and never registry-matched (S2)
    hits = [r for r in registry if _matches_key(r, ref)]
    if not hits:
        return []
    best = max(_SPECIFICITY[r.kind] for r in hits)
    survivors = [r for r in hits if _SPECIFICITY[r.kind] == best]
    if len(survivors) > 1 and best == 1:
        longest = max(len(p) for r in survivors for p in r.pattern if ref.path.startswith(p))
        survivors = [r for r in survivors if any(len(p) == longest and ref.path.startswith(p) for p in r.pattern)]
    return [Match(r, ref.path, _hub_element(r, ref), "direct") for r in survivors]


def consumer_matches(ref: ArtifactRef, registry: Iterable[Row] = REGISTRY) -> list[Match]:
    """Registered (stakes≥2) downstream consumers the action declared for a non-read ref."""
    if ref.mode == "read":
        return []
    out = []
    for c in ref.consumers:
        cref = ArtifactRef(path=c, mode="mutate")
        for r in registry:
            if r.kind in ("file", "callable") and c in r.pattern and r.stakes >= 2:
                out.append(Match(r, c, _hub_element(r, cref), "consumer"))
    return out


@dataclass
class Lookup:
    stakes: int
    hubs: list[str]
    gate: str  # none | checkpoint | owner
    owner: str | None
    matched: list[Match] = field(default_factory=list)

    def __iter__(self):
        yield self.stakes
        yield self.hubs
        yield self.gate
        yield self.owner

    @property
    def row_ids(self) -> list[str]:
        return [m.row.id for m in self.matched]

    @property
    def consumer_answer(self) -> str:
        cons = [m.row.id for m in self.matched if m.via == "consumer"]
        return ",".join(cons) if cons else "no"

    def tripwire_keys(self, hub: str) -> list[str]:
        """H6 (ABLATION_1): the keys a declared tripwire for `hub` may carry — the hub element's
        own name first, then the path of every ref that matched into it."""
        keys = [hub]
        for m in self.matched:
            if m.hub_element == hub and m.ref not in keys:
                keys.append(m.ref)
        return keys


def lookup(refs: Iterable[ArtifactRef], registry: Iterable[Row] = REGISTRY) -> Lookup:
    """D·2: look up every invoke/mutate ref; stakes = max over all matched rows
    in both sets; hub = union of hub?=yes survivors and hub?=yes consumers;
    gate per D·5 (stakes≥2 ⇒ checkpoint; stakes=3 ⇒ owner, named per the
    row's own owner column)."""
    registry = list(registry)
    matched: list[Match] = []
    for ref in refs:
        matched.extend(direct_matches(ref, registry))
        matched.extend(consumer_matches(ref, registry))
    if not matched:
        return Lookup(1, [], "none", None, [])
    stakes = max(m.row.stakes for m in matched)
    hubs: list[str] = []
    for m in matched:
        if m.hub_element and m.hub_element not in hubs:
            hubs.append(m.hub_element)
    if stakes == 3:
        owners = [m.row.owner for m in matched if m.row.stakes == 3 and m.row.owner]
        return Lookup(3, hubs, "owner", owners[0] if owners else None, matched)
    if stakes == 2:
        return Lookup(2, hubs, "checkpoint", None, matched)
    return Lookup(1, hubs, "none", None, matched)
