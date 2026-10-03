# Run 20261003-node-workdir — the first real run (build a feature, case C)

Feature: an optional per-node `workdir` in `dispatch.py` (commit fe1b21e). Pipeline: TASK_TYPES "build a feature",
run by `dispatch.py` itself. Pre-registered in 8ac8905 (restatement, R1–R7 with examples, exploration quote-checked,
per-test baseline, projection). Ledger row 1 in `docs/TASK_TYPES_LEDGER.md`.

## What happened
| Node | Engine | Result |
|---|---|---|
| dev | Codex `gpt-6.1-sol` (confirmed from its rollout) | round 1: implemented, 27 own tests green; round 2 after the gate: fixed R4 |
| cases | agy `gemini-3.8-flash-medium`, blind | 8 acceptance tests; **7 of 8 failed on the old code** (sabotage proven) |
| gate | `feature_gate.py` | round 1 **failed**: the verifier's R4 test caught that `--dry-run` cut arguments over 60 characters, hiding a long `-C` path — the dev's own tests missed it; round 2 passed: baseline 463/463, scope, must-not, tamper ok |
| review | agy | run 1 **blocked**: agy tried a command, headless mode auto-denied it, exit 0 and no output (caught as an empty result); run 2 with a self-contained brief: "No findings. Verdict: accept." |

Full suite after: 482 passed (463 + 19 new).

## Cost against the projection
Projected 210k–460k tokens, about 4 engine calls, 10–20 min. Actual: 5 engine calls; Codex new input 68.8k, cache
read 703k, output 5.5k; agy not measurable (its usage sits in a protobuf); 417 s of engine time. The projection named
no token measure, so it cannot be scored: Codex's processed total (777k) is above it, its new tokens (74k) below it.

## Lessons (each is now in code or in the method)
1. **The blind verifier paid for itself on the first run**: it found a defect the dev's tests did not (R4).
2. **The script gate's repair loop worked as designed**: real gate output went back to the dev, fixed in one round.
3. **A projection must name its token measure** (new input, cache read, output) — otherwise it cannot be scored.
4. **agy auto-denies tools in headless mode and exits 0**: briefs for agy must be self-contained; the dispatcher now
   treats the "auto-denied" notice as a failure (ea6bd32).
5. **Codex counts cached tokens inside `input_tokens`**: the harvester double-counted; fixed (d62be3a).
6. **`quote_check.py` caught the COO's own wrong citation** before the build used it.
7. Still open: the dispatcher does not save the prompt and feedback of each call, so the gate's round-1 output that
   reached the dev was reconstructed from the code, not read back; `review`'s first brief and the gate's record show
   the repair call's result path. Small fixes for the next run.
8. The review's "No findings" on a 10k-character diff from a flash-tier model is thin evidence; one data point.
