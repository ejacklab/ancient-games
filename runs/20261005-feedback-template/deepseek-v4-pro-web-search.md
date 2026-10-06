# web search — feedback template (deepseek-v4-pro)

## Verdict

**Confirm** the three-field shape — `Found` / `Sources` / `Disputed` — and add one
thing: a **claim→source key**. That one addition is what turns "claims traceable"
(the check) from something the verifier has to re-derive into something he reads
straight off the shape. Nothing else added. `Effort` stays out (loop types only).

## Template

```
## Summary
- Found:    <the fact the vote decided, one per line> [S1]
- Sources:  S1 · 2026-10-03 · https://…      (one line per source)
- Disputed: <contested fact> · vote 4–2 · winner [S1] · minority [S2]
```

Worker rules (the field contract):

- Every `Found` line ends with at least one `[S#]`.
- Every `[S#]` is defined in `Sources` with a date and a URL.
- A `Found` line with no key fails "traceable" before the verifier reads further.

## The six whys

### 1. Added — the claim→source key (`[S#]`)

1. Why? Because the check is "claims traceable", and two parallel lists do not show
   which source proves which claim.
2. Why? Because the verifier's one question is, for each `Found` line, "does it trace
   to a dated source with a URL?" — the pairing *is* the answer, and a flat list does
   not carry it without re-doing the search.
3. Why? Because the whole reason for a template is "the verifier reads a known shape
   instead of free text", and a known shape is one the check can run against
   mechanically — mechanical checking needs the pairing written down.
4. Why? Because the worker writes both lists and already knows the pairing at write
   time; attaching a key costs one token and can be recovered by no one afterwards.
5. Why? Because if the mapping stays implicit, each worker will inline it differently,
   and the verifier is back to reading free text.
6. **Stop — fact.** "Traceable = a claim is paired to its dated source + URL" is the
   operative sentence of the given check. What "traceable enough" means beyond that
   (how many sources, primary vs secondary) is the human's value judgement, not mine.

### 2. Changed — `Disputed` records the count and both sides' sources

1. Why? Because "the split — the voting" without numbers is a conclusion, not a vote;
   a verifier cannot see that a vote happened.
2. Why? Because the type is *voting on contested facts* — the vote is the node's whole
   reason to exist, and the template's job is to surface the vote, not bury it behind
   the word "disputed".
3. Why? Because "claims traceable" applies to every claim, the minority position
   included; a contested fact where only the winner is sourced is half-traceable.
4. Why? Because the worker is the only writer who holds the tally and both sides'
   sources at write time; if it is not captured then, it is gone.
5. **Stop — fact.** A vote has a count; writing it down is implied by "the split — the
   voting". The exact notation (`4–2`, `60/40`, "majority with dissent") is a human
   decision I will not pick.

### 3. Omitted (from this type) — `Effort`

1. Why? Because the rule, decided with the author, puts Effort (tokens + rounds) on
   loop types only, and this is a single node.
2. Why? Because "rounds" is the load-bearing half of Effort, and a single node has
   exactly one round — the field would be empty or degenerate.
3. Why? Because Effort exists to bound a loop (its limit and stop condition), and there
   is no loop here to bound.
4. **Stop — fact.** The loop-types-only rule is the author's, decided 2026-10-05/06; I
   record it, I do not defend or extend it.

## Left for the human (not mine to decide)

- The exact key and split notation (`[S#]` vs footnotes; `n–m` vs ratio). I propose one;
  the human owns the form.
- Whether `Found` carries only facts or the node's decided answer. I read it as "the
  fact the vote decided", because the type is a voting node — but that is the human's
  call.
- The pass threshold for "traceable" (every claim must have a source, or only the
  decided one). I assumed the strongest — every claim — and flagged it rather than
  weakening it.
