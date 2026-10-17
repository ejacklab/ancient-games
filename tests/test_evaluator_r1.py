"""Tests for Repair R1 — the 20 blind-review findings, written before the code changes.

DATA.md's "Repair R1" and "The workflow after R1" say what each finding must hold. This file holds the three evaluator
modules to those rules (`verdict.py`, `workspace.py`, `model_io.py`); `.claude/workflows/evaluate-requirements.js` is
held to them by `tests/workflows/evaluate_harness.mjs`. Every docstring starts with its finding id, `R1-F<n>`, so a
failure says which rule was undone.

House style: the helpers come from `test_evaluator_verdict.py`, `test_evaluator_workspace.py` and
`test_evaluator_model_io.py`, as `test_evaluator_k1_regressions.py` does, so each rule is tested over the same small
hand-written inputs the older tests use and no test depends on a step that has not been written down. A rule that
already holds in today's code is guarded by a test that passes today; the hand-back names those.
"""
from __future__ import annotations

import json
import re
import shlex
import shutil
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from test_evaluator_model_io import (CALL_ONE_MISSED, CALL_TWO_FOUND, CALC, CONFIRMED, REQUIREMENTS, build_run,
                                     cli_ok, read, run_model_io)
from test_evaluator_verdict import (CASE, EVIDENCE, FAITHFUL, GREEN_PROBE, JUDGED_CASE, RED_PROBE, case_of,
                                    classify_document, load_verdict, make_judged_run, make_run, matrix_document,
                                    requirement_of, requirements_document, run_main, several_groups, write_json)
from test_evaluator_workspace import (build as build_run_folder, build_product, build_spec, load_workspace)

REPO_RUNS = Path(__file__).resolve().parents[1] / "runs"
ABSENT = object()  # "this key is not in the document at all", which is not the same as its value being null

# Every file and folder F10 names as evidence a previous run left behind.
STALE_OUTPUT = ["classify.json", "probes", "mutants.json", "plants.json", "matrix.json", "confirm.json",
                "judge-1.json", "judge-2.json", "verdict.json"]

# F8's defaults: these names are the product's tests at any depth, whatever the depth.
DEEP_TESTS = {
    "src/tests/inner.py": "the builder's tests, one folder down\n",
    "pkg/test/inner.py": "singular, one folder down\n",
    "top/conftest.py": "a pytest fixture file\n",
    "top/helper_test.py": "a test file with the suffix\n",
    "top/test_helper.py": "a test file with the prefix\n",
    "test_at_the_root.py": "a test file at the root\n",
    "src/runs/20260101-old/notes.md": "an earlier run, nested\n",
    "src/__pycache__/app.cpython-311.pyc": "not really compiled\n",
    "pkg/.git/config": "[core]\n",
}
KEPT_BY_THE_DEFAULTS = {
    "pkg/spec/keep.py": "the product's own code\n",
    "docs/keep.md": "a build note the run was not told to leave out\n",
}


def with_keys(document: dict, overrides: dict) -> dict:
    """A copy of a recorded document with `overrides` applied; ABSENT removes a key."""
    updated = dict(document)
    for key, value in overrides.items():
        if value is ABSENT:
            updated.pop(key, None)
        else:
            updated[key] = value
    return updated


def names_entry(problem: str, filename: str, index: int) -> bool:
    """Whether an input_problems line names `filename`'s entry at `index` (counted from 0)."""
    match = re.fullmatch(rf"{re.escape(filename)}: entry (\d+): .+", str(problem))
    return bool(match) and int(match.group(1)) in (index, index + 1)


def run_folder_named(root, name="20261013-r1", **overrides):
    """make_run's folder under a realistic runId, so `run=` in the MEETS line has something to say."""
    renamed = Path(root) / name
    make_run(root, **overrides).rename(renamed)
    return renamed


@pytest.fixture
def run_in_runs():
    """A run folder inside the repository's own runs/, which is where F12 says --run has to point, removed after."""
    folder = REPO_RUNS / f"r1-test-{uuid.uuid4().hex[:10]}"
    folder.mkdir(parents=True)
    try:
        yield folder
    finally:
        shutil.rmtree(folder, ignore_errors=True)


@pytest.fixture
def judge_run(tmp_path):
    """One small run folder with a unique name, so the judge folder F2 builds is this test's own, removed after."""
    built = build_run(tmp_path)
    run = tmp_path / f"eval-{uuid.uuid4().hex[:10]}"
    built.rename(run)
    shutil.rmtree(judge_folder(run), ignore_errors=True)
    yield run
    shutil.rmtree(judge_folder(run), ignore_errors=True)


def judge_folder(run: Path) -> Path:
    """The folder F2 builds for call 1: outside the run folder, named after the runId."""
    return Path("/tmp") / f"evaluator-judge-{Path(run).name}"


def plant_case(run: Path):
    """Which case the run planted, read from the coordinator's own file by whatever key it uses."""
    written = json.loads((Path(run) / ".coordinator/plant.json").read_text(encoding="utf-8"))
    if isinstance(written, dict):
        for key in ("plant_case", "case", "plant"):
            if key in written:
                return written[key]
    return written


def confirm_run(root, answers):
    """build_run's folder, confirm-input's real output, then the confirm agent's own answers."""
    run = build_run(root)
    cli_ok("confirm-input", run)
    write_json(run / "confirm.json", {"cases": answers})
    return run


