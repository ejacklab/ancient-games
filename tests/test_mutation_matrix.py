"""The mutation matrix must keep catching what it caught, and must never count a hole as a pass.

`tests/workflows/mutation_matrix.py` injects one known-bad change at a time into a design the gate passes, and
reports whether the rule that should fire does. Run as a test, it is the guard against a rule dying: a rule that
stops firing shows up here rather than in a green corpus run.

The second assertion is the one that keeps the matrix honest — a mutation that nothing catches must be reported as
a HOLE, never silently accepted. If one of the three remaining holes is closed, this test does not notice, which is
correct: it is a floor, not a ceiling.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MATRIX = ROOT / "tests/workflows/mutation_matrix.py"


def test_the_gate_catches_every_mutation_aimed_at_a_rule():
    r = subprocess.run([sys.executable, str(MATRIX)], capture_output=True, text=True, timeout=120)
    assert "MISSED" not in r.stdout, f"a rule stopped firing:\n{r.stdout}"
    assert "ALARM" not in r.stdout, f"something fired that should not have:\n{r.stdout}"
    assert r.returncode == 0, r.stdout + r.stderr


def test_the_matrix_reports_the_holes_it_cannot_plug():
    """Three holes are known and deliberate: the algorithm requires work the gate has no rule for, and the matrix
    must keep saying so rather than quietly dropping them from the list."""
    r = subprocess.run([sys.executable, str(MATRIX)], capture_output=True, text=True, timeout=120)
    assert "HOLE" in r.stdout, r.stdout
    for hole in ("no baseline", "no three-part stop", "five_things names only"):
        assert hole in r.stdout, f"{hole!r} disappeared from the matrix without a rule to cover it"


def test_the_matrix_can_fail():
    """House rule: proof the check can fail. Poison the base design and confirm the matrix goes red."""
    r = subprocess.run([sys.executable, str(MATRIX), "--self-check"], capture_output=True, text=True, timeout=120)
    assert "MUTATION MATRIX CAN FAIL" in r.stdout, (
        "the matrix's own sabotage did not register — then it is not known to be able to fail"
        f"\n{r.stdout}\n{r.stderr}")
