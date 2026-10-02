#!/usr/bin/env python3
"""design_gate.py — the script layer of the default-first design rule (docs/TASK_TYPES.md).

Deterministic checks on a workflow design JSON. Judgment is NOT done here: the second layer is a
fixed-checklist reviewer (Sonnet 5.5; a different kind from the designer when the design builds or is
high-risk). The category table's single source is docs/TASK_TYPES.md — parsed here, never copied.

Findings are named:
  G1 category unknown
  G2 category-vs-facts guard (wrong category is a stop, not a repair; "others" is exempt)
  G3 node rules: a check, the five things, loops with limit+exit+feedback
  G4 edges: needs must exist, no cycles, pipeline name valid
  G5 challenger: claim >= 20%, arithmetic matches the estimates, coverage equal to the default
  G6 a design with building nodes carries a reviewer; single-kind builders get a different-kind reviewer
  G7 ledger rows carry every field the reconciliation needs

Usage:
  design_gate.py design.json [--types PATH]
  design_gate.py --ledger-row row.json [--types PATH]
  design_gate.py --self-test
Exit: 0 no findings, 1 findings, 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FIVE = {"tools", "context", "contract", "evidence", "state"}
LEDGER_KEYS = ["date", "run_id", "category", "design_source", "claimed_margin", "basis",
               "projected_cost", "actual_cost", "coverage_result", "reconciled"]
LEDGER_FIELDS = LEDGER_KEYS
_KINDS = (("codex", "codex"), ("gpt", "codex"), ("claude", "claude"), ("sonnet", "claude"),
          ("opus", "claude"), ("haiku", "claude"), ("agy", "agy"), ("gemini", "agy"), ("qwen", "qwen"))


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def engine_kind(engine: str) -> str:
    e = (engine or "").lower()
    for tok, kind in _KINDS:
        if e.startswith(tok) or f" {tok}" in e:
            return kind
    return "unknown"


def _table_rows(md: list[str], header_first_cell: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_tbl = False
    for line in md:
        s = line.strip()
        if not in_tbl:
            if s.startswith("|") and s.lstrip("|").strip().lower().startswith(header_first_cell.lower()):
                in_tbl = True
            continue
        if not s.startswith("|"):
            break
        if set(s) <= set("|-: "):
            continue
        rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows


def parse_types(path: Path) -> dict:
    md = Path(path).read_text(errors="replace").splitlines()
    cats: dict[str, dict] = {}
    for r in _table_rows(md, "Category"):
        if len(r) < 6:
            continue
        name = r[0].strip().strip("*").lower()
        prod = r[1].strip().lower()
        product = "yes" if prod.startswith("yes") else ("mixed" if prod.startswith("mixed") else "no")
        cats[name] = {"product": product, "touches_product": product == "yes",
                      "pattern": r[2], "engine": r[3], "check": r[4], "sabotage": r[5]}
    pipes: dict[str, dict] = {}
    for r in _table_rows(md, "Pipeline"):
        if len(r) < 4:
            continue
        pipes[r[0].strip().lower()] = {"nodes": r[1], "loop": r[2], "join": r[3]}
    return {"categories": cats, "pipelines": pipes, "path": str(path)}


def _has_cycle(nodes: list[dict]) -> bool:
    by_id = {n.get("id"): n for n in nodes}
    color = {i: 0 for i in by_id}

    def dfs(u: str) -> bool:
        color[u] = 1
        for v in by_id[u].get("needs", []) or []:
            if v not in color:
                continue
            if color[v] == 1 or (color[v] == 0 and dfs(v)):
                return True
        color[u] = 2
        return False

    return any(color[i] == 0 and dfs(i) for i in color)


def _cat(node: dict) -> str:
    return (node.get("category") or "").strip().lower()


def validate_design(d: dict, types: dict) -> list[str]:
    f: list[str] = []
    known = types["categories"]
    cats = [c.strip().lower() for c in d.get("categories", [])]
    for c in cats:
        if c not in known:
            f.append(f"G1: unknown category {c!r}")
    builds = bool(d.get("builds"))
    touched = d.get("touched_paths") or []
    building_cats = [c for c in cats if known.get(c, {}).get("product") in ("yes", "mixed")]
    if (builds or touched) and cats and not building_cats and "others" not in cats:
        f.append("G2: category-vs-facts: the design builds or touches product paths but carries no "
                 "building category — a wrong category is a stop, not a repair")
    pure_yes = [c for c in cats if known.get(c, {}).get("product") == "yes"]
    if pure_yes and not builds and not touched:
        f.append(f"G2: category {pure_yes[0]!r} always writes product, but the design claims it touches "
                 f"none (a mixed category may run read-only; a yes category may not)")
    nodes = d.get("nodes") or []
    ids = {n.get("id") for n in nodes}
    for n in nodes:
        nid = n.get("id", "?")
        if not (n.get("check") or "").strip():
            f.append(f"G3: node {nid} has no check")
        missing = FIVE - {str(x).lower() for x in n.get("five_things", [])}
        if missing:
            f.append(f"G3: node {nid} is missing {sorted(missing)}")
        lp = n.get("loop")
        if lp is not None:
            if not isinstance(lp.get("limit"), int) or lp["limit"] < 1:
                f.append(f"G3: node {nid} loop has no attempt limit")
            if not (lp.get("exit") or "").strip():
                f.append(f"G3: node {nid} loop has no exit for the limit")
            if not (lp.get("feedback") or "").strip():
                f.append(f"G3: node {nid} loop has no specific feedback")
    for n in nodes:
        for dep in n.get("needs", []) or []:
            if dep not in ids:
                f.append(f"G4: node {n.get('id')} needs unknown node {dep!r}")
    if _has_cycle(nodes):
        f.append("G4: dependency cycle")
    pipe = (d.get("pipeline") or "").strip().lower()
    if pipe and pipe not in types["pipelines"]:
        f.append(f"G4: unknown pipeline {pipe!r}")
    src = d.get("design_source", "default")
    if isinstance(src, dict):
        if src.get("type") != "challenger":
            f.append("G5: a design_source object must be type 'challenger'")
        claim = src.get("claim_margin")
        if not isinstance(claim, (int, float)) or isinstance(claim, bool) or claim < 0.20:
            f.append("G5: challenger claim must be a number >= 0.20")
        if not (src.get("basis") or "").strip():
            f.append("G5: challenger claim has no basis")
        est = (d.get("estimate") or {}).get("tokens")
        dest = (d.get("default_estimate") or {}).get("tokens")
        if isinstance(est, (int, float)) and isinstance(dest, (int, float)) and dest > 0:
            recomputed = (dest - est) / dest
            if recomputed < 0.20:
                f.append(f"G5: recomputed margin {recomputed:.2f} < 0.20")
            elif isinstance(claim, (int, float)) and abs(claim - recomputed) > 0.01:
                f.append(f"G5: margin arithmetic: claim {claim} != recomputed {recomputed:.3f}")
        else:
            f.append("G5: challenger without estimate/default_estimate tokens — the arithmetic cannot be checked")
        cov, dcov = d.get("coverage") or {}, d.get("default_coverage") or {}
        if (set(cov.get("criteria", [])) != set(dcov.get("criteria", []))
                or set(cov.get("checks", [])) != set(dcov.get("checks", []))):
            f.append("G5: coverage differs from the default — coverage is a gate, not an axis")
    builders = [n for n in nodes
                if known.get(_cat(n), {}).get("product") == "yes"
                or (builds and known.get(_cat(n), {}).get("product") == "mixed")]
    if builders:
        reviewers = [n for n in nodes if _cat(n) == "code review"]
        if not reviewers:
            f.append("G6: a design with building nodes has no review node")
        else:
            builder_ids = [b.get("id") for b in builders]
            for r in reviewers:
                rk = engine_kind(r.get("engine", ""))
                targets = r.get("reviews") or builder_ids  # no pairing → reviewed against all builders
                t_nodes = [n for n in nodes if n.get("id") in set(targets)]
                t_kinds = {engine_kind(t.get("engine", "")) for t in t_nodes}
                yes_kinds = {engine_kind(t.get("engine", "")) for t in t_nodes
                             if known.get(_cat(t), {}).get("product") == "yes"}
                # a reviewer must be a different kind from what it reviews; when its targets span
                # kinds, the pure builders are the constraint (round-3, p195)
                constraint = t_kinds if len(t_kinds) == 1 else (yes_kinds or t_kinds)
                if rk == "unknown" or rk in constraint:
                    f.append(f"G6: reviewer engine {r.get('engine')!r} is not a different kind from "
                             f"what it reviews ({sorted(constraint)})")
    return f


def parse_ledger(path: Path) -> list[dict]:
    """Read the markdown ledger table into row dicts (columns = LEDGER_KEYS, in order)."""
    rows = []
    for r in _table_rows(Path(path).read_text(errors="replace").splitlines(), "Date"):
        if len(r) < len(LEDGER_KEYS):
            continue
        row = dict(zip(LEDGER_KEYS, r))
        try:
            row["claimed_margin"] = float(row["claimed_margin"])
        except ValueError:
            pass  # "—" for a default row stays a string
        row["reconciled"] = row["reconciled"].strip().lower() in ("yes", "true")
        rows.append(row)
    return rows


def validate_ledger_row(row: dict) -> list[str]:
    f = [f"G7: ledger row is missing {k!r}" for k in LEDGER_FIELDS if k not in row]
    ds = row.get("design_source")
    if ds is not None and ds not in ("default", "challenger"):
        f.append("G7: design_source must be 'default' or 'challenger'")
    if ds == "challenger":
        if not str(row.get("basis") or "").strip() or row.get("basis") == "—":
            f.append("G7: a challenger row without a basis")
        cm = row.get("claimed_margin")
        if not isinstance(cm, (int, float)) or isinstance(cm, bool) or cm < 0.20:
            f.append("G7: a challenger row needs a claimed margin >= 0.20")
    if row.get("reconciled") in (True, "yes") and not str(row.get("actual_cost") or "").strip():
        f.append("G7: a reconciled row without an actual cost")
    return f


def _good_design() -> dict:
    five = sorted(FIVE)
    return {
        "categories": ["research and reports", "code generation"],
        "builds": True, "touched_paths": ["x.py"], "pipeline": "research → codegen",
        "nodes": [
            {"id": "n1", "category": "research and reports", "engine": "codex gpt-6.1-sol",
             "check": "questions answered (fixed checklist)", "five_things": five, "needs": []},
            {"id": "n2", "category": "code generation", "engine": "codex gpt-6.1-sol",
             "check": "pytest -q green", "five_things": five, "needs": ["n1"],
             "loop": {"limit": 2, "exit": "fresh node on stronger tier", "feedback": "the check's real output"}},
            {"id": "n3", "category": "code review", "engine": "claude sonnet 5.5",
             "check": "fixed checklist; findings with file:line", "five_things": five, "needs": ["n2"]}],
        "design_source": "default", "estimate": {"tokens": 100000},
    }


def self_test(types_path: Path) -> int:
    types = parse_types(types_path)
    if len(types["categories"]) < 14 or "others" not in types["categories"]:
        print(f"self-test FAIL: parsed {len(types['categories'])} categories from {types_path}")
        return 1
    import copy
    ok = True

    def expect(label, design, want_prefix):
        nonlocal ok
        findings = validate_design(design, types)
        hit = any(x.startswith(want_prefix) for x in findings)
        if want_prefix is None:
            hit = not findings
        print(f"{'ok  ' if hit else 'FAIL'} self-test: {label}")
        ok = ok and hit

    expect("a good design passes clean", _good_design(), None)
    d = copy.deepcopy(_good_design()); d["categories"] = ["research and reports"]
    expect("research-only categories on a building design -> G2", d, "G2")
    d = copy.deepcopy(_good_design()); d["categories"] = ["others"]
    expect("others may build (exempt) -> clean", d, None)
    d = copy.deepcopy(_good_design()); d["nodes"][1]["check"] = ""
    expect("a node without a check -> G3", d, "G3")
    d = copy.deepcopy(_good_design()); d["nodes"][1]["loop"] = {"exit": "x", "feedback": "y"}
    expect("a loop without a limit -> G3", d, "G3")
    d = copy.deepcopy(_good_design()); d["nodes"][2]["needs"] = ["nope"]
    expect("an edge to a missing node -> G4", d, "G4")
    d = copy.deepcopy(_good_design()); d["nodes"][0]["needs"] = ["n3"]
    expect("a cycle -> G4", d, "G4")
    d = copy.deepcopy(_good_design()); d["nodes"][2]["engine"] = "codex gpt-6-astra"
    expect("a same-kind reviewer on builders -> G6", d, "G6")
    d = copy.deepcopy(_good_design()); d["nodes"] = d["nodes"][:2]
    expect("builders without a reviewer -> G6", d, "G6")
    d = copy.deepcopy(_good_design())
    d["design_source"] = {"type": "challenger", "claim_margin": 0.19, "basis": "b"}
    d["default_estimate"] = {"tokens": 100000}
    d["coverage"] = d["default_coverage"] = {"criteria": ["R1.1"], "checks": ["pytest -q"]}
    expect("a 19% claim -> G5", d, "G5")
    d["design_source"] = {"type": "challenger", "claim_margin": 0.30, "basis": "b"}
    d["estimate"] = {"tokens": 90000}
    expect("margin arithmetic lie (claim .30, recomputed .10) -> G5", d, "G5")
    d = copy.deepcopy(_good_design())
    d["design_source"] = {"type": "challenger", "claim_margin": 0.25, "basis": "b"}
    d["estimate"] = {"tokens": 75000}; d["default_estimate"] = {"tokens": 100000}
    d["coverage"] = {"criteria": ["R1.1"], "checks": ["pytest -q"]}
    d["default_coverage"] = {"criteria": ["R1.1", "R1.2"], "checks": ["pytest -q"]}
    expect("coverage not equal -> G5 even with a real margin", d, "G5")
    row = {k: "x" for k in LEDGER_FIELDS}
    row.update({"design_source": "challenger", "claimed_margin": 0.25, "reconciled": True})
    findings = validate_ledger_row(row)
    print(f"{'ok  ' if not findings else 'FAIL'} self-test: a full challenger ledger row passes")
    ok = ok and not findings
    row2 = dict(row); row2["basis"] = "—"
    hit = any(x.startswith("G7") for x in validate_ledger_row(row2))
    print(f"{'ok  ' if hit else 'FAIL'} self-test: a challenger row without a basis -> G7")
    ok = ok and hit
    print("self-test:", "PASS — the gate can fail" if ok else "FAIL")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Script layer of the default-first design rule.")
    ap.add_argument("design", nargs="?", help="design JSON file")
    ap.add_argument("--types", default=str(repo_root() / "docs" / "TASK_TYPES.md"))
    ap.add_argument("--ledger-row", metavar="JSON", help="validate one ledger row JSON file")
    ap.add_argument("--ledger", metavar="FILE", help="validate every row of a markdown ledger table")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test(Path(a.types))
    if not a.design and not a.ledger_row and not a.ledger:
        ap.error("pass a design JSON, --ledger-row, --ledger, or --self-test")
    types = parse_types(Path(a.types))
    findings: list[str] = []
    if a.ledger_row:
        findings += validate_ledger_row(json.loads(Path(a.ledger_row).read_text()))
    if a.ledger:
        for i, row in enumerate(parse_ledger(Path(a.ledger)), 1):
            findings += [f"row {i}: {x}" for x in validate_ledger_row(row)]
    if a.design:
        findings += validate_design(json.loads(Path(a.design).read_text()), types)
    for x in findings:
        print("finding:", x)
    print("PASS" if not findings else f"FAIL: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
