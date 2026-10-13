#!/usr/bin/env python3
"""verdict.py — compute the verdict from recorded evidence (step E10).

Run:  python3 tools/evaluator/verdict.py --run DIR

DATA.md's E10 rules determine cases, then groups, then requirement counts.
Missing optional inputs supply no evidence. The CLI writes verdict.json and
verdict.md and prints the MEETS line for the workflow (EV-P1.3, EV-P2).
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path


class InputError(Exception):
    """An input cannot be read as a JSON object; the message names its path."""


def _read_json(path: Path, required: bool = False) -> dict:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        if not required:
            return {}
        raise InputError(f"{path}: {error.strerror}") from None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InputError(f"{path}: {error}") from None
    if not isinstance(document, dict):
        raise InputError(f"{path}: expected a JSON object")
    return document


def _probe_key(probe: str) -> str:
    """Normalize E8's file citation to E6's module::test key."""
    module, separator, name = probe.partition("::")
    return f"{Path(module).stem}{separator}{name}"


def _repro_command(probe: str, matrix: dict) -> str:
    module, _, name = probe.partition("::")
    product = matrix.get("product_dir", "workspace/product")
    probes = matrix.get("probes_dir", "probes")
    test_file = str(Path(probes) / f"{module}.py")
    return (f"EVAL_PRODUCT={shlex.quote(product)} python3 -m pytest -c /dev/null "
            f"{shlex.quote(test_file)} -k {shlex.quote(name.split('[')[0])}")


def _decide_case(case_id: str, label: dict, matrix: dict,
                 confirmations: list[dict], judged: dict) -> dict:
    kind = label.get("kind", "human")
    if not str(label.get("reason") or "").strip() or kind not in {
            "human", "judged", "executable", "static"}:
        kind = "human"
    row = {"case": case_id, "kind": kind, "verdict": "UNKNOWN", "reason": "", "repro": ""}
    if kind == "human":
        row["reason"] = "needs EJ"
    elif kind == "judged":
        entry = next((entry for entry in judged.get("cases", []) if entry["case"] == case_id), None)
        if judged.get("plant_found") is not True:
            row["reason"] = "judging void: plant missed"
        elif entry is None or entry.get("holds") not in (True, False):
            row["reason"] = "not judged"
        elif not str(entry.get("evidence") or "").strip():
            row["reason"] = "not judged: no quoted evidence"
        elif entry["holds"] is True:
            row["verdict"] = "PASS"
        else:
            row.update(verdict="FAIL", reason="judged case does not hold", repro=entry["evidence"])
    else:
        probes = [probe for probe, citations in matrix.get("citations", {}).items() if case_id in citations]
        product = matrix.get("product", {})
        red_probes = [probe for probe in probes if product.get(probe) == "fail"]
        if not probes:
            row["reason"] = "no probe"
        elif red_probes:
            confirmed = next((probe for probe in red_probes
                              if any(entry.get("case") == case_id
                                     and _probe_key(entry.get("probe", "")) == probe
                                     and entry.get("faithful") is True
                                     for entry in confirmations)), None)
            if confirmed is None:
                row["reason"] = "probe not confirmed faithful"
            else:
                row.update(verdict="FAIL", reason="confirmed faithful probe fails on product",
                           repro=_repro_command(confirmed, matrix))
        elif all(product.get(probe) == "pass" for probe in probes):
            mutant = matrix.get("mutants", {}).get(case_id)
            if not mutant or mutant.get("status") != "applied":
                row["reason"] = "no mutant"
            elif any(mutant.get("results", {}).get(probe) == "fail" for probe in probes):
                row["verdict"] = "PASS"
            else:
                row["reason"] = "unproven: no probe fails on its mutant"
        else:
            row["reason"] = "probe skipped or product result missing"
    # E10 rule 4 overrides all kinds, including confirmed failures and judging.
    if matrix.get("restored") is False:
        row.update(verdict="UNKNOWN", reason="product not restored", repro="")
    return row


def _group_verdict(group: dict, cases: list[dict]) -> tuple[str, str]:
    failures = [row for row in cases if row["verdict"] == "FAIL"]
    if failures:
        return "FAIL", "; ".join(f"{row['case']}: {row['reason']}" for row in failures)
    if cases and all(row["verdict"] == "PASS" for row in cases):
        return "PASS", ""
    if group.get("status") == "untestable":
        return "UNKNOWN", "untestable: no Fails if"
    return "UNKNOWN", ("; ".join(f"{row['case']}: {row['reason']}" for row in cases
                                 if row["verdict"] == "UNKNOWN") or "no cases")


def decide(run: Path) -> dict:
    """Return verdict.json's content without changing the recorded inputs."""
    run = Path(run)
    requirements = _read_json(run / "requirements.json", required=True)
    classify = _read_json(run / "classify.json")
    matrix = _read_json(run / "matrix.json")
    confirm = _read_json(run / "confirm.json")
    judged = _read_json(run / "judged.json")
    labels = {entry["case"]: entry for entry in classify.get("cases", [])}
    cases, requirement_rows, out_of_scope = [], [], []
    groups = requirements.get("groups", []) + [
        {"group": line["id"], "ids": [line["id"]], "cases": line.get("cases", [])}
        for line in requirements.get("vision", [])]
    for group in groups:
        group_cases = [_decide_case(case["case"], labels.get(case["case"], {}), matrix,
                                    confirm.get("cases", []), judged)
                       for case in group.get("cases", [])]
        cases.extend(group_cases)
        verdict, reason = _group_verdict(group, group_cases)
        for identifier in group.get("ids", []):
            if identifier in group.get("open_ids", []) or group.get("status") == "open":
                out_of_scope.append(identifier)
            else:
                requirement_rows.append({"id": identifier, "group": group["group"],
                                         "verdict": verdict, "reason": reason})
    counts = {verdict: sum(row["verdict"] == verdict for row in requirement_rows)
              for verdict in ("PASS", "FAIL", "UNKNOWN")}
    counts["out_of_scope"] = len(out_of_scope)
    return {"meets": all(row["verdict"] == "PASS" for row in requirement_rows),
            "counts": counts, "cases": cases, "requirements": requirement_rows,
            "out_of_scope": out_of_scope, "manifest": requirements.get("manifest", [])}


