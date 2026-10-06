# test data gen — return template (deepseek-v4-pro)

## Template

```
## Summary
- Created:  <each data/fixture, one line>
- Schema:   <schema check result: passed/failed — validator or command>
- Coverage: <the edge cases covered>
```

## Changes from the proposal

- **`Validated` → `Schema`, and the content reports the run's outcome, not a stamp.** The proposal's `Validated: <schema validation passed>` can only be true on success; a summary must be able to hold a failure too, and it should name the validator so the verifier can re-run the same check.
- **No `Location` line.** The fixture path is already the evidence path in the result file; adding a worker-written copy gives one fact two writers.
- **No `Effort`.** Single node, not a loop.

## The six whys

### `Created` — kept
1. **Why** — the verifier must be able to name what was produced before checking it.
2. **Why** — the check (schema validation + edge-case coverage) runs on specific files; you cannot validate a file you cannot identify.
3. **Why one line each** — each fixture is a unit of the deliverable, so one line per file keeps the list enumerable against `Coverage`.
- **Bedrock:** the deliverable is what the check runs on (fact from the brief).

### `Validated` → `Schema` — changed
1. **Why** — `Validated: <passed>` can only ever be true, so on a failed run the worker must lie or leave it empty.
2. **Why** — the worker is reporting their own check run, not the verifier's verdict; the verifier re-runs the schema check as the check anyway.
3. **Why** — a field that only says "passed" carries no information beyond a claim the verifier will redo; it earns its place only by naming the validator/schema and reporting the real outcome, pass or fail.
4. **Why rename to `Schema`** — a field called "Validated" that can read "failed" contradicts itself; `Schema` names the thing checked, not the verdict, so the writer stays the worker.
- **Bedrock:** a verdict lives elsewhere; the worker reports what they ran and what happened (the brief's own rule).

### `Coverage` — kept
1. **Why** — the check's second half is literally "edge-case coverage list", so the summary must expose the list for the verifier to compare.
2. **Why the worker writes it** — which edge cases were designed into the data is the worker's intent, known only at write time.
3. **Why intent over inspection** — checking is comparing a claim to a requirement; with no worker list there is nothing to compare the requirement against.
- **Bedrock:** the check defines the coverage list (fact from the brief).

### `Location` — not added
1. **Why** — the result file already carries the evidence path, which is where the fixtures live.
2. **Why redundant** — a second field for the same fact gives one fact two writers.
3. **Why two writers is wrong** — the worker's hand-copied path can go stale when a file moves; the harness-written path cannot, because the system writes it the moment it places the file.
- **Bedrock:** one fact, one writer — the people-form of the brief's one rule.
- **Open (only the author can settle, blind):** if fixtures can ever be written somewhere the harness-recorded path does not point to, `Location` earns its place. Otherwise it stays out.

### `Effort` — confirmed absent
1. **Why** — Effort goes on every *loop* type; test data gen is a single node.
2. **Why loopness decides** — tokens + rounds only mean something across rounds; a single node has one round, so Effort would be a constant.
3. **Why drop a constant** — a field that always says the same thing tells the verifier nothing and costs the worker a write.
- **Bedrock:** "Effort on every loop type" + "single node" (both facts from the brief).
