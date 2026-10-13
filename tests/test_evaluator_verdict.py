"""Tests for tools/evaluator/verdict.py, the step that turns the recorded results into the verdict.

Every input is written by hand under tmp_path, so each test names one rule of DATA.md's E10 section and no rule
depends on a step that ran before it. The module is imported by path inside a helper, not at module level, because
it does not exist yet: this file must collect today and every test must fail on its own until the code lands.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools/evaluator/verdict.py"

RED_PROBE = "test_b1::test_red"
GREEN_PROBE = "test_b3::test_green"
CASE = "B1-F1"
JUDGED_CASE = "G2-F1"
EVIDENCE = 'tools/app.py:12 "return 1"'
FAITHFUL = {"case": CASE, "probe": "probes/test_b1.py::test_red", "faithful": True,
            "requirement_quote": "It reads the thing.", "probe_quote": "E   assert False"}


def load_verdict():
    """Import tools/evaluator/verdict.py by path, inside the test, so this file collects without it."""
    if not TOOL.is_file():
        pytest.fail(f"{TOOL} does not exist yet")
    spec = importlib.util.spec_from_file_location("evaluator_verdict", TOOL)
    module = importlib.util.module_from_spec(spec)
    sys.modules["evaluator_verdict"] = module
    spec.loader.exec_module(module)
    return module


def write_json(path, document):
    """One recorded input, written the way the step before wrote it."""
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def requirements_document(case, group="B1", ids=None, open_ids=None, vision=None, status="in_scope"):
    """requirements.json's content for one group with one case, plus any vision lines."""
    ids = [ids] if isinstance(ids, str) else list(ids or [f"{group}.1"])
    vision = list(vision or [])
    return {"spec": {"requirements": "spec/REQUIREMENTS.md", "vision": None},
            "groups": [{"group": group, "title": "What it reads", "ids": ids, "status": status,
                        "fails_if": "a thing breaks",
                        "cases": [{"case": case, "text": "a thing breaks"}],
                        "open_ids": list(open_ids or [])}],
            "vision": vision,
            "manifest": ids + [line["id"] for line in vision]}


def several_groups(*groups):
    """requirements.json's content for several one-case groups, each given as (group, ids, open ids)."""
    document = requirements_document(f"{groups[0][0]}-F1", group=groups[0][0], ids=groups[0][1],
                                     open_ids=groups[0][2])
    for name, ids, open_ids in groups[1:]:
        document["groups"].append({"group": name, "title": "Another group", "ids": list(ids), "status": "in_scope",
                                   "fails_if": "a thing breaks",
                                   "cases": [{"case": f"{name}-F1", "text": "a thing breaks"}],
                                   "open_ids": list(open_ids)})
        document["manifest"].extend(ids)
    return document


def classify_document(case, kind="executable", reason="run the probe"):
    """classify.json's content: one labelled case with the reason that makes the label trustworthy."""
    return {"cases": [{"case": case, "kind": kind, "reason": reason}]}


def matrix_document(citations, product, mutants, restored=True):
    """matrix.json's content: which probe cites which case, and what each side of the run said."""
    return {"product_dir": "workspace/product", "probes_dir": "probes", "citations": citations,
            "product": product, "mutants": mutants, "restored": restored}


def default_files(case=CASE, probe=RED_PROBE):
    """The five recorded inputs for a case that is about to pass: green on the product, red on its mutant."""
    return {"requirements": requirements_document(case),
            "classify": classify_document(case),
            "matrix": matrix_document({probe: [case]}, {probe: "pass"},
                                      {case: {"status": "applied", "results": {probe: "fail"}}}),
            "confirm": {"cases": []},
            "judged": {"plant_found": True, "cases": []}}


def make_run(root, case=CASE, probe=RED_PROBE, **overrides):
    """A run folder holding the recorded inputs; an override of None leaves that file out of the folder."""
    run = root / "run"
    run.mkdir(parents=True, exist_ok=True)
    documents = default_files(case, probe)
    documents.update(overrides)
    for name, document in documents.items():
        if document is not None:
            write_json(run / f"{name}.json", document)
    return run


