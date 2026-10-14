# N1 repair — one more B2.7 case (test writer)

`tests/test_memory_index.py` is the file you wrote earlier, as it was frozen. The spec is in `docs/index-md/` as
before; `REQUIREMENTS.md` now also says, in B2.5 and the B2 Fails if, that B2.7 is an error in every status (the
contradiction you raised).

One part of **B2.7** has no test: the marker counts only when a line **starts** with `<<<<<<<` or `>>>>>>>`. A line
where the marker comes after other characters is not a conflict marker and is not an error. Add a test for that:
the marker after leading spaces, and after other text on the same line, in the header and in the body, in an active, a
superseded and a retired entry, in write and check mode. The entry must pass, and `INDEX.md` must be exactly what
the other passing tests expect for that entry. Cite `B2.7` in the docstring.

Change nothing else in the file. Change only `tests/test_memory_index.py`.

Before you finish, run:

```
python3 checks/trace_check.py tests/test_memory_index.py
python3 checks/fixture_ids.py tests/test_memory_index.py
python3 -m pytest --collect-only -q tests/test_memory_index.py | tail -1
```

Write `n1-result.md`:

```
status: done | blocked
new tests: <name — criterion id>
checks: <the three last lines>
contradictions: <CONTRADICTS lines, or none>
```
