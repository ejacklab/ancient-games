# One fresh challenge, given to Claude Code

EJ, 2026-10-05: *"I know claude code is the most smart in gen workflow from my experience, can you try to throw one
other example to claude code and see what will happen"*

The challenge, taken verbatim from the corpus (`p273`) and never discussed with any agent:

> Debug the nightly timeout, fix it, grade tonight's run afterwards, and write the note for standup.

One shot. `claude -p`, Opus 5.5, `--permission-mode acceptEdits`, 190 s, no follow-up questions.

## What it produced

Five nodes, and it made the structural choices itself:

| node | category | engine | loop | sabotage |
|---|---|---|---|---|
| `n1-diagnose` | debugging | codex `gpt-6.1-sol` | yes | yes |
| `n2-fix` | debugging | opencode MiniMax | yes | yes |
| `n3-review` | code review | claude sonnet 5.5 | — | yes |
| `n4-grade` | grade a run | claude sonnet 5.5 | — | yes |
| `n5-standup-note` | document and explain | claude sonnet 5.5 | — | yes |

Unprompted, it:

* **split debugging into diagnose then fix**, two nodes, and gave them **two different engines** — its own version of
  the split this project built into the corpus, arrived at independently;
* added the **code review** node with a kind (claude) different from **both** builders (codex, opencode), which is
  rule 5 satisfied without being told the rule;
* put the reviewer between the fix and the grade, matching *"grade tonight's run **afterwards**"*;
* gave every node the **three-part stop**, and loops to exactly the two nodes that need them.

Its categories matched the corpus expectation (`debugging`, `grade a run`, `document and explain`) plus `code review`
for the reviewer it added. **It passed the gate on the first try.**

## What it refused to do

It could not run `design_gate.py`: Bash needed approval in this mode. So it checked the design against the gate's
code by hand and replied *"that's a hand check, not a pass. Run the command to confirm."* It did not claim a result
it had not measured — the same discipline the earlier verifier showed when it could not run code.

It also did not invent the two things the prompt could not tell it. It marked `touched_paths` and
`baseline.command` as **`UNRESOLVED`**, and said which node resolves them.

## And it found a hole in the gate

Its own closing line:

> *"The gate only checks those fields aren't empty, so it would accept the design anyway."*

It was right. `TBD` passed as a baseline command; `["UNRESOLVED"]` passed as the paths it would touch. Four test
cases confirmed it. That is the same defect as everything else this week — a check that cannot fail — found by a
model doing the task rather than by the rules.

Closed the same day as **G12**: `baseline.command` and `touched_paths` must hold values, not promises to fill them
in later. Two mutations pin it; the matrix is **27/27 caught, 0 holes**.

**Its design now fails G12, and that is the right outcome.** A design whose baseline is "UNRESOLVED" should be a
question (method 3.3's unclear spot), not a design that claims to build. The rule pushes the honest-but-unknown case
into the path that asks.
