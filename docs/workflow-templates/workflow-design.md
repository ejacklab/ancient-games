# Workflow design — <run id>

A design, not a run. Sequential by default. Method: `docs/WORKFLOW_DESIGN_METHOD.md`.

## Questions for EJ (answer before running the designed workflow)

| # | Question | Provisional assumption | Blueprint section (or none) |
|---|---|---|---|

## Blueprint

- Kind of task: <not a product change | fix | feature | new product>. Map: <path, or none>.
- Acceptance criteria in scope: <R1.1, …, N1.1, …>. These are the run's success criteria. Where a blueprint piece
  is to write them, name the criteria you expect it to propose; they are fixed when EJ accepts that piece.
- A piece that builds stops when its criteria pass, what passed before still passes, and its "must not change" holds.
  Anything else found — a new wish, an improvement, a gap no criterion in scope covers — goes to
  `docs/blueprint/backlog.md`, not into this run.

## Pieces, in the order they run

One block per piece. A piece has at most 3 steps unless a reason is given. Every piece carries five things: tools,
context (the brief), a contract, evidence, and state. Contract and evidence names follow `ancient_games/schema.py`
where they fit (INTENT, STOP, OUTPUT, SCOPE; CLAIMS, NOT_ESTABLISHED).

### <piece id> — <name>

- **Steps:** 1. … 2. … 3. …
- **More than 3 steps because:** <reason, or leave out>
- **Pattern:** step (do once, check) · loop (attempt, check, repair) · explore (bounded search for an unknown)
- **Resolves unclear spot:** <spot id, or none>
- **Builds:** <yes: changes the product's code, schema, UI or configuration / no>
- **Blueprint sections it depends on:** <sections, or none>. If it builds, it does not start while any of them is
  unsettled; if not, it may use draft sections and its output names the drafts it assumed
- **Acceptance criteria it covers:** <R1.1, … — required when it builds; its stop names them, plus "what passed
  before still passes" and its "must not change">
- **Check:** <what decides done> — kind: script / checklist judged by a separate agent / EJ
- **Attempt limit:** <n> (loops and explores)
- **Feedback on failure:** <what goes back to the agent — the check's real output>
- **Exit when the limit is hit:** <back to the unclear list / to EJ>
- **Needs the result of:** <piece ids, or none>
- **Contract — intent:** <one sentence: why this piece exists>
- **Contract — stop:** <the condition that ends the piece, stated so it can be observed>
- **Contract — returns:** <what comes back and in what shape: the file, its headings or fields>
- **Contract — may change:** <paths the piece may create or edit>
- **Contract — must not change:** <paths or things that are off limits>
- **Evidence — what comes back:** <the proof for the result: the command and its output, or file:line — never "it works">
- **Evidence — saved in:** <the file the proof is written to; a verifier reads this, never the worker's reasoning>
- **State — reads:** <what it takes from the state file before it starts>
- **State — writes:** <what it records in the state file when it finishes>
- **Context — given:** <exact files and facts this agent gets>
- **Context — withheld:** <what it must not see, e.g. the worker's reasoning for a verifier>
- **Tools and skills:** <…>

## Joins

<where results from separately resolved spots or branches are compared; a contradiction is a stop>

## Parallel candidates (optional — decided last)

Only pieces for which all five hold. Otherwise they stay sequential.

| Pieces | Neither needs the other's result | No shared files or resources | One would not change how the other is done | Each has its own check | Time saved is worth the join |
|---|---|---|---|---|---|

## Predictability

- Agents in total: <n>. Bounds: <attempt limits, concurrency>.
- Cost estimate: <tokens or a range, and what it is based on>.
- Success criteria, written before the run: <for a product change, the acceptance criteria in scope>

## Debuggability

- Agent labels: <…>. Every step's input and output file: <…>. Resume point after a failure: <…>.

## Quality control

- Which checks are scripts, which are judged, which are EJ's.
- How each script check is shown to be able to fail (sabotage check).
- The final "what is missing" pass: <who, what it looks at>. It measures against the acceptance criteria in scope;
  what it finds outside them goes to the backlog.
