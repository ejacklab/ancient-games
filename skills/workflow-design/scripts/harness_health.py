#!/usr/bin/env python3
"""harness_health.py — harness health for method 3.1 (readiness), beside readiness.py.

readiness.py proves what is installed; this script reads how each installed harness is set up, against ten
requirements for a harness (context, tools, planning, state, verification, guardrails, recovery, human gates,
observability, feedback). It never spends quota, never writes a file, and never prints a config value other than
a recognised mode name or a count — config files hold keys.

Configured is not enforced: a line reads what a config file says; none proves the harness enforces it.

Every line is one finding:
  present   the thing the requirement names is configured
  absent    it is not — and a Help entry says which file, which key, and a snippet the person applies
  measured  a number with no verdict (no threshold is given)
  covered   a per-run requirement the method's own script covers; the line goes MISSING if that script is gone
  unknown   the harness's config format has not been verified, or the file could not be read
Status keeps readiness's meaning: verified (key names proved on the installed version: the harness rejected a bad
value) · reported (key names from another version or the binary's strings) · unknown · MISSING.

Key names, and the version they were checked on (runs/20261015-harness-health/evidence/ in the Ancient Games repo):
  codex   sandbox_mode, approval_policy — verified on codex-cli 0.160.0 (`codex -c 'sandbox_mode="bogus"' login
          status` is rejected; a misspelled key is silently accepted)
  claude  permissions.deny / defaultMode, sandbox.enabled, skipDangerousModePermissionPrompt, hooks — reported from
          the 2.1.299 binary's strings; no quota-free command validates them
  agy, qwen, dsh, opencode — not verified: unknown

Usage: harness_health.py [--harness NAME ...] [--json] [--self-test]
Exit: 0 ok · 1 a --harness named harness is not installed · 2 usage error. Findings never change the exit code.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import sys
import tempfile
import tomllib
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from readiness import MISSING, REPORTED, UNKNOWN, VERIFIED, cell, run_cmd  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
HARNESSES = ["claude", "codex", "agy", "qwen", "dsh", "opencode"]
CODEX_VERIFIED_ON = "0.160.0"
CLAUDE_KEYS_FROM = "2.1.299"
CLAUDE_MODES = {"default", "acceptEdits", "plan", "auto", "bypassPermissions", "dontAsk"}
CODEX_SANDBOX = {"read-only", "workspace-write", "danger-full-access"}
CODEX_APPROVAL = {"untrusted", "on-failure", "on-request", "granular", "never"}

REQUIREMENTS = {1: "Clear context delivery", 2: "Well-designed tools", 3: "Planning and task structure",
                4: "State and memory across sessions", 5: "Independent verification",
                6: "Guardrails and permissions", 7: "Recovery and retries", 8: "Human-in-the-loop gates",
                9: "Observability", 10: "Feedback loop that improves the harness"}
FINDINGS = ["present", "absent", "unknown", "measured", "covered"]


@dataclass
class Help:
    file: str
    changes: str
    snippet: str = ""
    lang: str = ""          # json: merge into the file · toml: a top-level line above the first [table]


@dataclass
class Finding:
    req: int
    harness: str            # "-" when the line is not about one harness
    item: str
    status: str
    finding: str
    detail: str
    proof: str
    help: Help | None = field(default=None)


def shown(p: Path, home: Path, cwd: Path) -> str:
    """A path as the person would type it, never the machine's absolute home or project path."""
    for base, label in ((cwd, "."), (home, "~")):
        try:
            return f"{label}/{p.relative_to(base)}"
        except ValueError:
            pass
    return str(p)


def load_json(p: Path) -> tuple[dict | None, str]:
    """(object, "") or (None, reason). Absent file → ({}, "absent")."""
    if not p.exists():
        return {}, "absent"
    try:
        d = json.loads(p.read_text())
    except (OSError, ValueError) as e:
        return None, f"unreadable: {type(e).__name__}"
    return (d, "") if isinstance(d, dict) else (None, "unreadable: top level is not a JSON object")


# --- per-run requirements: covered by the method's own scripts -------------------------------------------------

