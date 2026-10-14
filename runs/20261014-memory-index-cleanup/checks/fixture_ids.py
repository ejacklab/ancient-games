#!/usr/bin/env python3
"""fixture_ids.py — N1's lint, written by the COO for run 20261014-memory-index-cleanup (Dave's masking risk).

Every literal id in the acceptance file must be in W1.1's form `DD-MM-xxxxxx-YYYY`, so that a test meant to fail for
another reason cannot pass on its id alone. An id meant to be bad may appear only inside a test function whose
docstring cites B2.3 or G4.2.

A literal id is: a string given as `id=` to a call (not to `pytest.param`, whose `id` names a test case), a string default of a parameter named `id`, or the value of a
top-level `id:` line inside a string or bytes literal (quotes and spaces stripped, as B2.1 reads it).
What it does NOT establish: ids computed at run time (`id=name[:-3]`, `id=str(n)`, a loop variable) are not seen;
the N1 brief names those places, and the gate against a script with the id check catches the rest.

  fixture_ids.py FILE            exit 0 when every literal id is in the form, 1 otherwise (prints each)
  fixture_ids.py --self-test     proves the lint can fail
"""
from __future__ import annotations

import ast
import re
import sys

FORM = re.compile(r"[0-9]{2}-[0-9]{2}-[a-z0-9]{6}-[0-9]{4}")
ID_LINE = re.compile(r"(?m)^id:(.*)$")
HOLE = "\x00"
EXEMPT = re.compile(r"\b(B2\.3|G4\.2)\b")


def strip(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        v = v[1:-1]
    return v.strip()


def text_of(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Constant) and isinstance(node.value, bytes):
        return node.value.decode("latin-1")
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value if isinstance(v, ast.Constant) else HOLE for v in node.values)
    return None


def bad_ids(source: str) -> list[tuple[int, str]]:
    tree = ast.parse(source)
    exempt: set[int] = set()
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and fn.name.startswith("test") \
                and EXEMPT.search(ast.get_docstring(fn) or ""):
            exempt.update(id(n) for n in ast.walk(fn))
    inside_fstring = {id(c) for n in ast.walk(tree) if isinstance(n, ast.JoinedStr) for c in n.values}
    found: list[tuple[int, str]] = []

    def check(node: ast.AST, value: str) -> None:
        if id(node) not in exempt and HOLE not in value and not FORM.fullmatch(value):
            found.append((node.lineno, value))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
            for kw in node.keywords if name != "param" else ():  # pytest.param(id=...) names a case, not an entry
                if kw.arg == "id" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    check(kw.value, kw.value.value)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = node.args
            pos = args.posonlyargs + args.args
            pairs = list(zip(pos[len(pos) - len(args.defaults):], args.defaults)) + \
                [(a, d) for a, d in zip(args.kwonlyargs, args.kw_defaults) if d is not None]
            for a, d in pairs:
                if a.arg == "id" and isinstance(d, ast.Constant) and isinstance(d.value, str):
                    check(d, d.value)
        if id(node) in inside_fstring:
            continue
        text = text_of(node)
        if text is not None:
            for m in ID_LINE.finditer(text):
                check(node, strip(m.group(1)))
    return found


def self_test() -> int:
    good = '''def write_entry(repo, *, id="14-10-a1b2c3-2026"):\n    pass\n
def test_ok():\n    """B1.1"""\n    write_entry(1, id="01-02-zzzzzz-2026")\n    x = "---\\nid: '03-04-abc123-2026'\\n---\\n"\n'''
    assert bad_ids(good) == [], bad_ids(good)
    assert [v for _, v in bad_ids(good.replace("14-10-a1b2c3-2026", "D-20261012-a1"))] == ["D-20261012-a1"]
    assert [v for _, v in bad_ids(good.replace("01-02-zzzzzz-2026", "bad"))] == ["bad"]
    assert [v for _, v in bad_ids(good.replace("'03-04-abc123-2026'", "old"))] == ["old"]
    assert [v for _, v in bad_ids('X = b"---\\nid: bad\\n"\n')] == ["bad"]
    assert [v for _, v in bad_ids('X = f"---\\nid: old\\nstatus: {s}\\n"\n')] == ["old"]
    assert bad_ids('X = f"---\\nid: {i}\\n"\n') == [], "a computed id is not a literal"
    assert bad_ids('X = "ignored:\\n  id: nested\\n"\n') == [], "a nested id is not a top-level id"
    assert bad_ids('X = pytest.param("a", id="case-name")\n') == [], "a pytest case name is not an entry id"
    exempt = '''def test_form():\n    """B2.3: a bad id fails"""\n    write_entry(1, id="bad")\n'''
    assert bad_ids(exempt) == [], "a bad id inside a B2.3 test is allowed"
    assert bad_ids(exempt.replace("B2.3", "B2.4")) != [], "outside B2.3/G4.2 it is not"
    print("self-test: PASS")
    return 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--self-test"]:
        return self_test()
    found = bad_ids(open(argv[1], encoding="utf-8").read())
    for line, value in found:
        print(f"{argv[1]}:{line}: id not in W1.1's form outside a B2.3/G4.2 test: {value!r}")
    if found:
        print(f"{len(found)} literal id(s) not in W1.1's form")
        return 1
    print("every literal id is in W1.1's form, or inside a B2.3/G4.2 test")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
