from conftest import good_files, no_why_files, stale_index_files


def test_a_failing_must_does_not_exit_zero(lab):
    """R3-F1 — a run with a failing MUST must exit 1, never 0."""
    fixtures = {
        "stale INDEX.md": stale_index_files(),
        "entry without Why": no_why_files(),
        "no AGENTS.md": good_files(agents=False),
    }
    for label, files in fixtures.items():
        project = lab.project(files)
        proc, _ = lab.report(project)
        assert proc.returncode == 1, f"{label}: exit {proc.returncode}, stderr: {proc.stderr[:200]}"
        printed = lab.run(["--project", str(project), "--home", str(lab.home)])
        assert not printed.hung
        assert printed.returncode == 1, f"{label} (report printed): exit {printed.returncode}"
