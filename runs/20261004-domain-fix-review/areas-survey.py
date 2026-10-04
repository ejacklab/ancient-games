"""The survey check — n1..n3's contract, and proof the check can fail.

House rule: a check that has never failed is not a check. `--self-check` feeds this checker a deliberately broken
survey and requires it to reject it, before it is trusted on a real one.

  python3 areas-survey.py surveys/areas-claude-opus-5-5.md [...]
  python3 areas-survey.py --self-check
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
REGISTER = ROOT / "runs/20261004-defect-register.md"
VERDICTS = {"DIRECT", "SCHEMA", "DECISION", "DOC", "LATER"}

AREA = re.compile(r"^## Area (\d+)\.", re.M)
ROW = re.compile(r"^\|\s*(\d+\.\d+)\s*\|\s*([A-Z]+)\s*\|(.*?)\|\s*$", re.M)


def register_issues() -> dict[str, set[str]]:
    """{area number: {issue ids}} from the register's own tables."""
    out: dict[str, set[str]] = {}
    area = None
    for line in REGISTER.read_text().splitlines():
        m = re.match(r"^## (\d+)\.", line)
        if m:
            area = m.group(1)
            out.setdefault(area, set())
        m2 = re.match(r"^\| (\d+\.\d+) \|", line)
        if m2 and area:
            out[area].add(m2.group(1))
    return {a: v for a, v in out.items() if v}


def check(path: pathlib.Path) -> list[str]:
    text = path.read_text(errors="replace")
    want = register_issues()
    problems: list[str] = []

    areas = AREA.findall(text)
    if sorted(areas) != sorted(want):
        problems.append(f"areas present {sorted(areas)}, expected {sorted(want)}")

    rows = ROW.findall(text)
    seen: dict[str, str] = {}
    for issue, verdict, reason in rows:
        if verdict not in VERDICTS:
            problems.append(f"{issue}: verdict {verdict!r} is not one of {sorted(VERDICTS)}")
        if issue in seen:
            problems.append(f"{issue}: appears twice")
        seen[issue] = verdict
        if verdict == "DIRECT" and not re.search(r"check|test|mutation|gate|cmp|script", reason, re.I):
            problems.append(f"{issue}: marked DIRECT but names no check that would prove it")

    expected = {i for v in want.values() for i in v}
    missing = sorted(expected - set(seen))
    extra = sorted(set(seen) - expected)
    if missing:
        problems.append(f"{len(missing)} issue(s) missing: {', '.join(missing)}")
    if extra:
        problems.append(f"unknown issue id(s): {', '.join(extra)}")
    return problems


def self_check() -> int:
    """A survey missing an area, with a bad verdict and a DIRECT without a check, must be rejected."""
    sample = ROOT / "runs/20261004-domain-fix-review/.self-check-sample.md"
    areas = list(register_issues())
    lines = [f"## Area {a}. (self-check sample)\n" for a in areas[:-1]]        # one area deliberately missing
    lines.append("| 1.1 | MAYBE | nonsense verdict |\n")
    lines.append("| 1.2 | DIRECT | no proof here |\n")
    sample.write_text("".join(lines))
    got = check(sample)
    sample.unlink()
    ok = any("missing" in p for p in got) and any("not one of" in p for p in got) \
        and any("names no check" in p for p in got)
    print(f"MUTATION MATRIX CAN FAIL" if False else "SURVEY CHECK CAN FAIL" if ok else "SURVEY CHECK CANNOT FAIL")
    for p in got:
        print(f"  caught: {p[:110]}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-check" in argv:
        return self_check()
    paths = [pathlib.Path(a) for a in argv if not a.startswith("-")]
    if not paths:
        paths = sorted((ROOT / "runs/20261004-domain-fix-review/surveys").glob("areas-*.md"))
    if not paths:
        # Absence is not success. This is the very defect the register catalogues against readiness.py (3.2:
        # absent directories report "verified"); a check that passes when its subject does not exist is not a
        # check, and it would have made a missing survey look like a clean one.
        print("  FAIL  no survey files found — absence is not success")
        return 1
    bad = 0
    for p in paths:
        if not p.exists():
            print(f"  MISSING  {p}")
            bad += 1
            continue
        problems = check(p)
        print(f"  {'PASS' if not problems else 'FAIL'}  {p.name}")
        for x in problems:
            print(f"          {x[:150]}")
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
