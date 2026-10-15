# 孫子 (Sun Tzu) — a health check that makes the workflow unbeatable before it moves

## Answer

Build it as a **weighing layer, not a second inventory**: a separate `harness_health.py`, sharing readiness.py's `Probe` shape and statuses, that reads only facts a command has just proved, weighs each condition against the harnesses this design will actually dispatch to, and returns per-condition *present / absent / unknown* plus a **help** line that names the exact file and key. Pass/fail only where the requirement names a concrete thing; otherwise report the measurement and give no verdict; the help never edits a config file (an auto-edit is the siege). Build in the source's own order — measure, count, weigh, decide — and ship the small check that can fail before the broad one.

## How I decided

1. A readiness check is a temple reckoning, not a status report. My #1: `quoted` 「夫未戰而廟算勝者，得算多也；未戰而廟算不勝者，得算少也。多算勝，少算不勝，而況於無算乎？」 The extension's job is to raise the count before the workflow commits, and to compare, not to score.

2. The order of building is given by the source, not chosen by me. My #1: `quoted` 「地生度，度生量，量生數，數生稱，稱生勝」 — probe the ground, count, weigh, then derive the design effect. I use this as the build order below.

3. The purpose is to be unbeatable, not to predict. My #2: `quoted` 「昔之善戰者，先為不可勝，以待敵之可勝」 and 「無恃其不來，恃吾有以待之」. A green harness is never a guarantee that nothing will go wrong; it is only the part we own.

4. What may be judged is set by what we know of both sides. My #4: `quoted` 「知彼知己，百戰不殆；不知彼而知己，一勝一負」. A status that only a local file claims is "knowing yourself but not them" — a half-victory, and it must be labelled that way.

5. A config key may not be inferred. My #11: `quoted` 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也」. Do not borrow a key name from another harness by analogy ("不可象於事"); a probe reads only what has been verified against the installed version, or it is `unknown`.

6. The probe ladder is also given. My #17: `quoted` 「故策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處」 — from indirect reckoning to actual contact. Use the cheapest rung that genuinely verifies; do not jump to contact when reckoning will do.

7. Strike where the ground is certain. My #10: `quoted` 「水因地而制行」 and 「兵之勝，避實而擊虛」 — shape the probe to the installed version, avoid the config shapes nobody has verified.

8. The strength of the verdict must match the strength of the probe. My #14: `quoted` 「十則圍之，五則攻之…不若則能避之」 and 「故兵非貴益多也」. Hard-fail only where the probe is strong and the requirement names a concrete thing; a weak probe may report but must not fail; do not add checks for their own count.

9. The help is ranked by cost. My #3: `quoted` 「上兵伐謀，其次伐交，其次伐兵，其下攻城」 and 「攻城之法，為不得已」. Advice naming the setting is *plans*; a ready-to-apply snippet is *alliances*; a script that edits the config is the *walled city* — and my #3 opens `quoted` 「全國為上，破國次之」.

10. The help must change the condition, not the person. My #12: `quoted` 「故善戰者，求之於勢，不責於人」.

11. A failing condition must not corner the workflow. My #18: `quoted` 「歸師勿遏，圍師必闕」 — always leave a gap: a path, an exception, or the snippet.

12. The check must be answerable before it commands. My #16: `quoted` 「約束不明，申令不熟，將之罪也」 — an unclear criterion is the check's fault; and `quoted` 「厚而不能使，愛而不能令…譬若驕子，不可用也」 — a check that only shows green cannot command. This is the house rule "every check shown failing once."

13. The checker has faults too. My #15: `quoted` 「凡此五者，將之過也，用兵之災也」. A health check can be set on dying (hard-fail on weak evidence), set on living (never fail), quick to anger (any difference is an error), over-clean (floods the reader), or loving the people (so many warnings they cannot be used).

14. The output shape is a table from condition to response. My #19: `quoted` 「是故散地則無戰，輕地則無止…死地則戰」 and 「九地之變，屈伸之利，人情之理，不可不察也」. That is exactly U5's "Found → effect on the design" table.

15. Price it, and prefer the quick working thing. My #8: `quoted` 「故兵聞拙速，未睹巧之久也」. My #6: `quoted` 「是故智者之慮，必雜於利害」 — every check states its harm. My #5: `quoted` 「非利不動，非得不用，非危不戰」 — no check without advantage.

16. Judge a harness by structure and what it breeds, not by declaration. My #20 (`attributed`, the 〈吳問〉 dialogue, quoted in the list): the houses that fell had full coffers and many officials; Zhao held because its structure bred frugality. My reading: read what the harness records and enforces, not what its config says it intends.

### Verdicts on U1–U7 (and new spots)

