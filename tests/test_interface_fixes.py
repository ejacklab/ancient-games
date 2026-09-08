"""The five tool-interface fixes (docs/INTERFACE_FIXES_IMPL.md).

Step 0 pins the two forge reproductions BEFORE the fix exists: both are
`xfail(strict=True)` here, so they must FAIL at this commit — that is what proves they
test the hole and not the fix. This repo has twice shipped a green test that could not
fail; a test written after its fix cannot demonstrate it ever could.

The forge: `author` was a free caller string, and B·1 counts a category-(a) source as
`author != actor` (stages.py:325). Three invented author names bought n=3/3 with zero
dispatches — at stakes 3 (`ctx.governance_gated = "R1"`); at stakes 1 B·1 short-circuits
to `n=1 (single source)` and the forge does not reproduce.
"""
from __future__ import annotations

import pytest

from ancient_games.ctx import Ctx
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import (corroborate as corroborate_tool, ingest_return as ingest_tool,
                                        record_claim as record_claim_tool)
from ancient_games.hybrid.types import ToolEnv

TOOLS = load_tools()
ACTION = "claim the thing"
CLAIM = "C1"
FORGED = ("ghost-a", "ghost-b", "ghost-c")
FRAMINGS = ("f1", "f2", "f3")


def _env(tmp_path):
    """stakes 3 via governance_gated=R1 — n_required 3, so three sources are needed."""
    ctx = Ctx()
    ctx.actor = {ACTION: "MAIN"}
    ctx.governance_gated = "R1"
    return ToolEnv("tif", str(tmp_path / "j.jsonl"), ctx, cwd=str(tmp_path), tools=TOOLS)


def _corroborate(env):
    return corroborate_tool.run(env, {"action": ACTION, "claims": [{"claim_id": CLAIM, "kind": "judgment"}]})


# --- step 0: the two forges ---------------------------------------------------------------
@pytest.mark.xfail(strict=True, reason="step 0 pins the hole; F1 (step 1) closes it")
def test_forge_via_record_claim_is_refused(tmp_path):
    env = _env(tmp_path)
    for author, framing in zip(FORGED, FRAMINGS):
        r = record_claim_tool.run(env, {"claim_id": CLAIM, "author": author, "actor": "MAIN", "kind": "judgment",
                                        "text": "the thing holds", "evidence_type": "command",
                                        "evidence_ref": "$ true", "framing": framing})
        assert r.ok is False, f"a claim authored by the never-dispatched {author!r} was recorded"
    assert "n=3/3" not in _corroborate(env).value.exit_line


@pytest.mark.xfail(strict=True, reason="step 0 pins the hole; F1 (step 1) closes it")
def test_forge_via_ingest_return_is_refused(tmp_path):
    env = _env(tmp_path)
    for agent_id, framing in zip(FORGED, FRAMINGS):
        r = ingest_tool.run(env, {"agent_id": agent_id, "actor": "MAIN", "framing": framing,
                                  "fields": {"CLAIMS": [{"claim_id": CLAIM, "kind": "judgment",
                                                         "text": "the thing holds", "evidence_type": "command",
                                                         "evidence_ref": "$ true", "framing": framing}]}})
        assert r.ok is False, f"a return from the never-dispatched {agent_id!r} was ingested"
    assert "n=3/3" not in _corroborate(env).value.exit_line
