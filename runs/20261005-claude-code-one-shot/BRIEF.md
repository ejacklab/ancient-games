# A challenge to design a workflow for

Use the **`workflow-design`** skill in your skills list. It is the method this folder exists to package.

## The challenge, verbatim from the operator

> Debug the nightly timeout, fix it, grade tonight's run afterwards, and write the note for standup.

## What to produce

1. **`runs/20261005-claude-code-one-shot/design.json`** — the design, in the shape
   `.claude/skills/workflow-design/scripts/design_gate.py` accepts. Read that script; it is the gate your design
   will be checked by, and it will refuse a design that is vague or that skips its rules. You may run it yourself:

   ```
   python3 .claude/skills/workflow-design/scripts/design_gate.py runs/20261005-claude-code-one-shot/design.json
   ```

2. **`runs/20261005-claude-code-one-shot/NOTE.md`** — short. What you decided, what you were unsure about, and
   anything you assumed because the prompt did not say. If you had to ask a question you could not answer, say so
   here rather than inventing an answer silently.

## Rules

- Work it out yourself from the skill. Do not ask me anything; write your assumptions down instead.
- Do not edit anything outside `runs/20261005-claude-code-one-shot/`.
- When you are done, reply with only: whether the gate passed, and the one thing you were least sure about.
