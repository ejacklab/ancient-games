from conftest import good_files

CACHE_FILE = "project-memory/.cache/index.sqlite"


def _cache_project(lab, *, ignored: bool, agents_text: str | None = None):
    files = good_files()
    if agents_text is not None:
        files["AGENTS.md"] = agents_text
    project = lab.project(files, ignore=["project-memory/.cache/"] if ignored else None)
    target = project / CACHE_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("cache bytes\n", encoding="utf-8")
    return project


def _states(lab, project, wanted: tuple[str, ...]) -> set[str]:
    _, report = lab.report(project)
    found = {one.state for one in lab.results(report) if one.id.startswith("CACHES:") and one.bare in wanted}
    assert found, f"the report has no result for CACHES:{'/'.join(wanted)}"
    return found


def test_b2_and_rd1_are_checked_when_the_cache_folder_exists(lab):
    """C6-F1 — with a cache folder, B2.2 and Rd1 must each be decided: pass when it holds, fail when it breaks."""
    B2, RD1 = ("B2", "B2.2"), ("Rd1", "Rd1.1")

    clean = _cache_project(lab, ignored=True)
    assert _states(lab, clean, B2) == {"pass"}, "B2.2 on a cache folder that git ignores"
    assert _states(lab, clean, RD1) == {"pass"}, "Rd1 on a project whose instructions never open a cache file"

    open_cache = _cache_project(lab, ignored=True, agents_text=(
        "# Agents\n\nAt the start of each session, read project-memory/.cache/index.sqlite first.\n"
    ))
    assert _states(lab, open_cache, RD1) == {"fail"}, "Rd1 on an instruction that opens a cache file at session start"

    not_ignored = _cache_project(lab, ignored=False)
    assert _states(lab, not_ignored, B2) == {"fail"}, "B2.2 on a cache folder that git does not ignore"


def test_other_cache_requirements_are_left_to_a_reviewer(lab):
    """C6-F2 — with a cache folder, a cache requirement other than B2.2 and Rd1 must not get a pass or a fail."""
    project = _cache_project(lab, ignored=True)
    _, report = lab.report(project)
    others = [
        one for one in lab.results(report)
        if one.id.startswith("CACHES:") and one.bare not in ("B2", "B2.2", "Rd1", "Rd1.1")
    ]

    assert len(others) >= 5, f"too few other cache requirements found in the report: {[o.id for o in others]}"
    for one in others:
        assert one.state not in ("pass", "fail"), f"{one.id} got {one.state}, but only B2.2 and Rd1 are checked"
