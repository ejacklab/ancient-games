# P1 — fixture ground truth: an established dead deletion target

**Piece:** P1 of `workflow-design.md` (20260921-ablation7)
**Date:** 2026-09-21
**Domain:** software engineering — dead-code reachability analysis in a Python repo.
**State written:** `S1 = resolved`

---

## Verdict

**TARGET: `loop/tkg_forecast/core.py` — the top-level function `dataclass_dict` (lines 282–286)**
in `/home/smoke01/dev/seza/backtest`.

Fixture sha at final scan: **`ebdfd5f8a7a2fbe61f1b7b1d25d16b7488a3c062`** (branch `master`).
*Caveat, recorded because it is a hazard for P1V:* a **concurrent session moved this repo's HEAD
during my work**, `26aef09 → ebdfd5f`. Both shas contain the target at the identical line. See
§6 "HEAD moved mid-task".

The exact block, from `git show HEAD:loop/tkg_forecast/core.py`:

```python
def dataclass_dict(value: Any) -> dict[str, Any]:
    """Convert a dataclass while keeping tuples canonicalized as JSON arrays."""
    if not dataclasses.is_dataclass(value):
        raise TypeError("value must be a dataclass instance")
    return json.loads(canonical_json(dataclasses.asdict(value)))
```

**The headline fact.** Across all **254 commits reachable from all refs**, `dataclass_dict`
occurs **98 times**, and every single one of those 98 occurrences is **the same definition line**,
`loop/tkg_forecast/core.py:282`. It has never been referenced by anything, in any revision, since
it was written. It was born dead.

---

## Scope note: "I ran" vs "I read"

Everything in a fenced block below preceded by `$` or a `===` banner is **output I ran**.
Facts I state from reading (the registry rows, the `__init__` export list) are marked *read*.

---

## 1. Method, and why this granularity

### 1.1 First: is there a dead *whole module*? (No.)

A whole file would be a cleaner target than a function, so I ruled it out first, two ways.

**(a) Bare module-name reference count across every tracked file.** Run:

```
$ /tmp/p1scan/modcount.sh
eval/accounting.py                            70
eval/approvals.py                             9
eval/baseline_registry.py                     6
eval/bundle.py                                60
eval/calibration.py                           81
eval/deflated_sharpe.py                       55
eval/evaluator.py                             189
eval/experiment_spec.py                       13
eval/forecast.py                              52
eval/freeze_certificate.py                    7
eval/guardrails.py                            48
eval/holdout_exposure.py                      6
eval/identity.py                              90
eval/input_closure.py                         24
eval/ledger.py                                129
eval/partitions.py                            47
eval/phase_a_authority.py                     6
eval/protocol.py                              120
eval/publish.py                               20
eval/replay.py                                69
eval/robustness.py                            26
eval/scientific_result.py                     16
eval/walkforward.py                           78
loop/diff_guard.py                            39
loop/evaluate_candidate.py                    33
loop/graph_memory.py                          9
loop/program_db.py                            20
loop/tkg_forecast/assertions.py               47
loop/tkg_forecast/benchmark.py                68
loop/tkg_forecast/core.py                     59
loop/tkg_forecast/features.py                 45
loop/tkg_forecast/forecast.py                 52
loop/tkg_forecast/models.py                   40
loop/tkg_forecast/projection.py               51
loop/tkg_forecast/rules.py                    56
loop/tkg_forecast/service.py                  38
loop/tkg_forecast/training.py                 61
loop/trial_state.py                           27
loop/worktree.py                              83
```

No module scores 0. (These counts are inflated by common English words — `accounting`,
`identity`, `core` — so they are only useful as a floor, which is all I used them for.)

**(b) AST import graph, counting imports at ANY nesting depth** — so function-local and
branch-local lazy imports (an escape hatch named in `ABLATION_3.md:32`) are counted. Run
`python3 /tmp/p1scan/importgraph.py`, from `/home/smoke01/dev/seza/backtest`:

