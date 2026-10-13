Method 3.5 — before these pieces run as loops: are their checks real?

Asked of: Linus, 范蠡, 孫子, Dave (`--only linus,fan-li,sun-tzu,dave`). Answer **your own** question below, through
your rules, for each piece listed; the others answer theirs.

- **Linus:** could this check pass while the requested result is wrong, or while an existing user workflow breaks?
- **范蠡:** what bounds the attempts before the loop must exit, and how promptly must it close when the check passes?
- **孫子:** what is left to the worker's good character rather than to a check the worker cannot edit?
- **Dave:** what result would show this check can fail, and what is its control (old code, a plant, the baseline)?

In "Answer", give one line per piece id: loop-ready as written / strengthen the check (how) / not loop-ready (why).
Name a concrete failure the check would miss wherever you can; "looks fine" is not an answer.

Facts (filled in by the COO), per piece:
- <piece id> — deliverable: <what it produces>
  - check: <the command or checklist, and who runs it> · known to fail on: <the sabotage it catches, or "not yet shown">
  - attempt limit: <n> · feedback on failure: <what goes back> · exit: <where it goes when the limit is hit>
  - may change / must not change: <paths>
