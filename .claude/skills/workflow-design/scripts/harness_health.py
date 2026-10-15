#!/usr/bin/env python3
"""harness_health.py — harness health for method 3.1 (readiness), beside readiness.py: R1–R9, R11 and R12 (R12
replaces R10).

readiness.py proves what is installed; this script reads how each installed harness is set up, against eleven
requirements for a harness (context, tools, planning, state, verification, guardrails, recovery, human gates,
observability, results that can be judged, and failures and successes that update the harness — R12, which replaces
the earlier feedback loop, R10). It never spends quota and never prints a config value other than a recognised mode or
event name or a count — config files hold keys. It writes no file, `--self-test` included.

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
import subprocess
import sys
import tomllib
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from readiness import CMD_TIMEOUT, MISSING, REPORTED, UNKNOWN, VERIFIED, cell, run_cmd  # noqa: E402

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
CLAUDE_HOOK_HANDLERS = {"command": ("command",), "prompt": ("prompt",), "agent": ("prompt",), "http": ("url",),
                        "mcp_tool": ("server", "tool"), "script": ("script",)}   # type → the fields it needs
CODEX_SANDBOX = {"read-only", "workspace-write", "danger-full-access"}
CODEX_APPROVAL = {"untrusted", "on-failure", "on-request", "granular", "never"}
SKIPPED_RULE = re.compile(r"mcp__.*\(")   # Claude Code skips an mcp__ rule with parentheses in a settings file
JSON_HOW = "merge into the file: keep its other keys, and add list items to a list that is already there"

REQUIREMENTS = {1: "Clear context delivery", 2: "Well-designed tools", 3: "Planning and task structure",
                4: "State and memory across sessions", 5: "Independent verification",
                6: "Guardrails and permissions", 7: "Recovery and retries", 8: "Human-in-the-loop gates",
                9: "Observability", 11: "Results can be judged",
                12: "Failures and successes update the harness"}
R10_NOTE = ("R10 (feedback loop) is replaced by R12. R11 and R12: the workflow-design skill's "
            "references/harness-requirements.md.")
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
    try:
        if not p.exists():
            return {}, "absent"
        d = json.loads(p.read_text())
    except (OSError, ValueError) as e:
        return None, f"unreadable: {type(e).__name__}"
    return (d, "") if isinstance(d, dict) else (None, "unreadable: top level is not a JSON object")


# --- per-run requirements: covered by the method's own scripts -------------------------------------------------

COVERED = [(2, "engine adapters with pinned flags", "engines.py"), (2, "dispatcher", "dispatch.py"),
           (3, "design gate", "design_gate.py"), (4, "run state template", "../assets/templates/state.md"),
           (5, "build gate (tests, scope, tamper)", "feature_gate.py"), (7, "timers and bounded repair", "dispatch.py"),
           (9, "run event log", "runlog.py"), (9, "token harvest", "harvest_run.py"),
           (11, "use-case register and coverage (R11.1)", "../guard/src/register.ts"),
           (12, "engine result check (R12.1)", "../guard/src/traps.ts"),
           (12, "failure journal (R12.2)", "../guard/src/journal.ts"),
           (12, "insight gate (R12.3)", "../guard/src/insight.ts"),
           (12, "success lines and rates (R12.7)", "../guard/src/rates.ts"),
           (12, "success paths (R12.7)", "../guard/src/paths.ts"),
           (12, "criteria and score (R12.7)", "../guard/src/criteria.ts")]

# A sub-requirement no script can read off a machine: the run's own design is where it is shown or not.
UNCHECKED = [(11, "first signal before the full verdict (R11.2)"),
             (12, "judges say what is wrong, not how (R12.4)"),
             (12, "review when a model changes (R12.5)"),
             (12, "withdrawal conditions (R12.6)")]
UNCHECKED_PROOF = "references/harness-requirements.md"


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


def unchecked_lines() -> list[Finding]:
    return [Finding(req, "-", item, UNKNOWN, "unknown", "no script checks it; each run's design must show it",
                    UNCHECKED_PROOF) for req, item in UNCHECKED]


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

def claude_lines(w: Where, read=load_json) -> list[Finding]:
    scopes = [("user", w.claude / "settings.json"), ("project", w.cwd / ".claude" / "settings.json"),
              ("local", w.cwd / ".claude" / "settings.local.json")]
    rc, out = run_cmd(["claude", "--version"])
    version = out.split()[0] if rc == 0 and out else "?"
    basis = f"key names from the {CLAUDE_KEYS_FROM} binary; installed {version}"
    proof = ", ".join(w.show(p) for _, p in scopes)
    project_file = w.show(scopes[1][1])
    loaded = []
    for scope, p in scopes:
        d, why = read(p)
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
        n = sum(1 for r in rules if isinstance(r, str) and r.strip() and not SKIPPED_RULE.match(r)) \
            if isinstance(rules, list) else 0
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

    # R12 hooks: an event counts when it holds at least one hook with a command; names shown only if recognised
    def runnable(h):
        need = CLAUDE_HOOK_HANDLERS.get(h.get("type")) if isinstance(h, dict) else None
        return bool(need) and all(isinstance(h.get(k), str) and h[k].strip() for k in need)

    def has_handler(groups):
        return isinstance(groups, list) and any(
            isinstance(g, dict) and isinstance(g.get("hooks"), list) and any(runnable(h) for h in g["hooks"])
            for g in groups)

    disabled, scope, where = effective(("disableAllHooks",))
    events = {e for _, _, d in loaded if isinstance(d.get("hooks"), dict)
              for e, groups in d["hooks"].items() if has_handler(groups)}
    named = sorted(e for e in events if e in CLAUDE_HOOK_EVENTS)
    others = len(events) - len(named)
    if disabled is True and named:
        lines.append(line(12, "hooks", "absent", f"disableAllHooks true ({scope}): no hook runs", Help(
            where, "lets the configured hooks run again", json.dumps({"disableAllHooks": False}, indent=2), "json",
            JSON_HOW)))
    elif named:
        lines.append(line(12, "hooks", "present",
                          f"events: {', '.join(named)}" + (f"; {others} unrecognised (not shown)" if others else "")))
    else:
        lines.append(line(12, "hooks", "absent", "no runnable hook for a recognised event" +
                          (f"; {others} unrecognised (not shown)" if others else "") +
                          ("; disableAllHooks true" if disabled is True else ""), Help(
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
    try:
        d = tomllib.loads(p.read_text()) if p.exists() else {}
    except (OSError, ValueError) as e:  # TOMLDecodeError and UnicodeDecodeError are ValueErrors
        return [Finding(6, "codex", "config", UNKNOWN, "unknown", f"{where} unreadable: {type(e).__name__}", where)]
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


# --- the guard's own state, through its own commands (guard/SPEC.md, Round 7) ----------------------------------

GUARD_CLI = "../guard/src/cli.ts"
GUARD_HARNESS = {"claude-code": "claude"}      # the doctor's harness name → this script's
GUARD_EXIT = {"doctor": {0}, "rates": {0}, "insight": {0, 1}}
GUARD_KEY = {"doctor": "harnesses", "rates": "rows", "insight": "open"}
GUARD_STATES = {"installed", "absent", "unknown"}
GUARD_ENV = {"BUN_RUNTIME_TRANSPILER_CACHE_PATH": "0"}   # bun otherwise writes its cache under HOME: this script writes nothing


def guard_json(command: str, cli: Path, cwd: Path, env: dict):
    """(payload, "") or (None, why it failed). The command's own text is never carried out of here."""
    try:
        p = subprocess.run(["bun", str(cli), command, "--json"], cwd=cwd, env={**env, **GUARD_ENV}, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, errors="replace", timeout=CMD_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except (FileNotFoundError, OSError):
        return None, "bun not on PATH"
    if p.returncode not in GUARD_EXIT[command]:
        return None, f"exit {p.returncode}"
    try:
        d = json.loads(p.stdout)
    except ValueError:
        d = None
    key = GUARD_KEY[command]
    if not isinstance(d, dict) or not isinstance(d.get(key), list):
        return None, "unexpected output"
    return d, ""


def guard_failed(item: str, command: str, why: str) -> Finding:
    return Finding(12, "-", item, UNKNOWN, "unknown", f"the guard's {command} failed: {why}", f"`harness-guard {command}`")


def guard_lines(installed: set[str], w: Where, scripts: Path, cwd: Path, env: dict) -> list[Finding]:
    """One absence line and nothing else when the guard or bun is not there — the run still has to report."""
    cli = (scripts / GUARD_CLI).resolve()
    if not cli.is_file():
        return [Finding(12, "-", "harness-guard", MISSING, "unknown", "guard not found beside this script",
                        "guard/src/cli.ts")]
    if not shutil.which("bun", path=env.get("PATH")):
        return [Finding(12, "-", "harness-guard", MISSING, "unknown", "bun not on PATH", "`command -v bun`")]
    return (guard_hook_lines(cli, w, installed, cwd, env) + [guard_rates_line(cli, cwd, env)]
            + [guard_insight_line(cli, cwd, env)])


def guard_hook_lines(cli: Path, w: Where, installed: set[str], cwd: Path, env: dict) -> list[Finding]:
    """One line per harness the doctor names that is installed here; the doctor's note is a count, not a key."""
    payload, why = guard_json("doctor", cli, cwd, env)
    if payload is None:
        return [guard_failed("harness-guard hooks", "doctor", why)]
    rows = payload["harnesses"]
    if not all(isinstance(r, dict) and isinstance(r.get("harness"), str) and r.get("guard") in GUARD_STATES
               and isinstance(r.get("note"), str) for r in rows):
        return [guard_failed("harness-guard hooks", "doctor", "unexpected output")]
    out = []
    for row in rows:
        name = row["harness"]
        harness = GUARD_HARNESS.get(name, name)
        if harness not in installed:
            continue
        guard = row["guard"]
        finding = "present" if guard == "installed" else "absent" if guard == "absent" else "unknown"
        help_ = None
        if finding == "absent":
            help_ = Help("-", "installs the guard's hooks: it blocks known engine-call traps, logs failures as they "
                               "happen, and asks for the insight before the agent stops",
                         f"bun {w.show(cli)} install --print {name}", "sh",
                         "prints the settings to merge; you apply them")
        out.append(Finding(12, harness, "harness-guard hooks", REPORTED, finding, row["note"],
                           "`harness-guard doctor`", help_))
    return out


def guard_rates_line(cli: Path, cwd: Path, env: dict) -> Finding:
    payload, why = guard_json("rates", cli, cwd, env)
    if payload is None:
        return guard_failed("checked results in this project", "rates", why)
    ok = fail = 0
    for row in payload["rows"]:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), int) and not isinstance(row.get(k), bool)
                                                for k in ("ok", "fail")):
            return guard_failed("checked results in this project", "rates", "unexpected output")
        ok, fail = ok + row["ok"], fail + row["fail"]
    return Finding(12, "-", "checked results in this project", VERIFIED, "measured",
                   f"{ok} success lines, {fail} failure records", "`harness-guard rates`")


