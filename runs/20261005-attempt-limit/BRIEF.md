# Complete one requirement — you are the 孫子兵法 and game-strategy expert

A workflow-design method contains this statement, and a requirement check has found it wanting:

> **"A limit on attempts."** — `docs/WORKFLOW_DESIGN_METHOD.md`, 3.5's loop-ready list, item 2

Your job is **not to defend it and not to criticise it.** It is to **complete it**: write the requirement it should
have been.

## Read first

- `runs/20261005-attempt-limit/CHECK.md` — the eight-question check on the statement, and the five questions it
  leaves. Read this before anything else; it is the blank you are filling.
- `docs/research/20261005-requirement-statements/FINDINGS.md` §2 — the checklist you must satisfy. **Your answer is
  graded against it.**
- `docs/WORKFLOW_DESIGN_METHOD.md` §3.5 (loops) and §3.8 (running a node: timers, the 8-hour ceiling on one call).
- The four 孫子兵法 notes in `docs/research/20261004-sunzi/` — `claude-opus-5-5.md`, `minimax-m3.1-flash.md`,
  `deepseek-v4-pro.md`, `CANONICAL.md`.

## Write `runs/20261005-attempt-limit/<your-engine>.md`

**1. The completed requirement, or requirements.** If the checklist says the statement is two things, give two, each
separately complete. For each one:

| field | what to write |
|---|---|
| **Statement** | the requirement in one sentence, in the form a reader can act on |
| **Source** | who says so. *"EJ, 2026-10-05"* is valid; **"my domain reasoning" is also valid** if you label it; unlabelled is not |
| **Unit** | what every number counts — attempts, hours, seconds, tiers |
| **Value** | the number, **or the word `open`**. If you leave it open, say what the default should be meanwhile |
| **One failing input** | a concrete input that would make the check fail. `0`, empty and `absent` must be among them |
| **Level** | MUST (a gate), SHOULD (a default with reasons to override), or guidance (RFC 2119 §6: a method does not earn MUST) |
| **Basis** | measured, quoted, or a guess. A guess is fine if you mark it `n=0` |

**2. Your five answers.** The five questions in `CHECK.md` under "The questions this leaves". Answer each, and where
you would leave it open, say so and say why.

**3. Where 孫子兵法 helps, and where it does not.** This requirement is about stopping: how many times to try before
you stop, and what exhaustion costs. Say which principles from the notes bear on it — quoted, with their **Basis**
label — and name two or three parts of this requirement that a strategy text has nothing useful to say about. **Do
not manufacture a principle.** In an earlier round every expert used this section honestly and it was the most
useful part of the work.

## Rules

- **Your permitted classical source is those four notes and nothing else.** Quote only what is in them, and carry
  their `Basis` label (VERIFIED / RECALLED). A 孫子兵法 line from your own memory is forbidden.
- **Do not invent a number and present it as the answer.** If the value is EJ's to set, say `open` and give the
  default you would ship meanwhile. Marking it open is a *correct* answer here, not a failure.
- **Do not carry the inherited wording.** If the statement needs to be two requirements, or needs a word the original
  did not have, say so. You are completing it, not editing it.
- Write only your own file under `runs/20261005-attempt-limit/`.
- Work blind. Two other experts are answering the same brief and none of you will see the others until afterwards.
