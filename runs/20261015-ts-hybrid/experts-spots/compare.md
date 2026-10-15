# Unclear spots — Linus, 孫子, 老子, Dave (method 3.3)

Question: `../expert-question-spots.md`. Answers: `answers/`. Check: quotes pass (the one "failure" is 范蠡, not asked).
Engines: linus codex · sun-tzu dsh · lao-tzu opencode · Dave a Claude subagent.

| Spot | Linus | 孫子 | 老子 | Dave | Decision (the COO's; provisional, for EJ at the report) |
|---|---|---|---|---|---|
| U1 key | ownership contract; test concurrent sessions | half known | drop session id, key by run folder | subagent session id unknown — fold into N1 | one journal per repository, records keyed by `session_id` (concurrent sessions do not block each other — Linus); insight files anywhere under `runs/` |
| U2 Stop loop | block-once escape contradicts the MUST | "block once" is all we can guarantee | block once | keep block-once, measure | **block every time while open** — EJ made R12.3 MUST and asked for "log and raise"; the harness's block cap is the loop guard; SessionStart raises open failures (raise) |
| U3 recognition | normalise; report what is not observed | unknown, linchpin | make the wrapper the only allowed form | replay transcripts; misses are the result | catalogue of engine shapes; misses listed by the E2 replay; an unrecognised call is a reported limit, not a pass |
| U4 port | keep Python | EJ's | drop the port | — | keep `harness_health.py`; `doctor` calls it |
| U5 install | prove one path | the arm B hinge | do not wait for EJ | N1 test | **N1 verified**: `claude -p --settings` fires the hooks; no config edited |
| U6 format | version the schema | known | reuse an existing shape | — | YAML, `register: 1` |
| U7 catalogue | proposed vs approved; record which entry denied | half | read-only to the agent | — | `status: approved | proposed`; only approved acts; a denial names the entry id; insights propose entries |
| U8 dispatcher hole | fix with a reproducer, separate patch | known | drop the fix | — | fix as its own commit with a test that fails first (R12.1 is MUST) |
| U9 arms | freeze the comparison | unknown | drop the live arms | keep arm A as control | keep both arms (N1 makes arm B possible); n = 3 provisional; thresholds EJ's |
| U10 adapters | prove each by behaviour | the four, not agy | drop dsh claims | opencode throw is N3 | Claude-protocol handler (verified on Claude Code only; Codex/Qwen reported) + opencode lint plugin; agy and dsh deferred |
| New | N1 guard self-failure; N2 M4 has no trigger; N3 valid record ≠ valid evidence | N2 wrapper bypass | N4 drop the whys-depth check | N1–N5 experiments | guard error → exit 1 + record (fail-open, visible); Stop validates registers touched this session (trigger); whys depth kept as a count plus a labelled heuristic; E2 replay for N4/N5 |