def guard_insight_line(cli: Path, cwd: Path, env: dict) -> Finding:
    payload, why = guard_json("insight", cli, cwd, env)
    if payload is None:
        return guard_failed("insight for every failure (R12.3)", "insight", why)
    n = len(payload["open"])
    if not n:
        return Finding(12, "-", "insight for every failure (R12.3)", VERIFIED, "present", "no open failures",
                       "`harness-guard insight`")
    f = Finding(12, "-", "insight for every failure (R12.3)", VERIFIED, "absent",
                f"{n} open failures without a valid insight", "`harness-guard insight`")
    f.help = Help("runs/<run>/insight.md", "answers each open failure: six whys, the root cause, two or three fix "
                                         "options (R12.3)")
    return f


# --- gather, render ---------------------------------------------------------------------------------------------

def gather(home: Path, cwd: Path, env: dict, scripts: Path = SCRIPTS) -> list[Finding]:
    installed = {h for h in HARNESSES if shutil.which(h, path=env.get("PATH"))}
    w = Where(home, cwd, env)
    lines = [Finding(0, h, "installed", VERIFIED if h in installed else MISSING, "-",
                     "on PATH" if h in installed else "not on PATH", f"`command -v {h}`") for h in HARNESSES]
    parts = [(1, "-", "instruction files", lambda: context_lines(w)),
             (0, "-", "covered scripts", lambda: covered_lines(scripts)),
             (12, "-", "the guard", lambda: guard_lines(installed, w, scripts, cwd, env)),
             (12, "-", "unchecked sub-requirements", lambda: unchecked_lines()),
             (9, "-", "memory and logs", lambda: memory_and_log_lines(w, installed)),
             (5, "-", "engine kinds", lambda: [engine_kind_line(installed)])]
    parts += [(6, "claude", "settings", lambda: claude_lines(w))] if "claude" in installed else []
    parts += [(6, "codex", "config", lambda: codex_lines(w))] if "codex" in installed else []
    for req, harness, item, part in parts:
        try:
            lines += part()
        except OSError as e:  # a folder the person cannot read: say so, never crash or print its path
            lines.append(Finding(req, harness, item, UNKNOWN, "unknown", f"unreadable: {type(e).__name__}", "-"))
    lines += unverified_lines(installed)
    return sorted(lines, key=lambda f: f.req)


