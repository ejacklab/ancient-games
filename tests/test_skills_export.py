import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_skills_export_is_self_contained():
    """The bundle is a generated artifact: no symlinks, and the exported design_gate finds its own TASK_TYPES.md."""
    # regenerate the bundle from the source of truth
    r = subprocess.run([sys.executable, "tools/export_skills.py"], capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0, r.stderr

    skills = REPO / "skills"
    assert not any(p.is_symlink() for p in skills.rglob("*")), "the bundle must be symlink-free"

    # the portability fix: design_gate resolves --types relative to its own folder, so it works in the bundle
    r = subprocess.run(
        [sys.executable, "skills/workflow-design/scripts/design_gate.py", "--self-test"],
        capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "self-test: PASS" in r.stdout, r.stdout


def test_skills_export_is_current():
    """The committed skills/ must match a fresh export — drift is caught, not hand-synced."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # copy the export script to a scratch repo layout and run it into the temp dir is overkill;
        # instead, re-run the export and diff the committed skills/ against what it just produced.
        # The simplest sound check: re-running the export is idempotent (git status stays clean on skills/).
        before = subprocess.run(["git", "diff", "--name-only", "--", "skills/"], capture_output=True, text=True, cwd=REPO)
        assert before.stdout.strip() == "", f"skills/ already drifted before export:\n{before.stdout}"
        subprocess.run([sys.executable, "tools/export_skills.py"], check=True, capture_output=True, cwd=REPO)
        after = subprocess.run(["git", "diff", "--name-only", "--", "skills/"], capture_output=True, text=True, cwd=REPO)
        assert after.stdout.strip() == "", f"a fresh export changed skills/ (drift):\n{after.stdout}"