COVERED = [(2, "engine adapters with pinned flags", "engines.py"), (2, "dispatcher", "dispatch.py"),
           (3, "design gate", "design_gate.py"), (4, "run state template", "../assets/templates/state.md"),
           (5, "build gate (tests, scope, tamper)", "feature_gate.py"), (7, "timers and bounded repair", "dispatch.py"),
           (9, "run event log", "runlog.py"), (9, "token harvest", "harvest_run.py")]


def covered_lines(scripts: Path) -> list[Finding]:
    out = []
    for req, what, rel in COVERED:
        p = (scripts / rel).resolve()
        name = Path(rel).name
        if p.is_file():
            out.append(Finding(req, "-", what, VERIFIED, "covered", f"per run, by {name}", name))
        else:
            out.append(Finding(req, "-", what, MISSING, "unknown", f"{name} not found beside this script", name))
    return out


# --- requirement 1, 4, 5, 9: files and engines -----------------------------------------------------------------

def context_lines(home: Path, cwd: Path, claude_dir: Path, codex_dir: Path) -> list[Finding]:
    out = []
    project = [cwd / n for n in ("CLAUDE.md", "AGENTS.md", "QWEN.md", "GEMINI.md")]
    for p in project + [claude_dir / "CLAUDE.md", codex_dir / "AGENTS.md"]:
        if p.is_file():
            try:
                text = p.read_text(errors="replace")
            except OSError as e:
                out.append(Finding(1, "-", shown(p, home, cwd), UNKNOWN, "unknown", f"unreadable: {e}", shown(p, home, cwd)))
                continue
            out.append(Finding(1, "-", shown(p, home, cwd), VERIFIED, "measured",
                               f"{len(text.splitlines())} lines, {len(text.encode())} bytes", shown(p, home, cwd)))
    if not any(p.is_file() for p in project):
        out.append(Finding(1, "-", "project instruction file", VERIFIED, "absent",
                           "none of CLAUDE.md, AGENTS.md, QWEN.md, GEMINI.md in the project", "."))
        out[-1].help = Help("./AGENTS.md", "gives every harness one short, durable entry point; the bootstrap skill "
                            "writes one from the project's blueprint")
    return out


def memory_and_log_lines(home: Path, cwd: Path, claude_dir: Path, codex_dir: Path,
                         installed: set[str]) -> list[Finding]:
    out = []
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
    proj = claude_dir / "projects" / slug
    if "claude" in installed:
        mem = proj / "memory"
        n = len(list(mem.glob("*.md"))) if mem.is_dir() else 0
        out.append(Finding(4, "claude", "project memory", REPORTED, "measured",
                           f"{n} memory files" if mem.is_dir() else "no memory folder for this project",
                           shown(mem, home, cwd)))
        n = len(list(proj.glob("*.jsonl"))) if proj.is_dir() else 0
        out.append(Finding(9, "claude", "session transcripts", REPORTED, "measured",
                           f"{n} session logs for this project", shown(proj, home, cwd)))
    if "codex" in installed:
        p = codex_dir / "sessions"
        out.append(Finding(9, "codex", "session rollouts", VERIFIED, "measured",
                           "folder present" if p.is_dir() else "no sessions folder", shown(p, home, cwd)))
    if "dsh" in installed:
        p = home / ".dsh" / "sessions"
        out.append(Finding(9, "dsh", "sessions", VERIFIED, "measured",
                           "folder present" if p.is_dir() else "no sessions folder", shown(p, home, cwd)))
    return out


def engine_kind_line(installed: set[str]) -> Finding:
    kinds = sorted(installed)
    if len(kinds) >= 2:  # two is what "a reviewer that is not the builder" means, not a chosen threshold
        return Finding(5, "-", "engine kinds on PATH", VERIFIED, "present",
                       f"{len(kinds)}: {', '.join(kinds)} (installed, not canary-proved)", "`command -v`")
    f = Finding(5, "-", "engine kinds on PATH", VERIFIED, "absent",
                f"{len(kinds)}: {', '.join(kinds) or 'none'} — a builder's work cannot get a different-kind reviewer",
                "`command -v`")
    f.help = Help("-", "install and canary-prove a second engine kind (docs: executor-kinds), or plan every "
                       "building node's review as a script check")
    return f


