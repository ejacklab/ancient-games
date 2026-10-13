"""Contract tests for the evaluator's probe matrix, written before its implementation.

Import the tool inside a helper so this file collects when tools/evaluator/ is absent.
Every evaluation workspace and probe is built by hand under tmp_path.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest


TOOL = Path(__file__).resolve().parents[1] / "tools/evaluator/probe_matrix.py"
CALC = "def add(a, b):\n    return a + b\n"
PROBE_IMPORTS = """\
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.environ["EVAL_PRODUCT"])
import calc

"""
ADD_PROBE = '''\
def test_add():
    """X1-F1 — addition gives the sum."""
    assert calc.add(2, 3) == 5
'''


def load_tool():
    """Import the absent-until-implementation tool by path, as in the house style."""
    assert TOOL.is_file(), f"implementation is missing: {TOOL}"
    spec = importlib.util.spec_from_file_location("evaluator_probe_matrix", TOOL)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(autouse=True)
def isolate_pytest_environment(monkeypatch):
    """Keep host pytest options, plugins and bytecode writes out of temporary runs."""
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)
    monkeypatch.delenv("PYTEST_PLUGINS", raising=False)
    monkeypatch.delenv("PYTHONPATH", raising=False)
    monkeypatch.delenv("EVAL_PRODUCT", raising=False)
    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")


@pytest.fixture
def evaluation_run(tmp_path):
    """Build an evaluation's inputs without using workspace.py or any other tool."""
    run = tmp_path / "evaluation run"
    product = run / "workspace/product"
    product.mkdir(parents=True)
    (product / "calc.py").write_text(CALC, encoding="utf-8")
    (run / "probes").mkdir()
    write_probes(run, ADD_PROBE)
    return run


def write_probes(run, functions, filename="test_calc.py"):
    """Write real pytest probes that import the copy through EVAL_PRODUCT."""
    (run / "probes" / filename).write_text(
        PROBE_IMPORTS + textwrap.dedent(functions), encoding="utf-8"
    )


def write_mutants(run, mutants):
    """Write the E5 list without calling another evaluator module."""
    (run / "mutants.json").write_text(json.dumps(mutants), encoding="utf-8")


def add_mutant(case, replacement):
    """Describe one exact-once replacement in the calculator."""
    return {"case": case, "file": "calc.py", "old": "return a + b", "new": replacement}


def build_matrix(run):
    """Exercise the public function, with a finite timer for each real pytest run."""
    matrix = load_tool().build_matrix(run, timeout=10)
    assert isinstance(matrix, dict)
    assert matrix["product_dir"] == "workspace/product"
    assert matrix["probes_dir"] == "probes"
    assert isinstance(matrix["restored"], bool)
    return matrix


def run_cli(run, *arguments):
    """Run the actual CLI from the temporary directory, with an outer watchdog."""
    assert TOOL.is_file(), f"implementation is missing: {TOOL}"
    return subprocess.run(
        [sys.executable, str(TOOL), "--run", str(run), *arguments],
        cwd=run.parent, env=os.environ.copy(), capture_output=True, text=True, timeout=20,
    )


def file_bytes(folder):
    """Snapshot all files, including hidden, nested and binary files."""
    return {path.relative_to(folder).as_posix(): path.read_bytes()
            for path in folder.rglob("*") if path.is_file()}


def test_product_results_use_junit_keys(evaluation_run):
    """DATA.md E6 and E7 — every real probe records pass, fail or skip by its JUnit key."""
    write_probes(evaluation_run, '''\
        def test_copy_path():
            """X1-F1 — calc is imported from the product copy."""
            assert Path(calc.__file__).parent.resolve() == Path(os.environ["EVAL_PRODUCT"]).resolve()
            assert calc.add(2, 3) == 5

        def test_red():
            """X1-F2 — a failing assertion is red."""
            assert calc.add(2, 3) == 999

        @pytest.mark.skip(reason="deliberate contract fixture")
        def test_skipped():
            """X1-F3 — a skipped probe stays skipped."""
            assert False
    ''')
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {
        "test_calc::test_copy_path": "pass",
        "test_calc::test_red": "fail",
        "test_calc::test_skipped": "skip",
    }
    assert matrix["citations"] == {
        "test_calc::test_copy_path": ["X1-F1"],
        "test_calc::test_red": ["X1-F2"],
        "test_calc::test_skipped": ["X1-F3"],
    }
    assert matrix["mutants"] == {}  # Missing mutants.json means no mutants.
    assert matrix["restored"] is True


