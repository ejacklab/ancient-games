#!/usr/bin/env python3
"""trace_check.py — N1's check, written by the COO for run 20261012-index-md-build; copied for run 20261014-memory-index-cleanup with B2.7 added.

Every in-scope criterion id must be cited in the docstring of at least one test function in the given file.
It does NOT establish that the tests are right (N3's mutants do that), only that none of the criteria is forgotten.

  trace_check.py FILE            exit 0 when every id is cited, 1 otherwise (prints the missing ids)
  trace_check.py --self-test     proves the check can fail
"""
from __future__ import annotations

import ast
import re
import sys

IN_SCOPE = ("B1.1 B1.2 B1.3 B2.1 B2.2 B2.3 B2.4 B2.5 B2.6 B2.7 B2.8 B3.1 B3.2 B3.3 B3.4 B4.1 B4.2 B4.3 B4.4 B4.5 "
            "C1.1 C1.2 C1.3 C1.4 C2.1 C2.2 G1.1 G2.1 G2.3 G3.1 G3.2 G4.2").split()
ID = re.compile(r"\b([BCG]\d\.\d)\b")


def cited(source: str) -> dict[str, list[str]]:
    """{criterion id: [test names whose docstring cites it]}"""
    out: dict[str, list[str]] = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            for cid in set(ID.findall(ast.get_docstring(node) or "")):
                out.setdefault(cid, []).append(node.name)
    return out


def missing(source: str) -> list[str]:
    c = cited(source)
    return [i for i in IN_SCOPE if i not in c]


def self_test() -> int:
    full = "".join(f'def test_{n}():\n    """{i}"""\n' for n, i in enumerate(IN_SCOPE))
    assert missing(full) == [], "a file citing every id must pass"
    assert missing(full.replace('"""B3.1"""', '"""nothing"""')) == ["B3.1"], "a dropped id must be reported"
    assert missing("def helper():\n    '''B1.1'''\n") == IN_SCOPE, "a non-test docstring must not count"
    print("self-test: PASS")
    return 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--self-test"]:
        return self_test()
    m = missing(open(argv[1], encoding="utf-8").read())
    if m:
        print("missing criterion ids: " + " ".join(m))
        return 1
    print(f"all {len(IN_SCOPE)} in-scope ids cited")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
