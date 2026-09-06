"""§2 — ctx.validate(): every property is set by a stage and consumed by a field."""
from __future__ import annotations

from dataclasses import fields

import pytest

from ancient_games import ctx as ctxmod
from ancient_games.ctx import CTX_META, CappedClaim, Ctx, GateReason


def test_default_ctx_validates_and_every_property_has_meta():
    c = Ctx()
    c.validate()
    assert {f.name for f in fields(c)} == set(CTX_META)


def test_validate_raises_on_unset_or_unconsumed_property(monkeypatch):
    monkeypatch.setitem(CTX_META, "stakes", ("", "B·1"))
    with pytest.raises(ValueError, match="set by no stage"):
        Ctx().validate()
    monkeypatch.setitem(CTX_META, "stakes", ("D·2", ""))
    with pytest.raises(ValueError, match="referenced by no field"):
        Ctx().validate()
    monkeypatch.setitem(CTX_META, "stakes", ("D·2", "B·1"))
    monkeypatch.setitem(CTX_META, "ghost", ("C·1", "schema X"))
    with pytest.raises(ValueError, match="not a ctx property"):
        Ctx().validate()


def test_enum_values_are_checked():
    c = Ctx()
    c.execution_status = "paused"
    with pytest.raises(ValueError, match="execution_status"):
        c.validate()
    c = Ctx()
    assert c.difficulty == "UNKNOWN" and c.capability == []  # AA2′ escape values
    c.difficulty = "EASY"
    with pytest.raises(ValueError, match="difficulty"):
        c.validate()
    c = Ctx(dispatch_count=-1)
    with pytest.raises(ValueError, match="dispatch_count"):
        c.validate()
    with pytest.raises(ValueError, match="remedy"):
        CappedClaim("x", "judgment", 3, 3, 2, "ask-nicely")
    with pytest.raises(ValueError, match="reason"):
        GateReason("owner(ej)", "irreversible")


def test_keys_set_lists_only_non_defaults():
    c = Ctx()
    assert c.keys_set() == []
    c.count = 2
    c.hub = ["eval/protocol.json"]
    assert c.keys_set() == ["count", "hub"]
    assert ctxmod.REMEDIES == ("add-claim-specific-check", "add-differently-framed-source", "gate-checkpoint", "gate-owner")