def test_all_probes_run_against_every_mutant(evaluation_run):
    """EV-C3.2 — both probes run on both mutants, including another case's mutant."""
    write_probes(evaluation_run, '''\
        def test_positive():
            """X1-F1 — positive sums remain positive."""
            assert calc.add(2, 3) == 5

        def test_negative():
            """X2-F1 — negative sums remain negative."""
            assert calc.add(-2, -3) == -5
    ''')
    write_mutants(evaluation_run, [
        add_mutant("X1-F1", "return -abs(a + b)"),
        add_mutant("X2-F1", "return abs(a + b)"),
    ])
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {
        "test_calc::test_positive": "pass", "test_calc::test_negative": "pass",
    }
    assert matrix["mutants"] == {
        "X1-F1": {"status": "applied", "results": {
            "test_calc::test_positive": "fail", "test_calc::test_negative": "pass",
        }},
        "X2-F1": {"status": "applied", "results": {
            "test_calc::test_positive": "pass", "test_calc::test_negative": "fail",
        }},
    }


@pytest.mark.parametrize("occurrences", [0, 2], ids=["absent", "ambiguous"])
def test_invalid_mutants_have_no_results(evaluation_run, occurrences):
    """DATA.md E6 and E7 — an old string occurring zero or twice is invalid, not run."""
    product_file = evaluation_run / "workspace/product/calc.py"
    original = CALC + "# duplicate marker\n" * occurrences
    product_file.write_text(original, encoding="utf-8")
    write_mutants(evaluation_run, [
        {"case": "X9-F1", "file": "calc.py", "old": "duplicate marker", "new": "changed"},
        add_mutant("X1-F1", "return a - b"),
    ])
    matrix = build_matrix(evaluation_run)
    assert set(matrix["mutants"]) == {"X9-F1", "X1-F1"}
    invalid = matrix["mutants"]["X9-F1"]
    assert invalid["status"] == "invalid"
    assert invalid.get("results", {}) == {}
    assert matrix["product"] == {"test_calc::test_add": "pass"}
    assert matrix["mutants"]["X1-F1"] == {
        "status": "applied", "results": {"test_calc::test_add": "fail"},
    }
    assert product_file.read_bytes() == original.encode("utf-8")
    assert matrix["restored"] is True


def test_every_product_file_is_restored_and_source_is_untouched(evaluation_run, tmp_path):
    """EV-C3.3 — all copy files restore byte for byte and the original source stays untouched."""
    product = evaluation_run / "workspace/product"
    (product / "nested").mkdir()
    (product / "nested/settings.py").write_bytes(b'MODE = "clean"\r\n# caf\xc3\xa9\r\n')
    (product / "nested/payload.bin").write_bytes(b"\x00\xff\r\n\x80")
    (product / ".hidden").write_bytes(b"hidden\r\n")
    original_source = tmp_path / "original source"
    before = file_bytes(product)
    for relative, content in before.items():
        destination = original_source / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    original_before = file_bytes(original_source)
    hashes_before = {name: hashlib.sha256(content).hexdigest() for name, content in before.items()}
    write_mutants(evaluation_run, [
        add_mutant("X1-F1", "return a - b"),
        {"case": "X2-F1", "file": "nested/settings.py", "old": 'MODE = "clean"',
         "new": 'MODE = "broken"'},
        add_mutant("X3-F1", "return a + b + 1"),
    ])
    matrix = build_matrix(evaluation_run)
    assert matrix["mutants"] == {
        "X1-F1": {"status": "applied", "results": {"test_calc::test_add": "fail"}},
        "X2-F1": {"status": "applied", "results": {"test_calc::test_add": "pass"}},
        "X3-F1": {"status": "applied", "results": {"test_calc::test_add": "fail"}},
    }
    after = file_bytes(product)
    assert after == before
    assert {name: hashlib.sha256(content).hexdigest() for name, content in after.items()} == hashes_before
    assert matrix["restored"] is True
    assert file_bytes(original_source) == original_before


