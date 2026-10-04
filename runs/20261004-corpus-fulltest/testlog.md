# Test log — the workflow-design algorithm run over the 300-prompt corpus

## What was run

`tests/workflows/corpus_check.py`: corpus (300 prompts, `tests/fixtures/operator_prompts_r{1,2,3}.jsonl`)
x results x `docs/TASK_TYPES.md` x `design_gate.py`. For each prompt it builds the default design the
TASK_TYPES rows imply and runs the gate over it, then classifies each disagreement as a bug.

## Run 1 — perfect labels (300 prompts, no model calls, tests the MACHINERY only)

The results file is built from the corpus's own `exp` labels, so the classification step is taken as correct
by construction. Every bug here would be the algorithm's own fault.

```
bugs: 0 (none)
designs emitted: 300
```
So with correct categories, all 300 designs pass the gate.

## Run 2 — real classifier output (150 of 300 prompts; the campaign covered 25 per round per engine)

| engine | round | prompts classified | `no result row` | genuine mismatches | GATE findings |
|---|---|---|---|---|---|
| codex | r1 | 25 | 75 | 25 | 2 |
| codex | r2 | 25 | 75 | 4 | 0 |
| codex | r3 | 25 | 75 | 1 | 0 |
| agy | r1 | 25 | 75 | 21 | 0 |
| agy | r2 | 25 | 75 | 12 | 0 |
| agy | r3 | 25 | 75 | 10 | 0 |

**73 genuine mismatches across 150 classified prompts; 2 gate findings across all of
them.** Every `no result row` is a coverage artifact — the results file covers 25 of that round's 100
prompts — not a failure. Classification accuracy was measured separately on the two clean rounds:
sonnet-5.5 94%, codex 90%, agy 74%.

### What the mismatches are about

A sample of the actual reasons, verbatim from the logs:

```
codex r1: [MISMATCH] p001: cats result=['repo scanning', 'information extraction'] expected=['repo scanning']
codex r1: [MISMATCH] p002: cats result=['information extraction', 'document and explain'] expected=['research and reports']
codex r2: [MISMATCH] p130: builds result=False expected=True
codex r2: [MISMATCH] p139: cats result=['test script gen'] expected=['test cases gen']
codex r3: [MISMATCH] p231: cats result=['research and reports'] expected=['web search']
agy r1: [MISMATCH] p051: cats result=['debugging', 'information extraction'] expected=['debugging']
agy r1: [MISMATCH] p052: cats result=['code review', 'information extraction'] expected=['research and reports']
agy r2: [MISMATCH] p187: cats result=['research and reports', 'code generation', 'test script gen'] expected=['research and re
agy r2: [MISMATCH] p187: pipeline result=None expected='research → codegen'
agy r3: [MISMATCH] p271: pipeline result=None expected='research → codegen'
agy r3: [MISMATCH] p273: cats result=['debugging', 'code generation', 'grade a run', 'document and explain'] expected=['debugg
```

## Run 3 — a sample of the 300 designs that passed

The gate not firing is only good news if the designs are real. Six of the 300, chosen across categories:

### `p001`
```json
{
 "categories": [
  "repo scanning"
 ],
 "builds": false,
 "touched_paths": [],
 "pipeline": null,
 "nodes": [
  {
   "id": "n1",
   "category": "repo scanning",
   "engine": "agy (EJ, 2026-10-04)",
   "check": "default check for repo scanning (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": []
  }
 ],
 "design_source": "default",
 "estimate": {
  "tokens": 100000
 }
}
```

### `p050`
```json
{
 "categories": [
  "code generation"
 ],
 "builds": true,
 "touched_paths": [
  "product/x"
 ],
 "pipeline": null,
 "nodes": [
  {
   "id": "n1",
   "category": "code generation",
   "engine": "opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority)",
   "check": "default check for code generation (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": [],
   "loop": {
    "limit": 2,
    "exit": "fresh node on stronger tier with handoff note",
    "feedback": "the check's real output"
   }
  },
  {
   "id": "nr1",
   "category": "code review",
   "engine": "codex gpt-6.1-sol",
   "check": "fixed checklist; findings with file:line",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": [
    "n1"
   ],
   "reviews": [
    "n1"
   ]
  }
 ],
 "design_source": "default",
 "estimate": {
  "tokens": 100000
 }
}
```

### `p095`
```json
{
 "categories": [
  "research and reports",
  "code generation"
 ],
 "builds": true,
 "touched_paths": [
  "product/x"
 ],
 "pipeline": "research \u2192 codegen",
 "nodes": [
  {
   "id": "n1",
   "category": "research and reports",
   "engine": "agy (EJ, 2026-10-04)",
   "check": "default check for research and reports (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": []
  },
  {
   "id": "n2",
   "category": "code generation",
   "engine": "opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority)",
   "check": "default check for code generation (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": [
    "n1"
   ],
   "loop": {
    "limit": 2,
    "exit": "fresh node on stronger tier with handoff note",
    "feedback": "the check's real output"
   }
  },
  {
   "id": "nr1",
   "category": "code review",
   "engine": "codex gpt-6.1-sol",
   "check": "fixed checklist; findings with file:line",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": [
    "n2"
   ],
   "reviews": [
    "n2"
   ]
  }
 ],
 "design_source": "default",
 "estimate": {
  "tokens": 100000
 }
}
```

### `p150`
```json
{
 "categories": [
  "document and explain"
 ],
 "builds": false,
 "touched_paths": [],
 "pipeline": null,
 "nodes": [
  {
   "id": "n1",
   "category": "document and explain",
   "engine": "Sonnet 5.5",
   "check": "default check for document and explain (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": []
  },
  {
   "id": "n1r",
   "category": "code review",
   "engine": "claude sonnet 5.5",
   "check": "review against source: fixed checklist, facts traceable",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": [
    "n1"
   ],
   "reviews": [
    "n1"
   ]
  }
 ],
 "design_source": "default",
 "estimate": {
  "tokens": 100000
 }
}
```

### `p200`
```json
{
 "categories": [
  "research and reports"
 ],
 "builds": false,
 "touched_paths": [],
 "pipeline": null,
 "nodes": [
  {
   "id": "n1",
   "category": "research and reports",
   "engine": "agy (EJ, 2026-10-04)",
   "check": "default check for research and reports (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": []
  }
 ],
 "design_source": "default",
 "estimate": {
  "tokens": 100000
 }
}
```

### `p271`
```json
{
 "categories": [
  "research and reports",
  "code generation",
  "test cases gen"
 ],
 "builds": true,
 "touched_paths": [
  "product/x"
 ],
 "pipeline": "research \u2192 codegen",
 "nodes": [
  {
   "id": "n1",
   "category": "research and reports",
   "engine": "agy (EJ, 2026-10-04)",
   "check": "default check for research and reports (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": []
  },
  {
   "id": "n2",
   "category": "code generation",
   "engine": "opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority)",
   "check": "default check for code generation (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": [
    "n1"
   ],
   "loop": {
    "limit": 2,
    "exit": "fresh node on stronger tier with handoff note",
    "feedback": "the check's real output"
   }
  },
  {
   "id": "n3",
   "category": "test cases gen",
   "engine": "opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority)",
   "check": "default check for test cases gen (TASK_TYPES.md)",
   "five_things": [
    "context",
    "contract",
    "evidence",
    "state",
    "tools"
   ],
   "needs": [
    "n2"
   ]
  },
  {
   "id": "nr1",
   "category": "code review",
 
```
