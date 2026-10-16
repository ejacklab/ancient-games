"""tools/git-hooks/pre-commit: a commit that changes what skills/ is built from carries the fresh export, built from
the index (never from unstaged edits), and leaves the working tree's skills/ matching (EJ's pick, 2026-10-17; insight
F-5182be9b, F-1d185ee3).

Each test clones this repo, installs the working tree's hook in the clone and commits there."""
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
HOOK = REPO / "tools" / "git-hooks" / "pre-commit"
SPEC = ".claude/skills/workflow-design/guard/SPEC.md"
OTHER = ".claude/skills/requirement-check/SKILL.md"


def git(clone, *args, check=True):
    return subprocess.run(["git", *args], cwd=clone, capture_output=True, text=True, check=check)


@pytest.fixture
def clone(tmp_path):
    target = tmp_path / "clone"
    subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(REPO), str(target)], check=True)
    git(target, "config", "user.email", "test@example.invalid")
    git(target, "config", "user.name", "hook test")
    shutil.copy(HOOK, target / ".git" / "hooks" / "pre-commit")
    return target


def append(clone, rel, line):
    with open(clone / rel, "a", encoding="utf-8") as f:
        f.write(f"\n{line}\n")


def committed(clone):
    return git(clone, "show", "--name-only", "--format=", "HEAD").stdout.split()


def test_a_skill_source_change_commits_its_export(clone):
    append(clone, SPEC, "HOOK-TEST-LINE")
    git(clone, "add", SPEC)
    git(clone, "commit", "-q", "-m", "source only")
    assert "skills/workflow-design/guard/SPEC.md" in committed(clone)
    assert "HOOK-TEST-LINE" in git(clone, "show", "HEAD:skills/workflow-design/guard/SPEC.md").stdout
    assert git(clone, "status", "--porcelain", "--", "skills/").stdout == ""


def test_the_export_is_built_from_the_index_not_unstaged_edits(clone):
    append(clone, OTHER, "UNSTAGED-EDIT")
    append(clone, SPEC, "STAGED-EDIT")
    git(clone, "add", SPEC)
    git(clone, "commit", "-q", "-m", "one staged source")
    assert "UNSTAGED-EDIT" not in git(clone, "show", "HEAD:skills/requirement-check/SKILL.md").stdout
    assert "skills/requirement-check/SKILL.md" not in committed(clone)
    assert "UNSTAGED-EDIT" in (clone / OTHER).read_text(encoding="utf-8")  # the unstaged source is left alone


def test_a_commit_that_touches_no_skill_source_is_not_changed(clone):
    append(clone, OTHER, "UNSTAGED-EDIT")
    (clone / "notes.txt").write_text("x\n", encoding="utf-8")
    git(clone, "add", "notes.txt")
    git(clone, "commit", "-q", "-m", "unrelated")
    assert committed(clone) == ["notes.txt"]


def test_a_removed_source_file_is_removed_from_the_export(clone):
    rel = ".claude/skills/workflow-design/guard/test/round12-expect-fail.test.ts"
    git(clone, "rm", "-q", rel)
    git(clone, "commit", "-q", "-m", "remove a test")
    assert "skills/workflow-design/guard/test/round12-expect-fail.test.ts" in committed(clone)
    assert not (clone / "skills/workflow-design/guard/test/round12-expect-fail.test.ts").exists()
    assert git(clone, "status", "--porcelain", "--", "skills/").stdout == ""


def test_a_failing_export_stops_the_commit(clone):
    head = git(clone, "rev-parse", "HEAD").stdout
    script = clone / "tools" / "export_skills.py"
    script.write_text("raise SystemExit(3)\n" + script.read_text(encoding="utf-8"), encoding="utf-8")
    git(clone, "add", "tools/export_skills.py")
    result = git(clone, "commit", "-q", "-m", "broken export", check=False)
    assert result.returncode != 0
    assert "export_skills.py failed" in result.stderr
    assert git(clone, "rev-parse", "HEAD").stdout == head
