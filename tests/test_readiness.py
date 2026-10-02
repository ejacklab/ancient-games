"""RT-01–RT-21: readiness inventory with an isolated HOME and fake executables."""
from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import time
import uuid
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / ".claude/skills/workflow-design/scripts/readiness.py"
BINARIES = ["claude", "codex", "agy", "qwen", "node", "python3", "git"]
GROUPS = ["Tools", "Models and logins", "Skills and workflows", "Memory", "MCP",
          "Machine", "Open unknowns"]
MCP_LABELS = {"~/.claude/settings.json", "~/.claude.json", "~/.qwen/settings.json",
              ".mcp.json (project)"}


@pytest.fixture
def sandbox(tmp_path):
    home, bin_dir, cwd = (tmp_path / name for name in ("home", "bin", "proj"))
    for path in (home, bin_dir, cwd):
        path.mkdir()
    logs = tmp_path / "logs"
    logs.mkdir()
    # Do not inherit credentials, tool configuration, or a fallback search PATH.
    env = {"HOME": str(home), "PATH": str(bin_dir), "FAKE_LOGS": str(logs)}

    def fake(name, body=None):
        if body is None:
            body = f"print({name + '-fake 0.1'!r})\n"
        path = bin_dir / name
        path.write_text(
            f"#!{sys.executable}\n"
            "import json, os, sys\n"
            f"with open(os.path.join(os.environ['FAKE_LOGS'], {name!r}), 'a') as log:\n"
            "    log.write(json.dumps(sys.argv[1:]) + '\\n')\n" + body
        )
        path.chmod(0o755)
        return path

    def full():
        for name in BINARIES:
            fake(name)

    def run(*args, timeout=35):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              env=env, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout)

    def calls(name):
        path = logs / name
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def reset_logs():
        for path in logs.iterdir():
            path.unlink()

    return SimpleNamespace(home=home, bin=bin_dir, cwd=cwd, env=env, fake=fake,
                           full=full, run=run, calls=calls, reset_logs=reset_logs)


