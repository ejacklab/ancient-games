# Four experts and Dave — vision, requirements, use cases: which comes first?

Question: `../expert-question-order.md`. Answers: `answers/`. Labels: *quoted* (from an answer), *my reading*, *not measured*.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Answer (one line) | New product: a real user situation, then a minimal vision, requirements, then generated cases; a loop | New system: vision → requirements → cases; an existing, running system: use cases first | Within a pass vision → requirements → cases, strictly; across passes a loop | Write vision → units → cases; **check** in reverse, cases first | Vision is a strict gate; then requirements and cases loop; settle the order by a trial |
| Main items used | #2 #3 #5 #7 #9 #13 | #2 #3 #5 #7 #9 #10 #11 #18 | #1 #2 #3 #4 #12 #13 #17 | #1 #2 #4 #6 #8 #11 #17 | #1 #3 #4 #5 #6 #7 #9 |

## Where they agree (all five unless named)

- **"Use cases first" holds for discovery and breaks for counting.** *Quoted* 孫子: it "holds as discovery before the requirement is frozen and breaks as definition, where the case list sets coverage". The trial is the reason all five cite: the raw count moved 46% → 20% with the prompt, the unit count stayed 80%.
- **The vision is EJ's alone**; an agent only writes down what EJ said.
- **It is a loop, not a one-way line.** A case that exposes a gap goes back to the requirement; the vision changes last, and only when the change touches who it is for or what it will not do (孫子, 老子, Linus, Dave; 范蠡: "the vision remains the invariant temple plan").
- **Units are fixed before a generated case counts** — R11.1 as agreed.
- **EJ's own use cases and AI-generated cases are two different artifacts** (Dave: "two makers at two times means two forms"; Linus: "EJ's existing cases remain their separate artifact"; 范蠡: seeded by EJ, expanded by AI).
- **Each artifact gets a check that can fail before the next is built on it**, shown failing on a planted input — a vision line nobody can deny ("easy to use", 孫子), a requirement clause with no fails-if (the trial's real gap), a case that contradicts a settled decision (the trial's real case).

## Where they disagree (side by side, not averaged)

| Point | Positions |
|---|---|
| **When use cases come first** | Linus: a **new** product starts from "a concrete user situation" before the vision · Dave: a **new** product with only a vision — cases-first for discovery is worth testing · 范蠡: the opposite — on a **new** product generated cases are "speculative noise"; use cases first holds for an **existing, running** system · 孫子: an existing product starts its first pass from its old cases · 老子: never as the writing order; always as the checking order |
| **What closes the loop** | 孫子: a pass adds no new unit and no new fails-if, and every fails-if has a check shown failing · Dave: a round surfaces no gap the previous one did not, or a date fixed in advance (EJ's) · 老子: stop when the remaining uncovered units are those "whose absence nobody can name a loss for" · 范蠡: 80% of units covered · Linus: the artifacts agree, the checks reject wrong results, and EJ has decided the scope |
| **Who writes requirements** | 孫子: the named decider (EJ where EJ decides) · 老子: the agent running the engines, from EJ's words · 范蠡, Linus: a designated worker, with EJ deciding open choices · Dave: not given — asks |
| **How the vision is checked** | 孫子: every line traces to the maker's words · 老子: name a second project — the four lines must still hold there · Dave: plant a requirement that breaks "what it will not do"; it must be rejected · 范蠡: all four parts present, none agent-invented |

*My reading:* the new-versus-existing split dissolves under Linus's distinction. Linus's "holds" case is an **observed** situation EJ writes down; 范蠡's "breaks" case is an AI **brainstorm** on a product with no vision. So: real, observed use cases can come first on either kind of product; AI-generated cases come after the units are fixed.

## What each added that the others did not

- **Linus** — separate an *observed* situation (can precede requirements) from a *generated* acceptance case (cannot); and the three-musts rule fails the requirement check: a MUST for a method breaks the house rule, and nobody is named to decide when each is ready.
- **范蠡** — the new-versus-existing test: on a running system, measure what it does before codifying rules.
- **孫子** — "Nothing revises from vision straight to cases without the requirement in between"; a vision is not ready if no one but EJ can fail its check.
- **老子** — two orders, not one: write forward (vision → units → cases), check backward (a planted wrong case must fail at all three levels).
- **Dave** — EJ's own practice starts from a requirement ("I get requirement, I will gen use cases"), so "first" may mean most important, not earliest; a two-arm trial with metrics fixed in advance.

## What they need to know (merged, for EJ)

1. **By "use cases", do you mean real situations you write, or AI-generated cases?** The answer decides most of the disagreement.
2. **"First" in time, or first in importance?** (Dave)
3. **New products, existing ones, or both?** (范蠡, 孫子, Dave)
4. **"Must"** — a gate that stops work, or SHOULD? The house rule allows MUST only for a safety bound (Linus, Dave).
5. **Who writes the requirement text and its units?**
6. **What closes the loop?** 孫子's "a pass adds no new unit and no new fails-if" is the only one that can be checked without a judgement call (*my reading*).
7. **An order trial** — two arms on one to three requirements (Dave, 孫子, 老子). A paid engine call.

## Check

- `four_experts.py check`: **PASS, 5 answers, 0 failures.** `--sabotage`: 2 failures, as required. The check shows answers cite their own lists; not that the rules were applied well (written by Claude).
- Engines (`status.json`): linus codex gpt-6.1-sol 80 s · fan-li agy gemini-3.8-flash-medium 136 s, no fallback · sun-tzu dsh deepseek-flash 84 s · lao-tzu opencode MiniMax-M3.1-Flash-Preview 58 s · Dave a Claude subagent.
- 老子's answer again begins with a stray line ("I'll read that file first."). 老子 says the trial "does not report" unattached cases; `coverage-trial/results.md` does (the "Cases that fit no unit" table).
- All five read the same brief and the same n=1 trial, both from the main agent; their agreement leans on that trial.
