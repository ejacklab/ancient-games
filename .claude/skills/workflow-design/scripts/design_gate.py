#!/usr/bin/env python3
"""design_gate.py — the script layer of the default-first design rule (docs/TASK_TYPES.md).

Deterministic checks on a workflow design JSON. Judgment is NOT done here: the second layer is a
fixed-checklist reviewer (Sonnet 5.5; a different kind from the designer when the design builds or is
high-risk). The category table's single source is docs/TASK_TYPES.md — parsed here, never copied.

Findings are named:
  G1 category unknown
  G2 category-vs-facts guard (wrong category is a stop, not a repair; "others" is exempt), and the
     claim/evidence pair: a design that says it builds must name a product path it touches
  G3 node rules: a check, the five things, loops with limit+exit+feedback
  G4 edges: needs must exist, no cycles, pipeline name valid
  G5 challenger: claim >= 20%, arithmetic matches the estimates, coverage equal to the default
  G6 a design with building nodes carries a reviewer; single-kind builders get a different-kind reviewer
  G7 ledger rows carry every field the reconciliation needs
  G9 a building node carries the sabotage that proves its check can fail
  G10 a design that builds carries `baseline.command` and names the node that captures it
  G11 a node names a real engine, not the table's `—` placeholder
  G12 `baseline.command` and `touched_paths` hold values, not promises to fill them in later
  G13 an `others` piece is resolved by an explore node before it is the first thing to run
  G8 labels agree: the design's categories equal the categories its nodes carry (method 3.2: the piece
     labels replace the provisional category, so a claimed category no node carries, or a node category
     the design does not claim, means the relabelling did not happen; the in-run `code review` node that G6
     requires is exempt from the second direction)

Usage:
  design_gate.py design.json [--types PATH]
  design_gate.py --ledger-row row.json [--types PATH]
  design_gate.py --self-test
Exit: 0 no findings, 1 findings, 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# (No `FIVE` set here any more. It named the five things and was read by nothing once `check_five` started testing
# the *contents* — the same "defined and used 0 times" shape as register 1.4, reintroduced by that very fix and
# caught by a scan on 2026-10-05. The five names are in the docstring and in the method; nothing needs a set.)
LEDGER_KEYS = ["date", "run_id", "category", "design_source", "claimed_margin", "basis",
               "projected_cost", "actual_cost", "coverage_result", "reconciled"]
LEDGER_FIELDS = LEDGER_KEYS
_KINDS = (("codex", "codex"), ("gpt", "codex"), ("opencode", "opencode"), ("minimax", "opencode"),
          ("deepseek", "deepseek"), ("dsh", "deepseek"),
          ("claude", "claude"), ("sonnet", "claude"), ("opus", "claude"), ("haiku", "claude"),
          ("agy", "agy"), ("gemini", "agy"), ("qwen", "qwen"))


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def engine_kind(engine: str) -> str:
    """The kind of engine a cell names. A **leading** name wins over an embedded one.

    Two passes because a cell may name more than one engine — the build rows read "opencode ... + Codex ...", and
    the engine named first is the primary one. Matching embedded tokens in one pass returned `codex` for those
    cells (the "+ Codex" matches before the loop reaches `opencode`), which would have told the G6 different-kind
    rule the wrong thing about 60% of the build work.
    """
    e = (engine or "").lower()
    for tok, kind in _KINDS:
        if e.startswith(tok):
            return kind
    for tok, kind in _KINDS:
        if f" {tok}" in e:
            return kind
    return "unknown"


def _header_and_rows(md: list[str], header_first_cell: str) -> tuple[list[str], list[list[str]]]:
    """The header cells and the body rows of the first table whose first header cell matches."""
    hdr: list[str] = []
    for line in md:
        s = line.strip()
        if s.startswith("|") and s.lstrip("|").strip().lower().startswith(header_first_cell.lower()):
            hdr = [c.strip() for c in s.strip("|").split("|")]
            break
    return hdr, _table_rows(md, header_first_cell)


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
                      "pattern": r[2], "loop": "loop" in r[2].lower(),
                      "engine": r[3], "check": r[4], "sabotage": r[5]}
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


# The five things, as fields a node carries rather than names it lists. `context` is the brief the agent is given,
# `contract` is what the piece is for and how it ends, `state` is what it reads and writes, `tools` what it may use,
# `evidence` where its output lands.
CONTRACT_STOP = ("criteria", "baseline", "must_not_change")


def check_five(n: dict) -> str:
    """The first thing wrong with a node's contents, or '' when all five are carried."""
    brief = (n.get("brief_given") or "").strip()
    if not brief:
        return "has no context: brief_given is empty"
    if not (n.get("intent") or "").strip():
        return "has no contract: intent is empty"
    stop = n.get("stop")
    if not isinstance(stop, dict):
        return "has no three-part stop (method 3.6: criteria, baseline, must_not_change)"
    if [k for k in CONTRACT_STOP if not (stop.get(k) or "").strip()]:
        return f"stop is missing {[k for k in CONTRACT_STOP if not (stop.get(k) or '').strip()]}"
    if not (n.get("returns") or "").strip():
        return "has no contract: returns is empty"
    if not (n.get("state_reads") or n.get("state_writes") or ""):
        return "has no state: neither state_reads nor state_writes is set"
    if not (n.get("tools") or []):
        return "has no tools listed"
    if not (n.get("evidence") or []):
        return "has no evidence paths"
    return ""


