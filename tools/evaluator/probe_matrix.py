#!/usr/bin/env python3
"""probe_matrix.py — run the probes on the product copy and on every mutant, and write matrix.json (steps E6, E7).

Run:  python3 tools/evaluator/probe_matrix.py --run runs/<runId> [--timeout 600]

DATA.md's E6 and E7 section is the contract: each probe key is `<junit classname>::<junit name>`, each outcome is
pass, fail or skip, a mutant whose `old` text is not in its file exactly once is invalid and is not run, and
`restored` is true only when every file of the product copy hashes as it did before the first mutant (EV-C3.3).

The probes never see the builder's tree: they run against `<run>/workspace/product/`, one pytest call per mutant, with
`EVAL_PRODUCT` pointing at the copy. Nothing outside the run folder is read or written, and no bytecode is left in
the copy, so the final hash comparison means what it says (EV-R3.2).
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ElementTree
from pathlib import Path

DEFAULT_TIMEOUT = 600
CITATION = re.compile(r"[ \t]*(?:[,;][ \t]*)?([A-Za-z][A-Za-z0-9.]*-F[0-9]+)\b")


class InputError(Exception):
    """A path the run needs cannot be read. The message is the line the user gets on stderr."""


def report(text: str) -> None:
    """Print a problem to stderr. stdout is flushed first, so a piped run reads in order."""
    sys.stdout.flush()
    print(text, file=sys.stderr)


# --- the probes as written -------------------------------------------------------------------


def _citations(docstring: str) -> list[str]:
    """The case ids a probe's docstring starts with: `B1-F1 — …`, or several before the dash (DATA.md E6)."""
    found, position = [], 0
    while (match := CITATION.match(docstring, position)) is not None:
        found.append(match.group(1))
        position = match.end()
    return found


