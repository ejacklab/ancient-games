import os

from conftest import CLAIM_TOKEN, WHY_TOKEN, good_files, mentions, no_why_files, stale_index_files


def _failing_ids(lab, report):
    """Failing or could-not-run MUSTs of the guidelines' records, as bare ids (F1 has its own warning line)."""
    return {
        one.bare
        for one in lab.results(report)
        if ":" in one.id and one.level.upper() == "MUST" and one.state in ("fail", "could not run")
    }


def test_warning_lists_every_failing_must(lab):
    """R2-F1 — the warning must list each MUST that fails or could not run, by id."""
    for label, files in {"stale index": stale_index_files(), "entry without Why": no_why_files()}.items():
        project = lab.project(files)
        _, report = lab.report(project)
        failing = _failing_ids(lab, report)
        assert failing, f"{label}: the report shows no failing MUST, and the fixture is broken"

        warning = lab.warn(project)
        assert not warning.hung, f"{label}: --warn did not finish"
        for rid in sorted(failing):
            assert mentions(warning.stdout, rid), f"{label}: the warning does not list {rid}:\n{warning.stdout}"


def test_warning_holds_only_failing_musts_and_a_missing_agents_md(lab):
    """R2-F2 — the warning must hold one line per failing MUST and a missing AGENTS.md, and never entry text."""
    fixtures = {
        "stale index, no AGENTS.md": stale_index_files(agents=False),
        "entry without Why, no AGENTS.md": no_why_files(agents=False),
    }
    for label, files in fixtures.items():
        project = lab.project(files)
        _, report = lab.report(project)
        failing = _failing_ids(lab, report)
        assert failing, f"{label}: the report shows no failing MUST, and the fixture is broken"

        warning = lab.warn(project)
        assert not warning.hung, f"{label}: --warn did not finish"
        lines = [line for line in warning.stdout.splitlines() if line.strip()]
        assert "AGENTS.md" in warning.stdout, f"{label}: the warning does not say AGENTS.md is missing"
        for line in lines:
            assert "AGENTS.md" in line or any(mentions(line, rid) for rid in failing), (
                f"{label}: a warning line names neither a failing MUST nor AGENTS.md: {line!r}"
            )
        assert len(lines) <= len(failing) + 1, f"{label}: more lines than failing MUSTs plus AGENTS.md:\n{warning.stdout}"
        for token in (CLAIM_TOKEN, WHY_TOKEN):
            assert token not in warning.stdout + warning.stderr, f"{label}: the warning holds entry text ({token})"


def test_warning_never_opens_a_cache_file(lab):
    """R2-F3 — the hook's --warn run must not open a file under project-memory/.cache/."""
    project = lab.project(good_files(), ignore=["project-memory/.cache/"])
    cache = project / "project-memory" / ".cache"
    (cache / "nested").mkdir(parents=True)
    # a named pipe cannot be opened for reading without a writer: an open of it blocks the tool for good
    os.mkfifo(cache / "index.sqlite")
    os.mkfifo(cache / "nested" / "vectors.bin")

    proc = lab.warn(project)

    assert not proc.hung, "--warn blocked: it opened a file under project-memory/.cache/"