def utc(text) -> datetime:
    """The instant a stamp recorded, insisting it says UTC rather than local time or nothing."""
    parsed = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    assert parsed.utcoffset() == timedelta(0), f"{text!r} is not a UTC time"
    return parsed


# --- R1-F1: MEETS needs something to be about ---------------------------------------------------

def test_meets_is_false_when_there_is_no_in_scope_requirement_at_all(tmp_path):
    """R1-F1 — zero in-scope ids gave MEETS: yes, because all([]) is true: a vacuous yes is still a yes."""
    module = load_verdict()
    every_id_open = requirements_document(CASE, ids=["B1.1", "B1.2"], open_ids=["B1.1", "B1.2"])
    empty_spec = {"spec": {"requirements": "spec/REQUIREMENTS.md", "vision": None},
                  "groups": [], "vision": [], "manifest": []}
    for index, (requirements, out_of_scope) in enumerate([(every_id_open, 2), (empty_spec, 0)]):
        verdict = module.decide(make_run(tmp_path / f"case-{index}", requirements=requirements))
        assert verdict["requirements"] == [], requirements
        assert verdict["meets"] is False, requirements
        assert verdict["meets_reason"] == "no in-scope requirements", verdict.get("meets_reason")
        assert verdict["counts"]["out_of_scope"] == out_of_scope, verdict["counts"]


def test_meets_true_says_nothing_against_itself(tmp_path):
    """R1-F1 — the guard on F1's own fix: one requirement that really is PASS still reads as MEETS."""
    module = load_verdict()
    verdict = module.decide(make_run(tmp_path))
    assert verdict["meets"] is True
    assert not verdict.get("meets_reason"), verdict.get("meets_reason")
    assert verdict["counts"] == {"PASS": 1, "FAIL": 0, "UNKNOWN": 0, "out_of_scope": 0}


# --- R1-F4: the product copy has to be provably intact -------------------------------------------

def test_a_matrix_that_does_not_prove_the_copy_is_intact_blocks_every_probe_case(tmp_path):
    """R1-F4 — `restored is False` read a missing or null restored as intact, so a broken copy gave a PASS."""
    module = load_verdict()
    healthy = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "pass"},
                              {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}}, restored=True)
    broken = [("restored is not in the matrix at all", {"restored": ABSENT}),
              ("restored is null", {"restored": None}),
              ("restored is the word, not the boolean", {"restored": "true"}),
              ("the product run changed a file of the copy", {"restored": True, "product_changed": True})]
    for index, (shape, overrides) in enumerate(broken):
        verdict = module.decide(make_run(tmp_path / f"case-{index}", matrix=with_keys(healthy, overrides)))
        assert verdict["meets"] is False, shape
        for case in verdict["cases"]:
            assert case["verdict"] == "UNKNOWN", (shape, case)
            assert case["reason"] == "product copy not restored or changed", (shape, case["reason"])
            assert case["repro"] == "", shape


def test_an_intact_copy_with_nothing_changed_still_gives_a_pass(tmp_path):
    """R1-F4 — the guard on F4's own fix: an explicit restored true and product_changed false is proof enough."""
    module = load_verdict()
    matrix = with_keys(matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "pass"},
                                       {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}}),
                       {"restored": True, "product_changed": False})
    verdict = module.decide(make_run(tmp_path, matrix=matrix))
    assert case_of(verdict)["verdict"] == "PASS"
    assert verdict["meets"] is True


def test_a_judged_only_run_with_no_product_copy_is_not_blocked(tmp_path):
    """R1-F4 — a run with no matrix ran no probe over any copy, so there is no copy to prove intact."""
    module = load_verdict()
    judged = {"plant_found": True, "cases": [{"case": JUDGED_CASE, "holds": True, "evidence": EVIDENCE}]}
    verdict = module.decide(make_judged_run(tmp_path, judged))
    assert case_of(verdict, JUDGED_CASE)["verdict"] == "PASS"
    assert verdict["meets"] is True


# --- R1-F5: a mutant run has to have been healthy before it proves anything -----------------------

def mutant_matrix(results: dict, run_status: str, errors: list[str]):
    """matrix.json for one case that is red on its mutant, with the `runs` key F5 adds describing that run."""
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "pass"},
                             {CASE: {"status": "applied", "results": results}})
    matrix["runs"] = {"product": {"status": "ok", "errors": []},
                      CASE: {"status": run_status, "errors": list(errors)}}
    return matrix


def test_a_mutant_run_that_was_ok_with_its_red_probe_outside_the_errors_still_proves(tmp_path):
    """R1-F5 — the guard on F5's own fix: a healthy run that killed one probe is the proof EV-C3.2 asks for."""
    module = load_verdict()
    matrix = mutant_matrix({RED_PROBE: "fail", GREEN_PROBE: "pass"}, "ok", [])
    verdict = module.decide(make_run(tmp_path, matrix=matrix))
    assert case_of(verdict)["verdict"] == "PASS"
    assert verdict["meets"] is True


