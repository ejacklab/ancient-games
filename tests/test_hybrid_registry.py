"""HYBRID_SPEC §2 — manifest validation, the uniform signature check, discovery."""
from __future__ import annotations

import textwrap

import pytest

from ancient_games.hybrid.registry import (COSTS, INVARIANTS, ManifestError, REQUIRED, SIDE_EFFECTS, check_signature,
                                          load_tools, register, validate_manifest)
from ancient_games.hybrid.types import ToolEnv, ToolResult, hydrate
from ancient_games.stages import ActionInput, TaskInput

GOOD = {"name": "t", "inputs": {}, "outputs": "x", "side_effects": "read", "cost": "cheap", "participates_in": [], "entrypoint": "run"}
EIGHTEEN = ["commit", "corroborate", "dispatch", "done", "filter_candidates", "gate", "guard", "ingest_return", "localize",
            "lookup_registry", "prove", "read_journal", "rebuild_index", "record_check", "record_claim", "render_trace",
            "run_lint", "run_suite"]


def test_builtin_discovery_registers_the_spec_table_minus_dispatch_failed():
    tools = load_tools()
    assert sorted(tools) == EIGHTEEN and "dispatch_failed" not in tools
    assert tools["rebuild_index"].side_effects == "mutate"
    assert [n for n, t in tools.items() if t.side_effects == "mutate"] == ["rebuild_index"]
    assert tools["commit"].manifest["participates_in"] == ["I1", "I4"] and tools["dispatch"].manifest["cost"] == "agent"
    assert tools["run_suite"].manifest["cost"] == "suite"
    for t in tools.values():
        assert validate_manifest(t.manifest) is t.manifest
        assert check_signature(t.fn) is t.fn


def test_manifest_validation():
    assert validate_manifest(GOOD) is GOOD
    for k in REQUIRED:
        with pytest.raises(ManifestError, match=f"missing \\['{k}'\\]"):
            validate_manifest({kk: v for kk, v in GOOD.items() if kk != k})
    with pytest.raises(ManifestError, match="side_effects 'destroy'"):
        validate_manifest({**GOOD, "side_effects": "destroy"})
    with pytest.raises(ManifestError, match="cost '—'"):
        validate_manifest({**GOOD, "cost": "—"})  # L3: dispatch_failed's old row could never register
    with pytest.raises(ManifestError, match="participates_in"):
        validate_manifest({**GOOD, "participates_in": ["I6"]})
    with pytest.raises(ManifestError, match="must be a dict"):
        validate_manifest([])
    assert SIDE_EFFECTS == ("none", "read", "invoke", "mutate", "commit") and COSTS == ("cheap", "agent", "suite")
    assert INVARIANTS == ("I1", "I2", "I3", "I4", "I5")


def test_signature_check_exactly_env_args():
    def good(env, args):
        return None
    assert check_signature(good) is good
    for bad in (lambda env: None, lambda env, args, extra: None, lambda env, args=None: None, lambda *a: None,
                lambda env, **kw: None, lambda ctx, args: None, 42):
        with pytest.raises(ManifestError):
            check_signature(bad)


def _drop(tmp_path, name, body):
    p = tmp_path / f"{name}.py"
    p.write_text(textwrap.dedent(body))
    return p


def test_uc9_tool_dropped_into_a_directory_is_discovered(tmp_path):
    _drop(tmp_path, "shout", '''
        from ancient_games.hybrid.types import ToolResult
        MANIFEST = {"name": "shout", "inputs": {"s": "str"}, "outputs": "str", "side_effects": "none",
                    "cost": "cheap", "participates_in": [], "entrypoint": "run"}
        def run(env, args):
            return ToolResult(ok=True, value=args["s"].upper())
    ''')
    _drop(tmp_path, "_helper", "X = 1\n")  # underscore-prefixed modules are not tools
    tools = load_tools(str(tmp_path))
    assert "shout" in tools and "_helper" not in tools and len(tools) == 19
    env = ToolEnv("r", str(tmp_path / "j.jsonl"), None)
    assert tools["shout"].fn(env, {"s": "hi"}) == ToolResult(True, "HI", None)


def test_malformed_dropped_in_tool_never_registers(tmp_path):
    _drop(tmp_path, "nomanifest", "def run(env, args):\n    return None\n")
    with pytest.raises(ManifestError, match="MANIFEST must be a dict"):
        load_tools(str(tmp_path))
    (tmp_path / "nomanifest.py").unlink()
    _drop(tmp_path, "badsig", '''
        MANIFEST = {"name": "badsig", "inputs": {}, "outputs": "x", "side_effects": "none", "cost": "cheap",
                    "participates_in": [], "entrypoint": "run"}
        def run(env, args, extra):
            return None
    ''')
    with pytest.raises(ManifestError, match="signature"):
        load_tools(str(tmp_path))
    (tmp_path / "badsig.py").unlink()
    _drop(tmp_path, "dup", '''
        MANIFEST = {"name": "gate", "inputs": {}, "outputs": "x", "side_effects": "none", "cost": "cheap",
                    "participates_in": [], "entrypoint": "run"}
        def run(env, args):
            return None
    ''')
    with pytest.raises(ManifestError, match="duplicate tool name 'gate'"):
        load_tools(str(tmp_path))


def test_hydrate_recurses_into_nested_dataclasses():
    """L2: the shape a case file supplies (T2's own step-1 gate call, the §2 guard example)."""
    task = hydrate(TaskInput, {"name": "n", "stop_criterion": "s", "difficulty": "LOW",
                               "probe": {"path": "research/stability.py", "mode": "read"},
                               "known_facts": [["a", "b", "c", "d"]]})
    assert task.probe.mode == "read" and task.probe.path == "research/stability.py"
    assert task.known_facts == [("a", "b", "c", "d")] and task.probe_action is None and task.capability == []
    action = hydrate(ActionInput, {"name": "e", "refs": [{"path": "runner.py", "mode": "mutate", "consumers": ["x.jsonl"]}]})
    assert action.refs[0].mode == "mutate" and action.refs[0].consumers == ("x.jsonl",) and action.fallback == "retry, then revert"
    with pytest.raises(ValueError, match="unknown keys \\['bogus'\\]"):
        hydrate(ActionInput, {"name": "e", "refs": [], "bogus": 1})
    with pytest.raises(ValueError, match="mode must be one of"):
        hydrate(ActionInput, {"name": "e", "refs": [{"path": "p", "mode": "delete"}]})
