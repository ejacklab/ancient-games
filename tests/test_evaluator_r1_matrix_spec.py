"""R1-F3 — Repair R1 contract tests for probe_matrix.py and spec_parse.py.

The expected behavior comes from DATA.md's Repair R1, not from the implementation.
Real probes run only against hand-built temporary product copies.
"""
from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
import textwrap

import pytest

from test_evaluator_probe_matrix import (
    add_mutant,
    build_matrix,
    evaluation_run,
    file_bytes,
    isolate_pytest_environment,
    load_tool,
    run_cli,
    write_mutants,
    write_probes,
)
from test_evaluator_spec_parse import TOOL as SPEC_TOOL, load_spec_parse


@pytest.mark.parametrize("citation", [
    "EV-P1-F2", "EV-C3.3-F1", "B1-F1", "W1.3-F2", "V5-F1",
])
def test_required_citation_is_read(evaluation_run, citation):
    """R1-F3 — each specified group or vision case reaches the matrix's citations."""
    write_probes(evaluation_run, f'''\
        def test_cited():
            """{citation} — the calculator returns a sum."""
            assert calc.add(2, 3) == 5
    ''')
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {"test_calc::test_cited": "pass"}
    assert matrix["citations"] == {"test_calc::test_cited": [citation]}


def test_prefixed_citations_follow_parametrised_keys(evaluation_run):
    """R1-F3 — leading citations survive parameters and stop before prose citations."""
    write_probes(evaluation_run, '''\
        @pytest.mark.parametrize("value", [1, 2], ids=["one", "two"])
        def test_cited(value):
            """EV-P1-F2, EV-C3.3-F1; B1-F1 W1.3-F2 V5-F1 — prose mentions EV-R9-F9."""
            assert calc.add(value, 0) == value
    ''')
    matrix = build_matrix(evaluation_run)
    expected = ["EV-P1-F2", "EV-C3.3-F1", "B1-F1", "W1.3-F2", "V5-F1"]
    assert matrix["citations"] == {
        "test_calc::test_cited[one]": expected,
        "test_calc::test_cited[two]": expected,
    }


