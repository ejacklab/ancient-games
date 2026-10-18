import os
import time

from conftest import diff_snapshots, good_files, snapshot


def test_a_run_writes_nothing_but_the_report(lab):
    """F3-F1 — a run must not create, change or delete any file (ignored ones included) other than the report."""
    files = good_files()
    files["CLAUDE.md"] = "# Claude\n"
    project = lab.project(files, ignore=["*.log", "project-memory/.cache/"])
    for rel in ("ignored.log", "project-memory/.cache/index.sqlite", "project-memory/work/w.md"):
        target = project / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("x\n", encoding="utf-8")
    (project / "AGENTS.md").write_text("# Agents\n\nchanged in the working tree only\n", encoding="utf-8")
    agent = lab.home / ".claude" / "agent-memory" / "alpha"
    agent.mkdir(parents=True)
    (agent / "note.md").write_text("x\n", encoding="utf-8")
    # make git's cached file stats stale, so a run that let git refresh its index would have something to write
    later = time.time() + 5
    os.utime(project / "CLAUDE.md", (later, later))

    report_file = lab.out / "report.md"
    modes = {
        "report on stdout": [],
        "--warn": ["--warn"],
        "--out": ["--out", str(report_file)],
    }
    for label, extra in modes.items():
        before = snapshot(project, lab.home, lab.elsewhere)
        proc = lab.run(["--project", str(project), "--home", str(lab.home), *extra], home=lab.home)
        assert not proc.hung, f"{label}: the tool did not finish"
        after = snapshot(project, lab.home, lab.elsewhere)
        changes = diff_snapshots(before, after)
        assert not changes, f"{label}: the run changed files other than the report: {changes[:8]}"