def write_file(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def json_checks(result, code=0):
    assert result.returncode == code, result.stderr
    assert "Traceback" not in result.stderr
    return json.loads(result.stdout)["checks"]


def markdown_checks(text):
    checks = []
    group = None
    for line in text.splitlines():
        if line.startswith("## "):
            group = line[3:]
        elif line.startswith("| ") and not line.startswith("| Item |"):
            cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
            assert len(cells) == 4, line
            checks.append(dict(zip(("group", "item", "status", "detail", "proof"),
                                   [group, *cells])))
    return checks


def row(checks, item, group=None):
    matches = [c for c in checks if c["item"] == item and (group is None or c["group"] == group)]
    assert len(matches) == 1, matches
    return matches[0]


def assert_row(checks, item, status, detail, proof, group=None):
    actual = row(checks, item, group)
    assert (actual["status"], actual["detail"], actual["proof"]) == (status, detail, str(proof))


def test_rt_01_sanitized_full_inventory(sandbox):
    sandbox.full()
    before = date.today().isoformat()
    result = sandbox.run()
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[0] in {
        f"# Readiness tools check — {day} — {socket.gethostname()}"
        for day in (before, date.today().isoformat())
    }
    output = result.stdout + result.stderr
    assert str(Path.home()) not in output
    assert str(ROOT) not in output
    assert "Traceback" not in result.stderr
    checks = markdown_checks(result.stdout)
    assert len(checks) == 26
    for name in BINARIES:
        assert_row(checks, name, "verified", f"{name}-fake 0.1", f"`{name} --version`", "Tools")
        assert sandbox.calls(name) == [["--version"]]
    for item, path in [("qwen config (model, provider)", sandbox.home / ".qwen/settings.json"),
                       ("codex model cache", sandbox.home / ".codex/models_cache.json")]:
        assert_row(checks, item, "unknown", f"no {path}", path)
    directories = {
        "claude skills (user)": sandbox.home / ".claude/skills",
        "agents skills (cross-tool)": sandbox.home / ".agents/skills",
        "codex skills (user)": sandbox.home / ".codex/skills",
        "qwen skills (user)": sandbox.home / ".qwen/skills",
        "project skills": sandbox.cwd / ".claude/skills",
        "workflow scripts": sandbox.cwd / ".claude/workflows",
    }
    for item, path in directories.items():
        assert_row(checks, item, "verified", f"absent ({path})", path)
    mcp = [c for c in checks if c["group"] == "MCP"]
    assert {c["item"] for c in mcp} == MCP_LABELS
    assert all(c["status"] == "verified" and c["detail"] == "file absent → no servers from it" for c in mcp)
    assert row(checks, "project instruction files")["detail"] == (
        "present: none; absent: CLAUDE.md, AGENTS.md, QWEN.md, GEMINI.md")
    unknowns = [c for c in checks if c["group"] == "Open unknowns"]
    assert len(unknowns) == 2 and all(c["status"] == "unknown" for c in unknowns)


def test_rt_02_broken_qwen_json_keeps_inventory(sandbox):
    path = write_file(sandbox.home / ".qwen/settings.json", '{ "model": {')
    checks = json_checks(sandbox.run("--json"))
    assert len(checks) == 26
    unreadable = [c for c in checks if "unreadable" in c["detail"]]
    assert {(c["group"], c["item"]) for c in unreadable} == {
        ("Models and logins", "qwen config (model, provider)"), ("MCP", "~/.qwen/settings.json")}
    assert all(c["status"] == "unknown" and c["detail"].startswith("unreadable:")
               and c["proof"] == str(path) for c in unreadable)
    assert {c["item"] for c in checks if c["group"] == "MCP"} == MCP_LABELS
    assert len([c for c in checks if c["group"] == "Open unknowns"]) == 2
    assert all(c["status"] == "MISSING" for c in checks if c["group"] == "Tools")


def test_rt_03a_truncated_and_unreadable_cache(sandbox):
    cache = write_file(sandbox.home / ".codex/models_cache.json", '{"models": [{"id": "x"},')
    cache.chmod(0o644)
    checks = json_checks(sandbox.run("--json"))
    assert len(checks) == 26
    check = row(checks, "codex model cache")
    assert check["status"] == "unknown" and check["proof"] == str(cache)
    assert check["detail"].startswith("unreadable:") and "Expecting" in check["detail"]
    # Root can read mode 0000; exercise permission denial only when it is enforceable.
    if os.geteuid() != 0:
        cache.chmod(0o000)
        try:
            checks = json_checks(sandbox.run("--json"))
            assert len(checks) == 26
            check = row(checks, "codex model cache")
            assert check["status"] == "unknown" and check["proof"] == str(cache)
            assert check["detail"].startswith("unreadable:") and "Permission denied" in check["detail"]
        finally:
            cache.chmod(0o644)


def test_rt_03b_non_object_codex_cache(sandbox):
    cache = write_file(sandbox.home / ".codex/models_cache.json", '[{"id": "gpt-6"}]')
    checks = json_checks(sandbox.run("--json"))
    assert len(checks) == 26
    check = row(checks, "codex model cache")
    assert check["status"] == "unknown" and check["proof"] == str(cache)
    assert check["detail"].startswith("unreadable:")


def test_rt_03c_non_object_qwen_settings(sandbox):
    settings = write_file(sandbox.home / ".qwen/settings.json", '[{"id": "gpt-6"}]')
    checks = json_checks(sandbox.run("--json"))
    assert len(checks) == 26
    check = row(checks, "qwen config (model, provider)")
    assert check["status"] == "unknown" and check["proof"] == str(settings)
    assert check["detail"].startswith("unreadable:")


def test_rt_04_cache_fallbacks_cap_and_age(sandbox):
    sandbox.full()
    examples = [
        ({"models": [{"id": "a"}, {"slug": "b"}, {"name": "c"}, {"note": 1}, "raw"],
          "fetched_at": time.time() - 10 * 86400},
         "5 model ids, cache 10d old: a, b, c, ?, raw (cache may be stale)"),
        ({"models": [{"id": f"m{i}"} for i in range(1, 10)]},
         "9 model ids: m1, m2, m3, m4, m5, m6 … (cache may be stale)"),
        ({"models": {"x": {"o": 1}, "y": {}}, "fetched_at": "2026-09-01T00:00:00Z"},
         "2 model ids, fetched_at 2026-09-01: x, y (cache may be stale)"),
    ]
    for data, detail in examples:
        path = write_file(sandbox.home / ".codex/models_cache.json", json.dumps(data))
        assert_row(json_checks(sandbox.run("--json")), "codex model cache", "reported", detail, path)


def test_rt_05_qwen_secrets_never_printed(sandbox):
    sandbox.full()
    secrets = [f"sk-SENTINEL-{uuid.uuid4().hex}" for _ in range(3)]
    path = write_file(sandbox.home / ".qwen/settings.json", json.dumps({
        "env": {"AG_TEST_KEY": secrets[0], "EMPTY": ""}, "apiKey": secrets[1],
        "security": {"auth": {"selectedType": "test-oauth-type"}},
        "model": {"name": "sentinel-model", "baseUrl": f"https://sentinel-host.invalid/v1?token={secrets[2]}"},
    }))
    for args in [(), ("--json",)]:
        result = sandbox.run(*args)
        assert result.returncode == 0, result.stderr
        assert all(secret not in result.stdout + result.stderr for secret in secrets)
        checks = json_checks(result) if args else markdown_checks(result.stdout)
        assert_row(checks, "qwen config (model, provider)", "reported",
                   "default sentinel-model, auth test-oauth-type, 0 listed models, endpoint sentinel-host.invalid, "
                   "key set in settings env (file claim; key validity not tested)", path)


def test_rt_06_require_matrix_and_dedupe(sandbox):
    for name in ("git", "python3"):
        sandbox.fake(name)
    for args, code in [(('--require', 'git'), 0), (('--require', 'nope'), 1),
                       (('--require', 'git', '--require', 'nope'), 1),
                       ((), 0), (('--require', 'git', '--require', 'git', '--json'), 0)]:
        result = sandbox.run(*args)
        assert result.returncode == code, result.stderr
        checks = json_checks(result, code) if "--json" in args else markdown_checks(result.stdout)
        assert_row(checks, "git", "verified", "git-fake 0.1", "`git --version`", "Tools")
        if "nope" in args:
            assert_row(checks, "nope", "MISSING", "not on PATH", "`command -v nope`", "Tools")
        tools = [c for c in checks if c["group"] == "Tools"]
        assert len(tools) == (8 if "nope" in args else 7)
        assert len([c for c in tools if c["item"] == "git"]) == 1
        if not args:
            assert all(row(checks, n, "Tools")["status"] == "MISSING"
                       for n in ("claude", "codex", "agy", "qwen", "node"))


def test_rt_07_WART_require_accepts_present_broken_tool(sandbox):
    sandbox.fake("broken", "print('boom on stderr\\nsecond line', file=sys.stderr)\nsys.exit(3)\n")
    checks = json_checks(sandbox.run("--require", "broken", "--json"))
    assert_row(checks, "broken", "unknown", "exit 3: boom on stderr", "`broken --version`", "Tools")


def test_rt_08_json_contract_and_markdown_row_sets(sandbox):
    sandbox.full()
    before = date.today().isoformat()
    result = sandbox.run("--json")
    checks = json_checks(result)
    data = json.loads(result.stdout)
    assert set(data) == {"date", "host", "checks"}
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["date"])
    assert data["date"] in {before, date.today().isoformat()}
    assert data["host"] == socket.gethostname()
    assert isinstance(checks, list) and checks
    for check in checks:
        assert set(check) == {"group", "item", "status", "detail", "proof"}
        assert check["status"] in {"verified", "reported", "unknown", "MISSING"}
        assert check["group"] in GROUPS
    indices = [GROUPS.index(c["group"]) for c in checks]
    assert indices == sorted(indices)
    assert len({c["item"] for c in checks if c["group"] == "Tools"}) == 7
    assert len([c for c in checks if c["group"] == "MCP"]) == 4
    unknowns = [c for c in checks if c["group"] == "Open unknowns"]
    assert len(unknowns) == 2 and all(c["status"] == "unknown" for c in unknowns)
    plain = sandbox.run()
    assert plain.returncode == 0, plain.stderr
    markdown = markdown_checks(plain.stdout)
    assert len(markdown) == len(checks)
    # Free RAM can change between processes; all stable rows must agree in both modes.
    assert [c for c in markdown if c["group"] != "Machine"] == [c for c in checks if c["group"] != "Machine"]
    assert {(c["group"], c["item"]) for c in markdown} == {(c["group"], c["item"]) for c in checks}


