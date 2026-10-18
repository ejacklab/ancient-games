from conftest import good_files


def test_given_path_is_the_project(lab):
    """F2-F1 — a path given with --project must be the project checked, not the current folder."""
    project = lab.project(good_files())
    other = lab.project({"AGENTS.md": "# Other\n"}, name="other")

    proc = lab.run(["--project", str(project), "--home", str(lab.home)], cwd=other)

    assert not proc.hung, "the tool did not finish"
    assert str(project) in proc.stdout, f"the given root is not printed; stdout starts: {proc.stdout[:300]!r}"
    assert str(other) not in proc.stdout, "the current folder was checked instead of the given path"


def test_path_that_is_not_a_git_root_is_a_usage_error(lab):
    """F2-F2 — a folder inside a repository, or outside any, must exit 2 and not be checked."""
    project = lab.project(good_files())
    inside = project / "project-memory"
    outside = lab.base / "plain-folder"
    outside.mkdir()

    for target in (inside, outside):
        proc = lab.run(["--project", str(target), "--home", str(lab.home)])
        assert not proc.hung, f"the tool did not finish for {target}"
        assert proc.returncode == 2, f"{target}: exit {proc.returncode}, stdout starts: {proc.stdout[:200]!r}"