```
python files parsed: 223

=== eval/ and loop/ non-test modules and who imports them ===
eval.accounting            n=11  ['eval/evaluator.py', 'eval/forecast.py', 'eval/protocol.py', 'eval/tests/test_accounting.py']
eval.approvals             n=3   ['eval/phase_a_authority.py', 'eval/tests/test_approvals.py', 'eval/tests/test_phase_a_authority.py']
eval.baseline_registry     n=3   ['eval/tests/test_baseline_registry.py', 'eval/tests/test_publish_baseline_bundle.py', 'tools/publish_baseline_bundle.py']
eval.bundle                n=7   ['eval/publish.py', 'eval/replay.py', 'eval/tests/test_bundle.py', 'eval/tests/test_publish.py']
eval.calibration           n=5   ['eval/evaluator.py', 'eval/replay.py', 'eval/tests/test_acceptance.py', 'eval/tests/test_forecast.py']
eval.deflated_sharpe       n=13  ['eval/evaluator.py', 'eval/replay.py', 'eval/tests/test_acceptance.py', 'loop/tests/test_trial_state.py']
eval.evaluator             n=5   ['eval/tests/test_acceptance.py', 'eval/tests/test_evaluator_outputs.py', 'eval/tests/test_experiment_spec.py', 'tests/test_fill_log.py']
eval.experiment_spec       n=2   ['eval/tests/test_experiment_spec.py', 'tools/rebaseline.py']
eval.forecast              n=6   ['eval/protocol.py', 'eval/tests/test_forecast.py', 'eval/tests/test_protocol.py', 'eval/tests/test_replay.py']
eval.freeze_certificate    n=3   ['eval/phase_a_authority.py', 'eval/tests/test_freeze_certificate.py', 'eval/tests/test_phase_a_authority.py']
eval.guardrails            n=6   ['eval/evaluator.py', 'eval/replay.py', 'eval/tests/test_acceptance.py', 'eval/tests/test_experiment_spec.py']
eval.holdout_exposure      n=2   ['eval/phase_a_authority.py', 'eval/tests/test_holdout_exposure.py']
eval.identity              n=9   ['eval/bundle.py', 'eval/experiment_spec.py', 'eval/replay.py', 'eval/scientific_result.py']
eval.input_closure         n=9   ['eval/replay.py', 'eval/tests/test_input_closure.py', 'eval/tests/test_rebaseline.py', 'eval/tests/test_rebaseline_replay.py']
eval.ledger                n=7   ['eval/evaluator.py', 'eval/robustness.py', 'eval/tests/test_acceptance.py', 'eval/tests/test_robustness.py']
eval.partitions            n=20  ['eval/evaluator.py', 'eval/input_closure.py', 'eval/replay.py', 'eval/tests/test_acceptance.py']
eval.phase_a_authority     n=1   ['eval/tests/test_phase_a_authority.py']
eval.protocol              n=21  ['eval/approvals.py', 'eval/baseline_registry.py', 'eval/bundle.py', 'eval/freeze_certificate.py']
eval.publish               n=3   ['eval/tests/test_publish.py', 'eval/tests/test_publish_baseline_bundle.py', 'tools/publish_baseline_bundle.py']
eval.replay                n=3   ['eval/tests/test_rebaseline_replay.py', 'eval/tests/test_replay.py', 'tools/rebaseline_replay.py']
eval.robustness            n=2   ['eval/evaluator.py', 'eval/tests/test_robustness.py']
eval.scientific_result     n=3   ['eval/bundle.py', 'eval/tests/test_replay.py', 'eval/tests/test_scientific_result.py']
eval.walkforward           n=10  ['eval/evaluator.py', 'eval/forecast.py', 'eval/tests/test_acceptance.py', 'eval/tests/test_input_closure.py']
loop.diff_guard            n=5   ['loop/evaluate_candidate.py', 'loop/tests/test_diff_guard.py', 'loop/tests/test_evaluate_candidate.py', 'loop/tests/test_trial_state.py']
loop.evaluate_candidate    n=2   ['loop/tests/test_evaluate_candidate.py', 'loop/tests/test_trial_state.py']
loop.graph_memory          n=1   ['loop/program_db.py']
loop.program_db            n=7   ['eval/identity.py', 'eval/robustness.py', 'eval/tests/test_robustness.py', 'loop/evaluate_candidate.py']
loop.tkg_forecast.assertions  n=8  ['loop/tests/test_tkg_forecast.py', 'loop/tests/test_tkg_lexical.py', 'loop/tests/test_tkg_rules.py', 'loop/tests/test_tkg_training.py']
loop.tkg_forecast.benchmark   n=2  ['loop/tests/test_tkg_forecast.py', 'loop/tests/test_tkg_rules.py']
loop.tkg_forecast.core        n=13 ['loop/tests/test_tkg_forecast.py', 'loop/tests/test_tkg_lexical.py', 'loop/tests/test_tkg_rules.py', 'loop/tests/test_tkg_training.py']
loop.tkg_forecast.features    n=8  ['loop/tests/test_tkg_forecast.py', 'loop/tests/test_tkg_rules.py', 'loop/tests/test_tkg_training.py', 'loop/tkg_forecast/__init__.py']
loop.tkg_forecast.forecast    n=9  ['loop/tests/test_tkg_forecast.py', 'loop/tests/test_tkg_rules.py', 'loop/tests/test_tkg_training.py', 'loop/tkg_forecast/__init__.py']
loop.tkg_forecast.models      n=5  ['loop/tests/test_tkg_forecast.py', 'loop/tests/test_tkg_rules.py', 'loop/tkg_forecast/rules.py', 'loop/tkg_forecast/service.py']
loop.tkg_forecast.projection  n=5  ['loop/tests/test_tkg_forecast.py', 'loop/tests/test_tkg_lexical.py', 'loop/tests/test_tkg_rules.py', 'loop/tkg_forecast/__init__.py']
loop.tkg_forecast.rules       n=1  ['loop/tests/test_tkg_rules.py']
loop.tkg_forecast.service     n=3  ['loop/tests/test_tkg_forecast.py', 'loop/tests/test_tkg_rules.py', 'loop/tkg_forecast/training.py']
loop.tkg_forecast.training    n=2  ['loop/tests/test_tkg_training.py', 'loop/tkg_forecast/service.py']
loop.trial_state           n=6   ['eval/identity.py', 'eval/tests/test_rebaseline.py', 'loop/evaluate_candidate.py', 'loop/tests/test_evaluate_candidate.py']
loop.worktree              n=6   ['eval/tests/test_input_closure.py', 'loop/evaluate_candidate.py', 'loop/tests/test_evaluate_candidate.py', 'loop/tests/test_trial_state.py']
```

**Every** non-test module under `eval/` and `loop/` has at least one importer. `NONE FOUND` at
module granularity. So the target had to be a symbol inside a live module — which the dispatch had
already anticipated with `NetOutcomeResolver`.

### 1.2 The scanner

`/tmp/p1scan/scan.py` (and its survey predecessors `symscan2.py`, `symscan3.py`, same mechanism).
It builds an **inverted token index** over every readable non-binary file under a set of roots:

```
token -> [(path, lineno)]      tokens via  [A-Za-z_][A-Za-z0-9_]*
```

Then for a queried symbol it splits hits into:

- **DEF_SITES** — lines matching `^\s*(async\s+)?(def|class)\s+SYMBOL\b`. This is what a divergent
  worktree copy of the same module looks like, and separating them out is the step the naive
  reference count gets wrong.
- **REFS** — everything else.

**Why a token index and not an AST caller-walk.** A grep-class hit is a *superset* of an AST hit.
A name mentioned in a string literal, a JSON key, a Makefile, a markdown doc, or a `.jsonl`
journal all land in the index. A zero here is therefore strictly stronger evidence than a zero
from an import-graph walk, and it is what makes the string-dispatch hatch checkable at all. Its
limitation is stated in §8.1.

Full source of `scan.py` (40 lines, reproduced so the finding does not depend on `/tmp` surviving):

```python
import os, re, sys, collections
SKIP = {".git", "__pycache__", ".pytest_cache", ".benchmarks", "node_modules", ".mypy_cache"}
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

def files(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP]
        for fn in fns:
            p = os.path.join(dp, fn)
            if not os.path.islink(p):
                yield p

def main():
    sym, roots = sys.argv[1], sys.argv[2:]
    defre = re.compile(r"^\s*(async\s+)?(def|class)\s+" + re.escape(sym) + r"\b")
    index = collections.defaultdict(list); lines_of = {}; nf = 0; seen = set()
    for root in roots:
        for p in files(root):
            rp = os.path.realpath(p)
            if rp in seen: continue
            seen.add(rp)
            try:
                if os.path.getsize(p) > 20_000_000: continue
                t = open(p, encoding="utf-8", errors="replace").read()
            except OSError: continue
            if "\0" in t[:4096]: continue
            nf += 1; ls = t.splitlines(); lines_of[p] = ls
            for i, line in enumerate(ls, 1):
                for tok in set(TOK.findall(line[:20000])):
                    index[tok].append((p, i))
    print("SYMBOL   : %s" % sym); print("ROOTS    : %s" % ", ".join(roots)); print("FILES    : %d" % nf)
    defs, refs = [], []
    for p, i in sorted(index.get(sym, [])):
        (defs if defre.match(lines_of[p][i-1]) else refs).append((p, i, lines_of[p][i-1].strip()))
    print("DEF_SITES: %d" % len(defs))
    for p, i, t in defs: print("   DEF  %s:%d  %s" % (p, i, t))
    print("REFS     : %d" % len(refs))
    for p, i, t in refs: print("   REF  %s:%d  %s" % (p, i, t))

main()
```

### 1.3 The survey that selected the target

