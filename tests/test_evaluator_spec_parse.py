"""Tests for tools/evaluator/spec_parse.py, the step that reads the spec.

The answers here are frozen: the ids, the group counts, the case splits and the open ids were counted by hand
from the fixtures in tests/fixtures/evaluator/, which the COO counted independently. So a parser that drops an id,
mis-splits a Fails if line, numbers a case wrongly or forgets an open requirement fails here.

The module is imported by path inside a helper, not at module level, because it does not exist yet: this file must
collect today and every test must fail on its own until the code lands.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools/evaluator/spec_parse.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures/evaluator"
INDEX_REQUIREMENTS = FIXTURES / "index-md-REQUIREMENTS.md"
INDEX_VISION = FIXTURES / "index-md-VISION.md"
SOT_REQUIREMENTS = FIXTURES / "sot-SOURCE_OF_TRUTH.md"
CACHES_REQUIREMENTS = FIXTURES / "caches-CACHES.md"

INDEX_IDS = [
    "B1.1", "B1.2", "B1.3",
    "B2.1", "B2.2", "B2.3", "B2.4", "B2.5", "B2.6",
    "B3.1", "B3.2", "B3.3", "B3.4",
    "B4.1", "B4.2", "B4.3", "B4.4",
    "C1.1", "C1.2", "C1.3", "C1.4",
    "C2.1", "C2.2",
    "G1.1", "G1.2",
    "G2.1", "G2.2", "G2.3",
    "G3.1", "G3.2",
    "G4.1", "G4.2",
]

B1_CASE_TEXTS = [
    "an untracked entry gets a line",
    "a file outside B1.1 gets a line",
    "a path with a space or a non-ASCII character is read wrongly in either mode",
]

CACHES_B1_CASE_TEXTS = [
    "a vector index exists in `project-memory/.cache/` with no recorded comparison in which it found at least one"
    " entry full-text missed and lost none of full-text's answers",
    "with no recorded decision by EJ",
    "a cache exists under `project-memory/.cache/` with no recorded comparison showing its trigger fired, or with no"
    " recorded decision by EJ to build it",
    "a passed comparison has no record that EJ was told",
    "a comparison ran on a question set with no record of who wrote it and who checked it",
]

UNTESTABLE_REQUIREMENTS = """# A small spec

**Z1 — A group with no check** (d)
- **Z1.1** It reads the thing.
- **Z1.2** It writes the thing.

**Z2 — A group with a check** (d)
- **Z2.1** It reports the thing.
- **Fails if** a report is missing.
"""


def load_spec_parse():
    """Import tools/evaluator/spec_parse.py by path, inside the test, so this file collects without it."""
    if not TOOL.is_file():
        pytest.fail(f"{TOOL} does not exist yet")
    spec = importlib.util.spec_from_file_location("evaluator_spec_parse", TOOL)
    module = importlib.util.module_from_spec(spec)
    sys.modules["evaluator_spec_parse"] = module
    spec.loader.exec_module(module)
    return module


def parse_file(module, path):
    """requirements.json's content for one fixture, read as text and passed to parse()."""
    return module.parse(path.read_text(encoding="utf-8"))


def group_of(document, name):
    """One group entry by its id, so a failure says which group."""
    return next(g for g in document["groups"] if g["group"] == name)


def case_ids(group):
    """The group's case ids in the order they appear."""
    return [case["case"] for case in group["cases"]]


def case_texts(group):
    """The group's case texts in the order they appear."""
    return [case["text"] for case in group["cases"]]


def test_every_requirement_id_is_listed_and_the_open_one_is_marked():
    """EV-R1.1 — an id missing from the list, or an open id not marked, leaves a requirement with no verdict at all."""
    module = load_spec_parse()
    frozen = [(INDEX_REQUIREMENTS, 32, ["G4.1"], "G4"),
              (SOT_REQUIREMENTS, 44, ["K4.3"], "K4"),
              (CACHES_REQUIREMENTS, 24, ["Rd3.4"], "Rd3")]
    for path, id_count, open_ids, open_group in frozen:
        document = parse_file(module, path)
        ids = [i for group in document["groups"] for i in group["ids"]]
        assert len(ids) == id_count, path.name
        assert len(set(ids)) == id_count, path.name
        opened = [i for group in document["groups"] for i in group["open_ids"]]
        assert opened == open_ids, path.name
        assert group_of(document, open_group)["open_ids"] == open_ids, path.name
        assert group_of(document, open_group)["status"] == "in_scope", path.name


def test_every_group_with_ids_carries_a_fails_if_and_numbered_cases():
    """EV-R1.1 — a group whose ids lose their Fails if line gives the whole group nothing to check."""
    module = load_spec_parse()
    frozen = [(INDEX_REQUIREMENTS, 10, 10), (SOT_REQUIREMENTS, 16, 16), (CACHES_REQUIREMENTS, 11, 11)]
    for path, group_count, with_fails_if in frozen:
        document = parse_file(module, path)
        groups = document["groups"]
        assert len(groups) == group_count, path.name
        assert len([g for g in groups if g["fails_if"]]) == with_fails_if, path.name
        for group in groups:
            if not group["ids"]:
                continue
            assert group["fails_if"], (path.name, group["group"])
            assert case_ids(group) == [f"{group['group']}-F{n}" for n in range(1, len(group["cases"]) + 1)], \
                (path.name, group["group"])


