#!/usr/bin/env python3
"""probe_matrix.py — run the probes on the product copy and on every mutant, and write matrix.json (steps E6, E7).

Run:  python3 tools/evaluator/probe_matrix.py --run runs/<runId> [--timeout 600]

DATA.md's E6 and E7 section is the contract: each probe key is `<junit classname>::<junit name>`, each outcome is
pass, fail or skip, a mutant whose `old` text is not in its file exactly once is invalid and is not run, and
`restored` is true only when every file of the product copy hashes as it did before the product run (EV-C3.3, R1-F4).

The probes never see the builder's tree: they run against `<run>/workspace/product/`, one pytest call per mutant, with
`EVAL_PRODUCT` pointing at the copy. Nothing outside the run folder is read or written, and no bytecode is left in
the copy, so the final hash comparison means what it says (EV-R3.2).

Every pytest call also reports how it went, in the `runs` key (R1-F5): a run that timed out or left no report marks
every probe red, and on a mutant that red would read as proof, so the status and the keys that ended in a JUnit error
are recorded and `verdict.py` checks them before it calls a case proven.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import site
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ElementTree
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))  # loaded by path, with tools/evaluator/ off sys.path
from spec_parse import ID  # noqa: E402  R1-F3: one id grammar, not a copy of it; a case id is a group id plus -F<n>

DEFAULT_TIMEOUT = 600
CITATION = re.compile(r"[ \t]*(?:[,;][ \t]*)?(" + ID + r"-F[0-9]+)\b")
OK, TIMEOUT, NO_REPORT = "ok", "timeout", "no-report"


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


class Run:
    """One pytest call's answer: what each probe did, how the run itself went, and which probes ended in an error."""

    def __init__(self, results: dict[str, str], status: str = OK, errors: list[str] | None = None):
        self.results = results
        self.status = status
        self.errors = list(errors or [])

    def recorded(self) -> dict:
        """The run's entry in matrix.json's `runs` key."""
        return {"status": self.status, "errors": list(self.errors)}


def _run_probes(product: Path, probes: Path, plan: dict[str, list[str]], timeout: int) -> Run:
    """One pytest call over every probe. A timeout or a missing report leaves every probe red, never green."""
    # Absolute paths: pytest runs with the run folder as its cwd, so a relative --run would point it at nothing
    # and every probe would come back red (calibration K1, 2026-10-13).
    product, probes = product.resolve(), probes.resolve()
    environment = dict(os.environ)
    environment["EVAL_PRODUCT"] = str(product)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"  # a stale .pyc in the copy would make `restored` a lie
    with tempfile.TemporaryDirectory(prefix="probe-matrix-") as scratch:
        # R1-F9: model-written probes run with HOME and TMPDIR in a scratch folder, so they do not write into the
        # user's home or shared temp. Reads elsewhere are NOT prevented: narrowed, not enforced (DATA.md, R1-F9).
        home = Path(scratch) / "home"
        home.mkdir()
        # Keep the real user site-packages: pytest may live in ~/.local, and moving HOME alone would hide it, so
        # every probe would come back red with no report (found by the COO's regression test, 2026-10-13).
        environment.setdefault("PYTHONUSERBASE", site.getuserbase())
        environment["HOME"] = environment["TMPDIR"] = str(home)
        report_file = Path(scratch) / "junit.xml"
        command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-c", "/dev/null",
                   "--rootdir", str(probes), "--junitxml", str(report_file), str(probes)]
        try:
            subprocess.run(command, cwd=str(probes.parent), env=environment,
                           capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return Run({key: "fail" for key in plan}, TIMEOUT)
        except OSError as error:
            raise InputError(f"{error.filename or 'python3 -m pytest'}: {error.strerror or error}") from None
        return _read_report(report_file, plan)  # inside the scratch folder: it is gone once `with` ends


LAST_OUTPUT: dict[str, str] = {}  # each failing probe's message from the latest report, for E8 (DATA.md)


def _read_report(report_file: Path, plan: dict[str, list[str]]) -> Run:
    """Every outcome under its JUnit key, with the keys that ended in an error rather than a failure."""
    try:
        root = ElementTree.parse(report_file).getroot()
    except (OSError, ElementTree.ParseError):
        return Run({key: "fail" for key in plan}, NO_REPORT)  # no invented errors: nothing was reported
    results, errors = {}, []
    for case in root.iter("testcase"):
        key = f"{case.get('classname') or ''}::{case.get('name') or ''}"
        outcome = "pass"
        if case.find("failure") is not None or case.find("error") is not None:
            outcome = "fail"  # an error counts as fail (DATA.md E6)
            problem = case.find("failure") if case.find("failure") is not None else case.find("error")
            LAST_OUTPUT[key] = f"{problem.get('message') or ''}\n{problem.text or ''}".strip()
            if case.find("error") is not None:
                errors.append(key)  # the probe died on the way: it never reached its check (R1-F5)
        elif case.find("skipped") is not None:
            outcome = "skip"
        results[key] = outcome
    return Run(results or {key: "fail" for key in plan}, OK, errors)


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

    LAST_OUTPUT.clear()
    original = _bytes(product)  # R1-F4: the baseline is taken before the product run, not after it
    before = {relative: hashlib.sha256(data).hexdigest() for relative, data in original.items()}
    product_run = _run_probes(product, probes, plan, timeout)
    product_output = dict(LAST_OUTPUT)  # only the product run's messages are kept; E8 confirms those
    product_changed = _hashes(product) != before  # a green probe may still have written to the copy
    _restore(product, original)  # the product run's own damage is undone before any mutant is measured

    results, runs = {}, {"product": product_run.recorded()}
    for mutant in mutants:
        case = str(mutant.get("case", ""))
        if _apply(product, mutant):
            outcome = _run_probes(product, probes, plan, timeout)
            results[case] = {"status": "applied", "results": outcome.results}
            runs[case] = outcome.recorded()
        else:
            results[case] = {"status": "invalid"}
        _restore(product, original)

    matrix = {"product_dir": "workspace/product", "probes_dir": "probes",
              "citations": {key: _citations_for(key, plan) for key in product_run.results},
              "product": product_run.results,
              "mutants": results,
              "restored": _hashes(product) == before}
    # R1-F5: `runs` is optional and written only when some run was not plainly healthy (a timeout, no report, or a
    # JUnit error), so a healthy matrix keeps its pre-R1 shape; verdict.py reads an absent key as healthy (COO).
    if any(run.get("status") != "ok" or run.get("errors") for run in runs.values()):
        matrix["runs"] = runs
    output = {key: text for key, text in product_output.items() if product_run.results.get(key) == "fail"}
    if output:  # optional in DATA.md: only failing probes have a message, and E8 needs it
        matrix["output"] = output
    if product_changed:
        matrix["product_changed"] = True  # recorded only when true: no key means the product run changed nothing
    return matrix


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