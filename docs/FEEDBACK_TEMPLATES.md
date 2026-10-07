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
| 10–16 | the rest | — | **not yet walked** |

`Effort` goes on every loop type, unit `tokens + rounds`. Types whose source is code and whose check is "faithful
to source" (`document and explain`, `information extraction`; `repo scanning`, `code review`, `debugging` to come)
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

Still open for the `TASK_TYPES` row (not the template): who votes (sources or workers — "single node; voting" is a
contradiction), the corroboration number, undated-source policy, and staleness.

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
