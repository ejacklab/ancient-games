#!/usr/bin/env python3
"""harness_health.py — harness health for method 3.1 (readiness), beside readiness.py.

readiness.py proves what is installed; this script reads how each installed harness is set up, against ten
requirements for a harness (context, tools, planning, state, verification, guardrails, recovery, human gates,
observability, feedback). It never spends quota and never prints a config value other than a recognised mode or
event name or a count — config files hold keys. A run only reads; `--self-test` writes two settings files in a
temporary folder and deletes it.

Configured is not enforced: a line reads what a config file says; none proves the harness enforces it.

Every line is one finding:
  present   the thing the requirement names is configured
  absent    it is not — a Help entry names the file and what to change, with a snippet where the fix is a setting
  measured  a number with no verdict (no threshold is given)
  covered   a per-run requirement the method's own script covers; the line goes MISSING if that script is gone
  unknown   the harness's config format has not been verified, the file could not be read, or a value is not one
            the harness accepts
Status keeps readiness's meaning: verified (key names proved on the installed version: the harness rejected a bad
value) · reported (key names from another version or the binary's strings) · unknown · MISSING.

Key names, and the version they were checked on (runs/20261015-harness-health/evidence/ in the Ancient Games repo):
  codex   sandbox_mode, approval_policy — verified on codex-cli 0.160.0 (`codex -c 'sandbox_mode="bogus"' login
          status` is rejected; a misspelled key is silently accepted)
  claude  permissions.deny / defaultMode, sandbox.enabled, skipDangerousModePermissionPrompt, hooks and their event
          names, disableAllHooks — reported from the 2.1.299 binary's strings; no quota-free command validates them
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
CLAUDE_ASKS = {"default", "acceptEdits", "plan"}                 # a person is asked for what no rule allows
CLAUDE_NO_PERSON = {"bypassPermissions": "no approval prompts",
                    "auto": "a classifier, not a person, approves actions",
                    "dontAsk": "actions no rule allows are denied without asking anyone"}
CLAUDE_HOOK_EVENTS = {
    "PreToolUse", "PostToolUse", "PostToolUseFailure", "PostToolBatch", "Notification", "UserPromptSubmit",
    "UserPromptExpansion", "SessionStart", "SessionEnd", "Stop", "StopFailure", "SubagentStart", "SubagentStop",
    "PreCompact", "PostCompact", "PreModelSwitch", "PostModelSwitch", "PermissionRequest", "PermissionDenied",
    "Setup", "TeammateIdle", "TaskCreated", "TaskCompleted", "Elicitation", "ElicitationResult", "ConfigChange",
    "WorktreeCreate", "WorktreeRemove", "InstructionsLoaded", "CwdChanged", "FileChanged", "DirectoryAdded",
    "MessageDisplay"}
CODEX_SANDBOX = {"read-only", "workspace-write", "danger-full-access"}
CODEX_APPROVAL = {"untrusted", "on-failure", "on-request", "granular", "never"}
JSON_HOW = "merge into the file: keep its other keys, and add list items to a list that is already there"

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
    lang: str = ""
    how: str = ""           # how to apply the snippet, printed with it


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


class Where:
    """The machine's folders, and paths shown as the person would type them — never an absolute path."""

    def __init__(self, home: Path, cwd: Path, env: dict):
        self.home, self.cwd = home, cwd
        self.claude = Path(env["CLAUDE_CONFIG_DIR"]) if env.get("CLAUDE_CONFIG_DIR") else home / ".claude"
        self.codex = Path(env["CODEX_HOME"]) if env.get("CODEX_HOME") else home / ".codex"
        self.bases = ([(self.claude, "$CLAUDE_CONFIG_DIR")] if env.get("CLAUDE_CONFIG_DIR") else []) + \
                     ([(self.codex, "$CODEX_HOME")] if env.get("CODEX_HOME") else []) + [(cwd, "."), (home, "~")]

    def show(self, p: Path) -> str:
        for base, label in self.bases:
            try:
                return f"{label}/{p.relative_to(base)}"
            except ValueError:
                pass
        return f"…/{p.name}"


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
    """The script exists — not that the gate it names works; that is the gate's own tests' job."""
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