def test_citation_grammar_uses_imported_spec_id(tmp_path):
    """R1-F3 — changing ID in a scratch copy changes CITATION through a spec_parse import."""
    evaluator_copy = tmp_path / "tools/evaluator"
    shutil.copytree(SPEC_TOOL.parent, evaluator_copy)
    copied_spec = evaluator_copy / "spec_parse.py"
    source = copied_spec.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assignment = next(
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "ID" for target in node.targets)
    )
    original_id = load_spec_parse().ID
    lines = source.splitlines(keepends=True)
    lines[assignment.lineno - 1:assignment.end_lineno] = [
        f"ID = {f'(?:{original_id}|ZETA)'!r}\n"
    ]
    copied_spec.write_text("".join(lines), encoding="utf-8")
    matrix_source = (evaluator_copy / "probe_matrix.py").read_text(encoding="utf-8")
    imports = [node for node in ast.walk(ast.parse(matrix_source))
               if isinstance(node, (ast.Import, ast.ImportFrom))]
    assert any(
        (isinstance(node, ast.ImportFrom)
         and (node.module or "").split(".")[-1] == "spec_parse"
         and any(alias.name == "ID" for alias in node.names))
        or (isinstance(node, ast.Import)
            and any(alias.name.split(".")[-1] == "spec_parse" for alias in node.names))
        or (isinstance(node, ast.ImportFrom)
            and any(alias.name == "spec_parse" for alias in node.names))
        for node in imports
    ), "probe_matrix must import spec_parse.ID instead of copying its grammar"
    completed = subprocess.run(
        [sys.executable, "-c", textwrap.dedent('''\
            import sys
            sys.path.insert(0, "tools/evaluator")
            from tools.evaluator import probe_matrix
            assert probe_matrix.CITATION.fullmatch("ZETA-F7") is not None
        ''')],
        cwd=tmp_path, env=os.environ.copy(), capture_output=True, text=True, timeout=10,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_product_probe_write_is_recorded(evaluation_run):
    """R1-F4 — a passing product probe that writes into the copy sets product_changed true."""
    write_probes(evaluation_run, '''\
        def test_writes_product():
            """B1-F1 — a green probe can still change the product."""
            (Path(os.environ["EVAL_PRODUCT"]) / "probe-created.txt").write_text("changed")
            assert calc.add(2, 3) == 5
    ''')
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {"test_calc::test_writes_product": "pass"}
    assert matrix["product_changed"] is True


@pytest.mark.parametrize("with_mutant", [False, True], ids=["product-only", "with-mutant"])
@pytest.mark.parametrize("operation", ["overwrite", "create", "delete"])
def test_copy_restores_to_before_product_run(evaluation_run, operation, with_mutant):
    """R1-F4 — restoration uses the first baseline for overwritten, new and deleted files."""
    product = evaluation_run / "workspace/product"
    (product / "payload.bin").write_bytes(b"original\x00\xff\r\n")
    before = file_bytes(product)
    side_effect = {
        "overwrite": 'target.write_bytes(b"overwritten")',
        "create": '(target.parent / "new.bin").write_bytes(b"created")',
        "delete": 'target.unlink(missing_ok=True)',
    }[operation]
    write_probes(evaluation_run, f'''\
        def test_changes_copy():
            """B1-F1 — product and mutant runs can change files outside the mutant target."""
            target = Path(os.environ["EVAL_PRODUCT"]) / "payload.bin"
            {side_effect}
            assert calc.add(2, 3) == 5
    ''')
    if with_mutant:
        write_mutants(evaluation_run, [add_mutant("B1-F1", "return a - b")])
    matrix = build_matrix(evaluation_run)
    after = file_bytes(product)
    assert matrix["restored"] is (after == before), "restored must use the pre-product baseline"
    assert after == before, "the copy must be restored even when there are no mutants"
    assert matrix["restored"] is True
    assert matrix["product_changed"] is True


def test_junit_errors_are_separate_from_failures(evaluation_run):
    """R1-F5 — a completed report lists setup errors, excluding assertion and runtime failures."""
    write_probes(evaluation_run, '''\
        @pytest.fixture
        def broken_setup():
            raise RuntimeError("deliberate setup error")

        def test_setup_error(broken_setup):
            """B1-F1 — this probe never reaches its assertion."""
            assert calc.add(2, 3) == 5

        def test_assertion_failure():
            """B1-F2 — an assertion produces a JUnit failure."""
            assert calc.add(2, 3) == 999

        def test_runtime_failure():
            """B1-F3 — an exception in a test body also produces a JUnit failure."""
            raise RuntimeError("deliberate test-body failure")

        @pytest.mark.skip(reason="contract fixture")
        def test_skip():
            """B1-F4 — skips keep their existing result shape."""
            assert False
    ''')
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {
        "test_calc::test_setup_error": "fail",
        "test_calc::test_assertion_failure": "fail",
        "test_calc::test_runtime_failure": "fail",
        "test_calc::test_skip": "skip",
    }
    assert set(matrix["output"]) == {
        "test_calc::test_setup_error", "test_calc::test_assertion_failure",
        "test_calc::test_runtime_failure",
    }
    assert all(isinstance(message, str) and message for message in matrix["output"].values())
    assert matrix["runs"]["product"] == {
        "status": "ok", "errors": ["test_calc::test_setup_error"],
    }


def test_mutant_run_records_its_own_junit_errors(evaluation_run):
    """R1-F5 — a mutant's setup errors are recorded separately from its red assertions."""
    write_probes(evaluation_run, '''\
        @pytest.fixture
        def healthy_setup():
            if calc.add(2, 3) != 5:
                raise RuntimeError("mutant setup error")

        def test_setup(healthy_setup):
            """B1-F1 — a setup error belongs to the mutant run only."""
            assert calc.add(2, 3) == 5

        def test_sum():
            """B1-F1 — a red assertion remains a failure, not an error."""
            assert calc.add(2, 3) == 5

        def test_control():
            """B1-F2 — this control remains green."""
            assert calc.add(0, 0) == 0
    ''')
    write_mutants(evaluation_run, [add_mutant("B1-F1", "return a - b")])
    matrix = build_matrix(evaluation_run)
    assert matrix["product"] == {
        "test_calc::test_setup": "pass", "test_calc::test_sum": "pass",
        "test_calc::test_control": "pass",
    }
    assert matrix["mutants"] == {"B1-F1": {"status": "applied", "results": {
        "test_calc::test_setup": "fail", "test_calc::test_sum": "fail",
        "test_calc::test_control": "pass",
    }}}
    assert matrix["runs"] == {
        "product": {"status": "ok", "errors": []},
        "B1-F1": {"status": "ok", "errors": ["test_calc::test_setup"]},
    }
    assert "output" not in matrix, "mutant errors must not become product failure output"


def test_collection_error_is_listed_by_junit_key(evaluation_run):
    """R1-F5 — a collection error's JUnit key is preserved in results and in errors."""
    write_probes(evaluation_run, '''\
        raise RuntimeError("deliberate import error")

        def test_unreachable():
            """B1-F1 — collection fails before this function can execute."""
            assert calc.add(2, 3) == 5
    ''')
    matrix = build_matrix(evaluation_run)
    assert matrix["product"]
    assert set(matrix["product"].values()) == {"fail"}
    assert matrix["runs"]["product"]["status"] == "ok"
    assert set(matrix["runs"]["product"]["errors"]) == set(matrix["product"])


@pytest.mark.parametrize("mutant_only", [False, True], ids=["product-timeout", "mutant-timeout"])
def test_timeout_has_run_status(evaluation_run, mutant_only):
    """R1-F5 — a real timeout records timeout for the affected run and keeps red results."""
    write_probes(evaluation_run, f'''\
        import time

        def test_control():
            """B1-F2 — a timeout still marks every planned probe red."""
            assert calc.add(0, 0) == 0

        def test_slow():
            """B1-F1 — a hanging probe exceeds the run's two-second timer."""
            if {mutant_only!r} is False or calc.add(2, 3) != 5:
                time.sleep(30)
            assert calc.add(2, 3) == 5
    ''')
    before = file_bytes(evaluation_run / "workspace/product")
    if mutant_only:
        write_mutants(evaluation_run, [add_mutant("B1-F1", "return a - b")])
    completed = run_cli(evaluation_run, "--timeout", "2")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    matrix = json.loads((evaluation_run / "matrix.json").read_text(encoding="utf-8"))
    red = {"test_calc::test_control": "fail", "test_calc::test_slow": "fail"}
    if mutant_only:
        assert matrix["product"] == {key: "pass" for key in red}
        assert matrix["mutants"] == {"B1-F1": {"status": "applied", "results": red}}
        assert matrix["runs"]["product"] == {"status": "ok", "errors": []}
        run_name = "B1-F1"
    else:
        assert matrix["product"] == red
        assert matrix["mutants"] == {}
        run_name = "product"
    assert matrix["runs"][run_name] == {"status": "timeout", "errors": []}
    assert file_bytes(evaluation_run / "workspace/product") == before
    assert matrix["restored"] is True


def test_missing_junit_report_has_no_report_status(evaluation_run, monkeypatch):
    """R1-F5 — a subprocess leaving no JUnit file records no-report, with no invented errors."""
    module = load_tool()

    def finish_without_report(command, **kwargs):
        return subprocess.CompletedProcess(command, 2, stdout="", stderr="no report")

    monkeypatch.setattr(module.subprocess, "run", finish_without_report)
    write_mutants(evaluation_run, [add_mutant("B1-F1", "return a - b")])
    matrix = module.build_matrix(evaluation_run, timeout=10)
    assert matrix["product"] == {"test_calc::test_add": "fail"}
    assert matrix["mutants"] == {"B1-F1": {"status": "applied", "results": {
        "test_calc::test_add": "fail",
    }}}
    assert matrix["runs"] == {
        "product": {"status": "no-report", "errors": []},
        "B1-F1": {"status": "no-report", "errors": []},
    }


def test_existing_matrix_keys_keep_their_shapes(evaluation_run):
    """R1-F5 — added run metadata preserves every pre-existing matrix field's shape."""
    write_mutants(evaluation_run, [
        add_mutant("B1-F1", "return a - b"),
        {"case": "B2-F1", "file": "calc.py", "old": "absent text", "new": "anything"},
    ])
    matrix = build_matrix(evaluation_run)
    assert {key: matrix[key] for key in (
        "product_dir", "probes_dir", "citations", "product", "mutants", "restored",
    )} == {
        "product_dir": "workspace/product", "probes_dir": "probes",
        "citations": {"test_calc::test_add": ["X1-F1"]},
        "product": {"test_calc::test_add": "pass"},
        "mutants": {
            "B1-F1": {"status": "applied", "results": {"test_calc::test_add": "fail"}},
            "B2-F1": {"status": "invalid"},
        },
        "restored": True,
    }
    assert "output" not in matrix


@pytest.mark.parametrize("requirements", [
    "", "# No requirements\n\nOrdinary prose.\n",
    "**B1 — Empty group**\n- **Fails if** something goes wrong.\n",
], ids=["empty-file", "prose-only", "heading-only"])
def test_spec_cli_rejects_empty_manifest(tmp_path, requirements):
    """R1-F1 — no requirement or vision ids exits two with a path diagnostic and no output."""
    requirements_file = tmp_path / "REQUIREMENTS.md"
    requirements_file.write_text(requirements, encoding="utf-8")
    output = tmp_path / "requirements.json"
    completed = subprocess.run(
        [sys.executable, str(SPEC_TOOL), "--requirements", str(requirements_file),
         "--out", str(output)],
        cwd=tmp_path, env=os.environ.copy(), capture_output=True, text=True, timeout=10,
    )
    assert completed.returncode == 2, completed.stdout + completed.stderr
    assert completed.stderr.strip() == f"{requirements_file}: no requirement ids found"
    assert "Traceback" not in completed.stdout + completed.stderr
    assert not output.exists()


def test_vision_id_prevents_empty_manifest_rejection(tmp_path):
    """R1-F1 — a vision id makes the manifest nonempty even without requirement ids."""
    requirements = tmp_path / "REQUIREMENTS.md"
    requirements.write_text("# No requirement bullets\n", encoding="utf-8")
    vision = tmp_path / "VISION.md"
    vision.write_text("**What it will never do**\n- Lose a requirement.\n", encoding="utf-8")
    output = tmp_path / "requirements.json"
    completed = subprocess.run(
        [sys.executable, str(SPEC_TOOL), "--requirements", str(requirements),
         "--vision", str(vision), "--out", str(output)],
        cwd=tmp_path, env=os.environ.copy(), capture_output=True, text=True, timeout=10,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert json.loads(output.read_text(encoding="utf-8"))["manifest"] == ["V1"]


def test_unparsed_ids_include_colon_bold_bullets():
    """R1-F14 — id-shaped colon bullets cannot disappear from both manifest and unparsed_ids."""
    document = load_spec_parse().parse(textwrap.dedent('''\
        **B1 — Input**
        - **B1.2** A parsed requirement.
        - **B1.1:** A colon is inside the bold.
        - **EV-C3.3:** A prefixed dotted id is also visible.
        - **Fails if** an id disappears.
    '''))
    assert "B1.2" in document["manifest"]
    assert isinstance(document["unparsed_ids"], list)
    assert set(document["unparsed_ids"]) == {"B1.1", "EV-C3.3"} - set(document["manifest"])


def test_unparsed_ids_find_orphans_without_counting_prose():
    """R1-F14 — bold id bullets outside groups are reported; parsed ids and inline prose are excluded."""
    document = load_spec_parse().parse(textwrap.dedent('''\
        - **Q1.1** Before any group heading.
          - **EV-P2.1 Title** Also before a heading, but indented and titled.

        **B1 — Input**
        - **B1.1** Parsed plain id.
        - **B1.2 Title** Parsed titled id.
        - **B1.3:** Colon bullet.
        - **Fails if** a requirement disappears.
        A sentence mentions - **C1.1:** but is not a bullet.
        - Ordinary prose mentions **D1.1** after the bullet's start.
        - **Not-an-id** Ordinary bold text.
        - **B1.20Oops** Not a complete id token.
    '''))
    assert {"B1.1", "B1.2"} <= set(document["manifest"])
    assert isinstance(document["unparsed_ids"], list)
    assert set(document["unparsed_ids"]) == {"Q1.1", "EV-P2.1", "B1.3"} - set(document["manifest"])


def test_fully_parsed_spec_has_empty_unparsed_ids():
    """R1-F14 — unparsed_ids is an empty list when every bold id bullet is in the manifest."""
    document = load_spec_parse().parse(textwrap.dedent('''\
        **B1 — Input**
        - **B1.1** Parsed plain id.
        - **B1.2 Title** Parsed titled id.
        - **Fails if** a requirement disappears.
    '''))
    assert document["manifest"] == ["B1.1", "B1.2"]
    assert document["unparsed_ids"] == []


def test_spec_cli_writes_unparsed_ids(tmp_path):
    """R1-F14 — the CLI preserves unparsed_ids in its requirements.json output."""
    requirements = tmp_path / "REQUIREMENTS.md"
    requirements.write_text(
        "**B1 — Input**\n- **B1.2** Parsed.\n- **B1.1:** Unparsed colon bullet.\n",
        encoding="utf-8",
    )
    output = tmp_path / "requirements.json"
    completed = subprocess.run(
        [sys.executable, str(SPEC_TOOL), "--requirements", str(requirements),
         "--out", str(output)],
        cwd=tmp_path, env=os.environ.copy(), capture_output=True, text=True, timeout=10,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    document = json.loads(output.read_text(encoding="utf-8"))
    assert isinstance(document["unparsed_ids"], list)
    assert set(document["unparsed_ids"]) == {"B1.1"} - set(document["manifest"])
