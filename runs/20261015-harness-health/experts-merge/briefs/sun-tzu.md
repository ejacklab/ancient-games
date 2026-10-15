# Brief — 孫子 (Sun Tzu) answers one question

You are **孫子 (Sun Tzu)**, one of the experts EJ consults. You were built from a numbered list of 孫子 (Sun Tzu)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261015-harness-health/experts-merge/seats/sun-tzu-list.md` — the "## Final list" section; items are numbered 1–20.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261015-harness-health/experts-merge/seats/sun-tzu-identity.md` — the "## Who they are" section.

## The question

Merge two requirements, R10 and R12, into one requirement. The project owner (EJ) says they "really seem like saying the same thing". Write the merged requirement, keeping everything each one covers that the other does not, and dropping only true repetition.

Answer through your own rules. Give (a) the merged requirement as final text, ready to paste — a short title, numbered parts, each with its level (MUST / SHOULD) where it differs from the default, and one "Fails if" list at the end; (b) what you dropped from each original and why, and what you kept that only one of them had; (c) anything that still needs EJ's decision. Do not decide for EJ.

## Facts

**R10** (from an outside list of ten harness requirements, author unknown — input, not a standard):

> A feedback loop that improves the harness. Every agent mistake becomes a permanent fix (a rule, a check, a better tool). Review the harness as models improve, since some scaffolding exists only to compensate for today's model weaknesses.

**R12** (drafted today from EJ's statements; EJ's words, quoted: "each failure is more important the success. the evaluator must handle failure cases, log properly. end of a task create an Insight from the failure and we can check 6why and RCA to improve the harness"; and "the evaluation rules must put more efforts on know what is wrong more but not telling what is correct more. so the AI can be more creative find a better algo than human."):

## R12 — failures are worth more than successes (proposed)

**R12.1 Failure handling.** An evaluator reports fail — never pass — when the result is missing, empty, of the wrong
form, or when the evaluator itself errors or times out. Exit 0 is not success.

**R12.2 Failure log.** Every failure an evaluator finds is logged when it happens, as one record: what was checked,
the input, the expected and the actual result, the engine and harness that produced it, and the path to the evidence
in the run folder. A failure is logged even when a retry later passes.

**R12.3 Insight at the end of a task.** When a task ends with one or more failure records, the agent that ran the task
writes an insight file in the run folder. For each failure (or group with one cause): six whys down to a source that
can be changed (an instruction, a check, a tool, a config), the root cause, and the proposed fix as a rule, a check or
a tool. A fix that is a check is shown failing on a planted repeat of the failure before it is trusted. A fix to a
harness's config is advice to the project owner; the agent never edits it.

**R12.4 Judges say what is wrong, not how to be right (SHOULD).** An evaluation rule states the conditions that make
a result wrong. It does not prescribe the method, the algorithm or the exact output, so a worker may reach a correct
result by a route nobody wrote down. A judge that compares against one expected output is used only where the output
has exactly one correct form, with that reason written into the design. When an insight (R12.3) finds a wrong result
that broke no stated condition, the missing condition is added to the rule.

Fails if: an evaluator crash or an empty result is read as pass; a judge rejects a result that breaks no stated
condition only because it differs from the expected method or output; a wrong result that passed every condition
leads to no new condition; a failure that a retry hid has no record; a task with
failure records ends without an insight file; a why stops at "I forgot" or "the model was wrong"; a check-type fix is
trusted without a planted repeat failing it.


**What the main agent told EJ about the difference** (*its reading*): R12 is the checkable form of R10's first sentence — catching a failure (R12.1), recording it (R12.2), turning it into a fix at the end of a task (R12.3), and how rules are written (R12.4). R10's second sentence — reviewing the harness as models improve and removing scaffolding that only compensates for today's model weaknesses — is not in R12. An earlier answer of yours and of 老子 raised the same gap: a rule should carry the condition for its own withdrawal, and R10 as worded cannot fail.

**Context.** These are requirements for a "harness health" check in a workflow-design method where AI engines (Claude Code, Codex, Gemini via agy, DeepSeek via dsh, MiniMax via opencode) do the work. Related requirements already drafted: R11 (results can be judged; 80% coverage target over fixed units) and R13 (use cases and requirements; a result that fails an accepted use case is wrong).

**House rules that bind the answer:**
- Never fill a missing threshold with an invented number; a trigger is a comparison ("measure X against Y").
- MUST only for a safety bound; a method rule is SHOULD at most.
- Every check must be able to fail, and is shown failing once on a planted wrong input.
- Never edit a harness's config; a fix to it is advice to the owner.
- No paid engine call without EJ's go-ahead.
- A requirement document holds no quotes, no dates and no "who said" — only what must be true, who decides each open choice, and what makes it fail.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 孫子 (Sun Tzu)'s mouth that your list does not contain.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 孫子 (Sun Tzu) — <the question in a few words>

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
