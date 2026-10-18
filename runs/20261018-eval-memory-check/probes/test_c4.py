from conftest import by_id, good_files


def test_no_project_memory_means_no_failure(lab):
    """C4-F1 — with no project-memory/, no requirement may fail, and the absent location is named."""
    project = lab.project({"AGENTS.md": "# Agents\n"})
    _, report = lab.report(project)
    results = [one for one in lab.results(report) if ":" in one.id]

    assert results, "the report holds no SoT or CACHES result"
    for one in results:
        assert one.state not in ("fail", "pass", "could not run"), f"{one.id} on a project with no memory: {one.state}"
        if one.state == "not applicable":
            assert "project-memory" in one.line, f"{one.id} is not applicable but does not name the absent location"
    assert any(one.state == "not applicable" for one in results)


def test_no_cache_folder_means_cache_requirements_not_applicable(lab):
    """C4-F1 — with memory but no project-memory/.cache/, every cache requirement is not applicable, none fails."""
    project = lab.project(good_files())
    _, report = lab.report(project)
    table = by_id(lab.results(report))
    cache_ids = lab.caches()

    assert cache_ids, "the guidelines copy holds no cache requirement"
    for rid in cache_ids:
        lines = [one for ident, group in table.items() if ident.startswith(f"CACHES:{rid}") for one in group]
        assert lines, f"CACHES:{rid} has no result in the report"
        for one in lines:
            assert one.state == "not applicable", f"CACHES:{rid} with no cache folder: {one.state}"
            assert ".cache" in one.line, f"CACHES:{rid} does not name the absent cache folder"
