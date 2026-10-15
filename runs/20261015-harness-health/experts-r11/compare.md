# Four experts and Dave — review the eleven harness requirements (R1–R10, R11.1, R11.2)

Question: `../expert-question-r11.md`. Answers: `answers/`. Labels: *quoted* (from an answer), *my reading*, *not measured*.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Answer (one line) | Keep the intentions; every verdict must state what was tested; readiness proves prerequisites only | Split engine duties from orchestrator duties; replace file checks with active probes that can fail; count R11 at step 2 | Readiness *labels* the lines, does not verify behaviour; change 7, split 3, drop none; don't enforce 80% yet | R11.2 is the spine; 80% a report, not a gate; add a check on the call itself | Config is not health; a result check per dispatch carries the weight; replay the 7 to test it |
| Main items used | #1 #2 #3 #5 #7 #9 #13 | #1 #3 #7 #9 #14 #18 | #1 #2 #7 #11 #14 #15 #17 #19 | #2 #4 #6 #7 #8 #14 #17 | #1 #3 #4 #5 #8 #9 #10 |

## Where they agree (all five unless named)

- **The built check measures the wrong ground.** All seven recorded failures are behaviour at dispatch; config rows cannot catch them. *Quoted* 孫子: "it is measuring the wrong ground". *Quoted* 老子: "0 of 7 flagged is therefore not a defect in the thresholds; it is the shape of the instrument."
- **R11.1's placement as proposed:** readiness lists the judges; the share is counted after step 2.
- **Q2: a design-standard document alone is not a judge.** It counts only with something that applies it and can return fail (Linus: a human may apply it; Dave and 孫子: shown failing on a planted violation).
- **Q1 leans to acceptance criteria** — Linus, 范蠡, 老子 recommend it; 孫子 prefers it as *my reading* but says the deciding fact is EJ's ("which failure is the 80% meant to catch?"); Dave is conditional (if prompts, a prompt counts only when every one of its criteria has a judge). All say: count both ways on past designs to see whether it matters.
- **The list misses a check on each dispatch's result** — exit 0 is not success; output must exist, be non-empty, and be the kind asked for. Dave N1, Linus N1, 范蠡 N2, 孫子 N1, 老子 N1 + N2 (form). Said to catch failures 3, 4, 5, 7.
- **Dispatch preconditions / a trap lint per engine** (stdin, concurrency, write policy, plan mode) — Dave N2, Linus N2, 范蠡 N1, 孫子 N2 + N6. Said to catch 1, 2, 3, 5, 7.
- **R6 is the one MUST candidate** (a safety bound) — Dave, 孫子, 老子; Linus "a specific safety boundary may warrant MUST". EJ's call in every answer.
- **Replay the seven recorded failures as planted inputs** — costs no quota — before R11.2 or any new check is trusted.
- **R3 (and the design half of R7, R8) belong at step 2**, not readiness.

## Where they disagree (side by side, not averaged)

| Point | Positions |
|---|---|
| **80%: gate or report** | 老子: "make the number a report, not a gate" until there is a sample · 孫子: "keep it as a target measured over runs, not a gate" · Dave: count past designs first, "otherwise we cannot tell whether 80% binds anything" · Linus: after EJ settles the unit, "fail … coverage below the agreed threshold" · 范蠡: count at step 2, gate implied |
| **May readiness run things** | 范蠡: active probes at readiness — write/read/delete a marker file, run the workspace reset command, try a forbidden action · Linus: "a harmless local enforcement probe", else report configuration only · 孫子: asks EJ whether readiness may run the harness at all · 老子: readiness "must stay cheap … gets out of the way" |
| **R5** | Dave: merge into R11 (R5 becomes the list of judges) · Linus, 范蠡, 老子: split (mechanical judges at readiness; evaluator agent at run time) · 孫子: keep |
| **R10** | Linus: "Drop the automatic permanent-fix clause" · 范蠡: proven fixes must become permanent rules · Dave: each recorded failure has a check shown failing — today 0 of 7 · 老子: add the missing half, each requirement carries its own withdrawal condition · 孫子: keep, every failure links to a fix shown failing |
| **List size** | 老子: "one existing row must go" for the N-items, and does not choose which · 孫子: drop none, adds eight N-items · Dave: grows to about 14 lines |
| **R11.2's first check** | Linus alone: passing it does not establish acceptance, and a first-check rejection must show a real acceptance failure, "otherwise a cheap but unreliable filter can discard good work" · the others keep R11.2 as drafted |
| **Predicted catch on the replay** | Dave: N1 + R11.2 + N2 flag at least 6 of 7 · 范蠡: at least 5 of 7 · 老子: the R11.2 first signal must fail all 7 · Linus, 孫子: must beat 0 of 7 |