@pytest.mark.parametrize("status", ["timeout", "no-report"])
def test_a_mutant_run_that_never_answered_is_not_proof(tmp_path, status):
    """R1-F5 — a timeout marks every probe red, and verdict read that red as the mutant's proof."""
    module = load_verdict()
    matrix = mutant_matrix({RED_PROBE: "fail", GREEN_PROBE: "pass"}, status, [])
    verdict = module.decide(make_run(tmp_path, matrix=matrix))
    case = case_of(verdict)
    assert case["verdict"] == "UNKNOWN", matrix["runs"]
    assert case["reason"] == "unproven: the mutant run was not healthy", case["reason"]
    assert verdict["meets"] is False


def test_a_probe_that_ended_in_a_junit_error_is_not_proof(tmp_path):
    """R1-F5 — an error is not the mutant breaking the requirement; it is the probe dying on the way."""
    module = load_verdict()
    matrix = mutant_matrix({RED_PROBE: "fail", GREEN_PROBE: "pass"}, "ok", [RED_PROBE])
    verdict = module.decide(make_run(tmp_path, matrix=matrix))
    case = case_of(verdict)
    assert case["verdict"] == "UNKNOWN", matrix["runs"]
    assert case["reason"] == "unproven: the mutant run was not healthy", case["reason"]


@pytest.mark.parametrize("results", [
    pytest.param({RED_PROBE: "fail", GREEN_PROBE: "fail"}, id="every probe went red, so nothing was proved"),
    pytest.param({RED_PROBE: "fail", GREEN_PROBE: "fail", "test_b9::test_third": "fail"},
                 id="three probes went red, so nothing was proved"),
])
def test_a_mutant_run_that_turned_everything_red_proves_nothing(tmp_path, results):
    """R1-F5 — Dave's guarded rule: a mutant run with 2 or more probes that turns them all red broke the run.

    A run reporting a single probe is not judged by this rule: nothing else went red to show the run itself was
    unhealthy, so `test_a_matrix_with_no_runs_key_is_an_older_matrix_and_still_proves` is its guard.
    """
    module = load_verdict()
    verdict = module.decide(make_run(tmp_path, matrix=mutant_matrix(results, "ok", [])))
    case = case_of(verdict)
    assert case["verdict"] == "UNKNOWN", results
    assert case["reason"] == "unproven: the mutant run was not healthy", case["reason"]


def test_a_matrix_with_no_runs_key_is_an_older_matrix_and_still_proves(tmp_path):
    """R1-F5 — recordings made before F5 carry no run status, so nothing may be taken back from them."""
    module = load_verdict()
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "pass"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    assert "runs" not in matrix
    assert case_of(module.decide(make_run(tmp_path, matrix=matrix)))["verdict"] == "PASS"


# --- R1-F11: a model file of the wrong shape is a fact to report, not a traceback -----------------

def test_a_classify_file_whose_root_is_not_an_object_counts_as_empty(tmp_path, monkeypatch, capsys):
    """R1-F11 — model-written JSON of the wrong shape ended in a traceback at verdict.py:128."""
    module = load_verdict()
    run = make_run(tmp_path, classify=classify_document(CASE)["cases"])
    verdict = module.decide(run)
    assert case_of(verdict)["kind"] == "human", "a root of the wrong type must supply no label at all"
    assert verdict["meets"] is False
    assert run_main(module, monkeypatch, run) == 0
    assert "Traceback" not in capsys.readouterr().err


def test_a_classify_entry_that_is_not_an_object_is_skipped_and_listed(tmp_path):
    """R1-F11 — the dropped entry's position goes in input_problems, so a lost answer cannot pass unnoticed."""
    module = load_verdict()
    classify = {"cases": ["B1-F1", classify_document(CASE)["cases"][0]]}
    verdict = module.decide(make_run(tmp_path, classify=classify))
    assert case_of(verdict)["verdict"] == "PASS", "the sound entry still labels the case"
    assert len(verdict["input_problems"]) == 1, verdict["input_problems"]
    assert names_entry(verdict["input_problems"][0], "classify.json", 0), verdict["input_problems"]


def test_an_entry_with_no_string_case_is_skipped_and_can_only_lower_the_verdict(tmp_path):
    """R1-F11 — a skipped entry never invents a PASS or a FAIL; here it takes the label away and stops there."""
    module = load_verdict()
    classify = {"cases": ["not an object", {"kind": "executable", "reason": "run the probe"},
                          {"case": 7, "kind": "executable", "reason": "run the probe"}]}
    verdict = module.decide(make_run(tmp_path, classify=classify))
    case = case_of(verdict)
    assert case["verdict"] == "UNKNOWN", classify
    assert case["kind"] == "human"
    assert len(verdict["input_problems"]) == 3, verdict["input_problems"]
    assert names_entry(verdict["input_problems"][1], "classify.json", 1), verdict["input_problems"]
    assert names_entry(verdict["input_problems"][2], "classify.json", 2), verdict["input_problems"]


def test_a_confirmation_with_no_probe_is_skipped_so_the_red_probe_is_not_a_fail(tmp_path):
    """R1-F11 — a confirm entry with no probe says nothing about which red probe it answers for."""
    module = load_verdict()
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "fail"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    nameless = {key: value for key, value in FAITHFUL.items() if key != "probe"}
    verdict = module.decide(make_run(tmp_path, matrix=matrix, confirm={"cases": [nameless]}))
    case = case_of(verdict)
    assert case["verdict"] == "UNKNOWN", "an entry with no probe must not confirm anything"
    assert case["repro"] == ""
    assert len(verdict["input_problems"]) == 1, verdict["input_problems"]
    assert names_entry(verdict["input_problems"][0], "confirm.json", 0), verdict["input_problems"]


