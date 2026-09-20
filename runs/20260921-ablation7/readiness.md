# Readiness — 20260921-ablation7

Anything marked missing becomes a preparation piece at the front of the flow.
Every command below was **run**, not assumed. Two failed on the first attempt; both are recorded.

## Tools

| Tool | Needed for | Command that proved it works | Result |
|---|---|---|---|
| hybrid CLI | the run under test | `python3 -m ancient_games.hybrid tools` → table, rc=0 | works |
| scorer | P5 | `python3 -m ablation.score <journal> <case>` → markdown table | **works, but the first invocation FAILED**: `python3 ablation/score.py <journal>` → `ModuleNotFoundError: No module named 'ancient_games'`, and it needs **two** positionals (`journal`, `case`), optional `--repo`. Must be run as a module from the repo root. |
| pytest | regression gate | `python3 -m pytest -q` → **379 passed in 7.21s** | works |
| fixture repo | the task surface | `git cat-file -t 34c7bf66…` in `~/dev/seza/backtest` → `commit` | works (GM1's pinned sha exists; repo HEAD is `26aef09`) |
| `runs/` convention | output folder | `ls runs` → `20260920-readme-test-count` | exists, one prior run |
| Agent tool | the free agent under test, and the P1 researcher | used throughout this session | works |

## Skills that apply

| Skill | What it covers here |
|---|---|
| `workflow-design` | this document and the design beside it |
| `challenge-mediation` | typing the challenge and rating cost-of-being-wrong (input to the P1 risk judgement) |
| `chronos-ledger` | only if the run spans sessions; not used by default |

## Information

| What is needed | Where it is | Structure | Verified against source? | Who can read it |
|---|---|---|---|---|
| What the experiment must test | `docs/ABLATION_6.md:129-131` — "Testing it needs a task where the agent must act" | md | yes, quoted | any agent given the path |
| Pre-registration format | `docs/ABLATION_6.md`, commits `d6ec267`/`1a2259d` | md + git | yes | any agent |
| Case + packet format | `ablation/cases/GM1.json`, `ablation/packets/GM1.md` | json + md | yes, read | any agent |
| Scoring questions | `ablation/score.py:73` `PRIMARY`, `q1`–`q8` | python | yes, run | script |
| **Fixture ground truth: a genuinely dead, stakes-2 deletion target** | **NOT ESTABLISHED** | — | **no** | — |

## Missing or unverified → preparation pieces

| Item | Effect on the flow |
|---|---|
| **A deletion target whose deadness is established** | **Research piece P1 at the front.** This is the one blocking unknown. `eval/forecast.py` was the obvious candidate and is **disproved**: `tools/derive_g4_thresholds.py:57` imports from it and six files under `eval/tests/` reference it. Only the `NetOutcomeResolver` *class* (`eval/forecast.py:255`) is unreferenced — one definition, no other hit. |
| `loop/graph_memory.py` is unusable as a target | Its ground truth is the thing in dispute (`ABLATION_5.md:159`, `ABLATION_6.md:132`: "Still at the gate"). A new ablation must not inherit an unknown answer. **Excluded by rule.** |
| Stakes tier of a candidate target | Verified for the *directories*: `registry.py:55` R7 covers `engine/ runner.py config.py eval/ loop/` at **stakes 2, gate=checkpoint** — so a deletion there engages `guard` without hitting an owner gate. Per-target `consumers` could still pull in R1/R2 (`eval/protocol.json`, `eval/holdout_access.log`); P1 must check that for the chosen target. |
