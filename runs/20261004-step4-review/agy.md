## 0. RESTATEMENT
Step 4 decides the execution structure for a piece of work. If a piece requires ≤3 steps and has no unknown spots, it becomes a simple **prompt file** (with an independent check if it carries high risk). Pieces with >3 steps should be split, but only if splitting changes the execution route and retains checks. All other cases, including blueprint unknowns, become a **workflow design**. Workflow designs start by applying default patterns from `TASK_TYPES.md`. These defaults can only be overridden by a challenger design if it formally proves a ≥20% cost reduction at equal coverage, which is reviewed by a script gate and a blind checklist pass. 

**Decision produced:** Whether a piece becomes a prompt file or a workflow design, and whether it splits into multiple pieces.

## 1. VERDICT
UNSOUND. 
The single most important problem is that an unsplittable >3-step task falls into a routing black hole in the diagram, bypassing both the prompt file and workflow design assignments entirely.

## 2. FINDINGS
| id | severity | what step 4 says (quote) | evidence (file:line, quoted line, or the counterexample) | why it fails | concrete fix (the smallest edit that removes the problem) |
|---|---|---|---|---|---|
| F1 | BLOCKER | "More than 3 steps → consider a new piece. Split only if..." | Diagram A1 (lines 39, 42): `S4 -->\|"more than 3 steps"\| SPLIT`, `SPLIT --> S5` | An unsplittable >3-step piece bypasses `DESIGN`, moving straight to `S5` without ever being assigned an execution method. | In the diagram, route `SPLIT` back to `DESIGN` when a split is rejected, and state ">3 steps unsplit → workflow design" in text. |
| F2 | BLOCKER | "≥20% lower projected run cost (tokens / agents / wall time)" | A5 (`design_gate.py:177-182`): `est = (d.get("estimate") or {}).get("tokens")` | The text permits challenging on wall time or agents, but the script gate hardcodes tokens, erroneously blocking valid cost-saving challengers. | Update `design_gate.py` to calculate the margin using the specific cost metric claimed in the design's `basis`. |
| F3 | MAJOR | "A spot of kind information or unknown always means a workflow design." | `.claude/skills/workflow-design/SKILL.md` step 4 (omitted) | Agents following SKILL.md will wrongly route pieces with "kind information" or "unknowns" as prompt files if they have ≤3 steps. | Copy the missing sentences regarding "kind information" and blueprint spots from §3.4 into SKILL.md. |
| F4 | MINOR | "every run reconciles its claim... n=0" | A4 (`TASK_TYPES_LEDGER.md`): `final (Reconciled)` has one `yes`. | The text claims `n=0`, but the ledger shows one default has been successfully reconciled. | Update the text in §3.4 and SKILL.md to `n=1`. |
| F5 | MINOR | "pipeline in `references/task-types.md`" | A2 (`docs/TASK_TYPES.md`) | SKILL.md instructs agents to read a non-existent path, breaking the lookup. | Change `references/task-types.md` to `docs/TASK_TYPES.md` in SKILL.md. |

## 3. CHECKLIST
| check | result | note |
|---|---|---|
| C1 | WEAK | "tier" is completely absent from step 4, and SKILL.md drifts from §3.4 by using "default" instead of "provisional assumption". |
| C2 | FAIL | The text and diagram completely fail to route a >3-step task that cannot be split, bypassing both PF2 and DESIGN. |
| C3 | PASS | `stages.py:109` splits by 3, `registry.py:24` sets CAP=3, and `stages.py:309` limits plan dispatches to 3 via `ctx.dispatch_count`. |
| C4 | PASS | It correctly overrides the standard hand-off cost rule by explicitly enforcing an independent check on tiny tasks strictly due to risk. |
| C5 | PASS | `TASK_TYPES.md` has all four columns, and explicitly instructs `others` to use the full method from first principles. |
| C6 | FAIL | `design_gate.py` rejects non-token metrics, and a design can indeed sacrifice debuggability since the gate only checks final coverage. |
| C7 | PASS | Matches `EXECUTOR_KINDS.md` routing ("risk-tiered — Sonnet 5.5 when nothing builds") and standard blindness rules. |
| C8 | FAIL | Counted 8 default data rows with 1 `reconciled` to `yes`; this directly contradicts the text's claim of `n=0`. |
| C9 | FAIL | SKILL.md omits crucial routing rules for "kind information" and "blueprint spots", and points to the wrong `TASK_TYPES` path. |
| C10 | WEAK | The empirical marks match the context, but the "Added 2026-10-01... n=0" mark is outdated given the ledger's current state. |

## 4. STRONGEST COUNTEREXAMPLE
**Task**: A 4-step log parsing script (read file, strip whitespace, extract regex, write to csv) using identical logic and engines throughout, where splitting does not change the route.
**Route it gives**: The diagram routes it to `SPLIT` then directly to `S5` (clear pieces run as loops), entirely bypassing the decision to make it a prompt file or a workflow design.
**Route it should give**: Workflow Design, because it exceeds 3 steps and cannot be cleanly split into separate routes.

## 5. WHAT I COULD NOT VERIFY
* Whether `ancient_games/registry.py:24` was corrected specifically on 2026-10-03, as file history/git blame is unavailable.
* Whether "EJ flagged high risk" is formally defined elsewhere, since it isn't listed directly in the `EXECUTOR_KINDS.md` table.

## 6. WHAT THIS CHECKLIST MISSED
* **Floating point strictness in the script gate:** `design_gate.py` enforces `abs(claim - recomputed) > 0.01`. If a challenger accurately claims `0.2` (20%) but the recomputed token reduction is `0.215` (21.5%), the gate fails it (`claim 0.2 != recomputed 0.215`). This forces the human claim to perfectly match the script's calculation down to 1%, penalizing designs that clear the bar by a wider margin than they conservatively claimed.