# A placeholder says "I do not know", not the thing itself. Found by Claude Code, 2026-10-05, on its own design:
# it had marked two fields `UNRESOLVED` rather than inventing values, then noticed the gate would accept them
# anyway. It was right — G10 and the G2 touched_paths clause both tested only for emptiness, so `TBD` passed.
PLACEHOLDER = {"tbd", "todo", "unresolved", "unknown", "n/a", "na", "?", "??", "???", "-", "--", "---",
               "\u2014", "none", "fixme", "xxx"}


def is_placeholder(value) -> bool:
    """True when a field holds a promise to fill it in later rather than a value."""
    text = str(value).strip().lower()
    if not text:
        return True
    head = text.split(":")[0].split("\u2014")[0].strip()
    if head in PLACEHOLDER or text in PLACEHOLDER:
        return True
    return head.startswith(("tbd", "todo", "unresolved", "fixme", "unknown ", "n/a"))


def check_baseline(d: dict, nodes: list[dict]) -> list[str]:
    """A design that builds names the baseline and the node that captures it (register 1.2, and 5.1's owner)."""
    if not d.get("builds"):
        return []
    b = d.get("baseline")
    if not isinstance(b, dict) or not (b.get("command") or "").strip():
        return ["G10: the design builds, but carries no `baseline.command` — the product's test command that "
                "part 2 of every building node's stop is measured against"]
    if is_placeholder(b.get("command")):
        return [f"G12: `baseline.command` is {str(b.get('command'))[:40]!r} — a promise to fill it in later is "
                f"not the product's test command, and part 2 of every building node's stop is measured against it"]
    owner = b.get("captured_by")
    ids = {n.get("id") for n in nodes}
    # `script` is a real answer, not a dodge: from a repo root the dispatcher's own wrapper can capture the
    # baseline before it dispatches anything, and naming that is better than leaving the owner blank (register
    # 5.1). Anything else must be a node that runs before the first builder.
    if owner == "script":
        return []
    if owner not in ids:
        return [f"G10: baseline.captured_by {owner!r} is neither a node in this design nor \"script\""]
    builders = [n.get("id") for n in nodes
                if str(n.get("builds")).lower() == "true" or n.get("category") in ("code generation",)]
    order = [n.get("id") for n in nodes]
    if builders and order.index(owner) > order.index(builders[0]):
        return [f"G10: baseline.captured_by {owner!r} runs after the first building node {builders[0]!r} — the "
                f"baseline must be recorded before anything builds"]
    return []


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
    if builds and touched and all(is_placeholder(t) for t in touched):
        f.append(f"G12: touched_paths holds only {[str(t)[:30] for t in touched]} — a placeholder is not a path, "
                 f"and the claim to build names files it cannot name")
    if builds and not touched:
        # Found by the mutation matrix (2026-10-04): a design may claim `builds: true` and name nothing it
        # touches. The three G2 clauses above and below each look at one field; none compared the claim with its
        # evidence, so the two could contradict each other and pass. 1 of 16 targeted mutations escaped this way.
        f.append("G2: the design claims it builds, but names no product path in touched_paths — the claim and its "
                 "evidence contradict each other, so the gate cannot tell what it would write")
    nodes = d.get("nodes") or []
    ids = {n.get("id") for n in nodes}
    for n in nodes:
        nid = n.get("id", "?")
        if not (n.get("check") or "").strip():
            f.append(f"G3: node {nid} has no check")
        elif re.search(r"TASK_TYPES\.md|^default check for ", str(n.get("check")), re.I):
            # Found by the mutation matrix (2026-10-04). The corpus and the fixtures both emitted
            # "default check for <cat> (TASK_TYPES.md)", so 150 building nodes "had a check" that named no check.
            # A reference to the *document* is that defect — `TASK_TYPES.md` or a `default check for` stub — but a
            # filename like `tests/test_task_types.py` is not, which the first version of this rule got wrong
            # and a real design promptly demonstrated (2026-10-05).
            f.append(f"G3: node {nid}'s check points at the category table instead of stating what is checked")
        # The five things, as CONTENTS (2026-10-05). Until today this checked that five *names* appeared in a
        # list, with nothing behind them — `intake.js` had defined the real fields all along, so the gate now
        # reads them instead of a list of words. One shape, not two.
        f3 = check_five(n)
        if f3:
            f.append(f"G3: node {nid} {f3}")
        lp = n.get("loop")
        if lp is None and known.get(_cat(n), {}).get("loop"):
            f.append(f"G3: node {nid} is a loop-pattern category but carries no loop")
        elif lp is not None:
            # `not isinstance(v, bool)` because `isinstance(True, int)` is True in Python, so `limit: true` passed
            # every gate (found 2026-10-05 by an expert answering checklist question 4 — "name one failing input" —
            # who named `true` among them). A boolean is not a count.
            if isinstance(lp.get("limit"), bool) or not isinstance(lp.get("limit"), int) or lp["limit"] < 1:
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
    node_cats = {_cat(n) for n in nodes if _cat(n)}
    for n in nodes:
        # G9, found by the mutation matrix (2026-10-04): the table's `sabotage` column was parsed and never read,
        # so a design could not carry the proof its check can fail — and the algorithm requires exactly that.
        row = known.get(_cat(n), {})
        if _cat(n) in known and row.get("product") in ("yes", "mixed") and not n.get("sabotage"):
            f.append(f"G9: building node {n.get('id')!r} carries no sabotage proof — the table's sabotage column "
                     f"is the evidence its check can fail, and a check that cannot fail is not a check")
    for n in nodes:
        # G11 (2026-10-05): `TASK_TYPES.md` gives `others` an engine cell of `—`, meaning "no default". The
        # harness passed that placeholder straight through, so a design could name its engine as an em dash and
        # pass — `engine_kind` returned 'unknown' and nothing objected. A node whose engine cannot be dispatched
        # is not a design.
        kind = engine_kind(n.get("engine", ""))
        if kind == "unknown":
            f.append(f"G11: node {n.get('id')!r} names engine {n.get('engine')!r}, which is not an engine — "
                     f"`others` has no default in the table, so the design must work one out (method 3.2)")
    # G13 (2026-10-05). `others` is exempt from the category checks, so an unclassified piece could be a single
    # node that both decides what the work is and does it — the one case where "I do not know what this is" gets
    # to change the product in one step. Method 3.3's own table says what an unknown gets: a *bounded explore
    # loop*, which is a node of its own. Given an equally vague prompt and no help, Claude Code produced
    # `n1-diagnose` first and resolved it rather than labelling the piece `others`; this rule asks for that shape.
    #
    # The honest limit: `builds` is a design-level flag, so the gate cannot tell *which* node writes. This rule
    # therefore catches the shape it can see — a wholly unclassified design that builds in one node — and the
    # per-node witness is register 1.5's missing one, not something this rule can supply.
    if d.get("builds") and len(nodes) == 1 and _cat(nodes[0]) == "others":
        f.append("G13: the design builds and is one `others` node — an unclassified piece cannot both work out "
                 "what the work is and do it in one step; give it a bounded explore node first (method 3.3) and "
                 "run the work that depends on it after")
    if cats and node_cats:
        for c in sorted(set(cats) - node_cats):
            f.append(f"G8: category {c!r} is claimed but no node carries it — relabel from the algorithm (3.2)")
        # the in-run review node G6 demands is not a deliverable of the prompt, so it may be unlisted
        for c in sorted(node_cats - set(cats) - {"code review"}):
            f.append(f"G8: a node carries category {c!r} that the design does not list")
    f.extend(check_baseline(d, nodes))
    return f


