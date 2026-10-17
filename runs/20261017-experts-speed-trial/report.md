# Trial — rule card, vote form, no wandering (fixes 1, 2 and 5), and the round 3 rerun

Request (EJ, 2026-10-17): "ok try 1, 2 and 5 then rerun round 3". The fixes are from
`runs/20261015-four-experts-speed/report.md`.

## What changed

Two opt-in flags in `.claude/skills/six-experts/scripts/six_experts.py`. Without them, briefs and checks are as before.

- `--card` (fixes 1 and 5). The brief holds a card in place of the two files: who they are, then one line per rule,
  giving its heading and the Rule's first sentence. It tells the expert to read nothing else but the files the question
  names, and to run no shell. Rule 3 becomes "quote nothing"; rule 5 becomes "re-read your rules above". Cards are
  5.1–6.7 KB; before, the list and identity files were 55–78 KB.
- `--vote` (fix 2). The answer form is `## Answer` (APPROVE, or CHANGE with exact words), `## Why` (at most five
  lines, each citing a rule) and `## What I need to know`. The run writes `form.txt`. `check` and the agy fallback
  then require these three sections. Dario gets the same form.
- New file `assets/answer-vote.md`; `SKILL.md` §1 documents both flags as on trial.

My choices, which nobody gave me: the card line is the heading plus the Rule's first sentence; Why is at most five
lines; the rerun used `--timeout 900` (default 1800), which never came into play because no engine came near it.

## Tests

- 14 new tests in `tests/test_six_experts.py`.
- Before the change: 8 new-behaviour tests red. The other new tests passed: they pin unchanged behaviour and the
  check's exemptions under `--vote` (Dario, Dave's insights, sabotage).
- After: 37/37, and the whole suite 1139 passed (`pytest -q tests`).
- Mutants: 6 of 6 planted breaks were caught (`mutants/result.txt`). Claude wrote the tests and the mutants, so this
  is not an independent check.

## Round 3 rerun (`round3-rerun/`, numbers in `compare-numbers.txt`)

The question text was the same (byte-compared), with the same four experts. The file under review was unchanged since
2026-10-13 23:50, before the old run.

| | Old (2026-10-13) | New (--card --vote) |
|---|---|---|
| Round's wait (slowest engine) | 94.0 s | 48.1 s |
| Sum of engine seconds | 324.0 s | 162.3 s |
| Linus (Codex) | 70 s, 45,671 tokens, 10 shell commands | 24 s, 12,202 tokens, 3 shell commands |
| 范蠡 (agy) | 66 s | 48 s |
| 孫子 (dsh) | 94 s, 11 reasoning blocks | 44 s, 5 reasoning blocks |
| 老子 (opencode) | 94 s, 16 tool calls | 46 s, 7 tool calls |
| Answer size | 2.4–8.6 KB | 0.5–2.3 KB |
| Verdicts | 4 × APPROVE | 4 × APPROVE |
| `check` | — | 4 answers pass; sabotage caught 2 of 2 |

**Fix 5 only partly held.** These are calls the engines made against the brief:

| Engine | Call |
|---|---|
| Codex | `cat CLAUDE.md` (its habit) and one Python snippet |
| opencode | one `ls` to find the round-2 answers folder the question names |

The other reads were of files the question named.

**The vote form was mostly kept.** 老子's Why ran to five long points and a "proposed change to the pattern".

**What this does not establish:**

- n=1 per engine, on a different day and load.
- The new briefs also carry the Lessons section and the "How we work" section, which the old ones lacked.
- The three fixes ran together, so their effects are not separated.
- Whether the shorter answers are as good. My reading: each still cites rules and reaches the same verdict, but I
  did not have them judged blind.

## Decision — 2026-10-17

EJ: "make them the default for approve-or-change questions". The option was Claude's, offered as "make
`--card --vote` the default for approve-or-change questions now, or run each flag alone once first"; EJ chose the
first.

Rule as written (SKILL.md §1): an approve-or-change question (its answer is APPROVE, or CHANGE with the exact words)
runs with `--card --vote`. The caller decides the type from the question, as with `--needs-web`; in the
experts-decide workflow it passes `approveOrChange: true`. Any other question runs without them. Who decides the
type, the caller, is Claude's reading, following the `--needs-web` pattern.

Tests: experts_decide_harness.mjs case 9 (red before the change, planted copy caught); 42 checks pass;
test_six_experts.py 37 pass.
