import re

from conftest import good_files

EVIDENCE = re.compile(
    r"[\w./-]+\.(?:md|py|ts|json|yaml|yml|sh)\b|\bgit\b|\bpython3?\b|\bexit\b|\bmemory_index\b"
)


def test_no_pass_without_evidence(lab):
    """V2-F1 — a requirement must never be said to pass without the evidence (file and line, or command and output)."""
    passes = 0
    for files in (good_files(), {"AGENTS.md": "# Agents\n"}):
        project = lab.project(files)
        proc, report = lab.report(project)
        for one in lab.results(report):
            if one.state != "pass":
                continue
            passes += 1
            text = one.evidence.strip(" -—:|*`")
            assert len(text) >= 15 and EVIDENCE.search(text), f"{one.id} passes without evidence: {one.line!r}"
    assert passes > 0, "no pass line was found in the reports"
