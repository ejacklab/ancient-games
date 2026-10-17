# P4 judge — map-session.json against the M1 key (Claude opus subagent)

## Map shape

- 502 definitions.
- 3,930 links:
  - 1,084 resolved to an implementation;
  - 39 ambiguous;
  - the rest unresolved, each with its own reason.
- 8 entries.
- The `limits` list holds only 4 records, one per reason, not one per place. So the judge counted an unresolved link
  whose reason names the place as **limited**.

## Totals (61 key claims)

| Status | Count |
|---|---|
| held | 26 |
| limited | 8 |
| missed | 21 |
| wrong | 2 |
| n/a | 4 |

Of the 21 missed:
- 7 sit outside the query: tests, `tool.ts` and `tool/runtime.ts`.
- 10 are the steps of `attempt`, which is not an entry.
- The rest are a constant, a `yield* SessionStep.make` construction, a function passed as a value, and a callback
  that was not followed.

## Why claims were wrong

The two wrong claims share one link. At llm.ts:248, `steps.attempt` is labelled "implemented outside the repository".
The map's own definitions hold it at step.ts:73.

The judge found more wrong links of the same kind outside the sample. Each was checked in the code:
- At step.ts:99, :128, :130 and :208, the publisher calls are labelled outside the repository. They are defined at
  publish-llm-event.ts:604, :617 and :378.
- `new StepFailedError` at step.ts:280 and llm.ts:221 is labelled outside the repository. The class is at
  error.ts:45-51.

## Ten random links

All 10 are correct. Most were easy library calls, so the sample says little about links inside the repository.

## Not verified

The judge's own reading, not traced through the types: inbox.ts:328 `.returning` is labelled "no implementation
found", although delete.ts:198 defines it.