def test_a_judged_file_with_an_entry_that_is_not_an_object_leaves_the_sound_entry_alone(tmp_path):
    """R1-F11 — one malformed judgement entry does not take the judge's other answers down with it."""
    module = load_verdict()
    judged = {"plant_found": True,
              "cases": [{"case": JUDGED_CASE, "holds": True, "evidence": EVIDENCE}, "not an object"]}
    verdict = module.decide(make_judged_run(tmp_path, judged))
    assert case_of(verdict, JUDGED_CASE)["verdict"] == "PASS"
    assert len(verdict["input_problems"]) == 1, verdict["input_problems"]
    assert names_entry(verdict["input_problems"][0], "judged.json", 1), verdict["input_problems"]


def test_a_confirm_file_whose_root_is_not_an_object_counts_as_empty(tmp_path):
    """R1-F11 — model_io reads the same model files, and a wrong root there was an AttributeError, not an answer."""
    run = build_run(tmp_path)
    cli_ok("confirm-input", run)
    write_json(run / "confirm.json", "not an object at all")
    result = cli_ok("confirm-check", run)
    assert "Traceback" not in result.stderr, result.stderr
    assert read(run / "confirm.json")["cases"] == []


def test_a_judge_answer_whose_root_is_not_an_object_is_dropped_rather_than_crashing(tmp_path):
    """R1-F11 — one bad judgement file ends the judging as unknown, it does not end the run in a traceback."""
    run = build_run(tmp_path)
    cli_ok("judge-input", run)
    write_json(judge_folder(run) / "judge-1.json", ["not an object", {"case": "G2-F1"}])
    write_json(run / "judge-2.json", "not an object at all")
    result = cli_ok("judged-merge", run)
    assert "Traceback" not in result.stderr, result.stderr
    assert read(run / "judged.json")["cases"] == []


# --- R1-F13: the repro is a command, so every part of it has to be quoted -------------------------

@pytest.mark.parametrize("name", ["test red; touch pwned", "test red's name $HOME"])
def test_the_repro_shell_quotes_the_test_file_and_the_test_name(tmp_path, name):
    """R1-F13 — the repro is a command a reader runs; a probe name carrying a shell must not carry a command."""
    module = load_verdict()
    probe = f"test b1; touch pwned::{name}"  # the matrix's own key: module::name
    cited = f"probes/test b1; touch pwned.py::{name}"  # the confirm agent's citation of the same probe
    matrix = matrix_document({probe: [CASE]}, {probe: "fail"},
                             {CASE: {"status": "applied", "results": {probe: "fail"}}})
    verdict = module.decide(make_run(tmp_path, matrix=matrix,
                                     confirm={"cases": [dict(FAITHFUL, probe=cited)]}))
    repro = case_of(verdict)["repro"]
    assert verdict["cases"][0]["verdict"] == "FAIL", "the fixture must reach the repro"
    assert repro.startswith('EVAL_PRODUCT="$PWD"/'), repro
    assert "'probes/test b1; touch pwned.py'" in repro, repro
    assert shlex.quote(name) in repro, repro
    tokens = shlex.split(repro)
    assert tokens[-2] == "-k" and tokens[-1] == name, tokens
    assert "probes/test b1; touch pwned.py" in tokens, tokens


# --- R1-F14: an id the parser could not read blocks MEETS and is named --------------------------

def test_an_id_the_parser_could_not_read_blocks_meets_and_is_named(tmp_path):
    """R1-F14 — an id bullet in a shape the parser skipped left a requirement out of the manifest and the verdict."""
    module = load_verdict()
    requirements = requirements_document(CASE)
    requirements["unparsed_ids"] = ["B1.9", "EV-R2.1:"]
    verdict = module.decide(make_run(tmp_path, requirements=requirements))
    assert requirement_of(verdict, "B1.1")["verdict"] == "PASS", "the ids that were read still stand"
    assert verdict["meets"] is False
    assert "B1.9" in verdict["meets_reason"] and "EV-R2.1" in verdict["meets_reason"], verdict["meets_reason"]


# --- R1-F15: a case labelled twice is a case nobody can vouch for --------------------------------

def test_two_classify_entries_for_one_case_make_it_human(tmp_path):
    """R1-F15 — the last label silently won, so a case the classifier labelled twice was decided on one answer."""
    module = load_verdict()
    first = {"case": "B1-F1", "kind": "executable", "reason": "run the probe"}
    second = {"case": "B1-F1", "kind": "static", "reason": "read one line"}
    matrix = matrix_document({RED_PROBE: ["B1-F1"], GREEN_PROBE: ["B2-F1"]},
                             {RED_PROBE: "pass", GREEN_PROBE: "pass"},
                             {"B1-F1": {"status": "applied", "results": {RED_PROBE: "fail"}},
                              "B2-F1": {"status": "applied", "results": {GREEN_PROBE: "fail"}}})
    requirements = several_groups(("B1", ["B1.1"], []), ("B2", ["B2.1"], []))
    for index, entries in enumerate([[first, second], [first, second, dict(first, kind="judged")]]):
        classify = {"cases": entries + [{"case": "B2-F1", "kind": "executable", "reason": "run the probe"}]}
        verdict = module.decide(make_run(tmp_path / f"case-{index}", requirements=requirements,
                                         classify=classify, matrix=matrix))
        case = case_of(verdict, "B1-F1")
        assert case["kind"] == "human", entries
        assert case["verdict"] == "UNKNOWN", entries
        assert case["reason"] == "classified twice", case["reason"]
        assert case_of(verdict, "B2-F1")["verdict"] == "PASS", "another case was caught by the same rule"
        assert verdict["meets"] is False, entries