def test_a_fails_if_splits_on_commas_into_one_case_each():
    """EV-R1.1 — a Fails if line read as one case leaves the group with a single, vague failure case."""
    module = load_spec_parse()
    document = parse_file(module, INDEX_REQUIREMENTS)
    b1 = group_of(document, "B1")
    assert b1["ids"] == ["B1.1", "B1.2", "B1.3"]
    assert case_ids(b1) == ["B1-F1", "B1-F2", "B1-F3"]
    assert case_texts(b1) == B1_CASE_TEXTS
    assert case_texts(group_of(document, "B2")) == [
        "a malformed active entry gets a line",
        "a prefix/kind mismatch passes",
        "a duplicate id passes",
        "a broken retired entry stops the build",
        "any input ends in a traceback",
    ]


def test_a_fails_if_with_semicolons_splits_on_them_and_not_on_commas():
    """EV-R1.1 — splitting a semicolon list on its commas invents failure cases that never existed."""
    module = load_spec_parse()
    document = parse_file(module, INDEX_REQUIREMENTS)
    b3 = group_of(document, "B3")
    assert case_ids(b3) == ["B3-F1", "B3-F2", "B3-F3"]
    assert case_texts(b3)[0] == \
        "two runs over the same entries, on two machines or with two locales, give different bytes"
    assert case_texts(b3)[1] == "a superseded entry gets a line"
    assert case_texts(b3)[2].startswith("a file name with a space or")
    assert case_texts(b3)[2].endswith("gives a link that does not resolve")


def test_cases_are_numbered_across_several_fails_if_bullets():
    """EV-R1.1 — a second Fails if bullet numbered from one again makes two cases share an id."""
    module = load_spec_parse()
    document = parse_file(module, CACHES_REQUIREMENTS)
    b1 = group_of(document, "B1")
    assert b1["ids"] == ["B1.0", "B1.1", "B1.2", "B1.3"]
    assert case_ids(b1) == ["B1-F1", "B1-F2", "B1-F3", "B1-F4", "B1-F5"]
    assert case_texts(b1) == CACHES_B1_CASE_TEXTS


def test_only_the_two_named_vision_sections_become_requirements():
    """EV-R1.2 — a vision line outside the two sections gets a verdict nobody asked for, and an id of its own."""
    module = load_spec_parse()
    document = module.parse(INDEX_REQUIREMENTS.read_text(encoding="utf-8"),
                            INDEX_VISION.read_text(encoding="utf-8"))
    vision = document["vision"]
    assert [v["id"] for v in vision] == [f"V{n}" for n in range(1, 9)]
    assert [v["section"] for v in vision] == ["never"] * 5 + ["how_we_know"] * 3
    assert vision[0]["text"].startswith("Never cut, drop, rank or shorten")
    assert vision[5]["section"] == "how_we_know"
    assert vision[5]["text"].startswith("On any commit")
    for entry in vision:
        assert [case["case"] for case in entry["cases"]] == [f"{entry['id']}-F1"], entry["id"]
        assert entry["cases"][0]["text"] == entry["text"], entry["id"]


def test_a_group_with_no_fails_if_is_untestable_and_never_dropped():
    """EV-R1.3 — a group with no Fails if that disappears is a requirement the run never reports on at all."""
    module = load_spec_parse()
    document = module.parse(UNTESTABLE_REQUIREMENTS)
    z1 = group_of(document, "Z1")
    assert z1["ids"] == ["Z1.1", "Z1.2"]
    assert z1["status"] == "untestable"
    assert z1["cases"] == []
    assert z1["open_ids"] == []
    assert document["manifest"][:2] == ["Z1.1", "Z1.2"]
    z2 = group_of(document, "Z2")
    assert z2["status"] == "in_scope"
    assert case_texts(z2) == ["a report is missing"]


def test_the_coverage_manifest_lists_every_id_in_file_order():
    """EV-P2.1 — an id missing from the manifest is a requirement this run claims to have covered."""
    module = load_spec_parse()
    document = module.parse(INDEX_REQUIREMENTS.read_text(encoding="utf-8"),
                            INDEX_VISION.read_text(encoding="utf-8"))
    assert document["manifest"] == INDEX_IDS + [f"V{n}" for n in range(1, 9)]
    anchors = [(SOT_REQUIREMENTS, "W1.1", "Rd6.1"), (CACHES_REQUIREMENTS, "B2.1", "Rd3.5")]
    for path, first, last in anchors:
        manifest = parse_file(module, path)["manifest"]
        assert manifest[0] == first, path.name
        assert manifest[-1] == last, path.name
        assert len(manifest) == len(set(manifest)), path.name