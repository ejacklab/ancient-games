# Brief — n6-optimize (opencode, code generation)

## Task (one deliverable)
Fix what the review found, then prove the tool is complete by running it on this repository.

## Context (only what this task needs)
You get the tool, the spec, and the review's findings. Fix each finding, then run `python3 code_graph.py .` at the repo root and report the coverage summary. Write `code_graph.py` to disk, then print your summary to stdout. Do not touch anything outside `code_graph.py`.

## Template (fill this exactly)
```
## Findings fixed
<each finding, and what changed>
## Run on this repo
<nodes, edges, and coverage over the repo>
## Spot-check
<one function you verified by hand, and that the graph matches it>
```

## Example (one good result, short)
```
## Run on this repo
{"nodes": 210, "edges": 380, "coverage": {"tested": 34, "total": 210}}
## Spot-check
`validate_plan` in dispatch.py — node present, its callers listed. Matches.
```

## Standard (how it is judged)
Every review finding is addressed, the tool runs clean on this repo, and the coverage summary matches a manual spot-check. An unaddressed finding fails.
