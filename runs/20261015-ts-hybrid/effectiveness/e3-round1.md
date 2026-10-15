# E3 — twelve planted R11–R13 violations (round 1)

| Planted violation | Hybrid catches |
|---|---|
| empty result read as pass | yes |
| failure record with no reason | yes |
| failure record with no evidence | yes |
| session with failures and no insight ends | yes |
| insight missing a failure | yes |
| insight with one fix option | yes |
| insight not named in the final message | yes |
| AI suggestion in the accepted list with no decision | yes |
| accepted case with no fails-if | yes |
| requirement with no purpose | yes |
| a variant case raises the count | yes |
| a safety unit marked skippable | yes |

hybrid: 12 of 12

Prediction: hybrid 12 of 12, control 0 of 12. Measured: 12 of 12. Circular by construction: the plants come from the same fails-if lines as the tests; this shows the code does what the rules say, not that an agent behaves.