def select(lines: list[Finding], harnesses: list[str]) -> list[Finding]:
    return [f for f in lines if not harnesses or f.harness in ("-", *harnesses)]


def to_markdown(lines: list[Finding]) -> str:
    out = [f"# Harness health — {date.today().isoformat()} — {socket.gethostname()}", "",
           "Configured is not enforced: each line reads what a config file says; none proves the harness enforces "
           "it. Nothing was changed; no quota spent.", "", "## Requirements", "",
           "| # | Requirement | " + " | ".join(FINDINGS) + " |", "|---|---|" + "---|" * len(FINDINGS)]
    for n, name in REQUIREMENTS.items():
        counts = [sum(1 for f in lines if f.req == n and f.finding == k) for k in FINDINGS]
        out.append(f"| R{n} | {name} | " + " | ".join(str(c) for c in counts) + " |")
    out += ["", R10_NOTE]
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
    w = Where(Path("/nonexistent/home"), Path("/nonexistent/proj"), {})
    user = w.claude / "settings.json"

    def reader(settings):
        return lambda p: (settings, "") if p == user else ({}, "absent")
    bad = [f.finding for f in claude_lines(w, reader({"permissions": {"allow": ["Bash(ls:*)"]}}))
           if f.item == "deny rules"]
    good = [f.finding for f in claude_lines(w, reader({"permissions": {"deny": ["Read(./.env)"]}}))
            if f.item == "deny rules"]
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
