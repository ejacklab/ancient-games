# Create the workflow-design algorithm page — a tab for humans

Create `docs/workflow-design-algorithm.html`: a self-contained, human-readable page presenting the workflow-design
method's algorithm (the method half of the framework). Style it to match `docs/ancient-games-algorithm.html`
(same CSS palette: green for the method).

## Source of truth — read these, do not work from memory
- `docs/WORKFLOW_DESIGN_METHOD.md` (sections 3.0–3.8, plus 4 State and memory, 5 Three qualities)
- `.claude/skills/workflow-design/SKILL.md` (the eight-step packaging, the "every node carries five things" table)

## Hard rules (a previous draft got these wrong — do not repeat)
1. **Match the source's sections exactly: 3.0 through 3.8 — all nine.** Do not merge them, do not invent a step
   name, do not renumber. Each section gets its one-line essence plus its check/why in a sentence.
2. Every step's essence must be traceable to a sentence in the method doc. No paraphrase that changes the meaning.
3. Include, near the bottom: the **five things every node carries** (tools, context, contract, evidence, state) and
   the **three qualities** (predictability, debuggability, quality control).
4. Self-contained HTML, no external assets, clean CSS, readable on a phone.

## For humans
Simple words where possible; where a term is needed (blueprint, six whys, unclear spot, baseline, pass-back), gloss
it in one clause or a small legend — like `docs/ancient-games-algorithm.html` does.

Print a summary of the sections you included and where each came from.
