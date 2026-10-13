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

from test_evaluator_model_io import MATRIX, build_run, cli_ok, read, run_model_io, write_json


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
    plant = judge_input["plant_case"]
    copy_text = (run / "judge-copy/calc.py").read_text(encoding="utf-8")
    line = next(l for l in copy_text.splitlines() if l.strip())
    write_json(run / "judge-1.json", {"cases": [
        {"case": c["case"], "holds": c["case"] != plant, "evidence": f'judge-copy/calc.py:1 "{line.strip()}" — reason'}
        for c in judge_input["cases"]]})
    clean = (run / "workspace/product/calc.py").read_text(encoding="utf-8").splitlines()[0].strip()
    write_json(run / "judge-2.json", {"cases": [
        {"case": plant, "holds": True, "evidence": f'workspace/product/calc.py:1 "{clean}" — reason'}]})
    cli_ok("judged-merge", run)
    judged = read(run / "judged.json")
    assert judged["plant_found"] is True
    assert {c["case"] for c in judged["cases"]} == {c["case"] for c in judge_input["cases"]}
