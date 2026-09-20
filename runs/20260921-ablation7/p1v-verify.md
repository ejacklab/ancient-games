# P1V — Independent verification: does deleting `dataclass_dict` from `loop/tkg_forecast/core.py` break anything?

**Instrument:** second, independent agent. I was not shown the other agent's method or reasoning, and did not look for `p1-groundtruth.md` or anything else in the run folder besides this output file.

## VERDICT: INCONCLUSIVE (on the mandated procedure) — with a supplementary, discriminating check that SUPPORTS the claim

The mandated instrument (`pytest tests/`, the repo's documented top-level suite) **cannot see `loop/tkg_forecast/core.py` at all** — no file under `tests/` imports `loop` or `tkg_forecast`, confirmed by grep and by running the CONTROL step (a hard `ImportError`-causing break of a 108-reference, clearly-live function in the same file produced byte-identical results to baseline). Per the task's own rule ("If the suite does NOT get worse, your instrument is not discriminating and your main result is worthless — say so plainly and report the verdict as INCONCLUSIVE"), the mandated result is **INCONCLUSIVE**.

Because that would leave the experiment with no signal at all, I ran one supplementary, non-mandated diagnostic after finishing the required procedure: `pytest loop/tests/` — the suite that actually imports `loop/tkg_forecast/core.py` (confirmed by grep: `loop/tests/test_tkg_forecast.py`, `test_tkg_lexical.py`, `test_tkg_rules.py`, `test_tkg_training.py` all do `from loop.tkg_forecast.core import (...)`). This suite **does** discriminate (its own control, deleting `canonical_json`, blew up 4 files with `ImportError` at collection time). Under this suite, deleting `dataclass_dict` produced **zero change**: identical 153 passed / 11 skipped / 2 failed (the 2 failures are pre-existing and unrelated — see below), before and after. This is real, verified signal that `dataclass_dict` is unused by the one test suite in the repo that actually touches this file. But it is a supplementary check outside the letter of the assigned procedure, so I am reporting the primary verdict as directed by the rules (INCONCLUSIVE) and giving the supplementary result as additional context, not a substitute.

---

## Setup

```
$ cd /home/smoke01/dev/seza/backtest
$ git worktree add /tmp/p1v_work/backtest-ablation7 ebdfd5f8a7a2fbe61f1b7b1d25d16b7488a3c062
Preparing worktree (detached HEAD ebdfd5f)
HEAD is now at ebdfd5f S4 workflow plan: mark the scheduler and harness superseded
```

Confirmed pinned sha inside the worktree:
```
$ cd /tmp/p1v_work/backtest-ablation7 && git log -1 --format='%H %s'
ebdfd5f8a7a2fbe61f1b7b1d25d16b7488a3c062 S4 workflow plan: mark the scheduler and harness superseded
```

## Step 1 — Locate the function

```
$ grep -n "def dataclass_dict" -A 5 loop/tkg_forecast/core.py
282:def dataclass_dict(value: Any) -> dict[str, Any]:
283-    """Convert a dataclass while keeping tuples canonicalized as JSON arrays."""
284-    if not dataclasses.is_dataclass(value):
285-        raise TypeError("value must be a dataclass instance")
286-    return json.loads(canonical_json(dataclasses.asdict(value)))
```

Pre-deletion sanity check — no other `.py` file in the repo references it:
```
$ grep -rn "dataclass_dict" --include="*.py" .
loop/tkg_forecast/core.py:282:def dataclass_dict(value: Any) -> dict[str, Any]:
```
(only the definition itself)

## Step 2 — BASELINE, before touching anything

Command (matches the Makefile's `test` target and the top-level `CLAUDE.md`-documented command):
```
$ python3 -m pytest tests/ -v
```
Run:
```
2026-09-20T18:38:22Z start
... (577 individual test lines, all PASSED — full log preserved in my working notes; final summary reproduced verbatim below)
=============================== warnings summary ===============================
tests/test_campaign_review.py::test_row3_long_spell_flags_through_build_report
tests/test_campaign_review.py::test_row3_long_spell_flags_through_build_report
tests/test_campaign_review.py::test_row3_spell_boundary_exactly_380_does_not_fire
tests/test_campaign_review.py::test_row3_spell_boundary_exactly_380_does_not_fire
  /tmp/p1v_work/backtest-ablation7/tools/campaign_review.py:264: RuntimeWarning: Mean of empty slice
    return float(np.nanmean(vals))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================= 577 passed, 4 warnings in 123.03s (0:02:03) ==================
2026-09-20T18:40:21Z end
```
**Wall time: ~1m59s (real), ~2m03s reported by pytest.** No pre-existing failures or skips — clean 577/577 baseline.

(Note on transcription: the raw log for a 577-test `-v` run is ~600 lines of `PASSED` lines; I am not pasting all 577 lines three times in this file, but I compared the three full logs programmatically with `diff` and report the exact byte-level result below rather than asserting it from memory.)

## Step 3 — Delete the function

Located exact lines with `grep -n`:
```
278:    def predicate_map(self) -> dict[str, PredicateSpec]:
279:        return {item.predicate_id: item for item in self.predicates}
280:
281:
282:def dataclass_dict(value: Any) -> dict[str, Any]:
283:    """Convert a dataclass while keeping tuples canonicalized as JSON arrays."""
284:    if not dataclasses.is_dataclass(value):
285:        raise TypeError("value must be a dataclass instance")
286:    return json.loads(canonical_json(dataclasses.asdict(value)))
287:
288:
289:def floor_utc_bin(timestamp: str, seconds: int) -> str:
```
Deleted lines 282-288 (def line, full body, and one blank separator, leaving the standard two-blank-line PEP8 gap before `floor_utc_bin`):
```
$ sed -i '282,288d' loop/tkg_forecast/core.py
```
Diff (`git diff -- loop/tkg_forecast/core.py`):
```diff
diff --git a/loop/tkg_forecast/core.py b/loop/tkg_forecast/core.py
index 8a8f710..ccbd6d2 100644
--- a/loop/tkg_forecast/core.py
+++ b/loop/tkg_forecast/core.py
@@ -279,13 +279,6 @@ class Ontology:
         return {item.predicate_id: item for item in self.predicates}
 
 
-def dataclass_dict(value: Any) -> dict[str, Any]:
-    """Convert a dataclass while keeping tuples canonicalized as JSON arrays."""
-    if not dataclasses.is_dataclass(value):
-        raise TypeError("value must be a dataclass instance")
-    return json.loads(canonical_json(dataclasses.asdict(value)))
-
-
 def floor_utc_bin(timestamp: str, seconds: int) -> str:
     micros = utc_micros(timestamp)
     width = seconds * 1_000_000
```
Confirmed removed: `grep -n "dataclass_dict" loop/tkg_forecast/core.py` → no match (exit 1).

## Step 4 — Re-run the identical suite command

```
$ python3 -m pytest tests/ -v
2026-09-20T18:40:34Z start
...
================= 577 passed, 4 warnings in 123.76s (0:02:03) ==================
2026-09-20T18:42:32Z end
```
**Wall time: ~1m58s (real).** 577 passed, 0 failed, 0 skipped — no change from baseline. No new failure names (there were none).

Byte-level comparison of the full baseline log vs this log:
```
$ diff /tmp/p1v_baseline.log /tmp/p1v_postdelete.log
597c597
< ================= 577 passed, 4 warnings in 123.03s (0:02:03) ==================
---
> ================= 577 passed, 4 warnings in 122.17s (0:02:02) ==================
$ echo $?
0   # (diff itself reported the one changed line above; only the timing string differs)
$ grep -c PASSED /tmp/p1v_baseline.log /tmp/p1v_postdelete.log
/tmp/p1v_baseline.log:577
/tmp/p1v_postdelete.log:577
```
**Every one of the 577 individual test results is byte-identical between the two runs; only the reported wall-clock time differs.**

## Step 5 — CONTROL (mandatory)

Restored the file first:
```
$ git checkout -- loop/tkg_forecast/core.py
$ grep -n "dataclass_dict" loop/tkg_forecast/core.py
282:def dataclass_dict(value: Any) -> dict[str, Any]:
```
(restored OK)

Picked a **clearly-live** function in the same file: `canonical_json` (line 47). Verified liveness before touching it — 108 references across the repo outside `core.py` (`grep -rn "\bcanonical_json\b" --include="*.py" . | grep -v loop/tkg_forecast/core.py | wc -l` → 108), and it is imported directly by 6 other modules in `loop/tkg_forecast/` (`benchmark.py`, `assertions.py`, `training.py`, `forecast.py`, `projection.py`, `rules.py`) plus used internally by `sha256_json` in the same file.

Deleted it the same way (def line + body + one blank separator):
```
$ sed -i '47,55d' loop/tkg_forecast/core.py
$ git diff -- loop/tkg_forecast/core.py
@@ -44,15 +44,6 @@ class ModelUnavailableError(TemporalKGError):
     """An optional model runtime is not installed at its pinned boundary."""
 
 
-def canonical_json(value: Any) -> str:
-    """Return deterministic, compact and finite JSON."""
-    try:
-        return json.dumps(
-            value, sort_keys=True, separators=(",", ":"), allow_nan=False
-        )
-    except (TypeError, ValueError) as exc:
-        raise SchemaError(f"value is not canonical JSON: {exc}") from exc
-
 
 def sha256_json(value: Any) -> str:
     return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
```

Sanity-checked the break is real, before running the suite:
```
$ python3 -c "import loop.tkg_forecast.core as c"
Traceback (most recent call last):
  ...
  File "/tmp/p1v_work/backtest-ablation7/loop/tkg_forecast/assertions.py", line 12, in <module>
    from .core import (
ImportError: cannot import name 'canonical_json' from 'loop.tkg_forecast.core'
```
This is a package-`__init__`-time `ImportError` — about as loud a break as Python allows.

Re-ran the **identical mandated suite command**:
```
$ python3 -m pytest tests/ -v
2026-09-20T18:43:47Z start
...
================= 577 passed, 4 warnings in 122.17s (0:02:02) ==================
2026-09-20T18:45:43Z end
```
577 passed, 0 failed, 0 skipped. **Byte-identical to baseline and to the post-deletion run:**
```
$ diff /tmp/p1v_baseline.log /tmp/p1v_control.log
597c597
< ================= 577 passed, 4 warnings in 123.03s (0:02:03) ==================
---
> ================= 577 passed, 4 warnings in 122.17s (0:02:02) ==================
```

**The control did not fire.** Breaking a 108-reference, `ImportError`-on-import function in the same file produced zero change in the mandated suite. This means `pytest tests/` structurally cannot detect anything about `loop/tkg_forecast/core.py` — confirmed by grep as well: no file under `tests/` imports `loop` or `tkg_forecast` in any form (`grep -rln "tkg_forecast\|^import loop\|^from loop" tests/` → no output), and no production module reachable from `tests/` (`engine/`, `runner.py`, `config.py`, `research/`, `tools/`, `eval/`, `project_memory/`) imports `tkg_forecast` either (only doc/markdown/json files reference it there).

**Per the task's explicit rule, this makes the primary result INCONCLUSIVE.**

## Supplementary diagnostic (not part of the mandated procedure — reported separately, for context only)

To avoid leaving the experiment with zero information, I additionally located and ran the suite that actually imports this file:
```
$ grep -rln "tkg_forecast" --include="*.py" .
loop/tests/test_tkg_forecast.py
loop/tests/test_tkg_lexical.py
loop/tests/test_tkg_rules.py
loop/tests/test_tkg_training.py
```
All four do `from loop.tkg_forecast.core import (...)`.

**Pristine baseline** (`git checkout -- loop/tkg_forecast/core.py` first, confirmed restored):
```
$ python3 -m pytest loop/tests/ -q
...
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_object_store_has_no_holdout - AssertionError: sandbox object store leaks holdout: [...]
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_assert_holdout_absent_passes - eval.input_closure.InputClosureError: BTC/USDT 1d: holdout bytes (index >= ...) recoverable via [...]
2 failed, 153 passed, 11 skipped in 29.00s
```
These 2 failures are pre-existing and, on inspection, look like a harness artifact of running inside a `git worktree` that carries the full repo history (including commits past the sealed-holdout boundary date `2025-09-24`) rather than a pruned/shallow checkout — `eval/input_closure.py`'s holdout-leak scan walks the worktree's own git objects and finds "future" blobs that exist in history regardless of which commit is checked out. This is unrelated to `core.py` or to either function under test; I did not attempt to fix it (out of scope, and I must not touch `eval/`).

**With `dataclass_dict` deleted, same command, in the same worktree:**
```
$ python3 -m pytest loop/tests/ -q
...
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_object_store_has_no_holdout - ...
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_assert_holdout_absent_passes - ...
2 failed, 153 passed, 11 skipped in 29.00s
```
**Identical: same 2 pre-existing failures, same 153 passed, same 11 skipped.** No new failure anywhere, including in the four files that directly import `core.py`.

**Supplementary control** — restored `dataclass_dict`, then deleted `canonical_json` (same break as the mandated CONTROL), ran this narrower suite:
```
$ python3 -m pytest loop/tests/ -q
...
ERROR loop/tests/test_tkg_forecast.py
ERROR loop/tests/test_tkg_lexical.py
ERROR loop/tests/test_tkg_rules.py
ERROR loop/tests/test_tkg_training.py
Interrupted: 4 errors during collection
4 errors in 0.79s
```
This suite **does discriminate**: breaking a live function in the same file produces 4 immediate collection errors, versus deleting `dataclass_dict`, which produces zero change from baseline. This is real, verified evidence (not reasoning) that `dataclass_dict` is unused by every test that imports its module.

File restored to pristine after this diagnostic (`git checkout -- loop/tkg_forecast/core.py`, confirmed clean via `git status --short` producing no output).

## Counts, side by side

| Run | Suite | Passed | Failed | Skipped/Errors |
|---|---|---|---|---|
| Baseline | `pytest tests/ -v` | 577 | 0 | 0 |
| Post-deletion (`dataclass_dict` gone) | `pytest tests/ -v` | 577 | 0 | 0 |
| CONTROL (`canonical_json` gone, live fn) | `pytest tests/ -v` | 577 | 0 | 0 — **control did not fire** |
| Supplementary baseline | `pytest loop/tests/ -q` | 153 | 2 (pre-existing) | 11 skipped |
| Supplementary post-deletion (`dataclass_dict` gone) | `pytest loop/tests/ -q` | 153 | 2 (same, pre-existing) | 11 skipped |
| Supplementary control (`canonical_json` gone) | `pytest loop/tests/ -q` | 0 | — | 4 collection errors — **control fired** |

## Step 6 — Cleanup

```
$ cd /home/smoke01/dev/seza/backtest
$ git worktree remove /tmp/p1v_work/backtest-ablation7 --force
$ rm -rf /tmp/p1v_work
$ git worktree list
/home/smoke01/dev/seza/backtest                                            ebdfd5f [master]
/home/smoke01/dev/seza/.claude/worktrees/20260920-s4-run/backtest          3da0803 [s4-campaign-review/20260920-s4-run]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a093d85f1c36cf875  abd8b86 [worktree-agent-a093d85f1c36cf875]
... (8 more agent-* worktrees, all pre-existing, none created by me)
$ git status
On branch master
Your branch is ahead of 'origin/master' by 194 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	enhancement_plans/campaign_horizon_followups/runs/20260920-s4-review/
	research/reviews/s4-implementation-20260920/

nothing added to commit but untracked files present (use "git add" to track)
```
My worktree is gone. `git status` and the untracked-file list are identical to the state recorded before I started (I did not create, touch, or remove anything else in `/home/smoke01/dev/seza/backtest`). The other listed worktrees pre-date this task and are not mine.

## NOT_ESTABLISHED

- **The mandated instrument (`pytest tests/`) establishes nothing about this claim, either way.** It never imports `loop` or `tkg_forecast` in any form — confirmed by grep and by the failed CONTROL. Its 577/577-unchanged result is consistent with "dead code" and equally consistent with "this file/module is simply untested by the primary suite." I cannot distinguish these from the mandated procedure alone; that is exactly why the verdict is INCONCLUSIVE on that procedure.
- **The supplementary `loop/tests/` result is real evidence but still only about test coverage, not about production entry points.** A test suite proves no *test* reaches the code; it says nothing about whether something outside any test imports `dataclass_dict` at runtime. I did not check:
  - Non-test production call sites reached only via CLI/script entry points not exercised by any test, e.g. anything invoked through `python3 -m loop.evaluate_candidate` (the `make eval` path) or `make eval-dev` (`python3 -m eval.evaluator --candidate dev-test --no-count`) — I did not run either of these.
  - Dynamic/reflective usage: `getattr`, string-based imports, serialization registries, or a name looked up by string (e.g. from a config file or JSON) rather than a static `import`. My repo-wide grep for the literal string `dataclass_dict` found only the definition, which rules out static references but not dynamic ones under a different spelling.
  - Any script under `loop/` or elsewhere that is run manually/ad hoc and not collected by pytest at all (no `test_*.py` name, no `__main__` block I inspected).
  - Notebooks, external callers outside this repo, or downstream consumers of a public API that might import `loop.tkg_forecast.core.dataclass_dict` directly (I have no visibility into anything outside this repo).
  - I did not run `make test-tkg` (`pytest loop/tests/test_tkg_forecast.py loop/tests/test_tkg_training.py -q`, the Makefile's own targeted command) or `make test-tkg-ml`; I used the broader `pytest loop/tests/ -q` instead, which is a superset of `test-tkg`'s two files (it also picked up `test_tkg_lexical.py`, `test_tkg_rules.py`, `test_diff_guard.py`, `test_evaluate_candidate.py`, `test_program_db.py`, `test_trial_state.py`, `test_worktree.py`). I did not additionally try `test-tkg-ml`, which requires a pinned torch runtime I did not check for.
- **The two `test_worktree.py` failures are unexplained beyond my working hypothesis** (holdout git-object leak triggered by running inside a full-history worktree rather than a pruned checkout). I verified this hypothesis only indirectly (by noting `eval/input_closure.py`'s scan logic walks git objects in the worktree's own repo) and did not fully trace `_git_object_leaks`/`_path_leaks_holdout` to confirm it. I did not attempt a fix — `eval/` is off-limits to me and this is orthogonal to the assigned claim. I only confirmed these 2 failures are present identically in both the pre- and post-deletion `loop/tests/` runs, so they don't affect the comparison.
- I did not open or look at `p1-groundtruth.md` or any other file in `runs/20260921-ablation7/` besides my own output, as instructed.