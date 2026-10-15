# 孫子 (Sun Tzu) — can our troops, the task, and the ground carry this design

## Answer

Scoped to the four Claude-protocol harnesses and the structural modules (M2, M4, step 7), this is buildable now: our troops can attack and the ground allows the build. It is **half known** in my #4's sense on the enforcement chain and the effectiveness claim — we have not established how the code recognises a real engine call (U3), whether the guard can be loaded for the test without editing config (U5), how a failure is keyed to a session across subagents (U1/N1), whether the trap catalogue catches the recorded traps (U7), or the arms, model and n of the measurement (U9). Settle U3, U5 and U9 before building M5 or writing the prediction; ask EJ whether the opencode/agy fronts and M6 belong in this run at all.

**Pieces — can the three carry it?** (troops = engines/tools; the enemy = the task as posed; the ground = files, blueprint, information)

| Piece | Our troops | The task as posed | The ground | Verdict |
|---|---|---|---|---|
| M1 traps + result | yes — bun/TS, no deps | no — "after every engine call" needs call recognition (U3), and a wrapper hides the call (N2) | half — the 7 recorded traps exist; the catalogue caught 0 (U7) | **half** |
| M2 journal | yes — JSONL append | yes for failures the code sees | half — the per-session key is unproven across subagents and compaction (U1, N1) | **half** |
| M3 insight gate | half — structure yes; "a source that can be changed" is judgment | half — bounded by the Stop cap (U2) | half — no insight file exists anywhere yet to copy | **half** |
| M4 register + coverage | yes — YAML verified in bun 1.4.3 | yes — given a format (U6) | half — R11.1/R13 are a draft; the skip criterion is still open (N3) | **half** |
| M5 adapters | half — four Claude-protocol verified; opencode reported; agy unknown | half — blocking verified only for the four | half — dsh bridge not mounted; install is EJ's; test-load unverified (U5) | **half** |
| M6 doctor | yes — reads config, reports | half — "verified installed" is a claim about firing, not about a file | half — `harness_health.py` is on a branch, not master | **half** |
| step 3 prediction | yes | no — arms/model/n unset (U9) | half — the 7-trap replay is available | **unknown as posed** |
| step 5 review (Codex) | yes — codex present | yes | half — gpt-6.1-sol availability not verified | **half** |
| step 6 effectiveness | half — depends on U5 | no — depends on U9 | half — the replay half is ground-known | **unknown for the model arms** |
| step 7 integration | yes — `export_skills.py`, `SKILL.md` present | yes | yes | **known** |

**Spots — verdict and which half**

| Spot | Verdict | Known / missing |
|---|---|---|
| U1 session or run key | half | known: `session_id` is in the shared payload (verified). missing: the link from session to run folder, and whether subagents and compaction share it (N1) |
| U2 Stop loop guard | half | known: Stop can force continue and `stop_hook_active` exists. missing: the cap means "block until" is not ours to guarantee — "block once" is |
| U3 engine-call recognition | unknown | the linchpin of M1/M5; a wrapper bypasses a command pattern (N2) |
| U4 port vs keep | known | both doable; the choice is EJ's (conditional: the worktree branches from `feat/harness-health`, where the file is) |
| U5 hook install / test | half | known: `install --print` writes nothing. missing: that `claude -p --settings <file>` loads hooks — the whole effectiveness arm B |
| U6 register format | known | `Bun.YAML.parse` verified present; the format is EJ's |
| U7 trap catalogue | half | known: the mechanism. missing: coverage against the 7 recorded traps (0/7) |
| U8 dispatcher hole | known | ran and verified; one line plus a test. EJ decides now or later |
| U9 effectiveness arms/model/n | unknown | no n, metric or corpus; cannot be done as posed |
| U10 which adapters | half | known: the four Claude-protocol. missing: opencode blocking (reported), agy (exit code unknown) |
| N1 subagent/nested sessions | unknown | new — whose journal, and does the main Stop see a subagent's failures? |
| N2 wrapper bypass | unknown | new — the lint sees the command, not what it runs; the result check must then cover every tool result, not only recognised engine calls |
| N3 accepted blueprint | half | new — the ground is a draft (R11.2/R12 proposed; R12 has open items); freezing units against it may need a new count |

## How I decided

