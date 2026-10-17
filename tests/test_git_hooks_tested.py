"""Every git hook in tools/git-hooks/ is tested by a real commit in a clone, never by calling the script directly
(F-749688a0 option 2, chosen 2026-10-17). A direct call has no hook environment: inside a hook git passes
GIT_INDEX_FILE relative to the working tree, so the pre-commit hook's first version would have passed a direct call
and failed in every real commit.

A hook is tested when a tests/test_*.py names it (tools/git-hooks/<name>), clones the repository, puts the hook in the
clone's .git/hooks, and runs the git command that fires it. The check reads the test files' text; it does not run
them.

Observable (R12.6): this check reports a hook, or a hook fails in a real commit while its tests pass."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# The git command that fires each hook. A hook not listed here is reported until its command is added.
TRIGGER = {"pre-commit": "commit"}


def untested_hooks(root):
    """(hook, reason) for each hook in root/tools/git-hooks/ that no test commits through in a clone."""
    hooks_dir = root / "tools" / "git-hooks"
    if not hooks_dir.is_dir():
        return []
    tests = [(test, test.read_text(encoding="utf-8")) for test in sorted((root / "tests").glob("test_*.py"))]
    found = []
    for hook in sorted(p.name for p in hooks_dir.iterdir() if p.is_file()):
        trigger = TRIGGER.get(hook)
        if trigger is None:
            found.append((hook, f"no known git command fires it: add it to TRIGGER in {Path(__file__).name}"))
            continue
        names = re.compile(r"git-hooks[\"']?\s*[/,]\s*[\"']?" + re.escape(hook) + r"\b")
        naming = [text for _, text in tests if names.search(text)]
        if not naming:
            found.append((hook, "no test names it"))
            continue
        if not any(re.search(r"[\"']clone[\"']", text)
                   and re.search(r"\.git[\"']?\s*/\s*[\"']?hooks", text)
                   and re.search(r"[\"']" + trigger + r"[\"']", text) for text in naming):
            found.append((hook, f"its tests never install it in a clone's .git/hooks and run git {trigger}"))
    return found


def test_every_git_hook_in_the_repo_is_tested_by_a_commit_in_a_clone():
    assert untested_hooks(REPO) == []


def layout(tmp_path, test_text, hook="pre-commit"):
    (tmp_path / "tools" / "git-hooks").mkdir(parents=True)
    (tmp_path / "tools" / "git-hooks" / hook).write_text("#!/bin/sh\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_hook.py").write_text(test_text, encoding="utf-8")
    return tmp_path


def test_a_hook_tested_only_by_a_direct_call_is_reported(tmp_path):
    # The planted repeat of F-749688a0: the hook run as a script, outside any commit.
    root = layout(tmp_path, 'HOOK = REPO / "tools" / "git-hooks" / "pre-commit"\n'
                            'def test_hook():\n    subprocess.run([str(HOOK)], check=True)\n')
    assert untested_hooks(root) == [("pre-commit", "its tests never install it in a clone's .git/hooks and run git commit")]


def test_a_hook_run_directly_inside_a_clone_is_reported(tmp_path):
    # Cloned and installed, but run as a script: still no hook environment.
    root = layout(tmp_path, 'HOOK = REPO / "tools" / "git-hooks" / "pre-commit"\n'
                            'def test_hook(tmp_path):\n    subprocess.run(["git", "clone", str(REPO), str(tmp_path)])\n'
                            '    shutil.copy(HOOK, tmp_path / ".git" / "hooks" / "pre-commit")\n'
                            '    subprocess.run([str(tmp_path / ".git" / "hooks" / "pre-commit")], check=True)\n')
    assert [hook for hook, _ in untested_hooks(root)] == ["pre-commit"]


def test_a_clone_that_commits_without_installing_the_hook_is_reported(tmp_path):
    root = layout(tmp_path, 'HOOK = REPO / "tools" / "git-hooks" / "pre-commit"\n'
                            'def test_hook(tmp_path):\n    subprocess.run(["git", "clone", str(REPO), str(tmp_path)])\n'
                            '    subprocess.run(["git", "commit", "-m", "x"], cwd=tmp_path)\n')
    assert [hook for hook, _ in untested_hooks(root)] == ["pre-commit"]


def test_a_hook_installed_and_committed_outside_a_clone_is_reported(tmp_path):
    # The real repository's own hooks folder: a commit there is not a test.
    root = layout(tmp_path, 'HOOK = REPO / "tools" / "git-hooks" / "pre-commit"\n'
                            'def test_hook():\n    shutil.copy(HOOK, REPO / ".git" / "hooks" / "pre-commit")\n'
                            '    subprocess.run(["git", "commit", "-m", "x"], cwd=REPO)\n')
    assert [hook for hook, _ in untested_hooks(root)] == ["pre-commit"]


def test_a_hook_no_test_names_is_reported(tmp_path):
    root = layout(tmp_path, "def test_other():\n    pass\n")
    assert untested_hooks(root) == [("pre-commit", "no test names it")]


def test_a_hook_with_no_known_trigger_is_reported(tmp_path):
    root = layout(tmp_path, "", hook="post-merge")
    assert untested_hooks(root) == [("post-merge", "no known git command fires it: add it to TRIGGER in test_git_hooks_tested.py")]


def test_the_real_clone_and_commit_test_counts(tmp_path):
    text = (REPO / "tests" / "test_pre_commit_hook.py").read_text(encoding="utf-8")
    assert untested_hooks(layout(tmp_path, text)) == []
