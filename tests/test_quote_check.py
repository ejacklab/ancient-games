"""quote_check.py: an explorer's file:line quotes are checked against the code (method 3.8 item 10)."""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts/quote_check.py"

CODE = """def total(items):
    # sum the prices
    return sum(i.price for i in items)


def gate(count):
    if count > 3:
        return 'split'
    return 'one'
"""

HEADER = "| id | Claim | Kind | Source | Quote | Evidence |\n|---|---|---|---|---|---|\n"


def setup(tmp_path, rows, name="explore.md"):
    (tmp_path / "pkg").mkdir(exist_ok=True)
    (tmp_path / "pkg" / "calc.py").write_text(CODE)
    f = tmp_path / name
    f.write_text(rows if name.endswith(".jsonl") else "# Exploration\n\n" + HEADER + rows)
    return f


def run(f, root, *args):
    return subprocess.run([sys.executable, str(SCRIPT), str(f), "--root", str(root), *args],
                          capture_output=True, text=True)


def test_good_findings_pass_including_multiline_and_ran(tmp_path):
    f = setup(tmp_path,
              "| X1 | total sums prices | read | pkg/calc.py:3 | `return sum(i.price for i in items)` | — |\n"
              "| X2 | splits above three | ran | pkg/calc.py:7-8 | `if count > 3: return 'split'` | pytest -k gate |\n")
    r = run(f, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "2 findings: ok 2; kind ran 1, read 1" in r.stdout


def test_each_kind_of_bad_finding_fails(tmp_path):
    cases = {
        "wrong line": ("| X | c | read | pkg/calc.py:2 | `return sum(i.price for i in items)` | — |", "missing"),
        "no such file": ("| X | c | read | pkg/nope.py:3 | `return sum(i.price for i in items)` | — |", "does not exist"),
        "invented quote": ("| X | c | read | pkg/calc.py:3 | `return max(i.price for i in items)` | — |", "not found"),
        "line past end": ("| X | c | read | pkg/calc.py:99 | `return sum(i.price for i in items)` | — |", "outside the file"),
        "short quote": ("| X | c | read | pkg/calc.py:9 | `'one'` | — |", "shorter than"),
        "bad source": ("| X | c | read | calc.py line 3 | `return sum(i.price for i in items)` | — |", "is not path:LINE"),
        "bad kind": ("| X | c | guessed | pkg/calc.py:3 | `return sum(i.price for i in items)` | — |", "is not read or ran"),
        "ran without evidence": ("| X | c | ran | pkg/calc.py:3 | `return sum(i.price for i in items)` | — |",
                                 "names no evidence"),
    }
    for name, (row, want) in cases.items():
        r = run(setup(tmp_path, row + "\n"), tmp_path)
        assert r.returncode == 1 and want in r.stdout, (name, r.stdout)


def test_slack_reports_the_real_line(tmp_path):
    f = setup(tmp_path, "| X | c | read | pkg/calc.py:2 | `return sum(i.price for i in items)` | — |\n")
    assert run(f, tmp_path).returncode == 1
    r = run(f, tmp_path, "--slack", "2")
    assert r.returncode == 0 and "moved   X: quote is at pkg/calc.py:3" in r.stdout


def test_jsonl_escaped_pipe_and_fenced_placeholder(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "p.sh").write_text("cat log.txt | grep ERROR | wc -l\n")
    md = tmp_path / "e.md"
    md.write_text("```\n" + HEADER + "| X0 | placeholder | read / ran | path:1 | `x` | — |\n```\n\n" + HEADER
                  + "| X1 | counts errors | read | pkg/p.sh:1 | `grep ERROR \\| wc -l` | — |\n")
    r = run(md, tmp_path)
    assert r.returncode == 0 and "1 findings: ok 1" in r.stdout, r.stdout
    jl = tmp_path / "e.jsonl"
    jl.write_text(json.dumps({"id": "J1", "source": "pkg/p.sh:1", "quote": "cat log.txt | grep", "kind": "read"}) + "\n")
    assert run(jl, tmp_path).returncode == 0


def test_no_findings_is_a_usage_error(tmp_path):
    f = tmp_path / "empty.md"
    f.write_text("# nothing here\n")
    r = run(f, tmp_path)
    assert r.returncode == 2 and "no findings" in r.stderr