- **U1 — modify.** Give the verdict only on the harnesses this design will dispatch to; list all found as inventory. My #14 (`兵非貴益多也`: numbers are not valued for their own sake) and my #8 (speed). `--harness` narrows the verdict; the full list stays as inventory, not judgement.
- **U2 — agree, and rank it.** Advice naming the exact file and key first, a ready-to-apply snippet second, no auto-fix at all. My #3 and #12. An auto-edit trades the whole (a working harness) for one broken condition.
- **U3 — agree, and tighten it.** Pass/fail only where the requirement names a concrete thing (a deny list exists, a sandbox mode is set, a hook is installed). Elsewhere, report the measured number and give no verdict. My #1 (a reckoning is a comparison) and my #14 (verdict strength = probe strength). "Short" and "fast" are thresholds; do not supply them.
- **U4 — agree.** A separate `harness_health.py` with README's `Probe` shape and the four statuses; readiness stays the inventory. My #3 (keep the whole) and #10 (strike the empty — add a probe set, do not rewrite readiness). My #13: do not retake the roads readiness already drove; reuse its probes.
- **U5 — agree.** A "Found → effect on the design" table in method 3.1, the way the information-check table works. My #19 (name the ground, prescribe the response) and my #1 (the weighing gives the victory). Example effects: no explicit sandbox → Guard stakes rise; only one verified engine kind → the reviewer must be a script check, because a different-kind reviewer cannot be stood up (my #4).
- **U6 — agree strongly.** A probe reads only what has been verified against the installed version; everything else is `unknown` with the reason. My #11 (`不可象於事`: no borrowing by analogy) and my #10 (avoid the solid). Record the version the probe was verified against, so a later version change turns it `unknown`, not wrong.
- **U7 — do not decide this; it is EJ's.** I would not drop requirements 2, 3, 7: list them as `reported`, "covered by `<gate>`", and ask EJ to confirm that disposition. But my #4 says a coverage claim nobody verified is "knowing yourself, one win one loss", and my #11 forbids inferring coverage by analogy — so add one cheap path check that the named gate actually exists, which is verifiable. My #13: not every road is taken, but the one left untaken is named.

- **N1 — who holds the verdict?** Does `harness_health` gate dispatch, or only inform the design? This changes the exit code and the owner. My #19 (prescribe the response) and my #16 (orders clear first). Question for EJ.
- **N2 — per design or per engine?** Run once at readiness, or per node at dispatch? My #14 and #8. My reading: once per design; re-check only the engine being dispatched to.
- **N3 — may `reported` be good enough for a high-stakes node?** My #2 and #4: a pass rested on a file claim is a half-victory. Which nodes require `verified` is EJ's to set.
- **N4 — how is "never prints a secret" proved mechanically?** My #16 (a check shown failing) and my #11 (pay for the knowledge). It needs a fixture with a planted fake key, and an owner.
- **N5 — what is the unit of a finding?** One condition, or one harness? My #15 (six defeats from one weak part). My reading: one condition, so a weak probe cannot bring down the whole reckoning.
- **N6 — who re-verifies a config key when a harness updates?** My #11 and #20. My reading: the check records its verified version and turns `unknown`; re-verification is a named step with an owner, not a silent retry.

### The design I would build