def test_rt_09_markdown_groups_escaping_and_truncation(sandbox):
    sandbox.full()
    sandbox.fake("claude", "print('1.0 | beta')\n")
    sandbox.fake("codex", "print('X' * 300)\n")
    before = date.today().isoformat()
    plain = sandbox.run()
    assert plain.returncode == 0, plain.stderr
    lines = plain.stdout.splitlines()
    assert lines[0] in {f"# Readiness tools check — {d} — {socket.gethostname()}"
                        for d in (before, date.today().isoformat())}
    assert lines[1:4] == ["", "Installed and logged in only; no canary was run, no quota spent.", ""]
    assert [line for line in lines if line.startswith("## ")] == [f"## {g}" for g in GROUPS]
    for group in GROUPS:
        start = lines.index(f"## {group}")
        assert lines[start + 1:start + 4] == ["", "| Item | Status | Detail | Proof |", "|---|---|---|---|"]
    assert lines.count("| Item | Status | Detail | Proof |") == len(GROUPS)
    assert lines.count("|---|---|---|---|") == len(GROUPS)
    markdown = markdown_checks(plain.stdout)
    checks = json_checks(sandbox.run("--json"))
    assert row(markdown, "claude", "Tools")["detail"] == r"1.0 \| beta"
    assert row(checks, "claude", "Tools")["detail"] == "1.0 | beta"
    assert row(markdown, "codex", "Tools")["detail"] == "X" * 100
    assert row(checks, "codex", "Tools")["detail"] == "X" * 100
    assert len(markdown) == len(checks)


