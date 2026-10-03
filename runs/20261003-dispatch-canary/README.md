# Dispatcher live canary — Codex and agy (2026-10-03)

`dispatch.py run` on `plan.json` (brief: `brief.md`, no tools, body `CANARY OK`); codex-cli 0.159.3
(`gpt-6.1-sol`, effort low, read-only), agy 1.2.14 (`gemini-3.8-flash-medium`, plan mode). n=1 per engine.

| Run | Codex | agy |
|---|---|---|
| 1st | ran, 11.8 s; answered `UNCLEAR: What are the exact runtime model identifier and UTC timestamps?` — correct: the pass-back note asked for the model and times while the brief forbade tools. The dispatcher stopped on it as designed. **Fixed:** the note now gives the model, and the dispatcher fills `started`/`ended` itself. | not reached (the run stops at the first stop) |
| 2nd (resume) | **timed out** at the 120 s outer timer, no output kept. **Fixed:** engine calls now get `stdin=DEVNULL`, and output printed before a timeout is saved. Whether inherited stdin caused the hang is **not proven** (one occurrence). | not reached |
| 3rd (fresh) | **pass**: valid header, `CANARY OK`, check passed, 5.8 s | **pass**: valid header, `CANARY OK`, check passed, 13.0 s, empty stderr |
| Sabotage | `outer_timeout_s: 3` → timeout (exit 124) → blocked: **can fail** | `inner_timer: 1s` → agy **exits 0** with empty stdout and stderr `[agy] print timeout after 1s with turn in progress; returning partial output` (6.8 s wall) → caught as an empty result → blocked: **can fail**. **Hardened:** that notice now counts as a timeout even when partial output is printed. |

Model check: neither Codex (`-o` last message) nor agy (text output) reports its model in what the dispatcher reads,
so both nodes are logged "model unverified"; the result headers carry the model the brief gave. Codex's real model
is in its rollout (`harvest_run.py`).

## qwen (qwen 0.24.7, `qwen3.8-flash`, plan mode) — `plan-qwen.json`

| Run | Result |
|---|---|
| 1st | **timed out** at the 120 s outer timer although `--max-wall-time 90s` was set, with nothing printed. Worse: the dispatcher killed only the `qwen` wrapper, and its `node` child **kept running** (still alive at 2 min 45 s, ignored SIGTERM, needed SIGKILL). **Fixed:** each call now runs in its own process group and a timeout kills the whole group (test: a grandchild must not survive). Why the first call hung is **not known** (one occurrence). |
| 2nd | **pass**: `CANARY OK`, valid header, check passed, and the **model verified** — qwen's own `system` event reported `qwen3.8-flash`, the plan's model (the first engine the dispatcher can verify). 101 s wall, 1 turn, **197,871 tokens**. No stray process afterwards. |
| Sabotage | `inner_timer: 1s` → qwen's own budget fired: exit 55, `FatalBudgetExceededError` → blocked: **can fail**. No stray process. |

Two qwen lessons: (1) run from the repo root, qwen loads the project's context (AGENTS.md, skills, memory) and a
one-line answer cost about 198k tokens, against 18–27k from an empty folder on 2026-10-02 — so a qwen node should
run in a clean working folder, or try `--safe-mode` (documented to disable context files, skills and MCP; untested);
(2) the call ran 101 s with `--max-wall-time 90s` and still exited 0, so qwen's own budget does not cover the whole
wall time — the outer timer stays the real limit.
