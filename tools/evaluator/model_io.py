#!/usr/bin/env python3
"""model_io.py — prepare and check the files around the confirm and judge model steps.

Run:  python3 tools/evaluator/model_io.py {confirm-input,confirm-check,judge-input,judged-merge} --run DIR

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
from pathlib import Path

GROUP_HEADING = re.compile(r"^\*\*(?P<group>[A-Z][A-Za-z]*(?:-[A-Z][A-Za-z]*)?\d+(?:\.\d+)?) — .*?\*\*", re.MULTILINE)
CODE_EVIDENCE = re.compile(r'^\s*(?P<file>.+?):\d+\s+"(?P<quote>.*?)"(?:\s+—\s+.*)?\s*$', re.DOTALL)
OUTPUT_LINES = 40


class InputError(Exception):
    """An unreadable input, with its path in the message printed on stderr."""


def _read_json(path: Path, required: bool = False) -> dict | list:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        if not required:
            return {}
        raise InputError(f"{path}: {error.strerror}") from None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InputError(f"{path}: {error}") from None
    if not isinstance(document, (dict, list)) or (required and not isinstance(document, dict)):
        raise InputError(f"{path}: expected a JSON {'object' if required else 'object or list'}")
    return document


def _read_text(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8")
    except FileNotFoundError:
        return ""
    except (OSError, UnicodeDecodeError) as error:
        raise InputError(f"{path}: {error}") from None


def _write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _entries(document: dict | list) -> list[dict]:
    rows = document if isinstance(document, list) else document.get("cases", [])
    return [row for row in rows if isinstance(row, dict)]


def _case_contexts(run: Path, requirements: dict) -> dict[str, dict]:
    """Case order comes from E1; group blocks retain the spec's original bytes."""
    text = _read_text(run / "workspace/spec/REQUIREMENTS.md")
    headings = list(GROUP_HEADING.finditer(text))
    blocks = {}
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        blocks[heading["group"]] = text[heading.start():end]
    contexts = {}
    for group in requirements.get("groups", []):
        for case in group.get("cases", []):
            contexts[case["case"]] = {
                "case": case["case"], "case_text": case.get("text", ""),
                "group_text": blocks.get(group["group"], ""),
            }
    for vision in requirements.get("vision", []):
        for case in vision.get("cases", []):
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
    matrix = _read_json(run / "matrix.json")
    contexts = _case_contexts(run, requirements)
    sources = _probe_sources(run / "probes")
    rows = []
    for probe, outcome in matrix.get("product", {}).items():
        if outcome != "fail":
            continue
        output = matrix.get("output", {}).get(probe, "")
        citations = matrix.get("citations", {}).get(probe, [])
        case = citations[0] if citations else ""
        context = contexts.get(case, {"case": case, "case_text": "", "group_text": ""})
        rows.append({**context, "probe": probe,
                     "probe_source": sources.get(_probe_key(probe).split('[')[0], ""),
                     "output": "\n".join(str(output).splitlines()[-OUTPUT_LINES:])})
    document = {"cases": rows}
    _write_json(run / "confirm-input.json", document)
    print(f"{len(rows)} to confirm")
    return document


def _quote_found(quote: str, source: str) -> bool:
    if not isinstance(quote, str) or not isinstance(source, str):
        return False
    collapsed = " ".join(quote.split())
    return bool(collapsed) and collapsed in " ".join(source.split())


def confirm_check(run: Path, requirements: dict) -> dict:
    inputs = _entries(_read_json(run / "confirm-input.json"))
    answers = _entries(_read_json(run / "confirm.json"))
    voided = 0
    for answer in answers:
        context = next((row for row in inputs
                        if row.get("case") == answer.get("case")
                        and _probe_key(row.get("probe", ""))
                        == _probe_key(answer.get("probe", ""))), {})
        if not (_quote_found(answer.get("requirement_quote", ""), context.get("group_text", ""))
                and _quote_found(answer.get("probe_quote", ""), context.get("probe_source", ""))):
            answer.update(faithful=False, note="quote not found")
            voided += 1
    document = {"cases": answers}
    _write_json(run / "confirm.json", document)
    print(f"{len(answers)} checked, {voided} voided")
    return document


def _product_file(product: Path, relative: str) -> Path | None:
    target = product / relative
    if product.resolve() not in target.resolve().parents or not target.is_file():
        return None
    return target


def judge_input(run: Path, requirements: dict) -> dict:
    contexts = _case_contexts(run, requirements)
    labels = {row.get("case"): row for row in _entries(_read_json(run / "classify.json"))}
    rows = [context for case, context in contexts.items()
            if labels.get(case, {}).get("kind") == "judged"
            and str(labels[case].get("reason") or "").strip()]
    plants = _entries(_read_json(run / "plants.json"))
    product = run / "workspace/product"
    copy = run / "judge-copy"
    if copy.is_symlink():
        copy.unlink()
    elif copy.exists():
        shutil.rmtree(copy)
    if product.is_dir():
        shutil.copytree(product, copy, symlinks=True)
    else:
        copy.mkdir(parents=True)
    plant_case = None
    for row in rows:
        for plant in plants:
            if plant.get("case") != row["case"]:
                continue
            target = _product_file(copy, str(plant.get("file", "")))
            old, new = plant.get("old"), plant.get("new")
            if target is None or not isinstance(old, str) or not old or not isinstance(new, str):
                continue
            try:
                text = target.read_bytes().decode("utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if text.count(old) != 1:
                continue
            target.write_bytes(text.replace(old, new, 1).encode("utf-8"))
            plant_case = row["case"]
            break
        if plant_case is not None:
            break
    document = {"cases": rows, "plant_case": plant_case}
    _write_json(run / "judge-input.json", document)
    print(f"{len(rows)} to judge")
    return document


def _code_quote_found(entry: dict, product: Path) -> bool:
    evidence = entry.get("evidence", "")
    if not isinstance(evidence, str):
        return False
    match = CODE_EVIDENCE.fullmatch(evidence)
    if match is None or (entry.get("holds") is not True and entry.get("holds") is not False):
        return False
    target = _product_file(product, match["file"])
    return target is not None and _quote_found(match["quote"], _read_text(target))


def judged_merge(run: Path, requirements: dict) -> dict:
    inputs = _read_json(run / "judge-input.json")
    rows = _entries(inputs)
    if not rows:
        document = {"plant_found": True, "cases": []}
    else:
        plant_case = inputs.get("plant_case")
        first = {entry.get("case"): entry for entry in _entries(_read_json(run / "judge-1.json"))
                 if _code_quote_found(entry, run / "judge-copy")}
        second = {entry.get("case"): entry for entry in _entries(_read_json(run / "judge-2.json"))
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
    _write_json(run / "judged.json", document)
    print(f"plant_found: {str(document['plant_found']).lower()}")
    return document


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("subcommand", choices=["confirm-input", "confirm-check", "judge-input", "judged-merge"])
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args(argv)
    commands = {"confirm-input": confirm_input, "confirm-check": confirm_check,
                "judge-input": judge_input, "judged-merge": judged_merge}
    try:
        requirements = _read_json(args.run / "requirements.json", required=True)
        commands[args.subcommand](args.run, requirements)
        return 0
    except InputError as error:
        sys.stdout.flush()
        print(error, file=sys.stderr)
        return 2
    except OSError as error:
        sys.stdout.flush()
        print(f"{error.filename or args.run}: {error.strerror or error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
