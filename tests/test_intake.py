"""Run the intake workflow's offline scheduling and sabotage harness under pytest."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_intake_harness():
    r = subprocess.run(["node", str(ROOT / "tests/workflows/intake_harness.mjs")],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "all passed" in r.stdout
