"""HH-01–HH-11: harness health with an isolated HOME and fake executables (run 20261015-harness-health)."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".claude/skills/workflow-design/scripts"
SCRIPT = SCRIPTS / "harness_health.py"
HARNESSES = ["claude", "codex", "agy", "qwen", "dsh", "opencode"]
VERSIONS = {"claude": "2.1.299 (Claude Code)", "codex": "codex-cli 0.160.0"}
SECRET = "SECRET-PLANT-7f3a9c"
ALPHA = "SecretPlantToken"  # passes a letters-only filter, which SECRET does not

sys.path.insert(0, str(SCRIPTS))
import harness_health as hh  # noqa: E402


@pytest.fixture
def box():
    tmp = Path(tempfile.mkdtemp(dir="/tmp"))
    home, bin_dir, cwd = (tmp / n for n in ("home", "bin", "proj"))
    for p in (home, bin_dir, cwd):
        p.mkdir()
    env = {"HOME": str(home), "PATH": str(bin_dir)}

    def fake(name, version=None):
        out = version or VERSIONS.get(name, f"{name}-fake 0.1")
        p = bin_dir / name
        p.write_text(f"#!{sys.executable}\nprint({out!r})\n")
        p.chmod(0o755)

    def full():
        for h in HARNESSES:
            fake(h)

    def run(*args, extra_env=None):
        return subprocess.run([sys.executable, str(SCRIPT), *args], env={**env, **(extra_env or {})}, cwd=cwd,
                              capture_output=True, text=True, timeout=30)

    def findings(*args, extra_env=None):
        r = run("--json", *args, extra_env=extra_env)
        assert r.returncode == 0, r.stderr
        return json.loads(r.stdout)["findings"]

    yield SimpleNamespace(home=home, cwd=cwd, bin=bin_dir, env=env, fake=fake, full=full, run=run,
                          findings=findings)
    shutil.rmtree(tmp, ignore_errors=True)


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def one(findings, harness, item):
    m = [f for f in findings if f["harness"] == harness and f["item"] == item]
    assert len(m) == 1, m
    return m[0]


def claude_settings(box, obj, scope="user"):
    path = {"user": box.home / ".claude/settings.json", "project": box.cwd / ".claude/settings.json",
            "local": box.cwd / ".claude/settings.local.json"}[scope]
    return write(path, json.dumps(obj))


def tree_hash(*roots: Path) -> dict:
    return {str(p): (p.stat().st_mode, hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "dir")
            for r in roots for p in sorted(r.rglob("*"))}


def test_hh_01_ten_rows_and_no_machine_paths(box):
    box.full()
    r = box.run()
    assert r.returncode == 0, r.stderr
    rows = re.findall(r"^\| R(\d+) \| ([^|]+) \|", r.stdout.split("## Lines")[0], re.M)
    assert [int(n) for n, _ in rows] == list(range(1, 11))
    assert "Configured is not enforced" in r.stdout
    assert str(box.home) not in r.stdout and str(box.cwd) not in r.stdout and str(ROOT) not in r.stdout
    f = json.loads(box.run("--json").stdout)["findings"]
    for h in ("agy", "qwen", "dsh", "opencode"):
        assert one(f, h, "permissions and sandbox")["finding"] == "unknown"
    assert one(f, "claude", "deny rules")["finding"] == "absent"
    assert one(f, "codex", "sandbox_mode")["detail"].startswith("not set")


# HH-02: every check that can say absent is shown saying absent (the sabotage) and present.
CASES = [
    ("claude", "deny rules", {"permissions": {"allow": ["Bash(ls:*)"]}}, {"permissions": {"deny": ["Read(./x)"]}}),
    ("claude", "sandbox", {"sandbox": {"enabled": False}}, {"sandbox": {"enabled": True}}),
    ("claude", "permission mode", {"permissions": {"defaultMode": "bypassPermissions"}},
     {"permissions": {"defaultMode": "acceptEdits"}}),
    ("claude", "bypass-mode prompt", {"skipDangerousModePermissionPrompt": True}, {}),
    ("claude", "hooks", {"hooks": {}}, {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "true"}]}]}}),
    ("claude", "deny rules", {"permissions": {"deny": [None, "", 3]}}, {"permissions": {"deny": [None, "Read(./x)"]}}),
    ("claude", "hooks", {"hooks": {"Stop": [{"hooks": []}]}},
     {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "x"}]}]}}),
    ("claude", "hooks", {"disableAllHooks": True, "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "x"}]}]}},
     {"disableAllHooks": False, "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "x"}]}]}}),
    ("claude", "hooks", {"hooks": {"Stop": [{"hooks": [{"type": "bogus", "command": "x"}, {"command": "x"}]}]}},
     {"hooks": {"Stop": [{"hooks": [{"type": "prompt", "prompt": "Check completion"}]}]}}),
    ("claude", "deny rules", {"permissions": {"deny": ["mcp__github__create_issue(foo)"]}},
     {"permissions": {"deny": ["mcp__github__create_issue"]}}),
    ("claude", "permission mode", {"permissions": {"defaultMode": "auto"}}, {"permissions": {"defaultMode": "plan"}}),
    ("claude", "permission mode", {"permissions": {"defaultMode": "dontAsk"}}, {"permissions": {"defaultMode": "default"}}),
]


@pytest.mark.parametrize("harness,item,bad,good", CASES, ids=[f"{c[1]}-{i}" for i, c in enumerate(CASES)])
def test_hh_02_claude_absent_and_present(box, harness, item, bad, good):
    box.full()
    claude_settings(box, bad)
    assert one(box.findings(), harness, item)["finding"] == "absent"
    claude_settings(box, good)
    assert one(box.findings(), harness, item)["finding"] == "present"


@pytest.mark.parametrize("key,bad,good", [("sandbox_mode", "danger-full-access", "read-only"),
                                         ("approval_policy", "never", "on-request")])
def test_hh_02_codex_absent_and_present(box, key, bad, good):
    box.full()
    write(box.home / ".codex/config.toml", f'{key} = "{bad}"\n')
    assert one(box.findings(), "codex", key)["finding"] == "absent"
    write(box.home / ".codex/config.toml", f'{key} = "{good}"\n')
    assert one(box.findings(), "codex", key)["finding"] == "present"


def test_hh_02_engine_kinds_and_instruction_file(box):
    box.fake("claude")
    f = box.findings()
    assert one(f, "-", "engine kinds on PATH")["finding"] == "absent"
    assert one(f, "-", "project instruction file")["finding"] == "absent"
    box.fake("codex")
    write(box.cwd / "AGENTS.md", "# x\n")
    f = box.findings()
    assert one(f, "-", "engine kinds on PATH")["finding"] == "present"
    assert one(f, "-", "project instruction file")["finding"] == "present"
    assert one(f, "-", "./AGENTS.md")["detail"] == "1 lines, 4 bytes"


def test_hh_02_scopes_add_deny_and_local_overrides_mode(box):
    box.full()
    claude_settings(box, {"permissions": {"defaultMode": "bypassPermissions"}}, "user")
    claude_settings(box, {"permissions": {"deny": ["Read(./a)"]}}, "project")
    claude_settings(box, {"permissions": {"defaultMode": "plan"}}, "local")
    f = box.findings()
    assert one(f, "claude", "deny rules")["finding"] == "present"
    mode = one(f, "claude", "permission mode")
    assert mode["finding"] == "present" and "plan (local)" in mode["detail"]


def test_hh_03_planted_secret_never_printed(box):
    box.full()
    for token in (SECRET, ALPHA):
        claude_settings(box, {"env": {"API_KEY": token}, "permissions": {"deny": [f"Read({token})"],
                              "defaultMode": token}, "hooks": {token: [{"hooks": [{"command": token}]}]},
                              "sandbox": {"enabled": token}, "skipDangerousModePermissionPrompt": token})
        write(box.home / ".codex/config.toml",
              f'sandbox_mode = "{token}"\napproval_policy = "{token}"\n[model_providers.x]\napi_key = "{token}"\n')
        for args in ((), ("--json",)):
            r = box.run(*args)
            assert r.returncode == 0, r.stderr
            assert token not in r.stdout + r.stderr, (token, args)


def resolve(box, shown: str) -> Path:
    return (box.cwd / shown[2:]) if shown.startswith("./") else (box.home / shown[2:])


def merge(a: dict, b: dict) -> dict:
    """As JSON_HOW says: keep other keys, add list items to a list that is already there."""
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            a[k] = merge(a[k], v)
        elif isinstance(v, list) and isinstance(a.get(k), list):
            a[k] = a[k] + [x for x in v if x not in a[k]]
        else:
            a[k] = v
    return a


def apply_help(box, help_: dict):
    """Apply a snippet exactly as its help text says: merge JSON into the file; a TOML top-level line above the
    first [table], replacing that key's line if there is one."""
    path = resolve(box, help_["file"])
    if help_["lang"] == "json":
        old = json.loads(path.read_text()) if path.exists() else {}
        write(path, json.dumps(merge(old, json.loads(help_["snippet"]))))
    else:
        key = help_["snippet"].split("=")[0].strip()
        lines = [l for l in (path.read_text().splitlines() if path.exists() else [])
                 if not re.match(rf"\s*{key}\s*=", l)]
        first_table = next((i for i, l in enumerate(lines) if l.lstrip().startswith("[")), len(lines))
        write(path, "\n".join(lines[:first_table] + [help_["snippet"]] + lines[first_table:]) + "\n")


