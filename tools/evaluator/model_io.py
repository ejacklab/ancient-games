#!/usr/bin/env python3
"""model_io.py — prepare and check the files around the confirm and judge model steps.

Run:  python3 tools/evaluator/model_io.py SUBCOMMAND --run DIR

DATA.md's last section supplies the file contract. Quotes are plain substrings
after collapsing whitespace; only requirements.json is a required input.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

GROUP_HEADING = re.compile(r"^\*\*(?P<group>[A-Z][A-Za-z]*(?:-[A-Z][A-Za-z]*)?\d+(?:\.\d+)?) — .*?\*\*", re.MULTILINE)
CODE_EVIDENCE = re.compile(r'^\s*(?P<file>.+?):\d+\s+"(?P<quote>.*?)"(?:\s+—\s+.*)?\s*$', re.DOTALL)
OUTPUT_LINES = 40


class InputError(Exception):
    """An unreadable input, with its path in the message printed on stderr."""


class ModelStepMissing(Exception):
    """A model step had work and wrote nothing: exit 1, so the workflow blocks (EV-C6.2)."""


def _read_json(path: Path, required: bool = False) -> dict | list:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        if not required:
            return {}
        raise InputError(f"{path}: {error.strerror}") from None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InputError(f"{path}: {error}") from None
    if required and not isinstance(document, dict):
        raise InputError(f"{path}: expected a JSON object")
    if not isinstance(document, (dict, list)):
        return {}
    return document


def _read_text(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8")
    except FileNotFoundError:
        return ""
    except (OSError, UnicodeDecodeError) as error:
        raise InputError(f"{path}: {error}") from None


def _write_json(path: Path, document: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _object(value) -> dict:
    return value if isinstance(value, dict) else {}


def _entries(document, filename: str = "input", problems: list[str] | None = None,
             needs_probe: bool = False, bare_list: bool = False) -> list[dict]:
    rows = (document if isinstance(document, list) else []) if bare_list else _object(document).get("cases", [])
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
            if problems is not None:
                problems.append(f"{filename}: entry {index}: {problem}")
        else:
            entries.append(row)
    return entries


def _case_contexts(run: Path, requirements: dict) -> dict[str, dict]:
    """Case order comes from E1; group blocks retain the spec's original bytes."""
    text = _read_text(run / "workspace/spec/REQUIREMENTS.md")
    headings = list(GROUP_HEADING.finditer(text))
    blocks = {}
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        blocks[heading["group"]] = text[heading.start():end]
    contexts = {}
    for key in ("groups", "vision"):
        if not isinstance(requirements.get(key, []), list):
            raise InputError(f"requirements.json: {key} must be a list")
    for group in requirements.get("groups", []):
        if not isinstance(group, dict) or not isinstance(group.get("group"), str):
            raise InputError("requirements.json: invalid group")
        for case in _entries(group):
            contexts[case["case"]] = {
                "case": case["case"], "case_text": case.get("text", ""),
                "group_text": blocks.get(group["group"], ""),
            }
    for vision in requirements.get("vision", []):
        if not isinstance(vision, dict):
            raise InputError("requirements.json: invalid vision entry")
        for case in _entries(vision):
            contexts[case["case"]] = {
                "case": case["case"], "case_text": case.get("text", ""),
                "group_text": vision.get("text", ""),
            }
    return contexts


def _probe_sources(probes: Path) -> dict[str, str]:
    sources = {}
    for path in sorted(probes.glob("test_*.py")):
        text = _read_text(path)
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as error:
            raise InputError(f"{path}: {error.msg} at line {error.lineno}") from None
        lines = text.splitlines(keepends=True)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = min([node.lineno, *[decorator.lineno for decorator in node.decorator_list]])
                sources[f"{path.stem}::{node.name}"] = "".join(lines[start - 1:node.end_lineno])
    return sources


def _probe_key(probe: str) -> str:
    module, separator, name = probe.partition("::")
    return f"{Path(module).stem}{separator}{name}"