# --- R1-F16: an id left out of scope has to say why ----------------------------------------------

def test_out_of_scope_is_a_list_of_ids_with_the_reason_they_left(tmp_path):
    """R1-F16 — an out-of-scope id with no reason reads as a requirement the run dropped on purpose."""
    module = load_verdict()
    requirements = requirements_document(CASE, ids=["B1.1", "B1.2"], open_ids=["B1.2"])
    verdict = module.decide(make_run(tmp_path, requirements=requirements))
    assert [entry["id"] for entry in verdict["out_of_scope"]] == ["B1.2"], verdict["out_of_scope"]
    assert verdict["out_of_scope"][0]["reason"] == "marked open in the spec", verdict["out_of_scope"]
    assert verdict["counts"]["out_of_scope"] == 1, verdict["counts"]
    assert verdict["meets"] is True


def test_verdict_md_gives_each_out_of_scope_id_its_reason(tmp_path, monkeypatch):
    """R1-F16 — the report has to say why an id got no verdict, not only that it got none."""
    module = load_verdict()
    requirements = requirements_document(CASE, ids=["B1.1", "B1.2"], open_ids=["B1.2"])
    run = make_run(tmp_path, requirements=requirements)
    assert run_main(module, monkeypatch, run) == 0
    report = (run / "verdict.md").read_text(encoding="utf-8")
    assert "B1.2" in report and "marked open in the spec" in report, report


# --- R1-F19: the MEETS line names the run it came from -------------------------------------------