def test_hh_04_every_snippet_flips_its_finding(box):
    box.full()
    claude_settings(box, {"skipDangerousModePermissionPrompt": True, "disableAllHooks": True,
                          "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "x"}]}]},
                          "permissions": {"defaultMode": "bypassPermissions", "deny": [None]}})
    write(box.home / ".codex/config.toml", '[profiles.x]\nmodel = "m"\n')  # a table first: placement matters
    before = [f for f in box.findings() if f["help"] and f["help"]["snippet"]]
    assert {(f["harness"], f["item"]) for f in before} == {
        ("claude", "deny rules"), ("claude", "sandbox"), ("claude", "permission mode"),
        ("claude", "bypass-mode prompt"), ("claude", "hooks"), ("codex", "sandbox_mode"), ("codex", "approval_policy")}
    for f in before:
        assert f["help"]["how"] == (hh.JSON_HOW if f["help"]["lang"] == "json" else
                                    "a top-level line in ~/.codex/config.toml, above the first [table]; "
                                    "replace the line if the key is already set")
        apply_help(box, f["help"])
        assert one(box.findings(), f["harness"], f["item"])["finding"] == "present", f


def test_hh_05_no_file_changes(box):
    box.full()
    claude_settings(box, {"permissions": {"allow": ["Bash(ls:*)"]}})
    write(box.home / ".codex/config.toml", 'sandbox_mode = "never-valid"\n')
    write(box.cwd / "CLAUDE.md", "x\n")
    before = tree_hash(box.home, box.cwd)
    assert box.run().returncode == 0
    assert box.run("--json").returncode == 0
    assert box.run("--self-test").returncode == 0
    assert tree_hash(box.home, box.cwd) == before


