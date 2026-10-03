"""feature_gate.py: the script gate of the build-a-feature pipeline (docs/TASK_TYPES.md, step 4)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts/feature_gate.py"


def junit(path, cases):
    """cases: {id 'cls::name': 'pass'|'fail'|'skip'}"""
    body = []
    for tid, o in cases.items():
        cls, name = tid.split("::")
        inner = {"fail": "<failure message='x'/>", "skip": "<skipped/>"}.get(o, "")
        body.append(f'<testcase classname="{cls}" name="{name}">{inner}</testcase>')
    path.write_text(f'<testsuites><testsuite name="s">{"".join(body)}</testsuite></testsuites>')
    return path


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    for f in ["src/feature/a.py", "src/billing/b.py", "tests/acceptance/test_acc.py", "tests/unit/test_a.py", "README.md"]:
        (r / f).parent.mkdir(parents=True, exist_ok=True)
        (r / f).write_text("x = 1\n")
    git(r, "init", "-q"); git(r, "config", "user.email", "t@t"); git(r, "config", "user.name", "t")
    git(r, "add", "-A"); git(r, "commit", "-qm", "base")
    (tmp_path / "plan.json").write_text(json.dumps({
        "may_change": ["src/feature/*", "tests/unit/*"], "must_not_change": ["src/billing/*"],
        "protected": ["tests/acceptance/*"], "reasons": {"README.md": "documents the feature"}}))
    base = {"t.unit::test_old": "pass", "t.acc::test_case1": "pass", "t.acc::test_flip": "pass"}
    junit(tmp_path / "b1.xml", base)
    junit(tmp_path / "b2.xml", {**base, "t.acc::test_flip": "fail"})
    p = run("baseline", "--junit", tmp_path / "b1.xml", "--junit", tmp_path / "b2.xml", "--out", tmp_path / "base.json")
    assert p.returncode == 0 and "flaky 1" in p.stdout, p.stdout + p.stderr
    return r


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


def check(repo, current):
    t = repo.parent
    junit(t / "now.xml", current)
    return run("check", "--plan", t / "plan.json", "--base-ref", "HEAD", "--baseline", t / "base.json",
               "--junit", t / "now.xml", "--root", repo, "--json")


GOOD_NOW = {"t.unit::test_old": "pass", "t.acc::test_case1": "pass", "t.acc::test_flip": "fail", "t.unit::test_new": "pass"}


def test_clean_change_passes_and_flaky_is_not_judged(repo):
    (repo / "src/feature/a.py").write_text("x = 2\n")
    (repo / "tests/unit/test_new.py").write_text("def test_new(): pass\n")      # an untracked new file counts
    (repo / "README.md").write_text("doc\n")                                    # out of scope but has a reason
    p = check(repo, GOOD_NOW)
    out = json.loads(p.stdout)
    assert p.returncode == 0 and out["pass"], p.stdout
    assert out["flaky"] == ["t.acc::test_flip"]
    assert "tests/unit/test_new.py" in out["changed"]


@pytest.mark.parametrize("name,edit,current,check_name", [
    ("unit test fails", None, {**GOOD_NOW, "t.unit::test_new": "fail"}, "tests"),
    ("baseline test now fails", None, {**GOOD_NOW, "t.unit::test_old": "fail"}, "baseline"),
    ("baseline test deleted", None, {k: v for k, v in GOOD_NOW.items() if k != "t.acc::test_case1"}, "baseline"),
    ("file out of scope", "src/other.py", GOOD_NOW, "scope"),
    ("must-not-change touched", "src/billing/b.py", GOOD_NOW, "must-not"),
    ("verifier's case edited", "tests/acceptance/test_acc.py", GOOD_NOW, "tamper"),
])
def test_each_check_can_fail(repo, name, edit, current, check_name):
    if edit:
        (repo / edit).parent.mkdir(parents=True, exist_ok=True)
        (repo / edit).write_text("changed = True\n")
    p = check(repo, current)
    out = json.loads(p.stdout)
    assert p.returncode == 1 and not out["pass"], name
    assert out["checks"][check_name], (name, out["checks"])
    assert [k for k, v in out["checks"].items() if v] == [check_name], (name, out["checks"])


def test_staged_change_counts_and_bad_ref_is_usage_error(repo):
    (repo / "src/billing/b.py").write_text("y = 3\n")
    git(repo, "add", "src/billing/b.py")
    assert json.loads(check(repo, GOOD_NOW).stdout)["checks"]["must-not"] == ["src/billing/b.py"]
    t = repo.parent
    p = run("check", "--plan", t / "plan.json", "--base-ref", "no-such-ref", "--baseline", t / "base.json",
            "--junit", t / "now.xml", "--root", repo)
    assert p.returncode == 2 and "git diff" in p.stderr


def test_real_pytest_junit_is_read(tmp_path):
    (tmp_path / "test_x.py").write_text("def test_ok(): pass\ndef test_bad(): assert 0\n")
    subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={tmp_path}/r.xml",
                    str(tmp_path / "test_x.py")], capture_output=True)
    p = run("baseline", "--junit", tmp_path / "r.xml", "--out", tmp_path / "b.json")
    base = json.loads((tmp_path / "b.json").read_text())
    assert p.returncode == 0 and sorted(base.values()) == ["fail", "pass"]
