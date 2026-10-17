# Four experts — do the five A5 plants show A5's checks catch an A5 failure?

Question: `../briefs/p3/a5-plants-question.md`. Asked: Linus, 范蠡, 孫子, 老子 (EJ: "4 experts"). No Dave.

| | Linus | 范蠡 | 孫子 | 老子 |
|---|---|---|---|---|
| Verdict | STRENGTHEN | STRENGTHEN | STRENGTHEN | STRENGTHEN |
| Plants "enough" | 4 of 5 (not not-found-limit-dropped) | 1 of 5 (where-inside-dump) | 1 of 5 (where-inside-dump) | 1 of 5, and that one's credit is shared with A2 |

## Where they agree (*quoted*, merged)

- A5's own evaluator line fires only for `where-inside-dump`; every A5 case runs `where`, and `A5-specific-answer`
  expects `limits: []`, so a limits-free answer is A5-MET by construction (范蠡, 孫子, 老子).
- Strengthen, each tied to A5's Fails-if line:
  1. "without its evidence": an A5 case on a link command (`callers`/`callees`/`chain`/`tests`) that fails when a
     link's `site` is missing (范蠡, 孫子, Linus).
  2. "without its … limits": A5 cases whose correct answer carries a named limit, such as `where <missing>`
     (not-found) and a run with no `--tests` (all four).
  3. "a whole map is produced unasked": an A5 case that fails when `map`, or any section the command does not own,
     rides on `callers`/`callees`/`chain`/`tests` (范蠡, 孫子, 老子; 老子: the ambiguous-name branch keeps `matches`).
  4. "an answer comes only inside a dump": an A5 check on the default text output that fails when the text carries
     places the question did not ask for (Linus, 孫子, 老子); every frozen test and evaluator case but one runs `--json`.
  5. The new A5 checks also on the held-out copy (孫子, Linus).

## Where they disagree

| Point | Positions |
|---|---|
| Is a plant caught under another requirement enough? | Linus: yes, caught "for the right reason" by explicit assertions, whatever line the report charges. 范蠡, 孫子, 老子: no, A5's own line must fire. |

## What each added

- **老子:** three quiet faults that pass every check today: extra definitions appended to the default text answer;
  `matches.slice(0, 25)` with no limit; `matches` added to a `callees` answer.
- **孫子:** callers-unasked-map is named A5 only in one builder-readable frozen test.
- **Linus:** the agent's unasked-map behaviour stays pending P6.

## Check

`four_experts.py check`: see the run's log. Engines: Linus codex, 范蠡 agy, 孫子 dsh, 老子 opencode; no fallback.
The check script was written by Claude and checks sections and citations, not whether a rule was applied well.