# --- Claude Code -----------------------------------------------------------------------------------------------

def claude_lines(home: Path, cwd: Path, claude_dir: Path) -> list[Finding]:
    scopes = [("user", claude_dir / "settings.json"), ("project", cwd / ".claude" / "settings.json"),
              ("local", cwd / ".claude" / "settings.local.json")]
    rc, out = run_cmd(["claude", "--version"])
    version = out.split()[0] if rc == 0 and out else "?"
    basis = f"key names from the {CLAUDE_KEYS_FROM} binary; installed {version}"
    proof = ", ".join(shown(p, home, cwd) for _, p in scopes)
    loaded = []
    for scope, p in scopes:
        d, why = load_json(p)
        if d is None:
            return [Finding(6, "claude", "settings", UNKNOWN, "unknown", f"{shown(p, home, cwd)} {why}",
                            shown(p, home, cwd))]
        loaded.append((scope, p, d))

    def perms(d):
        v = d.get("permissions")
        return v if isinstance(v, dict) else {}

    lines = []
    # R6 deny rules: they add up across scopes
    deny = [(s, len(perms(d)["deny"])) for s, _, d in loaded
            if isinstance(perms(d).get("deny"), list) and perms(d)["deny"]]
    if deny:
        lines.append(Finding(6, "claude", "deny rules", REPORTED, "present",
                             f"{', '.join(f'{n} in {s}' for s, n in deny)}; {basis}", proof))
    else:
        f = Finding(6, "claude", "deny rules", REPORTED, "absent", f"no permissions.deny in any scope; {basis}", proof)
        f.help = Help(shown(scopes[1][1], home, cwd),
                      "blocks the listed tools/paths outright, whatever is allowed elsewhere. The two rules are "
                      "examples from Claude Code's settings docs — replace them with what this project must never "
                      "touch", json.dumps({"permissions": {"deny": ["Read(./.env)", "Read(./secrets/**)"]}}, indent=2),
                      "json")
        lines.append(f)

    def effective(key_path):
        """(value, scope, path) from the most specific scope that sets it: local > project > user."""
        for scope, p, d in reversed(loaded):
            v = d
            for k in key_path:
                v = v.get(k) if isinstance(v, dict) else None
            if v is not None:
                return v, scope, p
        return None, None, None

    # R6 sandbox
    v, scope, p = effective(("sandbox", "enabled"))
    if v is True:
        lines.append(Finding(6, "claude", "sandbox", REPORTED, "present", f"sandbox.enabled true ({scope}); {basis}", proof))
    else:
        f = Finding(6, "claude", "sandbox", REPORTED, "absent",
                    f"sandbox.enabled {'false (' + scope + ')' if v is False else 'not set'}; {basis}", proof)
        f.help = Help(shown(p or scopes[1][1], home, cwd), "runs Bash commands inside Claude Code's OS sandbox "
                      "(filesystem and network limits)", json.dumps({"sandbox": {"enabled": True}}, indent=2), "json")
        lines.append(f)

    # R8 permission mode — a human approves unless the mode bypasses it
    v, scope, p = effective(("permissions", "defaultMode"))
    if v == "bypassPermissions":
        f = Finding(8, "claude", "permission mode", REPORTED, "absent",
                    f"defaultMode bypassPermissions ({scope}): no approval prompts; {basis}", proof)
        f.help = Help(shown(p, home, cwd), "brings back approval prompts for actions not allowed by a rule",
                      json.dumps({"permissions": {"defaultMode": "default"}}, indent=2), "json")
        lines.append(f)
    else:
        mode = v if v in CLAUDE_MODES else ("not set (default)" if v is None else "unrecognised value (not shown)")
        lines.append(Finding(8, "claude", "permission mode", REPORTED, "present",
                             f"defaultMode {mode}{f' ({scope})' if scope else ''}; {basis}", proof))

    # R8 the prompt before entering bypass mode
    v, scope, p = effective(("skipDangerousModePermissionPrompt",))
    if v is True:
        f = Finding(8, "claude", "bypass-mode prompt", REPORTED, "absent",
                    f"skipDangerousModePermissionPrompt true ({scope}); {basis}", proof)
        f.help = Help(shown(p, home, cwd), "asks the person before a session enters bypass-permissions mode",
                      json.dumps({"skipDangerousModePermissionPrompt": False}, indent=2), "json")
        lines.append(f)
    else:
        lines.append(Finding(8, "claude", "bypass-mode prompt", REPORTED, "present",
                             f"not skipped; {basis}", proof))

    # R10 hooks: event names add up across scopes
    events = sorted({e for _, _, d in loaded if isinstance(d.get("hooks"), dict)
                     for e, v in d["hooks"].items() if v and re.fullmatch(r"[A-Za-z]+", str(e))})
    if events:
        lines.append(Finding(10, "claude", "hooks", REPORTED, "present", f"events: {', '.join(events)}; {basis}", proof))
    else:
        f = Finding(10, "claude", "hooks", REPORTED, "absent", f"no hooks in any scope; {basis}", proof)
        f.help = Help(shown(scopes[1][1], home, cwd), "a hook is how a recorded mistake becomes a check that "
                      "runs every time (e.g. a UserPromptSubmit or Stop hook); the command is the project's to write")
        lines.append(f)
    return lines


