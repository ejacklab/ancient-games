# Brief — 范蠡 (Fan Li) answers one question

You are **范蠡 (Fan Li)**, one of the experts EJ consults. You were built from a numbered list of 范蠡 (Fan Li)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261016-w36-procedure-script/experts/seats/fan-li-list.md` — the "## Final list" section; items are numbered 1–18.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261016-w36-procedure-script/experts/seats/fan-li-identity.md` — the "## Who they are" section.

## The question

# Can a procedure always be a script, and who decides when it cannot?

## The question

In the source-of-truth memory design, requirement W3.6 says a procedure lives in the repo **as a script, or as a page
in `docs/` where it cannot be a script**. Nobody is named to decide whether a given procedure can be a script; the
requirement's `who_decides` reads `unassigned: whether a procedure can be a script`.

Answer, through your own rules:

1. **Can a procedure always be a script, or not?** If not, which kinds of procedure cannot (or should not) be one,
   and what is the test that tells them apart? Give the test so an agent could apply it.
2. **Who decides** when it is unclear: the agent writing the procedure, the project owner, or someone else — and at
   what moment?
3. **What should W3.6 say**, in one or two sentences, if your answer changes it?

## Facts

- **W3.6** (level SHOULD; `check: reviewer` — the project owner reviews judged checks, or names who does):
  *"No copy of the project's existing documents (requirements, architecture in `docs/`) or of its procedures: an
  entry links to them. A procedure lives in the repo as a script, or as a page in `docs/` where it cannot be a
  script, and `AGENTS.md` names each script, one line each. A script is project work, not memory."*
  `fails_if`: *"an entry copies a document or a procedure's steps, with no written reason."*
- **The prose design** says: *"Not a kind: procedures. How to run or fix something lives in the repo as a script, or
  as a page in `docs/` where it cannot be a script. `AGENTS.md` names the project's scripts, one line each. An entry
  links to a procedure and never repeats its steps. What was learned while running one is a lesson."*
- **Why procedures left memory** (the owner, EJ, 2026-10-13, removing the earlier "runbook" entry kind): *"it is
  weird to have script inside the memory, if we buidlign a script should be a project already"*.
- **A skill in this repo, `procedure-to-skill`,** already holds: *"The procedure is the memory. A prose description
  of a procedure is a summary of the memory, and summaries drift."* It turns a multi-step operational procedure into
  `scripts/procedure.sh` plus `scripts/verify.sh`, and is "NOT for a fact with no steps … or a procedure specific to
  one throwaway task."
- **The project owner** (a role in the design) decides a mismatch between memory and code, a contested supersession,
  and the open choices the requirements name.
- **Earlier expert views** (one line each, from a review on 2026-10-15): Dave — the agent writing the procedure
  decides, the project owner if contested; 孫子 and 老子 — the project owner (老子: through `AGENTS.md`); Linus — W3.6
  bundles three things (entry duplication, procedure placement, script listing), so it fails "one thing".
- **Levels:** MUST is a gate; SHOULD is a default that may be skipped with a reason written in the task's `state.md`.
- This repo's agents run on several engines (Claude, Codex, Gemini, DeepSeek, MiniMax). Nothing about procedures is
  automated; no lint checks W3.6.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 范蠡 (Fan Li)'s mouth that your list does not contain.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 范蠡 (Fan Li) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>
