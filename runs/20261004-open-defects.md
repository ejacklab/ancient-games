# What is not fixed — 2026-10-04

The register (`runs/20261004-defect-register.md`) holds 45 distinct issues. This file is the honest status of each
after the day's work, so the next session does not have to rediscover which ones are live.

**Headline: 2 of 45 are fixed, 3 are partial, 1 is addressed. 39 are open** — the 10 listed below plus 29 the table never had a status for because nothing touched them. The gate work changed the gate's
*ability to reject* — three real rules, found by the mutation matrix — but that was new ground, not the register's
list. Almost everything the four reviews found is still standing.

## Fixed, partial, and addressed

| # | status | what remains |
|---|---|---|

| 1.1 | **OPEN** | needs a schema change: five_things is a list of names with no content field to check |
| 1.2 | **OPEN** | needs a schema change: a design has no baseline field |
| 1.3 | **OPEN** | needs a schema change: a building node has no stop field |
| 1.4 | **PARTIAL** | G9 now reads `sabotage`; `pattern` is still parsed and used 0 times |
| 1.5 | **PARTIAL** | the builds/touched_paths contradiction now fires (G2); G2 still takes both fields from the design |
| 1.6 | **OPEN** | loop rules still run only when a loop is already present |
| 1.7 | **FIXED** | G3 rejects a check that names the table instead of stating what is checked |
| 2.1 | **OPEN** | the corpus run is still circular — designs are emitted from the cells the gate parses |
| 2.2 | **OPEN** | every emitted design is design_source=default, so G5/G7 still never run |
| 2.3 | **ADDRESSED** | tests/workflows/mutation_matrix.py exists and is a test; 18/18, self-check proves it can fail |
| 2.4 | **OPEN** | the checklist review layer has still never been run |
| 2.5 | **FIXED** | the corpus README states the denominators; codex's 90% is named as r2+r3 |
| 2.6 | **PARTIAL** | the harness now emits the row's sabotage; the pattern column is still unexercised |
| 4.3 | **OPEN** | my own error: the 3.8 mapping row says 'no step' and the skill carries 3.8 in steps 1 and 7 |
| 8.1 | **OPEN** | the engine split lets a codex reviewer review code Codex partly wrote |
| 8.2 | **OPEN** | DEFAULT_FALLBACKS['codex'] is Claude, so rule 5 can be lost after a fallback |

Nothing in the table above is marked FIXED unless a check would now catch its return:

* **1.7** — G3 rejects a check naming the table; the mutation matrix has a mutation for it.
* **2.5** — a documentation correction, not a mechanism.
* **2.3** is ADDRESSED rather than fixed: the mutation matrix exists, runs in the suite, reports 18/18 caught, and
  `--self-check` neuters every mutation to prove it can report a MISSED at all.

## The three that need a schema decision

They are the largest open family, and they share one cause: the design JSON cannot carry the thing the algorithm
requires, so no rule can look for it.

| missing | would reject | register |
|---|---|---|
| a `baseline` on a design that builds | **94 of 300 designs (31%)** | 1.2 |
| a three-part `stop` on a building node | 150 building nodes | 1.3 |
| `five_things` with contents, not just names | 150 building nodes | 1.1 |

Method 3.6 states the three-part stop is *"what lets a run end"*. The projection says a gate enforcing that would
reject about half the building nodes — so this is a change to the design format, and EJ's decision, not a rule
someone adds quietly.

## The rest, by why they are open

**Unchanged code (never touched today)** — the readiness script (§3: the blueprint check that can never fail, absent
directories reporting `verified`, the `--require` hole) and `intake.js` (§7: readiness before method 3.0, a git
snapshot as the baseline, loop-exit vocabulary).

**Doc drift (§4)** — four files disagree about the engine split, the quality count, `classification`, and the
`intake.js`/gate schema. All are edits; none needs a decision except 4.3, which is a row I wrote and a reviewer
corrected.

**Composition (§5, §6)** — work the algorithm requires and no step owns: the baseline's producer, the "what is
missing" pass, step 5 running before steps 6-7 bound it. These change the algorithm rather than correct a slip.

**My own construction (§8)** — the engine split defeating rule 5, and `DEFAULT_FALLBACKS` defeating it again after a
fallback. Both are live.

## Known, and deliberately not on this list

`agy` cannot take part in a headless review: it auto-denies the `command` permission it needs, and the escape it
suggests is the flag rule 3 forbids. Rule 2 routes research to agy, so routing and behaviour disagree. Recorded in
the run READMEs; not a defect of the algorithm.
