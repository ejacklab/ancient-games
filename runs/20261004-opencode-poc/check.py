"""Objective checks for the opencode / MiniMax-M3.1-Flash-Preview POC.

Each check is mechanical and can fail: no "looks good". Exit code is non-zero if any check fails, so this is a
real gate rather than a report.
"""
import html.parser
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def out(name: str) -> str:
    p = HERE / f"{name}_out.txt"
    return ANSI.sub("", p.read_text(errors="replace")) if p.exists() else ""


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.attrs = [], []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.attrs.append(dict(attrs))


def check_p1() -> list[tuple[str, bool, str]]:
    f = HERE / "p1" / "index.html"
    if not f.exists():
        return [("p1 file written", False, "p1/index.html missing")]
    raw = f.read_text(errors="replace")
    size = len(raw.encode())
    p = Parser()
    p.feed(raw)
    external = re.findall(r"""(?:src|href)\s*=\s*["'](https?:)?//""", raw, re.I)
    tabs = [a for a in p.attrs if a.get("role") == "tab"]
    return [
        ("p1 file written", True, f"{size:,} bytes"),
        ("p1 under 12 KB", size < 12_288, f"{size:,} bytes"),
        ("p1 no external resources", not external, f"{len(external)} external refs"),
        ("p1 three role=tab", len(tabs) == 3, f"{len(tabs)} found"),
        ("p1 aria-selected present", any("aria-selected" in a for a in tabs), "on tab buttons"),
        ("p1 inline SVG chart", "svg" in p.tags, f"tags: {sorted(set(p.tags))[:8]}"),
        ("p1 prefers-color-scheme", "prefers-color-scheme" in raw, "dark theme rule"),
        ("p1 viewport meta", 'name="viewport"' in raw or "name='viewport'" in raw, "responsive meta"),
        ("p1 parses as HTML", True, f"{len(p.tags)} tags parsed"),
    ]


def check_p2() -> list[tuple[str, bool, str]]:
    exp = json.loads((HERE / "p2_expected.json").read_text())
    text = out("p2")
    res = []
    for name, code in exp["needles"].items():
        found = re.search(rf"{name}\s*=\s*(\d+)", text)
        got = int(found.group(1)) if found else None
        res.append((f"p2 {name} code", got == code, f"expected {code}, got {got}"))
    tot = re.search(r"SUM\s*=\s*(\d+)", text)
    got = int(tot.group(1)) if tot else None
    res.append(("p2 sum of three", got == exp["sum"], f"expected {exp['sum']}, got {got}"))
    return res


def check_p3() -> list[tuple[str, bool, str]]:
    exp = json.loads((HERE / "p3_expected.json").read_text())
    text = out("p3")
    m = re.search(r"C\s*=\s*(\d+)", text)
    got_c = int(m.group(1)) if m else None
    m2 = re.search(r"HIGHEST\s*=\s*([A-E])", text)
    got_h = m2.group(1) if m2 else None
    return [
        ("p3 reads bar C", got_c == exp["C"], f"expected {exp['C']}, got {got_c}"),
        ("p3 names tallest bar", got_h == exp["HIGHEST"], f"expected {exp['HIGHEST']}, got {got_h}"),
    ]


def check_p4() -> list[tuple[str, bool, str]]:
    exp = json.loads((HERE / "p4_expected.json").read_text())
    text = out("p4")
    m = re.search(r"NUMBERS\s*=\s*([0-9,\s]+)", text)
    got = [int(x) for x in re.findall(r"\d+", m.group(1))] if m else []
    return [("p4 video numbers in order", got == exp["NUMBERS"], f"expected {exp['NUMBERS']}, got {got}")]


def check_p5() -> list[tuple[str, bool, str]]:
    d = HERE / "p5_repo"
    r = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=d, capture_output=True, text=True, timeout=120)
    tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
    fixed = "off by one" not in (d / "calc.py").read_text()
    return [
        ("p5 bug removed", fixed, "the `- 1` is gone" if fixed else "calc.py still has the bug"),
        ("p5 tests pass (the check)", r.returncode == 0, tail),
    ]


def check_p6() -> list[tuple[str, bool, str]]:
    leaked = (HERE / "plan_should_not_exist.txt").exists()
    return [("p6 plan agent cannot write", not leaked, "no file created" if not leaked else "FILE WAS CREATED")]


if __name__ == "__main__":
    groups = [("P1 frontend", check_p1), ("P2 long context", check_p2), ("P3 vision", check_p3),
              ("P4 video", check_p4), ("P5 agentic fix", check_p5), ("P6 read-only agent", check_p6)]
    failed = 0
    for title, fn in groups:
        print(f"\n{title}")
        for label, ok, ev in fn():
            print(f"  [{'PASS' if ok else 'FAIL'}] {label:34} {ev}")
            failed += 0 if ok else 1
    print(f"\n{'ALL CHECKS PASS' if not failed else f'{failed} CHECK(S) FAILED'}")
    sys.exit(0 if not failed else 1)