def test_the_meets_line_names_the_run_folder_it_came_from(tmp_path, monkeypatch, capsys):
    """R1-F19 — meets was bare text relayed by a runner, and one run's MEETS line reads the same as another's."""
    module = load_verdict()
    passing = run_folder_named(tmp_path / "passing")
    assert run_main(module, monkeypatch, passing) == 0
    assert capsys.readouterr().out.splitlines()[0] == "MEETS: yes run=20261013-r1"
    matrix = matrix_document({RED_PROBE: [CASE]}, {RED_PROBE: "fail"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    failing = run_folder_named(tmp_path / "failing", name="20261013-r1b", matrix=matrix,
                               confirm={"cases": [FAITHFUL]})
    assert run_main(module, monkeypatch, failing) == 0
    assert capsys.readouterr().out.splitlines()[0] == "MEETS: no run=20261013-r1b"


# --- R1-F20: a probe that checks nothing is a probe nobody reported ------------------------------

def test_probes_that_cite_no_case_or_a_case_the_spec_never_read_are_reported_as_orphans(tmp_path):
    """R1-F20 — an orphaned probe was in the matrix and out of the report, so the run's coverage was overstated."""
    module = load_verdict()
    orphans = ["test_b1::test_cites_nothing", "test_b1::test_cites_nowhere"]
    matrix = matrix_document({RED_PROBE: [CASE], orphans[0]: [], orphans[1]: ["B9-F1"]},
                             {RED_PROBE: "pass", orphans[0]: "pass", orphans[1]: "pass"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    verdict = module.decide(make_run(tmp_path, matrix=matrix))
    assert sorted(verdict["orphan_probes"]) == sorted(orphans), verdict["orphan_probes"]
    assert case_of(verdict)["verdict"] == "PASS", "an orphan elsewhere is not this case's business"
    assert verdict["meets"] is True, "a run that measures everything it reads still MEETS"


def test_verdict_md_lists_the_orphan_probes(tmp_path, monkeypatch):
    """R1-F20 — verdict.md is what a reader reads, so the probes that checked nothing are named there too."""
    module = load_verdict()
    orphans = ["test_b1::test_cites_nothing", "test_b1::test_cites_nowhere"]
    matrix = matrix_document({RED_PROBE: [CASE], orphans[0]: [], orphans[1]: ["B9-F1"]},
                             {RED_PROBE: "pass", orphans[0]: "pass", orphans[1]: "pass"},
                             {CASE: {"status": "applied", "results": {RED_PROBE: "fail"}}})
    run = make_run(tmp_path, matrix=matrix)
    assert run_main(module, monkeypatch, run) == 0
    report = (run / "verdict.md").read_text(encoding="utf-8")
    assert all(probe in report for probe in orphans), report


# --- R1-F8: the blind workspace's defaults, and globs that add to them ----------------------------

def test_the_default_exclusions_hold_at_any_depth(tmp_path):
    """R1-F8 — nested tests/, test_*.py, *_test.py and conftest.py were all copied into the blind workspace."""
    module = load_workspace()
    product = build_product(tmp_path)
    for relative, content in {**DEEP_TESTS, **KEPT_BY_THE_DEFAULTS}.items():
        path = product / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    run = tmp_path / "run"
    manifest = module.build_workspace(product, build_spec(tmp_path), run, excludes=None)
    copied = run / "workspace/product"
    for relative in DEEP_TESTS:
        assert not (copied / relative).exists(), relative
        assert relative not in manifest["copied"], relative
    for relative in KEPT_BY_THE_DEFAULTS:
        assert (copied / relative).is_file(), relative
        assert relative in manifest["copied"], relative


def test_an_exclude_glob_adds_to_the_defaults_it_no_longer_replaces(tmp_path):
    """R1-F8 — --exclude replaced the defaults, so one glob for a build note brought the product's tests back."""
    module = load_workspace()
    run, manifest = build_run_folder(module, tmp_path, excludes=["*.log"])
    copied = run / "workspace/product"
    assert not (copied / "notes.log").exists()
    assert "notes.log" in manifest["excluded"]
    assert not (copied / "tests").exists(), "one --exclude turned the product's tests back on"
    assert "tests/MARKER.txt" not in manifest["copied"]
    assert (copied / "src/app.py").is_file()


def test_the_cli_takes_one_exclude_per_glob_and_keeps_the_defaults(run_in_runs, tmp_path):
    """R1-F8 — the workflow passes one --exclude per glob, so several have to survive the command line."""
    module = load_workspace()
    product = build_product(tmp_path)
    (product / "vendor").mkdir()
    (product / "vendor/lib.py").write_text("vendored = True\n", encoding="utf-8")
    spec = build_spec(tmp_path)
    exit_code = module.main(["--product", str(product), "--spec", str(spec), "--run", str(run_in_runs),
                             "--exclude", "*.log", "--exclude", "vendor"])
    assert exit_code == 0
    copied = run_in_runs / "workspace/product"
    assert not (copied / "notes.log").exists() and not (copied / "vendor").exists()
    assert not (copied / "tests").exists(), "the defaults were replaced again"
    assert (copied / "src/app.py").is_file()


# --- R1-F10: a rerun never reuses another run's evidence -----------------------------------------

@pytest.mark.parametrize("artefact", STALE_OUTPUT)
def test_a_run_folder_that_already_holds_model_output_is_refused(artefact, run_in_runs, tmp_path, capsys):
    """R1-F10 — a rerun on the same runId kept the previous run's answers, so 'wrote no file' never fired."""
    module = load_workspace()
    product = build_product(tmp_path)
    spec = build_spec(tmp_path)
    (run_in_runs / artefact).mkdir(parents=True, exist_ok=True)
    exit_code = module.main(["--product", str(product), "--spec", str(spec), "--run", str(run_in_runs)])
    assert exit_code == 2, f"{artefact} is stale evidence and the run carried on"
    err = capsys.readouterr().err
    assert "use a new runId" in err, err
    assert "Traceback" not in err, err


def test_a_run_folder_holding_only_its_own_workspace_is_accepted(run_in_runs, tmp_path):
    """R1-F10 — the guard on F10's own fix: a fresh runId builds, and a second workspace is a normal rerun."""
    module = load_workspace()
    product = build_product(tmp_path)
    spec = build_spec(tmp_path)
    argv = ["--product", str(product), "--spec", str(spec), "--run", str(run_in_runs)]
    assert module.main(argv) == 0
    assert (run_in_runs / "workspace/product/src/app.py").is_file()
    assert module.main(argv) == 0, "the workspace this step writes is not another run's evidence"


# --- R1-F12: --run has to point inside the repository's runs/ ------------------------------------

def test_a_run_folder_outside_the_repositorys_runs_is_refused(tmp_path, capsys):
    """R1-F12 — --run pointed anywhere at all wrote outside runs/, against EV-R3.2."""
    module = load_workspace()
    product = build_product(tmp_path)
    spec = build_spec(tmp_path)
    assert module.main(["--product", str(product), "--spec", str(spec), "--run", str(tmp_path / "elsewhere")]) == 2
    err = capsys.readouterr().err
    assert "runs" in err, err
    assert "Traceback" not in err, err
    assert not (tmp_path / "elsewhere/workspace").exists(), "the copy was made anyway"


def test_a_run_folder_that_symlinks_out_of_runs_is_refused(run_in_runs, tmp_path, capsys):
    """R1-F12 — symlinks are resolved, so a link that sits inside runs/ is not a way out of it."""
    module = load_workspace()
    product = build_product(tmp_path)
    spec = build_spec(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    link = run_in_runs / "linked"
    link.symlink_to(outside, target_is_directory=True)
    assert module.main(["--product", str(product), "--spec", str(spec), "--run", str(link)]) == 2
    assert "Traceback" not in capsys.readouterr().err
    assert not (outside / "workspace").exists(), "the copy was made through the link"


def test_a_run_folder_inside_the_repositorys_runs_is_accepted(run_in_runs, tmp_path):
    """R1-F12 — the guard on F12's own fix: the folder the workflow names is exactly where runs live."""
    module = load_workspace()
    product = build_product(tmp_path)
    spec = build_spec(tmp_path)
    assert module.main(["--product", str(product), "--spec", str(spec), "--run", str(run_in_runs)]) == 0
    assert (run_in_runs / "workspace/manifest.json").is_file()


# --- R1-F2: the judge is given a folder, not the run and not the plant ----------------------------

def test_the_judge_gets_its_own_folder_outside_the_run_and_is_not_told_the_plant(judge_run):
    """R1-F2 — judge-input.json named plant_case, so the judge could read the answer out of its own input."""
    result = cli_ok("judge-input", judge_run)
    folder = judge_folder(judge_run)
    assert folder.is_dir(), f"{folder} is not there: {result.stdout}{result.stderr}"
    given = read(folder / "judge-input.json")
    assert "plant_case" not in given, given.keys()
    assert sorted(entry["case"] for entry in given["cases"]) == ["G2-F1", "G2-F2", "G2-F3"]
    planted = (folder / "product/calc.py").read_text(encoding="utf-8")
    assert "return a - b" in planted and "return a + b" not in planted, repr(planted)
    if (judge_run / "judge-input.json").exists():
        assert "plant_case" not in read(judge_run / "judge-input.json")
    assert (judge_run / "workspace/product/calc.py").read_text(encoding="utf-8") == CALC, "EV-R3.2"


def test_the_plant_identity_lives_only_in_the_coordinators_own_folder(judge_run):
    """R1-F2 — the run still has to know which case it planted, but only in a folder the judge is never given."""
    cli_ok("judge-input", judge_run)
    plant = judge_run / ".coordinator/plant.json"
    assert plant.is_file(), sorted(str(path) for path in judge_run.rglob("plant*.json"))
    assert plant_case(judge_run) == "G2-F2", "the fixture's first valid plant is G2-F2's"


def test_judged_merge_reads_call_one_from_the_judge_folder_and_keeps_it_as_evidence(judge_run):
    """R1-F2 — call 1's answer lives in the judge folder, so the merge reads it there and copies it in."""
    cli_ok("judge-input", judge_run)
    folder = judge_folder(judge_run)
    write_json(folder / "judge-1.json", CALL_ONE_MISSED)
    write_json(judge_run / "judge-2.json", CALL_TWO_FOUND)
    result = cli_ok("judged-merge", judge_run)
    assert result.stdout.strip() == "plant_found: true", result.stdout
    judged = read(judge_run / "judged.json")
    assert sorted(entry["case"] for entry in judged["cases"]) == ["G2-F1", "G2-F2"], judged
    assert (judge_run / "judge-1.json").is_file(), "call 1's answer was not kept in the run folder as evidence"
    assert read(judge_run / "judge-1.json") == CALL_ONE_MISSED


# --- R1-F6: the count that decides whether the probes are repaired -------------------------------

def test_confirm_check_counts_the_models_own_unfaithful_answers_apart_from_the_voided_ones(tmp_path):
    """R1-F6 — the repair round turns on <u>, so it must count what the model said, not what the script voided."""
    answers = [CONFIRMED[0],                                    # faithful, with quotes that hold
               dict(CONFIRMED[1], faithful=False),               # the model itself said not faithful
               dict(CONFIRMED[0], requirement_quote="a line nobody wrote")]  # voided by the script
    result = cli_ok("confirm-check", confirm_run(tmp_path, answers))
    assert result.stdout.strip() == "3 checked, 1 voided, 1 unfaithful", result.stdout


def test_confirm_check_does_not_count_a_voided_answer_as_the_models_own(tmp_path):
    """R1-F6 — a void is the script's own finding; counting it would start a repair round out of a quote typo."""
    answers = [dict(CONFIRMED[0], requirement_quote="a line nobody wrote"),
               dict(CONFIRMED[1], probe_quote="a line the probe does not hold")]
    result = cli_ok("confirm-check", confirm_run(tmp_path, answers))
    assert result.stdout.strip() == "2 checked, 2 voided, 0 unfaithful", result.stdout


def test_a_run_where_every_confirmation_holds_reports_no_unfaithful_answer(tmp_path):
    """R1-F6 — the guard on F6's own fix: nothing unfaithful means no repair round, and says so in the count."""
    result = cli_ok("confirm-check", confirm_run(tmp_path, list(CONFIRMED)))
    assert result.stdout.strip() == "2 checked, 0 voided, 0 unfaithful", result.stdout


# --- R1-F7: the rerun with a second plant ------------------------------------------------------

def test_the_first_attempt_takes_the_first_valid_plant_in_case_order(judge_run):
    """R1-F7 — attempt 1 is now named on the command line, so the run's first plant is chosen explicitly."""
    result = cli_ok("judge-input", judge_run, "--attempt", "1")
    assert "3 to judge" in result.stdout, result.stdout
    assert plant_case(judge_run) == "G2-F2"


def test_the_second_attempt_takes_the_next_plant_not_the_first_one_again(judge_run):
    """R1-F7 — a rerun on the same plant would miss it twice; the second attempt moves to the next case's plant."""
    write_json(judge_run / "plants.json",
               [{"case": "G2-F1", "file": "calc.py", "old": 'return ""', "new": "return None"},
                {"case": "G2-F2", "file": "calc.py", "old": "return a + b", "new": "return a - b"}])
    cli_ok("judge-input", judge_run, "--attempt", "1")
    assert plant_case(judge_run) == "G2-F1"
    second = cli_ok("judge-input", judge_run, "--attempt", "2")
    assert plant_case(judge_run) == "G2-F2", "the second attempt planted the first attempt's plant again"
    assert "G2-F2" in second.stdout, second.stdout


def test_a_second_attempt_with_no_other_plant_says_so_and_changes_nothing(judge_run):
    """R1-F7 — with nothing else to plant, the run keeps its first result rather than rerun on the same plant."""
    cli_ok("judge-input", judge_run, "--attempt", "1")
    before = read(judge_run / ".coordinator/plant.json")
    result = cli_ok("judge-input", judge_run, "--attempt", "2")
    assert "no other plant" in result.stdout, result.stdout
    assert plant_case(judge_run) == "G2-F2"
    assert read(judge_run / ".coordinator/plant.json") == before


# --- R1-F9: the mutant writer's folder ----------------------------------------------------------

def test_the_mutant_view_is_the_workspace_without_the_probes(judge_run):
    """R1-F9 — Codex wrote mutants with the probes in its folder, which is how it saw what the probes assert."""
    result = cli_ok("mutant-view", judge_run)
    view = judge_run / "mutant-view"
    assert view.is_dir(), f"{view} is not there: {result.stdout}{result.stderr}"
    assert (view / "workspace/product/calc.py").read_text(encoding="utf-8") == CALC
    assert "**G2 — The judge**" in (view / "workspace/spec/REQUIREMENTS.md").read_text(encoding="utf-8")
    assert not (view / "probes").exists()
    assert not list(view.rglob("test_*.py")), sorted(str(path) for path in view.rglob("*") if path.is_file())


def test_collecting_the_mutant_view_copies_both_files_back_into_the_run(judge_run):
    """R1-F9 — Codex's writes land in the view; the run reads its mutants and plants from the run folder."""
    cli_ok("mutant-view", judge_run)
    view = judge_run / "mutant-view"
    mutants = [{"case": "B1-F1", "file": "calc.py", "old": "return a + b", "new": "return a - b"}]
    plants = [{"case": "G2-F2", "file": "calc.py", "old": "return a + b", "new": "return a * b"}]
    write_json(view / "mutants.json", mutants)
    write_json(view / "plants.json", plants)
    cli_ok("mutant-view", judge_run, "--collect")
    assert read(judge_run / "mutants.json") == mutants
    assert read(judge_run / "plants.json") == plants


# --- R1-F17: a model step that returns done and writes nothing usable ----------------------------

CHECK_OUTPUT = [
    pytest.param("classify", {"classify.json": {"cases": [{"case": "B1-F1", "kind": "executable"}]}}, 0,
                 id="classify.json is an object with a cases list"),
    pytest.param("classify", {}, 1, id="classify.json is missing"),
    pytest.param("classify", {"classify.json": []}, 1, id="classify.json is a list, not an object"),
    pytest.param("classify", {"classify.json": {}}, 1, id="classify.json has no cases at all"),
    pytest.param("classify", {"classify.json": {"cases": {}}}, 1, id="cases is not a list"),
    pytest.param("probes", {"probes/test_b1.py": '"""B1-F1 — one."""\n'}, 0, id="one probe was written"),
    pytest.param("probes", {}, 1, id="there is no probes folder"),
    pytest.param("probes", {"probes/helper.py": "not a probe\n"}, 1, id="the folder holds no test_*.py"),
    pytest.param("mutants", {"mutants.json": [{"case": "B1-F1", "file": "calc.py", "old": "a", "new": "b"}]}, 0,
                 id="mutants.json is a list"),
    pytest.param("mutants", {}, 1, id="mutants.json is missing"),
    pytest.param("mutants", {"mutants.json": {"cases": []}}, 1, id="mutants.json is an object, not a list"),
]


@pytest.mark.parametrize("step, written, expected", CHECK_OUTPUT)
def test_check_output_accepts_only_what_the_step_actually_wrote(step, written, expected, tmp_path):
    """R1-F17 — a model step can return done and write nothing usable; EV-C6.2 says that blocks the run."""
    run = tmp_path / "run"
    run.mkdir()
    write_json(run / "requirements.json", REQUIREMENTS)
    for name, content in written.items():
        (run / name).parent.mkdir(parents=True, exist_ok=True)
        write_json(run / name, content)
    result = run_model_io("check-output", run, "--step", step)
    assert result.returncode == expected, f"{step}: {result.stdout}{result.stderr}"
    assert "Traceback" not in result.stderr, result.stderr


# --- R1-F18: what the run cost, and what it never claimed -----------------------------------------

def test_the_start_stamp_records_when_the_run_began_and_never_zero_tokens(tmp_path):
    """R1-F18 — EV-P3.1: a missing count written as 0 reads as a free run, so it is written as not reported."""
    run = tmp_path / "run"
    run.mkdir()
    write_json(run / "requirements.json", REQUIREMENTS)
    cli_ok("stamp", run, "--event", "start")
    cost = read(run / "cost.json")
    utc(cost["start"])
    assert "end" not in cost, cost
    assert cost["tokens"] == "not reported", cost


def test_the_end_stamp_keeps_the_start_time_and_takes_the_agent_count(tmp_path):
    """R1-F18 — the end stamp closes the record: the same start, the real end, and the agents actually used."""
    run = tmp_path / "run"
    run.mkdir()
    write_json(run / "requirements.json", REQUIREMENTS)
    cli_ok("stamp", run, "--event", "start")
    started = read(run / "cost.json")
    cli_ok("stamp", run, "--event", "end", "--agents", "7")
    cost = read(run / "cost.json")
    assert cost["start"] == started["start"], "the end stamp restamped the beginning of the run"
    assert utc(cost["end"]) >= utc(cost["start"]), cost
    assert cost["agents"] == 7 and isinstance(cost["agents"], int), cost
    assert cost["tokens"] == "not reported", cost
