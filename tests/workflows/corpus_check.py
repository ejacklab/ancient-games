#!/usr/bin/env python3
"""corpus_check.py — the campaign harness: corpus × results × TASK_TYPES × design_gate.

Deterministic. Judgment (categorization) happens outside; this script compares, builds the
default design for each categorization, runs design_gate over it, and classifies bugs:

  MISMATCH  result categorization differs from the corpus expectation
  GAP       a category (expected or produced) is not in docs/TASK_TYPES.md
  BUILDER   the harness has no default engine/loop entry for a category in the table
  GATE      design_gate findings on the design built from the result
  EXEC      (with --compare) an executor sample disagrees with the corpus expectation

Usage:
  corpus_check.py --corpus r1.jsonl --results results_r1.jsonl [--out report.md]
  corpus_check.py ... --compare results_codex.jsonl --label codex
  corpus_check.py ... --emit-designs DIR        (round 3: write the generated designs)
Exit: 0 = no bugs, 1 = bugs (report lists them), 2 = usage error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / ".claude" / "skills" / "workflow-design" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import design_gate as dg  # noqa: E402

FIVE = sorted(dg.FIVE)
# Builder defaults per category (concrete engine ids per EXECUTOR_KINDS; the table's cell is prose).
# Derived from docs/TASK_TYPES.md via design_gate, not hand-kept: this file and test_task_types.py held
# the same 16-entry copy until 2026-10-04, and both had drifted from the table they were meant to mirror.
TYPES = dg.parse_types(ROOT / "docs" / "TASK_TYPES.md")
# `others` has no engine by design: the table's cell is a dash, meaning "no default — the full method
# from first principles" (TASK_TYPES.md:103). Passing that placeholder through produced nodes whose engine
# was literally a dash (found 2026-10-05, now caught by design_gate.py G11). The harness is not the method,
# so it must pick one and say which.
NO_DEFAULT_ENGINE = "deepseek deepseek-flash"   # cheap and general; the method's "first principles"
ENGINES = {c: (v.get("engine") if v.get("engine") not in ("", "—") else NO_DEFAULT_ENGINE)
           for c, v in TYPES["categories"].items()}
LOOP_CATS = {"code generation", "debugging", "ui/ux dev", "test script gen"}


def load_jsonl(path: Path) -> list[dict]:
    out = []
    for i, line in enumerate(Path(path).read_text(errors="replace").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError as e:
            out.append({"id": f"{Path(path).name}:{i}", "PARSE_ERROR": str(e)})
    return out


def index_by_id(rows: list[dict]) -> dict:
    return {r["id"]: r for r in rows if "id" in r}


def builder_cats(cats: list[str], builds: bool, types: dict) -> list[str]:
    known = types["categories"]
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

def build_design(cats: list[str], builds: bool, pipeline: str | None, types: dict,
                 tiny: bool = False) -> dict:
    known = types["categories"]
    nodes, prev = [], None
    for i, c in enumerate(cats):
        n = {"id": f"n{i + 1}", "category": c, "engine": ENGINES.get(c, "claude sonnet 5.5"),
             "check": (known[c].get("check") or f"a check for {c}"),
             **five_things(c, f"n{i + 1}", ENGINES.get(c, "claude sonnet 5.5"), types),
             "sabotage": known[c].get("sabotage") or "",
             "needs": [prev] if prev else []}
        if c in LOOP_CATS:
            n["loop"] = {"limit": 2, "exit": "fresh node on stronger tier with handoff note",
                         "feedback": "the check's real output"}
        nodes.append(n)
        prev = n["id"]
        if c == "document and explain" and not tiny:
            # the row's default pattern is "single node + review against source" — the review is a node;
            # when the document piece is itself a builder, the reviewer must be a different kind (G6)
            doc_rev = "codex gpt-6.1-sol" if builds else "claude sonnet 5.5"
            nodes.append({"id": f"n{i + 1}r", "category": "code review", "engine": doc_rev,
                          "check": "review against source: fixed checklist, facts traceable",
                          **five_things("code review", f"n{i + 1}r", doc_rev, types),
                          "needs": [prev], "reviews": [f"n{i + 1}"]})
            prev = f"n{i + 1}r"
    b_cats = builder_cats(cats, builds, types)
    b_nodes = [n for n in nodes if n["category"] in b_cats]
    covered = set()
    for n in nodes:
        if n["category"] == "code review":
            covered |= set(n.get("reviews", []))
    # a build group spanning engine kinds gets one reviewer per kind group — no single reviewer
    # can be different-kind from both (round-3, p195/p273)
    groups: dict = {}
    for n in b_nodes:
        if n["id"] not in covered:
            groups.setdefault(dg.engine_kind(n["engine"]), []).append(n["id"])
    for i, (k, ids) in enumerate(sorted(groups.items())):
        rev = "codex gpt-6.1-sol" if k != "codex" else "claude sonnet 5.5"
        nodes.append({"id": f"nr{i + 1}", "category": "code review", "engine": rev,
                      "check": "fixed checklist; findings with file:line",
                      **five_things("code review", f"nr{i + 1}", rev, types),
                      "needs": [prev] if prev else [],
                      "reviews": ids})
        prev = f"nr{i + 1}"
    if (pipeline or "").strip().lower() == "grade → fix → regrade":
        # the pipeline's recheck verb gets its own node (round-3 blind-review catch, p279)
        nodes.append({"id": "nrg", "category": "grade a run",
                      "engine": ENGINES.get("grade a run", "claude sonnet 5.5"),
                      "check": "regrade verdict on the same rubric; a surviving FAIL goes to EJ",
                      **five_things("code review", f"nr{i + 1}", rev, types),
                      "needs": [prev] if prev else []})
    base = {"command": "env -u NO_COLOR python3 -m pytest -q", "captured_by": "script"}
    return {"baseline": base if builds else None, "categories": cats, "builds": builds,
            "touched_paths": (["product/x"] if builds else []),
            "pipeline": pipeline, "nodes": nodes,
            "design_source": "default", "estimate": {"tokens": 100000}}


def check_round(corpus: list[dict], results: dict, types: dict, emit: Path | None) -> list[dict]:
    bugs = []
    known = types["categories"]
    for e in corpus:
        pid = e["id"]
        exp = e["exp"]
        r = results.get(pid)
        if r is None:
            bugs.append({"id": pid, "class": "MISMATCH", "detail": "no result row"})
            continue
        if "PARSE_ERROR" in r:
            bugs.append({"id": pid, "class": "MISMATCH", "detail": r["PARSE_ERROR"]})
            continue
        r_cats = [c.strip().lower() for c in r.get("cats", [])]
        e_cats = [c.strip().lower() for c in exp.get("cats", [])]
        for c in set(e_cats) | set(r_cats):
            if c not in known:
                bugs.append({"id": pid, "class": "GAP", "detail": f"category {c!r} not in TASK_TYPES.md"})
        if set(r_cats) != set(e_cats):
            bugs.append({"id": pid, "class": "MISMATCH",
                         "detail": f"cats result={r_cats} expected={e_cats}"})
        if bool(r.get("tiny")) != bool(exp.get("tiny")):
            bugs.append({"id": pid, "class": "MISMATCH",
                         "detail": f"tiny result={r.get('tiny')} expected={exp.get('tiny')}"})
        if bool(r.get("builds")) != bool(exp.get("builds")):
            bugs.append({"id": pid, "class": "MISMATCH",
                         "detail": f"builds result={r.get('builds')} expected={exp.get('builds')}"})
        r_pipe = (r.get("pipe") or None)
        e_pipe = (exp.get("pipe") or None)
        if e_pipe and r_pipe != e_pipe:
            bugs.append({"id": pid, "class": "MISMATCH",
                         "detail": f"pipeline result={r_pipe!r} expected={e_pipe!r}"})
        for c in r_cats:
            if c in known and c not in ENGINES:
                bugs.append({"id": pid, "class": "BUILDER", "detail": f"no builder engine for {c!r}"})
        # gate the design built from the result categorization
        if r_cats or (exp.get("tiny") and not r_cats):
            d = build_design(r_cats, bool(r.get("builds")), r_pipe, types, tiny=bool(r.get("tiny")))
            findings = dg.validate_design(d, types) if r_cats else []
            for x in findings:
                bugs.append({"id": pid, "class": "GATE", "detail": x})
            if emit is not None:
                emit.mkdir(parents=True, exist_ok=True)
                (emit / f"{pid}.json").write_text(json.dumps(d, indent=1))
    return bugs


def compare_exec(corpus: list[dict], exec_rows: dict, label: str, lenient: bool = False) -> tuple[list[dict], int, int]:
    bugs, agree, total = [], 0, 0
    for e in corpus:
        pid = e["id"]
        r = exec_rows.get(pid)
        if r is None or "PARSE_ERROR" in r:
            continue
        total += 1
        exp = e["exp" if "exp" in e else "expected"]
        e_cats = {c.strip().lower() for c in exp.get("cats", exp.get("categories", []))}
        r_cats = {c.strip().lower() for c in r.get("cats", [])}
        if lenient:
            # subset agreement: every expected label present (extra secondary labels tolerated);
            # tiny must match; builds tolerated when the prompt's deliverable is a findings/report file
            same = (e_cats <= r_cats and bool(r.get("tiny")) == bool(exp.get("tiny")))
        else:
            same = (r_cats == e_cats and bool(r.get("tiny")) == bool(exp.get("tiny"))
                    and bool(r.get("builds")) == bool(exp.get("builds")))
        if same:
            agree += 1
        else:
            bugs.append({"id": pid, "class": "EXEC",
                         "detail": f"{label}: result={sorted(r_cats)} tiny={r.get('tiny')} "
                                   f"builds={r.get('builds')} | expected={sorted(e_cats)} "
                                   f"tiny={exp.get('tiny')} builds={exp.get('builds')}"})
    return bugs, agree, total


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", action="append", required=True)
    ap.add_argument("--results", required=True)
    ap.add_argument("--types", default=str(ROOT / "docs" / "TASK_TYPES.md"))
    ap.add_argument("--compare", action="append", default=[])
    ap.add_argument("--label", action="append", default=[])
    ap.add_argument("--lenient", action="store_true",
                    help="compare mode: subset agreement on labels, builds tolerated (round-1 rules absent)")
    ap.add_argument("--emit-designs", metavar="DIR")
    ap.add_argument("--out", metavar="FILE")
    a = ap.parse_args(argv)
    types = dg.parse_types(Path(a.types))
    global ENGINES
    # the same substitution as at module level — this local copy shadowed it and kept passing the dash
    ENGINES = {c: (v.get("engine") if v.get("engine") not in ("", "\u2014") else NO_DEFAULT_ENGINE)
               for c, v in types["categories"].items()}
    corpus = [e for f in a.corpus for e in load_jsonl(Path(f))]
    results = index_by_id(load_jsonl(Path(a.results)))
    emit = Path(a.emit_designs) if a.emit_designs else None
    bugs = check_round(corpus, results, types, emit)
    exec_lines = []
    for i, cf in enumerate(a.compare):
        label = a.label[i] if i < len(a.label) else Path(cf).stem
        eb, agree, total = compare_exec(corpus, index_by_id(load_jsonl(Path(cf))), label, a.lenient)
        bugs += eb
        exec_lines.append(f"- {label}: agreement {agree}/{total}"
                          + (f" ({agree / total:.0%})" if total else ""))
    counts: dict[str, int] = {}
    for b in bugs:
        counts[b["class"]] = counts.get(b["class"], 0) + 1
    lines = [f"# corpus_check — {len(corpus)} prompts, results {Path(a.results).name}", "",
             f"bugs: {len(bugs)} " + (json.dumps(counts) if counts else "(none)"), ""]
    lines += exec_lines + [""] if exec_lines else []
    for b in bugs:
        lines.append(f"- [{b['class']}] {b['id']}: {b['detail']}")
    report = "\n".join(lines) + "\n"
    if a.out:
        Path(a.out).write_text(report)
    print(report, end="")
    return 1 if bugs else 0


if __name__ == "__main__":
    sys.exit(main())
