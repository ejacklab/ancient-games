import subprocess

from conftest import by_id, no_why_files, stale_index_files


def _index_tool_fails(lab, project):
    done = subprocess.run(
        ["python3", str(lab.index_tool), "--check"],
        cwd=project,
        env=lab.env(),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    return done.returncode


def test_no_pass_where_memory_index_check_fails(lab):
    """C3-F1 — the index and entry checks must not be a pass when tools/memory_index.py --check fails."""
    stale = lab.project(stale_index_files(), name="stale")
    assert _index_tool_fails(lab, stale) == 1, "the fixture does not fail memory_index.py --check"
    _, report = lab.report(stale)
    table = by_id(lab.results(report))
    for rid in ("K6.1a", "K6.2"):
        states = {one.state for one in table.get(f"SoT:{rid}", [])}
        assert states and "pass" not in states, f"SoT:{rid}: memory_index.py --check fails on a stale INDEX.md, tool says {states}"
    assert any(one.state == "fail" for one in table.get("SoT:K6.2", []) + table.get("SoT:K6.1a", []))

    broken = lab.project(no_why_files(), name="nowhy")
    assert _index_tool_fails(lab, broken) == 1, "the fixture does not fail memory_index.py --check"
    _, broken_report = lab.report(broken)
    broken_table = by_id(lab.results(broken_report))
    states = {one.state for one in broken_table.get("SoT:W1.3a", [])}
    assert states and "pass" not in states, f"SoT:W1.3a: memory_index.py --check fails on an entry with no Why, tool says {states}"
