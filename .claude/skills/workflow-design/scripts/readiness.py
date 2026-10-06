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

Exit codes: 0 ok · 1 a --require'd tool that is not verified, or an explicit --blueprint dir that is
MISSING · 2 usage error.
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

# The blueprint's own section files (docs/workflow-templates/blueprint.md); a .md that is not one of these
# is not a section, and a mapless directory is MISSING rather than verified.
SECTION_FILES = {"01-vision.md", "02-requirements.md", "03-domain-model.md", "04-business-logic.md",
                 "05-architecture.md", "06-data-model.md", "07-ui-ux.md", "08-non-functional.md"}


@dataclass
class Probe:
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


def probe_binary(name: str) -> Probe:
    """The version of the binary **on PATH**.

    That is NOT necessarily the binary that will make a call: a provider can bundle its own, older copy of an
    engine, and the two do not accept the same model names (docs/EXECUTOR_KINDS.md, "The bundled-runtime trap").
    This line is the most likely thing in the inventory to be misread as proof for a provider call, so the canary
    records the version of the binary that actually ran.
    """
    rc, out = run_cmd([name, "--version"])
    proof = f"`{name} --version`"
    if rc is None:
        return Probe("Tools", name, MISSING, "not on PATH", f"`command -v {name}`")
    if rc == "timeout":
        return Probe("Tools", name, UNKNOWN, out, proof)
    if rc == 0:
        return Probe("Tools", name, VERIFIED, first_line(out), proof)
    return Probe("Tools", name, UNKNOWN, f"exit {rc}: {first_line(out)}", proof)


def probe_codex_cache() -> Probe:
    item = "codex model cache"
    p = Path.home() / ".codex" / "models_cache.json"
    if not p.exists():
        return Probe("Models and logins", item, UNKNOWN, f"no {p}", str(p))
    try:
        d = json.loads(p.read_text())
    except (OSError, ValueError) as e:
        return Probe("Models and logins", item, UNKNOWN, f"unreadable: {e}", str(p))
    if not isinstance(d, dict):
        return Probe("Models and logins", item, UNKNOWN, "unreadable: top level is not a JSON object", str(p))
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
    return Probe("Models and logins", item, REPORTED,
                 f"{len(ids)} model ids{age}{shown} (cache may be stale)", str(p))


def probe_agy_login(net: bool) -> Probe:
    item = "agy login (model list)"
    proof = "`agy models` (network)"
    if not net:
        return Probe("Models and logins", item, UNKNOWN,
                     "offline run: not provable without `agy models`; rerun with --net", proof)
    rc, out = run_cmd(["agy", "models"], timeout=NET_TIMEOUT)
    if rc is None:
        return Probe("Models and logins", item, MISSING, "agy not on PATH", "`agy --version`")
    if rc == "timeout":
        return Probe("Models and logins", item, UNKNOWN, out, proof)
    ids = [l.split()[0] for l in out.splitlines()
           if l.split() and not l.lower().startswith("fetching")
           and not l.split()[0].endswith(":")]  # a label line ("Fetching…", "error: …") is not a model id
    if rc == 0 and ids:
        return Probe("Models and logins", item, VERIFIED,
                     f"{len(ids)} models: {', '.join(ids[:4])} …", proof)
    return Probe("Models and logins", item, UNKNOWN, f"exit {rc}: {first_line(out)}", proof)


