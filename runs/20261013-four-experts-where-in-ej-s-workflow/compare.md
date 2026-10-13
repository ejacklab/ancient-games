# Four experts and Dave — where in the workflow-design method can each give reliable help?

Written by Claude (main session), 2026-10-13. Question: `question.md`. Answers: `answers/`. All five ran on their
designed engines (Linus/Codex, 范蠡/agy — no fallback, 孫子/dsh, 老子/opencode, Dave/Claude subagent).

## The map (✓ = the expert claims reliable help · ✗ = the expert says it is NOT reliable there)

| Method step | Linus | 范蠡 | 孫子 | 老子 | Dave | Count |
|---|---|---|---|---|---|---|
| 3.0 objective, six whys | ✗ | | ✗ | | ✗ | **nobody** — 3 say not reliable |
| 3.1 readiness, blueprint check | | ✓ | ✓ (his #1 place) | ✗ | ✗ | 2 |
| 3.2 write the algorithm | ✓ (his #1 place) | ✗ | ✓ (with 3.3) | ✗ | | 2 |
| **3.3 unclear spots** | ✓ | | ✓ | ✓ (his #1 place) | ✓ | **4** |
| 3.4 size, challenger rule | ✗ | ✗ | ✗ | | ✓ (his #1 place) | 1 — 3 say not reliable |
| **3.5 loops, the check** | ✓ | ✓ | ✓ | ✗ | ✓ | **4** |
| 3.6 graph, run's end, backlog | | ✓ | ✓ (with 3.5) | ✓ | | 3 |
| 3.7 parallel | | | ✗ | ✓ (narrow) | ✗ | 1 |
| 3.8 node mechanics | | | | ✗ | | — |

## The question to ask each, where they are strongest (quoted from the answers)

**3.3 unclear spots — four experts, four different questions (they complement, not repeat):**
- **Linus:** "Which choices depend on missing technical facts, and what would make a mistaken choice reversible?" (#4, #5, #6, #7)
- **孫子:** "Which of the three do we know — that our engines and tools can do it, that the task as posed can be done, and that the ground permits it — and which is only half a victory?" (#4, #1)
- **老子:** "Which [spots] can be answered by giving up the step rather than by resolving it?" (#1, #2)
- **Dave:** "What is the smallest reversible experiment, what do you predict before it runs, and when do we stop?" (#2, #3, #8)

**3.5 the loop's check — four experts:**
- **Linus:** "Could this check pass while the requested result is wrong or an existing user workflow breaks?" (#1, #2, #3)
- **孫子:** "Where is this node's 勢 — the check it cannot edit … and what has been left to the worker's good character?" (#12)
- **范蠡:** "What bounds this loop's attempts before it must exit, and how promptly must it close when the check passes?" (#10, #4)
- **Dave:** "What result would show this check can fail? What is its control?" (#4, #9)

**Single strongest places:**
- **3.1 readiness — 孫子:** "what was actually run, not read; what is sourced to a file or a person" (#17, #2, #11); **范蠡:** wait until tools and EJ's requirements are both ready (#1, #9, #18).
- **3.2 algorithm — Linus:** "Does this algorithm follow the data and solve the immediate problem without unnecessary machinery?" (#9, #10, #13)
- **3.4 challenger rule — Dave:** is the prediction fixed before the run, is the default the control (#3, #4, #5).
- **3.6 run's end — 老子:** diff the acceptance-criteria ids against those fixed before the run; added ones belong in the backlog (#3, #4); **范蠡:** "the plan does not move" — no mid-run scope change (#5, #6).

## Where they agree they should NOT be asked (quoted)

- **3.0 vision and requirements — EJ's.** Linus: "#13 supplies no basis for inventing their vision"; 孫子: "Leave 3.0's vision and requirements to EJ"; Dave: "none of my ten rules is about stating objectives".
- **3.4 numbers — engines, budgets, sizes.** Linus: "no comparative measurements"; 范蠡: "an invented calculation"; 孫子: his #14 force ratio "invites me to fill a missing unit with my own value". (Dave is the exception, and only for checking a challenger's prediction, not for setting numbers.)
- **3.7 nature/swarm analogies — Dave himself:** "Agents are whales, not ants … my #7 says drop the analogy."

## Where they pull against each other (side by side, not averaged)

- **Wait or move.** 范蠡's #1/#9 say 「王姑待之」 ("for now, wait") until conditions are met — and he names the risk: "the workflow could block on harmless ambiguities that a cheap exploratory spike could have resolved". Dave's #2 says run the cheap test; 孫子's #8 (拙速, clumsy speed) also pushes to move. Which applies depends on how costly a wrong start is — 孫子 asks EJ exactly that.
- **Subtract or cover.** 老子's #1 subtracts; he names his own sharpest risk: "my rules reward subtraction, and the method's rules sometimes require addition" — a design judged only by him would drop a criterion nobody volunteered to cover. Pair him with the coverage check, never alone.

## Honesty each showed about itself

- 孫子: his #7 (deception) assumes a reacting enemy; "a workflow's workers are not an enemy" — not to be used at 3.7.
- 老子: two of his items rest on contested words across the manuscripts (#15 不爭/有靜, #8 不知知/不知不知); he named them so they can be discounted.
- Dave: "I would invent thresholds" — his #3 pulls toward writing a number; he must leave EJ's values open.
- Linus: every placement is labelled "my reading", the size of the help "not measured".

## Checks

- `four_experts.py check`: **PASS**, 5 answers, 0 failures (cited items exist; Chinese quotes verbatim from each list).
- Main session verified the method phrases they quoted exist in `docs/WORKFLOW_DESIGN_METHOD.md` / the skill:
  "Run it; do not assume" (line 102, wrapped), "A label is not a node", "must pay for itself", "known to be able to
  fail", "≥20% lower projected run cost", `feedback.jsonl` (DISPATCHER_DESIGN), "Designing is cheap" (skill). Dave's
  ledger counts verified: 18 rows, all `default`, 16 "token cost not measured".
- Not established: that any of this help is real or large — every expert says *not measured*. Linus, 孫子, 老子 and
  Dave each propose a test on the next real design; none has run.
- 老子's answer again starts with stray lines ("I'll read that brief first.").