def parse_ledger(path: Path) -> list[dict]:
    """Read the markdown ledger table into row dicts.

    Columns are matched **by position**, so the header is checked against `LEDGER_KEYS` first. It was not, until
    2026-10-05: swapping two columns parsed cleanly and silently mis-assigned every field after them (the review
    round demonstrated `claimed_margin` becoming the string `"default"`), because the only thing the reader anchored
    on was the first header cell. A header nothing reads is a header that cannot fail.
    """
    lines = Path(path).read_text(errors="replace").splitlines()
    hdr, rows = _header_and_rows(lines, "Date")
    if hdr:
        got = [c.strip().lower().replace(" ", "_") for c in hdr][:len(LEDGER_KEYS)]
        if got and got != LEDGER_KEYS:
            raise ValueError(f"ledger header does not match LEDGER_KEYS\n  header: {got}\n  keys:   {LEDGER_KEYS}")
    out: list[dict] = []
    for r in rows:
        if len(r) < len(LEDGER_KEYS):
            continue
        row = dict(zip(LEDGER_KEYS, r))
        try:
            row["claimed_margin"] = float(row["claimed_margin"])
        except ValueError:
            pass  # "—" for a default row stays a string
        row["reconciled"] = row["reconciled"].strip().lower() in ("yes", "true")
        out.append(row)
    return out


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