def context_lines(w: Where) -> list[Finding]:
    out = []
    project = [w.cwd / n for n in ("CLAUDE.md", "AGENTS.md", "QWEN.md", "GEMINI.md")]
    found = [p.name for p in project if p.is_file()]
    if found:
        out.append(Finding(1, "-", "project instruction file", VERIFIED, "present", ", ".join(found), "."))
    else:
        f = Finding(1, "-", "project instruction file", VERIFIED, "absent",
                    "none of CLAUDE.md, AGENTS.md, QWEN.md, GEMINI.md in the project", ".")
        f.help = Help("./AGENTS.md", "gives every harness one short, durable entry point; the bootstrap skill writes "
                      "one from the project's blueprint")
        out.append(f)
    for p in project + [w.claude / "CLAUDE.md", w.codex / "AGENTS.md"]:
        if p.is_file():
            try:
                text = p.read_text(errors="replace")
            except OSError as e:
                out.append(Finding(1, "-", w.show(p), UNKNOWN, "unknown", f"unreadable: {type(e).__name__}", w.show(p)))
                continue
            out.append(Finding(1, "-", w.show(p), VERIFIED, "measured",
                               f"{len(text.splitlines())} lines, {len(text.encode())} bytes", w.show(p)))
    return out


def memory_and_log_lines(w: Where, installed: set[str]) -> list[Finding]:
    out = []
    proj = w.claude / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(w.cwd))
    if "claude" in installed:
        mem = proj / "memory"
        n = len(list(mem.glob("*.md"))) if mem.is_dir() else 0
        out.append(Finding(4, "claude", "project memory", REPORTED, "measured",
                           f"{n} memory files" if mem.is_dir() else "no memory folder for this project", w.show(mem)))
        n = len(list(proj.glob("*.jsonl"))) if proj.is_dir() else 0
        out.append(Finding(9, "claude", "session transcripts", REPORTED, "measured",
                           f"{n} session logs for this project", w.show(proj)))
    if "codex" in installed:
        p = w.codex / "sessions"
        out.append(Finding(9, "codex", "session rollouts", VERIFIED, "measured",
                           "folder present" if p.is_dir() else "no sessions folder", w.show(p)))
    if "dsh" in installed:
        p = w.home / ".dsh" / "sessions"
        out.append(Finding(9, "dsh", "sessions", VERIFIED, "measured",
                           "folder present" if p.is_dir() else "no sessions folder", w.show(p)))
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

