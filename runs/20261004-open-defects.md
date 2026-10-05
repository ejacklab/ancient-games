# What is not fixed — 2026-10-04

The register (`runs/20261004-defect-register.md`) holds 45 distinct issues. This file is the honest status of each
after the day's work, so the next session does not have to rediscover which ones are live.

**Headline (after the format change, 2026-10-05): 7 of 45 are fixed, 3 are partial, 1 is addressed. 39 are open** — the 10 listed below plus 29 the table never had a status for because nothing touched them. The gate work changed the gate's
*ability to reject* — three real rules, found by the mutation matrix — but that was new ground, not the register's
list. Almost everything the four reviews found is still standing.

## Fixed, partial, and addressed

| # | status | what remains |
|---|---|---|

| 1.1 | **FIXED** | FIXED — G3 requires the five things' contents (check_five); the five names are gone |
| 1.2 | **FIXED** | FIXED — G10 requires `baseline.command` and an owner; the harness emits it |
| 1.3 | **FIXED** | FIXED — the stop carries method 3.6's three parts, in both the gate and intake.js |
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

## Closed by the format change — 2026-10-05

EJ ruled on the one question: **should the gate validate contents, using the fields `intake.js` already defines?**
Yes. One shape, and the gate reads it.

| # | what closed it |
|---|---|
| **1.1** | `check_five` requires the five things as **contents** — brief_given, intent, a three-part stop, returns, state, tools, evidence. The list of five names is gone from both sides. |
| **1.2** | **G10**: a design that builds must carry `baseline.command` and name who captures it. |
| **1.3** | The stop carries method 3.6's **three parts** (`criteria`, `baseline`, `must_not_change`), in the gate and in `intake.js` alike. |
| **4.5** | The gate and the runnable form finally share **one shape** — `design_gate.py` reads the fields `intake.js` emits. |
| **8.3** | A bare template list cannot pass, because there is no list to pass. |
| **5.1** | **PARTIAL.** The design must now name the baseline's owner — a step id or the literal `script` — so the blank the method left is gone. Which step in the run's own step list does it is still open. |

The mutation matrix went from **18/18 caught plus 3 holes** to **23/23 caught, 0 holes, 0 missed, 0 false alarms**.
That is the measurement: the three mutations that used to break what the algorithm requires with no rule to catch
them are now caught by a rule, each with its own mutation.

Cost, as projected: 94 of 300 designs needed a baseline (31%), 150 building nodes needed the three-part stop, and
150 needed contents. The harness emits all three now, so the corpus is 0 bugs again — for the right reason this
time, since the designs carry the substance rather than a list of its names.

**Two of the five names still have no field of their own.** `tools` and `evidence` are defined here for the first
time, with the minimum that makes them meaningful (a tool may be used; output lands somewhere). They are thinner
than `context`, `contract` and `state`, and that is worth knowing before building on them.


## Settled without a new decision — 2026-10-05

EJ: *"if already answered, please go fix it."* Six items were blocked on a decision that the code, or an earlier
answer, had already made. Checked one at a time against the files, and fixed or confirmed:

| # | what settled it |
|---|---|
| **4.4** | The role map sent classification to `agy`/`gemini-3.1-pro-high`. EJ's own instruction this session — *"classification is using Deepseek v4.1 flash"* — and the routing table 80 lines below it both say DeepSeek. The stale row is corrected. |
| **4.8** | The use-case table taught `repo scanning, information extraction` for "answer a question about existing code". Of 300 labelled prompts, **17 are `repo scanning` alone and 0 pair the two**. The table now matches the measurement. |
| **7.2** | The design carries `baseline.command` (G10), so `intake.js`'s V6 verifies **the recorded test command**, not a `git status` snapshot — a snapshot cannot tell a passing product from a broken one, which is what part 2 of a building node's stop measures. |
| **6.1** | Not undecided: `engines.py:157` `DEFAULT_FALLBACKS` maps every engine, and `intake.js` carries `attempt_limit`. Pinned by `test_dispatch.py:129`. |
| **6.2** | Not missing: `dispatch.py:41` sets `max_rounds: 2` and `:292` enforces it. Pinned by `test_rounds_cap_blocks` (`test_dispatch.py:145`) — the register's claim was simply wrong. |
| **8.1** | The split is handled: G6 requires a reviewer of a different kind from each build group it reviews. The corpus passes, and there is now a mutation for the split case specifically. |

The mutation matrix is now **24/24 caught, 0 holes, 0 missed, 0 false alarms** — the 24th is 8.1's own case.

Two of the six were the register being **wrong**, not the design being open: `6.2`'s limit has been in the code and
under test the whole time.


## 5.6 — the code half was false, and the real half was a bug

The register said: *"`others` has no engine, yet 3.2 sends every unmatched piece there and 3.6 requires every node to
name an engine."*

Checked against the method: **no step requires a node to name an engine.** 3.7 says a node names *its own* role,
engine, model and effort, and 3.2 says an unmatched piece *"is `others` and gets the full method from first
principles"* — so `others` having no table default is the design, not a gap.

What was real, and nobody had noticed:

* The table's engine cell for `others` is `—`. The harness read that cell straight into `ENGINES`, so an
  `others` piece produced a node whose engine was **an em dash**.
* `engine_kind("—")` returned `unknown`, and **the gate accepted it**: `p297` and `p300` were passing designs that
  could not be dispatched.
* Two `ENGINES` maps existed; fixing the module-level one left the local copy at `corpus_check.py:236` still
  passing the dash through, which is why the first fix appeared not to work.

Fixed: **G11** rejects any node whose engine is not an engine; the harness resolves `others` to a documented
`deepseek deepseek-flash` and says why. The mutation matrix is **25/25 caught, 0 holes**.

**The question this leaves** is smaller and real: `others` is exempt from the category checks (G2), so a piece
nobody could classify **may build product code** — now with an engine the harness chose, not the method. Whether
that is allowed is EJ's call, and it is the only part of 5.6 that was ever a decision.