def _markdown_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def _render_report(verdict: dict) -> str:
    counts = verdict["counts"]
    lines = [f"MEETS: {'yes' if verdict['meets'] else 'no'}", "",
             ", ".join(f"{name}: {count}" for name, count in counts.items()), ""]
    for status in ("FAIL", "UNKNOWN", "PASS"):
        lines.extend([f"## {status}", "",
                      "| Requirement | Verdict | Cases | Evidence | Reason | Repro |",
                      "|---|---|---|---|---|---|"])
        for requirement in verdict["requirements"]:
            if requirement["verdict"] != status:
                continue
            cases = [case for case in verdict["cases"]
                     if case["case"].startswith(requirement["group"] + "-F")]
            evidence = sorted({"judged.json" if case["kind"] == "judged" else
                               "classify.json" if case["kind"] == "human" else "matrix.json"
                               for case in cases})
            if any(case["kind"] in {"executable", "static"} and case["verdict"] == "FAIL" for case in cases):
                evidence.append("confirm.json")
            cells = [requirement["id"], status, ", ".join(case["case"] for case in cases),
                     ", ".join(evidence) or "requirements.json", requirement["reason"],
                     "<br>".join(case["repro"] for case in cases if case["verdict"] == "FAIL")]
            lines.append("| " + " | ".join(_markdown_cell(cell) for cell in cells) + " |")
        lines.append("")
    lines.extend(["## Out of scope", "", *[f"- {identifier}" for identifier in verdict["out_of_scope"]],
                  "", "## Manifest", "", *[f"- {identifier}" for identifier in verdict["manifest"]], ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Write the report files and expose the workflow's MEETS line on stdout."""
    parser = argparse.ArgumentParser(description="Compute a verdict from recorded results.")
    parser.add_argument("--run", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        verdict = decide(args.run)
        (args.run / "verdict.json").write_text(
            json.dumps(verdict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (args.run / "verdict.md").write_text(_render_report(verdict), encoding="utf-8")
    except InputError as error:
        print(str(error), file=sys.stderr)
        return 2
    except OSError as error:
        print(f"{error.filename or args.run}: {error.strerror or error}", file=sys.stderr)
        return 2
    print(f"MEETS: {'yes' if verdict['meets'] else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
