# The 300-prompt corpus as a test — and what four engines said about the log

EJ's idea: run the algorithm over the whole corpus and have the engines review the **test log** rather than the
specification. Reviewing behaviour beats reviewing prose — a spec review finds *possible* defects, a log shows
*observed* ones with frequencies.

It worked, and it immediately produced the most useful result of the day: **the test could not fail, and four
engines said so unanimously.**

## What was run

`tests/workflows/corpus_check.py` — corpus × results × `docs/TASK_TYPES.md` × `design_gate.py`. For each prompt it
builds the default design the TASK_TYPES rows imply, runs the gate over it, and classes each disagreement as a bug.

| run | input | prompts | result |
|---|---|---|---|
| 1 | **perfect labels** — built from the corpus's own `exp` fields, so classification is correct by construction | 300 | **0 bugs, 300 designs passed** |
| 2 | real classifier output from the 20261002 campaign (codex, agy) | 150 | **73 genuine mismatches, 2 gate findings** |

The real-run logs look alarming — hundreds of `no result row` — but that is a coverage artifact: each results file
covers 25 of that round's 100 prompts. Separated out, the honest numbers are 73 mismatches across 150 classified
prompts and **2 gate findings across all 450 designs from both runs**.

## The review of the log

Four engines, one brief: the log, all of `design_gate.py`, all of `TASK_TYPES.md`, and six of the 300 designs that
passed. Their evidence was inlined, so each one saw the same thing.

| engine | model | time | findings |
|---|---|---|---|
| agy | `gemini-3.8-flash-high` | 160 s | 5 |
| claude | `claude-opus-5-5` | 73 s | 16 |
| codex | `gpt-6.1-sol` | 60 s | 7 |
| opencode | `MiniMax-M3.1-Flash-Preview` | 170 s | 9 |

**37 findings, 36 located, 1 discarded.** Every engine answered every question.

## A — the verdict on the green log: **4/4, it is a null result**

**The test is circular.** claude and opencode, independently:

> `testlog.md:6` — *"The test builds each design from the same TASK_TYPES rows that the gate parses, so in Run 1 the
> label-agreement check (G8), the edge checks (G4) and the reviewer checks (G6) are satisfied by construction."*
> `testlog.md:9` — *"0/300 only proves the emitter copies strings the gate then string-matches."*

**And the gate cannot reject.** Four independent reasons, each verified:

- `design_gate.py:146` — G3 checks that five **names** appear, not their contents. **Verified:** every node's
  `five_things` is exactly `['context','contract','evidence','state','tools']` with nothing behind them.
- `design_gate.py:150` — loop rules run only *if a loop exists*, and **the gate has no rule at all for a baseline or
  the three-part stop**, though the algorithm promises both on every node that builds.
- `design_gate.py:130` — G2 takes `builds` and `touched_paths` **from the design itself**, so the guard is
  self-referential.
- `design_gate.py:93` — the gate parses `pattern` and `sabotage` from every category row and `validate_design` uses
  them **0 times**. **Verified:** parsed at line 93, zero uses.

So half of step (2) — the sabotage that is supposed to prove a check can fail — never runs, and the gate's silence
carries no information.

## B — the mismatches are partly the table's fault: **4/4**

All three of agy, claude and opencode point at the same line, `TASK_TYPES.md:63`, without conferring:

> the use-case table *teaches* adding `information extraction` to "answer a question about existing code" prompts,
> while rule 2 forbids it as a pass-through. The models produce the pairing the table taught, and the expected
> labels penalise it.

That is an **algorithm defect discovered only by running the test and reading the failures** — and it is the
concrete answer to "is a bad score the model's fault or the definition's". claude adds the same shape at
`TASK_TYPES.md:120` (a table deliverable is information extraction per rule 2; "a report in data shape is still a
report" per rule 5) and codex at `:153` (`research and reports` vs `document and explain`).

**And opencode caught my own reporting:** *"The headline accuracies have no stated denominator and codex's 90% is
exactly rounds r2+r3 … which silently drops r1 where codex mismatched 25 of 25."* Correct. I quoted 90% without its
denominator, and r1 is where codex was worst.

## C — the designs that passed break the algorithm's promises: **4/4**

Observed in the artefacts, not hypothesised:

- **No baseline before the first builder.** claude: *"In p050 the first node is already the builder, with no baseline
  node before it."* **Verified:** `p050` node 0 is `code generation` with `needs=[]`.
- **Checks are placeholders.** claude: the node's check is *"a placeholder pointing back at the table, not the row's
  actual check"* — `default check for code generation (TASK_TYPES.md)`, nowhere near *"tests/build pass (script)"*.
- **No node names its own model or effort**, though the table promises every node does, and the gate never checks.
- **The engine split can defeat rule 5.** claude: code generation is split between opencode and Codex, so a
  `codex gpt-6.1-sol` reviewer reviews code Codex partly wrote — it passes G6 only because `engine_kind` reads the
  cell's leading token. That is my design, observed failing in the artefacts.

## D — what the log cannot see: **4/4**

- `pattern` and `sabotage` are parsed and never used, so the sabotage rule is unmeasured.
- **Every one of the 300 designs is `design_source: "default"`** (**verified: 300 of 300**), so the 20% challenger
  rule (G5) and the ledger checks (G7) never execute.
- The **checklist review layer** — the semantic layer the file itself says exists to catch what the script gate
  cannot — was never run.

## E — what would make the test decisive: **4/4 said the same thing**

**A mutation run.** codex: *"independently remov[e] node contents, baseline dependencies, stop conditions and
individual builders' different-kind reviewers, with explicit rejection expectations."* claude: *"Take each of the
300 passing designs and make known-bad variants (drop the reviewer; make the reviewer Codex on a Codex-split build;
empty five_things contents) …"* agy and opencode agree, and add running the checklist layer against the prompts.

That is the project's own sabotage principle, applied to the test instead of to a check: **a test that has never
rejected anything is not known to be able to reject.** We had the rule for script checks and never applied it to
the corpus.

## Files

- `testlog.md` — the log as reviewed (numbers, breakdown, six designs)
- `results_expected.jsonl` — perfect labels built from the corpus `exp` fields
- `designs/` — the 300 designs the gate passed
- `bugs_expected.md`, `real/*.md` — the harness logs
- `verify_log.py` — quote verification and grouping by question
- `brief-testlog.txt` (gitignored), `run_review.sh`, `agy.out`, `claude.out`, `codex.out`, `opencode.out`

## Not done

Nothing fixed. The recommendation, from all four engines and from the log itself, is the mutation run — it is the
one change that turns a green log into evidence, and it costs no model calls.
