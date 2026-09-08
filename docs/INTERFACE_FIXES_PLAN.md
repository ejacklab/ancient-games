# Tool-interface fixes — design plan (2026-09-08)

Answers EJ's question *"each tool is an independent tool — should we use an interface like OpenAPI?
… or a better schema/algorithm? index? table? hash table? list? tree?"*

**Verdict: no new interface format.** Five targeted fixes instead. The research is in
`docs/research/` — `INTERFACE_PRIOR_ART.md` (external), `INTERFACE_CENSUS.md` (our own failures),
`INTERFACE_CONTRARIAN.md` (attack on the premise), three deliberately different framings that
converged.

---

## 1. Why not a schema

**The failure class a schema addresses is already dead.** Failure rate by harness generation:

| generation | failed / calls | rate | static-shape failures |
|---|---|---|---|
| attempt1 | 2 / 5 | 40.0% | — |
| attempt2 | 33 / 92 | 35.9% | 14 of 35 |
| attempt3 | 7 / 83 | 8.4% | 2 of 18 |
| attempt4 | 11 / 109 | 10.1% | **0 of 109 calls** |

Pooling these four generations (MAIN's first pass did) hides the trend entirely. **MAIN's own
classification was wrong and is corrected here**: it reported "29 semantic (55%)". Replaying that
rule shows the bucket held 15 bare `internal-error: False|True|'no'` (arg errors wearing a crash's
clothing), 9 correct-by-design declines (`no-prove-pass`, `uncommitted-changes`,
`checkpoint-not-cleared` — a regression to "fix"), and 5 `ctx.actor` precondition failures.
**Genuinely semantic: 1 of 53.**

**What actually fixed the arg-shape class was content, not format.** Per-field A/B against the
packet each agent really received: `record_claim`+`record_check` **14/34 → 0/93** once the schema
printed their enums (Fisher p=9.0e-10); `framings` **3/14 → 0/9** on ~90 characters
(`dict` → `dict[str, list[str]]  # {claim_id: [framing,...]}`). Both arms already carried a table
(`tools --inputs`) *and* a tree (`tools --schema`) — presentation topology moved nothing.

**The literature isolates the same variable.** [arXiv 2607.14167](https://arxiv.org/abs/2607.14167)
measured keyed-JSON vs identical content as prose at **+2pp / 0pp, both intervals including zero**,
while feedback naming the **admissible alternatives** moved terminal success **+44pp** (14/50→36/50,
Qwen2.5-Coder-14B) and **+42pp** (Llama-3.1-8B), with the ablation locating most of the gain in the
admissible-alternatives field specifically. JSON Schema is a change of representation. Every win
this repo has measured came from content.

**Cost if we did it anyway:** ~1,987 → ~3,308 tokens (pretty JSON) read into context every run,
28% of the bytes structural punctuation, carrying the identical 23 `cli.NOTES` strings, and
duplicating an `additionalProperties: false` that `types.hydrate` already enforces.

**On harness ≥ v1.3 there are 8 live interface failures left, and 6 are the CLI tool-name
positional** — `argparse`, not the tool surface.

---

## 2. The five fixes

Ordered by severity, not by effort. F1 and F2 are correctness; F3–F5 are the measured
"admissible alternatives" mechanism applied where it is still missing.

### F1 — constrain `record_claim.author` (corroboration is forgeable)

**Evidence (reproduced end to end through the real CLI, MAIN, not inferred):** three
`record_claim` calls with `author` = `ghost-1|2|3`, **zero `dispatch` events**, then:

```
Corroborate: C1: n=3/3; reconciled=they agree, dominance=ej (owner of R1).
```

on a stakes-3, governance-gated, `kind=judgment` claim. (At stakes 1 it reports `n=1 (single
source)`; the forge needs the stakes-3 path — worth stating, because the first repro attempt did
not reproduce it.)

`stages.py:325` counts category-(a) sources as `[e for e in recorded if e["author"] != claim.actor]`
— a **caller-supplied string**. `author` appears **0** times in `lints.py`, `invariants.py`,
`_plan.py`. All 33 real `record_claim` calls used `"MAIN"`, so constraining it breaks nothing.

**Change** — in `tools/record_claim.py::run`, before writing: accept `author` only if it is
`"MAIN"` or an `agent_id` carrying a `dispatch` event in this run. Reject with `invalid_args`
naming the admissible set (which is exactly `{"MAIN"} ∪ dispatched agent_ids`, already derivable
from the journal — the same shape `record_check.falsifies` already uses).

**What this does NOT fix, stated plainly:** an agent can still `dispatch` and then author claims as
that agent without the agent having done the work. This raises forging from *typing a string* to
*spending a journaled, I5-capped dispatch*. The residual is the same hole already recorded against
`ingest_return` (a dispatched agent's self-declared claim kind) and is not closed here.

### F2 — give `record_check` the validator its twin already has

**Evidence (run at HEAD by MAIN):**

```
record_check  → internal-error: check_executed.mechanism must be one of (...)   exit 0   ("executed")
record_claim  → invalid-args: evidence_type must be command | file:line ...     exit 2   (declined)
```

`record_check.py` has **0** uses of `invalid_args`; `record_claim.py` has 5. Bad enums and
mistyped `expected`/`observed` fall through to `journal.validate_event`, surface as
`internal-error:`, and — because `cmd_call` keys `EXIT_REFUSED` on the `invalid-args:` prefix —
**exit 0**, telling the caller the call executed. ABLATION_1's H2 fix ("a bad input is the caller's
error, named by field and accepted values — never an `internal-error`") is incomplete; H2 is
reopened.

**Change** — validate `mechanism` (against `MECHANISMS` + `other:<name>`), `pre_fix_result`
(`FAIL|None`), and the `expected`/`observed` types in `record_check.run`, each via `invalid_args`.
Keep the existing `falsifies` message, which is already the right shape.

**Also fix the exit code honestly:** a declined-for-bad-input result must exit 2 regardless of
which helper produced it. Prefer making `internal_error` unreachable for caller errors over
widening `cmd_call`'s prefix test — the prefix test is the contract, and widening it would let a
genuine internal error masquerade as a decline.

### F3 — reject a `call` tool name that starts with `{`

**Evidence:** 6 of the 8 live interface failures on harness ≥ v1.3; all one run
(attempt4/UC2J), 5.5% of that run's budget. The args JSON landed in the CLI's tool-name
positional. Structurally unfixable *inside* the tool surface — a real tool-calling API separates
`name` from `arguments` by construction; a CLI positional does not.

**Change** — in `cmd_call`, before `load_tools`: if the tool name starts with `{`, return
`EXIT_REFUSED` with the correct invocation shape (`call <tool> '<json args>'`) rather than
journaling `unknown-tool: {"claim_id"...`.

**Scope honestly:** `INSUFFICIENT_DATA` on frequency — 6 occurrences, 1 agent, 1 run. Cheap enough
that this does not matter; it is ~3 lines and removes a whole failure mode's worst case.

### F4 — re-key `cli.NOTES` by `(owner, field)`

**Evidence:** `NOTES` is `dict[str, str]` keyed by **bare field name**, consumed at `cli.py:215`
(dataclass fields) and `cli.py:237` (tool args). `Claim.actor`'s note therefore leaks onto
`record_claim.actor`, and `tools --schema` prints:

```
record_claim
  actor: str  # set by corroborate from ctx.actor — never passed by the caller
```

while `record_claim`'s MANIFEST declares `actor` a **required input**. The schema states something
provably false about a load-bearing argument. (This is the literal answer to EJ's "hash table?" —
yes, and its key is wrong.)

**Change** — allow `(owner, field)` keys with a bare-`field` fallback, so genuinely shared notes
stay shared and `record_claim.actor` gets its own. Add a test that every printed note is true of
the field it is printed against — mechanically, that no note says "never passed by the caller"
about a field in some tool's `MANIFEST["inputs"]`.

### F5 — make run-dependent rejections enumerate the legal values

**Evidence:** the +44pp mechanism, applied where it is still missing. `stages.py:463` raises
`ctx.actor has no entry for action {action!r} (set at C·3/C·4 or by D)` — it names the bad value
and **not** the admissible set, which it is holding (`ctx.actor` keys). 5 declines. The pattern
already works here: `record_check.falsifies` enumerates known claim_ids and has 0 failures since.

**Change** — append `sorted(ctx.actor)` to that message. Then sweep for the same shape: a rejection
whose admissible set is computed (or trivially available) at rejection time and thrown away.
`guard.unmatched_tripwire_keys` already returns the legal keys and is a candidate; check what it
currently prints before changing it.

**Deliberately not generalised into a mechanism.** Two of the three historic hotspots sit at 0
failures across 99 calls; a general framework would be built past the point of return.

---

## 3. Not building, with reasons

| rejected | why |
|---|---|
| JSON Schema / OpenAPI emission | §1. OpenAPI is an HTTP spec (paths, verbs, status codes) describing nothing here; the JSON Schema subset is a format change measured at ~0, addressing a class already at 0 failures. |
| YAML output | Measured 2,390 vs 1,987 tokens — worse than the text surface it would replace, and PyYAML would be this package's **first runtime dependency** (`pyproject` declares `dependencies = []`). |
| Precondition DAG | 7 of 18 nodes have preconditions, 10 edges, longest chain 5 — already implemented as per-tool predicate lists. Fails `STORE_DESIGN_DECISION.md`'s own written reopen trigger on all three counts. The repo has twice built structures nobody queried. |
| Dynamic tool availability (hide unavailable tools) | 0 of 53 failures attributable. **Veto:** turning a precondition into an absence deletes the refusal events `ablation/score.py` q4 reads as evidence, and ABLATION_1's "the human gate held against free agents, twice" is made of exactly those events. |
| Constrained / grammar-guided decoding | Structurally unavailable: the framework does not host the model (the agent shells out to a CLI), so there is no logit stream to mask. |
| Programmatic tool calling | Reported up to +18.8pp on long chains, and our tools are already typed Python — but it hands the agent an interpreter in the run's `cwd`, letting it `git commit` directly and route around `loop.step`. Dies on the invariant floor. |
| Printing `suggested_next` in `call` | Would contaminate ABLATION_1's 8-of-8 emergent-stage-order finding, which is a live result. |

---

## 4. Tests (e2e, per the standing rule)

1. F1: three `record_claim` calls with invented authors and no dispatch → refused, message names the
   admissible set. **The forge repro above becomes a regression test** and must go from `n=3/3` to refused.
2. F1: `author="MAIN"` still works; an author matching a real `dispatch` in this run still works.
3. F1: replaying all 33 historic `record_claim` calls still succeeds (the "breaks nothing" claim, asserted).
4. F2: out-of-enum `mechanism`, bad `pre_fix_result`, mistyped `expected` → each `invalid-args:` **and exit 2**.
5. F2: `record_check`'s existing `falsifies` behaviour is unchanged.
6. F3: `call '{"claim_id":...}'` → exit 2 naming the correct invocation shape; a real unknown tool still journals `unknown-tool`.
7. F4: `record_claim.actor` no longer prints "never passed by the caller"; `Claim.actor` (inside `corroborate`) still does.
8. F4: the mechanical check — no note claiming a field is never caller-passed appears against a field in that tool's `MANIFEST["inputs"]`.
9. F5: `corroborate` with an unknown action names the legal actions; with a legal action, unchanged.
10. All 318 existing tests still pass.

**Verified by sabotage, not assertion** (standing bar, and it has found two real defects this
session): each fix must have a one-line mutation that fails a case. Specifically — F1 accepting any
string, F2 falling back to `internal_error`, F4's fallback lookup ignoring the owner key.

---

## 5. Sequencing and risk

F1 first (it is the only correctness hole with a live exploit), then F2 (silent exit-0 on caller
error), then F3/F4/F5 which are independent and low-risk. Nothing here touches `loop.step`, the
invariant floor, or the autonomy layer.

**Main risk:** F1 changes what `corroborate` counts, so a run that previously reached `n=3/3` by
authoring under several names now will not. That is the point, but it means any stored ablation
journal replayed as a fixture may score differently — check `ablation/score.py` q3/q5 against the
attempt4 journals before and after, and record any movement rather than absorbing it.

**Open, not addressed here:** `ingest_return` still accepts a dispatched agent's self-declared
claim kind (D-KIND's remaining hole); F1 narrows the neighbouring surface without closing it.