def claude_lines(w: Where) -> list[Finding]:
    scopes = [("user", w.claude / "settings.json"), ("project", w.cwd / ".claude" / "settings.json"),
              ("local", w.cwd / ".claude" / "settings.local.json")]
    rc, out = run_cmd(["claude", "--version"])
    version = out.split()[0] if rc == 0 and out else "?"
    basis = f"key names from the {CLAUDE_KEYS_FROM} binary; installed {version}"
    proof = ", ".join(w.show(p) for _, p in scopes)
    project_file = w.show(scopes[1][1])
    loaded = []
    for scope, p in scopes:
        d, why = load_json(p)
        if d is None:
            return [Finding(6, "claude", "settings", UNKNOWN, "unknown", f"{w.show(p)} {why}", w.show(p))]
        loaded.append((scope, p, d))

    def at(d, key_path):
        for k in key_path:
            d = d.get(k) if isinstance(d, dict) else None
        return d

    def effective(key_path):
        """(value, scope, shown path) from the most specific scope that sets it: local > project > user."""
        for scope, p, d in reversed(loaded):
            v = at(d, key_path)
            if v is not None:
                return v, scope, w.show(p)
        return None, None, project_file

    def line(req, item, finding, detail, help_=None):
        return Finding(req, "claude", item, REPORTED, finding, f"{detail}; {basis}", proof, help_)

    lines = []
    # R6 deny rules add up across scopes; only non-empty strings are rules
    deny = []
    for s, _, d in loaded:
        rules = at(d, ("permissions", "deny"))
        n = sum(1 for r in rules if isinstance(r, str) and r.strip()) if isinstance(rules, list) else 0
        if n:
            deny.append((s, n))
    if deny:
        lines.append(line(6, "deny rules", "present", ", ".join(f"{n} in {s}" for s, n in deny)))
    else:
        lines.append(line(6, "deny rules", "absent", "no deny rule in any scope", Help(
            project_file, "blocks the listed tools/paths outright, whatever is allowed elsewhere. The two rules are "
            "examples from Claude Code's settings docs — replace them with what this project must never touch",
            json.dumps({"permissions": {"deny": ["Read(./.env)", "Read(./secrets/**)"]}}, indent=2), "json",
            JSON_HOW)))

    # R6 sandbox
    v, scope, where = effective(("sandbox", "enabled"))
    if v is True:
        lines.append(line(6, "sandbox", "present", f"sandbox.enabled true ({scope})"))
    elif v is None or v is False:
        lines.append(line(6, "sandbox", "absent", f"sandbox.enabled {'false (' + scope + ')' if v is False else 'not set'}",
                          Help(where, "runs Bash commands inside Claude Code's OS sandbox (filesystem and network "
                               "limits)", json.dumps({"sandbox": {"enabled": True}}, indent=2), "json", JSON_HOW)))
    else:
        lines.append(line(6, "sandbox", "unknown", f"sandbox.enabled is not true/false ({scope})"))

    # R8 permission mode — does a person approve what no rule allows?
    v, scope, where = effective(("permissions", "defaultMode"))
    if v is None:
        lines.append(line(8, "permission mode", "present", "defaultMode not set (default: a person is asked)"))
    elif isinstance(v, str) and v in CLAUDE_ASKS:
        lines.append(line(8, "permission mode", "present", f"defaultMode {v} ({scope}): a person is asked"))
    elif isinstance(v, str) and v in CLAUDE_NO_PERSON:
        lines.append(line(8, "permission mode", "absent", f"defaultMode {v} ({scope}): {CLAUDE_NO_PERSON[v]}", Help(
            where, "a person is asked before any action no rule allows",
            json.dumps({"permissions": {"defaultMode": "default"}}, indent=2), "json", JSON_HOW)))
    else:
        lines.append(line(8, "permission mode", "unknown", f"defaultMode not a recognised mode (not shown) ({scope})"))

    # R8 the prompt before entering bypass mode
    v, scope, where = effective(("skipDangerousModePermissionPrompt",))
    if v is True:
        lines.append(line(8, "bypass-mode prompt", "absent", f"skipDangerousModePermissionPrompt true ({scope})", Help(
            where, "asks the person before a session enters bypass-permissions mode",
            json.dumps({"skipDangerousModePermissionPrompt": False}, indent=2), "json", JSON_HOW)))
    elif v is None or v is False:
        lines.append(line(8, "bypass-mode prompt", "present", "not skipped"))
    else:
        lines.append(line(8, "bypass-mode prompt", "unknown", f"skipDangerousModePermissionPrompt not true/false ({scope})"))

    # R10 hooks: an event counts when it holds at least one hook with a command; names shown only if recognised
    def has_command(groups):
        return isinstance(groups, list) and any(
            isinstance(g, dict) and isinstance(g.get("hooks"), list) and any(
                isinstance(h, dict) and isinstance(h.get("command"), str) and h["command"].strip()
                for h in g["hooks"]) for g in groups)

    disabled, scope, where = effective(("disableAllHooks",))
    events = {e for _, _, d in loaded if isinstance(d.get("hooks"), dict)
              for e, groups in d["hooks"].items() if has_command(groups)}
    named = sorted(e for e in events if e in CLAUDE_HOOK_EVENTS)
    others = len(events) - len(named)
    if disabled is True:
        lines.append(line(10, "hooks", "absent", f"disableAllHooks true ({scope}): no hook runs", Help(
            where, "lets the configured hooks run again", json.dumps({"disableAllHooks": False}, indent=2), "json",
            JSON_HOW)))
    elif named:
        lines.append(line(10, "hooks", "present",
                          f"events: {', '.join(named)}" + (f"; {others} unrecognised (not shown)" if others else "")))
    else:
        lines.append(line(10, "hooks", "absent", "no hook with a command for a recognised event" +
                          (f"; {others} unrecognised (not shown)" if others else ""), Help(
            project_file, "a hook is how a recorded mistake becomes a check that runs every time (e.g. a "
            "UserPromptSubmit or Stop hook); the command is the project's to write")))
    return lines


# --- Codex -----------------------------------------------------------------------------------------------------