# --- Codex -----------------------------------------------------------------------------------------------------

def codex_lines(home: Path, cwd: Path, codex_dir: Path) -> list[Finding]:
    p = codex_dir / "config.toml"
    rc, out = run_cmd(["codex", "--version"])
    version = out.split()[-1] if rc == 0 and out else "?"
    status = VERIFIED if version == CODEX_VERIFIED_ON else REPORTED
    basis = f"key names verified on {CODEX_VERIFIED_ON}" + ("" if status == VERIFIED else f"; installed {version}")
    where = shown(p, home, cwd)
    if p.exists():
        try:
            d = tomllib.loads(p.read_text())
        except (OSError, tomllib.TOMLDecodeError) as e:
            return [Finding(6, "codex", "config", UNKNOWN, "unknown", f"{where} unreadable: {type(e).__name__}", where)]
    else:
        d = {}
    note = "; profiles and -c flags may override (not read)" if "profiles" in d else ""
    placement = f"a top-level line in {where}, above the first [table] (replace the line if it exists)"
    lines = []
    for req, key, allowed, bad, fix, changes in [
            (6, "sandbox_mode", CODEX_SANDBOX, "danger-full-access", "workspace-write",
             "commands run in Codex's sandbox: writes limited to the workspace"),
            (8, "approval_policy", CODEX_APPROVAL, "never", "on-request",
             "Codex asks the person before commands it may not run on its own")]:
        v = d.get(key)
        if v in allowed and v != bad:
            lines.append(Finding(req, "codex", key, status, "present", f"{v}; {basis}{note}", where))
            continue
        if v is None:
            detail = "not set: Codex's built-in default applies (not checked)"
        elif v == bad:
            detail = f"{v}"
        else:
            detail = "unrecognised value (not shown)"
        f = Finding(req, "codex", key, status, "absent", f"{detail}; {basis}{note}", where)
        f.help = Help(where, f"{changes}. Where: {placement}", f'{key} = "{fix}"', "toml")
        lines.append(f)
    return lines


def unverified_lines(installed: set[str]) -> list[Finding]:
    return [Finding(6, h, "permissions and sandbox", UNKNOWN, "unknown",
                    "config format not verified for this harness; prove key names on the installed version first",
                    "harness_health.py docstring") for h in ("agy", "qwen", "dsh", "opencode") if h in installed]


# --- gather, render ---------------------------------------------------------------------------------------------

def gather(home: Path, cwd: Path, env: dict, scripts: Path = SCRIPTS) -> list[Finding]:
    installed = {h for h in HARNESSES if shutil.which(h, path=env.get("PATH"))}
    claude_dir = Path(env["CLAUDE_CONFIG_DIR"]) if env.get("CLAUDE_CONFIG_DIR") else home / ".claude"
    codex_dir = Path(env["CODEX_HOME"]) if env.get("CODEX_HOME") else home / ".codex"
    lines = [Finding(0, h, "installed", VERIFIED if h in installed else MISSING, "-",
                     "on PATH" if h in installed else "not on PATH", f"`command -v {h}`") for h in HARNESSES]
    lines += context_lines(home, cwd, claude_dir, codex_dir)
    lines += covered_lines(scripts)
    lines += memory_and_log_lines(home, cwd, claude_dir, codex_dir, installed)
    lines.append(engine_kind_line(installed))
    if "claude" in installed:
        lines += claude_lines(home, cwd, claude_dir)
    if "codex" in installed:
        lines += codex_lines(home, cwd, codex_dir)
    lines += unverified_lines(installed)
    return sorted(lines, key=lambda f: f.req)