def confirm_input(run: Path, requirements: dict) -> dict:
    matrix = _object(_read_json(run / "matrix.json"))
    contexts = _case_contexts(run, requirements)
    sources = _probe_sources(run / "probes")
    rows = []
    for probe, outcome in _object(matrix.get("product")).items():
        if outcome != "fail":
            continue
        output = _object(matrix.get("output")).get(probe, "")
        citations = _object(matrix.get("citations")).get(probe, [])
        if not isinstance(citations, list):
            citations = []
        case = citations[0] if citations else ""
        if not isinstance(case, str):
            case = ""
        context = contexts.get(case, {"case": case, "case_text": "", "group_text": ""})
        rows.append({**context, "probe": probe,
                     "probe_source": sources.get(_probe_key(probe).split('[')[0], ""),
                     "output": "\n".join(str(output).splitlines()[-OUTPUT_LINES:])})
    document = {"cases": rows}
    (run / "confirm.json").unlink(missing_ok=True)
    _write_json(run / "confirm-input.json", document)
    print(f"{len(rows)} to confirm")
    return document


def _quote_found(quote: str, source: str) -> bool:
    if not isinstance(quote, str) or not isinstance(source, str):
        return False
    collapsed = " ".join(quote.split())
    return bool(collapsed) and collapsed in " ".join(source.split())


def _require_model_file(path: Path, step: str) -> None:
    """A model step that had work but left no file failed; that blocks the run (EV-C6.2), it is never 'empty'."""
    if not path.is_file():
        raise ModelStepMissing(f"{path}: the {step} step had work but wrote no file")


def confirm_check(run: Path, requirements: dict) -> dict:
    problems = []
    inputs = _entries(_read_json(run / "confirm-input.json"), "confirm-input.json", problems, needs_probe=True)
    if inputs:
        _require_model_file(run / "confirm.json", "confirm")
    previous = _object(_read_json(run / "confirm.json"))
    saved_problems = previous.get("input_problems", [])
    if isinstance(saved_problems, list):
        problems.extend(problem for problem in saved_problems if isinstance(problem, str))
    answers = _entries(previous, "confirm.json", problems, needs_probe=True)
    manifest = _read_json(run / "workspace/manifest.json")
    # Files the blind workspace removed on purpose (EV-R2.1). A probe that fails because one is missing failed on
    # the evaluator's own exclusion, not on the product (calibration K1b, 2026-10-13: C2 checks the product's tests).
    # Only files are matched: every absolute path contains a removed folder name such as "runs".
    excluded = _object(manifest).get("excluded", [])
    removed = [path for path in (excluded if isinstance(excluded, list) else [])
               if isinstance(path, str) and "." in path.rsplit("/", 1)[-1]]
    voided = 0
    for answer in answers:
        context = next((row for row in inputs
                        if row.get("case") == answer.get("case")
                        and _probe_key(row.get("probe", ""))
                        == _probe_key(answer.get("probe", ""))), {})
        if not str(context.get("output") or "").strip():
            # No recorded failure output: the probe may have died in setup, so nothing shows the product failed
            # (calibration K1, 2026-10-13: 28 setup failures were confirmed from the probe source alone).
            answer.update(faithful=False, note="no failure output")
            voided += 1
        elif any(path in str(context.get("output")) for path in removed):
            answer.update(faithful=False, note="needs a file the blind workspace removed")
            voided += 1
        elif not (_quote_found(answer.get("requirement_quote", ""), context.get("group_text", ""))
                  and _quote_found(answer.get("probe_quote", ""), context.get("probe_source", ""))):
            answer.update(faithful=False, note="quote not found")
            voided += 1
    document = {"cases": answers}
    if problems:
        document["input_problems"] = problems
    _write_json(run / "confirm.json", document)
    script_notes = ("no failure output", "needs a file the blind workspace removed", "quote not found")
    unfaithful = [answer for answer in answers
                 if answer.get("faithful") is False and answer.get("note") not in script_notes]
    if unfaithful and not (run / "repair.json").exists():
        _write_json(run / "repair.json", {"round": 1, "cases": unfaithful})
    print(f"{len(answers)} checked, {voided} voided, {len(unfaithful)} unfaithful")
    return document


def _product_file(product: Path, relative: str) -> Path | None:
    if not isinstance(relative, str):
        return None
    target = product / relative
    try:
        if product.resolve() not in target.resolve().parents or not target.is_file():
            return None
    except (ValueError, OSError, RuntimeError):
        return None
    return target


def _judge_folder(run: Path) -> Path:
    name = run.name
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name) or ".." in name:
        raise InputError(f"{run}: invalid run folder name")
    return Path("/tmp") / f"evaluator-judge-{name}"