def make_judged_run(root, judged, case=JUDGED_CASE):
    """A run whose only case is judged, so no probe and no matrix take part in it."""
    return make_run(root, case=case, requirements=requirements_document(case, group="G2"),
                    classify=classify_document(case, kind="judged"), matrix=None, judged=judged)


def run_main(module, monkeypatch, run):
    """The module's CLI, on one run folder."""
    monkeypatch.setattr(sys, "argv", ["verdict.py", "--run", str(run)])
    return module.main()


def case_of(verdict, case=CASE):
    """One case's row, so a failure says which case."""
    return next(entry for entry in verdict["cases"] if entry["case"] == case)


def requirement_of(verdict, requirement_id):
    """One requirement's row, so a failure says which requirement."""
    return next(entry for entry in verdict["requirements"] if entry["id"] == requirement_id)


def test_a_case_with_no_recorded_evidence_is_unknown_and_never_pass(tmp_path):
    """EV-P1.1 — a requirement with no evidence given PASS is the builder's own claim, called a verdict."""
    module = load_verdict()
    run = make_run(tmp_path, classify=None, matrix=None, confirm=None, judged=None)
    verdict = module.decide(run)
    case = case_of(verdict)
    assert case["verdict"] == "UNKNOWN"
    assert case["reason"]
    assert [entry["verdict"] for entry in verdict["requirements"]] == ["UNKNOWN"]
    assert verdict["meets"] is False


def test_a_green_probe_that_its_own_mutant_kills_passes(tmp_path):
    """EV-P1.1 — PASS has to mean the probe is green on the product and red on that case's mutant."""
    module = load_verdict()
    verdict = module.decide(make_run(tmp_path))
    case = case_of(verdict)
    assert (case["kind"], case["verdict"]) == ("executable", "PASS")
    assert case["reason"] == "" and case["repro"] == ""
    assert [entry["verdict"] for entry in verdict["requirements"]] == ["PASS"]
    assert verdict["meets"] is True
    assert verdict["counts"] == {"PASS": 1, "FAIL": 0, "UNKNOWN": 0, "out_of_scope": 0}


def test_an_executable_case_no_probe_cites_is_unknown(tmp_path):
    """EV-C2.2 — an executable or static case with no probe and no UNKNOWN is a requirement nobody checked."""
    module = load_verdict()
    matrix = matrix_document({}, {RED_PROBE: "pass"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    case = case_of(module.decide(make_run(tmp_path, matrix=matrix)))
    assert case["verdict"] == "UNKNOWN"
    assert "no probe" in case["reason"].lower()


def test_a_missing_or_invalid_mutant_leaves_the_case_unknown(tmp_path):
    """EV-C3.2 — a case whose mutant was never applied can be green for anything, so PASS would prove nothing."""
    module = load_verdict()
    for index, mutants in enumerate([{}, {CASE: {"status": "invalid", "results": {}}}]):
        matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "pass"}, mutants)
        case = case_of(module.decide(make_run(tmp_path / f"case-{index}", matrix=matrix)))
        assert case["verdict"] == "UNKNOWN", mutants
        assert "mutant" in case["reason"].lower(), mutants


def test_a_probe_that_stays_green_on_its_mutant_is_unproven(tmp_path):
    """EV-C3.2 — a probe that never went red on the broken copy cannot carry a PASS."""
    module = load_verdict()
    mutants = {CASE: {"status": "applied", "results": {RED_PROBE: "pass"}}}
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "pass"}, mutants)
    verdict = module.decide(make_run(tmp_path, matrix=matrix))
    case = case_of(verdict)
    assert case["verdict"] == "UNKNOWN"
    assert "unproven" in case["reason"].lower()
    assert verdict["meets"] is False