*My reading:* 范蠡's R7 probe ("run the workspace reset/clean command, and assert zero git diff") would discard uncommitted work in a real checkout; it is not safe as written. His R1 check asks for a "threshold bound" nobody has given — the house rule leaves that to EJ.

## What each added that the others did not

- **Linus** — the eight requirement checks run on the supplied list (R1, R5, R6, R7, R10 fail *one thing*); evidence tied to the setup it tested, stale when engine version, directory or mode changes (N3); safety boundaries never inside the 20% the 80% allows to be unjudged (N4); first-check false rejections.
- **范蠡** — the line between what the engine owns and what the orchestrator owns (N3); a zero-quota "dispatch channel" probe.
- **孫子** — each label (`unknown`, `MISSING`) needs a prescription for what work may be sent (N4); spend authority per dispatch (N5); the meta-rule that every check is shown failing once (N7); name who wrote the check (N8).
- **老子** — R11.2 as the spine with R1–R10 hanging off it; no rolled-up "healthy" total over `unknown` harnesses; retry only after a judge returns a retryable verdict, since a retry on an unjudged result hides the failure.
- **Dave** — a dated prediction for the replay; start the result check on the agy path (3 of 7 failures); re-score the check against the failure log every time it changes (N5). His N6 (no secret in the report) is already built: `tests/test_harness_health.py` HH-03 plants two secrets and asserts neither prints.

## What they need to know (merged, for EJ)

1. **Q1** — count over prompts or acceptance criteria? Four lean criteria; the deciding fact is which failure the 80% should catch.
2. **Q2** — confirm: a standard counts as a judge only with something that applies it and can return fail.
3. **80%** — a gate, or a reported count until past designs give a sample?
4. **Add the result check per dispatch** (all five) and **dispatch preconditions** (four)? **A deadline per dispatch** (Dave, 孫子)?
5. **R6 (and R8) as MUST?**
6. **May readiness run local, no-quota probes** (the test command, `--version </dev/null`, a scratch-file write) — or read files only?
7. **R10** — keep, drop the permanent-fix clause, or add a withdrawal condition per requirement?
8. **What do `unknown` and `MISSING` permit** — a gate or a report?
9. **Budget for a resume drill or denial probe** that spends a session (needs your go-ahead).

## Check

- `four_experts.py check`: 2 failures, both 老子 writing 以深為根 / 以約為紀 where the list has 爲 — a variant character, not an invention (same as the first round). `--sabotage`: 2 failures, as required. `check.txt`, `check-sabotage.txt`. The check was written by Claude; it shows answers cite their own lists, not that the rules were applied well.
- Engines (`status.json`): linus codex gpt-6.1-sol 134 s · fan-li agy gemini-3.8-flash-medium 154 s, no fallback · sun-tzu dsh deepseek-flash 108 s · lao-tzu opencode MiniMax-M3.1-Flash-Preview 114 s · Dave a Claude subagent.
- 老子's answer begins with a stray line ("I'll read the brief first.") before its title; the five sections are present.
- All five read the same brief, written by the main agent, including the main agent's 0-of-7 backtest — their agreement on it is not independent evidence for it.
