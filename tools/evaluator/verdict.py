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
        if required:
            raise InputError(f"{path}: expected a JSON object")
        return {}
    return document


def _object(value) -> dict:
    return value if isinstance(value, dict) else {}


def _case_entries(document: dict, filename: str, problems: list[str],
                  needs_probe: bool = False) -> list[dict]:
    rows = document.get("cases", [])
    if not isinstance(rows, list):
        return []
    entries = []
    for index, row in enumerate(rows):
        problem = ""
        if not isinstance(row, dict):
            problem = "expected an object"
        elif not isinstance(row.get("case"), str):
            problem = "case is not a string"
        elif needs_probe and not isinstance(row.get("probe"), str):
            problem = "probe is not a string"
        if problem:
            problems.append(f"{filename}: entry {index}: {problem}")
        else:
            entries.append(row)
    return entries


def _probe_key(probe: str) -> str:
    """Normalize E8's file citation to E6's module::test key."""
    module, separator, name = probe.partition("::")
    return f"{Path(module).stem}{separator}{name}"


def _repro_command(probe: str, matrix: dict) -> str:
    module, _, name = probe.partition("::")
    product = matrix.get("product_dir", "workspace/product")
    probes = matrix.get("probes_dir", "probes")
    if not isinstance(product, str) or not isinstance(probes, str):
        raise InputError("matrix.json: product_dir and probes_dir must be strings")
    test_file = str(Path(probes) / f"{module}.py")
    # Run from the run folder. "$PWD" makes the product path absolute: a probe that changes directory would not find
    # a relative one, and the repro would fail for a reason that is not the product (calibration K1b, 2026-10-13).
    return (f'EVAL_PRODUCT="$PWD"/{shlex.quote(product)} python3 -m pytest -c /dev/null '
            f"{shlex.quote(test_file)} -k {shlex.quote(name.split('[')[0])}")


