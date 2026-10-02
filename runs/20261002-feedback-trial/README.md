# Feedback harvester trial — option A on four past Workflow runs (2026-10-02)

Command: `harvest_run.py --run trial-<wf> --runs-root /tmp/... --workflow <wf>`; digests below, verbatim. n=4 runs, read-only, no model calls.

## wf_526758fa-2c8
```
run trial-wf_526758fa-2c8: 6 calls (6 with cost), engines claude-sub
tokens: new input 434,898 · cache read 5,129,235 · output 66,995
slowest: sweep:tools r1 265s
most new tokens: write r1 134,806
nodes with more than one round: none
cross-check run JSON tokens vs transcript (input+cache write): max drift 25.2%
ledger Actual cost: new 434,898 / cache-read 5,129,235 / out 66,995 tokens; 18.6 agent-min; 6 calls
```
## wf_9a7f9697-2a2
```
run trial-wf_9a7f9697-2a2: 7 calls (7 with cost), engines claude-sub
tokens: new input 371,528 · cache read 1,562,741 · output 41,303
slowest: bio:sperm r1 199s
most new tokens: combine r1 90,543
nodes with more than one round: none
cross-check run JSON tokens vs transcript (input+cache write): max drift 40.0%
ledger Actual cost: new 371,528 / cache-read 1,562,741 / out 41,303 tokens; 11.7 agent-min; 7 calls
```
## wf_0349f318-dcc
```
run trial-wf_0349f318-dcc: 5 calls (5 with cost), engines claude-sub
tokens: new input 289,542 · cache read 2,164,211 · output 72,768
slowest: 4-design r1 349s
most new tokens: 4-design r1 113,001
nodes with more than one round: 2-algorithm
cross-check run JSON tokens vs transcript (input+cache write): max drift 44.1%
ledger Actual cost: new 289,542 / cache-read 2,164,211 / out 72,768 tokens; 14.6 agent-min; 5 calls
```
## wf_fc2ffa51-890
```
run trial-wf_fc2ffa51-890: 6 calls (2 with cost), engines claude-sub
tokens: new input 186,248 · cache read 1,711,680 · output 45,902
slowest: plan r3 396s
most new tokens: plan r3 124,480
nodes with more than one round: plan, plan-critic
cost unknown: 4 call(s) (cached)
cross-check run JSON tokens vs transcript (input+cache write): max drift 0.0%
ledger Actual cost: new 186,248 / cache-read 1,711,680 / out 45,902 tokens; 9.6 agent-min; 6 calls
```
## What the cross-check found

Per agent, the run JSON's `tokens` was compared with input + cache-write tokens summed from that agent's own
transcript (message.usage, deduplicated by message id). Non-web agents matched within 1% (14 of 14). Every agent
that drifted (6 agents, 20–44% more in the run JSON) is a web-research agent (sweep:tools, sweep:methods,
bio:humpback/sperm/dolphin) except one 2-algorithm round, which I did not check for web use. **Hypothesis, not verified:** WebFetch summarises pages with
a separate model call whose tokens are counted by the run but are not in the agent transcript. Consequence: for
web-heavy nodes the transcript undercounts cost; the run JSON's figure is closer for new input, while cache reads
and output exist only in the transcript. The harvester reports both and prints the drift.

Also seen: cache reads dominate (5.1M cache-read vs 0.43M new input in wf_526758fa-2c8), so a token count without
the split misstates cost. wf_fc2ffa51-890 has 4 cached agents: reported as cost unknown, never as zero.