def test_a_red_probe_that_was_not_confirmed_faithful_is_unknown_not_fail(tmp_path):
    """EV-C4.2 — a FAIL on an unconfirmed probe reports a defect the requirement never had."""
    module = load_verdict()
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "fail"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    unfaithful = {"cases": [dict(FAITHFUL, faithful=False)]}
    for index, confirm in enumerate([unfaithful, None]):
        case = case_of(module.decide(make_run(tmp_path / f"case-{index}", matrix=matrix, confirm=confirm)))
        assert case["verdict"] == "UNKNOWN", confirm
        assert "faithful" in case["reason"].lower(), confirm
        assert case["repro"] == "", confirm


def test_a_confirmed_red_probe_fails_with_the_command_that_shows_it(tmp_path):
    """EV-P1.1 EV-C4.2 — a FAIL with no repro is a claim; the repro is the command that shows the same red."""
    module = load_verdict()
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "fail"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    verdict = module.decide(make_run(tmp_path, matrix=matrix, confirm={"cases": [FAITHFUL]}))
    case = case_of(verdict)
    assert case["verdict"] == "FAIL"
    assert case["repro"].startswith("EVAL_PRODUCT=")
    assert "test_red" in case["repro"]
    assert requirement_of(verdict, "B1.1")["verdict"] == "FAIL"
    assert verdict["counts"]["FAIL"] == 1
    assert verdict["meets"] is False


def test_a_label_with_no_reason_makes_the_case_human(tmp_path):
    """EV-C1.2 — a forced label with no reason behind it is a guess, and a guess must not reach the verdict."""
    module = load_verdict()
    unconfident = [{"case": CASE, "kind": "executable", "reason": ""},
                   {"case": CASE, "kind": "executable"},
                   {"case": CASE, "kind": "executable", "reason": "   "}]
    for index, entry in enumerate(unconfident):
        case = case_of(module.decide(make_run(tmp_path / f"case-{index}", classify={"cases": [entry]})))
        assert case["verdict"] == "UNKNOWN", entry
        assert "EJ" in case["reason"], entry
    human = {"cases": [{"case": CASE, "kind": "human", "reason": "only EJ can tell"}]}
    assert case_of(module.decide(make_run(tmp_path / "human", classify=human)))["kind"] == "human"


def test_a_missed_plant_voids_the_judging(tmp_path):
    """EV-C5.2 — a judging that missed its planted defect read nothing, so its answers are not verdicts."""
    module = load_verdict()
    judged = {"plant_found": False, "cases": [{"case": JUDGED_CASE, "holds": True, "evidence": EVIDENCE}]}
    verdict = module.decide(make_judged_run(tmp_path, judged))
    case = case_of(verdict, JUDGED_CASE)
    assert case["verdict"] == "UNKNOWN"
    assert "plant" in case["reason"].lower()
    assert requirement_of(verdict, "G2.1")["verdict"] == "UNKNOWN"
    assert verdict["meets"] is False


def test_a_judged_case_passes_when_it_holds_and_fails_with_the_quote_when_it_does_not(tmp_path):
    """EV-C5.2 — a judged FAIL's repro is the quoted file:line, so the reader can open the code that broke."""
    module = load_verdict()
    for index, holds in enumerate([True, False]):
        judged = {"plant_found": True, "cases": [{"case": JUDGED_CASE, "holds": holds, "evidence": EVIDENCE}]}
        case = case_of(module.decide(make_judged_run(tmp_path / f"case-{index}", judged)), JUDGED_CASE)
        assert case["verdict"] == ("PASS" if holds else "FAIL"), holds
        assert case["repro"] == ("" if holds else EVIDENCE), holds
        if holds:
            assert case["reason"] == "", holds


def test_a_judged_case_with_no_judging_entry_is_unknown(tmp_path):
    """EV-C5.2 — a judged case nobody judged is not a yes, and reporting it PASS would be one."""
    module = load_verdict()
    verdict = module.decide(make_judged_run(tmp_path, {"plant_found": True, "cases": []}))
    case = case_of(verdict, JUDGED_CASE)
    assert case["verdict"] == "UNKNOWN"
    assert "judged" in case["reason"].lower()