1. My #4 gives the exact three tests the question asks — our troops can attack, the enemy can be attacked, the ground permits battle — and the scale: 「知吾卒之可以擊，而不知敵之不可擊，勝之半也；…知敵之可擊，知吾卒之可以擊，而不知地形之不可以戰，勝之半也。…知彼知己，勝乃不殆；知天知地，勝乃可全」 (`quoted`, my #4). I applied it piece by piece and spot by spot above.
2. My #1 (`quoted`): 「多算勝，少算不勝，而況於無算乎？」 The readiness run counted tools (22 lines, bun 1.4.3, 1029 + 64 tests) but did not count the enemy or the ground. The reckoning is short on two columns, not empty — so my overall verdict is *half*, not *unknown*.
3. My #2 (`quoted`): 「先為不可勝，以待敵之可勝」. What is in our hands — modules, journal, tests, the replay corpus — can be made unbeatable now. What is in the enemy's hands — the agent's behaviour, the Stop cap, EJ's choices on U9 — is only waited for. So build, but do not build the effectiveness claim into the plan's success.
4. My #17 (`quoted`): 「策之而知得失之計，作之而知動靜之理」. The half-known spots become known by poking, not by more reading: replay the 7 traps, replay recorded engine commands through the linter, run one Stop round trip, run one subagent session.
5. My #6 (`quoted`): 「智者之慮，必雜於利害」. Every piece verdict above carries its harm column, not only its benefit.
6. My #3 (`quoted`): 「其下攻城。攻城之法，為不得已」. Strike the plan-level spots first (U3, U5, U9); the opencode and agy fronts are the walled city — last, or not now.
7. My #14 and #13 (`quoted`): 「少則能守之，不若則能避之」 and 「途有所不由」. Fight the verified front (the four Claude-protocol harnesses); hold on agy. A spot to drop is a question for EJ, not a removal — so I put M6 and the agy/opencode fronts as questions, not cuts.

## What I need to know

1. **U5:** is `claude -p --settings <file>` verified to load hooks? If not, arm B cannot be measured at all, and step 6 changes shape — perhaps to the quota-free replay alone. That is EJ's call.
2. **U1/N1:** is `session_id` stable for the whole session, subagents and compaction included? If not, M2 and M3 need a different key.
3. **N3:** does EJ accept R11–R13 as the blueprint now, or expect the draft to change? If it will change, do not compute the unit freeze and hash yet.
4. **U7:** does "backtest 0/7" mean the current catalogue caught none of the 7 recorded traps? If so, the first build item is the replay, not the handler.

## Costs and risks

- A command-pattern lint is defeatable by a wrapper — my #10, 「故兵無成勢，無恒形」. Price: a false sense of "cannot be skipped", the exact skip the design exists to close.
- The Stop cap is the enemy's ground — my #2. Price: the insight gate is one round; a session can end with an `insight_skipped` record, so R12.3's MUST is only as strong as `doctor`'s report.
- Enforcing a draft — my #1. Price: units frozen by hash against unaccepted text; a change starts a new count.
- Building M5 before U3 and U5 — my #3, 「攻城之法，為不得已」. Price: rework in the walled-city attack.
- Deferring opencode and agy — my #14. Price: the design's "every installed harness" table is stronger than what the build actually covers.
- PostToolUse annotates only (my reading of the facts; not from my list). Price: the result check cannot deny at the moment of failure; it journals, and only Stop blocks.
- A report without n — my #1, 「少算不勝」. Price: the honest line may be "not measured", and the claim that R11–R13 hold without memory is then not made.

## How we would know I was right

- Replay the 7 recorded traps and recorded engine commands through the linter: the hit count (0/7 today) is the measure. My #17: 「策之而知得失之計，作之而知動靜之理」.
- Load the guard with `claude -p --settings` in a sandbox against a catalogued trap and a session with a failure and no insight: PreToolUse denies, Stop blocks once, `insight_skipped` is written — count each.
- One subagent session with a planted failure: does the main Stop list it? yes or no.
- Effectiveness: if arms and n are set, the predicted counts against the measured ones, reported whichever way they fall. If not set, the observable is "not measured".
- I was wrong if a wrapper passes the lint unnoticed, or the trap replay stays at 0/7 after the catalogue is built.