def _probe_plan(probes: Path) -> dict[str, list[str]]:
    """Every module-level test function in `<probes_dir>/test_*.py`, keyed `module::name`, with its citations."""
    plan = {}
    for path in sorted(probes.glob("test_*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError) as error:
            raise InputError(f"{path}: {error}") from None
        except SyntaxError as error:
            raise InputError(f"{path}: {error.msg} at line {error.lineno}") from None
        for node in tree.body:  # module level, as DATA.md's E6 says the probe writer writes them
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
                plan[f"{path.stem}::{node.name}"] = _citations(ast.get_docstring(node) or "")
    return plan


def _citations_for(key: str, plan: dict[str, list[str]]) -> list[str]:
    """A parametrised key such as `test_b1::test_pairs[positive]` carries its function's citations."""
    module, _, name = key.partition("::")
    return plan.get(f"{module}::{name.split('[')[0]}", [])


# --- one pytest run ---------------------------------------------------------------------------


def _run_probes(product: Path, probes: Path, plan: dict[str, list[str]], timeout: int) -> dict[str, str]:
    """One pytest call over every probe. A timeout or a missing report leaves every probe red, never green."""
    environment = dict(os.environ)
    environment["EVAL_PRODUCT"] = str(product)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"  # a stale .pyc in the copy would make `restored` a lie
    with tempfile.TemporaryDirectory(prefix="probe-matrix-") as scratch:
        report_file = Path(scratch) / "junit.xml"
        command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-c", "/dev/null",
                   "--rootdir", str(probes), "--junitxml", str(report_file), str(probes)]
        try:
            subprocess.run(command, cwd=str(probes.parent), env=environment,
                           capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {key: "fail" for key in plan}
        except OSError as error:
            raise InputError(f"{error.filename or 'python3 -m pytest'}: {error.strerror or error}") from None
        return _read_report(report_file, plan)  # inside the scratch folder: it is gone once `with` ends


def _read_report(report_file: Path, plan: dict[str, list[str]]) -> dict[str, str]:
    """Every outcome under its JUnit key, or every probe red when the run left no report behind."""
    try:
        root = ElementTree.parse(report_file).getroot()
    except (OSError, ElementTree.ParseError):
        return {key: "fail" for key in plan}
    results = {}
    for case in root.iter("testcase"):
        outcome = "pass"
        if case.find("failure") is not None or case.find("error") is not None:
            outcome = "fail"  # an error counts as fail (DATA.md E6)
        elif case.find("skipped") is not None:
            outcome = "skip"
        results[f"{case.get('classname') or ''}::{case.get('name') or ''}"] = outcome
    return results or {key: "fail" for key in plan}


# --- the product copy -------------------------------------------------------------------------


def _apply(product: Path, mutant: dict) -> bool:
    """Write a mutant's replacement into the copy, or return False when it is invalid (DATA.md E6 and E7)."""
    target = product / str(mutant.get("file", ""))
    if not target.is_file() or product.resolve() not in target.resolve().parents:
        return False  # the copy holds no such file, or the path reaches outside it
    try:
        text = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False  # bytes a replacement cannot be found in are not a file this step can break
    old = mutant.get("old")
    if not isinstance(old, str) or not old or text.count(old) != 1:
        return False
    target.write_text(text.replace(old, str(mutant.get("new", "")), 1), encoding="utf-8")
    return True


def _hashes(folder: Path) -> dict[str, str]:
    """The sha256 of every file under the copy, hidden and nested ones included (EV-C3.3)."""
    hashes = {}
    for path in sorted(folder.rglob("*")):
        if path.is_file():
            hashes[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def _restore(folder: Path, original: dict[str, bytes]) -> None:
    """Put every file of the copy back to the bytes it held before the first mutant."""
    for relative, data in original.items():
        target = folder / relative
        if not target.is_file() or target.read_bytes() != data:
            target.write_bytes(data)
    for path in sorted(folder.rglob("*"), reverse=True):
        if path.is_file() and path.relative_to(folder).as_posix() not in original:
            path.unlink()


def _bytes(folder: Path) -> dict[str, bytes]:
    """Every file under the copy, as bytes, so a restore is exact and not a reconstruction."""
    return {path.relative_to(folder).as_posix(): path.read_bytes()
            for path in sorted(folder.rglob("*")) if path.is_file()}


def _mutants(run: Path) -> list[dict]:
    """E5's list, or none when the file is missing (DATA.md E6)."""
    path = run / "mutants.json"
    if not path.exists():
        return []
    try:
        mutants = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InputError(f"{path}: {error}") from None
    if not isinstance(mutants, list):
        raise InputError(f"{path}: a list of mutants, not {type(mutants).__name__}")
    for number, mutant in enumerate(mutants, start=1):
        if not isinstance(mutant, dict):
            raise InputError(f"{path}: mutant {number} is {type(mutant).__name__}, not an object")
    return mutants


# --- the matrix --------------------------------------------------------------------------------


def build_matrix(run: Path, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Run the probes on the product copy and on every mutant, and return matrix.json's content."""
    run = Path(run)
    product = run / "workspace/product"
    probes = run / "probes"
    for folder, what in ((product, "the product copy"), (probes, "the probes")):
        if not folder.is_dir():
            raise InputError(f"{folder}: {what} is missing")
    plan = _probe_plan(probes)
    mutants = _mutants(run)

    product_results = _run_probes(product, probes, plan, timeout)
    original = _bytes(product)  # the bytes every mutant is measured against
    before = {relative: hashlib.sha256(data).hexdigest() for relative, data in original.items()}

    results = {}
    for mutant in mutants:
        case = str(mutant.get("case", ""))
        if _apply(product, mutant):
            outcomes = _run_probes(product, probes, plan, timeout)
            results[case] = {"status": "applied", "results": outcomes}
        else:
            results[case] = {"status": "invalid"}
        _restore(product, original)

    return {"product_dir": "workspace/product", "probes_dir": "probes",
            "citations": {key: _citations_for(key, plan) for key in product_results},
            "product": product_results,
            "mutants": results,
            "restored": _hashes(product) == before}


def _write_matrix(run: Path, matrix: dict) -> None:
    """Write matrix.json as UTF-8, the shape DATA.md's E6 example gives."""
    path = run / "matrix.json"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(matrix, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError as error:
        raise InputError(f"{path}: {error.strerror or error}") from None


def main(argv: list[str] | None = None) -> int:
    """Run the matrix for one evaluation folder. 0 when it wrote matrix.json, 2 on an input it cannot read."""
    parser = argparse.ArgumentParser(
        description="Run the probes on the product copy and on every mutant, and write matrix.json.",
    )
    parser.add_argument("--run", required=True, help="the evaluation folder, holding workspace/ and probes/")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"seconds each pytest run may take (default {DEFAULT_TIMEOUT})")
    args = parser.parse_args(argv)
    try:
        matrix = build_matrix(Path(args.run), timeout=args.timeout)
        _write_matrix(Path(args.run), matrix)
    except InputError as error:
        report(str(error))
        return 2
    except OSError as error:  # e.g. the run folder is read-only: a problem, not a crash
        report(f"{error.filename or 'probe_matrix.py'}: {error.strerror or error}")
        return 2
    print(f"wrote {args.run}/matrix.json: {len(matrix['product'])} probes, "
          f"{len(matrix['mutants'])} mutants, restored: {matrix['restored']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())