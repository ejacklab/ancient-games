import re

from conftest import good_files


def _history(lab):
    """Four commits: the project, a README, the memory (the first to touch project-memory/), a README change."""
    project = lab.project({"AGENTS.md": "# Agents\n"}, name="history")
    first = lab.git(project, "rev-parse", "HEAD")
    (project / "README.md").write_text("one\n", encoding="utf-8")
    second = lab.commit_all(project, "readme")
    for rel, text in good_files(agents=False).items():
        target = project / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    third = lab.commit_all(project, "memory")
    (project / "README.md").write_text("two\n", encoding="utf-8")
    lab.commit_all(project, "readme again")
    return project, first, second, third


def test_first_line_names_the_snapshot_and_the_range(lab):
    """C5-F1 — the first line of the report must name the snapshot checked and the history range."""
    project, first, second, third = _history(lab)

    _, report = lab.report(project)
    line = report.splitlines()[0] if report else ""
    assert re.search(r"stag|index", line, re.I), f"the first line does not name the snapshot: {line!r}"
    # the range starts at the first commit that touches project-memory/ (or its parent)
    assert third[:7] in line or second[:7] in line, f"the first line does not name the range: {line!r}"

    _, report_since = lab.report(project, since=first)
    line_since = report_since.splitlines()[0] if report_since else ""
    assert re.search(r"stag|index", line_since, re.I), f"the first line does not name the snapshot: {line_since!r}"
    assert first[:7] in line_since, f"--since {first[:7]} is not the range named in the first line: {line_since!r}"
