#!/usr/bin/env python3
"""spec_parse.py — read the product's REQUIREMENTS and VISION text into requirements.json (step E1).

Run:  python3 tools/evaluator/spec_parse.py --requirements REQUIREMENTS.md [--vision VISION.md] --out requirements.json

DATA.md's E1 section is the contract, and its rules 1 to 8 are the only thing this module knows about a spec file:
a group heading, the ids under it, its **Fails if** lines split into cases, the open ids, and the two vision sections.
Every requirement id read here lands in the manifest, because an id the run never reports on is a requirement the
run claims to have covered (EV-P2.1), and an id the file marks open lands out of scope instead (EV-R1.1).

`parse()` takes the two texts and returns requirements.json's content, with the `spec` paths null; only `main` fills
them. That is why a test can hand the function a fixture's bytes and get the document a real run writes (EV-R1).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# DATA.md Ids: `B1.1`, `EV-R1.2`, `W1.3`. A group heading holds the same shape without the `.n` part.
ID = r"[A-Z][A-Za-z]*(-[A-Z][A-Za-z]*)?\d+(\.\d+)?"
GROUP_HEADING = re.compile(r"^\*\*(?P<group>" + ID + r") — (?P<title>.*?)\*\*")
BULLET = re.compile(r"^(?P<indent> *)(?P<text>- .*|-$)\Z")
ID_BOLD = re.compile(r"^\*\*(?P<id>" + ID + r")(?:\s+[^*]*)?\*\*")

# DATA.md E1 rule 5: an id whose own text says it is open gets no verdict. The word has to end a clause — `.`, `;`,
# `,`, `)` or the end of the bullet — so "is open." and "leaves this open." count, while "is opened read-only" and
# "can open the source" do not.
OPEN_AT_CLAUSE_END = re.compile(r"\bopen\b(?=[.;,)]|\Z)", re.IGNORECASE)

IN_SCOPE = "in_scope"
OPEN = "open"
UNTESTABLE = "untestable"


class InputError(Exception):
    """A path the user named cannot be read. The message is the line the user gets on stderr."""


def report(text: str) -> None:
    """Print a problem to stderr. stdout is flushed first, so a piped run reads in order."""
    sys.stdout.flush()
    print(text, file=sys.stderr)


# --- one spec file -------------------------------------------------------------------------


def _starts_block(line: str) -> bool:
    """Whether a line begins something of its own, so the bullet above it has ended (DATA.md E1 rule 3)."""
    stripped = line.strip()
    return (not stripped
            or stripped.startswith("-")
            or stripped.startswith("#")
            or stripped.startswith(">")
            or GROUP_HEADING.match(line) is not None)


def _continues(line: str, indent: int) -> bool:
    """Whether `line` is the wrapped rest of a bullet at `indent` spaces."""
    return len(line) - len(line.lstrip(" ")) > indent and not _starts_block(line)


def _bullet_body(lines: list[str], index: int) -> tuple[str, int]:
    """The bullet at `index` with its continuation lines joined by one space, and the line after it."""
    body = BULLET.match(lines[index]).group("text")[1:].strip()
    indent = len(lines[index]) - len(lines[index].lstrip(" "))
    index += 1
    while index < len(lines) and _continues(lines[index], indent):
        body = f"{body} {lines[index].strip()}"
        index += 1
    return body.strip(), index


def _fails_if(body: str) -> str | None:
    """The text after a **Fails if** marker, or None when the bullet is not one (DATA.md E1 rule 3)."""
    for marker in ("**Fails if:**", "**Fails if**"):
        if body.startswith(marker):
            return body[len(marker):].strip()
    return None


def _is_open(text: str) -> bool:
    """Whether an id's own bullet text says the requirement is still open (DATA.md E1 rule 5)."""
    return OPEN_AT_CLAUSE_END.search(text) is not None


def _outside_code(text: str, separator: str) -> list[str]:
    """Split on `separator`, but never inside backticks or brackets: `(a, b)` and `x, y` in code stay whole."""
    parts, start, code, opened = [], 0, False, []
    index = 0
    while index < len(text):
        character = text[index]
        if character == "`":
            code = not code
        elif not code and character in "([{":
            opened.append(character)
        elif not code and character in ")]}" and opened:
            opened.pop()
        elif not code and not opened and text.startswith(separator, index):
            parts.append(text[start:index])
            index += len(separator)
            start = index
            continue
        index += 1
    parts.append(text[start:])
    return parts


def _split_cases(text: str) -> list[str]:
    """One Fails if into its failure cases (DATA.md E1 rule 4): `; ` when it has one, `, ` otherwise."""
    separator = "; " if len(_outside_code(text, "; ")) > 1 else ", "
    cases = []
    for part in _outside_code(text, separator):
        part = part.strip()
        for lead in ("or ", "and "):
            if part.lower().startswith(lead):
                part = part[len(lead):].strip()
                break
        if part.endswith("."):
            part = part[:-1].strip()
        if part:
            cases.append(part)
    return cases


