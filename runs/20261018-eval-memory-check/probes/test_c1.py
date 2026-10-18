from conftest import by_id, good_files, no_why_files, stale_index_files


def _states(table, ident):
    return {one.state for one in table.get(ident, [])}


def test_decidable_tool_and_git_records_are_checked(lab):
    """C1-F1 — a record whose check is tool or git must be checked where it can be decided, not left out."""
    project = lab.project(good_files())
    _, report = lab.report(project)
    table = by_id(lab.results(report))

    checked = 0
    for rid, record in lab.sot().items():
        checks = record["checks"]
        if not ({"tool", "git"} & set(checks)):
            continue
        states = _states(table, f"SoT:{rid}")
        assert states, f"SoT:{rid} (check: {'; '.join(checks)}) has no result in the report"
        assert "not applicable" not in states, f"SoT:{rid} is marked not applicable but the memory is there"
        if checks == ["tool"]:
            assert states == {"pass"}, f"SoT:{rid} (check: tool) on a clean memory: {states}"
        checked += 1
    assert checked > 0, "the guidelines copy holds no tool or git record"


def test_a_break_in_a_tool_record_is_found(lab):
    """C1-F1 — a break of a tool-checked record must come out as a fail, so the record was truly checked."""
    stale = lab.project(stale_index_files(), name="stale")
    _, stale_report = lab.report(stale)
    stale_table = by_id(lab.results(stale_report))
    for rid in ("K6.1a", "K6.2"):
        assert _states(stale_table, f"SoT:{rid}") == {"fail"}, f"SoT:{rid} on a stale INDEX.md"

    broken = lab.project(no_why_files(), name="nowhy")
    _, broken_report = lab.report(broken)
    broken_table = by_id(lab.results(broken_report))
    assert "fail" in _states(broken_table, "SoT:W1.3a"), "SoT:W1.3a on an entry with no Why line"


def test_a_record_the_tool_cannot_decide_is_not_passed_or_failed(lab):
    """C1-F2 — a record whose check is a reviewer must never get a pass or a fail."""
    reviewer_only = [rid for rid, record in lab.sot().items() if record["checks"] == ["reviewer"]]
    assert reviewer_only, "the guidelines copy holds no reviewer-only record"
    fixtures = {
        "clean": good_files(),
        "stale index": stale_index_files(),
        "entry without Why": no_why_files(),
    }
    for label, files in fixtures.items():
        project = lab.project(files)
        _, report = lab.report(project)
        table = by_id(lab.results(report))
        for rid in reviewer_only:
            states = _states(table, f"SoT:{rid}")
            assert states, f"{label}: SoT:{rid} has no result in the report"
            assert not (states & {"pass", "fail"}), f"{label}: SoT:{rid} (check: reviewer) got {states}"
