# Dave — the smallest experiment for each unknown spot

## Answer
Only **U3** is marked *unknown*. Four of the "decision" spots, though, rest on facts nobody has seen happen yet, so I raise them as **N1–N5**. Every hook fact in the research was checked against help text, schemas or bundles, and none was seen firing. One cheap "dump the payload" hook, fired once per harness before step 4, settles N1, N2 and part of U1 together. U3 and N4 can be tested for free by replaying commands from past session transcripts. Every acceptance threshold (recall, false positives, n per arm, what effect counts as "effective") stays open for EJ.

| Spot | Verdict |
|---|---|
| **U3** (unknown) | **Test before M1/M5.** Replay the engine-call commands already recorded in this project's Claude Code transcripts through the draft pattern list, then label every hit and every miss by hand. *Prediction:* direct calls are recognised (`codex exec`, `opencode run`, `four_experts.py`). Calls hidden behind a variable, a wrapper script or a heredoc are missed. Output files are found for `codex -o` and `> FILE` but not for engines that write only to stdout. *Stop:* one pass over the whole corpus, before M1's tests are written. The recall EJ would accept is **open**. A missed call fails *open*: PostToolUse stays silent, which works against R12.1, a MUST. So the miss list is the result, not the hit rate. |
| **N1** (new, unknown; hidden in U5 and U9) | Does `claude -p --settings <run file>` load and fire hooks from that file, with no change to user config? *Experiment:* a hook that writes a marker file and its stdin into the run folder, plus one trivial prompt. *Prediction:* it fires, and the existing why-chain hook still runs alongside it. *Stop:* one run. If there is no marker, U5's assumption fails and U9 arm B has nothing to run on. That goes to EJ before step 3 is committed. |
| **N2** (new, unknown; hidden in "one handler serves four") | Do Codex, Qwen and the dsh bridge send the payload the handler expects? The field *names* match per the schemas, but the *values* may not. *Experiment:* the same dump hook, one harmless shell call per harness. *Prediction (my reading):* the names match, but `tool_name` for the shell tool and the shape of `tool_input` differ between harnesses (for example the command as a string versus an array). If so, U3's patterns need an adapter for each harness. *Stop:* one call per harness. A harness that will not fire within one attempt is reported *unknown*, not fixed. |
| **N3** (new, unknown; U10's opencode half) | "Throwing in `tool.execute.before` blocks" is only *reported*. *Experiment:* a plugin that throws on one marker command, one `opencode run`, with its inputs copied inside the repo. *Prediction:* the call is blocked. *Stop:* one run. If the call is not blocked, the opencode adapter leaves this build and goes to EJ. |
| **N4** (new, unknown; AC2 tests only one clean command) | How often would the trap linter deny a command that was fine? *Experiment:* replay the same transcript corpus as U3 through `lintCommand` and hand-check every deny. *Prediction:* a few false denies, most likely on the stdin rule (commands that already feed stdin from a heredoc or pipe). *Stop:* one pass. The false-deny rate EJ would accept is **open**. A wrong deny blocks the agent mid-task, so this is the real cost of turning the guard on. |
| **N5** (new, unknown; the replay arm in U9 is circular) | The trap catalogue is written *from* the 7 recorded traps, so replaying those same 7 can only score 7/7. *Experiment:* hold-out data. Find later or earlier occurrences of the same traps in the transcripts that the catalogue was not written from, and count how many are caught. *Prediction:* lower than on the 7. *Stop:* one pass. Before writing the catalogue, also write down how many of the 7 can be expressed as a command pattern at all. |
| **U9** (decision, with unknowns inside) | Keep arm A (rules only) as the control. n per arm and the effect size that counts as "effective" are **EJ's**. *Prediction to commit in `prediction.md`:* in arm B, every expressible trap is denied, and a session that has failures but no insight is blocked once (AC4). In arm A, the agent skips the insight in at least some sessions with failures. The quota-free replay measures the *code*, not the agent; only the live arms measure skipping. |
| **U2** (decision; its effect is unknown) | Keep block-once. Whether one block actually produces an insight is measured inside U9 arm B: count the `insight_skipped` records against the insights written. No separate experiment. |
| **U1** (decision; one unknown) | The decision is EJ's. The unknown is whether a subagent's tool calls carry the parent's `session_id`. Fold that into N1: add one subagent call to the same dump run. |
| **U4, U6, U7, U8** | Decisions, not unknowns. No experiment needed. U6's fact (`Bun.YAML.parse` works) is already checked. |
| **U5** | The decision stands. Its hidden unknown is N1. |
| **U10** | Decision. agy's exit-code meaning stays *unknown* and agy stays deferred. Testing it is cheap (same dump hook) but not needed for this build, so whether to run it is a question for EJ. |

## How I decided
1. My #5: I started from what is already measured. The research shows no hook ever fired (*verified* means read from the installed version's own files). The 7-trap backtest exists (0 of 7 flagged, `runs/20261015-harness-health/report.md:36`). Claude Code transcripts for this project exist. I ran a rough count: 73 session files, 72 with Bash calls, and 53 command strings whose first 60 characters match an engine-call pattern. That is a crude grep, not a labelled count.
2. My #2: firing a dump hook once per harness costs far less than arguing about payload shape. Replaying transcripts costs no quota at all. So each unknown gets a test, not a discussion.
3. My #8: one path first. One dump hook and one run per harness, before any module is built on the assumption.
4. My #3: each spot above carries a prediction. Each stops after one run or one pass, and the stop date is "before step 4 starts" (step 3 for N1 and N5). I give no numeric bar, because EJ has given none.
5. My #4: the replay has no control and its known answers come from the same catalogue as the code. That is why N5 needs hold-out data, and why the effect on the agent is judged only arm A against arm B.
6. My #1: what would change my mind. If N1's marker appears, N2's payloads match exactly and the U3 replay misses nothing, then U3 and N2 shrink to "done" and the single-handler design stands as written.
7. My #6 and #7 (nature). The immune system is a close fit. Fixed innate recognisers match the PreToolUse lint, and memory added after an infection matches an insight adding a trap. *Same:* known patterns, matched fast, grown after an incident. *Different:* immune memory forms by itself, while here the agent proposes and EJ chooses (R12.3). The difference does not break the mechanism. The fit also points at autoimmunity, meaning false positives, which is why N4 exists.
8. My #9 and #10: every result above is reported however it falls. Each experiment is n=1 per harness, which is a hint about that version and nothing more.

## What I need to know
- U3: what share of recorded engine calls must be recognised for the guard to count as working? (EJ's threshold.)
- N4: what false-deny rate is acceptable? Or is any false deny a fail? (EJ's.)
- U9: n per arm, and what difference between arm A and arm B counts as "effective". (EJ's.)
- May the transcript replay read EJ's Claude Code session files? If it may, the evidence written to `runs/` should be counts and hashes, not raw commands, because the repo is public. Where that evidence lives needs EJ's agreement.
- If N1 fails (hooks do not load from `--settings`), does EJ want a different sandbox, or does the live arm drop to the replay only?

## Costs and risks
- N1–N3 spend quota: one call each on Claude, Codex, Qwen and opencode, plus dsh if the bridge is mounted for the test. Mounting the bridge may count as config, which is a question for EJ (my #8).
- Transcripts may hold secrets and are the user's private record. They are read locally with bun or Claude only, never sent to another engine, and raw lines never go into `runs/` (my #5; my reading).
- The U3 and N4 labels are hand-made by the main agent, so that check is mine, not independent. A second labeller on a sample would fix that, at extra cost (my #10).
- A dump hook writes stdin to a file, and stdin can contain prompt text or secrets. Write it to `/tmp` scratch and keep only the field names and value shapes as evidence (my reading).
- Doing these before step 4 delays the build by one short step. The price of skipping them is building M1/M5 on payload facts no one has seen fire (my #2).

## How we would know I was right
- Before step 4, there is a marker file per harness showing a fired hook, the recorded payload shapes, and U3/N4 tables listing every miss and every false deny. Each is compared with the prediction written above, whichever way it falls (my #3, #9).
- If N2 shows a payload difference between harnesses and U3's pattern list then needs an adapter per harness, my prediction held. If the payloads are identical, it failed, and I report that with the same weight.
- In step 6, arm B catches the hold-out traps (N5) at a rate written down before the run, against arm A. The single-handler design stands only if this matches what was committed in `prediction.md` (my #4).
