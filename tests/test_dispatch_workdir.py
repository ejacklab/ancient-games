import json
import os
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(os.environ.get("DISPATCH_SCRIPT", str(Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts/dispatch.py")))


def test_r1_workdir_runs_engine_in_target_folder(tmp_path):
    (tmp_path / "w" / "q").mkdir(parents=True)
    plan = {
        "run_id": "r1",
        "nodes": [
            {
                "id": "n1",
                "role": "worker",
                "engine": "script",
                "outer_timeout_s": 30,
                "passback": False,
                "workdir": "w/q",
                "cmd": [sys.executable, "-c", "import os; print(os.getcwd())"]
            }
        ]
    }
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "run", str(tmp_path / "plan.json")],
        capture_output=True,
        text=True
    )
    assert r.returncode == 0, r.stderr
    st = json.loads((tmp_path / "runs/r1/dispatch.json").read_text())
    result_text = Path(st["nodes"]["n1"]["result"]).read_text().strip()
    assert Path(result_text).resolve() == (tmp_path / "w/q").resolve()


def test_r2_relative_workdir_resolves_and_creates_missing_folder(tmp_path):
    target = tmp_path / "w" / "new"
    assert not target.exists()
    plan = {
        "run_id": "r2",
        "nodes": [
            {
                "id": "n2",
                "role": "worker",
                "engine": "script",
                "outer_timeout_s": 30,
                "passback": False,
                "workdir": "w/new",
                "cmd": [sys.executable, "-c", "import os; print(os.getcwd())"]
            }
        ]
    }
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "run", str(tmp_path / "plan.json")],
        capture_output=True,
        text=True
    )
    assert r.returncode == 0, r.stderr
    assert target.exists() and target.is_dir()
    st = json.loads((tmp_path / "runs/r2/dispatch.json").read_text())
    result_text = Path(st["nodes"]["n2"]["result"]).read_text().strip()
    assert Path(result_text).resolve() == target.resolve()


def test_r3_no_workdir_runs_in_the_root(tmp_path):
    plan = {
        "run_id": "r3",
        "nodes": [
            {
                "id": "n3",
                "role": "worker",
                "engine": "script",
                "outer_timeout_s": 30,
                "passback": False,
                "cmd": [sys.executable, "-c", "import os; print(os.getcwd())"]
            }
        ]
    }
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "run", str(tmp_path / "plan.json")],
        capture_output=True,
        text=True
    )
    assert r.returncode == 0, r.stderr
    st = json.loads((tmp_path / "runs/r3/dispatch.json").read_text())
    assert Path(st["nodes"]["n3"]["result"]).read_text().strip() == str(tmp_path)


def test_r4_codex_adapter_dry_run_names_workdir_with_dash_c(tmp_path):
    brief_content = "## Template\n...\n## Example\n...\n## Standard\n..."
    (tmp_path / "brief.md").write_text(brief_content)
    plan = {
        "run_id": "r4",
        "nodes": [
            {
                "id": "c",
                "role": "coder",
                "engine": "codex",
                "model": "m",
                "brief": "brief.md",
                "inner_timer": "60s",
                "outer_timeout_s": 70,
                "workdir": "w"
            }
        ]
    }
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "run", str(tmp_path / "plan.json"), "--dry-run"],
        capture_output=True,
        text=True
    )
    assert r.returncode == 0, r.stderr
    assert "[dry-run] c attempt 1:" in r.stdout
    expected_workdir = str((tmp_path / "w").resolve())
    expected_workdir_unresolved = str(tmp_path / "w")
    assert f"-C {expected_workdir}" in r.stdout or f"-C {expected_workdir_unresolved}" in r.stdout


def test_r5_brief_result_and_check_resolve_against_root(tmp_path):
    (tmp_path / "w").mkdir(parents=True, exist_ok=True)
    (tmp_path / "brief.md").write_text("## Template\n## Example\n## Standard\n")
    check_code = (
        "import sys, pathlib\n"
        "res = pathlib.Path(sys.argv[1]).resolve()\n"
        "assert res.is_file(), f'missing result {res}'\n"
        "assert 'runs' in res.parts\n"
    )
    (tmp_path / "check.py").write_text(check_code)
    plan = {
        "run_id": "r5",
        "nodes": [
            {
                "id": "n5",
                "role": "worker",
                "engine": "script",
                "outer_timeout_s": 30,
                "passback": False,
                "workdir": "w",
                "brief": "brief.md",
                "cmd": [sys.executable, "-c", "import os; assert os.path.basename(os.getcwd()) == 'w'; print('done')"],
                "check": {
                    "name": "c",
                    "cmd": [sys.executable, "check.py", "{result}"]
                }
            }
        ]
    }
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "run", str(tmp_path / "plan.json")],
        capture_output=True,
        text=True
    )
    assert r.returncode == 0, r.stderr
    st = json.loads((tmp_path / "runs/r5/dispatch.json").read_text())
    assert st["nodes"]["n5"]["status"] == "done"
    result_file = Path(st["nodes"]["n5"]["result"]).resolve()
    assert result_file.is_file()
    assert (tmp_path / "runs/r5/nodes").resolve() in result_file.parents


def test_r7_check_refuses_workdir_existing_as_file(tmp_path):
    (tmp_path / "x.txt").write_text("not a folder")
    plan = {
        "run_id": "r7",
        "nodes": [
            {
                "id": "node_with_file_workdir",
                "role": "worker",
                "engine": "script",
                "outer_timeout_s": 30,
                "passback": False,
                "workdir": "x.txt",
                "cmd": [sys.executable, "-c", "print('hello')"]
            }
        ]
    }
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "validate", str(tmp_path / "plan.json")],
        capture_output=True,
        text=True
    )
    assert r.returncode == 1, f"Expected returncode 1, got {r.returncode}\nstdout: {r.stdout}\nstderr: {r.stderr}"
    combined = r.stdout + "\n" + r.stderr
    assert "plan refused:" in combined.lower()
    assert "node_with_file_workdir" in combined
    assert "folder" in combined.lower() or "directory" in combined.lower()
