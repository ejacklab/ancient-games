# Explorer file — findings about existing code

What an explorer node writes (method 3.8 item 10). Findings go to a file; the COO reads the digest. Each finding
cites file:line with a short verbatim quote, and `.claude/skills/workflow-design/scripts/quote_check.py FILE --root
<repo>` confirms every quote is at its line. Folder: the run's `runs/<id>/` (or `docs/research/` when it is kept).

```
# Exploration — <system or area>
Produced <date> by <who>. Question asked: <the question>. Commit explored: <git rev-parse --short HEAD>.

| id | Claim | Kind | Source | Quote | Evidence |
|---|---|---|---|---|---|
| X1 | <one claim about the code> | read / ran | path/to/file.py:120 or path:120-124 | `a short verbatim piece of those lines` | <for ran: the command and where its output is saved; for read: —> |

## Gaps
<what was not read; claims a build depends on that are still `read`>
```

- **Kind.** `read` = inferred from reading the code. `ran` = confirmed by running it (a test, a differential run,
  `~/skills/verify-extraction`); it must name its evidence. Only `ran` claims may feed a node that builds.
- **Quote.** At least 8 characters, copied from the cited lines (whitespace may differ); a pipe inside a quote is
  written `\|`. Cite the commit explored: a quote that no longer matches after the code changed is a stale finding.
- **Scope.** Inside the affected area, under the brief's budget; never a repo-wide overview.

## Example

| id | Claim | Kind | Source | Quote | Evidence |
|---|---|---|---|---|---|
| X1 | The Gate splits a capability list when it is longer than three | read | ancient_games/stages.py:109-111 | `if count > 3:` | — |
| X2 | A long list is split into groups of three | read | ancient_games/stages.py:111 | `k = math.ceil(count / 3)` | — |
| X3 | An unreadable skills directory is reported as unknown, not a crash | ran | .claude/skills/workflow-design/scripts/readiness.py:180-181 | `except OSError as e: return Check(group, item, UNKNOWN, f"unreadable: {e}", str(p))` | `pytest tests/test_readiness.py -k rt_22` (passes; fails with the guard removed) |
