import re

from conftest import by_id, good_files, stale_index_files

EVIDENCE = re.compile(
    r"[\w./-]+\.(?:md|py|ts|json|yaml|yml|sh)\b|\bgit\b|\bpython3?\b|\bexit\b|\bmemory_index\b"
)
FIVE = {"pass", "fail", "needs a reviewer", "not applicable", "could not run"}


def test_every_pass_and_fail_carries_evidence(lab):
    """C2-F1 — a pass or a fail must give its evidence: a file (and line) or the command and its output."""
    seen = {"pass": 0, "fail": 0}
    for files in (good_files(), stale_index_files()):
        project = lab.project(files)
        _, report = lab.report(project)
        for one in lab.results(report):
            if one.state not in seen:
                continue
            seen[one.state] += 1
            text = one.evidence.strip(" -—:|*`")
            assert len(text) >= 15 and EVIDENCE.search(text), f"{one.id} {one.state} without evidence: {one.line!r}"
    assert seen["pass"] > 0 and seen["fail"] > 0, f"the fixtures gave {seen}; both states are needed"


def test_every_requirement_has_one_of_the_five_results(lab):
    """C2-F2 — each requirement must get one of the five results, nothing outside them."""
    fixtures = {
        "clean": good_files(),
        "stale index": stale_index_files(),
        "no memory": {"AGENTS.md": "# Agents\n"},
    }
    for label, files in fixtures.items():
        project = lab.project(files)
        _, report = lab.report(project)
        table = by_id(lab.results(report))
        for ident in lab.all_ids():
            states = {one.state for one in table.get(ident, [])}
            assert states, f"{label}: {ident} has no line with a level and one of the five results"
            assert states <= FIVE, f"{label}: {ident} got {states}"