def test_rt_10_hanging_binary_is_bounded(sandbox):
    # A Python sleeper needs no real sleep binary and is killed directly, without a shell child.
    pid_file = sandbox.bin.parent / "hanging.pid"
    sandbox.fake("claude", f"with open({str(pid_file)!r}, 'w') as pid_file:\n"
                 "    pid_file.write(str(os.getpid()))\nimport time\ntime.sleep(60)\n")
    start = time.monotonic()
    result = sandbox.run("--require", "claude", "--json", timeout=35)
    elapsed = time.monotonic() - start
    pid = int(pid_file.read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    assert 10 <= elapsed < 25
    checks = json_checks(result)
    assert len(checks) == 26
    assert_row(checks, "claude", "unknown", "no answer within 10s", "`claude --version`", "Tools")
    assert all(row(checks, name, "Tools")["status"] == "MISSING" for name in BINARIES[1:])


def test_rt_11_qwen_quota_tripwire(sandbox):
    sandbox.fake("qwen", "if sys.argv[1:] != ['--version']:\n"
                 "    print('UNEXPECTED qwen INVOCATION: ' + ' '.join(sys.argv[1:]))\n"
                 "    sys.exit(9)\nprint('qwen-fake 0.0')\n")
    for args in [(), ("--json",), ("--require", "qwen"), ("--self-test",)]:
        sandbox.reset_logs()
        result = sandbox.run(*args)
        assert result.returncode == 0, result.stderr
        assert "UNEXPECTED" not in result.stdout + result.stderr
        assert "exit 9" not in result.stdout + result.stderr
        assert sandbox.calls("qwen") == ([] if "--self-test" in args else [["--version"]])
        if "--self-test" not in args:
            checks = json_checks(result) if "--json" in args else markdown_checks(result.stdout)
            assert_row(checks, "qwen", "verified", "qwen-fake 0.0", "`qwen --version`", "Tools")


def test_rt_12_net_opt_in_and_agy_banner_parsing(sandbox):
    sandbox.fake("agy", "if sys.argv[1:] == ['--version']:\n"
                 "    print('agy-fake 1.2.14')\n"
                 "elif sys.argv[1:] == ['models']:\n"
                 "    print('Fetching models…\\ngemini-9-pro\\n gemini-9-flash\\n\\n   \\ngpt-oss-120b-medium')\n"
                 "else:\n    print('UNEXPECTED agy INVOCATION')\n    sys.exit(9)\n")
    offline = json_checks(sandbox.run("--json"))
    assert sandbox.calls("agy") == [["--version"]]
    assert_row(offline, "agy", "verified", "agy-fake 1.2.14", "`agy --version`", "Tools")
    assert_row(offline, "agy login (model list)", "unknown",
               "offline run: not provable without `agy models`; rerun with --net", "`agy models` (network)")
    sandbox.reset_logs()
    online = json_checks(sandbox.run("--json", "--net"))
    assert sandbox.calls("agy") == [["--version"], ["models"]]
    assert_row(online, "agy login (model list)", "verified",
               "3 models: gemini-9-pro, gemini-9-flash, gpt-oss-120b-medium …", "`agy models` (network)")


def test_rt_13_blueprint_workflows_and_usage_errors(sandbox):
    bp, wf, nope = (sandbox.cwd / name for name in ("bp", "wf", "nope"))
    for name in ("README.md", "a.md", "b.md", "notes.txt"):
        write_file(bp / name, "")
    for name in ("a.js", "b.js", "tool.py", ".hidden.js"):
        write_file(wf / name, "")
    result = sandbox.run("--blueprint", bp)
    assert result.returncode == 0, result.stderr
    assert_row(markdown_checks(result.stdout), f"blueprint ({bp})", "verified",
               "3 sections, map present: README.md, a.md, b.md", bp)
    checks = json_checks(sandbox.run("--blueprint", nope, "--json"), code=1)
    assert_row(checks, f"blueprint ({nope})", "MISSING", "directory not found", nope)
    result = sandbox.run("--workflows", wf)
    assert result.returncode == 0, result.stderr
    assert_row(markdown_checks(result.stdout), "workflow scripts", "verified", "2: a.js, b.js", wf)
    for args in [("--nope",), ("--blueprint",), ("--require", "a", "b")]:
        result = sandbox.run(*args)
        assert result.returncode == 2
        assert "usage:" in result.stderr and "error:" in result.stderr
        assert result.stdout == ""


def test_rt_14_self_test_pass_fail_and_json_precedence(sandbox):
    sandbox.full()
    expected = ("self-test PASS: `readiness-selftest-fake-tool` reported MISSING and --require on it exits 1 "
                "— the check can fail.\n")
    for args in [("--self-test",), ("--self-test", "--json")]:
        result = sandbox.run(*args)
        assert result.returncode == 0 and result.stdout == expected
        assert result.stderr == ""
        assert all(sandbox.calls(name) == [] for name in BINARIES)
        assert "#" not in result.stdout and "| Item | Status" not in result.stdout
        with pytest.raises(json.JSONDecodeError):
            json.loads(result.stdout)
    sandbox.fake("readiness-selftest-fake-tool", "print('fake 1.0')\n")
    result = sandbox.run("--self-test")
    assert result.returncode == 1
    assert result.stdout == "self-test FAIL: status=verified, exit code=0 (expected MISSING, 1)\n"
    assert result.stderr == ""
    assert sandbox.calls("readiness-selftest-fake-tool") == [["--version"]]
    assert all(sandbox.calls(name) == [] for name in BINARIES)



def test_rt_15_blueprint_without_map(sandbox):
    bp = sandbox.cwd / "bp"
    for name in ("b.md", "a.md", "notes.txt"):
        write_file(bp / name, "")
    checks = json_checks(sandbox.run("--blueprint", bp, "--json"))
    assert_row(checks, f"blueprint ({bp})", "verified",
               "2 sections, map MISSING: a.md, b.md", bp, "Skills and workflows")


def test_rt_16_empty_skill_directory(sandbox):
    skills = sandbox.home / ".claude/skills"
    skills.mkdir(parents=True)
    assert_row(json_checks(sandbox.run("--json")), "claude skills (user)", "verified",
               f"empty ({skills})", skills, "Skills and workflows")


def test_rt_17_skill_symlink_and_listing_cap(sandbox):
    skills = sandbox.home / ".claude/skills"
    skills.mkdir(parents=True)
    (skills / "a-link").symlink_to("../target")
    (skills.parent / "target").mkdir()
    for i in range(1, 8):
        (skills / f"skill-{i}").mkdir()
    detail = "8: a-link → ../target, " + ", ".join(f"skill-{i}" for i in range(1, 8))
    assert_row(json_checks(sandbox.run("--json")), "claude skills (user)", "verified",
               detail, skills, "Skills and workflows")
    (skills / "skill-8").mkdir()
    assert_row(json_checks(sandbox.run("--json")), "claude skills (user)", "verified",
               "9:" + detail[2:] + " …", skills, "Skills and workflows")


def test_rt_18_mcp_servers_and_empty_object(sandbox):
    sources = [
        ("~/.claude/settings.json", sandbox.home / ".claude/settings.json"),
        ("~/.claude.json", sandbox.home / ".claude.json"),
        ("~/.qwen/settings.json", sandbox.home / ".qwen/settings.json"),
        (".mcp.json (project)", sandbox.cwd / ".mcp.json"),
    ]
    for data, detail in [({"mcpServers": {"alpha": {}, "beta": {}}}, "2 servers: alpha, beta"),
                         ({}, "no mcpServers key"),
                         ({"mcpServers": {}}, "mcpServers present but empty")]:
        for _, path in sources:
            write_file(path, json.dumps(data))
        checks = json_checks(sandbox.run("--json"))
        assert {c["item"] for c in checks if c["group"] == "MCP"} == MCP_LABELS
        for label, path in sources:
            assert_row(checks, label, "verified", detail, path, "MCP")


def test_rt_19_populated_memory_and_history(sandbox):
    memories = sandbox.home / ".qwen/memories"
    write_file(memories / "MEMORY.md", "first\n\nthird\nlast")
    projects = sandbox.home / ".claude/projects"
    for name in ("project-a", "project-b"):
        (projects / name).mkdir(parents=True)
    write_file(projects / "notes.txt", "not a project directory")
    checks = json_checks(sandbox.run("--json"))
    assert_row(checks, "qwen auto-memory (user)", "verified",
               "4 index lines in MEMORY.md; project dirs under ~/.qwen/projects/", memories, "Memory")
    assert_row(checks, "claude session history", "verified", "2 project histories", projects, "Memory")


def test_rt_20_present_instruction_files(sandbox):
    for name in ("CLAUDE.md", "QWEN.md"):
        write_file(sandbox.cwd / name, "instructions")
    assert_row(json_checks(sandbox.run("--json")), "project instruction files", "verified",
               "present: CLAUDE.md, QWEN.md; absent: AGENTS.md, GEMINI.md", sandbox.cwd, "Memory")
    for name in ("AGENTS.md", "GEMINI.md"):
        write_file(sandbox.cwd / name, "instructions")
    assert_row(json_checks(sandbox.run("--json")), "project instruction files", "verified",
               "present: CLAUDE.md, AGENTS.md, QWEN.md, GEMINI.md", sandbox.cwd, "Memory")


def test_rt_21_net_agy_absent_and_nonzero(sandbox):
    checks = json_checks(sandbox.run("--json", "--net"))
    assert_row(checks, "agy login (model list)", "MISSING", "agy not on PATH",
               "`agy --version`", "Models and logins")
    assert sandbox.calls("agy") == []
    sandbox.fake("agy", "if sys.argv[1:] == ['--version']:\n"
                 "    print('agy-fake 0.1')\n"
                 "elif sys.argv[1:] == ['models']:\n"
                 "    print('login failed\\nsecond line', file=sys.stderr)\n"
                 "    sys.exit(3)\n"
                 "else:\n    sys.exit(9)\n")
    checks = json_checks(sandbox.run("--json", "--net"))
    assert sandbox.calls("agy") == [["--version"], ["models"]]
    assert_row(checks, "agy", "verified", "agy-fake 0.1", "`agy --version`", "Tools")
    assert_row(checks, "agy login (model list)", "unknown", "exit 3: login failed",
               "`agy models` (network)", "Models and logins")


def test_rt_22_unreadable_dirs_report_unknown(sandbox):
    # Found by the agy re-review: an unreadable skills or history dir crashed the inventory.
    if os.geteuid() == 0:
        pytest.skip("root can read mode 0000 directories")
    skills = sandbox.home / ".claude/skills"
    projects = sandbox.home / ".claude/projects"
    skills.mkdir(parents=True)
    projects.mkdir(parents=True)
    skills.chmod(0o000)
    projects.chmod(0o000)
    try:
        checks = json_checks(sandbox.run("--json"))
        for item, path in (("claude skills (user)", skills), ("claude session history", projects)):
            check = row(checks, item)
            assert check["status"] == "unknown" and check["proof"] == str(path)
            assert check["detail"].startswith("unreadable:") and "Permission denied" in check["detail"]
    finally:
        skills.chmod(0o755)
        projects.chmod(0o755)
