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
# Derived from docs/TASK_TYPES.md itself: its engine column is the one place this policy lives, and a
# hand-kept copy here would let a routing change pass unnoticed. Two such copies existed until
# 2026-10-04 and had already drifted (gpt-6-astra vs Opus, agy vs deepseek-flash).
ENGINES = {c: v.get("engine", "") for c, v in TYPES["categories"].items()}


def builder_cats(cats: list, builds: bool) -> list:
    known = TYPES["categories"]
    return [c for c in cats if known.get(c, {}).get("product") == "yes"
            or (builds and known.get(c, {}).get("product") == "mixed")]



def five_things(cat: str, nid: str, engine: str, types: dict) -> dict:
    """The five things as fields, not as a list of their names (2026-10-05).

    `intake.js` had defined these fields all along; the gate now reads them, so the harness emits them. `stop`
    carries method 3.6's three parts.
    """
    row = types["categories"].get(cat, {})
    return {
        "brief_given": row.get("pattern") or f"the brief for {cat}",
        "intent": f"{cat}: one bounded piece",
        "stop": {"criteria": row.get("check") or f"the check for {cat} passes",
                 "baseline": "everything the baseline recorded as passing still passes",
                 "must_not_change": "paths outside the design's may_change set"},
        "returns": "the node's result file",
        "state_reads": "the state file",
        "tools": [engine.split()[0]],
        "evidence": [f"runs/<runId>/nodes/{nid}.result.md"],
    }


def _five(n: dict) -> dict:
    """The five contents for an inline fixture node."""
    return five_things(n.get("category", ""), str(n.get("id")), n.get("engine", ""), TYPES)

