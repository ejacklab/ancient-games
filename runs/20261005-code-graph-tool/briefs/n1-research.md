# Brief — n1-research (agy, research)

## Task (one deliverable)
Research how code graphs are generated today, and answer one question: **what can a stdlib-`ast` Python script honestly do, and what must it not claim?** Print the findings and a digest of at most 15 lines to stdout. Do not write any file.

## Context (only what this task needs)
You are read-only. The goal is a tool that turns a Python repo into a code graph — functions/classes as nodes, calls/imports as edges — so a verifier reads a graph instead of one function. Cover: the three tiers (stdlib `ast`, import-resolved, language-server), the precision each gives, and what a pure-`ast` script gets wrong (dynamic dispatch, `getattr`, decorators, pytest fixtures). Cite every claim.

## Template (fill this exactly)
```
# Research: code-graph generation

## The three tiers
- tier, tool, precision, cost — one line each

## What stdlib `ast` can and cannot see
- can: <…>
- cannot: <…>  (each with why)

## Existing tools worth knowing
- name — what it does, one line

## Digest (<= 15 lines)
<the 15-line summary a designer will read>
```

## Example (one good result, short)
```
## What stdlib ast cannot see
- `f = helper; f()` — the callee is a variable, not a name; the edge is absent, not wrong.
```

## Standard (how it is judged)
Every claim cites a source URL. The digest is 15 lines or fewer. A claim with no source, or a digest over 15 lines, is a failure.
