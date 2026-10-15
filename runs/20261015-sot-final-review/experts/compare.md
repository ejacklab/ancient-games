# Four experts and Dave — review of the finished source-of-truth design (prose + requirements YAML)

Question: `../question.md`. Answers: `answers/`. Every line is *my reading* of the answers unless quoted.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Verdict | keep the design, "fix the contradictions and incomplete checks before calling it finished" | "An agent will stumble on three contradictions" | "An agent will not follow this design as it stands" — the design's fault | "An agent will mostly follow it — … but four things will stop a careful one" | "An agent will follow most of it. It will stumble in four places" |

## Where they agree — fixes (count of the five who raised each)

1. **Retiring an entry with nothing replacing it is impossible** (K4.1 demands `superseded_by`; the tool itself says
   "retire or merge entries until it fits"). 4 of 5: let `retired` carry a `changed:` reason instead of a link.
   老子 dissents: keep requiring a replacement.
2. **K1.1 "change the entry first" reads as an edit; K4.3 forbids rewriting a claim.** 5 of 5: spell out the
   supersession steps (new entry with `supersedes`; old entry gets `changed:`, `status: superseded`,
   `superseded_by`; regenerate `INDEX.md` in the same commit), or link K1.1 to K4.3.
3. **What a failed MUST stops.** 4 of 5: the thing its `fails_if` names (the entry, commit, load or action), not the
   whole task — as Rd5.3 already says.
4. **"text governs" points at a parent that has no text** (W1.1 etc. have no record). Linus, 孫子, Dave.
5. **W1.2a (MUST) "each field is one `key: value` line" contradicts W1.2b** (multi-value fields on indented lines).
   Linus, 老子.
6. **A SHOULD's "written reason" has no named place.** 老子, Dave: the task's `state.md` (or the commit message).
7. **The secret scanner does not exist**, yet W3.2 (MUST) lists it first. Linus, 老子, Dave: say so.
8. **The prose says "never" where the YAML says SHOULD** (W3.1, W3.3b, W3.4, Rd2.3b, K6.1b); nothing says which
   governs. Linus, Dave.
9. **`who_decides: none` on reviewer records contradicts "the project owner names who reviews"; `roles` says the
   owner decides the open choices while W3.6 and Rd3.1a say `unassigned`.** 孫子.

## Who reviews the judged checks (Q3) — they differ

- Dave: whoever merges reviews what the files show; session-behaviour checks (what was loaded or read) only by an
  audit the project owner orders, "otherwise unchecked", said plainly.
- 老子: the reader the prose already names, recording what it read in `state.md`.
- 范蠡: the task's verifier or the reviewing agent on the branch.
- 孫子: the project owner, as the default reviewer of record.
- Linus: unresolved until assigned; mark judged checks as partial detection.

## The two unassigned choices (Q4)

- **W3.6** (can a procedure be a script): 孫子, 老子 → the project owner (老子: via `AGENTS.md`); Dave → the agent
  writing it, the owner if contested.
- **Rd3.1a** (which agents, so the `INDEX.md` limit): Dave, 孫子 → the project owner, recorded where the tool can read
  it; 老子 → whoever measures. Dave: the tool already hard-codes 200 lines / 24,000 bytes, so the choice was made
  silently.

## Check

`four_experts.py check`: 5 answers, 3 failures — 老子's answer is cut short (no "What I need to know", "Costs and
risks", "How we would know"); its Answer and reasoning are complete. The check was written by Claude; it does not
establish that the rules were applied well. Engines: Linus codex gpt-6.1-sol, 范蠡 agy gemini-3.8-flash-medium,
孫子 dsh, 老子 opencode MiniMax-M3.1-Flash-Preview, Dave a Claude subagent.
