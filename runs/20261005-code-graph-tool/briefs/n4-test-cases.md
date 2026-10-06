# Brief — n4-test-cases (codex, test cases gen)

## Task (one deliverable)
Generate the test cases that `code_graph.py` must be exercised against — positive and negative. Print them to stdout. Do not write any file.

## Context (only what this task needs)
You get the built tool and the spec. The point is to cover the algorithm's expected cases: a direct call, an imported call, a class method, a nested function, and the cases a static `ast` script is known to miss (call through a variable, `getattr`, a decorator, a lambda). Report the coverage as a percentage.

## Template (fill this exactly)
```
## Cases
- <case name> — positive|negative — what it checks — expected result
## Coverage
<number> of ~<expected> expected cases covered = <N%>
```

## Example (one good result, short)
```
## Cases
- direct_call — positive — a -> b edge drawn — edge present
- call_through_variable — negative — the edge is absent, not wrong
## Coverage
5 of ~7 expected cases = 71%
```

## Standard (how it is judged)
Both positive and negative cases are present, each names what it checks and the expected result, and the coverage % is stated. A list with only positive cases, or with no %, fails.