def test_an_untestable_group_is_unknown_with_that_reason(tmp_path):
    """EV-P1.1 — an untestable group reported as anything but UNKNOWN hides a requirement nobody could check."""
    module = load_verdict()
    requirements = requirements_document(CASE, status="untestable")
    requirements["groups"][0]["cases"] = []
    requirements["groups"][0]["fails_if"] = ""
    verdict = module.decide(make_run(tmp_path, requirements=requirements))
    assert verdict["cases"] == []
    entry = requirement_of(verdict, "B1.1")
    assert entry["verdict"] == "UNKNOWN"
    assert "untestable" in entry["reason"].lower()
    assert verdict["meets"] is False


def test_an_open_id_gets_no_verdict_and_is_listed_out_of_scope(tmp_path):
    """EV-P1.1 — an open requirement given a verdict settles, by script, what EJ has not settled."""
    module = load_verdict()
    requirements = requirements_document(CASE, ids=["B1.1", "B1.2"], open_ids=["B1.2"])
    verdict = module.decide(make_run(tmp_path, requirements=requirements))
    assert [entry["id"] for entry in verdict["requirements"]] == ["B1.1"]
    assert requirement_of(verdict, "B1.1")["verdict"] == "PASS"
    assert verdict["out_of_scope"] == ["B1.2"]
    assert verdict["counts"]["out_of_scope"] == 1
    assert verdict["meets"] is True


def test_a_vision_id_takes_the_verdict_of_its_single_case(tmp_path):
    """EV-P1.1 — a vision line left out of the verdict is a promise the run never checked."""
    module = load_verdict()
    vision = [{"id": "V1", "section": "never", "text": "Never guesses.",
               "cases": [{"case": "V1-F1", "text": "Never guesses."}]}]
    requirements = requirements_document(CASE, vision=vision)
    classify = {"cases": [{"case": CASE, "kind": "executable", "reason": "run the probe"},
                          {"case": "V1-F1", "kind": "human", "reason": "only EJ can tell"}]}
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "pass"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    verdict = module.decide(make_run(tmp_path, requirements=requirements, classify=classify, matrix=matrix))
    assert case_of(verdict, "V1-F1")["verdict"] == "UNKNOWN"
    assert requirement_of(verdict, "B1.1")["verdict"] == "PASS"
    assert verdict["manifest"] == ["B1.1", "V1"]
    assert verdict["meets"] is False


def test_a_product_copy_that_was_not_restored_makes_every_case_unknown(tmp_path):
    """EV-P1.1 — a PASS over bytes the run left broken measures a product that does not exist."""
    module = load_verdict()
    matrix = default_files()["matrix"]
    matrix["restored"] = False
    verdict = module.decide(make_run(tmp_path, matrix=matrix))
    assert [case["verdict"] for case in verdict["cases"]] == ["UNKNOWN"]
    assert "restored" in verdict["cases"][0]["reason"].lower()
    assert verdict["meets"] is False


def test_meets_needs_every_in_scope_id_to_pass(tmp_path):
    """EV-P1.2 — MEETS given with one UNKNOWN calls the whole product met on the strength of a case nobody read."""
    module = load_verdict()
    names = ("B1", "B2", "B3")
    requirements = several_groups(*[(name, [f"{name}.1"], []) for name in names])
    matrix = matrix_document({RED_PROBE: [f"{name}-F1" for name in names]}, {RED_PROBE: "pass"},
                             {f"{name}-F1": {"status": "applied", "results": {RED_PROBE: "fail"}}
                              for name in names})

    def classify(reason):
        return {"cases": [{"case": f"{name}-F1", "kind": "executable", "reason": reason} for name in names]}

    unlabelled = module.decide(make_run(tmp_path / "unlabelled", requirements=requirements,
                                        classify=classify(""), matrix=matrix))
    assert unlabelled["meets"] is False
    assert unlabelled["counts"] == {"PASS": 0, "FAIL": 0, "UNKNOWN": 3, "out_of_scope": 0}
    assert {entry["verdict"] for entry in unlabelled["requirements"]} == {"UNKNOWN"}
    labelled = module.decide(make_run(tmp_path / "labelled", requirements=requirements,
                                      classify=classify("run the probe"), matrix=matrix))
    assert labelled["meets"] is True
    assert labelled["counts"] == {"PASS": 3, "FAIL": 0, "UNKNOWN": 0, "out_of_scope": 0}


