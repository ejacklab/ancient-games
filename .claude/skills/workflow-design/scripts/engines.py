#!/usr/bin/env python3
"""engines.py — the engine adapters dispatch.py runs nodes with, one descriptor each.

The seam exists so adding or re-enabling an engine is one entry here, not four edits scattered through the
dispatcher (`ENGINES`, the command builder, the result parser, the silent-failure map). Adding an engine means
adding one `Engine(...)` to `REGISTRY`; nothing else in dispatch.py knows engine names.

An adapter answers two questions: what command line runs this node, and how is the engine's final answer read
back. Everything else — timers, process groups, the pass-back check, the model check — is engine-neutral and
stays in dispatch.py.

  codex · qwen · agy   external CLIs, each with its own subscription auth (EXECUTOR_KINDS.md)
  claude               Claude Code's own CLI; re-enabled 2026-10-03 (on Claude Code the Workflow tool already
                       served Claude nodes, so the dispatcher refused it — that reason does not hold on another
                       harness, and here `claude -p` is the only route to a Claude executor)
  dsh                  the DeepSeek Harness itself, headless: `dsh headless "<task>"` answers one task and exits
  script               a local command, for tests and for deterministic checks

Adding an engine is a claim about a CLI, so it carries a canary (method 3.1, EXECUTOR_KINDS "the canary piece")
and the flags are pinned against the installed version. Verified against: codex-cli 0.159.3, agy 1.2.16,
qwen 0.24.7, claude 2.1.288, dsh 0.2.0-rc.2 — all on 2026-10-03.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Mapping

# A builder turns one node into argv. A parser turns the engine's stdout (and, for some engines, the result file
# the engine wrote) into (result text, the model the tool itself reported or None). Both raise ValueError when
# the stream is unreadable; dispatch.py turns that into an executor failure, not a failed attempt.
Builder = Callable[[dict, str, str, Path, Path, int], list[str]]
Parser = Callable[[str, Path], "tuple[str, str | None]"]


@dataclass(frozen=True)
class Engine:
    """One engine adapter.

    name             the value a plan node puts in `engine`
    build, parse     the two engine-specific operations
    needs_model      when false, `check_plan` does not demand a model (the engine takes it from its own config)
    silent_failures  stderr notices that mean the call did not finish although the exit code was 0
    (no fallback: removed 2026-10-05 — a failed engine blocks the node and reports) no fallback
    note             one line for the design docs; keep it factual and dated
    """
    name: str
    build: Builder
    parse: Parser
    needs_model: bool = True
    silent_failures: Mapping[str, str] = field(default_factory=dict)
    note: str = ""


def _mode(node: dict) -> str:
    return node.get("mode", "read-only")


def _timer(node: dict) -> str:
    return node.get("inner_timer", "")


# ---------------------------------------------------------------- external CLIs
def build_codex(node, model, prompt, out_file, cwd, attempt) -> list[str]:
    cmd = ["codex", "exec", "-m", model, "-s", "workspace-write" if _mode(node) == "write" else "read-only",
           "-C", str(cwd), "-o", str(out_file)]
    if node.get("effort"):
        cmd += ["-c", f"model_reasoning_effort={node['effort']}"]
    return cmd + [prompt]


def parse_codex(stdout, out_file) -> tuple[str, str | None]:
    return (out_file.read_text() if out_file.exists() else ""), None


def build_qwen(node, model, prompt, out_file, cwd, attempt) -> list[str]:
    return ["qwen", "--approval-mode", "auto-edit" if _mode(node) == "write" else "plan",
            "--max-wall-time", _timer(node), "-m", model, "--output-format", "json", prompt]


def parse_qwen(stdout, out_file) -> tuple[str, str | None]:
    events = json.loads(stdout)
    res = next((e for e in events if e.get("type") == "result"), None)
    init = next((e for e in events if e.get("type") == "system"), {})
    if res is None:
        raise ValueError("qwen stream has no result event")
    return res.get("result") or "", init.get("model")


def build_agy(node, model, prompt, out_file, cwd, attempt) -> list[str]:
    return ["agy", "-p", prompt, "--mode", "accept-edits" if _mode(node) == "write" else "plan",
            "--model", model, "--print-timeout", _timer(node), "--output-format", "text"]


def parse_stdout(stdout, out_file) -> tuple[str, str | None]:
    """The engine prints its final answer to stdout (agy, claude, dsh)."""
    return stdout, None


def build_claude(node, model, prompt, out_file, cwd, attempt) -> list[str]:
    # `-p/--print` is the flag; the prompt is positional. Permission modes are read-only `plan` / write
    # `acceptEdits`. Never `bypassPermissions` (EXECUTOR_KINDS rule 3, the `agy` equivalent).
    return ["claude", "-p", prompt, "--model", model, "--output-format", "text",
            "--permission-mode", "acceptEdits" if _mode(node) == "write" else "plan"]


def build_opencode(node, model, prompt, out_file, cwd, attempt) -> list[str]:
    """`opencode run` — headless, verified on opencode 1.18.34 (2026-10-04).

    The message MUST come before any `--file=`: `-f` is a greedy array option that swallows the following
    positional, so a file-first call makes opencode read the *prompt* as the attachment path and fail with
    "File not found: <the prompt>". Verified both ways with a one-line file.

    `--agent plan` is read-only and enforces it: asked to write a file it declined and created nothing.
    `--agent build` writes. Model ids are namespaced by provider (`minimax-coding-plan/MiniMax-M3.1-Flash-Preview`).

    No `-f` is emitted on purpose. An attachment opencode cannot read (a video) makes it exit 1 *even when the
    task then succeeds* — it recovered by extracting frames with ffmpeg and answering correctly — and the
    dispatcher reads a non-zero exit as an executor failure before it ever parses stdout. A node reads its own
    inputs instead.
    """
    return ["opencode", "run", "-m", model, "--agent", "build" if _mode(node) == "write" else "plan", prompt]


# ---------------------------------------------------------------- the harness itself
def build_dsh(node, model, prompt, out_file, cwd, attempt) -> list[str]:
    # `dsh headless "<task>"` boots one harness session, answers, prints the answer to stdout and exits
    # (`dsh headless --help`). It takes no --model: the model is the headless profile's, so the plan's model is
    # recorded but not passed. The prompt goes in argv because the dispatcher gives every engine stdin=DEVNULL.
    return ["dsh", "headless", prompt]


# ---------------------------------------------------------------- local commands
def build_script(node, model, prompt, out_file, cwd, attempt) -> list[str]:
    return [str(x).replace("{prompt_file}", str(out_file.with_suffix(".prompt"))).replace("{out}", str(out_file))
            .replace("{attempt}", str(attempt)) for x in node["cmd"]]


def parse_script(stdout, out_file) -> tuple[str, str | None]:
    if out_file.exists():
        return out_file.read_text(), None
    return stdout, None


# ---------------------------------------------------------------- the registry
# No fallbacks (removed 2026-10-05 at EJ's direction). One engine per node: a failure blocks the node and reports,
# and the COO decides. The map used to be here; see EXECUTOR_KINDS, "When a kind fails mid-run".
REGISTRY: dict[str, Engine] = {e.name: e for e in (
    Engine("codex", build_codex, parse_codex,
           note="codex exec; -o carries the answer, so no stdout parsing"),
    Engine("qwen", build_qwen, parse_qwen,
           note="--output-format json; the model is read from the tool's own `system` event, not the worker"),
    Engine("agy", build_agy, parse_stdout, silent_failures={"print timeout": "timeout", "auto-denied": "denied"},
           note="exit 0 can still mean timeout or an auto-denied tool in headless mode"),
    Engine("claude", build_claude, parse_stdout,
           note="claude -p; permission mode plan (read-only) or acceptEdits (write), never bypassPermissions"),
    Engine("opencode", build_opencode, parse_stdout,
           note="opencode run; --agent plan (read-only) or build (write). Answer on stdout, banner on stderr"),
    Engine("dsh", build_dsh, parse_stdout, needs_model=False,
           note="dsh headless; the model is the headless profile's, so a plan's model is recorded, not passed"),
    Engine("script", build_script, parse_script, needs_model=False,
           note="a local command with {prompt_file}/{out}/{attempt}; for tests and deterministic checks"),
)}

if __name__ == "__main__":       # a tiny listing, so the seam is inspectable without reading the dispatcher
    for e in REGISTRY.values():
        print(f"{e.name:8} model={'required' if e.needs_model else 'from its config':14} {e.note}")
