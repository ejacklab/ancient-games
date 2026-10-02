#!/usr/bin/env python3
"""readiness.py — the standard tool inventory for method 3.1 (readiness).

Proves what is installed and logged in on this machine. It never spends quota:
no canary is run, so "executes a task" stays unknown here and remains an
explicit, separately approved step (docs/EXECUTOR_KINDS.md in the Ancient Games
repo). Every line carries a status and the command or path that proved it:

  verified  a command run just now proved it
  reported  a local file claims it (may be stale)
  unknown   not provable on this machine
  MISSING   expected and not there

Generic by design (the skill is global): nothing hardcodes a project. Project
extras come in through flags (--blueprint, --workflows).

Usage:
  readiness.py [--net] [--json] [--require TOOL ...] [--blueprint DIR]
               [--workflows DIR] [--self-test]

Exit codes: 0 ok · 1 a --require'd tool or an explicit --blueprint dir is MISSING · 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path

CMD_TIMEOUT = 10   # seconds per local command
NET_TIMEOUT = 30   # seconds for --net commands (agy models talks to the network)
DEFAULT_BINARIES = ["claude", "codex", "agy", "qwen", "node", "python3", "git"]

VERIFIED = "verified"
REPORTED = "reported"
UNKNOWN = "unknown"
MISSING = "MISSING"

GROUPS = ["Tools", "Models and logins", "Skills and workflows", "Memory", "MCP",
          "Machine", "Open unknowns"]


@dataclass
class Check:
    group: str
    item: str
    status: str
    detail: str
    proof: str


def run_cmd(cmd: list[str], timeout: int = CMD_TIMEOUT) -> tuple:
    """(returncode, stripped output). rc is None if the binary does not exist,
    'timeout' if it did not answer in time."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=timeout)
    except FileNotFoundError:
        return None, "not on PATH"
    except subprocess.TimeoutExpired:
        return "timeout", f"no answer within {timeout}s"
    except OSError as e:
        return None, str(e)
    return p.returncode, ((p.stdout or "").strip() or (p.stderr or "").strip())


def first_line(out: str) -> str:
    return out.splitlines()[0][:100] if out else "(no output)"


def check_binary(name: str) -> Check:
    rc, out = run_cmd([name, "--version"])
    proof = f"`{name} --version`"
    if rc is None:
        return Check("Tools", name, MISSING, "not on PATH", f"`command -v {name}`")
    if rc == "timeout":
        return Check("Tools", name, UNKNOWN, out, proof)
    if rc == 0:
        return Check("Tools", name, VERIFIED, first_line(out), proof)
    return Check("Tools", name, UNKNOWN, f"exit {rc}: {first_line(out)}", proof)


def check_codex_cache() -> Check:
    item = "codex model cache"
    p = Path.home() / ".codex" / "models_cache.json"
    if not p.exists():
        return Check("Models and logins", item, UNKNOWN, f"no {p}", str(p))
    try:
        d = json.loads(p.read_text())
    except (OSError, ValueError) as e:
        return Check("Models and logins", item, UNKNOWN, f"unreadable: {e}", str(p))
    if not isinstance(d, dict):
        return Check("Models and logins", item, UNKNOWN, "unreadable: top level is not a JSON object", str(p))
    models = d.get("models")
    ids: list[str] = []
    if isinstance(models, list):
        for m in models:
            ids.append(str(m.get("id") or m.get("slug") or m.get("name") or "?")
                       if isinstance(m, dict) else str(m))
    elif isinstance(models, dict):
        ids = list(models)
    age = ""
    f_at = d.get("fetched_at")
    if isinstance(f_at, (int, float)):
        age = f", cache {(datetime.now(timezone.utc).timestamp() - f_at) / 86400:.0f}d old"
    elif isinstance(f_at, str):
        age = f", fetched_at {f_at[:10]}"
    shown = f": {', '.join(ids[:6])}" + (" …" if len(ids) > 6 else "") if ids else ""
    return Check("Models and logins", item, REPORTED,
                 f"{len(ids)} model ids{age}{shown} (cache may be stale)", str(p))