def probe_qwen_config(home: Path) -> Probe:
    """Reads ~/.qwen/settings.json only; never prints a key and never calls `qwen`
    (a bare `qwen <word>` is a one-shot prompt that spends quota)."""
    item = "qwen config (model, provider)"
    p = home / ".qwen" / "settings.json"
    if not p.exists():
        return Probe("Models and logins", item, UNKNOWN, f"no {p}", str(p))
    try:
        d = json.loads(p.read_text())
    except (OSError, ValueError) as e:
        return Probe("Models and logins", item, UNKNOWN, f"unreadable: {e}", str(p))
    if not isinstance(d, dict):
        return Probe("Models and logins", item, UNKNOWN, "unreadable: top level is not a JSON object", str(p))
    for key in ("model", "modelProviders", "env", "security"):
        if d.get(key) is not None and not isinstance(d[key], dict):
            return Probe("Models and logins", item, UNKNOWN,
                         f"unreadable: settings.{key} is not an object", str(p))
    model = d.get("model") or {}
    providers = d.get("modelProviders") or {}
    n_models = sum(len(v) for v in providers.values() if isinstance(v, list))
    env = d.get("env") or {}
    key = "key set in settings env" if any(env.values()) else "no key in settings env"
    host = str(model.get("baseUrl", "?")).split("/")[2:3]
    auth = (d.get("security") or {}).get("auth", {}).get("selectedType", "?")
    return Probe("Models and logins", item, REPORTED,
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


def probe_dir_listing(group: str, item: str, p: Path, absent_status: str = MISSING) -> Probe:
    try:
        names = list_names(p)
    except OSError as e:
        return Probe(group, item, UNKNOWN, f"unreadable: {e}", str(p))
    if names is None:
        return Probe(group, item, absent_status, f"absent ({p})", str(p))
    if not names:
        return Probe(group, item, absent_status, f"empty ({p})", str(p))
    shown = ", ".join(names[:8]) + (" …" if len(names) > 8 else "")
    return Probe(group, item, VERIFIED, f"{len(names)}: {shown}", str(p))


def probe_blueprint(p: Path) -> Probe:
    item = f"blueprint ({p})"
    if not p.is_dir():
        return Probe("Skills and workflows", item, MISSING, "directory not found", str(p))
    sections = sorted(e.name for e in p.iterdir() if e.is_file() and e.name in SECTION_FILES)
    if not (p / "README.md").is_file():
        return Probe("Skills and workflows", item, MISSING,
                     f"map MISSING, {len(sections)} sections: {', '.join(sections) or 'none'}", str(p))
    if not sections:
        return Probe("Skills and workflows", item, MISSING, "map present, 0 sections", str(p))
    return Probe("Skills and workflows", item, VERIFIED,
                 f"{len(sections)} sections, map present: {', '.join(sections)}", str(p))


def probe_instruction_files(cwd: Path) -> Probe:
    names = ["CLAUDE.md", "AGENTS.md", "QWEN.md", "GEMINI.md"]
    present = [n for n in names if (cwd / n).exists()]
    absent = [n for n in names if n not in present]
    detail = (f"present: {', '.join(present) or 'none'}"
              + (f"; absent: {', '.join(absent)}" if absent else ""))
    return Probe("Memory", "project instruction files", VERIFIED, detail, str(cwd))


def probe_qwen_memory(home: Path) -> Probe:
    p = home / ".qwen" / "memories"
    idx = p / "MEMORY.md"
    if not p.is_dir():
        return Probe("Memory", "qwen auto-memory (user)", VERIFIED, f"absent ({p})", str(p))
    try:
        n = len(idx.read_text(errors="replace").splitlines()) if idx.exists() else 0
    except OSError as e:
        return Probe("Memory", "qwen auto-memory (user)", UNKNOWN, f"MEMORY.md unreadable: {e}", str(p))
    return Probe("Memory", "qwen auto-memory (user)", VERIFIED,
                 f"{n} index lines in MEMORY.md; project dirs under ~/.qwen/projects/", str(p))


def probe_claude_history(home: Path) -> Probe:
    p = home / ".claude" / "projects"
    if not p.is_dir():
        return Probe("Memory", "claude session history", VERIFIED, f"absent ({p})", str(p))
    try:
        n = sum(1 for e in p.iterdir() if e.is_dir())
    except OSError as e:
        return Probe("Memory", "claude session history", UNKNOWN, f"unreadable: {e}", str(p))
    return Probe("Memory", "claude session history", VERIFIED, f"{n} project histories", str(p))


def probe_mcp(home: Path, cwd: Path) -> list[Probe]:
    out = []
    sources = [("~/.claude/settings.json", home / ".claude" / "settings.json"),
               ("~/.claude.json", home / ".claude.json"),
               ("~/.qwen/settings.json", home / ".qwen" / "settings.json"),
               (".mcp.json (project)", cwd / ".mcp.json")]
    for label, p in sources:
        if not p.exists():
            out.append(Probe("MCP", label, VERIFIED, "file absent → no servers from it", str(p)))
            continue
        try:
            d = json.loads(p.read_text())
        except (OSError, ValueError) as e:
            out.append(Probe("MCP", label, UNKNOWN, f"unreadable: {e}", str(p)))
            continue
        servers = d.get("mcpServers") if isinstance(d, dict) else None
        if servers:
            out.append(Probe("MCP", label, VERIFIED,
                             f"{len(servers)} servers: {', '.join(list(servers)[:6])}", str(p)))
        else:
            out.append(Probe("MCP", label, VERIFIED,
                             "no mcpServers key" if servers is None else "mcpServers present but empty", str(p)))
    return out


def probe_machine(cwd: Path) -> Probe:
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
    return Probe("Machine", "this machine", VERIFIED,
                 f"{cores} cores; {mem_gib} RAM available; {du.free / 2**30:.0f} G free on {cwd}",
                 "`os.cpu_count`, `/proc/meminfo`, `shutil.disk_usage`")


def open_unknowns() -> list[Probe]:
    return [
        Probe("Open unknowns", "subagent concurrency limit", UNKNOWN,
              "runtime policy, not provable from outside. Claude Code docs report 20 concurrent, nesting depth 3 "
              "(v2.1.217+, env overrides; reported, not measured here); codex/agy: no figure",
              "docs/EXECUTOR_KINDS.md, Concurrency row"),
        Probe("Open unknowns", "codex/agy/qwen execute a task", UNKNOWN,
              "canary required (spends quota; needs the person's go-ahead)",
              "docs/EXECUTOR_KINDS.md canary piece"),
    ]


def gather(args: argparse.Namespace) -> list[Probe]:
    home, cwd = Path.home(), Path.cwd()
    binaries = list(dict.fromkeys(DEFAULT_BINARIES + list(args.require or [])))
    with ThreadPoolExecutor(max_workers=max(1, min(8, len(binaries)))) as ex:
        checks: list[Probe] = list(ex.map(probe_binary, binaries))
    checks.append(probe_codex_cache())
    checks.append(probe_agy_login(args.net))
    checks.append(probe_qwen_config(home))
    for label, p in [("claude skills (user)", home / ".claude" / "skills"),
                     ("agents skills (cross-tool)", home / ".agents" / "skills"),
                     ("codex skills (user)", home / ".codex" / "skills"),
                     ("qwen skills (user)", home / ".qwen" / "skills"),
                     ("project skills", cwd / ".claude" / "skills")]:
        checks.append(probe_dir_listing("Skills and workflows", label, p))
    checks.append(probe_dir_listing("Skills and workflows", "workflow scripts",
                                    Path(args.workflows) if args.workflows else cwd / ".claude" / "workflows"))
    if args.blueprint:
        checks.append(probe_blueprint(Path(args.blueprint)))
    checks.append(probe_instruction_files(cwd))
    checks.append(probe_qwen_memory(home))
    checks.append(probe_claude_history(home))
    checks.extend(probe_mcp(home, cwd))
    checks.append(probe_machine(cwd))
    checks.extend(open_unknowns())
    checks.sort(key=lambda c: GROUPS.index(c.group))
    return checks


def exit_code(checks: list[Probe], requires: list[str]) -> int:
    for r in requires:  # a --require'd tool must be VERIFIED: present-but-unproven is not enough
        if not any(c.item == r and c.status == VERIFIED for c in checks):
            return 1
    for c in checks:  # an explicitly named --blueprint dir that is not there is a hard fail
        if c.item.startswith("blueprint (") and c.status == MISSING:
            return 1
    return 0


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def to_markdown(checks: list[Probe]) -> str:
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
    c = probe_binary(fake)
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
                    help="tool that must be verified present; exit 1 if not verified (repeatable)")
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
