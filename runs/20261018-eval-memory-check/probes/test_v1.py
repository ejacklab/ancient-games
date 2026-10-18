from conftest import ENTRY_NAME, INDEX_GOOD, diff_snapshots, snapshot, stale_index_files


def test_memory_entries_index_and_cache_are_left_untouched(lab):
    """V1-F1 — a run must not change any memory, entry, index or cache; only its own report is written."""
    project = lab.project(stale_index_files(), ignore=["project-memory/.cache/"])
    # the working tree holds an index that differs from the staged one: a tool that "fixes" it would change it
    (project / "project-memory" / "INDEX.md").write_text(INDEX_GOOD, encoding="utf-8")
    for rel in ("project-memory/.cache/index.sqlite", "project-memory/work/w.md", "project-memory/journal/j.md"):
        target = project / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("bytes\n", encoding="utf-8")
    (project / "project-memory" / "entries" / "F-new.md").write_text("not staged\n", encoding="utf-8")
    agent = lab.home / ".claude" / "agent-memory" / "alpha"
    agent.mkdir(parents=True)
    (agent / "note.md").write_text("bytes\n", encoding="utf-8")
    assert (project / "project-memory" / "entries" / ENTRY_NAME).is_file()

    report_file = lab.out / "report.md"
    modes = {"report on stdout": [], "--warn": ["--warn"], "--out": ["--out", str(report_file)]}
    for label, extra in modes.items():
        before = snapshot(project / "project-memory", lab.home / ".claude")
        proc = lab.run(["--project", str(project), "--home", str(lab.home), *extra], home=lab.home)
        assert not proc.hung, f"{label}: the tool did not finish"
        changes = diff_snapshots(before, snapshot(project / "project-memory", lab.home / ".claude"))
        assert not changes, f"{label}: the run changed memory: {changes[:8]}"
