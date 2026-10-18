---
agents: [all]
kinds: [engine-call]
from: runs/20261016-six-experts/insight.md#F-8ac06aae
---
Run each engine call as its own background Bash call, never as `( … ) &` subshells inside one call: one of two such
subshells once never started, and nothing showed it until a file was missing at the end.
