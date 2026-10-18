import os

from conftest import good_files


def test_transcripts_and_credentials_are_never_opened(lab):
    """V3-F1 — a run must not open another agent's transcripts or credential files, wherever they sit."""
    project = lab.project(good_files(), ignore=[".env", "credentials.json", "project-memory/.cache/"])
    decoys = [
        lab.home / ".claude" / "projects" / "-tmp-other" / "session-1.jsonl",
        lab.home / ".codex" / "sessions" / "rollout-1.jsonl",
        lab.home / ".claude" / ".credentials.json",
        lab.home / ".aws" / "credentials",
        lab.home / ".ssh" / "id_rsa",
        lab.home / ".netrc",
        project / ".env",
        project / "credentials.json",
    ]
    # a named pipe cannot be opened for reading without a writer: an open of any of these blocks the tool for good
    for decoy in decoys:
        decoy.parent.mkdir(parents=True, exist_ok=True)
        os.mkfifo(decoy)
    agent = lab.home / ".claude" / "agent-memory" / "alpha"
    agent.mkdir(parents=True)
    (agent / "note.md").write_text("bytes\n", encoding="utf-8")

    modes = {"report on stdout": [], "--warn": ["--warn"]}
    for label, extra in modes.items():
        proc = lab.run(["--project", str(project), "--home", str(lab.home), *extra], home=lab.home)
        assert not proc.hung, f"{label}: the tool blocked, so it opened a transcript or credential file"
