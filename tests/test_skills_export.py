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

    # every `references/<file>` a bundled SKILL.md names is in the bundle — in its own folder, or in the bundled
    # skill it points at (bootstrap names workflow-design's) (run 20261016-integrate-r11-r13 review)
    import re
    for skill in skills.glob("*/SKILL.md"):
        for ref in re.findall(r"`(references/[^`\s]+\.md)`", skill.read_text()):
            assert (skill.parent / ref).is_file() or any(skills.glob(f"*/{ref}")), \
                f"{skill.parent.name}: {ref} named but not exported"


def export_drift(repo, rev="HEAD"):
    """The skills/ paths where `rev`'s committed export differs from a fresh export of `rev`'s own sources. Reads the
    commit through `git archive` into a temp folder; the repository's working tree is never read or written."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tree, committed = Path(td) / "tree", Path(td) / "committed"
        tree.mkdir()
        archive = subprocess.run(["git", "archive", "--format=tar", rev], cwd=repo, capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(tree)], input=archive.stdout, check=True)
        if (tree / "skills").is_dir():
            shutil.copytree(tree / "skills", committed)
        else:
            committed.mkdir()
        subprocess.run([sys.executable, str(tree / "tools" / "export_skills.py")], cwd=tree, check=True,
                       capture_output=True)

        def files(root):
            return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}

        old, new = files(committed), files(tree / "skills")
        return sorted(f"skills/{name}" for name in old.keys() | new.keys() if old.get(name) != new.get(name))


def test_skills_export_is_current():
    """The committed skills/ matches a fresh export of the same commit's sources — drift is caught, not hand-synced.
    It reads HEAD only, so it passes before a commit as after one (F-d8221199): the pre-commit hook makes each commit
    carry its export, and this catches a commit made without the hook (a fresh clone, a web session)."""
    assert export_drift(REPO) == []


# F-d8221199 (the pick, 2026-10-17): the check reads one commit, never the working tree, so a run before a commit
# passes as one after it does. Each test below clones this repository and plants the situation in the clone.
SOURCE = ".claude/skills/workflow-design/guard/SPEC.md"
EXPORTED = "skills/workflow-design/guard/SPEC.md"


def clone_of(tmp_path):
    target = tmp_path / "clone"
    subprocess.run(["git", "clone", "--quiet", "--shared", str(REPO), str(target)], check=True)
    for key, value in (("user.email", "test@example.invalid"), ("user.name", "export test")):
        subprocess.run(["git", "config", key, value], cwd=target, check=True)
    return target


def change_source(clone):
    with open(clone / SOURCE, "a", encoding="utf-8") as f:
        f.write("\nEXPORT-TEST-LINE\n")


def test_an_uncommitted_source_change_passes_it(tmp_path):
    # F-d8221199's situation: a skill source changed, the commit (and its hook) not made yet.
    clone = clone_of(tmp_path)
    change_source(clone)
    assert export_drift(clone) == []


def test_a_commit_without_its_export_fails_it(tmp_path):
    # A commit made where the pre-commit hook is not installed: the source moved on, skills/ did not.
    clone = clone_of(tmp_path)
    change_source(clone)
    subprocess.run(["git", "commit", "-q", "--no-verify", "-am", "source only"], cwd=clone, check=True)
    assert export_drift(clone) == [EXPORTED]


def test_it_never_writes_to_the_working_tree(tmp_path):
    clone = clone_of(tmp_path)
    change_source(clone)
    export_drift(clone)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=clone, capture_output=True, text=True, check=True)
    assert status.stdout.splitlines() == [f" M {SOURCE}"]
