Plan and design a "harness health" extension to the readiness step of a workflow-design method. What should it check, how should it judge "good enough" without invented thresholds, what "help" should it give when a condition is not good enough, and in what order should the pieces be built and checked?

Each of you: answer through your own rules. Give (a) your verdict on each unclear spot U1–U7 below (and raise new ones as N1, N2 …), (b) the design you would build — the checks per requirement, the output, the help, where it lives — and (c) the build order, each step with the check that can fail. Do not decide for EJ: a spot to drop is a question for EJ.

## Facts

**The request** (EJ, 2026-10-15, quoted): "design and execute a workflow that enhance the readiness step to also validate a harness health conditions, if not good enough can we provide some help, get the 4 experts to plan and design these."

**What a "harness" is here.** The app or CLI that runs an AI agent: Claude Code (`claude`), Codex CLI (`codex`), Antigravity (`agy`), Qwen Code (`qwen`), the DeepSeek Harness (`dsh`), opencode (`opencode`). All six are installed on this machine. The method dispatches work to them as "engines".

**The ten requirements** (pasted by EJ from an outside source, author unknown — treat as input, not a standard):
1. Clear context delivery — short durable instruction file (AGENTS.md / CLAUDE.md) plus skills and docs pulled on demand; context window as a budget.
2. Well-designed tools — simple unambiguous interfaces, error messages that tell how to fix the call, explicit boundaries.
3. Planning and task structure — task list with clear done-criteria.
4. State and memory across sessions — progress files, checkpoints, clean handoffs.
5. Independent verification — tests, linters, a separate evaluator so the builder does not grade its own work.
6. Guardrails and permissions — sandboxing, least privilege, hard policies for risky actions, prompt-injection defenses.
7. Recovery and retries — idempotent steps, rollback points, sensible retry limits.
8. Human-in-the-loop gates — define when a human approves or decides.
9. Observability — log every action, token and cost, decision point and anomaly.
10. Feedback loop — every agent mistake becomes a permanent fix (rule, check, tool); review the harness as models improve.

**The current readiness step** (`.claude/skills/workflow-design/scripts/readiness.py`, 398 lines, Python stdlib only):
- Runs at the start of every workflow design (method 3.1). Proves what is installed and logged in; never spends model quota.
- Output: a markdown (or `--json`) table in groups Tools · Models and logins · Skills and workflows · Memory · MCP · Machine · Open unknowns. Every line has a status — `verified` (a command run now proved it), `reported` (a local file claims it, may be stale), `unknown` (not provable here), `MISSING` (expected and absent) — plus the command or path that proved it.
- Probes today: `--version` of claude, codex, agy, qwen, node, python3, git; codex model cache; `agy models` (only with `--net`); qwen settings (never prints a key); skill folders of each harness; workflow scripts dir; optional blueprint dir; which instruction files exist (CLAUDE.md, AGENTS.md, QWEN.md, GEMINI.md); qwen memory; claude history; MCP servers from four config files; machine cores/RAM/disk; two fixed "open unknowns".
- Exit 0 ok · 1 when a `--require`d tool is not verified or a named blueprint dir is MISSING · 2 usage error. `--self-test` proves the check can fail.
- "Generic by design": no project hardcoded; the skill is copied into other projects through a skills bundle.
- Tests: `tests/test_readiness.py`, 26 tests (RT-01–RT-21), isolated HOME and fake executables; 26 passed on 2026-10-15.
- Gap: `dsh` and `opencode` are installed and the dispatcher has adapters for both, but readiness.py does not probe either.

**What the method already has per requirement** (main agent's mapping, not verified by anyone else):
1 readiness lists instruction files and skills · 2 dispatcher engine adapters with pinned flags · 3 workflow-design method + `design_gate.py` (per run) · 4 run `state.md`, state-entry skill, memory dirs · 5 `feature_gate.py`, `quote_check.py`, gate rule G6 (a different-kind reviewer for build nodes) · 6 the "Guard" stage — written rules only, nothing enforced · 7 `dispatch.py` timers, bounded repair rounds, resume · 8 Guard stage with approval owners · 9 `runlog.py`, `events.jsonl`, `harvest_run.py` (tokens per run) · 10 why-chain skill and a why-chain hook, a task-types ledger.

**Observed on this machine, 2026-10-15** (key names only were printed, no values):
- `~/.claude/settings.json`: keys env, permissions, model, enabledPlugins, extraKnownMarketplaces, effortLevel, modelSettings, tui, skipDangerousModePermissionPrompt, skipWorkflowUsageWarning, agentPushNotifEnabled, autoMode, hooks. `permissions` has one `allow` entry, no `deny` list. `hooks` has only `UserPromptSubmit`.
- The project has no `.claude/settings.json`.
- `~/.codex/config.toml` has no top-level `sandbox_mode` or `approval_policy` (so the CLI defaults apply; the defaults were not checked).
- Instruction files: project CLAUDE.md 127 lines, AGENTS.md 4 lines (a pointer), user-level ~/CLAUDE.md 73 lines.
- Config locations for dsh, opencode and agy permissions/sandbox: not looked at; unknown.

**House rules that bind the design:**
- Every check must be able to fail, and is shown failing once on a planted wrong input (a "sabotage") before it is trusted.
- Never fill a missing threshold with an invented number. A trigger is a comparison ("measure X against Y"), not a number picked up front; numbers that are needed are EJ's to give.
- Never print a secret; config files may hold keys.
- Sequential first; state-file driven; one writer.
- Evidence lives in `runs/<run-id>/`.
- The skill is used in other projects, so nothing project-specific may be hardcoded.

## Unclear spots (the main agent's list — id · what is unclear · kind · blocks · provisional assumption)

- **U1** Which harnesses are checked: every one found, or only those the design will dispatch to · decision · output shape · *assume: all found are listed; a `--harness` flag narrows the verdict to the ones the design uses.*
- **U2** What "help" is: advice text naming the exact setting and file, an auto-fix, a generated config patch the person applies, or a pointer to docs · decision · the help piece · *assume: advice plus a ready-to-apply snippet; the script never edits harness config.*
- **U3** What "good enough" means with no thresholds given · decision · every verdict · *assume: a pass/fail only where the requirement names a concrete thing (a deny list exists, a sandbox mode is set, a hook is installed); elsewhere report the measured number with no verdict.*
- **U4** Where it lives: more probes inside readiness.py, or a new `harness_health.py` that readiness calls or that runs beside it · decision · the build · *assume: a separate script with the same Probe shape and statuses, so readiness stays the inventory.*
- **U5** How the result changes the design (e.g. no sandbox → build nodes' Guard stakes go up; one verified engine kind → reviewer must be a script check) · decision · method text · *assume: a "Found → effect on the design" table in method 3.1, like the information-check table.*
- **U6** The config formats and key names of each harness (sandbox, permissions, hooks, logs) are not verified, and differ per version · unknown · every per-harness probe · *assume: a probe reads only what has been verified against the installed version; everything else is `unknown` with the reason.*
- **U7** Requirements 2, 3, 7 (and parts of 5, 8) are judged per run or per tool, not properties of the harness config · decision · scope · *assume: they are covered by the method's existing per-run gates and listed as "covered by <gate>", not probed.*
