# Four experts and Dave — plan and design a harness-health extension to readiness

| | Linus (Codex) | 范蠡 (agy) | 孫子 (dsh) | 老子 (opencode) | Dave (control, Claude) |
|---|---|---|---|---|---|
| Answer (one line) | Compare effective capability with the task's stated need; keep config evidence, behaviour evidence and EJ's acceptance apart | Separate companion script; measure, never auto-fix; weak harness → stricter external Guard | A weighing layer, not a second inventory; verdict only where the probe is strong | Ten requirement rows, not sixty; help names file+key+snippet and stops; no total grade | One harness, one requirement first; backtest against the 7 recorded traps; predict config probes catch ≤2 of 7 |
| Main items used | #2 #3 #5 #7 #9 #13 | #3 #12 #14 #15 #18 | #1 #3 #4 #11 #14 #16 #19 | #2 #4 #8 #13 #14 #17 | #1–#10 |

All labels *quoted* unless marked *my reading*.

## Where they agree

- **U4 — a separate `harness_health.py` beside `readiness.py`, same `Probe` shape and four statuses.** All five.
- **U2 — help is advice + snippet; the script never edits harness config.** All five. Dave, Linus and 孫子 add: a snippet
  must be shown to work (Dave's "flip test": applying it to the bad fixture turns the finding to pass).
- **U6 — read only keys verified against the installed version; everything else `unknown` with the reason.** All five.
  孫子 and 老子: record the version each probe was verified against.
- **U1 — list every harness found; `--harness` narrows the verdict.** Linus, 范蠡, 老子, Dave agree; 孫子 "modify"
  (verdict only on dispatched harnesses) — the same mechanism, *my reading*.
- **A planted fake secret must never appear in the output** (markdown and JSON). Dave N4, 孫子 N4, 老子 #13.
- **`dsh` and `opencode` go into readiness first** — the measured gap. Dave N2, Linus, 孫子 step 2.
- **"Covered by <gate>" only if the gate file is found** (U7). Dave, 孫子, 老子; Linus goes further (below).
- **Every check shown failing on a planted wrong input** — all five.

## Where they disagree (side by side; not averaged)

- **U3 — what may be judged.**
  - 孫子, 老子, 范蠡: pass/fail where a concrete named thing is present/absent; numbers reported without verdict.
  - Linus: *"Concrete-looking settings do not automatically justify pass/fail. Compare effective behavior with accepted
    task requirements"*; presence of a deny list does not establish enforcement.
  - Dave: health lines are comparisons — *"changed since", "worse than" the control, or "absent"* — never a number alone.
  - 老子: *"report the number **and** where its comparison value lives; if that place does not exist, the line is
    `unknown`"*.
- **U5 — the "Found → effect on the design" table.** 范蠡, 孫子, 老子: write it into method 3.1 now. Dave: *"defer …
  until then mark it n=0"*. Linus: keep it but make effects *"specific to dependent work"*.
- **Config precedence.** 范蠡 (*my reading*): project settings take precedence over user settings. Linus: establish
  effective precedence across defaults, config, profiles, launch flags. (Main agent's note: for Claude Code a `deny` in
  any scope applies — 范蠡's "project replaces user" reading is not right for deny rules; not verified here.)
- **Scope of the first build.** Dave and Linus: one harness slice first, then scale. 范蠡, 孫子, 老子: all ten
  requirements in one script, ordered build.

## What each added that the others did not

- **Linus:** presence ≠ enforcement — config evidence, behaviour evidence and EJ's acceptance are three different
  records; a missing key may mean a documented default applies, not a failure.
- **范蠡:** R5 as "at least two distinct verified engine kinds", so reviewer ≠ builder is possible.
- **孫子:** the checker's own five faults (hard-fail on weak evidence, never fail, any difference an error, flood,
  so many warnings they cannot be used); verdict strength must match probe strength.
- **老子:** ten rows, not sixty; no overall grade; measure readiness's wall time before and after.
- **Dave:** the backtest — of the seven recorded harness traps only two are config-dependent (opencode allowed paths,
  agy allow-rules); five are behaviour seen only at dispatch. So the "help" worth most may be a trap memory, not more
  config keys. Opt-in `--canary` (N1) is the only way to see behaviour traps at readiness.

## What they need to know (merged, for EJ)

1. **Block or inform?** Does a health finding stop dispatch (exit 1) or only inform the design? (Linus N1, 范蠡 N2,
   孫子 N1, 老子 N1.)
2. **Opt-in canary?** May readiness spend a little quota behind a flag to catch behaviour traps? (Dave N1, Linus N2.)
3. **Where do comparison values live**, if EJ wants any (instruction-file size, etc.)? (老子 N2/N5, Dave, 范蠡 Q1.)
4. **Is "no deny list" a finding?** Requirement 6 names "hard policies", not a deny list. (Dave, Linus.)
5. **Drift** against the previous health output — wanted, and where is it stored? (Dave N5, 老子 N8.)
6. **Trap catalogue** — a file passed by flag, project-owned? (Dave N3.)

## Check

`four_experts.py check experts`: 5 answers, 2 failures — both 老子 quoting 以深為根 / 以約為紀 where the list has
爲 (one variant character each; a script variant, not an invention). `--sabotage`: 2 failures reported, as required.
The check was written by Claude; it establishes citations and sections, not that a rule was applied well.
Engines (status.json): linus codex gpt-6.1-sol 212 s · fan-li agy gemini-3.8-flash-medium 135 s (no fallback) ·
sun-tzu dsh deepseek-flash 97 s · lao-tzu opencode MiniMax-M3.1-Flash-Preview 69 s · dave Claude subagent.
