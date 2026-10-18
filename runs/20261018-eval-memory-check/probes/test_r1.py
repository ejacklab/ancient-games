import re

from conftest import good_files, mentions, no_why_files, stale_index_files


def test_every_c1_requirement_is_in_the_report(lab):
    """R1-F1 — every requirement of C1 (each SoT record, each CACHES core requirement) must be in the report."""
    fixtures = {
        "clean": good_files(),
        "stale index": stale_index_files(),
        "no memory": {"AGENTS.md": "# Agents\n"},
    }
    ids = lab.all_ids()
    assert len(ids) > 10, "the guidelines copy gave too few requirement ids"
    for label, files in fixtures.items():
        project = lab.project(files)
        _, report = lab.report(project)
        assert report, f"{label}: no report was written"
        for ident in ids:
            assert re.search(re.escape(ident) + r"(?![A-Za-z0-9])", report), f"{label}: {ident} is missing from the report"


def test_report_results_match_the_checks(lab):
    """R1-F2 — the results in the report must match the checks' own: the warning and the exit code."""
    for label, files in {"stale index": stale_index_files(), "entry without Why": no_why_files()}.items():
        project = lab.project(files)
        _, report = lab.report(project)
        results = [one for one in lab.results(report) if ":" in one.id and one.level.upper() == "MUST"]
        failing = {one.bare for one in results if one.state in ("fail", "could not run")}
        passing = {one.bare for one in results if one.state not in ("fail", "could not run")}
        assert failing, f"{label}: the report shows no MUST failing, and the fixture is broken"

        warning = lab.warn(project)
        assert not warning.hung
        for rid in failing:
            assert mentions(warning.stdout, rid), f"{label}: the report says {rid} fails but the warning does not list it"
        for rid in passing - failing:
            assert not mentions(warning.stdout, rid), f"{label}: the report says {rid} is not failing but the warning lists it"
