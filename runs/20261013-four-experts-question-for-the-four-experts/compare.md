# Four experts and Dave — how to fix the evaluator's 20 review findings

Labels: *quoted* (from an answer), *my reading* (the COO's).

## The answers

| | Linus (Codex) | 范蠡 (agy) | 孫子 (dsh) | 老子 (opencode) | Dave, the control (Claude) |
|---|---|---|---|---|---|
| Answer, one line (*quoted*, shortened) | "Fix false proof and unsafe run handling first, then blindness and requirement coverage, then repair behaviour and reporting" | "steadying what is tilting (F1, F5, F4, F3), then … borders (F12, F10, F8, F2, F11), then … runners and loop boundaries (F9, F6, F7)" | "Fix what lets it lie before what lets it miss … F9 last" | "first every place where *nothing there* is read as *something good there*"; "leave F6, F7, F2, F8, F9 for a decision" | "four rounds … defer F6, F7, F13, F16, F17's model check and F18"; "Do F5 and F4 the guarded way I measured" |
| First fixes | F1, F12, F10, F11, F5, F4 | F1, F5, F4, F3 | F1, F5, F3 | F3, F1, F5, F17 (`done: false`), F11 | F1, F5, F4, F19, F10 with F12, F11 |
| Main items cited | #2, #5, #9, #10, #13 | #2, #5, #10, #14, #18 | #2, #3, #5, #6, #16, #20 | #1, #6, #7, #8, #12, #13, #14 | #1–#10 |

## Where they agree

- **The false-PASS paths come first:** F1 and F5, in all five; F3 and F4 in four of them.
- **Every fix ships with a test that fails when the fix is undone.**
- **F9, sandboxing, is the riskiest and the hardest to really close.**
  - Linus: "report F9 unresolved" if isolation cannot be enforced.
  - Dave: "detection only".
  - 孫子: narrow it, "rather than skip it".
- **Expect more UNKNOWN results:** the numbers get worse before they get better.

## Where they disagree (side by side; not averaged)

- **F6 and F7 (the missing repair and rerun loops):**
  - Linus and 范蠡 put them later, inside the plan.
  - 老子 and Dave defer them, since both end in UNKNOWN, the safe direction.
  - **EJ has decided: all 20.**
- **F2 (the plant leak):**
  - Linus: keep the plant's identity in "coordinator-only state".
  - Dave measured that on this product, which has only one judged case, the fix cannot be observed, and that
    `plants.json` stays readable, so it "narrows the leak but does not close it".
- **F10 (a reused runId):** Linus and Dave refuse a reused runId; Linus also allows a deliberate reset. Refusing is
  the shared default.

## What each added that the others did not

- **Dave (measured):** the obvious F4 fix breaks 3 frozen tests and the strict F5 fix breaks 4; the guarded versions
  pass. Replaying the 10 recorded runs, the F1 and F5 fixes change 0 cases, so each needs a fixture of its own.
- **老子:** F4 "is two findings wearing one number"; for F8, "list everything a blind copy can see" before choosing
  what leaves.
- **Linus:** F12 before F10, so cleanup cannot escape its folder; F11's validation before F5 changes the meaning of
  results.
- **孫子:** rank by "what a defect breeds, not by its size"; F4 and F11 make one fail-closed rule.

## What they need to know (merged, for EJ)

- **May DATA.md change?** An optional key recording why a mutant run went red, and a missing `restored` meaning "not
  restored". *My reading:* yes. DATA.md is the COO's interface detail, and these changes add to it.
- **F9:** no OS-level isolation exists here. Everything beyond scoped folders and a write sandbox is narrowed, not
  closed.
- **K2's fault list** lives in session scratch. It needs a home the workers cannot read, so K2 can be rerun after the
  fixes.

## Check

- `four_experts.py check` (written by Claude): 5 answers, 1 failure.
  - 老子 wrote 以約為紀 where the list has 以約爲紀. That is a one-character script variant, not an invented quote.
- **Engines:** Linus on Codex, 范蠡 on agy (no fallback), 孫子 on dsh, 老子 on opencode, all exit 0; Dave on a Claude
  subagent.
- **What the check does not establish:** that the advice is right.
