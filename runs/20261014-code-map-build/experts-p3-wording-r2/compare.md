# Four experts — final wording of A2 and A5 (round 2 of 2)

Questions: `../briefs/p3/wording-r1-question.md` (round 1), `../briefs/p3/wording-r2-question.md` (round 2).
Answers: round 1 `../experts-p3-wording-r1/answers/`, round 2 `answers/`. Each line is *quoted* (condensed from an
answer), *my reading* (the COO's), or *not measured*.

| # | Proposal | Linus | 范蠡 | 孫子 | 老子 | Settled? |
|---|---|---|---|---|---|---|
| 1 | ambiguity: tool duty and agent duty | accept, two bullets | accept, **one** bullet naming both | accept, two bullets (changed, after 范蠡) | accept, two bullets | **yes**, both actors named inside A2; layout 3–1 |
| 2 | define "known" | accept: "established from repository source or type information" | **reject** | accept, Linus's wording (changed, after 范蠡) | accept: place = what the code or description points to; link = what the type checker establishes | **no**, 3 accept, 1 rejects; wordings split 2–1 |
| 3 | a body written straight into a call is its own place | accept; adds "unresolved links carry limits" | accept | accept, "or a stated limit" cut (changed) | accept, "or a stated limit" cut (changed) | **yes**: no "or a stated limit"; the name of such a body is not fixed in the requirement (all four) |
| 4 | depth = shortest route; a reference back never hides a link | accept | accept | accept | accept | **yes**; 3 keep "the place is level 0; each link adds one level" in A2, 老子 leaves it to the spec |
| 5 + 8 + 9 | no content the question did not ask for, beside or inside the answer, JSON and default text | accept | accept | accept | accept | **yes**: all four state what an answer holds (result, evidence, limits, candidates) and nothing else; 老子 words the rest as "nothing the command does not answer" (范蠡: misses an extra link inside a `callees` answer) |
| 6 | a stop that stops short carries its limit | cut the stop sentence; keep "limits the interface requires for that command" | **reject** (L1) | **reject** (changed, after 范蠡) | cut the stop sentence; keep "that whole answer" and the interface-required limit | **yes** on cutting the stop-short sentence (L1 owns it); **no** on the interface-required-limit clause (2–2) |
| 7 | map: tool and agent | accept: only `map` returns a whole module map; the agent runs `map` only when asked | accept the agent half; tool half covered by 5/9 | accept, both halves | accept, both halves | **yes**, wording "a whole module map" and "the agent runs `map`" (all four) |

Added in round 2 by two experts (Linus, 老子): the "shown twice" line also fails when the reference back is
missing or does not say where the function is shown.

## Questions only the owner can settle (from the answers)

1. **Does a known link the tool marks with a `dynamic` limit count as missing?** (范蠡). 老子: under "a link is known
   when the type checker establishes it" the wording answers it (not missing); under a wider "known", A2's line
   needs 范蠡's conditional: "a known link within the depth is missing with no limit at its site naming why".
   This is the question behind the split on 2.
2. **Does going into a body written straight into a call count as a level?** (范蠡, from 老子's round 1). It changes
   how far the default six reaches on opencode; the vision does not say.

## Remaining splits (the owner picks; the arguments are in the answers)

- 2: reject (范蠡), or define "known" by evidence (Linus, 孫子), or by the code/description for places and the type
  checker for links (老子). Tied to question 1.
- 6: whether A5 says "a limit the interface requires for that command is part of the answer" (Linus, 老子: yes;
  范蠡, 孫子: no, "its limits" already covers it).
- 1 and 7: one bullet naming both actors (范蠡), or a tool bullet and an agent bullet (the other three).

## Side findings (for the COO, not wording)

- `find` keeps only the best score tier of description matches, with no limit (老子, verified in code by 范蠡,
  `commands.ts` `matchesByDescription`). Whether that breaks A2's "every candidate" or L1 is a spec question.
- `reachableFrom` stops at 400 visits with no limit (范蠡, from reading `commands.ts:183–186`; *not run*). If so, an
  L1 fault in the `tests` path.
- Changing a Fails-if line's text means re-mapping every case's `line` field in `eval/requirements.ts` before a
  round can be read (范蠡, 老子).

## Check

`four_experts.py check`: Linus, 孫子, 老子 status ok (131 s, 192 s, 537 s); 范蠡 ran as a Claude subagent (needs
shell), answer saved by the COO. Two flags on 老子, both 為/爲 script variants of his own list's 爲; no invented
quotes. The check (written by Claude) does not establish that a rule was applied correctly.
