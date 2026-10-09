---
name: meaningful-names
description: The clean-code standard for naming functions, variables, classes and concepts, and for naming the one thing a name must do. Use when naming or renaming a function, variable, class, module, field or config key; when a name is ambiguous, vague, a pun, or does several jobs; when a function does more than one thing; or when a requirement or rule reads as arbitrary because a word means several things.
---

# Meaningful names

A general standard (Clean Code, chapters 2-3), installed globally — not part of the Ancient Games framework;
the worked failure below uses the Ancient Games as its example.

Names are the interface of code. A bad name does not just look bad — it misleads the next reader, and a name that
does several jobs produces rules nobody can later explain. This is the naming half of *Clean Code* (Robert C. Martin,
chapters 2 and 3), compressed into something a person can apply in thirty seconds.

## The one principle everything else follows

**A name must reveal what the thing is, or what the function does — including the object it acts on.**

`run_verification` fails twice: "run" carries nothing, and "verification" does not say *what* is verified.
`verify_node_result` says both. This is the single rule to remember.

## Names — the rules (Clean Code, chapter 2)

| rule | what it rejects |
|---|---|
| **Intention-revealing** | `d`, `n`, `tmp2` — a name must say what it *is* or *does*, not what it looks like |
| **Avoid disinformation** | `AccountList` for something that is not a list; a name that means something else in another context |
| **Meaningful distinctions** | `a1`/`a2` for source/destination; `CustomerData`/`CustomerInfo`/`Customer` — spell out the difference |
| **Pronounceable** | `genymdhms`, `mnger` — you must be able to say it in conversation |
| **Searchable** | `WORK_DAYS_PER_WEEK` over `5` — a single letter or number cannot be found |
| **No encodings** | Hungarian (`tblStudent`), member prefixes (`m_name`) — the type system carries this now |
| **Class = noun, method = verb** | a class is a thing (`Customer`), a method is an action (`save()`, `isEven()`, `hasElement()`) |
| **Pick one word per concept** | `fetch`/`retrieve`/`get` for the same idea — choose one and use it everywhere |
| **Don't pun** | the same word for two different ideas (`add` for both a sum and an insert) — one word, one meaning |
| **No mental mapping** | the reader must not translate your name into the one they already know |
| **Solution/problem domain** | use the CS term (`queue`, `hash`) when one exists; otherwise the problem's own word (`account`, `policy`) |
| **Context, not gratuitous context** | add just enough prefix to disambiguate; `GSDAccountAddress` is too much |

## Functions — the rules (Clean Code, chapter 3)

- **Do one thing.** A function that does two things should be two functions — a name cannot describe a function that
  does two jobs, and neither can a reader trust it.
- **The name describes what it does.** If you need the word "and", or a sentence, to name it, it does too much.
- **One level of abstraction per function.** A function should not mix "save the file" with "loop over bytes".
- **Few arguments.** Zero or one is ideal; three needs a strong reason. More than three usually means a missed object.
- **Verbs, with an object.** `deletePage`, `setPoint`, `verify_node_result` — the object goes in the name, so nobody
  has to ask "verify *what*?".

## The tie to requirements

A function name is a small requirement statement, and the same checklist applies. Ask of a name what you would ask of
a rule (`requirement-check`):

1. **Source** — is it my name, or the domain's name? Say so.
2. **One thing** — does the name claim one action, or does it smuggle in a second ("and")?
3. **Unit** — does the number or noun name what it counts? `attempts` or `hours`? A `queue` or a `set`?
4. **Weak words** — `handle`, `process`, `manage`, `do`, `run`, `data`, `info` — these mean nothing until something
   follows. Replace, or add the object.
5. **One word, one job** — the *naming* form of "unit": if `check` means five things, split it.

## A worked failure, from the Ancient Games project

The word `check` did five jobs in one codebase: a node's success test (the `check` field), validating a plan
(`check_plan`), running the test (`run_check`), probing the environment (`check_binary`, `check_blueprint`,
`check_machine`), and comparing plan to design. That is a pun in Clean Code's sense — one word, five meanings — and it
produced rules that read as arbitrary.

The split:

| was | now | one job |
|---|---|---|
| `check` field | `check` (kept) | a node's success test |
| `check_plan` | `validate_plan` | is the document well-formed |
| `run_check` | `verify_node_result` | does this node's work meet its test |
| `Check`, `check_binary`, … | `Probe`, `probe_binary`, … | inspect the environment |
| `compare_design` | `compare_plan_to_design` | plan against design |

## Limits and source

The rules are Robert C. Martin's *Clean Code*, chapters 2 ("Meaningful Names") and 3 ("Functions"). The rule **names**
above were verified against a public study guide of the book (HTTP 200); the book itself was not read in the session
that wrote this skill, so exact wording is RECALLED and the rule names are VERIFIED-secondhand. The worked example
and the "name the object" phrasing are the Ancient Games project's own, 2026-10-05.

Complements `requirement-check` (a rule is a statement; a name is a one-word statement) and `coding-discipline` (the
broader hands-on baseline). If the three overlap, the more specific one wins.