def design_for(entry: dict) -> dict:
    exp = entry["expected"]
    cats = exp["categories"]
    known = TYPES["categories"]
    nodes, prev = [], None
    for i, c in enumerate(cats):
        n = {"id": f"n{i + 1}", "category": c, "engine": ENGINES[c],
             "check": (known[c].get("check") or f"a check for {c}"),
             **five_things(c, f"n{i + 1}", ENGINES.get(c, "claude sonnet 5.5"), TYPES),
             "sabotage": known[c].get("sabotage") or "",
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
                      **five_things("code review", f"nr{i + 1}", rev, TYPES),
                      "needs": [prev] if prev else []})
    return {"categories": cats, "builds": exp["builds"],
            "baseline": ({"command": "env -u NO_COLOR python3 -m pytest -q", "captured_by": "script"}
                         if exp["builds"] else None),
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


def test_parse_types_marks_loop_from_the_pattern_column(tmp_path):
    p = tmp_path / "TASK_TYPES.md"
    p.write_text("| Category | Touches product | Default pattern | Default engine | Default check | Sabotage (proof the check can fail) |\n"
                 "|---|---|---|---|---|---|\n"
                 "| custom iterative work | no | bounded LOOP | codex | check | sabotage |\n"
                 "| code generation | yes | step | codex | check | sabotage |\n")
    cats = dg.parse_types(p)["categories"]
    assert cats["custom iterative work"]["loop"] is True
    assert cats["code generation"]["loop"] is False
    assert cats["custom iterative work"]["pattern"] == "bounded LOOP"


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
                    "check": "repro test red before, green after",
                     "sabotage": "revert the fix → red again",
                     **five_things("debugging", "n1", "codex gpt-6.1-sol", TYPES), "needs": [],
                    "loop": {"limit": 2, "exit": "fresh node stronger tier", "feedback": "test output"}}],
         "design_source": "default"}
    assert dg.validate_design(d, TYPES) == []
    d2 = json.loads(json.dumps(d)); d2["builds"] = True; d2["baseline"] = {"command": "pytest", "captured_by": "script"}; d2["touched_paths"] = ["engine/x.py"]
    assert any(x.startswith("G6") for x in dg.validate_design(d2, TYPES))
    d2["nodes"].append({"id": "nr", "category": "code review", "engine": "claude sonnet 5.5",
                        "check": "fixed checklist",
                        **five_things("code review", "nr", "claude sonnet 5.5", TYPES), "needs": ["n1"]})
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
    d = json.loads(json.dumps(base)); d["nodes"][0].pop("intent", None)
    assert any(x.startswith("G3") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["nodes"][0]["stop"] = {"criteria": "only one part"}
    assert any(x.startswith("G3") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["nodes"][0]["loop"] = {"limit": 0, "exit": "x", "feedback": "y"}
    assert any(x.startswith("G3") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["nodes"][0]["needs"] = ["ghost"]
    assert any(x.startswith("G4") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["pipeline"] = "not-a-pipeline"
    assert any(x.startswith("G4") for x in dg.validate_design(d, TYPES))
    d = json.loads(json.dumps(base)); d["categories"] = ["frobnicate"]
    assert any(x.startswith("G1") for x in dg.validate_design(d, TYPES))


def routing_rows() -> list[str]:
    """The category labels in EXECUTOR_KINDS.md's routing table, split on commas only.

    Commas only, because category names contain "and" (`document and explain`, `research and reports`).
    """
    text = (ROOT / "docs" / "EXECUTOR_KINDS.md").read_text().splitlines()
    starts = [i for i, l in enumerate(text) if l.startswith("| Category | Engine | Basis |")]
    assert len(starts) == 1, f"expected one category-keyed routing table, found {len(starts)}"
    labels = []
    for line in text[starts[0] + 1:]:
        if not line.startswith("|"):
            break
        if line.startswith("|---"):
            continue
        labels += [c.strip().strip("*").strip("`") for c in line.split("|")[1].split(",") if c.strip()]
    return labels


def test_the_routing_table_is_keyed_by_category_and_nothing_else():
    """One row per TASK_TYPES category: the same 16, no more and no fewer.

    This is the structural fix for a real confusion. EXECUTOR_KINDS' routing table had four rows naming things that
    are **not** categories — "complex debugging and root-cause analysis" and "algorithm and solution design" (rule 3
    phrases), "configuration files, folder structure" (rule 2), and a daily-work catch-all — and it had no row for
    `others`. Because `algorithm and solution design` shared a row with `multi step planning`, EJ's instruction that
    planning runs on deepseek-flash read as if it overrode rule 3. Two vocabularies in one table is the defect; this
    assertion keeps them apart.
    """
    assert sorted(routing_rows()) == sorted(TYPES["categories"]), (
        "the routing table must name every TASK_TYPES category exactly once, and nothing else")


def test_every_row_in_the_table_has_a_classifiable_engine():
    """No row may be invisible to the kind rules.

    `design_gate._KINDS` is a hand-kept list of engine tokens, and an engine missing from it makes every row
    routed to it classify as `unknown` — which silently disarms G6's different-kind rule for that work. Two
    engines were added in one day (opencode, deepseek) and each exposed exactly this, with the DeepSeek tier
    invisible from the start. This is the check that would have caught both.
    """
    placeholder = {"", "-", "—", "n/a", "none"}          # `others` is a catch-all and names no engine
    unknown = {c: v.get("engine", "") for c, v in TYPES["categories"].items()
               if v.get("engine", "").strip().lower() not in placeholder
               and dg.engine_kind(v.get("engine", "")) == "unknown"}
    assert unknown == {}, f"rows the gate cannot classify: {unknown}"


def test_reviewer_kind_rule():
    base = design_for(next(x for x in CORPUS if x["id"] == "t02-codegen-flag"))
    d = json.loads(json.dumps(base))
    d["nodes"] = [n for n in d["nodes"] if n["category"] != "code review"]
    assert any(x.startswith("G6") for x in dg.validate_design(d, TYPES)), \
        "a building node with no reviewer must be G6"

    # G6 fires when the reviewer is the SAME KIND as the builder, so the reviewer's engine must be read from the
    # builder's rather than hardcoded. This broke on 2026-10-04: the build rows became two-engine cells
    # ("opencode ... + Codex ...") and began classifying as opencode, so a hardcoded codex reviewer was correctly
    # a different kind and the finding stopped firing.
    d = json.loads(json.dumps(base))
    kinds = [dg.engine_kind(n["engine"]) for n in d["nodes"]]
    kind = next((k for k in kinds if k in ("codex", "opencode")), "codex")
    same_kind = {"codex": "codex gpt-6-astra", "opencode": "opencode MiniMax-M3.1-Flash-Preview",
                 "claude": "claude sonnet 5.5", "agy": "agy gemini-3.1-pro-high"}[kind]
    for n in d["nodes"]:
        if n["category"] == "code review":
            n["engine"] = same_kind
    assert any(x.startswith("G6") for x in dg.validate_design(d, TYPES)), \
        f"a {kind} reviewer for a {kind} builder must be G6"


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
              "check": "checklist against source; LF endings",
              "sabotage": "plant a wrong command → the checklist rejects it",
              **five_things("document and explain", "n1", "claude sonnet 5.5", TYPES), "needs": []}
    same = {"id": "n1r", "category": "code review", "engine": "claude sonnet 5.5",
            "check": "review against source",
            **five_things("code review", "n1r", "claude sonnet 5.5", TYPES), "needs": ["n1"]}
    other = dict(same, engine="codex gpt-6.1-sol")
    base = {"categories": ["document and explain"], "builds": True, "touched_paths": ["docs/cmds.sh"],
            "baseline": {"command": "env -u NO_COLOR python3 -m pytest -q", "captured_by": "script"},
            "pipeline": None, "design_source": "default"}
    assert any(x.startswith("G6") for x in dg.validate_design(dict(base, nodes=[writer, same]), TYPES))
    assert dg.validate_design(dict(base, nodes=[writer, other]), TYPES) == []


def test_reviewer_kind_not_diluted_by_mixed_builders():
    # round-3 blind-review catch (p274): pure builders are codex, a mixed builder is claude —
    # the blend must not make a codex reviewer acceptable
    d = {"categories": ["test data gen", "test script gen"], "builds": True,
         "baseline": {"command": "env -u NO_COLOR python3 -m pytest -q", "captured_by": "script"},
         "touched_paths": ["tests/x"], "pipeline": None,
         "nodes": [
             {"id": "n1", "category": "test data gen", "engine": "claude sonnet 5.5",
              "check": "schema validation", "sabotage": "corrupt a field → the schema rejects it",
               **five_things("test data gen", "n1", "claude sonnet 5.5", TYPES), "needs": []},
             {"id": "n2", "category": "test script gen", "engine": "codex gpt-6.1-sol",
              "check": "seeded failure detected", "sabotage": "seed a failure → the script exits non-zero",
               **five_things("test script gen", "n2", "codex gpt-6.1-sol", TYPES), "needs": ["n1"],
              "loop": {"limit": 2, "exit": "stronger tier", "feedback": "output"}},
             {"id": "nr", "category": "code review", "engine": "codex gpt-6-astra",
              "check": "fixed checklist",
              **five_things("code review", "nr", "codex gpt-6-astra", TYPES), "needs": ["n2"]}],
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
