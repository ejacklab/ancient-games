---
name: requirement-check
description: Evaluate a rule, requirement, threshold or algorithm against requirement-quality criteria before applying or writing it down, and ask the person which criteria it fails. Use when someone states a rule, requirement, constraint, threshold, algorithm or design guideline; when writing or editing a normative line in a document, plan or config; or when a rule reads as arbitrary, unattributed or impossible to check.
---

# Requirement check

A general standard (RFC 2119 / 8174), installed globally — not part of the Ancient Games framework. The
worked failure in `meaningful-names` cites the Ancient Games as one example.

A short gate between **hearing a rule** and **acting on it**. It exists because rules get written down that nobody
can trace, that count two different things at once, or that nothing can ever fail — and the cost lands months later,
when nobody can say whether the rule still means anything.

Run it when someone states a rule, and run it on yourself before writing a normative line into any document.

## The eight questions

Ask them of **one statement**. Say which it passes and which it fails, then **ask the person about the failures** —
do not fill the gaps yourself.

1. **Source.** Who said this, and where? Can you point to the exact line? *"Mine"* is a valid answer. Unlabelled is
   not.
2. **One thing.** An "and", an "or", a "/", or a second number means it is **two** statements. Split them, and give
   each its own source.
3. **Unit.** Every number says what it counts. Attempts or hours? Roles, or processes running at once? Bytes or
   files?
4. **Can it fail.** Name one concrete input that would make it fail. `TBD`, `—`, `0` and empty must be among the
   failing inputs. If you cannot name one, it is not checkable — it is a wish.
5. **Weak words.** *like, about, appropriate, as needed, logical, fast, enough, reasonable, only has to, TBD.* Replace
   each with a value, **or mark the value open**. Never invent the number.
6. **Level.** Is it **MUST** (a gate that stops work), **SHOULD** (a default that may be overridden with a stated
   reason), or **guidance**? A safety bound earns MUST. **A method does not** — see the RFC note below.
7. **Basis.** Measured, quoted from a source, or a guess? A guess is fine **if it is labelled** — `n=0`, with when it
   will be looked at again.
8. **Links.** Does it claim a relation to another rule — *"half of"*, *"pairs with"*, *"the same as"*, *"the runtime
   part"*? The person probably did not say that. **A link is its own claim and needs its own source.**

## Two rules for the agent

- **Never fill a gap with your own value.** A missing unit, threshold or test goes back as a question. Inventing it
  is exactly how a rule becomes unattributable later, and the invention is indistinguishable from the original by
  the time anyone notices.
- **Never add structure that was not given.** No halves, no numbered reasons, no ordered pairs, no named phases,
  unless the person said so. Quote them, state the operative sentence, stop. If a relationship between two rules is
  wanted, that is a separate claim with its own evidence.

## Two verified facts, worth quoting

- **RFC 2119 §6, "Guidance in the use of these Imperatives":** imperatives *"must be used with care and sparingly…
  they MUST only be used where it is actually required… they must not be used to try to impose a particular method."*
  Most design rules are method. Method does not earn MUST.
- **RFC 8174 (updates 2119):** the key words *"have the meanings specified herein only when they are in all
  capitals."* Lowercase *must* and *should* carry no defined requirement meaning. If nothing marks which lines are
  requirements, a reader cannot tell rules from explanation.

## How to answer

Evaluate first, in a table or a short list — **pass / FAIL per question**. Then ask the failing ones as questions,
one line each, with the options if you can see them. Two or three real questions beat eight formalities.

Do not report a rule as complete when you chose its missing value. Say which values you left open.

## A worked failure

> *"At most 5 subagent roles per run and at most 3 running at once."*

Four of the eight fail: **Source** — nobody could name one; **One thing** — a count of roles *and* a count of
concurrent processes; **Unit** — two different units, one word ("subagent") used for both; **Level** — a method
preference written as a cap. The sentence would not parse, and it took four days to find out why. The checklist
catches it in thirty seconds.

The same checklist, run on *"No single call runs longer than the ceiling: 8 hours"*, passes all eight — because it
names who set it, counts one thing, uses a unit, and some input (a 40-hour plan) makes it fail.

## Limits

The quality characteristics behind these questions (necessary, appropriate, unambiguous, complete, singular,
feasible, verifiable, correct, conforming) come from requirements-engineering sources — IEEE 830, ISO/IEC/IEEE 29148
and the INCOSE *Guide to Writing Requirements* — which were **not read** when this skill was written: they are
paywalled or blocked, and the list is recalled rather than verified. The two RFC points above **were** read, and the
quotes are checked. Treat the rest as a good working list, not as a citation.

Origin: `docs/research/20261005-requirement-statements/FINDINGS.md` in the Ancient Games project, 2026-10-05.