One `harness_health.py`, same `Probe` shape and statuses as readiness.py, output appended as a **Harness health** group plus a per-harness reckoning. Each line: condition, status (`verified` / `reported` / `unknown` / `MISSING`), the command or path that proved it, and a `help` line. One condition per finding. Proposed dispositions for the ten requirements (U7's dispositions still need EJ):

| # | Requirement | Owner | Check (read-only unless noted) | Verdict | Help |
|---|---|---|---|---|---|
| 1 | Clear context | harness | instruction files exist per harness, and any pointer's target exists | present / absent | name the missing file and its canonical path; report the line count with **no** "short" verdict |
| 2 | Tools | run | dispatcher adapters with pinned flags present | `reported`, covered by dispatcher | none |
| 3 | Plan structure | run | `design_gate.py` / method present for this run | `reported`, covered | none |
| 4 | State & memory | harness + run | run `state.md` and memory dir exist; a temp write-and-remove proves writability | present / absent | name the path |
| 5 | Independent verification | harness | is there a verified engine kind different from the builder's? | a named consequence, not a number | name the kind to verify |
| 6 | Guardrails & permissions | harness | sandbox mode explicit? deny list present? approval policy explicit? hooks installed? | present / absent / unknown | snippet naming file + key; the person applies it |
| 7 | Recovery | run | dispatch timers and bounded repair present | `reported`, covered | none |
| 8 | Human gates | harness + run | harness approval flag explicit; Guard approvals named | present / absent / unknown | name the key / the owner |
| 9 | Observability | harness + run | harness log path exists and was written this run; `runlog` / `events.jsonl` present | present / absent | name the missing log or flag |
| 10 | Feedback loop | harness + run | a hook is installed (e.g. `UserPromptSubmit`); why-chain skill path and ledger exist | present / absent | name the hook to install |

Where it lives (U4): beside readiness.py, reusing its `Probe` class and status vocabulary, called by readiness or run standalone; exit codes mirroring readiness. It must never print a secret — config files may hold keys — and it must never write a harness config. Evidence and the new tests live in the skill's test tree and `runs/<run-id>/`.

### Build order, each step with the check that can fail

1. **Frame (度).** Write the disposition table: each requirement is harness-owned, run-owned, or unknown. *Check that can fail:* a test that fails if any requirement has zero or two dispositions; sabotage — delete one row, the test fails. (my #1, #13, #16)
2. **Measure (量).** Add the two missing probes, `dsh` and `opencode` `--version` — the known gap — and nothing else. *Check that can fail:* remove or fake the binary and the status flips to `MISSING`; a self-test plants a fake executable returning a version. (my #4, #8, #17 at the reckoning rung)
3. **Count (數).** Add the read-only config probes (permission allow/deny, sandbox mode, approval policy, hooks, instruction files, log path), each reading only keys verified against the installed version. *Check that can fail:* `--self-test` points HOME at a fixture with one known-good and one known-bad config; each probe must go present on good and absent on bad. (my #2, #14, #16)
4. **Verified-or-unknown (形).** Store, per probe, the harness version it was verified against; on a different version emit `unknown` with the reason, never a guess. *Check that can fail:* a fixture with a changed version must yield `unknown`; sabotage — a stub that returns `absent` under a changed version makes the test fail. (my #11, #10, #6)
5. **Weigh (稱).** The comparison layer and the "Found → effect on the design" table (U5). *Check that can fail:* a fixture with no deny list yields the named effect (Guard stakes rise); a fixture with only one verified engine kind yields the "script reviewer" effect. (my #1, #19, #4)
6. **Help (勝).** One help line per finding, naming file + key and a snippet; a hard test that no harness config file changed. *Check that can fail:* run against a fixture and assert the config bytes and mtime are unchanged; assert every finding carries a snippet; sabotage — a stub that writes makes the test fail. (my #3, #12, #18)
7. **Examine the checker (察).** `--self-test` plants one wrong input per check and shows it failing; document the checker's own five dangers. *Check that can fail:* the sabotage suite itself fails if any check passes its planted wrong input. (my #15, #16, #6)
8. **Wire and price.** Call it from readiness / method 3.1; record the unknowns and the run's cost. *Check that can fail:* an end-to-end run on this machine reproduces the observed facts (no `permissions.deny`; no top-level `sandbox_mode`) and the method 3.1 table names the resulting effects. (my #8, #5, #19)

## What I need to know

- Which harnesses this design will actually dispatch to, and whether EJ wants the list-all inventory (U1).
- The config key names and formats for each installed version (U6), or who is authorised to verify them.
- Whether `harness_health` may change any state — a temp file for the writability probe, a `--net` probe — and where its output is kept.
- Whether the verdict gates dispatch or only informs the design (N1), and which nodes require `verified` rather than `reported` (N3).
- Who applies the help snippet, and whether each snippet gets a worked example (N6, N7).
- Whether the ten requirements are binding or only input; the brief says input, and I have treated them as reckonings to test, not a standard.
- For "short instruction file": is any verdict wanted at all? If so, EJ supplies the comparison; I will not invent the number (my #14, house rule).

## Costs and risks

- Building all ten requirements before shipping is a long war; the quick working version risks later rework. (my #8)
- Keeping configs whole means a bad harness stays bad until a person applies the snippet — the price of not sacking the walled city. (my #3)
- Verified-only probing yields many `unknown`s: honest, but incomplete, and the missing verification is real work. (my #11)
- Reporting without a verdict returns the decision to EJ on every run, every time. (my #14)
- The checker's own faults can make it hard-fail on weak evidence or stay all green. (my #15)
- Each added check is upkeep across harness versions, and a version change can silently turn it `unknown`. (my #6, my #11)
- A green harness can be read as a guarantee it is not; if the report is taken that way, we have deceived ourselves. (my #2, my #7)
- Changing conditions rather than people can turn the human into a patch-applier; snippets must be tested, or the help is an unclear order. (my #12, my #16)

## How we would know I was right

- On a fixture where `permissions.deny` is removed, the check emits a named finding and a snippet, and the config file's bytes are unchanged — a test, not a promise.
- On this machine the output reproduces the observed facts: `~/.claude/settings.json` has an allow entry and no deny list; `~/.codex/config.toml` has no top-level `sandbox_mode`; `dsh` and `opencode` now appear (verified or `MISSING`); and method 3.1's "Found → effect" table names the resulting effects.
- Every check is shown failing once on a planted wrong input before it is trusted — my #16's `quoted` 「約束不明，申令不熟，將之罪也」 applied to the checker itself.
- The reckoning is falsifiable: a run against a harness with an actually unsafe config must come out behind one with the sandbox and deny list set — my #1's `quoted` 「多算勝，少算不勝」 as a test, not a slogan.
