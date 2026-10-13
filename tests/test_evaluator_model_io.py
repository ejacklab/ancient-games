"""Tests for tools/evaluator/model_io.py, the files written around the model steps (steps E8 and E9).

Every input is written by hand under tmp_path, so each test names one rule of DATA.md's model_io.py section and no
test leans on a step that has not been written down. Where a step's own output is the next step's input
(confirm-input then confirm-check, judge-input then judged-merge) the earlier subcommand is really run, because that
is the order DATA.md's table puts them in and a hand-written stand-in would only test the test. The tool is called
through its CLI, which is the only interface DATA.md gives it, so this file collects today and every test fails on
its own until the code lands.

One thing DATA.md does not fix: confirm-input's `output` comes "from matrix.json", but DATA.md's matrix.json records
no per-probe output, so these tests hold only that every entry carries an `output` string, not what is in it. They
also read a written list as either a bare list or an object with a `cases` key, because DATA.md names the fields
inside an entry but not the top-level shape.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools/evaluator/model_io.py"
SUBCOMMANDS = ["confirm-input", "confirm-check", "judge-input", "judged-merge"]

SPEC = """# Requirements — the calculator product

## The arithmetic

**B1 — The calculator**

- **B1.1** MUST. It  adds two numbers and never writes to the product.
- **B1.2** MUST. It reads the first line of a file whose name may hold a space.
- **Fails if:** the sum of two numbers is wrong; a file with a space in its name is read wrongly

**B2 — The reader**

- **B2.1** MUST. It reports a missing file instead of raising.
- **Fails if:** a missing file is not reported

**G2 — The judge**

- **G2.1** MUST. A judged case carries quoted file:line evidence.
- **Fails if:** a judged verdict has no quoted evidence
"""

VISION = """# Vision — the calculator product

**What it will never do**

- It never writes to the product it reads.
"""

CALC = '''"""The product's calculator."""


def add(a, b):
    """B1-F1 — the sum of two numbers."""
    return a + b


def first_line(path):
    """B2-F1 — the first line of a file."""
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            return line.strip()
    return ""
'''
NOTES = "the product's own notes\nsecond line\n"

PROBES = '''"""The E4 probes for B1 and B2."""
import os
import sys

sys.path.insert(0, os.environ["EVAL_PRODUCT"])
import calc


def test_sum():
    """B1-F1 — the sum of two numbers is right."""
    assert calc.add(2, 3) == 5


def test_named_file():
    """B1-F2 — a file with a space in its name is read."""
    assert calc.first_line("a file.txt") == "x"


def test_missing_file():
    """B2-F1 — a missing file is reported, not raised."""
    assert calc.first_line("no such file") == ""