def _contents(nid: str, engine: str = "codex gpt-6.1-sol") -> dict:
    """The five things as contents, not as names — the shape `.claude/workflows/intake.js` already emits."""
    return {
        "brief_given": "the brief this piece is given, and what it is withheld",
        "intent": "one bounded piece: why it exists",
        "stop": {"criteria": "the check's criteria pass",
                 "baseline": "everything the baseline recorded as passing still passes",
                 "must_not_change": "the paths outside this design's may-change set"},
        "returns": "the node's result file",
        "state_reads": "the state file",
        "tools": [engine.split()[0]],
        "evidence": [f"runs/<runId>/nodes/{nid}.result.md"],
    }


def _good_design() -> dict:
    return {
        "categories": ["research and reports", "code generation"],
        "builds": True, "touched_paths": ["x.py"], "pipeline": "research → codegen",
        "baseline": {"command": "env -u NO_COLOR python3 -m pytest -q", "captured_by": "script"},
        "nodes": [
            {"id": "n1", "category": "research and reports", "engine": "codex gpt-6.1-sol",
             "check": "questions answered (fixed checklist)", **_contents("n1"), "needs": []},
            {"id": "n2", "category": "code generation", "engine": "codex gpt-6.1-sol",
             "check": "pytest -q green", "sabotage": "break the code → the check goes red",
             **_contents("n2"), "needs": ["n1"],
             "loop": {"limit": 2, "exit": "fresh node on stronger tier", "feedback": "the check's real output"}},
            {"id": "n3", "category": "code review", "engine": "claude sonnet 5.5",
             "check": "fixed checklist; findings with file:line", **_contents("n3", "claude sonnet 5.5"),
             "needs": ["n2"]}],
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
        hit = (not findings) if want_prefix is None else any(x.startswith(want_prefix) for x in findings)
        print(f"{'ok  ' if hit else 'FAIL'} self-test: {label}")
        ok = ok and hit

    expect("a good design passes clean", _good_design(), None)
    d = copy.deepcopy(_good_design()); d["categories"] = ["research and reports"]
    expect("research-only categories on a building design -> G2", d, "G2")
    d = copy.deepcopy(_good_design()); d["categories"] = ["others"]
    for n in d["nodes"]:
        if n["category"] != "code review":
            n["category"] = "others"
    expect("others may build (exempt) -> clean", d, None)
    d = copy.deepcopy(_good_design()); d["categories"] = ["research and reports"]
    d["nodes"][0]["category"] = "research and reports"; d["nodes"][1]["category"] = "code generation"
    expect("a node category the design does not list -> G8", d, "G8")
    d = copy.deepcopy(_good_design()); d["categories"] = ["research and reports", "code generation", "classification"]
    expect("a claimed category no node carries -> G8", d, "G8")
    d = copy.deepcopy(_good_design()); d["nodes"][1]["brief_given"] = ""
    expect("a node with no context -> G3", d, "G3")
    d = copy.deepcopy(_good_design()); d["nodes"][1]["stop"] = {"criteria": "x"}
    expect("a stop missing two of its three parts -> G3", d, "G3")
    d = copy.deepcopy(_good_design()); d["baseline"]["captured_by"] = "nobody"
    expect("a baseline with no real owner -> G10", d, "G10")
    d = copy.deepcopy(_good_design()); del d["baseline"]
    expect("a design that builds with no baseline -> G10", d, "G10")
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
