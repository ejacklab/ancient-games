# Tool-interface fixes — implementation plan

Executes `docs/INTERFACE_FIXES_PLAN.md` (design, as amended by review `aad7630`). Read that first
for *why*; this document is *how*, and is meant to be followed without re-deriving the decisions.

**Baseline:** `aad7630`, tree clean, `python3 -m pytest -q` → **318 passed**. Every step below ends
green; do not carry a red suite across steps.

**Order is not arbitrary.** F1 and F2 are correctness (a live forge; a caller error reporting
success). F3–F5 are the measured "admissible alternatives" mechanism applied where it is missing.
Each is an independent commit so any one can be reverted alone.

---

## Step 0 — pin the current behaviour before changing it (one commit)

Write the two forge reproductions as **failing** tests first, in `tests/test_interface_fixes.py`.
They must FAIL at this commit — that is what proves they test the hole and not the fix.

```
test_forge_via_record_claim_is_refused          # xfail(strict=True) at step 0
test_forge_via_ingest_return_is_refused         # xfail(strict=True) at step 0
```

Both: `ctx.actor = {"claim the thing": "MAIN"}`, `ctx.governance_gated = "R1"` (stakes 3 →
`n_required` 3 — at stakes 1 corroborate short-circuits to `n=1 (single source)` and the forge does
not reproduce), three authored claims under invented ids, zero `dispatch` events, then
`corroborate`. Assert on `exit_line`.

Remove the `xfail` in step 1. Rationale: this repo has twice shipped a green test that could not
fail; a test written after its fix cannot demonstrate it ever could.

---

## Step 1 — F1: constrain the author at both writers

### 1.1 New helper — `ancient_games/hybrid/tools/_shared.py`

```python
def dispatched_agent_ids(events: list[dict]) -> set[str]:
    """agent_ids this run actually dispatched (journaled, I5-capped)."""
    return {e["agent_id"] for e in events if e.get("event") == "dispatch"}


def eligible_authors(events: list[dict]) -> set[str]:
    """Who may author a `claim_recorded` in this run: MAIN, or an agent this run dispatched.

    B·1 counts category-(a) sources as `author != actor` (stages.py:325), so `author` is
    load-bearing and was previously a free caller string: three invented names bought n=3/3 with
    zero dispatches. Policy lives here, in the tool layer — `journal.py` records events and is not
    the gate."""
    return {"MAIN"} | dispatched_agent_ids(events)


def author_refusal(author: str, events: list[dict]) -> ToolResult | None:
    ok = eligible_authors(events)
    if author in ok:
        return None
    return invalid_args("author", "MAIN, or an agent_id this run dispatched (" + ", ".join(sorted(ok)) + ")", author)
```

`events` MUST come from `Journal(...).read()` (run-scoped). Using `read_all()` here would let
another run's dispatches authorise this run's claims.

### 1.2 `tools/record_claim.py::run`
After the existing `evidence_type` check, before the `try`, read the journal and apply
`author_refusal(args["author"], journal.read())`. Move the `Journal(...)` construction above the
`try` (it does no I/O) so the check can use it; keep `journal.claim_recorded(...)` inside.

### 1.3 `tools/ingest_return.py::run`
Same check on `args["agent_id"]`, which `journal.py:271` passes through as the claims' `author`.
Apply it **before** `journal.ingest_return(...)`, because that call writes the `return` event and
the claims together — a partial write would leave a `return` with no claims.

**This is the fix the review caught.** Constraining only `record_claim` leaves an equivalent and
in fact stronger path: `ingest_return` also writes a `return` event, so a forged journal reads as
genuine agent returns.

### 1.4 Pin the writer set — `tests/test_interface_fixes.py`

```python
SANCTIONED_CLAIM_RECORDED_WRITERS = {
    "ancient_games/journal.py",                       # the ingest_return mirror (guarded in ingest_return.py)
    "ancient_games/hybrid/tools/record_claim.py",     # the direct writer
}
```

AST-walk `ancient_games/**/*.py` for `Call` nodes whose func is an attribute named
`claim_recorded`, excluding the definition site. Assert equality with the set above. Model on
`tests/test_review_b_fixes.py::test_f8_read_events_importers_are_the_sanctioned_set` (same shape,
lines 356–388). A third writer must not appear silently — that is exactly how this hole would reopen.

