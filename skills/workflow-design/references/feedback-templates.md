# Feedback templates — per task type

The summary shape a worker reports back at the end of a task, so a verifier reads a known shape instead of free text.
Design rule: **default-first** — the table carries the default; the LLM may propose a better one from the actual
prompt, with a written reason and at least the default's coverage.

**The one rule over all of them (EJ, 2026-10-05): every field has a writer, and the writer is the worker.** A return
template is the worker's output. The human's verdict, the design's decision, the COO's call — those live in the
loop's exit and the state file, not in the worker's summary. *"We are doing things for who."*

## Decided so far (walked through 1-by-1 with EJ, 2026-10-05)

| # | type | loop? | template (worker-filled) |
|---|---|---|---|
| 1 | `code generation` | yes | `Changed / Why / Proof / Effort` |
| 2 | `test script gen` | yes | `Created / Run / Effort` |
| 3 | `test cases gen` | no | `Created / Type / Coverage / Location` |
| 4 | `ui/ux dev` | yes | `Changed / Look / Why / Effort` |
| 5 | `debugging` | yes | `Bug / Fixed / Test / Effort` |
| 6 | `test data gen` | no | `Created / Schema / Coverage / Source` |
| 7 | `document and explain` | no | `Written / Source (code + graph) / Format` |
| 8 | `information extraction` | no | `Extracted / Source (code + graph) / Schema` |
| 9 | `web search` | no | `Found (FACT / INFERRED / GAP) / Disputed` |
| 10 | `classification` | no | `Labels / Labeled / Unlabelable / Why` (batch; `T` from the brief) |
| 11 | `code review` | no | `Against / Method / Findings (suggested fix) / Unclear` |
| 12 | `multi step planning` | no | `Objective / Nodes / Coverage / Method / Unclear` |
| 13 | `repo scanning` | no | `Scope / Coverage / Findings / Source (code graph) / Unclear` |
| 14 | `research and reports` | no | `Answer / Findings (CONFIRMED / INFERRED / GAP / UNPROVEN) / Gaps` |
| 15 | `grade a run` | no | `Run / Against / Rubric / Unclear` |
| 16 | `others` | — | `Done / Evidence / Findings` (+ `Effort` if the design runs it as a loop, + `Source` if it has one) |

**Rows 12–16 are proposals merged from three runs (`runs/20261006-feedback-remaining/`, attempt 2 of each), not yet
walked with EJ.** They are marked `n=0` until EJ settles each.

`Effort` goes on every loop type, unit `tokens + rounds`. Types whose source is code and whose check is "faithful
to source" (`document and explain`, `information extraction`, `repo scanning`, `code review`, `debugging`)
carry the code-graph tool, and `Source` names the graph.

### `web search` (minimax's shape, chosen by EJ)

```
## Summary
- Searched: <N queries — M near>
    <keyword>           — near | far     (results close to, or far from, the query)
    <refined keyword>   — near           (derived from "<original>" because <reason>)
- Found:
    FACT     <claim> — <publisher, published YYYY-MM-DD | "undated", URL>  [N sources — independent | same]
    INFERRED <claim> — <why it follows from the FACT lines>
    GAP      <asked fact> — not found; searched: <query, where>; or: exists at <URL> but undated
- Disputed: <fact> — <k of n> say A (<sources>), <m> say B (<sources>), split <why>; or: none found
```

`Searched` is the web-search `Effort`: the query log plus accuracy. "accurate" = the returned results are **near**
the query (relevant), not off-topic — a `near | far` judgment the worker writes (only it saw the results). Refined
keywords are marked with what they replaced and why. (EJ, 2026-10-06.)

### `code review`

```
## Summary
- Against:  <what it reviewed against — the checklist/spec>
- Method:   <what it actually did, and why any deviation from the default>
- Findings: <N — each: file:line, rule broken, what's wrong, suggested fix (optional)>
- Unclear:  <anything ambiguous, left for the COO>
```

`Method` and `Why` are one field: the worker can honestly write "why I deviated from the default", not "why the
design chose a blind review" (that is in the brief). `Unclear` is the `UNCLEAR:` escape's home. Two kinds of
suggestion: a **fix** rides with its finding; an **enhancement** (a new wish) goes to `docs/blueprint/backlog.md`,
never into the review — findings are checkable, enhancements are unbounded (the method step 8).

### `classification` (batch labeling — EJ's correction, 2026-10-06)

Classification is **sorting/labeling a batch of data** (e.g. "which business rule belongs to which call-file type"),
not one item -> one label. The return is the labels plus two counts. All three experts agree; the argued point was
resolved: the **unlabeled count is the worker's field** (only it tried every item), while **"labeled wrong" is the
verifier's** (from the sample) — two different numbers, two writers.

```
## Summary
T = <batch size from the brief — not re-derived>
- Labels:       <item -> label(s), one line each — several allowed, may be proposed>
- Labeled:      <N of T>
- Unlabelable:  <M of T>
- Why:          <item -> reason, one line per unlabelable item>
```

Settled (EJ): several labels allowed (`item -> label, label`); no cap — the list is the list; "refuse" is just
`Unlabelable`; labels may be proposed, not locked to a pre-given set. Still open: whether the unlabeled reason
(reported, not verified) needs a check.

