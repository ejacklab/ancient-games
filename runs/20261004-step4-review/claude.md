## 0. RESTATEMENT

Count the algorithm's steps (§3.2: one action with a nameable check). The rule below applies only when no step is unclear.

- **Three steps or fewer, nothing unclear except decisions that carry a provisional assumption:** one piece, and the output is a prompt file with those decisions listed as questions at the top.
- **Any information or unknown spot, or a missing or incomplete blueprint section:** a workflow design, whatever the step count.
- **More than three steps:** "consider" a new piece, and split only if each part keeps its own check and the split changes the route.
- **Risk is judged separately.** A tiny but risky task gets a prompt file plus one independent check.
- **Workflow design:** start from the `TASK_TYPES.md` row for each piece. A challenger replaces it only on a written claim of ≥20% lower cost at equal coverage. The claim goes through `design_gate.py` plus a blind checklist pass and is logged in the ledger.

**Decision produced:** prompt file (one piece) or workflow design (per labelled piece). For more than three steps the rule gives no decision.

## 1. VERDICT

**SOUND WITH FIXES.** The most important problem is that the ≥20%-at-equal-coverage gate (G5) compares only designer-declared sets and token estimates. It never compares blindness, and it cannot check the baseline, so a design that is not genuinely cheaper at equal coverage can pass it.

## 2. FINDINGS

| id | severity | what step 4 says | evidence | why it fails | fix |
|---|---|---|---|---|---|
| F1 | BLOCKER | "replaces a default only on a written claim of ≥20% lower projected run cost **at equal coverage** (same criteria ids, same checks, same blindness)" (METHOD §3.4) | `design_gate.py:185–188` compares only `set(cov["criteria"])` and `set(cov["checks"])`, both supplied by the designer. There is no blindness field. `default_estimate.tokens` is also supplied by the designer, so the baseline can be inflated. Counterexample: a challenger drops the blind verifier node but still lists the same check names. Coverage is "equal" and the margin is 30%. | The gate checks what the designer declares and never reads the nodes. "Same blindness" is stated in prose but never enforced. | In G5, derive `checks` and blind-node ids from the design's own nodes, and compute `default_estimate` from the TASK_TYPES row. Add a `blind` set to the coverage comparison. |
| F2 | MAJOR | "More than 3 steps → consider a new piece. Split only if…" | Diagram `S4 -->|"more than 3 steps"| SPLIT`. Neither §3.4 nor SKILL.md:93–100 says where that branch ends: prompt file or workflow design. | A clear 5-step, single-engine, single-deliverable task has no stated route. One reader writes a long prompt file, another designs a workflow. | Add: "more than 3 steps, nothing unclear, no split → one piece, still a prompt file unless risk or kind needs an independent check (then a workflow design)." |
| F3 | MAJOR | "used at `stages.py:309`; it caps dispatches per plan… (corrected 2026-10-03)" | `stages.py:309` is the `CapState` docstring: `"""cap_state = (ctx.dispatch_count, CAP=3)…"""`. That is a definition, not a use. `stages.py:134,150` show `ctx.dispatch_count +=` in the Gate stage, so the same counter is also consumed by Gate dispatches, not only by "corroborating sources". | The citation line does not show the claimed use, and the "corrected" wording is still inexact. | Cite `stages.py:316` (`slot_remains`) and say "shared Gate + corroboration dispatch count". Fix the "the the" typo. |
| F4 | MAJOR | "Anchors for the number 3: Gate splits capability lists over three (`stages.py:109`)" | `stages.py:109` is `if count > 3:` after `count = decision_tree(task.difficulty, task.capability)`, followed by `ceil(count/3)` groups. `count` is an agent count. `registry.py:24` is `CAP = 3`, also agents. | The anchors justify a limit on agents. Step 4's 3 counts algorithm steps. The anchors are not evidence for the threshold, and the sentence presents them as if they were. | Relabel the sentence "analogy only (agent counts, not steps); the threshold is an unmeasured working value", or delete it. |
| F5 | MAJOR | "that ledger is how the defaults earn their n" | `TASK_TYPES_LEDGER.md` has 8 rows, all `default`, none a challenger. `Reconciled=yes` on 1 of 8. The other 7 read "no — token cost not measured". The one reconciled row's actual is `new input 68.8k · cache read 703k…` against a projection of "210k–460k tokens (token measure not named — a flaw)". | The projection and the actual are in different units. Challenger margins can never be reconciled. The "n=0" tag is stale (n≤1) and the 20% rule has never been exercised. | Name the cost unit in §3.4 (for example "output+new-input tokens, cache excluded"). State "ledger: 8 rows, 1 reconciled, 0 challengers" in place of the bare "n=0". |
| F6 | MAJOR | "…projected run cost" | TASK_TYPES "Challenger (the 20% rule)" says "(tokens / agents / wall time)"; `design_gate.py:174–184` uses tokens only; §3.4 says only "run cost". Ledger projections are ranges (for example 750k–1.1M). | Three definitions of cost. A margin of 20% is smaller than the range width of a single estimate. A design can win on tokens and lose on wall time or debuggability, and the rule allows it. | Fix tokens as the unit. Require comparing the range midpoints and require non-overlapping ranges, or state the 20% is on midpoints. |
| F7 | MAJOR | "Up to 3 steps and nothing unclear except decisions that have a provisional assumption" (§3.4) vs. SKILL "decisions that have a default" | SKILL.md:93. "Default" is also the TASK_TYPES default pattern, used in the same paragraph. | Two terms for one thing, and one of them collides with the next sentence's "default". | Use "provisional assumption" in SKILL, and reserve "default" for TASK_TYPES rows. |
| F8 | MINOR | (SKILL step 4) | The SKILL omits the §3.4 rules "a spot of kind information or unknown always means a workflow design", "or EJ flagged high risk", "Sonnet 5.5", and "others gets the full method". It adds "Too-small pieces cost more…", which §3.4 lacks. METHOD §3.2 says "Same warning as 3.4: fixed cost per agent, context lost at every split, more joins" and §3.4 contains no such warning. | Drift between the two copies, and a dangling cross-reference. | Add the missing clauses to SKILL step 4 (or point to step 3), and move the cost warning into §3.4. |
| F9 | MINOR | "Tiny but risky → the prompt file gets one independent check." | §3.4 and SKILL give no threshold for risk. "EJ flagged high risk" appears only in the checklist-reviewer clause, not in this bullet. Risky with more than 3 steps is unrouted. | Two readers rate "late" differently. | Add: "any one of the three risk answers 'yes' → independent check; more than 3 steps and risky → workflow design." |
| F10 | MINOR | "a different kind when the design builds" | `design_gate.py` G6 (the `builders` computation) uses `product=="yes"` or `builds and product=="mixed"`. The `builds` flag is designer-set. For `mixed` categories (debugging, test data gen, document and explain), the designer decides whether the stricter reviewer applies. | The reviewer kind can be avoided by setting `builds: false` on a `mixed` piece. | Derive `builds` from the nodes' write-scope, or have the checklist reviewer check the flag. |

