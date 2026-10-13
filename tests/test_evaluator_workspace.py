"""Tests for tools/evaluator/workspace.py, the step that copies the product into the blind workspace.

The fake product carries the four things EV-R2.1 names as outside the workspace — its tests, its run folders, its git
history and its caches — plus a symlink and a marker file planted in its tests. The module is imported by path
inside a helper, not at module level, because it does not exist yet: this file must collect today and every test
must fail on its own until the code lands.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools/evaluator/workspace.py"

MARKER_CONTENT = "EVALUATOR-MARKER-CONTENT-7f3a"
PRODUCT_FILES = {
    "README.md": "# Product\n",
    "src/app.py": "def run():\n    return 1\n",
    "src/__pycache__/app.cpython-311.pyc": "not really compiled\n",
    "tests/test_product.py": "def test_run():\n    assert True\n",
    "tests/MARKER.txt": f"{MARKER_CONTENT}\n",
    "runs/20260101-old/notes.md": "an earlier run\n",
    ".git/config": "[core]\n",
    "notes.log": "one\n",
}
SPEC_REQUIREMENTS = "**Z1 — A group** (d)\n- **Z1.1** It does one thing.\n- **Fails if** it does not.\n"
SPEC_VISION = "# Vision\n\n**What it will never do**\n- Never guesses.\n"


def load_workspace():
    """Import tools/evaluator/workspace.py by path, inside the test, so this file collects without it."""
    if not TOOL.is_file():
        pytest.fail(f"{TOOL} does not exist yet")
    spec = importlib.util.spec_from_file_location("evaluator_workspace", TOOL)
    module = importlib.util.module_from_spec(spec)
    sys.modules["evaluator_workspace"] = module
    spec.loader.exec_module(module)
    return module


def build_product(root):
    """A product with source, tests holding the marker, runs, .git, a __pycache__, a log file and a symlink."""
    product = root / "product"
    for name, content in PRODUCT_FILES.items():
        path = product / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    (product / "link.py").symlink_to("src/app.py")
    return product


def build_spec(root, requirements=True, vision=True):
    """A spec folder; VISION.md may be left out, which the run is allowed to go without."""
    spec = root / "spec"
    spec.mkdir(parents=True, exist_ok=True)
    if requirements:
        (spec / "REQUIREMENTS.md").write_text(SPEC_REQUIREMENTS, encoding="utf-8")
    if vision:
        (spec / "VISION.md").write_text(SPEC_VISION, encoding="utf-8")
    return spec


def sha256_of(path):
    """The file's own bytes, hashed."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    """Every path under root with its kind and hash, so a changed, added or removed file shows up."""
    seen = {}
    for directory, subdirectories, names in os.walk(root, followlinks=False):
        for name in subdirectories + names:
            path = Path(directory) / name
            relative = str(path.relative_to(root))
            if path.is_symlink():
                seen[relative] = ("link", os.readlink(path))
            elif path.is_file():
                seen[relative] = ("file", sha256_of(path))
            else:
                seen[relative] = ("directory", "")
    return seen


def build(module, root, excludes=None, **spec_files):
    """build_workspace over a fresh fake product and spec under root; returns the run folder and the manifest."""
    product = build_product(root)
    spec = build_spec(root, **spec_files)
    manifest = module.build_workspace(product, spec, root / "run", excludes=excludes)
    return root / "run", manifest


def test_a_marker_planted_in_the_product_tests_never_reaches_the_workspace(tmp_path):
    """EV-R2.1 — the builder's tests reaching a model step's input makes the check inherit the builder's blind spots."""
    module = load_workspace()
    run, manifest = build(module, tmp_path)
    copied = run / "workspace/product"
    assert not (copied / "tests").exists()
    assert not (copied / "runs").exists()
    assert not (copied / ".git").exists()
    assert not (copied / "src/__pycache__").exists()
    assert not (copied / "link.py").exists()
    assert "tests/MARKER.txt" not in manifest["copied"]
    for path in sorted((run / "workspace").rglob("*")):
        if path.is_file():
            assert MARKER_CONTENT not in path.read_text(encoding="utf-8", errors="replace"), path


def test_an_exclude_glob_replaces_the_default_tests_glob(tmp_path):
    """EV-R2.2 — an --exclude that only added to the default would go on hiding the product's tests forever."""
    module = load_workspace()
    run, manifest = build(module, tmp_path, excludes=["*.log"])
    copied = run / "workspace/product"
    assert (copied / "tests/MARKER.txt").is_file()
    assert (copied / "src/app.py").is_file()
    assert not (copied / "notes.log").exists()
    assert "notes.log" in manifest["excluded"]
    assert "tests/MARKER.txt" not in manifest["excluded"]


def test_the_product_and_spec_trees_are_unchanged_by_the_run(tmp_path):
    """EV-R3.2 — a run that changes the product measures something the product never had."""
    module = load_workspace()
    product = build_product(tmp_path)
    spec = build_spec(tmp_path)
    before = (snapshot(product), snapshot(spec))
    module.build_workspace(product, spec, tmp_path / "run", excludes=None)
    assert (snapshot(product), snapshot(spec)) == before
    assert (tmp_path / "run/workspace/product/src/app.py").read_bytes() == (product / "src/app.py").read_bytes()


def test_the_manifest_lists_what_was_copied_excluded_and_skipped(tmp_path):
    """EV-R2.1 — a manifest that does not say what was left out cannot show the workspace was blind."""
    module = load_workspace()
    product = build_product(tmp_path)
    spec = build_spec(tmp_path)
    manifest = module.build_workspace(product, spec, tmp_path / "run", excludes=None)
    assert set(manifest) == {"copied", "excluded", "skipped"}
    assert manifest["copied"] == {"README.md": sha256_of(product / "README.md"),
                                  "notes.log": sha256_of(product / "notes.log"),
                                  "src/app.py": sha256_of(product / "src/app.py")}
    assert {"tests/test_product.py", "tests/MARKER.txt"} <= set(manifest["excluded"])
    for relative in (".git/config", "runs/20260101-old/notes.md", "src/__pycache__/app.cpython-311.pyc"):
        assert relative not in manifest["copied"], relative
    assert "link.py" in manifest["skipped"]
    assert "link.py" not in manifest["copied"]
    copied_spec = tmp_path / "run/workspace/spec"
    assert (copied_spec / "REQUIREMENTS.md").read_bytes() == (spec / "REQUIREMENTS.md").read_bytes()
    assert (copied_spec / "VISION.md").read_bytes() == (spec / "VISION.md").read_bytes()


def test_a_missing_requirements_file_exits_two_with_a_problem_line(tmp_path, monkeypatch, capsys):
    """EV-R2.1 — a workspace with no requirements in it cannot judge anything, so the run stops with exit 2."""
    module = load_workspace()
    product = build_product(tmp_path)
    spec = build_spec(tmp_path, requirements=False)
    monkeypatch.setattr(sys, "argv", ["workspace.py", "--product", str(product), "--spec", str(spec),
                                      "--run", str(tmp_path / "run")])
    assert module.main() == 2
    err = capsys.readouterr().err
    assert "REQUIREMENTS.md" in err
    assert "Traceback" not in err