'''

REQUIREMENTS = {
    "spec": {"requirements": "workspace/spec/REQUIREMENTS.md", "vision": "workspace/spec/VISION.md"},
    "groups": [
        {"group": "B1", "title": "The calculator", "ids": ["B1.1", "B1.2"], "status": "in_scope",
         "fails_if": "the sum of two numbers is wrong; a file with a space in its name is read wrongly",
         "cases": [{"case": "B1-F1", "text": "the sum of two numbers is wrong"},
                   {"case": "B1-F2", "text": "a file with a space in its name is read wrongly"}],
         "open_ids": []},
        {"group": "B2", "title": "The reader", "ids": ["B2.1"], "status": "in_scope",
         "fails_if": "a missing file is not reported",
         "cases": [{"case": "B2-F1", "text": "a missing file is not reported"}],
         "open_ids": []},
        {"group": "G2", "title": "The judge", "ids": ["G2.1"], "status": "in_scope",
         "fails_if": "a judged verdict has no quoted evidence",
         "cases": [{"case": "G2-F1", "text": "a judged verdict has no quoted evidence"},
                   {"case": "G2-F2", "text": "a judged verdict quotes a line that is not there"},
                   {"case": "G2-F3", "text": "a missed plant is never rerun"}],
         "open_ids": []},
    ],
    "vision": [],
    "manifest": ["B1.1", "B1.2", "B2.1", "G2.1"],
}

CLASSIFY = {"cases": [{"case": "B1-F1", "kind": "executable", "reason": "run the probe"},
                      {"case": "B1-F2", "kind": "executable", "reason": "run the probe"},
                      {"case": "B2-F1", "kind": "static", "reason": "read the one line"},
                      {"case": "G2-F1", "kind": "judged", "reason": "read calc.py"},
                      {"case": "G2-F2", "kind": "judged", "reason": "read calc.py"},
                      {"case": "G2-F3", "kind": "judged", "reason": "read calc.py"}]}

NO_JUDGED = {"cases": [{"case": "B1-F1", "kind": "executable", "reason": "run the probe"},
                       {"case": "B1-F2", "kind": "executable", "reason": "run the probe"},
                       {"case": "B2-F1", "kind": "static", "reason": "read the one line"}]}

PLANTS = [{"case": "G2-F1", "file": "calc.py", "old": "raise NotImplementedError", "new": "pass"},
          {"case": "G2-F2", "file": "calc.py", "old": "return a + b", "new": "return a - b"}]

RED_PROBES = ["test_b1::test_sum", "test_b1::test_missing_file"]
MATRIX = {"product_dir": "workspace/product", "probes_dir": "probes",
          "citations": {"test_b1::test_sum": ["B1-F1"], "test_b1::test_named_file": ["B1-F2"],
                        "test_b1::test_missing_file": ["B2-F1"]},
          "product": {"test_b1::test_sum": "fail", "test_b1::test_named_file": "pass",
                      "test_b1::test_missing_file": "fail"},
          # the failing probes' messages, which probe_matrix records since calibration K1 (COO, 2026-10-13)
          "output": {"test_b1::test_sum": "AssertionError: assert 5 == 6",
                     "test_b1::test_missing_file": "AssertionError: assert False"},
          "mutants": {}, "restored": True}
ALL_GREEN = {**MATRIX, "product": {key: "pass" for key in MATRIX["product"]}}

CONFIRMED = [{"case": "B1-F1", "probe": "test_b1::test_sum", "faithful": True,
              "requirement_quote": "the sum of two numbers is wrong",
              "probe_quote": "assert calc.add(2, 3) == 5"},
             {"case": "B2-F1", "probe": "test_b1::test_missing_file", "faithful": True,
              "requirement_quote": "a missing file is not reported",
              "probe_quote": 'assert calc.first_line("no such file") == ""'}]

PLANT_QUOTE = 'calc.py:6 "return a - b"'
CLEAN_QUOTE = 'calc.py:6 "return a + b"'
ABSENT_QUOTE = 'calc.py:6 "return a * b"'

CALL_ONE_MISSED = {"cases": [{"case": "G2-F1", "holds": True, "evidence": PLANT_QUOTE},
                             {"case": "G2-F2", "holds": False, "evidence": PLANT_QUOTE},
                             {"case": "G2-F3", "holds": True, "evidence": ABSENT_QUOTE}]}
CALL_TWO_FOUND = {"cases": [{"case": "G2-F2", "holds": True, "evidence": CLEAN_QUOTE}]}


def write_json(path, document):
    """One recorded file, written the way the step before wrote it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read(path):
    """A file the tool wrote."""
    return json.loads(path.read_text(encoding="utf-8"))


def entries(document):
    """The list inside a written file, whichever of the two top-level shapes it was written in."""
    return document if isinstance(document, list) else document["cases"]


def judge_folder(run):
    """The folder F2 builds outside the run folder for judge call 1, named after the run folder."""
    return Path("/tmp") / f"evaluator-judge-{Path(run).name}"


def planted_case(run):
    """The case the run planted, read from the coordinator's own file: F2 keeps it out of judge-input.json."""
    return read(Path(run) / ".coordinator/plant.json")["plant_case"]


def one_per_case(document):
    """The entries keyed by case, insisting there is exactly one entry per case."""
    written = entries(document)
    keyed = {entry["case"]: entry for entry in written}
    assert len(keyed) == len(written), f"a case has more than one entry: {[e['case'] for e in written]}"
    return keyed


def build_run(root, *, matrix=None, classify=None, plants=None):
    """Write a small run folder by hand: E1's, E3's and E5's outputs, the workspace, the spec and the probes."""
    run = Path(root) / "run"
    (run / "probes").mkdir(parents=True)
    (run / "probes" / "test_b1.py").write_text(PROBES, encoding="utf-8")
    product = run / "workspace/product"
    product.mkdir(parents=True)
    (product / "calc.py").write_text(CALC, encoding="utf-8")
    (product / "notes.txt").write_text(NOTES, encoding="utf-8")
    spec = run / "workspace/spec"
    spec.mkdir(parents=True)
    (spec / "REQUIREMENTS.md").write_text(SPEC, encoding="utf-8")
    (spec / "VISION.md").write_text(VISION, encoding="utf-8")
    write_json(run / "requirements.json", REQUIREMENTS)
    write_json(run / "matrix.json", MATRIX if matrix is None else matrix)
    write_json(run / "classify.json", CLASSIFY if classify is None else classify)
    write_json(run / "plants.json", PLANTS if plants is None else plants)
    return run


@pytest.fixture
def evaluation_run(tmp_path):
    """One small run folder, ready for any of the four subcommands."""
    return build_run(tmp_path)


def run_model_io(subcommand, run, *extra):
    """Run the real CLI from outside the run folder, with an outer watchdog."""
    assert TOOL.is_file(), f"implementation is missing: {TOOL}"
    return subprocess.run([sys.executable, str(TOOL), subcommand, "--run", str(run), *extra],
                          cwd=str(Path(run).parent), capture_output=True, text=True, timeout=30)


def cli_ok(subcommand, run, *extra):
    """Run one subcommand and insist it wrote its output."""
    result = run_model_io(subcommand, run, *extra)
    assert result.returncode == 0, f"{subcommand} exited {result.returncode}: {result.stdout}{result.stderr}"
    return result


def confirm_answers(root, answers):
    """confirm-input's real output, then the confirm agent's answers, ready for confirm-check."""
    run = build_run(root)
    cli_ok("confirm-input", run)
    write_json(run / "confirm.json", {"cases": answers})
    return run


def judge_answers(root, call_one, call_two, classify=None):
    """judge-input's real output, then the judge step's two answers, ready for judged-merge.

    Call 1 writes into the judge's own folder (F2) and call 2 into the run folder, which is where DATA.md puts them.
    """
    run = build_run(root, classify=classify)
    cli_ok("judge-input", run)
    write_json(judge_folder(run) / "judge-1.json", call_one)
    write_json(run / "judge-2.json", call_two)
    return run


def test_confirm_input_lists_one_entry_per_probe_that_is_red_on_the_product(evaluation_run):
    """DATA.md model_io.py confirm-input — one entry per red probe, and the count it prints."""
    result = cli_ok("confirm-input", evaluation_run)
    assert result.stdout.strip() == "2 to confirm", result.stdout
    written = one_per_case(read(evaluation_run / "confirm-input.json"))
    assert sorted(written) == ["B1-F1", "B2-F1"], sorted(written)
    assert written["B1-F1"]["probe"] == "test_b1::test_sum"
    assert written["B1-F1"]["case_text"] == "the sum of two numbers is wrong"
    assert written["B2-F1"]["probe"] == "test_b1::test_missing_file"
    assert written["B2-F1"]["case_text"] == "a missing file is not reported"
    for case, entry in written.items():
        assert isinstance(entry.get("output"), str), f"{case} carries no output"


def test_confirm_input_group_text_is_the_group_block_verbatim(evaluation_run):
    """DATA.md model_io.py confirm-input — group_text is the group's own block, from its heading to the next one."""
    cli_ok("confirm-input", evaluation_run)
    written = one_per_case(read(evaluation_run / "confirm-input.json"))
    first = written["B1-F1"]["group_text"]
    assert first.startswith("**B1 — The calculator**"), repr(first[:60])
    assert "It  adds two numbers" in first, "the block is not verbatim: the double space was collapsed"
    assert "the sum of two numbers is wrong" in first, repr(first)
    assert "B2" not in first, "the block reaches into the next group"
    second = written["B2-F1"]["group_text"]
    assert second.startswith("**B2 — The reader**"), repr(second[:60])
    assert second != first, "both cases were given the same block"


def test_confirm_input_probe_source_is_the_function_behind_the_probe_key(evaluation_run):
    """DATA.md model_io.py confirm-input — probe_source is the source of that probe's own function."""
    cli_ok("confirm-input", evaluation_run)
    written = one_per_case(read(evaluation_run / "confirm-input.json"))
    source = written["B1-F1"]["probe_source"]
    assert "def test_sum():" in source, repr(source)
    assert "assert calc.add(2, 3) == 5" in source, repr(source)
    assert "def test_named_file" not in source, "the source holds another function"
    assert "def test_missing_file" in written["B2-F1"]["probe_source"], "the two entries got the same source"


def test_confirm_input_with_no_red_probe_prints_zero_to_confirm(tmp_path):
    """DATA.md model_io.py confirm-input — nothing red on the product means nothing to confirm."""
    run = build_run(tmp_path, matrix=ALL_GREEN)
    result = cli_ok("confirm-input", run)
    assert result.stdout.strip() == "0 to confirm", result.stdout
    assert entries(read(run / "confirm-input.json")) == []


def test_confirm_check_keeps_a_probe_whose_both_quotes_are_there(tmp_path):
    """DATA.md model_io.py confirm-check — quotes found in both sources keep the answer faithful."""
    run = confirm_answers(tmp_path, CONFIRMED)
    result = cli_ok("confirm-check", run)
    assert result.stdout.strip() == "2 checked, 0 voided, 0 unfaithful", result.stdout
    checked = {entry["case"]: entry for entry in entries(read(run / "confirm.json"))}
    assert all(entry["faithful"] is True for entry in checked.values()), checked
    assert all("note" not in entry for entry in checked.values()), checked


def test_confirm_check_voids_a_requirement_quote_the_group_does_not_hold(tmp_path):
    """DATA.md model_io.py confirm-check (EV-C4.2) — a requirement quote that is not in the block voids the entry."""
    answers = [dict(CONFIRMED[0], requirement_quote="a line nobody wrote"), CONFIRMED[1]]
    run = confirm_answers(tmp_path, answers)
    result = cli_ok("confirm-check", run)
    assert result.stdout.strip() == "2 checked, 1 voided, 0 unfaithful", result.stdout
    checked = {entry["case"]: entry for entry in entries(read(run / "confirm.json"))}
    assert checked["B1-F1"]["faithful"] is False, checked
    assert checked["B1-F1"]["note"] == "quote not found", checked
    assert checked["B2-F1"]["faithful"] is True, "the sound entry was voided too"


def test_confirm_check_voids_a_probe_quote_the_probe_does_not_hold(tmp_path):
    """DATA.md model_io.py confirm-check (EV-C4.2) — a probe quote that is not in the probe's own source voids it."""
    answers = [CONFIRMED[0], dict(CONFIRMED[1], probe_quote="assert calc.first_line(\"no such file\") == \"here\"")]
    run = confirm_answers(tmp_path, answers)
    result = cli_ok("confirm-check", run)
    assert result.stdout.strip() == "2 checked, 1 voided, 0 unfaithful", result.stdout
    checked = {entry["case"]: entry for entry in entries(read(run / "confirm.json"))}
    assert checked["B2-F1"]["faithful"] is False, checked
    assert checked["B2-F1"]["note"] == "quote not found", checked
    assert checked["B1-F1"]["faithful"] is True, "the sound entry was voided too"


def test_confirm_check_collapses_whitespace_runs_before_comparing(tmp_path):
    """DATA.md model_io.py confirm-check — a quote that differs only in spacing, or crosses a line, is the same."""
    answers = [dict(CONFIRMED[0], requirement_quote="the sum   of two numbers is wrong",
                             probe_quote="assert  calc.add(2,  3) == 5"),
               dict(CONFIRMED[1], probe_quote='def test_missing_file():\n    """B2-F1 — a missing file is '
                                              'reported, not raised."""')]
    run = confirm_answers(tmp_path, answers)
    result = cli_ok("confirm-check", run)
    assert result.stdout.strip() == "2 checked, 0 voided, 0 unfaithful", result.stdout
    checked = {entry["case"]: entry for entry in entries(read(run / "confirm.json"))}
    assert all(entry["faithful"] is True for entry in checked.values()), checked


def test_judge_input_names_the_first_judged_case_with_a_valid_plant(evaluation_run):
    """DATA.md model_io.py judge-input — G2-F1's plant text is in no file, so G2-F2 is the plant case."""
    result = cli_ok("judge-input", evaluation_run)
    assert result.stdout.splitlines() == ["3 to judge", "plant G2-F2"], result.stdout
    assert planted_case(evaluation_run) == "G2-F2"
    written = read(evaluation_run / "judge-input.json")
    assert "plant_case" not in written, written.keys()  # F2: the judge may not read the plant out of its own input
    judged = {entry["case"]: entry for entry in entries(written)}
    assert sorted(judged) == ["G2-F1", "G2-F2", "G2-F3"], sorted(judged)
    assert judged["G2-F1"]["case_text"] == "a judged verdict has no quoted evidence"
    assert judged["G2-F1"]["group_text"].startswith("**G2 — The judge**"), repr(judged["G2-F1"]["group_text"])
    assert "a judged verdict has no quoted evidence" in judged["G2-F1"]["group_text"]


def test_judge_copy_is_the_product_with_only_that_plant_applied(evaluation_run):
    """DATA.md model_io.py judge-input (EV-C5.2) — the judge's copy is the product plus one plant; the copy is untouched."""
    product = evaluation_run / "workspace/product/calc.py"
    before = product.read_text(encoding="utf-8")
    cli_ok("judge-input", evaluation_run)
    copy = judge_folder(evaluation_run) / "product"
    planted = (copy / "calc.py").read_text(encoding="utf-8")
    assert "return a - b" in planted, repr(planted)
    assert "return a + b" not in planted, "the plant was added without taking the original out"
    notes = (copy / "notes.txt").read_text(encoding="utf-8")
    assert notes == NOTES, "the rest of the product did not come across"
    assert product.read_text(encoding="utf-8") == before, "the product copy was changed (EV-R3.2)"


def test_judge_input_with_no_judged_case_prints_zero_to_judge(tmp_path):
    """DATA.md model_io.py judge-input — a run with nothing judged says 0 and writes no case."""
    run = build_run(tmp_path, classify=NO_JUDGED)
    result = cli_ok("judge-input", run)
    assert result.stdout.strip() == "0 to judge", result.stdout
    assert entries(read(run / "judge-input.json")) == []


@pytest.mark.parametrize("plants", [
    pytest.param([{"case": "G2-F1", "file": "calc.py", "old": "raise NotImplementedError", "new": "pass"}],
                 id="no such text in the file"),
    pytest.param([{"case": "G2-F2", "file": "calc.py", "old": "return", "new": "pass"}],
                 id="the text is there three times, not once"),
    pytest.param([{"case": "G2-F2", "file": "nowhere.py", "old": "return a + b", "new": "return a - b"}],
                 id="the text is in the copy, but the file is not"),
])
def test_judge_input_with_judged_cases_but_no_valid_plant_names_none(tmp_path, plants):
    """DATA.md model_io.py judge-input — only a plant whose old text is found exactly once can be the plant."""
    run = build_run(tmp_path, plants=plants)
    result = cli_ok("judge-input", run)
    assert result.stdout.strip() == "3 to judge", result.stdout
    assert planted_case(run) is None
    assert sorted(entry["case"] for entry in entries(read(run / "judge-input.json"))) == ["G2-F1", "G2-F2", "G2-F3"]


def test_judged_merge_calls_the_plant_found_when_call_one_says_the_case_does_not_hold(tmp_path):
    """DATA.md model_io.py judged-merge (EV-C5.2) — plant_found is true only when the judge missed the plant."""
    run = judge_answers(tmp_path, CALL_ONE_MISSED, CALL_TWO_FOUND)
    result = cli_ok("judged-merge", run)
    assert result.stdout.strip() == "plant_found: true", result.stdout
    assert read(run / "judged.json")["plant_found"] is True


def test_judged_merge_calls_the_plant_missed_when_call_one_says_the_case_holds(tmp_path):
    """DATA.md model_io.py judged-merge (EV-C5.2) — the judge saw the plant, so the judging is void."""
    call_one = {"cases": [{"case": "G2-F1", "holds": True, "evidence": PLANT_QUOTE},
                          {"case": "G2-F2", "holds": True, "evidence": PLANT_QUOTE},
                          {"case": "G2-F3", "holds": True, "evidence": PLANT_QUOTE}]}
    run = judge_answers(tmp_path, call_one, CALL_TWO_FOUND)
    result = cli_ok("judged-merge", run)
    assert result.stdout.strip() == "plant_found: false", result.stdout
    assert read(run / "judged.json")["plant_found"] is False


def test_judged_merge_takes_the_plant_case_entry_from_call_two(tmp_path):
    """DATA.md model_io.py judged-merge — the plant case's entry is the second call's answer, not the first's."""
    run = judge_answers(tmp_path, CALL_ONE_MISSED, CALL_TWO_FOUND)
    cli_ok("judged-merge", run)
    judged = one_per_case(read(run / "judged.json"))
    assert judged["G2-F2"]["evidence"] == CLEAN_QUOTE, "call one's answer for the plant case was kept"
    assert judged["G2-F2"]["holds"] is True, "call two said the case holds on the clean product"
    assert judged["G2-F1"]["evidence"] == PLANT_QUOTE, "another case did not keep call one's answer"


def test_judged_merge_drops_an_entry_whose_quote_is_in_no_file(tmp_path):
    """DATA.md model_io.py judged-merge — a case 1 entry quoting code that is in no file is dropped."""
    run = judge_answers(tmp_path, CALL_ONE_MISSED, CALL_TWO_FOUND)
    cli_ok("judged-merge", run)
    judged = one_per_case(read(run / "judged.json"))
    assert sorted(judged) == ["G2-F1", "G2-F2"], sorted(judged)
    assert "G2-F3" not in judged, "an entry whose quoted code is in neither file was kept"


def test_judged_merge_drops_the_plant_case_when_call_two_does_not_quote_the_real_code(tmp_path):
    """DATA.md model_io.py judged-merge — the same check for call 2, against the clean product copy."""
    call_two = {"cases": [{"case": "G2-F2", "holds": True, "evidence": ABSENT_QUOTE}]}
    run = judge_answers(tmp_path, CALL_ONE_MISSED, call_two)
    cli_ok("judged-merge", run)
    judged = one_per_case(read(run / "judged.json"))
    assert "G2-F2" not in judged, "a quote in neither file was kept, so the plant case counts as judged"


def test_judged_merge_with_no_judged_case_writes_an_empty_verdict(tmp_path):
    """DATA.md model_io.py judged-merge — with nothing judged, plant_found is true and there are no cases."""
    run = judge_answers(tmp_path, {"cases": []}, {"cases": []}, classify=NO_JUDGED)
    result = cli_ok("judged-merge", run)
    assert result.stdout.strip() == "plant_found: true", result.stdout
    assert read(run / "judged.json") == {"plant_found": True, "cases": []}


@pytest.mark.parametrize("subcommand", SUBCOMMANDS)
def test_every_subcommand_exits_2_on_a_missing_requirements_file(tmp_path, subcommand):
    """DATA.md model_io.py — every subcommand exits 2 on a missing requirements.json, with a line and no traceback."""
    run = tmp_path / "run"
    (run / "probes").mkdir(parents=True)
    result = run_model_io(subcommand, run)
    assert result.returncode == 2, f"exited {result.returncode}: {result.stdout}{result.stderr}"
    assert "requirements.json" in result.stderr, result.stderr
    assert "Traceback" not in result.stderr, result.stderr