def test_the_verdict_is_computed_by_the_script_from_the_recorded_results(tmp_path, monkeypatch):
    """EV-P1.3 — a verdict that changes between two runs over the same files was written, not computed."""
    module = load_verdict()
    run = make_run(tmp_path)
    assert module.decide(run) == module.decide(run)
    assert run_main(module, monkeypatch, run) == 0
    first = (run / "verdict.md").read_bytes()
    assert run_main(module, monkeypatch, run) == 0
    assert (run / "verdict.md").read_bytes() == first
    assert json.loads((run / "verdict.json").read_text(encoding="utf-8")) == module.decide(run)


def test_a_run_writes_the_verdict_files_and_the_coverage_manifest(tmp_path, monkeypatch):
    """EV-P2.1 — a run with no readable report, or a manifest missing an id, leaves the verdict uncheckable."""
    module = load_verdict()
    requirements = requirements_document(CASE, ids=["B1.1", "B1.2"], open_ids=["B1.2"])
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "fail"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    run = make_run(tmp_path, requirements=requirements, matrix=matrix, confirm={"cases": [FAITHFUL]})
    assert run_main(module, monkeypatch, run) == 0
    written = json.loads((run / "verdict.json").read_text(encoding="utf-8"))
    report = (run / "verdict.md").read_text(encoding="utf-8")
    assert written["manifest"] == ["B1.1", "B1.2"]
    assert written["out_of_scope"] == ["B1.2"]
    for requirement_id in ("B1.1", "B1.2"):
        assert requirement_id in report
    assert case_of(written)["repro"] in report


def test_verdict_md_leads_with_the_answer_then_the_fail_unknown_pass_rows(tmp_path, monkeypatch):
    """EV-P2.2 — a report that lists the PASSes first buries the one requirement that failed."""
    module = load_verdict()
    requirements = several_groups(("B1", ["B1.1"], []), ("B2", ["B2.1"], []), ("B3", ["B3.1", "B3.2"], ["B3.2"]))
    matrix = matrix_document({RED_PROBE: ["B1-F1"], GREEN_PROBE: ["B3-F1"]},
                             {RED_PROBE: "fail", GREEN_PROBE: "pass"},
                             {"B1-F1": {"status": "applied", "results": {RED_PROBE: "fail"}},
                              "B3-F1": {"status": "applied", "results": {GREEN_PROBE: "fail"}}})
    classify = {"cases": [{"case": f"{name}-F1", "kind": "executable", "reason": "run the probe"}
                          for name in ("B1", "B2", "B3")]}
    run = make_run(tmp_path, requirements=requirements, classify=classify, matrix=matrix,
                   confirm={"cases": [FAITHFUL]})
    assert run_main(module, monkeypatch, run) == 0
    report = (run / "verdict.md").read_text(encoding="utf-8")
    lines = report.splitlines()
    assert lines[0].startswith("MEETS: ") and lines[0].rstrip().endswith("no")
    assert all(word in "\n".join(lines[:5]) for word in ("PASS", "FAIL", "UNKNOWN"))
    assert case_of(module.decide(run))["repro"] in report
    assert requirement_of(module.decide(run), "B2.1")["reason"] in report
    assert report.index("B1.1") < report.index("B2.1") < report.index("B3.1") < report.index("B3.2")


def test_a_run_without_a_requirements_file_exits_two_with_a_problem_line(tmp_path, monkeypatch, capsys):
    """EV-P2.1 — a report with no requirements in it can answer nothing, so the run stops with exit 2."""
    module = load_verdict()
    run = make_run(tmp_path, requirements=None)
    assert run_main(module, monkeypatch, run) == 2
    err = capsys.readouterr().err
    assert "requirements.json" in err
    assert "Traceback" not in err