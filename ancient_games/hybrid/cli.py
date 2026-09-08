"""HYBRID_SPEC §9 — the ablation CLI: a thin shell over the loop's own `step`.

A subagent acting as the main agent calls tools one process at a time:

    python3 -m ancient_games.hybrid init --run-id R --journal /abs/j.jsonl --cwd /abs/repo
    python3 -m ancient_games.hybrid tools [--inputs | --schema]
    python3 -m ancient_games.hybrid call gate '{"name": ...}'
    python3 -m ancient_games.hybrid approve --gate checkpoint --action-id "commit:['master']" --approver ej
    python3 -m ancient_games.hybrid fail-dispatch --agent-id X --reason "..."

`init` writes a run manifest (run_id, journal, cwd, tool dirs, ceiling, ctx
file); every other subcommand reads it via `--manifest` or `$ANCIENT_GAMES_RUN`.
`call` loads the manifest's ctx, runs `loop.step` (the same invariant check →
execute-or-refuse → `tool_call` event the scripted loop runs), saves ctx, and
prints the ToolResult as JSON. Exit codes: 0 executed (ok or declined by the
tool's own body — read `ok`), 2 refused by an invariant or declined for malformed
args (`reason` starts `invalid-args:` and names the expected shape — H10, never a
traceback), 1 error.

`init`'s default ceiling (H13, ABLATION_2) is 2× the longest free-agent journal
under `ablation/runs/**` (tool_call events), overridable with `--ceiling`.

`approve` and `fail-dispatch` write the two orchestrator-only events (§6).
The subagent under ablation must NOT call `approve` — MAIN does; the packet
says so and the scorer counts the event regardless of who wrote it.

Ctx persists between processes as `dataclasses.asdict(ctx)` JSON and is
rehydrated with `types.hydrate` (tuples come back as tuples, nested
dataclasses as dataclasses) — no new logic, the loop's own `Ctx` end to end.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import re
import sys
import typing
from typing import Any

from ancient_games import registry as reg
from ancient_games.ctx import ABSENCE_PATTERNS, CLAIM_KINDS, DIFFICULTIES, MECHANISMS, MODES, ROLES, ArtifactRef, Ctx
from ancient_games.journal import _ENUMS, Journal
from ancient_games.stages import ActionInput, Candidate, Claim, TaskInput

from . import autonomy, loop
from .registry import RegisteredTool, load_tools
from .types import Call, hydrate

ENV_MANIFEST = "ANCIENT_GAMES_RUN"
FALLBACK_CEILING = 44  # used only when no journal exists under RUNS_DIR
RUNS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ablation", "runs")
EXIT_EXECUTED, EXIT_ERROR, EXIT_REFUSED, EXIT_PAUSED = 0, 1, 2, 3
INVALID_ARGS = "invalid-args:"


def default_ceiling(runs_dir: str = RUNS_DIR, fallback: int = FALLBACK_CEILING) -> int:
    """H13: 2× the most tool_call events any journal under `runs_dir` holds (the real free-agent traces),
    not 2× a scripted trace — a free agent spends calls on discovery and retries a script never needs."""
    longest = 0
    for dirpath, _, files in os.walk(runs_dir):
        for name in files:
            if not name.endswith(".jsonl"):
                continue
            with open(os.path.join(dirpath, name), encoding="utf-8") as fh:
                n = sum(1 for ln in fh if ln.strip() and json.loads(ln).get("event") == "tool_call")
            longest = max(longest, n)
    return 2 * longest if longest else fallback


# --- manifest ---------------------------------------------------------------------
def default_manifest_path(journal: str) -> str:
    return journal + ".run.json"


def write_manifest(run_id: str, journal: str, cwd: str, tool_dirs: list[str], ceiling: int,
                   manifest: str | None = None, autonomy_mode: str = "auto",
                   pause_after: list[dict] | None = None, resume: bool = False) -> str:
    for p in (journal, cwd, *tool_dirs):
        if not os.path.isabs(p):
            raise ValueError(f"path must be absolute: {p!r}")
    if not os.path.isdir(cwd):
        raise ValueError(f"cwd is not a directory: {cwd!r}")
    rules = autonomy.validate_rules(autonomy.rules_for(autonomy_mode, pause_after))
    if resume:
        # The journal is the mode's home (§8), so a resume adopts what the run already declared
        # rather than letting a second `init` with different flags contradict it.
        cfg = autonomy.config_from(Journal(journal, run_id).read())
        autonomy_mode, rules = cfg["autonomy"], autonomy.rules_for(cfg["autonomy"], cfg["pause_after"])
    manifest = manifest or default_manifest_path(journal)
    ctx_path = manifest + ".ctx.json"
    # `pause_after` here is the RESOLVED rule list, so the manifest never reads `[]` for a mode
    # that pauses on every call; enforcement still reads `run_config` back off the journal.
    data = {"run_id": run_id, "journal": journal, "cwd": cwd, "tool_dirs": list(tool_dirs),
            "ceiling": int(ceiling), "ctx_path": ctx_path,
            "autonomy": autonomy_mode, "pause_after": list(rules)}
    os.makedirs(os.path.dirname(manifest), exist_ok=True)
    with open(manifest, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
    if not resume:
        save_ctx(ctx_path, Ctx())
        # The mode's home is the journal, not the manifest and not ctx (AUTONOMY_DESIGN v2 §8):
        # a journal is append-only, so no tool can unwrite it. The manifest copy is a convenience
        # for `queue`/`--help`; every enforcement path reads `run_config` back off the journal.
        Journal(journal, run_id).append({"event": "run_config", "autonomy": autonomy_mode,
                                         "pause_after": list(rules), "ceiling": int(ceiling)})
    return manifest


def read_manifest(path: str | None) -> dict:
    path = path or os.environ.get(ENV_MANIFEST)
    if not path:
        raise ValueError(f"no run manifest: pass --manifest or set ${ENV_MANIFEST} (run `init` first)")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# --- ctx persistence ------------------------------------------------------------------
def save_ctx(path: str, ctx: Ctx) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(dataclasses.asdict(ctx), fh, sort_keys=True, default=str)


def load_ctx(path: str) -> Ctx:
    if not os.path.exists(path):
        return Ctx()
    with open(path, encoding="utf-8") as fh:
        return hydrate(Ctx, json.load(fh))


# --- output ---------------------------------------------------------------------------
def json_safe(v: Any) -> Any:
    if dataclasses.is_dataclass(v) and not isinstance(v, type):
        v = dataclasses.asdict(v)
    return json.loads(json.dumps(v, default=str))


def tools_table(tools: dict[str, RegisteredTool], inputs: bool = False) -> str:
    rows = [("name", "side_effects", "cost", "participates_in", "doc") + (("inputs",) if inputs else ())]
    for name in sorted(tools):
        t = tools[name]
        m = t.manifest
        row = (name, m["side_effects"], m["cost"], ",".join(m["participates_in"]) or "-", t.doc)
        if inputs:
            row += (json.dumps(m["inputs"], sort_keys=True),)
        rows.append(row)
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]) - 1)]
    lines = []
    for r in rows:
        head = "  ".join(c.ljust(w) for c, w in zip(r[:len(widths)], widths))
        lines.append((head + "  " + r[len(widths)]).rstrip())
    return "\n".join(lines)


# --- schema (H4, ABLATION_1) -----------------------------------------------------------------
DATACLASSES: dict[str, type] = {"TaskInput": TaskInput, "ActionInput": ActionInput, "ArtifactRef": ArtifactRef,
                                "Claim": Claim, "Candidate": Candidate}
ENUMS: dict[str, tuple] = {
    "mode": MODES, "difficulty": DIFFICULTIES, "role": ROLES, "kind": CLAIM_KINDS,
    "mechanism": MECHANISMS + ("other:<name>",),
    "evidence_type": _ENUMS[("claim_recorded", "evidence_type")],
    "pre_fix_result": _ENUMS[("check_executed", "pre_fix_result")],
    "irreversible_clause": ("a", "b", None),
    "governance_gated": ("none",) + tuple(r.id for r in reg.REGISTRY if r.gate == "owner"),
}
NOTES: dict[str, str] = {
    "governance_gated": "a registry row id whose gate=owner, or \"none\" — never a bool",
    "consumers": "downstream paths that READ the mutated artifact (D2′) — not the files this action reads; "
                 "naming an owner-gated file here owner-gates the action",
    "tripwires": "{hub-name-or-matched-ref-path: command}; declare the command in the form it will be run at prove "
                 "time (a pre-commit `git diff HEAD` is wrong post-commit) — re-call guard to correct it",
    "falsifies": "a claim_id (this call's, or one recorded in this run); the condition goes in `expected`",
    "framings": "{claim_id: [framing, ...]} — a LIST per claim, e.g. {\"C1\": [\"static-scan\", \"runtime-trace\"]}; "
                "keyed by claim_id, not by author",
    "kind": "assigned by rule (D-KIND): text asserting absence / a universal negative (" + "|".join(ABSENCE_PATTERNS)
            + ") is judgment; executable is accepted for such text only with closed_world",
    "closed_world": "record_claim only: why the check space is complete (e.g. \"AST over every .py + grep for the name as a "
                    "string + no getattr/globals() idioms\"); required to keep kind=executable on absence text; shown "
                    "verbatim at the checkpoint gate",
    "n_required": "set by corroborate — never passed by the caller",
    "stakes": "set by corroborate — never passed by the caller",
    "actor": "set by corroborate from ctx.actor — never passed by the caller",
    "known_facts": "list of [fact, method, result, date]",
    "actors": "{action-name: MAIN | <agent-id> | none}",
    "gate_at": "the action the gate sits at, e.g. \"commit\"",
    "deliverables": "done only (H14): changed paths this run leaves deliberately uncommitted, e.g. "
                    "[\"research/holdout_recommendation.md\"]; each must also be the mutate ref of a guard in this run — "
                    "any other changed path still refuses",
}
_NAME_RE = re.compile(r"\b(" + "|".join(DATACLASSES) + r")\b")


def _type_str(hint: Any) -> str:
    s = str(hint) if not isinstance(hint, type) else hint.__name__
    s = s.replace("typing.", "")
    return re.sub(r"\b(?:[a-z_]+\.)+(?=[A-Za-z])", "", s)


def _field_lines(cls: type, indent: int, seen: tuple[str, ...]) -> list[str]:
    pad = "  " * indent
    hints = typing.get_type_hints(cls)
    out: list[str] = []
    for f in dataclasses.fields(cls):
        t = _type_str(hints.get(f.name, Any))
        if f.default is not dataclasses.MISSING:
            req = f" = {f.default!r}"
        elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
            req = f" = {f.default_factory()!r}"  # type: ignore[misc]
        else:
            req = "  (required)"
        line = f"{pad}{f.name}: {t}{req}"
        if f.name in ENUMS:
            line += "  one of: " + " | ".join("null" if v is None else str(v) for v in ENUMS[f.name])
        if f.name in NOTES:
            line += f"  # {NOTES[f.name]}"
        out.append(line)
        for name in _NAME_RE.findall(t):
            if name not in seen:
                out += _field_lines(DATACLASSES[name], indent + 1, seen + (name,))
    return out


def tools_schema(tools: dict[str, RegisteredTool]) -> str:
    """Per tool: each arg's name and type from the manifest, dataclass-typed args expanded field by
    field (type, default or required, enum values, notes) — what a caller needs to form valid args."""
    lines: list[str] = []
    for name in sorted(tools):
        m = tools[name].manifest
        lines.append(f"{name}  side_effects={m['side_effects']}  cost={m['cost']}  -> {m['outputs']}")
        if not m["inputs"]:
            lines.append("  (no args)")
        for arg, t in sorted(m["inputs"].items()):
            line = f"  {arg}: {t}"
            if arg in ENUMS:
                line += "  one of: " + " | ".join("null" if v is None else str(v) for v in ENUMS[arg])
            if arg in NOTES:
                line += f"  # {NOTES[arg]}"
            lines.append(line)
            for dc in _NAME_RE.findall(t):
                lines += _field_lines(DATACLASSES[dc], 2, (dc,))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# --- subcommands ------------------------------------------------------------------------
PHASES_EXAMPLE = [{"name": "research", "tool": "corroborate"},
                  {"name": "implement", "tool": "prove", "exit_type": "PASS"},
                  {"name": "land", "tool": "commit"}]


def cmd_init(a: argparse.Namespace) -> int:
    if a.phases_example:
        print(json.dumps(PHASES_EXAMPLE, indent=2))
        return EXIT_EXECUTED
    ceiling = a.ceiling if a.ceiling is not None else default_ceiling()
    pause_after = json.loads(a.pause_after) if a.pause_after else None
    if pause_after is not None and not isinstance(pause_after, list):
        raise ValueError("--pause-after must be a JSON list of {name, tool, exit_type?} objects")
    if a.resume and not os.path.exists(a.journal):
        raise ValueError(f"--resume needs an existing journal: {a.journal!r}")
    path = write_manifest(a.run_id, a.journal, a.cwd, a.tool_dir, ceiling, a.manifest,
                          a.autonomy, pause_after, resume=a.resume)
    print(json.dumps({"manifest": path, **read_manifest(path)}, indent=2, sort_keys=True))
    return EXIT_EXECUTED


def cmd_preauthorize(a: argparse.Namespace) -> int:
    m = read_manifest(a.manifest)
    journal = Journal(m["journal"], m["run_id"])
    for pat in a.scope_path:
        if not autonomy.safe_path(pat.replace("*", "x")):
            raise ValueError(f"scope path must be repo-relative with no '..' segment: {pat!r}")
    gid = f"grant:{len(autonomy.grants(journal.read())) + 1}"
    ev = journal.append({"event": "preauthorization_recorded", "grant_id": gid, "approver": a.approver,
                         "scope_paths": list(a.scope_path), "max_uses": a.max_uses,
                         "allow_kind_overrides": a.allow_kind_overrides, "note": a.note})
    print(json.dumps(ev, indent=2, sort_keys=True))
    return EXIT_EXECUTED


def cmd_queue(a: argparse.Namespace) -> int:
    """The deferral queue (§6). Exits non-zero while any deferral stands — the queue is a record,
    not a gate, and a non-zero exit is the cheapest teeth that does not touch the invariant floor."""
    m = read_manifest(a.manifest)
    q = [e for e in Journal(m["journal"], m["run_id"]).read() if e.get("event") == "deferred_decision"]
    print(json.dumps({"deferred": q, "count": len(q)}, indent=2, sort_keys=True))
    return EXIT_ERROR if q else EXIT_EXECUTED


def cmd_tools(a: argparse.Namespace) -> int:
    dirs: list[str] = []
    if a.manifest or os.environ.get(ENV_MANIFEST):
        try:
            dirs = read_manifest(a.manifest).get("tool_dirs", [])
        except FileNotFoundError:
            dirs = []
    tools = load_tools(*dirs)
    print(tools_schema(tools) if a.schema else tools_table(tools, inputs=a.inputs))
    return EXIT_EXECUTED


def cmd_call(a: argparse.Namespace) -> int:
    m = read_manifest(a.manifest)
    try:
        args = json.loads(a.args) if a.args else {}
    except json.JSONDecodeError as e:
        raise ValueError(f"args must be JSON: {e}") from e
    if not isinstance(args, dict):
        raise ValueError("args must be a JSON object")
    tools = load_tools(*m["tool_dirs"])
    journal = Journal(m["journal"], m["run_id"])
    events = journal.read()
    index = sum(1 for e in events if e.get("event") == "tool_call" and e.get("run_id") == m["run_id"])
    # AUTONOMY_DESIGN v2 §3: a pause is an effective ceiling, so the bound check the CLI already
    # performs on every process is the whole enforcement — no new refusal path, and it survives a
    # restart for free because the budget is recomputed from the journal rather than remembered.
    rules = autonomy.rules_from_events(events)
    if index >= autonomy.effective_ceiling(events, rules, m["ceiling"]):
        b = autonomy.open_boundary(events, rules)
        if b is None:
            raise ValueError(f"ceiling reached: {index} tool calls >= ceiling {m['ceiling']}")
        print(json.dumps({"paused_at": b.id, "boundary": b.name, "step": index,
                          "resume": autonomy.pause_message(b)}, indent=2, sort_keys=True))
        return EXIT_PAUSED
    ctx = load_ctx(m["ctx_path"])
    st = loop.step(tools, Call(a.tool, args), journal, ctx, index, cwd=m["cwd"], events=events)
    save_ctx(m["ctx_path"], ctx)
    out = {"tool": a.tool, "step": index, "refused_by": st.refused_by,
           "ok": bool(st.result.ok) if st.result is not None else False,
           "reason": st.result.reason if st.result is not None else journal.read()[-1]["reason"],
           "value": json_safe(st.result.value) if st.result is not None else None}
    print(json.dumps(out, indent=2, sort_keys=True))
    if st.refused_by:
        return EXIT_REFUSED
    if st.result is not None and not st.result.ok and (st.result.reason or "").startswith(INVALID_ARGS):
        return EXIT_REFUSED  # H10: malformed args are declined with the expected shape, exit 2
    if a.tool not in tools:
        return EXIT_ERROR  # journaled as the loop journals it, but not a tool that ran
    return EXIT_EXECUTED


def cmd_approve(a: argparse.Namespace) -> int:
    m = read_manifest(a.manifest)
    ev = Journal(m["journal"], m["run_id"]).append({"event": "approval_recorded", "action_id": a.action_id,
                                                    "gate": a.gate, "approver": a.approver, "note": a.note})
    print(json.dumps(ev, sort_keys=True))
    return EXIT_EXECUTED


def cmd_fail_dispatch(a: argparse.Namespace) -> int:
    m = read_manifest(a.manifest)
    ev = Journal(m["journal"], m["run_id"]).append({"event": "dispatch_failed", "agent_id": a.agent_id,
                                                    "reason": a.reason})
    print(json.dumps(ev, sort_keys=True))
    return EXIT_EXECUTED


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 -m ancient_games.hybrid", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--manifest", help=f"run manifest written by `init` (default: ${ENV_MANIFEST})")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="write the run manifest (and an empty ctx)")
    s.add_argument("--run-id", required=True)
    s.add_argument("--journal", required=True, help="absolute path of the journal (.jsonl)")
    s.add_argument("--cwd", required=True, help="absolute path of the repo the tools act on")
    s.add_argument("--tool-dir", action="append", default=[], help="extra tool directory (repeatable)")
    s.add_argument("--ceiling", type=int, default=None,
                   help="max tool calls for the run (default: 2x the longest journal under ablation/runs/, H13)")
    s.add_argument("--autonomy", choices=autonomy.MODES, default="auto",
                   help="auto: stop only where an invariant demands it (default, = today's behaviour); "
                        "phase: also stop after each --pause-after rule; step: stop after every call")
    s.add_argument("--pause-after", default=None,
                   help="JSON list of {name, tool, exit_type?} — required for --autonomy phase, "
                        "which has no default list (phases are named per task)")
    s.add_argument("--phases-example", action="store_true", help="print an example --pause-after list and exit")
    s.add_argument("--resume", action="store_true",
                   help="reuse an existing journal and run_id; keeps the saved ctx and run_config")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("tools", help="list the registered tools")
    s.add_argument("--inputs", action="store_true", help="also print each manifest's inputs")
    s.add_argument("--schema", action="store_true", help="print each tool's arg names, types, enum values and notes")
    s.set_defaults(fn=cmd_tools)

    s = sub.add_parser("call", help="call one tool through the loop's check → execute → journal step")
    s.add_argument("tool")
    s.add_argument("args", nargs="?", default="{}", help="JSON object of the tool's args")
    s.set_defaults(fn=cmd_call)

    s = sub.add_parser("approve", help="ORCHESTRATOR ONLY: record a gate approval (never called by the subagent)")
    s.add_argument("--gate", required=True, choices=("checkpoint", "owner", "resume"))
    s.add_argument("--action-id", required=True)
    s.add_argument("--approver", required=True)
    s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_approve)

    s = sub.add_parser("preauthorize", help="ORCHESTRATOR ONLY: grant an advance, path-scoped commit approval")
    s.add_argument("--approver", required=True)
    s.add_argument("--scope-path", action="append", required=True,
                   help="repo-relative glob the grant covers (repeatable); * stays within one path "
                        "segment, ** crosses segments. EVERY changed path must match one, or the commit refuses")
    s.add_argument("--max-uses", type=int, default=1)
    s.add_argument("--allow-kind-overrides", action="store_true",
                   help="permit committing under this grant when the run carries a D-KIND closed_world "
                        "override. OFF by default: it turns a pre-commit disclosure into a post-commit review")
    s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_preauthorize)

    s = sub.add_parser("queue", help="list this run's deferred decisions (exits non-zero while any stands)")
    s.set_defaults(fn=cmd_queue)

    s = sub.add_parser("fail-dispatch", help="ORCHESTRATOR ONLY: record that a dispatched agent failed")
    s.add_argument("--agent-id", required=True)
    s.add_argument("--reason", required=True)
    s.set_defaults(fn=cmd_fail_dispatch)
    return p


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    try:
        return a.fn(a)
    except (ValueError, FileNotFoundError, KeyError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
