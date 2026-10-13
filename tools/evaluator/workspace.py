#!/usr/bin/env python3
"""workspace.py — copy the product and spec into the blind workspace (step E2).

Run:  python3 tools/evaluator/workspace.py --product DIR --spec DIR --run DIR [--exclude GLOB]...

The manifest records product-relative paths and hashes. Symlinks are skipped,
and the source trees are only read (EV-R2, EV-R3.2).
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

EXCLUDED_SEGMENTS = {"tests", "test", ".git", "runs", "__pycache__"}
STALE_OUTPUTS = ("classify.json", "probes", "mutants.json", "plants.json", "matrix.json",
                 "confirm.json", "judge-1.json", "judge-2.json", "verdict.json")


def _excluded(relative: Path, patterns: list[str]) -> bool:
    """Match a path or one of its parent directories against the product globs."""
    if any(part in EXCLUDED_SEGMENTS for part in relative.parts):
        return True
    if (relative.name == "conftest.py" or fnmatch.fnmatchcase(relative.name, "test_*.py")
            or fnmatch.fnmatchcase(relative.name, "*_test.py")):
        return True
    candidates = [relative, *relative.parents]
    return any(fnmatch.fnmatchcase(path.as_posix(), pattern.rstrip("/"))
               for path in candidates if path != Path(".") for pattern in patterns)


def _reset_directory(path: Path) -> None:
    """Remove stale output before copying a new blind workspace."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def build_workspace(product: Path, spec: Path, run: Path,
                    excludes: list[str] | None) -> dict:
    """Copy the allowed product files and spec, write and return manifest.json."""
    product, spec, run = Path(product), Path(spec), Path(run)
    if any((run / name).exists() or (run / name).is_symlink() for name in STALE_OUTPUTS):
        raise OSError(22, "use a new runId", str(run))
    if not product.is_dir():
        raise OSError(2, "not a product directory", str(product))
    # Read mandatory inputs before changing any previous output.
    spec_bytes = {"REQUIREMENTS.md": (spec / "REQUIREMENTS.md").read_bytes()}
    try:
        spec_bytes["VISION.md"] = (spec / "VISION.md").read_bytes()
    except FileNotFoundError:
        pass

    workspace = run / "workspace"
    for destination in (workspace / "product", workspace / "spec"):
        for source in (product, spec):
            if source.resolve().is_relative_to(destination.resolve()):
                raise OSError(22, "workspace output overlaps an input", str(destination))
    if workspace.is_symlink():
        raise OSError(22, "workspace must not be a symlink", str(workspace))
    _reset_directory(workspace / "product")
    _reset_directory(workspace / "spec")

    patterns = excludes or []
    manifest = {"copied": {}, "excluded": [], "skipped": []}

    def walk_error(error: OSError) -> None:
        raise error

    for directory, subdirectories, names in os.walk(product, followlinks=False, onerror=walk_error):
        subdirectories.sort()
        names.sort()
        for name in subdirectories[:]:
            source = Path(directory) / name
            relative = source.relative_to(product)
            if source.is_symlink():
                manifest["skipped"].append(relative.as_posix())
                subdirectories.remove(name)
            elif name in {".git", "runs", "__pycache__"}:
                manifest["excluded"].append(relative.as_posix())
                subdirectories.remove(name)
            elif not _excluded(relative, patterns):
                (workspace / "product" / relative).mkdir(parents=True, exist_ok=True)
        for name in names:
            source = Path(directory) / name
            relative = source.relative_to(product)
            key = relative.as_posix()
            if source.is_symlink():
                manifest["skipped"].append(key)
            elif _excluded(relative, patterns):
                manifest["excluded"].append(key)
            else:
                content = source.read_bytes()
                destination = workspace / "product" / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(content)
                shutil.copymode(source, destination)
                manifest["copied"][key] = hashlib.sha256(content).hexdigest()
    manifest["copied"] = dict(sorted(manifest["copied"].items()))
    manifest["excluded"].sort()
    manifest["skipped"].sort()
    for name, content in spec_bytes.items():
        (workspace / "spec" / name).write_bytes(content)
    (workspace / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    """Build the workspace; report path errors on stderr with exit code 2."""
    parser = argparse.ArgumentParser(description="Build a blind product workspace.")
    parser.add_argument("--product", required=True, type=Path)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--exclude", action="append")
    args = parser.parse_args(argv)
    try:
        requirements = args.spec / "REQUIREMENTS.md"
        if not requirements.is_file():
            raise OSError(2, "not a requirements file", str(requirements))
        runs = Path(__file__).resolve().parents[2] / "runs"
        if args.run.resolve() == runs.resolve() or not args.run.resolve().is_relative_to(runs.resolve()):
            raise OSError(22, "run must resolve inside the repository's runs/ folder", str(args.run))
        manifest = build_workspace(args.product, args.spec, args.run, args.exclude)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"{args.run}: {error}", file=sys.stderr)
        return 2
    print(f"wrote {args.run / 'workspace/manifest.json'}: {len(manifest['copied'])} files copied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