`symscan3.py` enumerated **855 definitions** — every top-level function, top-level class, class
**method**, and module-level `UPPER_CASE` constant — in every non-test module under `eval/` and
`loop/`, excluding `loop/graph_memory.py` by rule. Corpus: **5,851 files, 2,009,519 lines, 51,801
distinct tokens**, spanning the fixture tree, all 10 agent worktrees, the `20260920-s4-run`
worktree, and the `seza` repo root outside `backtest`.

```
$ python3 /tmp/p1scan/symscan3.py
indexed 5851 files
=== ZERO non-definition references (incl. methods + CONSTANTS) ===
top-func         loop/tkg_forecast/core.py        dataclass_dict                     L282

total definitions scanned: 855
```

**Exactly one** definition out of 855 has zero references. That is the target.

For context, the next-sparsest tier (`symscan2.py`, 1–3 refs) is entirely genuinely-live private
helpers whose only callers are one call site plus its worktree duplicates — `_sigmoid`
(`models.py:124` ← `models.py:536`), `_load_vocabularies`, `_lexical_match_query`,
`_relevance_score`, `_bodies`, `_cenet_stage1_batches`, `_contrastive_valid_anchor_count`,
`_fit_binary_temperature`, `_make_tensor_manifest`, `_load_cygnet`, `_load_cenet`. None is dead.
**There is no near-miss; `dataclass_dict` is alone at zero.**

### 1.4 The final finding scan, verbatim

```
$ cd /home/smoke01/dev/seza/backtest && git rev-parse HEAD
ebdfd5f8a7a2fbe61f1b7b1d25d16b7488a3c062
$ git log --oneline -1
ebdfd5f S4 workflow plan: mark the scheduler and harness superseded

$ python3 /tmp/p1scan/scan.py dataclass_dict /home/smoke01/dev/seza
SYMBOL   : dataclass_dict
ROOTS    : /home/smoke01/dev/seza
FILES    : 5851
DEF_SITES: 3
   DEF  /home/smoke01/dev/seza/.claude/worktrees/20260920-s4-run/backtest/loop/tkg_forecast/core.py:282  def dataclass_dict(value: Any) -> dict[str, Any]:
   DEF  /home/smoke01/dev/seza/.claude/worktrees/20260920-s4-run/seza/backtest/loop/tkg_forecast/core.py:282  def dataclass_dict(value: Any) -> dict[str, Any]:
   DEF  /home/smoke01/dev/seza/backtest/loop/tkg_forecast/core.py:282  def dataclass_dict(value: Any) -> dict[str, Any]:
REFS     : 0
```

All three DEF_SITES were read individually; each is the genuine `def` line of a copy of the same
file. None is a reference masquerading as a definition.

---

## 2. Registry tier

*Read from `/home/smoke01/dev/ancient-games/ancient_games/registry.py`.*

**Match: R7 — stakes 2, hub=False, gate=checkpoint, owner=None.**

Reasoning, from the matching code (`registry.py`, `_matches_key`, read):

```python
def _matches_key(row: Row, ref: ArtifactRef) -> bool:
    if row.kind == "dir":
        return any(ref.path == p or ref.path.startswith(p) for p in row.pattern)
```

- R7 is `("engine/", "runner.py", "config.py", "eval/", "loop/")`, `kind="dir"`.
  `"loop/tkg_forecast/core.py".startswith("loop/")` → **True**. R7 matches.
- R8 is `("research/", "tests/", "scratchpad")` — the path starts with none of them. No match.
- R4 and R5 are `kind="file"`, **exact-path** rows for two `.jsonl` files. The target path is
  neither. No match.
- R7 is therefore the sole direct match; D2 specificity suppression is a no-op with one survivor.
  → `stakes = 2`, `gate = checkpoint`.
- R6 (`verb="commit"`, stakes 2, gate=checkpoint) will additionally match when the deletion is
  committed. Also stakes 2, also checkpoint — it does **not** change the terminus.

**The three owner-gated rows are NOT engaged.** This is the specific thing the dispatch asked me
to check.

```
$ grep -rn -E "protocol\.json|holdout_access|load_holdout|partitions" loop/tkg_forecast/
(no hits)
```

`loop/tkg_forecast/` contains no reference to the R1 protocol file, the R2 access log, or the R3
sealed loader. A legitimate `consumers` declaration for this deletion cannot name any of them, so
`consumer_matches` cannot pull an owner row in. The terminus stays **checkpoint**, not **owner**.

Corroborating — `core.py`'s entire import block is stdlib only:

```
$ sed -n '1,12p' loop/tkg_forecast/core.py
"""Closed schemas and deterministic identities for temporal-KG forecasting."""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import json
import math
import re
from typing import Any, Iterable, Mapping, Optional, Sequence, Tuple
```

---

## 3. Escape hatches — enumerated, each with its command and result

`docs/ABLATION_3.md:32` (read) names these as exactly why `graph_memory` was contested:
*"`validate_event` dispatches on `event_type` strings and eleven worktrees hold divergent copies
with live callers."* Each is checked below.

### H1 — `event_type` / string-keyed dynamic dispatch

```
$ grep -rn --include=*.py -E "event_type|validate_event" eval loop
loop/trial_state.py:214:def _event(event_type: str, request_key: str, payload: Dict[str, Any]) -> Dict[str, Any]:
loop/trial_state.py:219:        "event_type": event_type, "request_key": request_key, "payload": payload,
loop/trial_state.py:224:        "event_type": event_type,
loop/trial_state.py:254:    required = {"schema_version", "event_id", "event_type", "request_key", "ts", "payload"}
loop/trial_state.py:260:    if event["event_type"] not in EVENT_TYPES:
loop/trial_state.py:261:        raise TrialStateError(f"{context}: unknown event_type {event['event_type']!r}")
loop/trial_state.py:317:        et = e["event_type"]
loop/trial_state.py:379:    et = event["event_type"]
loop/tkg_forecast/forecast.py:225:    event_type: str
loop/tkg_forecast/forecast.py:238:            "event_type": self.event_type,
loop/tkg_forecast/forecast.py:253:            "schema_version", "ledger_seq", "event_type", "forecast_id",
loop/tkg_forecast/forecast.py:264:        if value["event_type"] not in {"issued", "resolved", "invalidated"}:
loop/tkg_forecast/forecast.py:270:            event_type=value["event_type"],
loop/tkg_forecast/forecast.py:303:        if event.event_type == "issued":
loop/tkg_forecast/forecast.py:344:            if event.event_type == "resolved":
loop/tkg_forecast/forecast.py:426:        resolved = tuple(item for item in events if item.event_type == "resolved")
loop/tests/test_tkg_forecast.py:540:    assert resolved.event_type == "resolved"
(plus 7 lines in loop/tests/test_trial_state.py, all literal "trial_finalized"/"reserved"/"epoch_reset")
```

