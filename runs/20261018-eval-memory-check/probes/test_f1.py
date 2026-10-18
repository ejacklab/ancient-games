import re

from conftest import good_files, location_lines

NAMED = [
    "AGENTS.md",
    "CLAUDE.md",
    "project-memory/INDEX.md",
    "project-memory/entries",
    "project-memory/work",
    "project-memory/journal",
    "project-memory/.cache",
    ".claude/agent-memory",
]
OPTIONAL = NAMED[1:]


def _says(lines: list[str], word: str) -> bool:
    return any(re.search(r"\b" + word + r"\b", line, re.I) for line in lines)


def test_every_named_location_that_exists_is_found(lab):
    """F1-F1 — a named location that exists on disk must be reported as there, not missed or reported missing."""
    files = good_files()
    files["CLAUDE.md"] = "# Claude\n"
    project = lab.project(files, ignore=["project-memory/.cache/"])
    for rel in ("project-memory/work/w.md", "project-memory/journal/j.md", "project-memory/.cache/index.sqlite"):
        target = project / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("x\n", encoding="utf-8")
    agent = lab.home / ".claude" / "agent-memory" / "alpha"
    agent.mkdir(parents=True)
    (agent / "note.md").write_text("x\n", encoding="utf-8")

    _, report = lab.report(project)

    assert report, "no report was written"
    for name in NAMED:
        lines = location_lines(report, name)
        assert _says(lines, "present"), f"{name} exists but no line of the report says it is there"
        assert not _says(lines, "absent"), f"{name} exists but a line of the report says it is missing: {lines}"


def test_no_location_is_reported_that_does_not_exist(lab):
    """F1-F2 — a location that is not on disk must be reported as missing, never as found."""
    project = lab.project({"AGENTS.md": "# Agents\n"})

    _, report = lab.report(project)

    assert report, "no report was written"
    for name in OPTIONAL:
        lines = location_lines(report, name)
        assert lines, f"{name} is a named location and the report does not mention it"
        assert _says(lines, "absent"), f"{name} is not on disk but no line says it is missing: {lines}"
        assert not _says(lines, "present"), f"{name} is not on disk but a line says it is there: {lines}"


def test_missing_agents_md_is_a_failure(lab):
    """F1-F3 — a project with no AGENTS.md must fail the run and name AGENTS.md."""
    project = lab.project({"CLAUDE.md": "# Claude\n"})

    proc, report = lab.report(project)

    assert proc.returncode == 1, f"exit {proc.returncode}, stderr: {proc.stderr[:300]}"
    assert "AGENTS.md" in report + proc.stdout