## 3. CHECKLIST

| check | result | note |
|---|---|---|
| C1 | WEAK | "Step" and "piece" are defined in §3.2. "Provisional assumption" vs "default" collide (F7). "Coverage" is defined in prose (criteria ids, checks, blindness). "Projected run cost" has no unit in §3.4 (F6). "Tier" is not used in step 4 and is only implied by the risk-tiered reviewer. |
| C2 | WEAK | "Up to 3" is decidable. More than 3 with no useful split has no route (F2). |
| C3 | FAIL | `stages.py:109`: `if count > 3:`. It is an agent count, not steps (F4). `registry.py:24`: `CAP = 3` is fine. `stages.py:309` is a docstring, not a use (F3). |
| C4 | WEAK | Consistent with §3.2's "a hand-off must pay for itself", because the independent check pays by being a different kind. No risk threshold, and the more-than-3-steps risky case is unrouted (F9). |
| C5 | PASS | All 17 category rows carry pattern, engine, check and sabotage. `others` has "—" in all four and is routed to the full method. Not checked: the combination-pipeline rows and the labelling rules past rule 6. |
| C6 | FAIL | Computed by the designer from self-declared estimates in tokens. Baseline and blindness are not checked (F1, F6). A design can pass while worse on predictability or debuggability, since nothing scores those. |
| C7 | WEAK | TASK_TYPES names Codex `gpt-6.1-sol` for the high-risk reviewer. EXECUTOR_KINDS rule 5 says "different kind from the worker" (builder vs verifier), not designer vs checklist reviewer. §3.4 never names the reference for "different kind". `builds` is designer-set (F10). I did not verify §3.7's blindness text line by line. |
| C8 | FAIL | 8 rows, 8 defaults, 0 challengers, 1 `Reconciled=yes`, 7 "no — token cost not measured". The ledger does not yet let any default earn n (F5). |
| C9 | WEAK | Drift is real (F7, F8). Diagram node DF matches §3.4 closely. |
| C10 | WEAK | "Added 2026-10-01" matches TASK_TYPES ("Agreed with EJ 2026-10-01"). The 2026-10-03 correction is located correctly but the corrected text is still inexact (F3). The "n=0" on the ledger claim is stale (F5). I could not check the "Changed 2026-09-20 / trial 1 / n=1" claim against any trial record. |

## 4. STRONGEST COUNTEREXAMPLE

**Task:** "Fix the flaky timeout in the exporter, add a regression test, and update the changelog." This is three steps, one deliverable, no unclear spot, but it writes product code.

- **Route step 4 gives:** a prompt file, because it is "up to 3 steps". Risk is "judged separately", so one independent check is added, and nothing says whether that check must be a different kind.
- **Route it should give:** a workflow design with a build default (debugging → code generation with a different-kind reviewer). TASK_TYPES says a piece that touches product code is never read-only, and G6 demands a reviewer on builders.
- **Why it fails:** the 3-step threshold routes this task before the label and risk facts are consulted. The "tiny but risky" rule only rescues it if the reader happens to rate it risky.

## 5. WHAT I COULD NOT VERIFY

- The "Changed 2026-09-20 after trial 1 … n=1" claim. I did not look for the trial record.
- Whether the diagram's `SPLIT` node has outgoing edges (I read only lines 37–43).
- EXECUTOR_KINDS §3.7's blindness rule line by line, and whether `design_gate.py` enforces the checklist-reviewer kind for the design decision itself (G6 as I read it covers in-run reviewers).
- The combination pipelines in TASK_TYPES (I read only the category table and the labelling rules up to rule 6).
- That the 8 ledger rows are the complete state. I counted `^| 2026` lines.

## 6. WHAT THIS CHECKLIST MISSED

- **Ordering:** §3.4 consumes labels produced by §3.2, but step 4 says "up to 3 steps → prompt file" before any labelling, so a prompt file never gets a TASK_TYPES lookup. A 3-step build task skips the build default, the sabotage and the reviewer rule.
- **No penalty path:** nothing says what happens when a challenger's actual margin falls below 20%, other than a mention that a default overridden repeatedly "gets its row rewritten".
- **Combination runs:** all 8 ledger rows are multi-category runs labelled `default`. If only a few pipelines are seeded, "default" for an ad hoc combination is vacuous, and the ledger counts it as a default run.
- **Predictability, debuggability and variance:** the challenger rule scores cost only. Nothing penalises a cheaper design with a worse failure signature.