def check_agy_login(net: bool) -> Check:
    item = "agy login (model list)"
    proof = "`agy models` (network)"
    if not net:
        return Check("Models and logins", item, UNKNOWN,
                     "offline run: not provable without `agy models`; rerun with --net", proof)
    rc, out = run_cmd(["agy", "models"], timeout=NET_TIMEOUT)
    if rc is None:
        return Check("Models and logins", item, MISSING, "agy not on PATH", "`agy --version`")
    if rc == "timeout":
        return Check("Models and logins", item, UNKNOWN, out, proof)
    ids = [l.split()[0] for l in out.splitlines()
           if l.split() and not l.lower().startswith("fetching")]
    if rc == 0 and ids:
        return Check("Models and logins", item, VERIFIED,
                     f"{len(ids)} models: {', '.join(ids[:4])} …", proof)
    return Check("Models and logins", item, UNKNOWN, f"exit {rc}: {first_line(out)}", proof)


def check_qwen_config(home: Path) -> Check:
    """Reads ~/.qwen/settings.json only; never prints a key and never calls `qwen`
    (a bare `qwen <word>` is a one-shot prompt that spends quota)."""
    item = "qwen config (model, provider)"
    p = home / ".qwen" / "settings.json"
    if not p.exists():
        return Check("Models and logins", item, UNKNOWN, f"no {p}", str(p))
    try:
        d = json.loads(p.read_text())
    except (OSError, ValueError) as e:
        return Check("Models and logins", item, UNKNOWN, f"unreadable: {e}", str(p))
    if not isinstance(d, dict):
        return Check("Models and logins", item, UNKNOWN, "unreadable: top level is not a JSON object", str(p))
    model = d.get("model") or {}
    providers = d.get("modelProviders") or {}
    n_models = sum(len(v) for v in providers.values() if isinstance(v, list))
    env = d.get("env") or {}
    key = "key set in settings env" if any(env.values()) else "no key in settings env"
    host = str(model.get("baseUrl", "?")).split("/")[2:3]
    auth = (d.get("security") or {}).get("auth", {}).get("selectedType", "?")
    return Check("Models and logins", item, REPORTED,
                 f"default {model.get('name', '?')}, auth {auth}, {n_models} listed models, "
                 f"endpoint {host[0] if host else '?'}, {key} (file claim; key validity not tested)", str(p))


def list_names(p: Path) -> list[str] | None:
    if not p.is_dir():
        return None
    out = []
    for e in sorted(p.iterdir()):
        if e.name.startswith("."):
            continue
        if e.is_symlink():
            out.append(f"{e.name} → {os.readlink(e)}")
        elif e.is_dir() or e.suffix in (".js", ".mjs", ".md"):
            out.append(e.name)
    return out


def check_dir_listing(group: str, item: str, p: Path, absent_status: str = VERIFIED) -> Check:
    names = list_names(p)
    if names is None:
        return Check(group, item, absent_status, f"absent ({p})", str(p))
    if not names:
        return Check(group, item, absent_status, f"empty ({p})", str(p))
    shown = ", ".join(names[:8]) + (" …" if len(names) > 8 else "")
    return Check(group, item, VERIFIED, f"{len(names)}: {shown}", str(p))


def check_blueprint(p: Path) -> Check:
    item = f"blueprint ({p})"
    if not p.is_dir():
        return Check("Skills and workflows", item, MISSING, "directory not found", str(p))
    files = sorted(e.name for e in p.iterdir() if e.suffix == ".md")
    has_map = "README.md" in files
    return Check("Skills and workflows", item, VERIFIED,
                 f"{len(files)} sections, map {'present' if has_map else 'MISSING'}: {', '.join(files[:8])}",
                 str(p))


