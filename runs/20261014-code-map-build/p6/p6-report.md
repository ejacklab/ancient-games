# P6 — the code-map skill inside a workflow-design run, round 1

## Setup

- **Tasks:** three real change tasks on opencode, one per module (`prompt-task1..3.md`). Each asks for a design only,
  through the workflow-design skill, including its explorer step.
- **Arms:** two arms per task, on the same model (claude-sonnet-5-5, `claude -p`, fresh session). Both arms have the
  same tools: Read, Grep, Glob, Skill and `Bash(bun:*)`.
  - The **with** arm also loads the `code-map` skill as a plugin (`--plugin-dir p6/plugin`). The skill is the A5
    tool, frozen.
  - The **without** arm does not.
- **Who decides:** the agent chooses whether to use the skill. Nothing in the prompt names it.

## Results

| Task | Arm | Turns | Wall time | Total tokens | Output tokens | Cost (USD) | Skills used | code-map calls | Reads | Greps |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 session | with | 60 | 292 s | 2,219,988 | 36,734 | 1.13 | workflow-design | 0 | 51 | 49 |
| 1 session | without | 47 | 254 s | 2,168,594 | 28,334 | 0.93 | workflow-design, requirement-check ×2 | 0 | 36 | 26 |
| 2 tool | with | 50 | 315 s | 2,249,111 | 36,165 | 1.22 | workflow-design, requirement-check | 0 | 50 | 22 |
| 2 tool | without | 57 | 311 s | 1,940,639 | 36,657 | 1.05 | workflow-design | 0 | 54 | 40 |
| 3 ai | with | 51 | 295 s | 2,638,582 | 34,236 | 1.17 | workflow-design, requirement-check | 0 | 51 | 25 |
| 3 ai | without | 55 | 393 s | 3,586,257 | 49,653 | 1.53 | workflow-design, requirement-check | 0 | 35 | 29 |

- **The skill was offered and never used:**
  - The with-arm sessions list it: the transcript shows the line "code-map:code-map: Answer one question …".
  - In none of the three did the agent call the skill or run the tool.
  - Its explorer step read and grepped, the same as the arm without the skill.
- The token and time differences come from two runs that each read and grepped. They do not measure the tool.
- No blind judge was run on the designs. Neither arm used the tool, so a quality comparison would compare two runs
  that differ only by chance.

## What it shows (my reading)

- In this setup, the agent does not reach for the code-map skill. Three things may play a part:
  - workflow-design's explorer step (method 3.8 item 10) says how to read code and does not mention a map;
  - the skill's description competes with plain reading, which the agent already knows;
  - the tasks fit in a few files.
- This is a finding about the method and the skill's trigger. It is not one about the tool's answers. P6 may not
  change the method or its skill text, so it goes to EJ as a request.

## What it does not establish

- n = 1 per arm per task, one model and one version of the tool.
- Whether a design is better when the explorer does use the map. That needs an arm told to use it, which is a
  different question: forced use against free choice.