def test_hh_06_covered_goes_missing_without_its_script(tmp_path):
    scripts = tmp_path / "scripts"
    (tmp_path / "assets/templates").mkdir(parents=True)
    scripts.mkdir()
    for name in ("engines.py", "dispatch.py", "design_gate.py", "feature_gate.py", "runlog.py", "harvest_run.py"):
        (scripts / name).write_text("")
    (tmp_path / "assets/templates/state.md").write_text("")
    assert all(f.finding == "covered" for f in hh.covered_lines(scripts))
    (scripts / "dispatch.py").unlink()
    gone = [f for f in hh.covered_lines(scripts) if f.finding != "covered"]
    assert {(f.item, f.status) for f in gone} == {("dispatcher", "MISSING"), ("timers and bounded repair", "MISSING")}


def test_hh_07_harness_flag(box):
    box.fake("claude")
    box.fake("codex")
    assert box.run("--harness", "nope").returncode == 2
    assert box.run("--harness", "agy").returncode == 1
    r = box.run("--json", "--harness", "codex")
    assert r.returncode == 0
    harnesses = {f["harness"] for f in json.loads(r.stdout)["findings"]}
    assert harnesses == {"-", "codex"}


def test_hh_08_self_test_and_json_contract(box):
    r = subprocess.run([sys.executable, str(SCRIPT), "--self-test"], capture_output=True, text=True)
    assert r.returncode == 0 and "self-test PASS" in r.stdout
    box.full()
    for f in box.findings():
        assert set(f) == {"req", "harness", "item", "status", "finding", "detail", "proof", "help"}
        assert f["status"] in {"verified", "reported", "unknown", "MISSING"}
        assert f["finding"] in {"present", "absent", "unknown", "measured", "covered", "-"}
        assert (f["help"] is not None) == (f["finding"] == "absent")


def test_hh_09_codex_status_follows_the_verified_version(box):
    box.full()
    assert one(box.findings(), "codex", "sandbox_mode")["status"] == "verified"
    box.fake("codex", "codex-cli 0.170.0")
    f = one(box.findings(), "codex", "sandbox_mode")
    assert f["status"] == "reported" and "installed 0.170.0" in f["detail"]


def test_hh_10_unreadable_config_is_unknown(box):
    box.full()
    write(box.home / ".claude/settings.json", "{not json")
    write(box.home / ".codex/config.toml", "sandbox_mode = \n")
    f = box.findings()
    assert one(f, "claude", "settings")["finding"] == "unknown"
    assert one(f, "codex", "config")["finding"] == "unknown"


