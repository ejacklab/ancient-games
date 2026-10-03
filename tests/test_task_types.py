"""Tests for the task-types gate: docs/TASK_TYPES.md parsing, design_gate.py rules, and the
16-prompt corpus (tests/fixtures/task_type_prompts.json).

The corpus expectations are provisional working values (n=0) for EJ to correct; what is enforced
here is the gate machinery: every good design passes, every sabotaged variant fails named, and the
checks are known to be able to fail (the house rule).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "skills" / "workflow-design" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import design_gate as dg  # noqa: E402

TYPES = dg.parse_types(ROOT / "docs" / "TASK_TYPES.md")
CORPUS = json.loads((ROOT / "tests" / "fixtures" / "task_type_prompts.json").read_text())

FIVE = sorted(dg.FIVE)
LOOP_CATS = {"code generation", "debugging", "ui/ux dev", "test script gen"}
# Test-side engine defaults (concrete ids, per EXECUTOR_KINDS); the table's engine cell is prose.
ENGINES = {
    "code generation": "codex gpt-6.1-sol", "code review": "claude sonnet 5.5",
    "debugging": "codex gpt-6.1-sol", "ui/ux dev": "codex gpt-6.1-sol",
    "test data gen": "claude sonnet 5.5", "test cases gen": "codex gpt-6.1-sol",
    "test script gen": "codex gpt-6.1-sol", "repo scanning": "claude sonnet 5.5",
    "multi step planning": "codex gpt-6-astra", "information extraction": "claude sonnet 5.5",
    "web search": "codex gpt-6.1-sol", "classification": "agy gemini-3.1-pro-high",
    "research and reports": "codex gpt-6.1-sol", "others": "claude sonnet 5.5",
    "document and explain": "claude sonnet 5.5", "grade a run": "claude sonnet 5.5",
}


def builder_cats(cats: list, builds: bool) -> list:
    known = TYPES["categories"]
    return [c for c in cats if known.get(c, {}).get("product") == "yes"
            or (builds and known.get(c, {}).get("product") == "mixed")]


def design_for(entry: dict) -> dict:
    exp = entry["expected"]
    cats = exp["categories"]
    nodes, prev = [], None
    for i, c in enumerate(cats):
        n = {"id": f"n{i + 1}", "category": c, "engine": ENGINES[c],
             "check": f"default check for {c} (TASK_TYPES.md)", "five_things": list(FIVE),
             "needs": [prev] if prev else []}
        if c in LOOP_CATS:
            n["loop"] = {"limit": 2, "exit": "fresh node on stronger tier with handoff note",
                         "feedback": "the check's real output"}
        nodes.append(n)
        prev = n["id"]
    b_cats = builder_cats(cats, exp["builds"])
    if b_cats:
        yes_kinds = {dg.engine_kind(ENGINES[c]) for c in b_cats
                     if TYPES["categories"].get(c, {}).get("product") == "yes"}
        b_kinds = yes_kinds or {dg.engine_kind(ENGINES[c]) for c in b_cats}
        rev = "claude sonnet 5.5" if b_kinds == {"codex"} else "codex gpt-6.1-sol"
        nodes.append({"id": "nr", "category": "code review", "engine": rev,
                      "check": "fixed checklist; findings with file:line",
                      "five_things": list(FIVE), "needs": [prev] if prev else []})
    return {"categories": cats, "builds": exp["builds"],
            "touched_paths": (["product/x.py"] if exp["builds"] else []),
            "pipeline": exp["pipeline"], "nodes": nodes,
            "design_source": "default", "estimate": {"tokens": 100000}}


def test_types_table_parses():
    cats = TYPES["categories"]
    assert len(cats) >= 14
    assert "others" in cats
    for name, row in cats.items():
        if name != "others":
            assert row["sabotage"].strip() not in ("", "—"), f"{name} has no sabotage"
            assert row["check"].strip() not in ("", "—"), f"{name} has no default check"
    assert len(TYPES["pipelines"]) >= 4


def test_corpus_shape():
    assert len(CORPUS) == 16
    ids = set()
    for e in CORPUS:
        assert e["id"] not in ids
        ids.add(e["id"])
        assert e["prompt"].strip()
        exp = e["expected"]
        assert exp["complexity"] in ("tiny", "single", "combo", "open")
        for c in exp["categories"]:
            assert c in TYPES["categories"], f"{e['id']}: unknown category {c}"
        if exp["pipeline"]:
            assert exp["pipeline"].strip().lower() in TYPES["pipelines"], f"{e['id']}: unknown pipeline"


def test_corpus_covers_every_category():
    used = {c for e in CORPUS for c in e["expected"]["categories"]}
    fixtures = ROOT / "tests" / "fixtures"
    for name in ("operator_prompts_r1.jsonl", "operator_prompts_r2.jsonl", "operator_prompts_r3.jsonl"):
        p = fixtures / name
        if p.exists():
            for line in p.read_text().splitlines():
                if line.strip():
                    used |= set(json.loads(line)["exp"]["cats"])
    assert set(TYPES["categories"]) - used == set()


def test_mixed_category_semantics():
    known = TYPES["categories"]
    assert known["debugging"]["product"] == "mixed"
    assert known["test data gen"]["product"] == "mixed"
    assert known["document and explain"]["product"] == "mixed"
    assert known["code generation"]["product"] == "yes"
    d = {"categories": ["debugging"], "builds": False, "touched_paths": [],
         "nodes": [{"id": "n1", "category": "debugging", "engine": "codex gpt-6.1-sol",
                    "check": "repro test red before, green after", "five_things": list(FIVE), "needs": [],
                    "loop": {"limit": 2, "exit": "fresh node stronger tier", "feedback": "test output"}}],
         "design_source": "default"}
    assert dg.validate_design(d, TYPES) == []
    d2 = json.loads(json.dumps(d)); d2["builds"] = True; d2["touched_paths"] = ["engine/x.py"]
    assert any(x.startswith("G6") for x in dg.validate_design(d2, TYPES))
    d2["nodes"].append({"id": "nr", "category": "code review", "engine": "claude sonnet 5.5",
                        "check": "fixed checklist", "five_things": list(FIVE), "needs": ["n1"]})
    assert dg.validate_design(d2, TYPES) == []


def test_gate_accepts_every_corpus_design():
    for e in CORPUS:
        if e["expected"]["tiny"]:
            continue
        findings = dg.validate_design(design_for(e), TYPES)
        assert findings == [], (e["id"], findings)


def test_guard_research_only_on_building_design():
    e = next(x for x in CORPUS if x["expected"].get("guard_case"))
    d = design_for(e)
    d["categories"] = ["research and reports"]
    d["nodes"] = [n for n in d["nodes"] if n["category"] != "code review"]
    findings = dg.validate_design(d, TYPES)
    assert any(x.startswith("G2") for x in findings), findings


def test_others_category_may_build():
    e = next(x for x in CORPUS if x["id"] == "t16-vague-better")
    d = design_for(e)
    assert d["categories"] == ["others"] and d["builds"]
    assert dg.validate_design(d, TYPES) == []


def test_margin_boundaries():
    base = design_for(next(x for x in CORPUS if x["id"] == "t02-codegen-flag"))
    base["default_estimate"] = {"tokens": 100000}
    base["coverage"] = base["default_coverage"] = {"criteria": ["R1.1"], "checks": ["pytest -q"]}
    base["design_source"] = {"type": "challenger", "claim_margin": 0.19, "basis": "b"}
    assert any(x.startswith("G5") for x in dg.validate_design(base, TYPES))
    base["design_source"] = {"type": "challenger", "claim_margin": 0.20, "basis": "b"}
    base["estimate"] = {"tokens": 80000}
    assert dg.validate_design(base, TYPES) == []
    base["design_source"] = {"type": "challenger", "claim_margin": 0.30, "basis": "b"}
    assert any("arithmetic" in x for x in dg.validate_design(base, TYPES))
    base["design_source"] = {"type": "challenger", "claim_margin": 0.30, "basis": ""}
    assert any("basis" in x for x in dg.validate_design(base, TYPES))


def test_coverage_is_a_gate_not_an_axis():
    base = design_for(next(x for x in CORPUS if x["id"] == "t02-codegen-flag"))
    base["default_estimate"] = {"tokens": 200000}
    base["estimate"] = {"tokens": 100000}  # a real 50% margin
    base["design_source"] = {"type": "challenger", "claim_margin": 0.50, "basis": "b"}
    base["coverage"] = {"criteria": ["R1.1"], "checks": ["pytest -q"]}
    base["default_coverage"] = {"criteria": ["R1.1", "R1.2"], "checks": ["pytest -q"]}
    assert any("coverage" in x for x in dg.validate_design(base, TYPES))


def test_node_and_edge_rules():
    base = design_for(next(x for x in CORPUS if x["id"] == "t02-codegen-flag"))
    d = json.loads(json.dumps(base)); d["nodes"][0]["check"] = ""
    assert any(x.startswith("G3") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["nodes"][0]["five_things"] = ["tools"]
    assert any(x.startswith("G3") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["nodes"][0]["loop"] = {"limit": 0, "exit": "x", "feedback": "y"}
    assert any(x.startswith("G3") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["nodes"][0]["needs"] = ["ghost"]
    assert any(x.startswith("G4") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["pipeline"] = "not-a-pipeline"
    assert any(x.startswith("G4") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["categories"] = ["frobnicate"]
    assert any(x.startswith("G1") for x in dg.validate_design(d, TYPES))


def test_reviewer_kind_rule():
    base = design_for(next(x for x in CORPUS if x["id"] == "t02-codegen-flag"))
    d = json.loads(json.dumps(base))
    d["nodes"] = [n for n in d["nodes"] if n["category"] != "code review"]
    assert any(x.startswith("G6") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base))
    for n in d["nodes"]:
        if n["category"] == "code review":
            n["engine"] = "codex gpt-6-astra"
    assert any(x.startswith("G6") for x in dg.validate_design(d, TYPES))


def test_ledger_row_rules():
    row = {k: "x" for k in dg.LEDGER_FIELDS}
    row.update({"design_source": "default", "claimed_margin": "—", "reconciled": False})
    assert dg.validate_ledger_row(row) == []
    row2 = dict(row); row2.pop("basis")
    assert any(x.startswith("G7") for x in dg.validate_ledger_row(row2))
    row3 = dict(row); row3.update({"design_source": "challenger", "claimed_margin": 0.1, "basis": "—"})
    assert any(x.startswith("G7") for x in dg.validate_ledger_row(row3))
    row4 = dict(row); row4.update({"reconciled": True, "actual_cost": ""})
    assert any(x.startswith("G7") for x in dg.validate_ledger_row(row4))


def test_ledger_markdown_parses_and_validates(tmp_path):
    # the shipped ledger: every row it holds must validate (row 1 is the first real run, 2026-10-03)
    shipped = dg.parse_ledger(ROOT / "docs" / "TASK_TYPES_LEDGER.md")
    assert shipped and all(dg.validate_ledger_row(r) == [] for r in shipped)
    good = "| 2026-10-02 | 20261002-x | code generation | challenger | 0.25 | one node instead of three | 130k | 95k | criteria pass | yes |"
    bad = "| 2026-10-02 | 20261002-y | debugging | challenger | 0.3 | — | 100k |  | criteria pass | yes |"
    p = tmp_path / "ledger.md"
    p.write_text("# L\n\n| Date | Run id | Category | Design source | Claimed margin | Basis | Projected cost | Actual cost | Coverage outcome | Reconciled |\n"
                 "|---|---|---|---|---|---|---|---|---|---|\n" + good + "\n" + bad + "\n")
    rows = dg.parse_ledger(p)
    assert len(rows) == 2
    assert dg.validate_ledger_row(rows[0]) == []
    findings = dg.validate_ledger_row(rows[1])
    assert any("basis" in x for x in findings)          # challenger without a basis
    assert any("actual cost" in x for x in findings)     # reconciled without an actual cost
    r = subprocess.run([sys.executable, str(SCRIPTS / "design_gate.py"), "--ledger", str(p)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 1 and "row 2" in r.stdout, r.stdout


def test_gate_self_test_cli():
    p = subprocess.run([sys.executable, str(SCRIPTS / "design_gate.py"), "--self-test"],
                       capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, p.stdout + p.stderr
    assert "PASS" in p.stdout


def test_building_document_needs_different_kind_review():
    # round-3 regression (p073): a document piece that builds gets its review-against-source
    # node from a different kind than the writer
    writer = {"id": "n1", "category": "document and explain", "engine": "claude sonnet 5.5",
              "check": "checklist against source; LF endings", "five_things": list(FIVE), "needs": []}
    same = {"id": "n1r", "category": "code review", "engine": "claude sonnet 5.5",
            "check": "review against source", "five_things": list(FIVE), "needs": ["n1"]}
    other = dict(same, engine="codex gpt-6.1-sol")
    base = {"categories": ["document and explain"], "builds": True, "touched_paths": ["docs/cmds.sh"],
            "pipeline": None, "design_source": "default"}
    assert any(x.startswith("G6") for x in dg.validate_design(dict(base, nodes=[writer, same]), TYPES))
    assert dg.validate_design(dict(base, nodes=[writer, other]), TYPES) == []


def test_reviewer_kind_not_diluted_by_mixed_builders():
    # round-3 blind-review catch (p274): pure builders are codex, a mixed builder is claude —
    # the blend must not make a codex reviewer acceptable
    d = {"categories": ["test data gen", "test script gen"], "builds": True,
         "touched_paths": ["tests/x"], "pipeline": None,
         "nodes": [
             {"id": "n1", "category": "test data gen", "engine": "claude sonnet 5.5",
              "check": "schema validation", "five_things": list(FIVE), "needs": []},
             {"id": "n2", "category": "test script gen", "engine": "codex gpt-6.1-sol",
              "check": "seeded failure detected", "five_things": list(FIVE), "needs": ["n1"],
              "loop": {"limit": 2, "exit": "stronger tier", "feedback": "output"}},
             {"id": "nr", "category": "code review", "engine": "codex gpt-6-astra",
              "check": "fixed checklist", "five_things": list(FIVE), "needs": ["n2"]}],
         "design_source": "default"}
    assert any(x.startswith("G6") for x in dg.validate_design(d, TYPES))
    d["nodes"][2]["engine"] = "claude sonnet 5.5"
    assert dg.validate_design(d, TYPES) == []


def test_gate_cli_end_to_end(tmp_path):
    entry = next(x for x in CORPUS if x["id"] == "t05-research-then-hook")
    d = design_for(entry)
    p = tmp_path / "design.json"
    p.write_text(json.dumps(d))
    r = subprocess.run([sys.executable, str(SCRIPTS / "design_gate.py"), str(p)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and "PASS" in r.stdout, r.stdout + r.stderr
    d["categories"] = ["research and reports"]  # the corpus's guard case: research-only on a building design
    p.write_text(json.dumps(d))
    r = subprocess.run([sys.executable, str(SCRIPTS / "design_gate.py"), str(p)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 1 and "G2" in r.stdout, r.stdout + r.stderr


def test_labels_agree_between_design_and_nodes():
    # method 3.2: piece labels replace the provisional category, so design and nodes must carry the same set
    import copy
    good = dg._good_design()
    assert not [f for f in dg.validate_design(good, TYPES) if f.startswith("G8")]

    unlisted = copy.deepcopy(good)
    unlisted["categories"] = ["research and reports"]          # nodes still carry code generation
    assert any(f.startswith("G8") and "code generation" in f for f in dg.validate_design(unlisted, TYPES))

    unclaimed = copy.deepcopy(good)
    unclaimed["categories"] = good["categories"] + ["classification"]   # no node carries it
    assert any(f.startswith("G8") and "classification" in f for f in dg.validate_design(unclaimed, TYPES))

    # the in-run review node that G6 demands is exempt from the "unlisted" direction
    assert any(n["category"] == "code review" for n in good["nodes"])
    assert not any("code review" in f for f in dg.validate_design(good, TYPES) if f.startswith("G8"))
