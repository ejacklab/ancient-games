Read the brief and the method's own why-table (`docs/WORKFLOW_DESIGN_METHOD.md:52`). Answer below; no files touched.

## Improved default: `Changed / Shown at / Why / Verdict / Effort`

| field | filled by | one line |
|---|---|---|
| **Changed** | worker | screens and components touched — and what else they render into that was *not* looked at (often "none") |
| **Shown at** | worker | route, viewport/device, data + interaction state on screen; screenshot path if one exists |
| **Why** | worker | the intent being served |
| **Verdict** | **human** | `accepted` / `accepted-with-changes` / `rejected` + the one thing the next round must do |
| **Effort** | worker | rounds spent on this screen (+ tokens or minutes if the run records them) |

## Whys

**Changed (kept, with a blast radius added)**
1. Why does it exist? → the human checkpoint needs a target; with none, the verdict is an opinion about nothing.
2. Why not files, as `test cases gen` does? → files are not what a human opens for UI; they open a route. A file list is the builder's address book, not the reviewer's.
3. Why add "what else it renders into, unchecked"? → UI work edits shared components; the human checks only the screen they were asked about, so a regression on a *different* screen is invisible by construction.
4. Why does that matter? → a type or layout error elsewhere in the product renders wrong while the build stays green. **← fact**
5. Why six? → who ranks the affected surfaces is a judgement about the design, and no rule can. Stopped; "none" is a valid fill.

**Shown at (this was `Proof`, renamed)**
1. Why does it exist? → a human verdict is only valid against what was actually shown; the same route renders differently per state and per viewport.
2. Why not `Proof`, meaning a command and its output? → in `code generation` Proof means a test run; there is usually no such run for UI, so the field would be empty or faked.
3. Why not drop it and trust the human to find the screen? → then each round spends human minutes rediscovering the state; the loop's exit condition *is* this human, so its latency is the loop's latency.
4. Why does the difference matter? → a reviewer shown an empty state, or the wrong breakpoint, rejects correct work and the next round "fixes" the wrong thing. **← fact**
5. Escape hatch: where the prompt implies an automated check (screenshot diff, a11y run), the LLM may propose replacing this field — the default-first rule. **← value judgement: a screenshot in chat beats a route name**

**Why (kept)**
1. Why does it exist? → the checkpoint judges intent-fit, not pixel-fit; intent is in the prompt, which the human may not have read closely.
2. Why not fold it into `Changed`? → "changed the modal spacing, per the brief's request for a wider sheet" and "changed the modal spacing, because the sheet must hold two columns" fail differently, and the second one is what tells the reviewer the worker understood the ask.
3. Why does it matter? → restating a requirement is where worker and client most often mean different things. **← value judgement**

**Verdict (was `Accepted`)**
1. Why does it exist? → it is the loop's only exit condition (method why-6: check kind = EJ).
2. Why not a boolean? → "no" without a reason hands the next round nothing new; the loop repeats the same screen.
3. Why not let the worker fill it? → whether a screen looks right is a taste judgement, the one thing a model cannot self-certify. Self-accepting makes the human checkpoint decorative — the loop stops on its own say-so. **← value judgement**
4. So it stays blank until the human writes it. I did not invent a default for it. **← unanswerable by anyone but the human**

**Effort (kept, weakest)**
1. Why does it exist? → it is the only field that says a loop is thrashing (three rounds, one screen).
2. Why is it weaker here than in `code generation`? → in a human-in-loop task the wall-clock cost is human wait, not tokens, so "Effort" mostly measures the wrong resource. **← fact**
3. Why keep it? → 3 rounds on one screen is the escalate signal, and it is free to report.
4. Open: drop it for human-in-loop types? **← open, your call**

## Where your brief is incompleteThree requirement gaps, per the rule in CLAUDE.md:

1. **"a worker fills each with one line"** — I have to break it: `Verdict` is filled by the human, not the worker, and `Shown at` (route + viewport + state + path) is one *line of text* but three *items*. Needs a unit: one sentence, or one item each?
2. **`Effort` has no unit** — rounds, tokens, or minutes? The whys above assume rounds.
3. **The human verdict has no home in the shape** — if it is blank until a person writes it, the run needs a way to know "worker done, waiting on human" vs "worker did not report". That is a state, not a field. Do you want it as a sixth field, or as run state outside the template?
