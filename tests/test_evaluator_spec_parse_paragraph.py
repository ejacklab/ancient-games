"""Tests for DATA.md E1 rule 9, the paragraph form, in tools/evaluator/spec_parse.py.

The answers are frozen, counted by hand from the fixtures (frozen copies of docs/HARNESS_REQUIREMENTS.md and
memory_check/REQUIREMENTS.md, 2026-10-18) by the main agent (Claude), which does not write the parser. The rule 1–8
fixtures keep their own tests in test_evaluator_spec_parse.py, unchanged.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools/evaluator/spec_parse.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures/evaluator"
HARNESS = FIXTURES / "harness-REQUIREMENTS.md"
MEMORY_CHECK = FIXTURES / "memory-check-REQUIREMENTS.md"

HARNESS_IDS = ["R11.1", "R11.2", "R12.1", "R12.2", "R12.3", "R12.4", "R12.5", "R12.6", "R12.7"]
MEMORY_CHECK_IDS = ["F1", "F2", "F3", "C1", "C2", "C3", "C4", "C5", "C6", "R1", "R2", "R3", "T1"]


def parser():
    spec = importlib.util.spec_from_file_location("spec_parse", TOOL)
    module = importlib.util.module_from_spec(spec)
    sys.modules["spec_parse"] = module
    spec.loader.exec_module(module)
    return module


def parsed(path: Path) -> dict:
    return parser().parse(path.read_text(encoding="utf-8"), None)


def test_harness_ids_are_all_read_in_file_order():
    assert parsed(HARNESS)["manifest"] == HARNESS_IDS


def test_harness_groups_come_from_the_headings():
    groups = {g["group"]: g["ids"] for g in parsed(HARNESS)["groups"]}
    assert groups == {"R11": ["R11.1", "R11.2"], "R12": HARNESS_IDS[2:]}


def test_harness_group_fails_if_paragraphs_become_cases():
    by_group = {g["group"]: g for g in parsed(HARNESS)["groups"]}
    assert by_group["R11"]["status"] == "in_scope"
    assert by_group["R11"]["cases"][0]["text"] == "the units are written after the cases"
    assert by_group["R12"]["cases"][0]["text"] == "an evaluator crash or an empty result is read as pass"
    # R12 has two Fails if paragraphs (after R12.6 and after R12.7); both reach the group (rule 3: joined).
    texts = [c["text"] for c in by_group["R12"]["cases"]]
    assert any(t.startswith("a check's successes are not recorded") for t in texts)


def test_memory_check_ids_are_all_read_each_its_own_group():
    document = parsed(MEMORY_CHECK)
    assert document["manifest"] == MEMORY_CHECK_IDS
    assert [g["group"] for g in document["groups"]] == MEMORY_CHECK_IDS
    assert all(g["ids"] == [g["group"]] for g in document["groups"])


def test_memory_check_inline_fails_if_is_each_groups_cases():
    by_group = {g["group"]: g for g in parsed(MEMORY_CHECK)["groups"]}
    assert all(g["status"] == "in_scope" and g["cases"] for g in by_group.values())
    assert by_group["C5"]["fails_if"].startswith("the report does not name its snapshot or its range")
    assert "Who decides" not in by_group["C5"]["fails_if"]


def test_paragraph_text_outside_a_requirement_is_ignored():
    document = parsed(MEMORY_CHECK)
    assert document.get("unparsed_ids", []) == []
    assert not any("leaves open" in g["fails_if"] for g in document["groups"])


def test_the_main_command_no_longer_refuses_our_files(tmp_path):
    for path in (HARNESS, MEMORY_CHECK):
        out = tmp_path / f"{path.stem}.json"
        assert parser().main(["--requirements", str(path), "--out", str(out)]) == 0
        assert out.exists()