def select(lines: list[Finding], harnesses: list[str]) -> list[Finding]:
    return [f for f in lines if not harnesses or f.harness in ("-", *harnesses)]


def to_markdown(lines: list[Finding]) -> str:
    out = [f"# Harness health — {date.today().isoformat()} — {socket.gethostname()}", "",
           "Configured is not enforced: each line reads what a config file says; none proves the harness enforces "
           "it. Nothing was changed; no quota spent.", "", "## Ten requirements", "",
           "| # | Requirement | " + " | ".join(FINDINGS) + " |", "|---|---|" + "---|" * len(FINDINGS)]
    for n, name in REQUIREMENTS.items():
        counts = [sum(1 for f in lines if f.req == n and f.finding == k) for k in FINDINGS]
        out.append(f"| R{n} | {name} | " + " | ".join(str(c) for c in counts) + " |")
    out += ["", "## Lines", "", "| # | Harness | Item | Status | Finding | Detail | Proof |",
            "|---|---|---|---|---|---|---|"]
    for f in lines:
        out.append(f"| {'R' + str(f.req) if f.req else '—'} | {f.harness} | {cell(f.item)} | {f.status} | "
                   f"{f.finding} | {cell(f.detail)} | {cell(f.proof)} |")
    helps = [f for f in lines if f.help]
    out += ["", "## Help", ""]
    if not helps:
        out.append("Nothing absent.")
    for f in helps:
        out += [f"### R{f.req} · {f.harness} · {f.item}", "", f"- File: `{f.help.file}`", f"- What it changes: {f.help.changes}"]
        if f.help.snippet:
            out += ["", f"```{f.help.lang}", f.help.snippet, "```"]
        out.append("")
    out.append("You apply any change; this script changed nothing.")
    return "\n".join(out) + "\n"


def self_test() -> int:
    """A settings file with no deny list must come out `absent` — the check can fail."""
    with tempfile.TemporaryDirectory() as td:
        home, cwd = Path(td) / "home", Path(td) / "proj"
        (home / ".claude").mkdir(parents=True)
        cwd.mkdir()
        (home / ".claude" / "settings.json").write_text('{"permissions": {"allow": ["Bash(ls:*)"]}}')
        bad = [f for f in claude_lines(home, cwd, home / ".claude") if f.item == "deny rules"]
        (home / ".claude" / "settings.json").write_text('{"permissions": {"deny": ["Read(./.env)"]}}')
        good = [f for f in claude_lines(home, cwd, home / ".claude") if f.item == "deny rules"]
    if [f.finding for f in bad] == ["absent"] and [f.finding for f in good] == ["present"]:
        print("self-test PASS: no deny list → absent, a deny list → present — the check can fail.")
        return 0
    print(f"self-test FAIL: bad={[f.finding for f in bad]} good={[f.finding for f in good]}")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Harness health for method 3.1 (no quota spent, nothing written).")
    ap.add_argument("--harness", action="append", default=[], choices=HARNESSES,
                    help="narrow the lines and help to this harness (repeatable); exit 1 if it is not installed")
    ap.add_argument("--json", action="store_true", help="JSON instead of markdown")
    ap.add_argument("--self-test", action="store_true", help="prove the check can fail, then exit")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    lines = select(gather(Path.home(), Path.cwd(), dict(os.environ)), args.harness)
    if args.json:
        print(json.dumps({"date": date.today().isoformat(), "host": socket.gethostname(),
                          "findings": [asdict(f) for f in lines]}, indent=1))
    else:
        print(to_markdown(lines), end="")
    missing = [f for f in lines if f.item == "installed" and f.harness in args.harness and f.status == MISSING]
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