def check_instruction_files(cwd: Path) -> Check:
    names = ["CLAUDE.md", "AGENTS.md", "QWEN.md", "GEMINI.md"]
    present = [n for n in names if (cwd / n).exists()]
    absent = [n for n in names if n not in present]
    detail = (f"present: {', '.join(present) or 'none'}"
              + (f"; absent: {', '.join(absent)}" if absent else ""))
    return Check("Memory", "project instruction files", VERIFIED, detail, str(cwd))


def check_qwen_memory(home: Path) -> Check:
    p = home / ".qwen" / "memories"
    idx = p / "MEMORY.md"
    if not p.is_dir():
        return Check("Memory", "qwen auto-memory (user)", VERIFIED, f"absent ({p})", str(p))
    try:
        n = len(idx.read_text(errors="replace").splitlines()) if idx.exists() else 0
    except OSError as e:
        return Check("Memory", "qwen auto-memory (user)", UNKNOWN, f"MEMORY.md unreadable: {e}", str(p))
    return Check("Memory", "qwen auto-memory (user)", VERIFIED,
                 f"{n} index lines in MEMORY.md; project dirs under ~/.qwen/projects/", str(p))


def check_claude_history(home: Path) -> Check:
    p = home / ".claude" / "projects"
    if not p.is_dir():
        return Check("Memory", "claude session history", VERIFIED, f"absent ({p})", str(p))
    n = sum(1 for e in p.iterdir() if e.is_dir())
    return Check("Memory", "claude session history", VERIFIED, f"{n} project histories", str(p))


def check_mcp(home: Path, cwd: Path) -> list[Check]:
    out = []
    sources = [("~/.claude/settings.json", home / ".claude" / "settings.json"),
               ("~/.claude.json", home / ".claude.json"),
               ("~/.qwen/settings.json", home / ".qwen" / "settings.json"),
               (".mcp.json (project)", cwd / ".mcp.json")]
    for label, p in sources:
        if not p.exists():
            out.append(Check("MCP", label, VERIFIED, "file absent → no servers from it", str(p)))
            continue
        try:
            d = json.loads(p.read_text())
        except (OSError, ValueError) as e:
            out.append(Check("MCP", label, UNKNOWN, f"unreadable: {e}", str(p)))
            continue
        servers = d.get("mcpServers") if isinstance(d, dict) else None
        if servers:
            out.append(Check("MCP", label, VERIFIED,
                             f"{len(servers)} servers: {', '.join(list(servers)[:6])}", str(p)))
        else:
            out.append(Check("MCP", label, VERIFIED, "no mcpServers key", str(p)))
    return out


def check_machine(cwd: Path) -> Check:
    cores = os.cpu_count() or "?"
    mem_gib = "?"
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                mem_gib = f"{int(line.split()[1]) / 1048576:.1f} GiB"
                break
    except OSError:
        pass
    du = shutil.disk_usage(cwd)
    return Check("Machine", "this machine", VERIFIED,
                 f"{cores} cores; {mem_gib} RAM available; {du.free / 2**30:.0f} G free on {cwd}",
                 "`os.cpu_count`, `/proc/meminfo`, `shutil.disk_usage`")


def open_unknowns() -> list[Check]:
    return [
        Check("Open unknowns", "subagent concurrency limit", UNKNOWN,
              "runtime policy, not provable from outside. Claude Code docs report 20 concurrent, nesting depth 3 "
              "(v2.1.217+, env overrides; reported, not measured here); codex/agy: no figure",
              "docs/EXECUTOR_KINDS.md, Concurrency row"),
        Check("Open unknowns", "codex/agy/qwen execute a task", UNKNOWN,
              "canary required (spends quota; needs the person's go-ahead)",
              "docs/EXECUTOR_KINDS.md canary piece"),
    ]


