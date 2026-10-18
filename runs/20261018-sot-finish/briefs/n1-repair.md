# N1 repair — tests for the spec's new clauses (test writer)

`tests/test_memory_index.py` is the file you wrote earlier, as frozen. The spec in `docs/index-md/REQUIREMENTS.md`
gained clauses since; add acceptance tests for them. The script is still not here; write from the spec alone.

## The new clauses (read them in the spec: B2.8, B4.1, B4.5)

1. **B2.8, whole tokens.** A form preceded by a letter, digit or `_` is not a credential (for example `x` + an AWS
   key id); the same form after a space, `(`, `:` or at the line start is.
2. **B2.8, the private key block.** The BEGIN and END lines are lines that *contain* the markers: an indented, `> `
   quoted, `- ` listed or trailing-space BEGIN or END line still counts. The body is counted without line breaks and
   surrounding spaces; 64 counted characters make a block, 63 do not; a BEGIN with no END is not a block.
3. **B2.8, nothing else prints it.** A credential inside a conflict-marker line, a `kind`, an `id` or a `status`
   value: the run fails, and the credential's text appears nowhere in the output; the problem is still reported.
4. **B4.1.** `limit` given as `1.0` is an error; an empty or blank `agent`, `unit`, `basis` or `source` is an error.
5. **B4.5.**
   - JSON nested too deeply to read (for example 100000 `[`) is an error with the file named, no `Traceback`, in
     both modes.
   - In write mode, a dangling symlink at `project-memory/start-limits.json`, or a folder there, is an error, not the
     example.
   - In check mode, a limits file left unmerged (a merge conflict on it, stages 1–3 and no stage 0) is an error, not
     the example. Build the conflict with two branches in the test repo.
   - A bad entry and a bad limits file in the same run: both problems are reported.

Every new test's docstring cites its id. Keep the existing tests unless a new clause changes what one expects; say
which, and why. Build credential values from parts, as before.

## Before you finish

```
python3 checks/trace_check.py tests/test_memory_index.py
python3 checks/fixture_ids.py tests/test_memory_index.py
python3 -m pytest --collect-only -q tests/test_memory_index.py | tail -1
```

## Return

Write `n1-result.md`:

```
status: done | blocked
new tests: <name — id>
existing tests changed: <name — why>, or none
checks: <the three last lines>
contradictions: <CONTRADICTS lines, or none>
```