Still open for the `TASK_TYPES` row (not the template): who votes (sources or workers — "single node; voting" is a
contradiction), the corroboration number, undated-source policy, and staleness.

### `multi step planning` (proposed, n=0)

```
## Summary
- Objective: <challenge restated — what is true when done, in scope, out of scope; copied from the challenge>
- Nodes:     <one line per node — id, category, engine, check, deliverable, `needs`, loop | no-loop; where design.json
              lives; touched_paths and baseline.command as values, not promises>
- Coverage:  <acceptance-criterion ids and checks the nodes cover — and those NOT covered>
- Method:    <default | challenger; a challenger's margin (>= 20%), basis and arithmetic; default reads "default, unchanged">
- Unclear:   <spot — read A, chose A because ...; or "none">
```

No `Effort` (not a loop), no `Source` (the source is the challenge, not code), no gate result or `Accepted` (the gate and
the reviewer write those after the worker).

### `repo scanning` (proposed, n=0)

```
## Summary
- Scope:    <area; one row per section — id, files and graph nodes, budget, `git rev-parse --short HEAD`; what was left unscanned>
- Coverage: <per section, what IT read and skipped — nodes, functions, edges, files, counts against the graph's `stats`;
             claims resting on `unresolved_calls` are `read`, never facts>
- Findings: <one line each — claim, file:line, verbatim quote (>= 8 chars), read | ran; no severity, no fix>
- Source:   <the code-graph command, schema, tier, root, stats, and every entry in `errors`>
- Unclear:  <each spot the scan could not settle, with file:line; or "none">
```

`Coverage` is written by each section worker; the join concatenates the rows and does not re-derive them. No `Effort`,
no `Verdict`.

### `research and reports` (proposed, n=0)

```
## Summary
- Answer:   <what is true in answer to the question, naming the finding ids it rests on; an unsettled part is written as unresolved>
- Findings: <id claim — CONFIRMED | INFERRED | GAP | UNPROVEN — both sides: <A> | <B>; each side a file:line with a verbatim quote
             (>= 8 chars) or a URL with its published date (or "undated"); "— none" when no source opposes>
- Gaps:     <what the question presupposed that no finding settles, where it was looked for, why open; or "none">
```

`INFERRED` names the `CONFIRMED` rows it follows from; `GAP` names the query run and where. No `Disputed` (the
both-side citation sits on the row), no `Effort`, no `Source`.

### `grade a run` (proposed, n=0)

```
## Summary
- Run:     <the run directory graded, copied from the brief>
- Against: <rubric path or id and version, copied from the brief>
- Rubric:  <per dimension: `<dimension> — PASS | FAIL — <path:line inside the run directory>`, or
            `<dimension> — UNKNOWN — looked for <what> at <path>: absent`; no total, no score>
- Unclear: <each dimension that could not be applied as written, and the reading used; or "none">
```

Per dimension the value is `UNKNOWN`; the run as a whole is `INVALID_RUN` (decided 2026-10-08). An empty run directory gives
UNKNOWN everywhere and `INVALID_RUN`, never PASS. `VALID` / `INVALID_RUN` is the VERIFIER's line, derived from the `Rubric` rows (any `UNKNOWN` dimension
=> `INVALID_RUN`); the worker does not self-report it.

### `others` (proposed, n=0)

```
## Summary
- Done:     <one line per deliverable, with where it is (a path, or "inline below")>
- Evidence: <per Done line: a re-runnable check and what it showed, or a file under runs/<run-id>/; or "none — unchecked">
- Findings: <what the work found that is not a deliverable, one line each; or "none">
- New type: <proposal — this matched no known type; pattern, engine, check, sabotage>  (propose when it looks recurring)
```

`Effort` (tokens + rounds) only when the brief says the design runs the node as a loop; `Source` (naming the code graph
when the source is code) only when there is a source. `others` is a placeholder, not a permanent type: a task that matches no row is run from first principles, and the `New type` proposal goes to the COO, who asks the three experts to design it and add it to `TASK_TYPES.md` + `FEEDBACK_TEMPLATES.md`. `unclear` is different — it means "cannot be done", which stops and reports via `UNCLEAR:`..

`Effort` goes on every loop type, and its unit is **`tokens + rounds`** (both already measured and harvested).

## Field meanings (the shared vocabulary)

| field | what it is |
|---|---|
| `Changed` | files/components touched, one line each — and *what else it renders into, unchecked* (blast radius) |
| `Created` | the tests/cases produced, one line each |
| `Type` | unit / integration / negative / boundary / regression |
| `Coverage` | which acceptance criteria the cases exercise (`R1.1`, `N1.1`, …) |
| `Location` | where each test lives and what code it targets — `file:line` |
| `Run` | the result of running the tests — green, and against what |
| `Look` | route + viewport + state, **and which states it does NOT show** |
| `Why` | the one-line intent the change serves |
| `Proof` | the check that ran and passed (re-runnable) |
| `Effort` | tokens + rounds — cost and thrash |

## Provenance of the design

Walked through one type at a time with EJ. `ui/ux dev` was also given to Claude Code (Opus 5.5) and MiniMax with the
six whys; both independently found that `Accepted`/`Verdict` does not belong in the worker's return (the worker writes
before the human looks), which is how the "who fills it" rule was born.
