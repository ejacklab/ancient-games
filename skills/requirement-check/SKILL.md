---
name: requirement-check
description: Evaluate a rule, requirement, threshold or algorithm against requirement-quality criteria before applying or writing it down, and ask the person which criteria it fails. Use when someone states a rule, requirement, constraint, threshold, algorithm or design guideline; when writing or editing a normative line in a document, plan or config; or when a rule reads as arbitrary, leaves a choice with no one to decide it, or is impossible to check. Also checks use cases and the requirements written from them (R13: two lists merged by the user's decisions; purpose, fails-if and minimum acceptance; a requirement's purpose and acceptance; use case wins a conflict) — use when writing, suggesting, accepting or judging work against use cases.
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

1. **Who decides.** Find every choice the statement leaves open, and name who decides each one: the user, the agent,
   the tool by a stated rule, a config value, a checker. Write the decider into the requirement. *"Must not read a
   single line and conclude"* leaves open how many lines are enough — who determines that? Answering it completes the
   requirement. This asks who decides **inside** the rule, not who asked for it; where the rule came from is
   **Basis**. *(EJ, 2026-10-14.)*
2. **One thing.** It is about **one action or one event**: one thing that happens, and what must be true when it
   does. A condition or a record that belongs to that event is part of it, not a second statement. If it names two
   events (a role is defined, a process starts), it is **two** — split them, and check each one on its own. An "and",
   an "or", a "/" or a second number is only a hint to look; it is not the verdict. *(EJ, 2026-10-12.)*
3. **Unit.** Every number says what it counts. Attempts or hours? Roles, or processes running at once? Bytes or
   files?
4. **Can it fail.** Name one concrete input that would make it fail. `TBD`, `—`, `0` and empty must be among the
   failing inputs. If you cannot name one, it is not checkable — it is a wish.
5. **Weak words.** *like, about, appropriate, as needed, logical, fast, enough, reasonable, only has to, TBD.* Replace
   each with a value, **or mark the value open**. Never invent the number.
6. **Level.** Is it **MUST** (a gate that stops work), **SHOULD** (a default that may be overridden with a stated
   reason), or **guidance**? A safety bound earns MUST. **A method does not** — see the RFC note below.
7. **Basis.** Measured, quoted from a source, or a guess? A guess is fine **if it is labelled** — `n=0`, with when it
   will be looked at again. In the document the basis is at most a short label and a path to the evidence, never the
   conversation it came from.
8. **Links.** Does it claim a relation to another rule — *"half of"*, *"pairs with"*, *"the same as"*, *"the runtime
   part"*? The person probably did not say that. **A link is its own claim and needs its own basis.**

## Four rules for the agent

- **Check the line you write, not only the reply you heard.** When the person answers your question briefly ("yes",
  "flag them", "use git"), the requirement is **your question plus their answer**. Write that whole rule — what, when,
  who, what happens next — run the eight questions on the written line, and only then put it in the document. A
  pasted short reply fails *one thing*, *weak words* and *can it fail* on its own. *(EJ, 2026-10-12, after "flag
  them" was written into a design alone and later misread.)*
- **Never fill a gap with your own value.** A missing unit, threshold or test goes back as a question. Inventing it
  is exactly how a rule becomes unattributable later, and the invention is indistinguishable from the original by
  the time anyone notices.
- **Never add structure that was not given.** No halves, no numbered reasons, no ordered pairs, no named phases,
  unless the person said so. Write the operative sentence, and stop. If a relationship between two rules is
  wanted, that is a separate claim with its own evidence.
- **No conversation in a requirement.** A requirements document states what must be true, who decides each open
  choice, and what makes it fail. It holds no quotes of the person, no "X said", no dates, no `Source:` line and no
  mark of who proposed what. That history goes in the run folder (`runs/<id>/`), never in the product document. The
  eight questions are asked of the line; their answers change the line, they are not printed beside it. *(EJ,
  2026-10-14, after conversation was put into requirements again and again.)*

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

Four of the eight fail: **Basis** — nobody could say where it came from; **One thing** — a count of roles *and* a count of
concurrent processes; **Unit** — two different units, one word ("subagent") used for both; **Level** — a method
preference written as a cap. The sentence would not parse, and it took four days to find out why. The checklist
catches it in thirty seconds.

The same checklist, run on *"No single call runs longer than the ceiling: 8 hours"*, passes *one thing*,
*unit* and *can it fail* — it counts one thing, uses a unit, and some input (a 40-hour plan) makes it fail. *Who
decides* still asks who stops a call that reaches the ceiling.

## Use cases and requirements (R13)

The eight questions check one statement. R13 checks the **list** a piece of work is built and judged against: the
accepted use cases, and the requirements written where they leave a detail unclear. The rule itself, R13.1–R13.7 with
its fails-if, is `references/use-cases-and-requirements.md` — one copy; read it before writing or accepting a list.

Check, in this order:

1. **Whose list.** The user's own cases and the agent's suggestions are two lists; a suggestion is in the accepted list
   only with the user's recorded decision (R13.1).
2. **Each use case** holds its purpose, its fails-if and its minimum acceptance, each an observable outcome, never a
   method (R13.2). Run *can it fail* and *weak words* on the fails-if and the minimum acceptance.
3. **Each requirement** names the use case or vision line it serves, and binds only once the user has accepted it — an
   edit needs a new acceptance (R13.5). Two qualities that pull against each other each get a target the user gives
   (R13.4). Then run the eight questions on it.
4. **A conflict** between an accepted use case and an accepted requirement: the use case wins, and the conflict is
   recorded and shown to the user (R13.7).

The part that needs no judgment — recorded decisions, the three fields, a purpose, a conflict shown, and coverage
(R11.1) — is checked by the workflow-design skill's guard: `bun <workflow-design>/guard/src/cli.ts register <file>`.
Whether a purpose is the real one, or a fails-if observable, stays a reading.

## Limits

The quality characteristics behind these questions (necessary, appropriate, unambiguous, complete, singular,
feasible, verifiable, correct, conforming) come from requirements-engineering sources — IEEE 830, ISO/IEC/IEEE 29148
and the INCOSE *Guide to Writing Requirements* — and the standard and the guide are still **not read**: paywalled or
blocked (HTTP 403, checked 2026-10-16). The nine names are confirmed only at second hand: a 2024 paper (Lubos et al.,
arXiv 2408.10886, Table I) lists the same nine as the characteristics of ISO/IEC/IEEE 29148:2018; an older summary
gives a different list, probably the 2011 edition. No INCOSE rule number is verified. The two RFC points above
**were** read, and the quotes are checked. Treat the rest as a good working list, not as a citation; the sources and
their labels are in `runs/20261016-integrate-r11-r13/research/findings.md` in the Ancient Games project.

Origin: `docs/research/20261005-requirement-statements/FINDINGS.md` in the Ancient Games project, 2026-10-05.