def test_hh_11_config_dir_overrides(box):
    box.full()
    alt_claude, alt_codex = box.home / "alt-claude", box.home / "alt-codex"
    write(alt_claude / "settings.json", json.dumps({"permissions": {"deny": ["Read(./x)"]}}))
    write(alt_codex / "config.toml", 'sandbox_mode = "read-only"\n')
    f = box.findings(extra_env={"CLAUDE_CONFIG_DIR": str(alt_claude), "CODEX_HOME": str(alt_codex)})
    assert one(f, "claude", "deny rules")["finding"] == "present"
    assert one(f, "codex", "sandbox_mode")["finding"] == "present"


@pytest.mark.parametrize("settings,toml", [
    ({"permissions": {"defaultMode": []}}, "sandbox_mode = []\n"),
    ({"permissions": {"defaultMode": {}}, "sandbox": []}, "approval_policy = {}\n"),
    ({"permissions": [], "hooks": [], "skipDangerousModePermissionPrompt": {}}, "sandbox_mode = 3\n"),
    ({"hooks": {"Stop": "x"}, "sandbox": {"enabled": []}}, "approval_policy = true\n"),
])
def test_hh_12_odd_shapes_never_crash(box, settings, toml):
    box.full()
    claude_settings(box, settings)
    write(box.home / ".codex/config.toml", toml)
    for args in ((), ("--harness", "codex")):
        r = box.run(*args)
        assert r.returncode == 0 and "Traceback" not in r.stderr, r.stderr
    f = box.findings()
    assert all(x["finding"] in {"absent", "unknown", "present"} for x in f if x["req"] in (6, 8, 10))
    assert one(f, "claude", "permission mode")["finding"] in {"present", "unknown"}


def test_hh_13_non_utf8_codex_config_is_unknown(box):
    box.full()
    p = box.home / ".codex/config.toml"
    p.parent.mkdir(parents=True)
    p.write_bytes(b'sandbox_mode = "read-only"\n\xff\n')
    assert one(box.findings(), "codex", "config")["finding"] == "unknown"


def test_hh_14_no_absolute_path_outside_home(box):
    box.full()
    shared = box.home.parent / "shared-codex"
    write(shared / "config.toml", "sandbox_mode = [\n")
    for args in ((), ("--json",)):
        r = box.run(*args, extra_env={"CODEX_HOME": str(shared)})
        assert r.returncode == 0, r.stderr
        assert str(shared) not in r.stdout and str(box.home) not in r.stdout
    assert "$CODEX_HOME/config.toml" in r.stdout


def test_hh_15_disabled_hooks_with_none_gets_no_disable_snippet(box):
    box.full()
    claude_settings(box, {"disableAllHooks": True})
    f = one(box.findings(), "claude", "hooks")
    assert f["finding"] == "absent" and f["help"]["snippet"] == "" and "disableAllHooks true" in f["detail"]


def test_hh_16_unreadable_folders_are_unknown_not_a_crash(box):
    box.full()
    locked = box.home.parent / "locked"
    write(locked / "settings.json", "{}")
    write(locked / "config.toml", "")
    write(locked / "CLAUDE.md", "x")
    locked.chmod(0)
    try:
        for args in ((), ("--json",), ("--harness", "codex")):
            r = box.run(*args, extra_env={"CLAUDE_CONFIG_DIR": str(locked), "CODEX_HOME": str(locked)})
            assert r.returncode == 0 and "Traceback" not in r.stderr, r.stderr
            assert str(locked) not in r.stdout + r.stderr
            assert "--json" in args or "## Ten requirements" in r.stdout
        f = box.findings(extra_env={"CLAUDE_CONFIG_DIR": str(locked), "CODEX_HOME": str(locked)})
        assert one(f, "claude", "settings")["finding"] == "unknown"
        assert one(f, "codex", "config")["finding"] == "unknown"
    finally:
        locked.chmod(0o755)


def test_hh_17_self_test_writes_nothing(monkeypatch):
    """Every way the script could write is made to raise; the self-test must still pass."""
    import builtins
    import os as os_
    real_open = builtins.open

    def no_write(*a, **k):
        raise AssertionError(f"write attempted: {a[:1]}")

    def guarded_open(file, mode="r", *a, **k):
        if any(c in mode for c in "wax+"):
            no_write(file)
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)
    for name in ("write_text", "write_bytes", "mkdir", "touch"):
        monkeypatch.setattr(Path, name, no_write)
    for name in ("mkdir", "makedirs", "open"):
        monkeypatch.setattr(os_, name, no_write)
    assert hh.self_test() == 0