def codex_lines(w: Where) -> list[Finding]:
    p = w.codex / "config.toml"
    rc, out = run_cmd(["codex", "--version"])
    version = out.split()[-1] if rc == 0 and out else "?"
    status = VERIFIED if version == CODEX_VERIFIED_ON else REPORTED
    basis = f"key names verified on {CODEX_VERIFIED_ON}" + ("" if status == VERIFIED else f"; installed {version}")
    where = w.show(p)
    if p.exists():
        try:
            d = tomllib.loads(p.read_text())
        except (OSError, ValueError) as e:  # TOMLDecodeError and UnicodeDecodeError are ValueErrors
            return [Finding(6, "codex", "config", UNKNOWN, "unknown", f"{where} unreadable: {type(e).__name__}", where)]
    else:
        d = {}
    note = "; profiles and -c flags may override (not read)" if "profiles" in d else ""
    how = f"a top-level line in {where}, above the first [table]; replace the line if the key is already set"
    lines = []
    for req, key, allowed, bad, fix, changes in [
            (6, "sandbox_mode", CODEX_SANDBOX, "danger-full-access", "workspace-write",
             "commands run in Codex's sandbox: writes limited to the workspace"),
            (8, "approval_policy", CODEX_APPROVAL, "never", "on-request",
             "Codex asks the person before commands it may not run on its own")]:
        v = d.get(key)
        help_ = Help(where, changes, f'{key} = "{fix}"', "toml", how)
        if v is None:
            lines.append(Finding(req, "codex", key, status, "absent",
                                 f"not set: Codex's built-in default applies (not checked); {basis}{note}", where, help_))
        elif not isinstance(v, str) or v not in allowed:
            lines.append(Finding(req, "codex", key, status, "unknown",
                                 f"not a value Codex accepts (not shown); {basis}{note}", where))
        elif v == bad:
            lines.append(Finding(req, "codex", key, status, "absent", f"{v}; {basis}{note}", where, help_))
        else:
            lines.append(Finding(req, "codex", key, status, "present", f"{v}; {basis}{note}", where))
    return lines


def unverified_lines(installed: set[str]) -> list[Finding]:
    return [Finding(6, h, "permissions and sandbox", UNKNOWN, "unknown",
                    "config format not verified for this harness; prove key names on the installed version first",
                    "harness_health.py docstring") for h in ("agy", "qwen", "dsh", "opencode") if h in installed]


# --- gather, render ---------------------------------------------------------------------------------------------

def gather(home: Path, cwd: Path, env: dict, scripts: Path = SCRIPTS) -> list[Finding]:
    installed = {h for h in HARNESSES if shutil.which(h, path=env.get("PATH"))}
    w = Where(home, cwd, env)
    lines = [Finding(0, h, "installed", VERIFIED if h in installed else MISSING, "-",
                     "on PATH" if h in installed else "not on PATH", f"`command -v {h}`") for h in HARNESSES]
    lines += context_lines(w)
    lines += covered_lines(scripts)
    lines += memory_and_log_lines(w, installed)
    lines.append(engine_kind_line(installed))
    if "claude" in installed:
        lines += claude_lines(w)
    if "codex" in installed:
        lines += codex_lines(w)
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
        out += [f"### R{f.req} · {f.harness} · {f.item}", "", f"- File: `{f.help.file}`",
                f"- What it changes: {f.help.changes}"]
        if f.help.snippet:
            out += [f"- How: {f.help.how}", "", f"```{f.help.lang}", f.help.snippet, "```"]
        out.append("")
    out.append("You apply any change; this script changed nothing.")
    return "\n".join(out) + "\n"


def self_test() -> int:
    """A settings file with no deny list must come out `absent` — the check can fail."""
    with tempfile.TemporaryDirectory() as td:
        home, cwd = Path(td) / "home", Path(td) / "proj"
        (home / ".claude").mkdir(parents=True)
        cwd.mkdir()
        w = Where(home, cwd, {})
        (home / ".claude" / "settings.json").write_text('{"permissions": {"allow": ["Bash(ls:*)"]}}')
        bad = [f.finding for f in claude_lines(w) if f.item == "deny rules"]
        (home / ".claude" / "settings.json").write_text('{"permissions": {"deny": ["Read(./.env)"]}}')
        good = [f.finding for f in claude_lines(w) if f.item == "deny rules"]
    if bad == ["absent"] and good == ["present"]:
        print("self-test PASS: no deny list → absent, a deny list → present — the check can fail.")
        return 0
    print(f"self-test FAIL: bad={bad} good={good}")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Harness health for method 3.1 (no quota spent; a run only reads).")
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
