I'll read the actual skill before answering — the question is about what those nine steps really do.
Read the skill (`.claude/skills/workflow-design/SKILL.md`) and the finding that already tested this question. Answer:

## 1. What the design still buys, sequentially

- **A falsifiable objective before any work** (understand). A prompt chain inherits the first prompt's framing. Six whys + in/out of scope make "done" checkable, and "a part that cannot be written" surfaces a misread while it still costs one paragraph.
- **Proved tools + blueprint check** (readiness). A chain discovers the missing binary or the unwritten requirement at step 7, having paid for steps 1–6. Here it is a preparation piece at the front.
- **The algorithm *is* the test.** Writing steps and their checks is the evaluation: a step you cannot write, or whose check you cannot name, is an unclear spot. A chain finds those by failing at them.
- **One batched question list.** One answer often removes another spot — asking one at a time asks the wrong one twice. Human attention is the scarcest input in the system.
- **A node-count budget.** With parallel gone, a split must buy context room or a different kind of eye; every extra node costs a fixed call, lost context and a join. The 3-step rule is what stops a sequential design decaying into a chain of one-liners.
- **Loops that terminate** — a check the worker cannot edit, an attempt limit, a tier exit as a *fresh* node (an in-session switch voids the prompt cache).
- **An artifact.** Design, state and evidence files make a run reviewable *before* it starts and resumable *after* it breaks. A prompt chain has only the conversation.

## 2. Worth it?

Conditionally, and the method says so: the tiny test routes you to a prompt file instead (SKILL.md:35 — Trial 1 cost ~309k tokens on a one-line README fix). Two steps genuinely lost their reason when parallel went: the five-condition independence test and join-contradiction handling. The rest were never about parallel — the whale finding (docs/research/20261002-whale-dolphin-hunting/FINDINGS.md:470) already concluded hand-offs buy nothing unless they buy a check, a different kind, or context room.

## 3. The one thing

**Acceptance criteria plus a recorded baseline, written before the first piece that builds.** Everything else above fires only when something goes wrong. This fires on the success path: it is the only element that makes "done" a test instead of the agent's momentum. A sequential chain has ordering, and no external stop.
