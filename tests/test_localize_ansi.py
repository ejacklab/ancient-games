"""localize must tolerate ANSI colour in captured suite output.

Agent harnesses set FORCE_COLOR/PY_COLORS, so a captured pytest run arrives with SGR
escapes and every ^-anchored pattern in localize missed them. Found while verifying an
unrelated review finding: UC7's suite went red-then-green correctly while localize
reported "no failure located in suite output"."""
from __future__ import annotations

import os

# --- localize must tolerate coloured suite output ------------------------------------------
def test_localize_parses_pytest_output_that_carries_ansi_colour(tmp_path):
    """Harnesses set FORCE_COLOR/PY_COLORS, so a captured pytest run arrives with SGR escapes.
    Every ^-anchored pattern in localize missed them: UC7's suite went red-then-green correctly
    while localize reported 'no failure located in suite output'."""
    import json, subprocess, sys as _s
    from ancient_games.hybrid.tools import localize
    from ancient_games.hybrid.types import ToolEnv

    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "mod.py").write_text("from nope import x\n")
    (tmp_path / "test_x.py").write_text("def test_a():\n    import pkg.mod\n")
    out = subprocess.run([_s.executable, "-m", "pytest", "-q"], cwd=tmp_path,
                         capture_output=True, text=True,
                         env={**os.environ, "FORCE_COLOR": "3"}).stdout
    assert "\x1b[" in out, "this test is only meaningful on coloured output"

    env = ToolEnv(run_id="r", journal_path=str(tmp_path / "j.jsonl"), ctx=None, cwd=str(tmp_path))
    res = localize.run(env, {"suite_output": out})
    assert res.ok, res.reason
    assert res.reason is None
    assert "ModuleNotFoundError" in json.dumps(res.value)
    assert "test_x.py" in json.dumps(res.value)
