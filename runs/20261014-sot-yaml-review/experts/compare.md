# Four experts and Dave — will an agent follow the requirements YAML, and what layout serves it

Question: `../question.md` (the full draft is embedded in it). Answers: `answers/`.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Answer (one line, *quoted*) | "reliable agent compliance is **not measured**, and several checks contradict or incompletely describe their requirements" | "Another AI agent will not follow this YAML draft reliably because gates and defaults are entangled in shared text blocks" | "No — not reliably as a gate, though it is a fine readable annex" | "An agent will follow this draft about half as reliably as it looks" | "Nobody knows yet whether an agent follows this YAML more reliably than the Markdown … So test it" |
| A — level per clause | split into clauses, one level each | split | split the 15 mixed-level ones only | split the 15 mixed-level ones only | keep the text whole; one `level` shape |
| B — `fails_if` | beside each clause; shared only with its ids named | one per requirement | one per requirement, plus `check:` naming the runner | one per requirement; one check may name several ids | keep per group, tag each clause with its ids |
| C — links | `links:` with the relationship | `links:` list | `links:` plus inline, with a lint | no; generate later when a lint exists | no |
| D — who decides | on each open choice | per requirement | only where a choice is open; `none` otherwise | on the open choice; `unassigned` where nobody | no field; say it in the text |

## Where they agree

*My count*, the four experts; Dave is the control.
- **A, B and D: all four change the draft.** Split mixed-level requirements so each clause has one level (孫子 and 老子:
  only the 15 mixed ones). Put the check on the requirement it checks. Name who decides each open choice. Dave alone
  keeps A and B as they are.
- **C: three of four add a `links:` list**; 老子 and Dave would wait until a script reads it.
- **Nobody's claim is measured.** All five ask for a test with agents, draft against revised, before saying "agents
  follow it better". 孫子: *"Formatting cannot fix the real exposure: MUST gates whose only check a non-existent
  reviewer can judge."*

## Faults in the draft that several found (*my reading*, merged)

1. **`level` has two shapes** (a word or a map) and `text` a third (a sentence ending in a colon, with the rule in
   `items:`). 孫子, 老子, Dave.
2. **A group's `fails_if` gates what the level calls SHOULD** — W1 (missing field or section), W2, W4 (`changed:`
   line), K1. Linus, 孫子, 老子. 老子 also: W1's check says "a lint" finds three things `memory_index.py` does not check.
3. **Judged MUSTs with no reviewer** — all five. 老子 counts 14 of 22 MUSTs judged only.
4. **Rd2.3 "the other four"** makes the reader count a list to learn a level. 孫子, 老子, Dave.
5. **K2 and K3 are missing** with no word why. 孫子, 老子, Dave.
6. **Header facts live in comments**, which parsers drop. 孫子, 老子.
7. **The levels have no basis in the file** — `SOURCE_OF_TRUTH.md` says MUST nowhere. 老子.
8. **`guidance` is under `level:`** though it has nothing to pass; and Rd5.4, labelled guidance, carries operative
   exceptions to the Rd5.3 MUST. 孫子, 范蠡.
9. **"EJ" is named in a product meant for any repo**; use a role ("the project owner"). Dave.
10. **No reading order**: an agent setting up memory reads Write first and meets session start (Rd2.1) last. 老子.
11. **Behaviour gaps the layout cannot fix** (Linus): retiring an entry with no replacement; K1.1 "change the entry"
    against K4.3 "never rewrite"; what work a failed MUST stops; Rd4.1 "entries" against its check's "decisions";
    Rd2's check against the link exception in Rd2.3.

## Where they disagree

- **C, links.** Linus: *"A bare reference cannot distinguish an exception from a dependency"*. 老子: *"A list that only a
  future lint would follow is machinery bought for a reader who does not exist"*.
- **D, scope.** 范蠡: a field per requirement. 孫子 and 老子: only on open choices, with `none` / `unassigned` explicit.
  Dave: in the text, no field.

## Check

`four_experts.py check`: 5 answers, 3 failures, all 老子: 為/爲 twice (a script variant) and 吾有三寶 against his
list's 我有三寶 (a variant reading of the same line). The check was written by Claude; it does not establish that a
rule was applied well. One fact error by reading: Linus says the size check is not implemented; `--check` does fail
an oversized `INDEX.md` (the COO's facts list omitted it). Engines (`status.json`): Linus codex gpt-6.1-sol, 范蠡 agy
gemini-3.8-flash-medium (no fallback), 孫子 dsh, 老子 opencode MiniMax-M3.1-Flash-Preview, Dave a Claude subagent.
