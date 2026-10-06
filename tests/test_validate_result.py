import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts/validate_result.py"

GOOD = """---
node: n2
attempt: 1
engine: codex
model: gpt-6.1-sol
status: ok
started: 2026-10-02T10:00:00Z
ended: 2026-10-02T10:03:10Z
evidence: ev.txt
---
Returned the three rows asked for.
line 2
"""


def run(tmp_path, text, *args):
    f = tmp_path / "r.md"
    if text is not None:
        f.write_text(text)
    return subprocess.run([sys.executable, str(SCRIPT), str(f), *args], capture_output=True, text=True)


def test_valid_result_and_summary_cap(tmp_path):
    (tmp_path / "ev.txt").write_text("proof")
    r = run(tmp_path, GOOD, "--node", "n2", "--attempt", "1", "--model", "gpt-6.1-sol",
            "--root", str(tmp_path), "--summary", "1")
    assert r.returncode == 0 and r.stdout.startswith("ok ")
    assert "Returned the three rows" in r.stdout and "line 2" not in r.stdout


def test_each_instability_is_a_failure(tmp_path):
    (tmp_path / "ev.txt").write_text("proof")
    cases = {
        "missing file": (None, "does not exist"),
        "empty file": ("  \n", "empty"),
        "no header": ("just text, no header\n", "no header"),
        "missing key": (GOOD.replace("model: gpt-6.1-sol\n", ""), "missing 'model'"),
        "bad status": (GOOD.replace("status: ok", "status: done"), "status"),
        "empty body": (GOOD.split("---\n")[0] + "---\n" + GOOD.split("---\n")[1] + "---\n", "body is empty"),
    }
    for name, (text, want) in cases.items():
        r = run(tmp_path, text, "--root", str(tmp_path))
        assert r.returncode == 1 and want in r.stdout, (name, r.stdout)
        (tmp_path / "r.md").unlink(missing_ok=True)


def test_a_prelude_before_the_header_is_tolerated(tmp_path):
    """A real run (2026-10-05) had claude print one sentence of context before the `---` header, and the strict
    'header at byte 0' contract blocked the whole node on 'no header'. The header is the first `---` block,
    wherever it is; a harmless prelude is discarded."""
    (tmp_path / "ev.txt").write_text("proof")
    prelude = "I've checked how this repo's tests import the scripts. Writing now.\n\n"
    r = run(tmp_path, prelude + GOOD, "--root", str(tmp_path))
    assert r.returncode == 0, r.stdout


def test_contract_mismatches(tmp_path):
    (tmp_path / "ev.txt").write_text("proof")
    for args, want in [(["--model", "qwen3.8-flash"], "model"), (["--node", "n9"], "node"),
                       (["--attempt", "2"], "attempt")]:
        r = run(tmp_path, GOOD, *args, "--root", str(tmp_path))
        assert r.returncode == 1 and want in r.stdout, (args, r.stdout)
    r = run(tmp_path, GOOD, "--root", str(tmp_path / "nowhere"))   # evidence path missing
    assert r.returncode == 1 and "evidence path" in r.stdout


def test_digest_cap_and_headings(tmp_path):
    good = "# Digest\n**Answer.** x\n**Confidence.** y\n**Decision it triggers.** z\n"
    assert run(tmp_path, good, "--kind", "digest").returncode == 0
    r = run(tmp_path, good.replace("**Confidence.** y\n", ""), "--kind", "digest")
    assert r.returncode == 1 and "Confidence" in r.stdout
    r = run(tmp_path, good + "x\n" * 30, "--kind", "digest")
    assert r.returncode == 1 and "cap" in r.stdout