def test_restored_flag_matches_all_file_hashes(evaluation_run):
    """EV-C3.3 — restored reflects every copy file's hash, including probe side effects."""
    product = evaluation_run / "workspace/product"
    (product / "payload.bin").write_bytes(b"original payload\x00\xff")
    before = {name: hashlib.sha256(content).hexdigest()
              for name, content in file_bytes(product).items()}
    write_probes(evaluation_run, '''\
        def test_probe_side_effect():
            """X1-F1 — a mutant run also changes a file outside its replacement target."""
            if calc.add(2, 3) != 5:
                (Path(os.environ["EVAL_PRODUCT"]) / "payload.bin").write_bytes(b"changed payload")
            assert calc.add(2, 3) == 5
    ''')
    write_mutants(evaluation_run, [add_mutant("X1-F1", "return a - b")])
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {"test_calc::test_probe_side_effect": "pass"}
    assert matrix["mutants"] == {"X1-F1": {"status": "applied", "results": {
        "test_calc::test_probe_side_effect": "fail",
    }}}
    assert (product / "calc.py").read_bytes() == CALC.encode("utf-8")
    after = {name: hashlib.sha256(content).hexdigest()
             for name, content in file_bytes(product).items()}
    # Either restoring the entire copy or reporting its remaining damage is observable.
    assert matrix["restored"] is (after == before)


def test_citations_follow_docstring_prefix_and_parametrised_keys(evaluation_run):
    """DATA.md E6 and E7 — each parametrised JUnit key inherits only leading case ids."""
    write_probes(evaluation_run, '''\
        @pytest.mark.parametrize("left,right,total", [(2, 3, 5), (-2, -3, -5)], ids=["positive", "negative"])
        def test_pairs(left, right, total):
            """X1-F1 X2-F2 — addition covers both cases; X9-F9 is prose, not a citation."""
            assert calc.add(left, right) == total

        def test_plain():
            """X3-F1 — a plain function also gets a citation."""
            assert calc.add(0, 0) == 0
    ''')
    write_probes(evaluation_run, '''\
        def test_other_module():
            """V1-F1 — module names distinguish identical test names."""
            assert calc.add(1, 1) == 2
    ''', filename="test_other.py")
    matrix = build_matrix(evaluation_run)
    assert matrix["citations"] == {
        "test_calc::test_pairs[positive]": ["X1-F1", "X2-F2"],
        "test_calc::test_pairs[negative]": ["X1-F1", "X2-F2"],
        "test_calc::test_plain": ["X3-F1"],
        "test_other::test_other_module": ["V1-F1"],
    }
    assert matrix["product"] == {key: "pass" for key in matrix["citations"]}


def test_import_error_counts_as_fail(evaluation_run):
    """DATA.md E6 and E7 — an exception during probe import is recorded as fail."""
    write_probes(evaluation_run, '''\
        raise RuntimeError("deliberate collection error")

        def test_unreachable():
            """X1-F1 — the module must import before this can run."""
            assert calc.add(2, 3) == 5
    ''')
    matrix = build_matrix(evaluation_run)
    assert matrix["product"], "a collection error must not become an empty successful run"
    assert all("::" in key for key in matrix["product"])
    assert set(matrix["product"].values()) == {"fail"}
    assert matrix["restored"] is True


def test_runtime_exception_counts_as_fail(evaluation_run):
    """DATA.md E6 and E7 — an exception in a probe is fail under that probe's key."""
    write_probes(evaluation_run, '''\
        def test_exception():
            """X1-F1 — exceptions cannot be treated as passing evidence."""
            raise RuntimeError("deliberate probe exception")
    ''')
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {"test_calc::test_exception": "fail"}


