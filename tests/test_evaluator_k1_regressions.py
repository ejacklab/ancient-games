"""Regression tests for what calibration K1 found (run 20261013-requirements-evaluator, D5, 2026-10-13).

Written by the COO after K1:
- 49 of 49 probes came back red because probe_matrix ran pytest on relative paths (tested in
  test_evaluator_probe_matrix.py);
- the confirm step confirmed 28 of those setup failures from the probe source alone, because no failure output was
  recorded;
- the judge's files never landed (the shell write was refused) and the merge read them as empty;
- the judge cited its code by a run-folder path.

Helpers come from the model_io tests, so these cases build the same small run folder.
"""
from __future__ import annotations

from test_evaluator_model_io import MATRIX, build_run, cli_ok, judge_folder, read, run_model_io, write_json


def test_a_confirmation_with_no_failure_output_is_voided(tmp_path):
    """EV-C4.1 — a red probe with no recorded failure message cannot be confirmed as a product failure."""
    run = build_run(tmp_path, matrix={key: value for key, value in MATRIX.items() if key != "output"})
    cli_ok("confirm-input", run)
    entries = read(run / "confirm-input.json")["cases"]
    write_json(run / "confirm.json", {"cases": [
        {"case": e["case"], "probe": e["probe"], "faithful": True,
         "requirement_quote": e["group_text"].split("\n")[0], "probe_quote": e["probe_source"].split("\n")[0]}
        for e in entries]})
    cli_ok("confirm-check", run)
    answers = read(run / "confirm.json")["cases"]
    assert answers and all(a["faithful"] is False and a["note"] == "no failure output" for a in answers)


def test_a_failure_on_a_file_the_blind_workspace_removed_is_voided(tmp_path):
    """EV-R2.1 EV-C4.1 — K1b: a probe that failed because the evaluator removed the product's tests is not a FAIL."""
    run = build_run(tmp_path)
    write_json(run / "workspace/manifest.json", {"copied": {}, "excluded": ["runs", "tests/test_calc.py"], "skipped": []})
    matrix = dict(MATRIX, output={"test_b1::test_sum": "AssertionError: tests/test_calc.py is missing from the product",
                                  "test_b1::test_missing_file": "AssertionError: /x/runs/abc/workspace assert False"})
    write_json(run / "matrix.json", matrix)
    cli_ok("confirm-input", run)
    entries = read(run / "confirm-input.json")["cases"]
    write_json(run / "confirm.json", {"cases": [
        {"case": e["case"], "probe": e["probe"], "faithful": True,
         "requirement_quote": e["group_text"].split("\n")[0], "probe_quote": e["probe_source"].split("\n")[0]}
        for e in entries]})
    cli_ok("confirm-check", run)
    notes = {a["probe"]: a.get("note", "") for a in read(run / "confirm.json")["cases"]}
    assert notes["test_b1::test_sum"] == "needs a file the blind workspace removed"
    assert notes["test_b1::test_missing_file"] != "needs a file the blind workspace removed"  # 'runs' is a folder


def test_a_fail_repro_runs_from_the_run_folder_with_an_absolute_product_path():
    """EV-P2.1 — K1b: a relative EVAL_PRODUCT broke the repro inside a probe that changes directory."""
    import importlib.util
    from pathlib import Path
    tool = Path(__file__).resolve().parents[1] / "tools/evaluator/verdict.py"
    spec = importlib.util.spec_from_file_location("verdict_k1b", tool)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    repro = module._repro_command("test_b1::test_x[1]", {"product_dir": "workspace/product", "probes_dir": "probes"})
    assert repro.startswith('EVAL_PRODUCT="$PWD"/workspace/product ')


def test_probes_run_with_home_and_tmpdir_in_a_scratch_folder(tmp_path):
    """R1-F9 — a model-written probe must not see the user's real HOME or shared TMPDIR (COO, after R1)."""
    import importlib.util
    import json
    import os
    from pathlib import Path
    run = tmp_path / "run"
    (run / "workspace/product").mkdir(parents=True)
    (run / "workspace/product/calc.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    (run / "probes").mkdir()
    (run / "probes/test_env.py").write_text(
        "import os\n\ndef test_env():\n    '''X1-F1 — env'''\n"
        "    open(os.path.join(os.environ['EVAL_PRODUCT'], '..', 'seen.json'), 'w').write("
        "__import__('json').dumps([os.environ['HOME'], os.environ['TMPDIR']]))\n", encoding="utf-8")
    tool = Path(__file__).resolve().parents[1] / "tools/evaluator/probe_matrix.py"
    spec = importlib.util.spec_from_file_location("probe_matrix_f9", tool)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.build_matrix(run, timeout=30)
    home, tmpdir = json.loads((run / "workspace/seen.json").read_text())
    assert home != os.environ.get("HOME") and tmpdir == home
    assert "probe-matrix-" in home


def test_confirm_check_blocks_when_the_confirm_step_wrote_nothing(tmp_path):
    """EV-C6.2 — work to confirm and no confirm.json is a failed model step: exit 1, never an empty answer."""
    run = build_run(tmp_path)
    cli_ok("confirm-input", run)
    result = run_model_io("confirm-check", run)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "confirm.json" in result.stderr and "Traceback" not in result.stderr


def test_judged_merge_blocks_when_a_judge_wrote_nothing(tmp_path):
    """EV-C6.2 — judged cases and no judge-1.json is a failed model step: exit 1, not 'plant missed'."""
    run = build_run(tmp_path)
    cli_ok("judge-input", run)
    assert read(run / "judge-input.json")["cases"], "the fixture must have a judged case"
    result = run_model_io("judged-merge", run)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "judge-1.json" in result.stderr


def test_a_judge_may_cite_code_by_its_run_folder_path(tmp_path):
    """EV-C5.1 — evidence written as judge-copy/<file>:<line> still finds its quote (K1's judge wrote it so)."""
    run = build_run(tmp_path)
    cli_ok("judge-input", run)
    judge_input = read(run / "judge-input.json")
    # After R1-F2 the plant lives in .coordinator/ and call 1 works in its own folder outside the run (COO, R1).
    plant = read(run / ".coordinator/plant.json")["plant_case"]
    folder = judge_folder(run)
    copy_text = (folder / "product/calc.py").read_text(encoding="utf-8")
    line = next(l for l in copy_text.splitlines() if l.strip())
    write_json(folder / "judge-1.json", {"cases": [
        {"case": c["case"], "holds": c["case"] != plant, "evidence": f'judge-copy/calc.py:1 "{line.strip()}" — reason'}
        for c in judge_input["cases"]]})
    clean = (run / "workspace/product/calc.py").read_text(encoding="utf-8").splitlines()[0].strip()
    write_json(run / "judge-2.json", {"cases": [
        {"case": plant, "holds": True, "evidence": f'workspace/product/calc.py:1 "{clean}" — reason'}]})
    cli_ok("judged-merge", run)
    judged = read(run / "judged.json")
    assert judged["plant_found"] is True
    assert {c["case"] for c in judged["cases"]} == {c["case"] for c in judge_input["cases"]}