def gather(args: argparse.Namespace) -> list[Check]:
    home, cwd = Path.home(), Path.cwd()
    binaries = list(dict.fromkeys(DEFAULT_BINARIES + list(args.require or [])))
    with ThreadPoolExecutor(max_workers=max(1, min(8, len(binaries)))) as ex:
        checks: list[Check] = list(ex.map(check_binary, binaries))
    checks.append(check_codex_cache())
    checks.append(check_agy_login(args.net))
    checks.append(check_qwen_config(home))
    for label, p in [("claude skills (user)", home / ".claude" / "skills"),
                     ("agents skills (cross-tool)", home / ".agents" / "skills"),
                     ("codex skills (user)", home / ".codex" / "skills"),
                     ("qwen skills (user)", home / ".qwen" / "skills"),
                     ("project skills", cwd / ".claude" / "skills")]:
        checks.append(check_dir_listing("Skills and workflows", label, p))
    checks.append(check_dir_listing("Skills and workflows", "workflow scripts",
                                    Path(args.workflows) if args.workflows else cwd / ".claude" / "workflows"))
    if args.blueprint:
        checks.append(check_blueprint(Path(args.blueprint)))
    checks.append(check_instruction_files(cwd))
    checks.append(check_qwen_memory(home))
    checks.append(check_claude_history(home))
    checks.extend(check_mcp(home, cwd))
    checks.append(check_machine(cwd))
    checks.extend(open_unknowns())
    checks.sort(key=lambda c: GROUPS.index(c.group))
    return checks


def exit_code(checks: list[Check], requires: list[str]) -> int:
    missing = {c.item for c in checks if c.status == MISSING}
    known = {c.item for c in checks}
    for r in requires:
        if r in missing or r not in known:
            return 1
    for c in checks:  # an explicitly named --blueprint dir that is not there is a hard fail
        if c.item.startswith("blueprint (") and c.status == MISSING:
            return 1
    return 0


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def to_markdown(checks: list[Check]) -> str:
    lines = [f"# Readiness tools check — {date.today().isoformat()} — {socket.gethostname()}", "",
             "Installed and logged in only; no canary was run, no quota spent.", ""]
    current = None
    for c in checks:
        if c.group != current:
            if current is not None:
                lines.append("")
            current = c.group
            lines += [f"## {current}", "", "| Item | Status | Detail | Proof |", "|---|---|---|---|"]
        lines.append(f"| {cell(c.item)} | {c.status} | {cell(c.detail)} | {cell(c.proof)} |")
    return "\n".join(lines) + "\n"


def self_test() -> int:
    fake = "readiness-selftest-fake-tool"
    c = check_binary(fake)
    code = exit_code([c], [fake])
    if c.status == MISSING and code == 1:
        print(f"self-test PASS: `{fake}` reported MISSING and --require on it exits 1 — the check can fail.")
        return 0
    print(f"self-test FAIL: status={c.status}, exit code={code} (expected MISSING, 1)")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Method 3.1 readiness inventory (no quota spent).")
    ap.add_argument("--net", action="store_true",
                    help="also run network checks (`agy models`); off by default")
    ap.add_argument("--json", action="store_true", help="JSON instead of markdown")
    ap.add_argument("--require", action="append", default=[],
                    help="tool that must be verified present; exit 1 if MISSING (repeatable)")
    ap.add_argument("--blueprint", metavar="DIR", help="a product's blueprint directory to include")
    ap.add_argument("--workflows", metavar="DIR", help="workflow scripts directory (default .claude/workflows)")
    ap.add_argument("--self-test", action="store_true", help="prove the check can fail, then exit")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    checks = gather(args)
    if args.json:
        print(json.dumps({"date": date.today().isoformat(), "host": socket.gethostname(),
                          "checks": [asdict(c) for c in checks]}, indent=1))
    else:
        print(to_markdown(checks), end="")
    return exit_code(checks, args.require)


if __name__ == "__main__":
    sys.exit(main())
