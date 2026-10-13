#!/usr/bin/env python3
"""extract_content.py — copy the four seats' final lists and "who they are" into content/ancients.json, verbatim.

Blueprint: docs/blueprint/06-data-model.md (schema), 04-business-logic.md (which files). Nothing is reworded: each
field is the source text with only its list indentation removed, so check_content.py can test it as a substring.

Usage: extract_content.py [--runs DIR] [--out content/ancients.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PERSONS = [  # order is R1.1
    ("fan-li", "范蠡 (Fan Li)"),
    ("sun-tzu", "孫子 (Sun Tzu)"),
    ("lao-tzu", "老子 (Laozi)"),
    ("linus", "Linus Torvalds"),
]
FIELDS = {"Kind": "kind", "Rule": "rule", "Their words": "words", "Source": "source", "Words are": "label",
          "From": "from"}
KINDS = ("decision rule", "mindset", "algorithm")
ITEM_START = re.compile(r"^(?:### (\d{1,2})\. (.+)|(\d{1,2})\. \*\*(.+?)\*\*\s*)$")
FIELD_START = re.compile(r"^\s*- \*\*(" + "|".join(FIELDS) + r"):\*\*\s?(.*)$")


def section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        raise SystemExit(f"no '## {heading}' section")
    return m.group(1).strip("\n")


def items(final_list: str) -> list[dict]:
    out, cur, field = [], None, None
    for line in final_list.splitlines():
        m = ITEM_START.match(line)
        if m:
            cur = {"n": int(m.group(1) or m.group(3)), "title": (m.group(2) or m.group(4)).strip()}
            out.append(cur)
            field = None
            continue
        if cur is None:
            continue  # preamble before item 1
        f = FIELD_START.match(line)
        if f:
            field = FIELDS[f.group(1)]
            cur[field] = [f.group(2)]
        elif field:
            cur[field].append(line)
    for it in out:
        for key in FIELDS.values():
            lines = it.get(key, [])
            head, rest = (lines[0], lines[1:]) if lines else ("", [])
            it[key] = (head + ("\n" + textwrap.dedent("\n".join(rest)) if rest else "")).strip()
        kind = it["kind"].lower()
        it["kind_tag"] = next((k for k in KINDS if kind.startswith(k)), "")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=str(HERE.parent.parent / "runs" / "20261013-four-seats"))
    ap.add_argument("--out", default=str(HERE / "content" / "ancients.json"))
    a = ap.parse_args()
    runs = Path(a.runs)
    persons = []
    for pid, name in PERSONS:
        lst = runs / "final-opus" / f"{pid}.md"
        bio = runs / "identity" / f"{pid}.md"
        persons.append({
            "id": pid, "name": name,
            "who": {"markdown": section(bio.read_text(encoding="utf-8"), "Who they are"),
                    "source": str(bio.relative_to(runs.parent.parent))},
            "list_source": str(lst.relative_to(runs.parent.parent)),
            "items": items(section(lst.read_text(encoding="utf-8"), "Final list")),
        })
    doc = {"title": "The Ancient Games — Four Seats", "built_from": "runs/20261013-four-seats", "persons": persons}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {a.out}: " + ", ".join(f"{p['id']} {len(p['items'])}" for p in persons))
    return 0


if __name__ == "__main__":
    sys.exit(main())
