# The Ancient Games — v1 spine

The Ancient Games is an agent-orchestration framework: five fixed algorithms
— **C** Gate(task), **D** Guard(action), **B** Corroborate(claims, stakes),
**E** Filter(candidates), **A** Prove(plan) — that decide how many agents a
task gets, which actions are gated and by whom, how many independent sources
a load-bearing claim needs and whether it has them, what survives filtering,
and whether the resulting plan is cleared. Every decision the spine makes is
derived from a typed `ctx` object, a data-only registry of high-stakes
artifacts, and an append-only trace journal; the `[LLM]` judgment cells
(difficulty, framings, claim kinds, reconciliation) are explicit parameters,
never computed here.

This package is the **program side only** of that framework, implemented from
`V3_3_SPEC.md` (the spec of record, copied into `tests/fixtures/`). It makes
no LLM calls, opens no network, and uses only the Python standard library.
Its purpose is to make the framework's own correctness oracle executable: the
spec's eight trace test cases (two real runs, T1/T2, and six constructed
cases) and its nine lints run as a pytest suite instead of being checked by
eye across successive review rounds.

The source-counting rule in `stages.count_sources` implements V3.3 literally
and is isolated so that V3.4's self-exclusion rule (review finding Y2)
replaces that one function. Three tests are `xfail(strict=True)` pending
V3.4: the Case 1 trace (Y2) and the two replay assertions that depend on
`consumer_check` events §10 does not yet list (Y4). See `DECISIONS.md` for
every choice the spec left open.

## Running the tests

```bash
cd ~/dev/ancient-games
python3 -m pytest -q          # 62 passed, 3 xfailed
python3 -m pytest -q -rx      # list the three strict xfails and their reasons
```

No installation is needed (stdlib only); `pytest` is the only test dependency.

## Modules

| module | implements (spec §) | notes |
|---|---|---|
| `ancient_games/ctx.py` | §2 ctx object | `@dataclass` with every property, typed; `validate()` raises on a property set by no stage or referenced by no field (`CTX_META`) |
| `ancient_games/registry.py` | §3 registry | rows R1–R9 as data; D6 matching (dir prefix / file exact / callable import path / action verb / R9 per-instance); D2 same-ref specificity suppression; D2′ hub union; `lookup(refs) -> (stakes, hubs, gate, owner)` |
| `ancient_games/schema.py` | §5 field tables, §6 return contract | `FIELDS` rows with `when(ctx)`, `payload(ctx)`, `return_contract(ctx)`; escape values per row; `TEMPLATE_HEADINGS` in D7 order |
| `ancient_games/stages.py` | §4 C/D/B/E/A — spine parts only | one function per algorithm, `ctx` + `[LLM]` inputs as parameters; exit lines emitted via the journal; `count_sources` is the single owner of B·1's rule |
| `ancient_games/lints.py` | §8 all nine lints | `lint_x(input) -> list[Finding]`, pure; `run_all_on_plan` is what A runs |
| `ancient_games/journal.py` | §7 events | append-only JSONL at an absolute path (relative ⇒ `ValueError`); typed shapes for all seven events; `read_events(path)`; `ingest_return` mirrors `CLAIMS` into `claim_recorded`/`check_executed` |
| `ancient_games/trace.py` | §10 trace format | renders stage exit lines + per-claim corroboration table + consumer checks + dispatches from journal events |

## Tests

| file | covers |
|---|---|
| `tests/test_traces.py` | all eight §10 cases end to end, T2/T1 matched against `fixtures/T2_trace.md`/`T1_trace.md`, trace replays |
| `tests/test_lints.py` | a FAIL and a PASS input for every one of the nine lints |
| `tests/test_registry.py` | matching semantics, specificity suppression, the D2′ union |
| `tests/test_schema.py` | `payload`/`return_contract` for T2 (count=0), T1, T3; escape values; D7 headings |
| `tests/test_journal.py` | absolute-path enforcement, round-trip, shape validation |
| `tests/test_self_lint.py` | the nine lints against the spec's own tables (`fixtures/V3_3_SPEC.md`) |
| `tests/test_ctx.py` | `validate()` and enum checks |
| `tests/cases.py` | the eight case builders shared by the above |
