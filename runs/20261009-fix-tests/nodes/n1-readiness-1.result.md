---
node: n1-readiness
attempt: 1
engine: claude
model: claude-opus-5-5
status: fail
started: 2026-10-09T12:51:47.913Z
ended: 2026-10-09T12:53:24.834Z
evidence: none
---
## Root cause
Not confirmed by a run. I couldn't run pytest or python3 here because every such command was blocked for approval. Reading the code points to the test's environment rather than to readiness.py. The two failing-side assertions, `str(Path.home())` and `str(ROOT)` "not in output", check the real home and the real repo. readiness.py never reads those: it uses the sandbox `HOME` and `cwd`. So those assertions can only fail if pytest's `tmp_path` is inside the real home or the repo, for example through `TMPDIR` or `--basetemp`. That was probably the case in the 2026-10-09 15:34 run that `.pytest_cache/v/cache/lastfailed` records as failing.
## Fix
None. readiness.py is unchanged, because the fix in the brief contradicts the test. The same test asserts absolute sandbox paths: `f"no {path}"`, `f"absent ({path})"` and `proof == str(path)`. So do RT-02, RT-03a–d, RT-16, RT-17, RT-18, RT-19 and RT-22. Replacing the home with `~` would therefore break rt_01's own `assert_row` lines and those other tests, which the Standard forbids. If `tmp_path` is not under the real home or the repo, the leak assertions already hold and no change is needed. If it is, no change to readiness.py alone can satisfy both kinds of assertion.
## Verified
Not verified, because no test command could run in this session.
- **Before:** `lastfailed` (mtime 2026-10-09 15:34) lists `test_rt_01_sanitized_full_inventory`, but its output and environment were not recorded.
- **After:** not run.

UNCLEAR: In the failing run, what were `TMPDIR`, `--basetemp` and `HOME` for the pytest process, and where did `tmp_path` resolve? / Best guess: under `/home/smoke01`, either in the repo or a home tmp dir. If so, the fix belongs in the test or the dispatcher, for example a `--basetemp` outside home, not in readiness.py.

UNCLEAR: May this node change the test, or the dispatcher's pytest environment, given the brief says only readiness.py? / Best guess: no; this goes back to EJ.