def test_cli_timeout_marks_every_product_probe_fail(evaluation_run):
    """DATA.md E6 and E7 — --timeout caps pytest, records all probes fail and exits zero."""
    write_probes(evaluation_run, '''\
        import time

        def test_fast():
            """X1-F1 — even a fast probe is fail when its run times out."""
            assert calc.add(2, 3) == 5

        def test_slow():
            """X2-F1 — this probe outlasts the one-second run timer."""
            time.sleep(30)
    ''')
    completed = run_cli(evaluation_run, "--timeout", "1")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    matrix = json.loads((evaluation_run / "matrix.json").read_text(encoding="utf-8"))
    assert matrix["product"] == {
        "test_calc::test_fast": "fail", "test_calc::test_slow": "fail",
    }
    assert matrix["citations"] == {
        "test_calc::test_fast": ["X1-F1"], "test_calc::test_slow": ["X2-F1"],
    }
    assert matrix["restored"] is True


def test_cli_timeout_on_mutant_restores_product(evaluation_run):
    """EV-C3.2 EV-C3.3 — a mutant timeout fails all its probes and still restores the copy."""
    write_probes(evaluation_run, '''\
        import time

        def test_fast():
            """X1-F1 — the run has a fast probe as well as a sleeper."""
            assert calc.add(0, 0) == 0

        def test_slow_if_mutated():
            """X2-F1 — only the broken product causes a timeout."""
            if calc.add(2, 3) != 5:
                time.sleep(30)
            assert calc.add(2, 3) == 5
    ''')
    before = file_bytes(evaluation_run / "workspace/product")
    write_mutants(evaluation_run, [add_mutant("X2-F1", "return a - b")])
    completed = run_cli(evaluation_run, "--timeout", "1")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    matrix = json.loads((evaluation_run / "matrix.json").read_text(encoding="utf-8"))
    assert matrix["product"] == {
        "test_calc::test_fast": "pass", "test_calc::test_slow_if_mutated": "pass",
    }
    assert matrix["mutants"] == {"X2-F1": {"status": "applied", "results": {
        "test_calc::test_fast": "fail", "test_calc::test_slow_if_mutated": "fail",
    }}}
    assert file_bytes(evaluation_run / "workspace/product") == before
    assert matrix["restored"] is True


def test_neighbour_pytest_config_is_ignored(evaluation_run, monkeypatch):
    """DATA.md E6 and E7 — -c /dev/null prevents neighbouring pytest.ini breaking collection."""
    (evaluation_run / "pytest.ini").write_text(
        "[pytest]\naddopts = --deliberately-invalid-evaluator-option\n", encoding="utf-8"
    )
    monkeypatch.chdir(evaluation_run)
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {"test_calc::test_add": "pass"}
    assert matrix["citations"] == {"test_calc::test_add": ["X1-F1"]}
    assert not (evaluation_run / ".pytest_cache").exists()
    assert not (evaluation_run / "probes/.pytest_cache").exists()


def test_missing_product_exits_two_without_traceback(evaluation_run):
    """DATA.md E6 and E7 — a missing workspace/product is a path diagnostic with exit two."""
    product = evaluation_run / "workspace/product"
    (product / "calc.py").unlink()
    product.rmdir()
    completed = run_cli(evaluation_run)
    assert completed.returncode == 2
    diagnostics = completed.stderr.splitlines()
    assert any(line.startswith(f"{product}: ") and line[len(str(product)) + 2:].strip()
               for line in diagnostics), completed.stderr
    assert "Traceback" not in completed.stderr + completed.stdout
    assert not (evaluation_run / "matrix.json").exists()


def test_cli_writes_matrix_contract(evaluation_run):
    """DATA.md E6 and E7 — the CLI writes UTF-8 matrix.json with the agreed relative paths."""
    write_mutants(evaluation_run, [add_mutant("X1-F1", "return a - b")])
    completed = run_cli(evaluation_run)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    matrix = json.loads((evaluation_run / "matrix.json").read_text(encoding="utf-8"))
    assert matrix == {
        "product_dir": "workspace/product", "probes_dir": "probes",
        "citations": {"test_calc::test_add": ["X1-F1"]},
        "product": {"test_calc::test_add": "pass"},
        "mutants": {"X1-F1": {"status": "applied", "results": {"test_calc::test_add": "fail"}}},
        "restored": True,
    }