def _remove_judge_folder(folder: Path) -> None:
    """The judge's /tmp folder goes once the merge has read what it needs (item 8).

    A folder that is not there is nothing to remove, and a symlink at that path is never followed: only the
    real directory the evaluator made is deleted, and only that path.
    """
    if not folder.is_symlink() and folder.is_dir():
        shutil.rmtree(folder)


def _reset_directory(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def judge_input(run: Path, requirements: dict, attempt: int = 1) -> dict:
    contexts = _case_contexts(run, requirements)
    problems = []
    labels = {}
    for row in _entries(_read_json(run / "classify.json"), "classify.json", problems):
        case = row["case"]
        labels[case] = {"kind": "human"} if case in labels else row
    rows = [context for case, context in contexts.items()
            if labels.get(case, {}).get("kind") == "judged"
            and isinstance(labels[case].get("reason"), str) and labels[case]["reason"].strip()]
    plants = _entries(_read_json(run / "plants.json"), "plants.json", problems, bare_list=True)
    product = run / "workspace/product"
    valid_plants = []
    for row in rows:
        for plant in plants:
            if plant.get("case") != row["case"]:
                continue
            target = _product_file(product, plant.get("file", ""))
            old, new = plant.get("old"), plant.get("new")
            if target is None or not isinstance(old, str) or not old or not isinstance(new, str):
                continue
            try:
                text = target.read_bytes().decode("utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if text.count(old) != 1:
                continue
            valid_plants.append(plant)
            break
    previous = _object(_read_json(run / ".coordinator/plant.json")).get("plant_case")
    if attempt == 2:
        previous_index = next((index for index, plant in enumerate(valid_plants)
                               if plant["case"] == previous), None)
        available = valid_plants[previous_index + 1:] if previous_index is not None else []
        if not available:
            print("no other plant")
            return _object(_read_json(run / "judge-input.json"))
    else:
        available = valid_plants
    plant = available[0] if available else None
    folder = _judge_folder(run)
    _reset_directory(folder)
    copy = folder / "product"
    if product.is_dir():
        shutil.copytree(product, copy, symlinks=True)
    else:
        copy.mkdir()
    plant_case = plant["case"] if plant else None
    if plant:
        target = _product_file(copy, plant["file"])
        if target is None:
            raise InputError("plants.json: plant target is outside the judge copy")
        text = target.read_bytes().decode("utf-8")
        target.write_bytes(text.replace(plant["old"], plant["new"], 1).encode("utf-8"))
    # Fresh calls must not inherit answers from the previous attempt.
    for filename in ("judge-1.json", "judge-2.json"):
        (run / filename).unlink(missing_ok=True)
    document = {"cases": rows}
    _write_json(run / "judge-input.json", document)
    _write_json(folder / "judge-input.json", document)
    coordinator = {"plant_case": plant_case, "attempt": attempt}
    if problems:
        coordinator["input_problems"] = problems
    _write_json(run / ".coordinator/plant.json", coordinator)
    print(f"{len(rows)} to judge")
    if plant_case:
        print(f"plant {plant_case}")
    return document


def _code_quote_found(entry: dict, product: Path) -> bool:
    evidence = entry.get("evidence", "")
    if not isinstance(evidence, str):
        return False
    match = CODE_EVIDENCE.fullmatch(evidence)
    if match is None or (entry.get("holds") is not True and entry.get("holds") is not False):
        return False
    relative = match["file"]
    for prefix in ("judge-copy/", "workspace/product/", "product/"):
        if relative.startswith(prefix):
            relative = relative[len(prefix):]
    target = _product_file(product, relative)
    return target is not None and _quote_found(match["quote"], _read_text(target))


def judged_merge(run: Path, requirements: dict) -> dict:
    inputs = _read_json(run / "judge-input.json")
    problems = []
    rows = _entries(inputs, "judge-input.json", problems)
    coordinator = _object(_read_json(run / ".coordinator/plant.json"))
    saved_problems = coordinator.get("input_problems", [])
    if isinstance(saved_problems, list):
        problems.extend(problem for problem in saved_problems if isinstance(problem, str))
    if not rows:
        document = {"plant_found": True, "cases": []}
    else:
        plant_case = coordinator.get("plant_case")
        if not isinstance(plant_case, str):
            plant_case = None
        folder = _judge_folder(run)
        try:
            _require_model_file(folder / "judge-1.json", "first judge")
            if plant_case is not None:
                _require_model_file(run / "judge-2.json", "second judge")
            first_document = _read_json(folder / "judge-1.json")
            shutil.copyfile(folder / "judge-1.json", run / "judge-1.json")
            first = {entry["case"]: entry for entry in _entries(first_document, "judge-1.json", problems)
                     if _code_quote_found(entry, folder / "product")}
        finally:
            # Call 1's answer and its code quotes have both been read; the folder is the evaluator's own and goes.
            _remove_judge_folder(folder)
        second = {entry["case"]: entry for entry in _entries(_read_json(run / "judge-2.json"),
                                                            "judge-2.json", problems)
                  if _code_quote_found(entry, run / "workspace/product")}
        cases = []
        for row in rows:
            case = row["case"]
            entry = (second if case == plant_case else first).get(case)
            if entry is not None:
                cases.append(entry)
        document = {"plant_case": plant_case,
                    "plant_found": plant_case is not None and first.get(plant_case, {}).get("holds") is False,
                    "cases": cases}
    if problems:
        document["input_problems"] = problems
    _write_json(run / "judged.json", document)
    print(f"plant_found: {str(document['plant_found']).lower()}")
    return document


def check_output(run: Path, step: str) -> None:
    """Validate the model's output file, independently of its done answer."""
    try:
        if step == "probes":
            valid = any(path.is_file() for path in (run / "probes").glob("test_*.py"))
        else:
            path = run / f"{step}.json"
            document = _read_json(path)
            valid = path.is_file() and (
                isinstance(document, dict) and isinstance(document.get("cases"), list)
                if step == "classify" else isinstance(document, list))
    except InputError as error:
        raise ModelStepMissing(str(error)) from None
    if not valid:
        raise ModelStepMissing(f"{run}: {step} output missing or not valid")
    print(f"{step}: valid")


def stamp(run: Path, event: str, agents: int | None) -> dict:
    cost = {} if event == "start" else _object(_read_json(run / "cost.json"))
    cost[event] = datetime.now(timezone.utc).isoformat()
    cost.update(tokens="not reported", models="requested, not verified")
    if agents is not None:
        cost["agents"] = agents
    _write_json(run / "cost.json", cost)
    if event == "start":
        (run / "probe-scratch").mkdir(exist_ok=True)
    print(f"{event} stamped")
    return cost


def mutant_view(run: Path, collect: bool) -> None:
    view = run / "mutant-view"
    if collect:
        # Validate presence before copying either deliverable back into the run.
        for filename in ("mutants.json", "plants.json"):
            _require_model_file(view / filename, "mutants")
        for filename in ("mutants.json", "plants.json"):
            shutil.copyfile(view / filename, run / filename)
        print("mutants and plants collected")
    else:
        _reset_directory(view)
        for filename in ("requirements.json", "classify.json"):
            shutil.copyfile(run / filename, view / filename)
        shutil.copytree(run / "workspace", view / "workspace", symlinks=True)
        print("mutant view built")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("subcommand", choices=["confirm-input", "confirm-check", "judge-input", "judged-merge",
                                               "check-output", "stamp", "mutant-view"])
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--step", choices=["classify", "probes", "mutants"])
    parser.add_argument("--event", choices=["start", "end"])
    parser.add_argument("--agents", type=int)
    parser.add_argument("--attempt", type=int, choices=[1, 2], default=1)
    parser.add_argument("--collect", action="store_true")
    args = parser.parse_args(argv)
    if args.subcommand == "check-output" and args.step is None:
        parser.error("check-output requires --step")
    if args.subcommand == "stamp" and args.event is None:
        parser.error("stamp requires --event")
    if args.agents is not None and args.agents < 0:
        parser.error("--agents must be non-negative")
    commands = {"confirm-input": confirm_input, "confirm-check": confirm_check,
                "judge-input": judge_input, "judged-merge": judged_merge}
    try:
        if args.subcommand == "stamp":
            stamp(args.run, args.event, args.agents)
        elif args.subcommand == "check-output":
            check_output(args.run, args.step)
        else:
            requirements = _read_json(args.run / "requirements.json", required=True)
            if args.subcommand == "judge-input":
                judge_input(args.run, requirements, args.attempt)
            elif args.subcommand == "mutant-view":
                mutant_view(args.run, args.collect)
            else:
                commands[args.subcommand](args.run, requirements)
        return 0
    except ModelStepMissing as error:
        sys.stdout.flush()
        print(error, file=sys.stderr)
        return 1
    except InputError as error:
        sys.stdout.flush()
        print(error, file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        sys.stdout.flush()
        print(f"{args.run}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
