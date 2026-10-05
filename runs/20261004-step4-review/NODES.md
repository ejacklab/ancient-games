# Run: 20261004-step4-review — node contracts

Challenge: review step 4 ("Size", method §3.4) of the workflow design algorithm.
Route: 4 independent read-only reviewers, blind to each other, one identical fixed checklist. Then a joining
comparison by the COO. No worker's verdict is taken on trust: every finding the reviewers raise is re-checked
against the cited line by the COO before it is reported.

Blindness: all four read the same brief. None sees another's output. They run concurrently — §3.7's five
conditions hold (no dependency between them; no shared writable resource; one does not change another's method;
each has its own output; the clock saving is worth the join).

| Node | Role | Engine | Model, effort | Mode | Inner timer | Output file |
|---|---|---|---|---|---|---|
| r-codex | independent reviewer | codex (CLI, `codex-cli 0.160.0`) | `gpt-6.1-sol`, `model_reasoning_effort=medium` | `-s read-only` | 1500 s | `codex.md` (`-o`), `codex.log` |
| r-claude | independent reviewer | claude (CLI, Claude Code 2.1.289) | `claude-sonnet-5-5`, effort n/a | `--permission-mode plan` | 1500 s | `claude.md`, `claude.log` |
| r-agy | independent reviewer | agy (CLI 1.2.16) | `gemini-3.1-pro-high`, high via model id | `--mode plan` | `--print-timeout 25m`, wrapped in 1500 s | `agy.md`, `agy.log` |
| r-opencode | independent reviewer | opencode (CLI 1.18.34) | `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, effort n/a | `--agent plan` | 1500 s | `opencode.md`, `opencode.log` |

Model choice, recorded so it is not a default:
- codex: `EXECUTOR_KINDS.md` reviewer row — `gpt-6.1-sol`, default effort. Passed explicitly as `medium` so a
  `~/.codex/config.toml` edit cannot change the run. `gpt-6.1-sol` is `visibility: list` in `codex debug models`
  (checked this run).
- claude: the daily tier, and the tier step 4 itself names for the blind fixed-checklist pass. Sonnet 5.5 not
  Opus 5.5 because this is a review, not the design work itself, and the reviewer row is the cheaper tier.
- agy: `EXECUTOR_KINDS.md` — "high thinking uses Gemini 3.1 Pro". This is a high-thinking review, so
  `gemini-3.1-pro-high`, not the `gemini-3.8-flash-medium` default. Present in `agy models` (checked this run).
- opencode: the only model `TASK_TYPES.md` routes to opencode. Present in `opencode models` (checked this run).

Readiness (method 3.1), proved this run, not assumed:
- `claude --version` = 2.1.289 · `codex --version` = codex-cli 0.160.0 · `agy --version` = 1.2.16 ·
  `opencode --version` = 1.18.34 — all on `PATH`, so all four are CLI calls, the first-choice route.
- Catalogs read for the binary that will make the call: `codex debug models`, `agy models`, `opencode models`.

Context given to each node: the brief path and the repository working tree, read-only. Withheld: the other three
reviewers' output, and the COO's own reading of step 4.

Contract: print the fixed-structure report in `BRIEF.md`; every finding carries file:line or a quote; at most 10
findings; write nothing to disk.

Evidence: each reviewer's stdout, saved verbatim to its output file. The COO re-runs any citation before reporting
a finding as real.

State: the COO writes each output file and the join; the reviewers read the brief and write nothing.