def _decide_case(case_id: str, label: dict, matrix: dict,
                 confirmations: list[dict], judged: dict, matrix_present: bool = False) -> dict:
    kind = label.get("kind", "human")
    reason = label.get("reason")
    if not isinstance(kind, str) or not isinstance(reason, str) or not reason.strip() or kind not in {
            "human", "judged", "executable", "static"}:
        kind = "human"
    row = {"case": case_id, "kind": kind, "verdict": "UNKNOWN", "reason": "", "repro": ""}
    if kind == "human":
        row["reason"] = "classified twice" if label.get("reason") == "classified twice" else "needs EJ"
    elif kind == "judged":
        entry = next((entry for entry in judged.get("cases", []) if entry["case"] == case_id), None)
        if judged.get("plant_found") is not True:
            row["reason"] = "judging void: plant missed"
        elif entry is None or (entry.get("holds") is not True and entry.get("holds") is not False):
            row["reason"] = "not judged"
        elif not isinstance(entry.get("evidence"), str) or not entry["evidence"].strip():
            row["reason"] = "not judged: no quoted evidence"
        elif entry["holds"] is True:
            row["verdict"] = "PASS"
        else:
            row.update(verdict="FAIL", reason="judged case does not hold", repro=entry["evidence"])
    else:
        probes = [probe for probe, citations in _object(matrix.get("citations")).items()
                  if isinstance(citations, list) and case_id in citations]
        product = _object(matrix.get("product"))
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
            mutant = _object(_object(matrix.get("mutants")).get(case_id))
            if not mutant or mutant.get("status") != "applied":
                row["reason"] = "no mutant"
            else:
                results = _object(mutant.get("results"))
                mutant_run = _object(_object(matrix.get("runs")).get(case_id))
                errors = mutant_run.get("errors", [])
                red = [probe for probe in probes if results.get(probe) == "fail"]
                # R1-F5(c), Dave's guarded rule: with 2 or more results, not every one may be red; a single-probe
                # run is not judged by (c) (DATA.md, corrected 2026-10-13).
                healthy = ((len(results) < 2 or any(outcome != "fail" for outcome in results.values()))
                           and all(isinstance(outcome, str) and outcome in {"pass", "fail", "skip"}
                                   for outcome in results.values())
                           and ("runs" not in matrix or mutant_run.get("status") == "ok")
                           and isinstance(errors, list) and all(isinstance(probe, str) for probe in errors))
                if not healthy or (red and not any(probe not in errors for probe in red)):
                    row["reason"] = "unproven: the mutant run was not healthy"
                elif red:
                    row["verdict"] = "PASS"
                else:
                    row["reason"] = "unproven: no probe fails on its mutant"
        else:
            row["reason"] = "probe skipped or product result missing"
    if (kind in {"executable", "static"} and matrix_present
            and (matrix.get("restored") is not True or matrix.get("product_changed") is True)):
        row.update(verdict="UNKNOWN", reason="product copy not restored or changed", repro="")
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
    problems = []
    for document in (classify, confirm, judged):
        recorded = document.get("input_problems", [])
        if isinstance(recorded, list):
            problems.extend(problem for problem in recorded if isinstance(problem, str))
    labels = {}
    for entry in _case_entries(classify, "classify.json", problems):
        if entry["case"] in labels:
            labels[entry["case"]] = {"kind": "human", "reason": "classified twice"}
        else:
            labels[entry["case"]] = entry
    confirmations = _case_entries(confirm, "confirm.json", problems, needs_probe=True)
    judged["cases"] = _case_entries(judged, "judged.json", problems)
    cases, requirement_rows, out_of_scope = [], [], []
    for key in ("groups", "vision", "manifest", "unparsed_ids"):
        if not isinstance(requirements.get(key, []), list):
            raise InputError(f"requirements.json: {key} must be a list")
    for group in requirements.get("groups", []):
        if (not isinstance(group, dict) or not isinstance(group.get("group"), str)
                or not isinstance(group.get("ids", []), list)
                or not all(isinstance(identifier, str) for identifier in group.get("ids", []))
                or not isinstance(group.get("open_ids", []), list)):
            raise InputError("requirements.json: invalid group")
    for line in requirements.get("vision", []):
        if not isinstance(line, dict) or not isinstance(line.get("id"), str):
            raise InputError("requirements.json: invalid vision entry")
    groups = requirements.get("groups", []) + [
        {"group": line["id"], "ids": [line["id"]], "cases": line.get("cases", [])}
        for line in requirements.get("vision", [])]
    for group in groups:
        if (not isinstance(group.get("cases", []), list)
                or any(not isinstance(case, dict) or not isinstance(case.get("case"), str)
                       for case in group.get("cases", []))):
            raise InputError("requirements.json: invalid cases")
        group_cases = [_decide_case(case["case"], labels.get(case["case"], {}), matrix,
                                    confirmations, judged, (run / "matrix.json").exists())
                       for case in group.get("cases", [])]
        cases.extend(group_cases)
        verdict, reason = _group_verdict(group, group_cases)
        for identifier in group.get("ids", []):
            if identifier in group.get("open_ids", []) or group.get("status") == "open":
                out_of_scope.append({"id": identifier, "reason": "marked open in the spec"})
            else:
                requirement_rows.append({"id": identifier, "group": group["group"],
                                         "verdict": verdict, "reason": reason})
    counts = {verdict: sum(row["verdict"] == verdict for row in requirement_rows)
              for verdict in ("PASS", "FAIL", "UNKNOWN")}
    counts["out_of_scope"] = len(out_of_scope)
    known_cases = {row["case"] for row in cases}
    citations = _object(matrix.get("citations"))
    probe_keys = dict.fromkeys([*citations, *_object(matrix.get("product"))])
    for mutant in _object(matrix.get("mutants")).values():
        probe_keys.update(dict.fromkeys(_object(_object(mutant).get("results"))))
    orphans = [probe for probe in probe_keys
               if not isinstance(citations.get(probe), list) or not citations[probe]
               or any(not isinstance(case, str) or case not in known_cases for case in citations[probe])]
    verdict = {"meets": bool(requirement_rows) and all(row["verdict"] == "PASS" for row in requirement_rows),
            "counts": counts, "cases": cases, "requirements": requirement_rows,
            "out_of_scope": out_of_scope, "manifest": requirements.get("manifest", []),
            "input_problems": problems, "orphan_probes": orphans}
    if not requirement_rows:
        verdict["meets_reason"] = "no in-scope requirements"
    if requirements.get("unparsed_ids"):
        verdict.update(meets=False, meets_reason="unparsed ids: " + ", ".join(
            str(identifier) for identifier in requirements["unparsed_ids"]))
    return verdict


def _markdown_cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", "<br>")


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
    lines.extend(["## Out of scope", "", *[f"- {entry['id']}: {entry['reason']}"
                                          for entry in verdict["out_of_scope"]],
                  "", "## Orphan probes", "", *[f"- {probe}" for probe in verdict["orphan_probes"]],
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
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        print(f"{args.run}: {error}", file=sys.stderr)
        return 2
    print(f"MEETS: {'yes' if verdict['meets'] else 'no'} run={args.run.resolve().name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