def _close(group: dict) -> dict:
    """Give a collected group its status, its cases and the key order DATA.md's example uses."""
    texts = group.pop("fails")
    fails_if = " / ".join(texts)
    cases = [case for text in texts for case in _split_cases(text)]
    group["fails_if"] = fails_if
    group["cases"] = [{"case": f"{group['group']}-F{number}", "text": text}
                      for number, text in enumerate(cases, start=1)]
    if group["ids"] and all(identifier in group["open_ids"] for identifier in group["ids"]):
        group["status"] = OPEN
    elif group["ids"] and not fails_if:
        group["status"] = UNTESTABLE
    else:
        group["status"] = IN_SCOPE
    return {"group": group["group"], "title": group["title"], "ids": group["ids"],
            "status": group["status"], "fails_if": group["fails_if"],
            "cases": group["cases"], "open_ids": group["open_ids"]}


def _read_groups(text: str) -> list[dict]:
    """Every requirement group in the file, in file order (DATA.md E1 rules 1, 2, 3, 5, 6)."""
    lines = text.splitlines()
    groups, current, index = [], None, 0
    while index < len(lines):
        heading = GROUP_HEADING.match(lines[index])
        if heading is not None:
            current = {"group": heading.group("group"), "title": heading.group("title").strip(),
                       "ids": [], "open_ids": [], "fails": []}
            groups.append(current)
            index += 1
            continue
        if current is None or BULLET.match(lines[index]) is None:
            index += 1
            continue
        body, index = _bullet_body(lines, index)
        fails_if = _fails_if(body)
        if fails_if is not None:
            current["fails"].append(fails_if)
            continue
        bold = ID_BOLD.match(body)
        if bold is None:
            continue
        current["ids"].append(bold.group("id"))
        if _is_open(body[bold.end():]):
            current["open_ids"].append(bold.group("id"))
    return [_close(group) for group in groups]


# --- one vision file -----------------------------------------------------------------------


def _read_vision(text: str | None) -> list[dict]:
    """The two named vision sections as requirements, each bullet one id with one case (DATA.md E1 rule 7)."""
    if not text:
        return []
    sections = {"**What it will never do": "never", "**How we know it works": "how_we_know"}
    entries, section, lines, index = [], None, text.splitlines(), 0
    while index < len(lines):
        line = lines[index]
        if any(line.startswith(marker) for marker in sections):
            section = next(marker for marker in sections if line.startswith(marker))
            index += 1
            continue
        if line.startswith("**") or line.startswith("#"):
            section = None
            index += 1
            continue
        bullet = BULLET.match(line)
        if section is None or bullet is None:
            index += 1
            continue
        body, index = _bullet_body(lines, index)
        identifier = f"V{len(entries) + 1}"
        entries.append({"id": identifier, "section": sections[section], "text": body,
                        "cases": [{"case": f"{identifier}-F1", "text": body}]})
    return entries


def parse(requirements_text: str, vision_text: str | None = None) -> dict:
    """requirements.json's content for two texts, with the spec paths left null for `main` to fill (EV-R1)."""
    groups = _read_groups(requirements_text)
    vision = _read_vision(vision_text)
    manifest = [identifier for group in groups for identifier in group["ids"]]
    manifest += [entry["id"] for entry in vision]
    return {"spec": {"requirements": None, "vision": None}, "groups": groups,
            "vision": vision, "manifest": manifest}


# --- files and command line -----------------------------------------------------------------


def _read_text(path: Path) -> str:
    """One UTF-8 text file, or the line the user gets instead of a traceback."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise InputError(f"{path}: no such file") from None
    except IsADirectoryError:
        raise InputError(f"{path}: is a directory") from None
    except UnicodeDecodeError:
        raise InputError(f"{path}: not UTF-8 text") from None
    except OSError as error:
        raise InputError(f"{path}: {error.strerror or error}") from None


def _write_json(path: Path, document: dict) -> None:
    """Write requirements.json as UTF-8, the shape DATA.md's E1 example gives."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError as error:
        raise InputError(f"{path}: {error.strerror or error}") from None


def main(argv: list[str] | None = None) -> int:
    """Read the two spec files and write requirements.json. 0 when it wrote it, 2 on an input it cannot read."""
    parser = argparse.ArgumentParser(
        description="Read a product's REQUIREMENTS and VISION text into requirements.json.",
    )
    parser.add_argument("--requirements", required=True, help="the product's REQUIREMENTS file")
    parser.add_argument("--vision", help="the product's VISION file; optional")
    parser.add_argument("--out", required=True, help="where requirements.json is written")
    args = parser.parse_args(argv)
    try:
        document = parse(_read_text(Path(args.requirements)),
                         _read_text(Path(args.vision)) if args.vision else None)
        document["spec"] = {"requirements": args.requirements, "vision": args.vision}
        _write_json(Path(args.out), document)
    except InputError as error:
        report(str(error))
        return 2
    except OSError as error:  # e.g. --out is a folder: a problem, not a crash
        report(f"{error.filename or 'spec_parse.py'}: {error.strerror or error}")
        return 2
    print(f"wrote {args.out}: {len(document['groups'])} groups, "
          f"{len(document['manifest'])} ids in the manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())