**Result: does not reach the target.** The hatch is real and lives in two places. Its key space is
closed and literal: `{"issued", "resolved", "invalidated"}` at `forecast.py:264`, and `EVENT_TYPES`
at `trial_state.py:260`. Neither contains `"dataclass_dict"`. More decisively, this dispatch keys
on *data* values, not function names — and the scanner indexes string literals anyway, so with
**zero** occurrences of the token outside the three `def` lines, no string key anywhere can name
it. (The scanner's ability to see a string key is positive-controlled in §4 step 3b.)

### H2 — function-local / lazy imports inside branches

**Result: covered by construction.** `importgraph.py` (§1.1b) uses `ast.walk`, which visits
`Import`/`ImportFrom` at **any** nesting depth, not just module top level. Nesting cannot hide an
import from it. Separately, the token index does not care about nesting at all.

### H3 — `getattr` / `globals()` / `importlib` / `__dict__` / `eval` / `exec`

```
$ grep -rn --include=*.py -E "getattr\(|globals\(\)|locals\(\)|vars\(|importlib|__import__|__dict__|eval\(|exec\(" eval loop | grep -v '/tests/'
eval/protocol.py:399:    for _src, _live_slip in (("config", float(getattr(live_config, "EXEC_SLIPPAGE_RATE"))),
eval/evaluator.py:183:    fill_log = list(getattr(bt, "fill_log", []) or [])
eval/evaluator.py:188:        common = getattr(bt, "_common_index", None)
eval/evaluator.py:244:        return getattr(_rnr, "INITIAL_EQUITY", 10000.0)
eval/evaluator.py:344:    config_repr = "|".join(f"{k}={getattr(cfg, k, None)}" for k in sorted(keys))
loop/tkg_forecast/models.py:12:import importlib
loop/tkg_forecast/models.py:40:        torch = importlib.import_module("torch")
loop/tkg_forecast/models.py:45:    observed = str(getattr(torch, "__version__", "")).split("+")[0]
loop/tkg_forecast/models.py:88:        if not callable(getattr(module, "parameters", None)):
loop/tkg_forecast/models.py:90:        if callable(getattr(module, "eval", None)):
loop/tkg_forecast/models.py:93:            if not callable(getattr(parameter, "requires_grad_", None)):
loop/tkg_forecast/models.py:99:    if any(getattr(parameter, "requires_grad", True) for parameter in parameters):
loop/tkg_forecast/models.py:162:            require_hex64(getattr(self, name), name)
loop/diff_guard.py:303:    "eval", "exec", "compile", "open", "input", "__import__", "globals", "locals",
loop/diff_guard.py:309:    "os", "_os", "sys", "subprocess", "socket", "shutil", "pathlib", "importlib",
loop/diff_guard.py:329:        self.reasons.append(f"{msg} (line {getattr(node, 'lineno', '?')})")
loop/tkg_forecast/training.py:1534:    model.eval()
loop/tkg_forecast/training.py:1555:    model.eval()
eval/walkforward.py:138:        int(getattr(cfg, "MOM_LONG_OFFSET")),
eval/walkforward.py:139:        int(getattr(cfg, "VOL_LOOKBACK")),
eval/walkforward.py:140:        int(getattr(cfg, "ATR_PERIOD")),
eval/walkforward.py:141:        int(getattr(cfg, "PIVOT_LOOKBACK")),
eval/walkforward.py:142:        int(getattr(cfg, "CORR_LONG_WINDOW")),
eval/walkforward.py:145:    configured = int(getattr(cfg, "WARMUP_DAILY_BARS"))
eval/walkforward.py:346:    all_fills = getattr(bt_test, "fill_log", None) or []
eval/walkforward.py:357:    contexts = getattr(bt_test, "contexts", {}) or {}
eval/walkforward.py:363:            df = getattr(ctx, "df_1d", None) if ctx is not None else None
eval/walkforward.py:538:        for f in (getattr(bt_test, "fill_log", None) or [])
eval/walkforward.py:572:    regimes = getattr(test_res, "regime_labels", pd.DataFrame())
eval/robustness.py:66:            value = getattr(self, name)
loop/tkg_forecast/service.py:64:            if getattr(adapter, "model_id", None) != selector:
loop/tkg_forecast/features.py:180:            require_hex64(getattr(self, name), name)
loop/tkg_forecast/assertions.py:64:            require_id(getattr(self, name), name)
```

**Result: does not reach the target.** Every `getattr` uses either a **literal** attribute name, or
a `name` bound by iteration over a fixed tuple of that class's own field names. There is no
`getattr(<module>, <computed>)` anywhere in `eval/` or `loop/`. The only `importlib` call in the
whole stakes-2 surface is `importlib.import_module("torch")` — a literal. `loop/diff_guard.py:303`
and `:309` are a **denylist of forbidden names**, not a dispatch table. `globals()`, `locals()`,
`vars()`, `__dict__`, `eval(`, `exec(` do not appear at all outside that denylist (the two
`model.eval()` lines are torch's method, not the builtin).

Name-assembly check (an `import_module`/`getattr` whose argument is built at runtime):

```
$ grep -rn --include=*.py -E "getattr\([^,]+,\s*(f\"|f'|[A-Za-z_]+\s*\+)|import_module\(\s*(f\"|f'|[^\"'])" eval loop runner.py config.py tools research
research/atr_conformance.py:74:    return importlib.import_module(spec)
research/atr_tournament.py:67:    mod = importlib.import_module(module_name)
research/atr_tournament.py:136:    mod = importlib.import_module(module_name)
research/atr_tournament.py:251:        src = open(importlib.import_module(mod).__file__, encoding="utf-8").read()
research/growth_potential/hist/universe_history.py:226:    module = importlib.import_module(exclusions_from)
```

All five are in `research/` (registry R8, stakes 1) and all take **module** names from CLI/config,
never a function name inside `tkg_forecast`.

### H4 — the divergent worktree copies with live callers

```
$ for w in $(git worktree list --porcelain | grep '^worktree ' | cut -d' ' -f2); do
    if [ -f "$w/loop/tkg_forecast/core.py" ]; then echo "HAS  $w";
      grep -n dataclass_dict "$w/loop/tkg_forecast/core.py" | sed 's/^/       /';
    else echo "none $w"; fi; done
HAS  /home/smoke01/dev/seza/backtest
       282:def dataclass_dict(value: Any) -> dict[str, Any]:
HAS  /home/smoke01/dev/seza/.claude/worktrees/20260920-s4-run/backtest
       282:def dataclass_dict(value: Any) -> dict[str, Any]:
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a093d85f1c36cf875
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a0cc78d12efead4a1
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a40c9739a5ac27ef3
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a68e82f812be1fb63
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a71d74ff1f94f022a
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-aafccee3e485690a0
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-ab35a0e43fc454858
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-ac07e3c9b81d79c6f
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-ae4225e7360433868
none /home/smoke01/dev/seza/backtest/.claude/worktrees/agent-af97697d225d43c00
```

**Result: the hatch is empty for this target.** The ten agent worktrees do not contain
`loop/tkg_forecast/` at all — they are checked out at commits predating it. Only the
`20260920-s4-run` worktree has a copy (twice, via a nested path), and in it the symbol is a bare
definition with no caller (§1.4 DEF_SITES). **This is precisely the fact that made `graph_memory`
contestable and that does not apply here.**

### H5 — plugin / entry-point registration, and doctest collection

```
$ ls setup.py pyproject.toml setup.cfg *.egg-info
(no packaging files in backtest/)
$ ls /home/smoke01/dev/seza/setup.py /home/smoke01/dev/seza/pyproject.toml
(none at seza root)
$ ls pytest.ini tox.ini setup.cfg pyproject.toml
ls: cannot access 'pytest.ini': No such file or directory
ls: cannot access 'tox.ini': No such file or directory
ls: cannot access 'setup.cfg': No such file or directory
ls: cannot access 'pyproject.toml': No such file or directory
$ grep -rn "doctest" --include=*.py --include=*.ini --include=*.cfg --include=Makefile .
(no output)
```

**Result: no such mechanism exists.** No packaging metadata anywhere, so no `entry_points`. No
pytest config, so no `--doctest-modules` collection that could execute the docstring. `conftest.py`
(read) only registers a `slow` marker.

### H6 — star imports and `__all__` re-export

```
$ grep -rn "import \*" --include=*.py . | grep -v '\.claude'
(no output)
$ grep -rn "__all__" loop/
loop/tkg_forecast/__init__.py:13:__all__ = (
```

`loop/tkg_forecast/__init__.py` (read) exports exactly:
`AssertionJournal, FactStore, ForecastLedger, ForecastPrediction, ForecastRequest,
TemporalFeatureSnapshot, build_feature_snapshot, build_projection, verify_projection`.
`dataclass_dict` is **not** among them. There are **zero** star imports in the entire repo, so
there is no invisible re-export path. The package docstring states the package "is deliberately
not imported by `loop`".

### H7 — the import lists from `core` itself (the likeliest hiding place)

All nine modules that import from `core`, complete. `dataclass_dict` appears in **none**:

```
loop/tkg_forecast/rules.py:17      from .core import (IntegrityError, SchemaError, UnresolvedError,
                                     canonical_json, require_finite_number, require_hex64,
                                     require_id, sha256_json, utc_micros)
loop/tkg_forecast/projection.py:21 from .core import (SCHEMA_VERSION, ConflictError, IntegrityError,
                                     Ontology, SchemaError, UnresolvedError, canonical_json,
                                     intervals_overlap, require_finite_number, require_hex64,
                                     require_id, require_utc, sha256_json, strict_json, utc_micros)
loop/tkg_forecast/features.py:11   from .core import (SNAPSHOT_POLICY_VERSION, IntegrityError,
                                     SchemaError, UnresolvedError, floor_utc_bin, require_hex64,
                                     require_id, require_utc, sha256_json, strict_json, utc_micros)
loop/tkg_forecast/models.py:17     from .core import (ModelUnavailableError, IntegrityError,
                                     SchemaError, UnresolvedError, require_finite_number,
                                     require_hex64, require_id, require_utc, sha256_json, utc_micros)
loop/tkg_forecast/forecast.py:13   from .core import (FORECAST_LEDGER_VERSION, IntegrityError,
                                     SchemaError, canonical_json, require_finite_number,
                                     require_hex64, require_id, require_unique_ids, require_utc,
                                     sha256_json, strict_json, utc_micros, utc_now)
loop/tkg_forecast/service.py:9     from .core import SchemaError, UnresolvedError, require_id, require_utc
loop/tests/test_tkg_forecast.py:21 from loop.tkg_forecast.core import (IntegrityError,
                                     ModelUnavailableError, Ontology, EntitySpec, PredicateSpec,
                                     SchemaError, SourceRef, UnresolvedError, sha256_json)
loop/tests/test_tkg_lexical.py:10  from loop.tkg_forecast.core import (EntitySpec, IntegrityError,
                                     Ontology, PredicateSpec, SchemaError, SourceRef)
loop/tests/test_tkg_rules.py:17    from loop.tkg_forecast.core import (EntitySpec, IntegrityError,
                                     ModelUnavailableError, Ontology, PredicateSpec, SchemaError,
                                     SourceRef, UnresolvedError)
loop/tests/test_tkg_training.py:19 from loop.tkg_forecast.core import (SNAPSHOT_POLICY_VERSION,
                                     IntegrityError, SchemaError, UnresolvedError, sha256_json)
```

(Printed by an `awk` extraction over each file; reflowed here for width. Names verbatim and
complete — each block ends at its closing paren.)

### H8 — git history across every reachable revision

```
$ git rev-list --all | wc -l
254
$ git grep -n "dataclass_dict" $(git rev-list --all | head -400) -- | head -6
26aef09a9b51d5ece1fe89abc04b171947c586c3:loop/tkg_forecast/core.py:282:def dataclass_dict(value: Any) -> dict[str, Any]:
247fb9b6c1a4c77678336344167b4fff007b92eb:loop/tkg_forecast/core.py:282:def dataclass_dict(value: Any) -> dict[str, Any]:
54b77602433cf156a06e669491edb44f4ccabf74:loop/tkg_forecast/core.py:282:def dataclass_dict(value: Any) -> dict[str, Any]:
0070d4bdde8ee75736a6f50366a2631719989e5a:loop/tkg_forecast/core.py:282:def dataclass_dict(value: Any) -> dict[str, Any]:
3da08031a49a8bb423968eb6c46f5fce73a543a5:loop/tkg_forecast/core.py:282:def dataclass_dict(value: Any) -> dict[str, Any]:
7232f75780ff4fca85fdaf29566d2b47cbea8364:loop/tkg_forecast/core.py:282:def dataclass_dict(value: Any) -> dict[str, Any]:
$ git grep -n "dataclass_dict" $(git rev-list --all | head -400) -- | wc -l
98
$ git grep -n "dataclass_dict" $(git rev-list --all | head -400) -- | sed 's/^[0-9a-f]*://' | sort -u
loop/tkg_forecast/core.py:282:def dataclass_dict(value: Any) -> dict[str, Any]:
```

**Result: 98 hits across 254 revisions, collapsing to exactly one distinct `file:line:text`** — the
definition. `head -400` over 254 revisions covers all of them. `rev-list --all` spans every ref, so
branch tips that are not checked out are included. The symbol has **never** had a caller in the
recorded history of this repository.

*(The `sed 's/^[0-9a-f]*://'` strips only the leading commit sha; file, line and text are
preserved, so the collapse to a single line is a real collapse, not an artifact of the filter. The
unfiltered first six lines are printed above and are all the same `core.py:282` def.)*

### H9 — importers outside the seza tree, and installed copies

```
$ grep -rIl --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=__pycache__ \
    -e "dataclass_dict" /home/smoke01 | grep -v "^/home/smoke01/dev/seza"
/home/smoke01/.venv/lib/python3.14/site-packages/pydantic/_internal/_decorators_v1.py
/home/smoke01/.cache/uv/archive-v0/HTDRqIZ5suLR3zYkElItR/lib/python3.14/site-packages/pydantic/_internal/_decorators_v1.py
   ... 18 more, every one of them pydantic/_internal/_decorators_v1.py ...
```

**Result: a name collision, not an importer.** Every out-of-tree hit is **pydantic's own unrelated
`dataclass_dict`** in `_decorators_v1.py`. **This is a trap worth flagging for anyone re-checking
by a bare `grep -r dataclass_dict ~`: they will get pydantic hits and may misread them as callers.**

```
$ python3 -c "import loop; print(loop.__file__)"
loop NOT importable outside repo: ModuleNotFoundError No module named 'loop'
```

No `.pth`, `.egg-link` or site-packages copy puts `loop` on the path outside the repo, so no
external process can import it.

---

## 4. The positive control on the scanner — PASSED on attempt 1

Per the contract: inject exactly one reference in a throwaway worktree, confirm the scan reports
that reference **and only it**, then remove it.

**Worktree used:** `/tmp/p1-pc-worktree`, created detached from `backtest`, **now removed** (§6).

### Step 1 — baseline, expect REFS: 0

```
$ git worktree add --detach /tmp/p1-pc-worktree HEAD
Preparing worktree (detached HEAD ebdfd5f)
HEAD is now at ebdfd5f S4 workflow plan: mark the scheduler and harness superseded
$ git -C /tmp/p1-pc-worktree rev-parse HEAD
ebdfd5f8a7a2fbe61f1b7b1d25d16b7488a3c062

$ python3 /tmp/p1scan/scan.py dataclass_dict /tmp/p1-pc-worktree
SYMBOL   : dataclass_dict
ROOTS    : /tmp/p1-pc-worktree
FILES    : 445
DEF_SITES: 1
   DEF  /tmp/p1-pc-worktree/loop/tkg_forecast/core.py:282  def dataclass_dict(value: Any) -> dict[str, Any]:
REFS     : 0
```

### Step 2 — inject exactly one reference

```
$ printf '\n\n_PC_PROBE = dataclass_dict  # injected by P1 positive control\n' >> \
    /tmp/p1-pc-worktree/loop/tkg_forecast/projection.py
$ grep -n "dataclass_dict" /tmp/p1-pc-worktree/loop/tkg_forecast/projection.py
1014:_PC_PROBE = dataclass_dict  # injected by P1 positive control
$ git -C /tmp/p1-pc-worktree diff --stat
 loop/tkg_forecast/projection.py | 3 +++
 1 file changed, 3 insertions(+)
```

### Step 3 — re-scan, expect REFS: 1 and only the injection

```
$ python3 /tmp/p1scan/scan.py dataclass_dict /tmp/p1-pc-worktree
SYMBOL   : dataclass_dict
ROOTS    : /tmp/p1-pc-worktree
FILES    : 445
DEF_SITES: 1
   DEF  /tmp/p1-pc-worktree/loop/tkg_forecast/core.py:282  def dataclass_dict(value: Any) -> dict[str, Any]:
REFS     : 1
   REF  /tmp/p1-pc-worktree/loop/tkg_forecast/projection.py:1014  _PC_PROBE = dataclass_dict  # injected by P1 positive control
```

**The control fires: 0 → 1, reporting the injected reference and nothing else. Attempt 1, passed.**

### Steps 3b / 3c — supplementary controls for the two reference forms an AST walker cannot see

Each injected alone, after reverting the previous.

```
$ git -C /tmp/p1-pc-worktree checkout -- loop/tkg_forecast/projection.py
$ printf '\n\n_PC_PROBE2 = getattr(_core, "dataclass_dict")  # injected string-keyed reference\n' \
    >> /tmp/p1-pc-worktree/loop/tkg_forecast/service.py
$ python3 /tmp/p1scan/scan.py dataclass_dict /tmp/p1-pc-worktree
DEF_SITES: 1
   DEF  /tmp/p1-pc-worktree/loop/tkg_forecast/core.py:282  def dataclass_dict(value: Any) -> dict[str, Any]:
REFS     : 1
   REF  /tmp/p1-pc-worktree/loop/tkg_forecast/service.py:179  _PC_PROBE2 = getattr(_core, "dataclass_dict")  # injected string-keyed reference

$ git -C /tmp/p1-pc-worktree checkout -- loop/tkg_forecast/service.py
$ printf '\nThe helper `dataclass_dict` is used by the X pipeline.\n' >> /tmp/p1-pc-worktree/README.md
$ python3 /tmp/p1scan/scan.py dataclass_dict /tmp/p1-pc-worktree
DEF_SITES: 1
   DEF  /tmp/p1-pc-worktree/loop/tkg_forecast/core.py:282  def dataclass_dict(value: Any) -> dict[str, Any]:
REFS     : 1
   REF  /tmp/p1-pc-worktree/README.md:246  The helper `dataclass_dict` is used by the X pipeline.
```

The scanner detects a **string-literal `getattr` key** and a **markdown-doc mention**. This is what
licenses the H1 and H9 results — without it, "no string dispatch reaches this symbol" would be an
assertion rather than a measurement.

### Step 4 — removal, expect REFS back to 0

```
$ git -C /tmp/p1-pc-worktree checkout -- README.md
$ git -C /tmp/p1-pc-worktree status --porcelain
(empty)
$ python3 /tmp/p1scan/scan.py dataclass_dict /tmp/p1-pc-worktree
SYMBOL   : dataclass_dict
ROOTS    : /tmp/p1-pc-worktree
FILES    : 445
DEF_SITES: 1
   DEF  /tmp/p1-pc-worktree/loop/tkg_forecast/core.py:282  def dataclass_dict(value: Any) -> dict[str, Any]:
REFS     : 0
```

---

## 5. Supplementary: a runtime check by a different mechanism

The static scan cannot see a runtime call. So I also **sabotaged the function** in the throwaway
worktree and ran the suite. This is deliberately **not** P1V's remove-and-retest: it is a mutation
(raise-on-call), not a deletion, and it answers a different question — *is this function ever
executed?*

**Baseline, clean worktree:**

```
$ cd /tmp/p1-pc-worktree && python3 -m pytest tests/ eval/tests/ loop/tests/ -q
FAILED eval/tests/test_input_closure.py::test_input_closure_cli_clean_sandbox_exit_0
FAILED eval/tests/test_input_closure.py::test_constructed_sandbox_omits_holdout
FAILED eval/tests/test_phase_a_authority.py::test_current_repo_state_refuses
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_object_store_has_no_holdout
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_assert_holdout_absent_passes
5 failed, 1220 passed, 15 skipped, 4 warnings in 180.58s (0:03:00)
```

*(Those 5 failures are pre-existing artifacts of running in a fresh checkout — sealed-partition and
missing-file conditions — unrelated to the target. They are the control, not a problem. P1V should
expect them too.)*

**With `raise AssertionError` inserted as the first statement of `dataclass_dict`:**

```
$ sed -i '282a\    raise AssertionError("P1 SABOTAGE: dataclass_dict was called at runtime")' \
    loop/tkg_forecast/core.py
$ sed -n '282,288p' loop/tkg_forecast/core.py
def dataclass_dict(value: Any) -> dict[str, Any]:
    raise AssertionError("P1 SABOTAGE: dataclass_dict was called at runtime")
    """Convert a dataclass while keeping tuples canonicalized as JSON arrays."""
    if not dataclasses.is_dataclass(value):
        raise TypeError("value must be a dataclass instance")
    return json.loads(canonical_json(dataclasses.asdict(value)))

$ python3 -m pytest tests/ eval/tests/ loop/tests/ -q
FAILED eval/tests/test_input_closure.py::test_input_closure_cli_clean_sandbox_exit_0
FAILED eval/tests/test_input_closure.py::test_constructed_sandbox_omits_holdout
FAILED eval/tests/test_phase_a_authority.py::test_current_repo_state_refuses
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_object_store_has_no_holdout
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_assert_holdout_absent_passes
5 failed, 1220 passed, 15 skipped, 4 warnings in 180.63s (0:03:00)
```

**Identical counts and the identical five failures.** The sabotage never fired.

### 5.1 Proving the sabotage *could* have fired

A null result from a sabotage is worthless unless the sabotage is shown to work. So I applied the
**same edit technique** to `floor_utc_bin` — a **known-live sibling helper seven lines below the
target in the same file** — and ran the same subset:

```
=== CONTROL A: loop/tests baseline, clean ===
$ python3 -m pytest loop/tests/ -q
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_object_store_has_no_holdout
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_assert_holdout_absent_passes
2 failed, 149 passed, 15 skipped in 28.04s

=== CONTROL B: sabotage floor_utc_bin (known-live sibling, same file, same technique) ===
$ sed -i '289a\    raise AssertionError("P1 SABOTAGE-CONTROL: floor_utc_bin was called at runtime")' \
    loop/tkg_forecast/core.py
$ sed -n '289,291p' loop/tkg_forecast/core.py
def floor_utc_bin(timestamp: str, seconds: int) -> str:
    raise AssertionError("P1 SABOTAGE-CONTROL: floor_utc_bin was called at runtime")
    micros = utc_micros(timestamp)
$ python3 -m pytest loop/tests/ -q
FAILED loop/tests/test_tkg_training.py::test_training_manifest_is_chronological_direction_specific_and_test_blind
       - AssertionError: P1 SABOTAGE-CONTROL: floor_utc_bin was called at runtime
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_object_store_has_no_holdout
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_assert_holdout_absent_passes
21 failed, 130 passed, 15 skipped in 28.06s

=== CONTROL C: revert, sabotage dataclass_dict only, same subset ===
$ git checkout -- loop/tkg_forecast/core.py
$ sed -i '282a\    raise AssertionError("P1 SABOTAGE: dataclass_dict was called at runtime")' \
    loop/tkg_forecast/core.py
$ python3 -m pytest loop/tests/ -q
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_object_store_has_no_holdout
FAILED loop/tests/test_worktree.py::test_sealed_sandbox_assert_holdout_absent_passes
2 failed, 149 passed, 15 skipped in 28.18s
```

**2 → 21 failures for the live sibling; 2 → 2 for the target.** Same file, same `sed` technique,
same test subset, same interpreter. The instrument discriminates. The target is not executed.

---

## 6. Cleanup — nothing was left behind

```
$ git checkout -- loop/tkg_forecast/core.py        # in the throwaway worktree
$ git status --porcelain                            # in the throwaway worktree
(empty)
$ cd /home/smoke01/dev/seza/backtest
$ git worktree remove /tmp/p1-pc-worktree --force && git worktree prune
$ ls -d /tmp/p1-pc-worktree
ls: cannot access '/tmp/p1-pc-worktree': No such file or directory
$ git worktree list
/home/smoke01/dev/seza/backtest                                            ebdfd5f [master]
/home/smoke01/dev/seza/.claude/worktrees/20260920-s4-run/backtest          3da0803 [s4-campaign-review/20260920-s4-run]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a093d85f1c36cf875  abd8b86 [worktree-agent-a093d85f1c36cf875]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a0cc78d12efead4a1  b8f4012 [worktree-agent-a0cc78d12efead4a1]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a40c9739a5ac27ef3  86b1a5e [worktree-agent-a40c9739a5ac27ef3]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a68e82f812be1fb63  54ec6e5 [worktree-agent-a68e82f812be1fb63]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-a71d74ff1f94f022a  2199b6c [worktree-agent-a71d74ff1f94f022a]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-aafccee3e485690a0  2001457 [worktree-agent-aafccee3e485690a0]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-ab35a0e43fc454858  5529c0e [worktree-agent-ab35a0e43fc454858]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-ac07e3c9b81d79c6f  6c30239 [worktree-agent-ac07e3c9b81d79c6f]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-ae4225e7360433868  8257459 [worktree-agent-ae4225e7360433868]
/home/smoke01/dev/seza/backtest/.claude/worktrees/agent-af97697d225d43c00  d405c54 [worktree-agent-af97697d225d43c00]
$ git status --porcelain
?? enhancement_plans/campaign_horizon_followups/runs/20260920-s4-review/
?? research/reviews/s4-implementation-20260920/
```

The worktree list is identical to its pre-P1 state. The two untracked directories were **already
present before P1 started** (they appear in the session's opening git status). **P1 made no change
to `/home/smoke01/dev/seza/backtest`, to `ancient_games/`, or to `ablation/`.**

Scratch scanner scripts live in `/tmp/p1scan/` — outside every protected path, disposable. The
finding does not depend on them surviving: `scan.py` is reproduced in full in §1.2.

### HEAD moved mid-task

`git rev-parse HEAD` in `backtest` returned `26aef09` at the start of P1 and `ebdfd5f` later. A
**concurrent session committed to `backtest/master` while I was scanning** — `ebdfd5f "S4 workflow
plan: mark the scheduler and harness superseded"`. I verified the target is byte-identical at both
shas:

```
$ git show 26aef09:loop/tkg_forecast/core.py | sed -n '282p'
def dataclass_dict(value: Any) -> dict[str, Any]:
$ git show ebdfd5f:loop/tkg_forecast/core.py | sed -n '282p'
def dataclass_dict(value: Any) -> dict[str, Any]:
```

**Consequence for P1V and P4: pin the sha.** This repo is live and will move again. The ground
truth is asserted at `ebdfd5f`. P1V should check out `ebdfd5f` explicitly rather than `HEAD`, or
the two pieces are inspecting different trees and their join is meaningless.

---

## 7. Why deletion is clearly the correct action (validity criterion 2)

- It is a **5-line pure helper with no caller, ever**, in a module whose other helpers
  (`floor_utc_bin`, `intervals_overlap`, `canonical_json`, `sha256_json`) all have live callers —
  so this is not a coherent public utility surface being left intact, it is one straggler.
- It is **not exported** by `loop/tkg_forecast/__init__.py`'s `__all__`, which is the package's
  explicit statement of its public API; the package docstring adds that it "is deliberately not
  imported by `loop`". There is no external consumer by design.
- There is **no packaging**, so it cannot be a library API anyone outside the repo depends on.
- **No test imports it**, so deletion does not break the suite. *(Reported as the dispatch asked: a
  test-only importer would have been a finding, not a disqualification. There is none — 1220 passed
  both with and without the sabotage.)*
- **No documentation mentions it** — not a README, not a design doc, not a knowledge-graph note,
  not a journal entry, in any revision. This is the property that separates it from
  `NetOutcomeResolver` (§9).
- "Leave it" has no defensible ground: no caller, no export, no test, no historical caller, no
  runtime execution, no documentation asserting it as a current component.

---

## 8. NOT_ESTABLISHED — what my method cannot rule out

Stated plainly, because a blind verifier needs the holes, not the confidence.

1. **Runtime name assembly. This is the single biggest hole.** A caller could do
   `getattr(core, "dataclass" + "_dict")`, or `getattr(core, some_var)` where `some_var` is read
   from a file or a journal. My token index cannot see a name that never appears as a contiguous
   token. I **checked and found no computed-name `getattr`/`import_module` anywhere in `eval/` or
   `loop/`** (H3) — but that is an enumeration of the sites I found, not a proof that none exists.

2. **"AST + grep over every .py" does not close the world in this repo, and I want that explicit.**
   This repo *does* dispatch on strings (`event_type` in `loop/trial_state.py` and
   `loop/tkg_forecast/forecast.py`). A `closed_world` claim here cannot rest on an AST walk. Mine
   rests on a **token index over all file types including string literals, JSON, markdown and
   `.jsonl`** — positive-controlled in §4 step 3b — and it is still subject to item 1.

3. **Corpus bound.** I scanned `/home/smoke01/dev/seza` (5,851 files, 2,009,519 lines) plus a
   `$HOME`-wide grep. I did **not** scan other machines, remote branches never fetched, or any
   consumer outside this filesystem. `git rev-list --all` covers local refs only.

4. **Runtime coverage is bounded by the test suite.** The sabotage proves no *test* executes the
   function. It does **not** prove no production path does — `make eval`, `runner.py --assets ALL`,
   `python3 -m project_memory sync`, and the pinned-ML path (`make test-tkg-ml`) were not run.
   Mitigating: the static scan finds no call site at all, so there is no path that *could* reach
   it. But the static scan and this mitigation are the same evidence base, not two independent ones.

5. **The 15 skipped tests** skip because the pinned ML runtime (torch) is absent. If one of them
   called `dataclass_dict`, my sabotage would not have fired. Their *source text* is in the corpus
   and contains no reference — so this is closed statically, not dynamically.

6. **Definition-line classification could in principle suppress a reference.** My scanner drops
   lines matching `^\s*(def|class) NAME\b`; a reference formatted to look like a definition would
   be dropped with them. I mitigated by reading all 3 DEF_SITES individually (§1.4) — each is a
   genuine `def` in a copy of `core.py`. At n=3 this is fully auditable; the technique would not
   scale to a symbol with hundreds of def-sites (`NetOutcomeResolver` has 13).

7. **n=1 on the sabotage discrimination.** `floor_utc_bin` is one live control, not a distribution.
   It is a strong control — same file, same technique, 2→21 — but it is one.

8. **The repo moves under the analysis** (§6). Any downstream piece that does not pin `ebdfd5f` is
   checking a different tree than I did.

9. **I did not adjudicate `loop/graph_memory.py`.** It was excluded by rule and I made no attempt
   to resolve the ablation 4/5/6 dispute. The one datum I have that bears on it — its import graph
   shows `n=1`, the lazy import in `program_db.py` — is recorded here without interpretation.

---

## 9. Candidates considered and rejected

| Candidate | Why rejected |
|---|---|
| `loop/graph_memory.py` | **Excluded by rule.** Disputed ground truth; not adjudicated (see §8.9). |
| `eval/forecast.py` (whole module) | Already disproved in the dispatch. My import graph independently confirms: **n=6** importers, including `eval/protocol.py` and `tools/derive_g4_thresholds.py`. |
| `eval/forecast.py :: NetOutcomeResolver` (class) | **Viable but strictly weaker, so rejected.** My scan: `n_ref=4, n_def=13`. All 4 refs are prose in `seza/knowledge/raw/kg-self-review/03-currency-and-gaps.md` (and its worktree duplicate) describing it as a live design entity — *"`code_component` forecast/prequential module; `NetOutcomeResolver` (shared…)"*. Zero **code** references, so it is probably dead too. But it sits in a heavily-imported module under `eval/`, it has 13 definition copies across worktrees (weakening my §8.6 mitigation), and a knowledge document asserts it as a current component — which makes "leave it, it is documented as part of the design" defensible, and criterion 2 forbids that. `dataclass_dict` has **no** mention of any kind, anywhere, in any revision. |
| Any whole module under `eval/` or `loop/` | **NONE FOUND.** All 39 have at least one importer (§1.1). |
| The 11 symbols at `n_ref` 1–3 | All genuinely live private helpers; their low counts are one real call site plus its worktree duplicates (§1.3). |
| Class methods and module-level constants | 855 definitions scanned; none at zero except the target (§1.3). |

---

## 10. State written

```
S1      = resolved
target  = /home/smoke01/dev/seza/backtest/loop/tkg_forecast/core.py :: dataclass_dict
          (lines 282-286, definition at line 282)
sha     = ebdfd5f8a7a2fbe61f1b7b1d25d16b7488a3c062   <-- P1V and P4 must pin this
stakes  = 2   (registry R7, dir-prefix "loop/", gate=checkpoint, owner=None)
owner-gated rows engaged: none (R1 / R2 / R3 all unreachable from this path)
positive control: PASSED on attempt 1 (attempt limit was 2)
expected P1V baseline noise: 5 pre-existing failures on a fresh worktree checkout
          (2x test_input_closure, 1x test_phase_a_authority, 2x test_worktree),
          1220 passed, 15 skipped
```
