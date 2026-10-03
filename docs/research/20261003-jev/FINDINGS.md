# Findings — Jev (TypeSafe) as a routing layer for agents
Produced 2026-10-03 by the COO (three WebSearch calls, three WebFetch reads). Question asked: what is the "JEV" EJ's
friend uses on the fork layer of his agent setup, and does it fit our method?

All rows are **reported**: every page was read through WebFetch, which returns a model-written summary, and the
sources are a vendor-adjacent site, a third-party blog and a plugin README. Nothing was run.

| id | Finding | Label | Source |
|---|---|---|---|
| J1 | Jev is a typed-decision model by TypeSafe AI, released 2026-09-15 with $40M seed funding; TypeSafe calls it a "System One model, built to make fast decisions inside software". It does not write text or code. | reported | https://flaviocopes.com/jev/ |
| J2 | Three question types: Noul (yes/no, a probability), Choice (one of the options you supply, with the full distribution and a confidence), Score (a calibrated position on a spectrum). Every answer is constrained to the supplied options; the output shape is guaranteed. | reported | https://flaviocopes.com/jev/ ; https://madewithjev.com/jev-multi-agent |
| J3 | A request carries a model name, the state (the data to judge) and a set of questions; all questions run in parallel against the same state, so independent questions go in one call. | reported | https://flaviocopes.com/jev/ |
| J4 | Price $0.042 per million input tokens, output free; latency typically 70–500 ms, mostly about 100 ms. Vendor claim "193.6x faster, 444.6x cheaper" than frontier LLMs on comparable tasks. | reported (vendor numbers) | https://flaviocopes.com/jev/ |
| J5 | Stated weaknesses: arithmetic and counting, dates, measurements and numeric comparison, extracting text values, images/audio/video, contradictory instructions. "Numbers, dates and counting stay in code." | reported | https://flaviocopes.com/jev/ |
| J6 | Hosted API only (TypeSafe direct, OpenRouter, Vercel AI Gateway); no open weights or local deployment — the state you send leaves the machine. | reported | https://flaviocopes.com/jev/ ; https://madewithjev.com/jev-multi-agent |
| J7 | A "fork" is a branching decision in a multi-agent workflow. Five routing forks named: who acts next; is the research good enough (accept/verify/reject); is the objective finished; should this action proceed (allow/confirm/deny); is this command safe (a score). Advice: start with one fork, the routing fork, because it runs at the top of every workflow and its answer is cheap to check. | reported | https://madewithjev.com/jev-multi-agent |
| J8 | The routing menu is built from live state: only workers that exist, tools that are installed, actions the host can run. | reported | https://madewithjev.com/jev-multi-agent |
| J9 | Limits stated by the same site: "the shape is guaranteed, the answer inside is not"; it classifies but must not grant permissions; it does not replace the orchestrator's control of workflow state. | reported | https://madewithjev.com/jev-multi-agent |
| J10 | "Almost none of this has a published benchmark. The measured figures are single-call, and the honest label for the rest is architecture, not result." No published routing accuracy, false-completion or recovery measure. | reported | https://madewithjev.com/jev-multi-agent |
| J11 | A DeepSeek Harness plugin routes routine turns to cheap subagent models with Jev: six questions per turn (task class, effort, blast radius, multi-module, user asked for the main agent, risk), a declarative policy (delegate mechanical/bugfix/research when effort ≤ M–L, blast radius below cross-module, confidence > 0.7, risk < 20%; a "careful" profile needs > 0.85), roles mapped to models (junior → qwen3.8-flash, implementer → deepseek-v4-flash). | reported | https://github.com/vitas/dsh-jev-subagent-dispatch |
| J12 | That plugin fails open: a missing key, timeout, 429 or bad config logs the reason and the main agent keeps the work. Its authors say the recommendation "should earn its place with evidence, not faith", and admit their log cannot see whether a child was spawned or the work redone. | reported | https://github.com/vitas/dsh-jev-subagent-dispatch |
| J13 | Other uses found: Jev-as-root orchestration and judge samples, an action-probability orchestration repo, and a pull request "route subagents with Jev" in a Claude Code mods repository. Not read. | unknown | https://github.com/sakthijas/multiAgent-jev ; https://github.com/prove-ai/jev-orchestration ; https://github.com/Reilley64/mods/pull/106 |

## Fit with our method (COO inference, n=0)

- Jev is a candidate engine for the **classification** row of `docs/TASK_TYPES.md` and for the **routing fork** of the
  dispatcher layer (`TODO.md`): who acts next, delegate to the cheap coder or keep with the COO, task category and
  case (A–D). It is not a coder, researcher, explorer or verifier.
- It must not replace a check. Its own sources say the answer inside the guaranteed shape may be wrong (J9) and
  routing accuracy is unmeasured (J10). Our checks stay scripts and blind reviewers; Jev may only choose *which*
  worker or check runs, with a confidence threshold and a fail-open fallback to the COO (J11, J12).
- It is measurable at almost no cost: the 300-prompt corpus (`tests/fixtures/operator_prompts_r*.jsonl`) with
  `tests/workflows/corpus_check.py` already scored codex at 96% and agy at 76% strict agreement on category labels.
  Running Jev on the same corpus with the same labelling rules would give a direct comparison.

## Gaps

No primary TypeSafe documentation was read, only summaries. Accuracy on our labels is unknown. Whether the
corpus prompts may be sent to a hosted API is EJ's call (J6). No API key exists on this machine (not checked).
