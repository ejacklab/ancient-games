# Four experts and Dave — EJ's direction: use cases must, requirements should

Question: `../expert-question-direction.md`. Answers: `answers/`. Labels: *quoted* (from an answer), *my reading*, *not measured*.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Answer (one line) | Holds for discovery; breaks if writing a requirement makes it binding, or if counting cases replaces fixed units | Holds when EJ anchors and the AI completes; two records; a settled requirement is followed | Holds as a loop on EJ's vision; "must" does two jobs; each accepted use case needs a written fails-if | Holds at steps 2–3; breaks at step 4 — the requirement is the comparison, not a detail document | Core holds; three breaks; test the denominator on the existing lists before writing the rule |
| Main items used | #2 #3 #5 #7 #9 #11 #13 | #2 #3 #5 #7 #10 #11 #14 | #1 #6 #8 #10 #11 #15 #16 #19 | #2 #3 #7 #8 #10 #12 #13 #14 #16 #17 | #1 #2 #4 #5 #6 #7 #8 #9 #10 |

## Where they agree (all five unless named)

- **Steps 1–2 hold:** EJ writes the basic use cases, the AI suggests more, EJ decides. It matches the earlier split between an observed situation and a generated case.
- **T1 is not a contradiction.** "Requirements are SHOULD have" is about whether one has to *exist*; "must follow" is about whether a result has to *obey* one that does. All five read it that way.
- **T3: two records.** The AI's suggestion list and EJ's accepted list are different artifacts with different makers (Dave, 范蠡 "AI Suggestion Docket / Accepted Scope Register", 老子, Linus "authorship and approval are different acts"). 孫子 calls it one maker (EJ) and one lever (the AI) — provided the suggestion is recorded as input, which is the same two records.
- **T2: the main agent's reading is half right.** EJ's acceptance fixes *which* cases are in, not *what one case counts as*. *Quoted* Linus: "one accepted case covers exporting CSV and JSON … that is 0/1 cases passed. Split the same scope into two accepted cases and it becomes 1/2. The product has not changed." The fix all five give: each accepted use case carries a written condition for what makes a result wrong (its fails-if), and the count runs over those, frozen before counting.
- **With no written fails-if, report no percentage.** *Quoted* 孫子: "the honest output is 'no measurement', not a percentage" (Linus: "do not silently label a use-case percentage as R11.1 coverage").
- **"Use cases are must" as a MUST conflicts with the house rule** unless it is a safety bound. Dave and 老子 suggest the wording already agreed in R12.4: *a result that fails an accepted use case is wrong*.

## Where they disagree (side by side, not averaged)

| Point | Positions |
|---|---|
| **Level of "results valid for use cases"** | 孫子: MUST — a validity bound, and following a requirement is MUST because it "details" a use case · 老子: SHOULD — only a safety unit earns MUST · Linus: a level belongs to each rule, never to a document type · 范蠡: a settled requirement is binding in execution · Dave: drop the label, write what makes a result wrong |
| **Are requirements "details"?** | Linus: no — some cut across every case: "exporting a report succeeds, but includes another user's private rows. A successful ordinary example does not establish that an access constraint holds." · 老子: no — the requirement *is* the comparison a case is held against · 孫子, 范蠡: yes, details of a use case |
| **When a requirement must be written** | 孫子: when a use case's fails-if cannot be written from its own text · 老子: the fails-if must always exist; the document stays optional · Linus: when a constraint spans cases |
| **When AI-suggested requirements bind** | Linus: only once EJ accepts them — "an unaccepted proposal … cannot justify a product change" · the others do not separate this |
| **Which wins when an accepted use case contradicts a requirement** | Dave raises it; nobody answers it; 孫子 implies the use case wins (a requirement details a use case) |
| **Bounding the AI's suggestions** | 范蠡: a cap on suggestions per round, EJ's number · 孫子: one generator pass; a second that adds no defect is waste · Dave: anchoring and fatigue on 200 items · 老子: count declines — "an acceptance that never declines is not a check" |

## What each added that the others did not

- **Linus** — the granularity counterexample; cross-cutting requirements (privacy) are not details; an acceptance applies to one version, so an edited requirement needs a new acceptance.
- **范蠡** — names for the two records; an intake gate that fails a suggestion entering the count without EJ's mark.
- **孫子** — a rule for when a requirement is needed; the AI cannot know settled decisions from the vision and use cases alone, so where are settled decisions recorded?
- **老子** — the decline count as the check on acceptance; re-read the accepted list at the end of a task so no case vanishes silently.
- **Dave** — a test that needs no engine call: EJ accepts blind from the trial's existing 28 and 200 lists (`../coverage-trial/out/`); if the two accepted lists come out close and overlapping, acceptance fixes the denominator.

## What they need to know (merged, for EJ)

1. **Does each accepted use case carry a written "fails if"** (what makes a result wrong), written or accepted by EJ at acceptance? It decides T2.
2. **Precedence:** when an accepted use case contradicts a requirement, which wins?
3. **Cross-cutting requirements** (privacy, safety) — are they still "SHOULD have", or always written?
4. **Wording:** replace "must" with "a result that fails an accepted use case, or an accepted requirement, is wrong"?
5. **Does an AI-suggested requirement bind only after EJ accepts it?** (Linus)
6. **Dave's blind acceptance test** on the existing 28/200 lists — EJ's time, no engine call.

## Check

- `four_experts.py check`: 1 failure — 老子 quotes 善故能勇 where its list has **慈**故能勇 ("compassion, therefore able to be brave"). Unlike earlier rounds this is not a script variant: 善 replaces 慈, a different word. A misquote. `--sabotage`: 2 failures, as required.
- Engines (`status.json`): linus codex 94 s · fan-li agy 126 s, no fallback · sun-tzu dsh 100 s · lao-tzu opencode 112 s · Dave a Claude subagent.
- 老子's answer again begins with a stray line ("I'll read the brief first.").
- All five read the main agent's restatement and its three tensions. Dave notes the restatement's step 5 ("once a requirement exists") already builds in one answer to T1; EJ's own reason for the must was "requirements are normally details".