### 1.5 Tests
- the two step-0 forges now **refused**, message naming the admissible set
- `author="MAIN"` still writes; a genuinely dispatched `agent_id` still writes (dispatch → record_claim under it)
- **historic replay:** for every journal under `ablation/runs/**`, assert
  `authors ⊆ {"MAIN"} ∪ dispatched`. Verified true today (only attempt4/UC3 dispatched — `adv-1` —
  and recorded all claims under `MAIN`); this pins the "breaks nothing" claim rather than asserting it.
- the AST pin

### 1.6 Sabotage
`eligible_authors` returning any string → the forge tests fail. Run it against **each writer
separately** (guard removed from `record_claim` only, then `ingest_return` only): both must fail.
A sabotage that only fails one means the other path is untested.

---

## Step 2 — F2: `record_check` validation and its exit code

### 2.1 `tools/record_check.py::run`
Import `MECHANISMS` from `ancient_games.ctx` and `_ENUMS` from `ancient_games.journal`
(`_ENUMS[("check_executed", "pre_fix_result")]` → `("FAIL", None)`). Add, before the `try`:

- `mechanism` ∈ `MECHANISMS` **or** matches `other:<name>` with a non-empty name — mirror
  `journal.validate_event`'s rule exactly; do not re-derive it, or the two drift.
- `pre_fix_result` ∈ `("FAIL", None)`
- `expected` / `observed` are `str | int` (the `_NUM_OR_STR` shape)

each via `invalid_args`.

### 2.2 The `falsifies` message — review P1b
`record_check.py:35` returns a bare `FALSIFIES_REASON` with no `invalid-args:` prefix, and
`cmd_call` keys `EXIT_REFUSED` on that prefix, so a bad `falsifies` **exits 0 today** (confirmed at
HEAD). Wrap it with `invalid_args` while **retaining the enumerated detail** — this call's
`claim_id` and the claim_ids recorded in this run. That detail is the admissible-alternatives
content and is why the field has had 0 failures since it was added; losing it to gain a prefix
would be a net regression.

```python
return invalid_args("falsifies",
                    f"a claim_id — put the condition in `expected` (this call's claim_id is {claim_id!r}; "
                    f"claim_ids recorded in this run: {known})", falsifies)
```

### 2.3 Do NOT widen `cmd_call`'s prefix test
The `invalid-args:` prefix is the contract between the tool layer and the CLI's exit code. Widening
it to catch `internal-error:` would let a genuine internal error masquerade as a clean decline —
the opposite of the defect being fixed. Make `internal_error` unreachable for caller errors instead.

### 2.4 Tests
- out-of-enum `mechanism`, bad `pre_fix_result`, mistyped `expected` → each `invalid-args:` **and CLI exit 2**
- bad `falsifies` → keeps `claim_id` and the known-ids list in the message **and now exits 2** (today: 0)
- `other:my-thing` is still accepted; a bare `other:` is not
- a valid call is byte-identical to today's event

Assert the **CLI exit code**, not only `ToolResult.reason` — the exit code is the defect.

### 2.5 Sabotage
Any one validator falling back to `internal_error` → its test fails on the exit code.

---

## Step 3 — F3: reject a `call` tool name that starts with `{`

`cli.py::cmd_call`, first statement after `read_manifest`:

```python
if a.tool.lstrip().startswith("{"):
    print(json.dumps({"error": "the tool NAME goes first, then its args: "
                               "call <tool> '<json args>' — got JSON in the tool-name position"}), file=sys.stderr)
    return EXIT_REFUSED
```

Before `load_tools` and before the journal is touched: today this path journals a `tool_call` with
`unknown-tool: {"claim_id"...` and spends budget. 6 of the 8 live interface failures on harness
≥ v1.3, all in one run, 5.5% of its budget.

**Tests:** JSON in the name slot → exit 2, nothing appended to the journal; a genuine unknown tool
(`call bogus '{}'`) still journals `unknown-tool: bogus` and behaves exactly as today
(`tests/test_ablation_harness.py` already pins this — it must still pass unchanged).

---

## Step 4 — F4: re-key `cli.NOTES` by `(owner, field)`

### 4.1 Change
`NOTES` becomes `dict[str | tuple[str, str], str]`. One lookup helper, used by both sites:

```python
def note_for(owner: str, field: str) -> str | None:
    return NOTES.get((owner, field), NOTES.get(field))
```

- `_field_lines` (cli.py:215) — owner is `cls.__name__`; thread it in (it already recurses per class)
- `tools_schema` (cli.py:237) — owner is the tool `name`

Then move the offending entry: `"actor"` becomes `("Claim", "actor")`, so `record_claim.actor`
(a **required input**) no longer prints *"set by corroborate — never passed by the caller"*. Give
`("record_claim", "actor")` its own note describing what it actually is.

### 4.2 The mechanical check — the point of the fix
```
test_no_note_claims_a_field_is_never_caller_passed_when_a_tool_requires_it
```
For every tool and every `arg` in its `MANIFEST["inputs"]`, assert the note rendered against that
arg does not contain "never passed by the caller". This catches the *class*, not the instance —
the standard `ctx.CHECKED_CONSUMERS` already sets in this repo.

### 4.3 Also check `ENUMS` for the same collision
`ENUMS` is keyed by bare field name too and is consumed at the same two sites, so it can print a
*wrong enum list* against a same-named field of a different owner. **Check whether a real collision
exists before changing anything** — if none does, leave it and record that in the commit message.
Do not re-key a hash nobody has shown to be wrong.

---

## Step 5 — F5: rejections enumerate their legal values

### 5.1 `stages.py:463`
```python
raise ValueError(f"ctx.actor has no entry for action {action!r} (set at C·3/C·4 or by D); "
                 f"actions with an actor: {sorted(ctx.actor)}")
```
5 declines. This is the +44pp mechanism (`arXiv 2607.14167`: naming admissible alternatives, not
the format, carried the gain) applied where the set is already in hand.

### 5.2 `guard.py::unmatched_tripwire_keys` — review P2
It **computes** `allowed = {k for h in hit.hubs for k in hit.tripwire_keys(h)}` and then returns
`(unmatched, list(hit.hubs))`, discarding `allowed`. Its own docstring says a key may be the hub's
name **or** the path of a ref that matched into it, so hubs is a strict subset — printing it is
incomplete and, for a path-alias key, misleading.

Return `(unmatched, sorted(allowed))` and print that. **Keep the `consumers` clause**: where
`hit.hubs` is empty, `allowed` is empty too, and an empty admissible set is not guidance — that
clause is the only part telling the caller what to do next.

`unmatched_tripwire_keys` is imported elsewhere? Check before changing the return shape; if it has
other callers, add `allowed` as a third element rather than replacing the second.

### 5.3 Tests
- unknown action → message lists the legal actions; a legal action → unchanged
- a tripwire keyed by a **matched-ref path alias** is accepted (the case hubs-only would have misreported)
- empty-hubs case still carries the `consumers` clause

### 5.4 Stop here
Do **not** generalise this into a mechanism. Two of the three historic hotspots sit at 0 failures
across 99 calls; a framework would be built past the point of return.

---

## Verification

Per step: `python3 -m pytest -q` green, then the step's sabotage mutation must fail the named
test(s), then revert the mutation. Record the counts in the commit message — that is the evidence
separating "tested" from "enforced", and it has caught two real defects this session.

Final gate:
```bash
python3 -m pytest -q                 # expect 318 + new, all green
git status --short                   # clean
python3 -m ancient_games.hybrid tools --schema | grep -c "never passed by the caller"   # F4
```

**F1 changes what `corroborate` counts, so re-score the stored journals:** run
`ablation/score.py` over `ablation/runs/attempt4/**` before and after step 1 and diff q3/q5.
Movement is expected only if a historic run authored under a non-dispatched name — the replay test
in 1.5 says none did, so **any movement here means the replay test is wrong**; investigate rather
than absorb it.

## Risks and rollback
- Each step is one commit; revert individually.
- F1 is the only step that changes scoring semantics. If a downstream consumer breaks, revert step 1
  alone — F2–F5 are independent.
- F4 touches the rendering path every agent reads. A mistake there is loud (schema output changes)
  and caught by the `tools --schema` golden expectations in the existing suite.

## Out of scope
`ingest_return` still accepts a dispatched agent's self-declared claim *kind* (D-KIND's remaining
hole). F1 narrows the neighbouring surface — forging now costs a journaled, I5-capped dispatch
instead of a typed string — without closing it.
