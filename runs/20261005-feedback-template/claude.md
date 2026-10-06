# ui/ux dev feedback template — Claude (Opus 5.5), blind

Read before answering: `BRIEF.md`, method §3.0 (six whys), `docs/TASK_TYPES.md` ui/ux row. Nothing else in this folder.

## Template

`Changed / Why / Proof / Look / Effort`

This is the `code generation` template plus one field, **Look**, for the human checkpoint. **Accepted** moves off
the worker's summary and onto EJ's verdict.

| field | one line the worker writes |
|---|---|
| Changed | files / components touched |
| Why | which requirement in the prompt this change serves |
| Proof | the build/render command and its result |
| Look | where EJ sees it (screenshot, URL or steps), which states it shows, and which it does not |
| Effort | open: unit not given (see Q1) |

## The whys

**Accepted: removed from the worker's template**
1. *Why does it exist?* The ui/ux check ends with EJ's acceptance (TASK_TYPES row: "EJ's acceptance (last per 3.5)").
2. *Why not let the worker fill it?* The worker writes its summary before EJ has looked. All it can write is
   "pending", or a claim that EJ accepted, which it has no standing to make.
3. *Why does that matter?* A worker writing "Accepted: yes" is checking its own work, in the field a reader looks
   at first.
4. *Why not keep it as "pending"?* A field that always holds the same value tells the reader nothing, and teaches
   them to skip it. → **fact**: the summary comes before the acceptance.

**Look: added**
1. *Why does it exist?* The human checkpoint needs something to look at, and the worker knows where the change shows up.
2. *Why not let EJ find it?* Finding the right page, state and viewport costs EJ time, and EJ may look at a different
   state and accept that one instead.
3. *Why not put it inside Proof?* Proof is a machine check: the build exits 0. Look is what a human judges. If they
   share one field, "build passed" can stand in for "looks right".
4. *Why does that difference matter?* The row's sabotage test ("break a component → the build fails") only covers
   breakage. Whether the layout is wrong or the result is ugly, only the human check can tell, so the human check
   needs a precise input.
5. *Why name the states it does not show?* A screenshot shows a few states (empty/loading/error, narrow/wide). When
   EJ accepts it, EJ accepts only what it shows. Naming what is missing turns a silent gap into a visible one.
6. *Why believe that list is complete?* No one can. The worker lists only the gaps it knows about. →
   **unanswerable**, n=0.

**Proof: kept, narrowed to the command and its result**
1. *Why does it exist?* A loop needs an objective check on each pass, and this field records that check.
2. *Why the command and not a description?* A verifier can re-run a command. It cannot re-run an opinion.
3. *Why does that matter?* Without the command, the claim cannot be re-checked. → **fact**.

**Why: kept**
1. *Why does it exist?* It names the intent the change serves.
2. *Why not let EJ read the original prompt instead?* The worker's own restatement shows whether it misread the task.
   One line catches that before anyone looks at the screen.
3. *Why does that matter?* EJ's attention is the scarcest check in this loop. → **value judgement**, n=0.

**Changed: kept as in code generation**
1. *Why does it exist?* It tells the verifier how far the diff reaches.
2. *Why the same wording as code generation?* The ui/ux row is "codegen loop + human checkpoint". If the fields are
   the same, one verifier can parse both. → **fact** (the table row).

**Effort: kept, unit left open**
1. *Why does it exist?* The loop has a limit. A pass on attempt 5 of 5 tells you something different from a pass on
   attempt 1 of 5.
2. *Why not choose the unit here?* Attempts, tokens and minutes would each make a different rule. Picking one would
   be filling a gap with my own value. → **open for EJ**.

## Open for EJ (not invented)

- **Q1.** What unit does Effort count: attempts out of the limit, tokens, minutes, or something else? This applies to
  the code generation and test script templates too.
- **Q2.** Where does EJ's Accepted go: a blank `Accepted:` slot in the summary file that EJ fills in, or a separate
  verdict record?
- **Q3.** What form does Look take: a screenshot file, a URL, or steps? It depends on whether opencode or Codex can
  render headless in this setup, which I have not checked.
