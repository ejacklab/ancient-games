# HYBRID_SEQUENCES.md — §8, v1.4, companion to `HYBRID_SPEC.md` v1.4

Per MAIN's targeted scope for this round (`DECISIONS_HYBRID_4.md`): only Adversarial A (the
`live_dispatches` computation, L3) and UC1's `gate` step (`hydrate`'s recursion, L2) are fully re-walked.
Every other sequence keeps its v1.3 shape; the two mechanical wording swaps L1 forces (`env.ctx` for
`prove`/`done` is a `Ctx` with four fields nulled via `dataclasses.replace`, never a `dict`) are applied
wherever that phrase appeared, with no other change to any step, outcome, or exit line.

> Every tool call below is `TOOLS[name].fn(env, args)`, `env = ToolEnv(run_id, journal_path, ctx)`,
> returning `ToolResult(ok, value, reason)`. `ctx` is always a real `Ctx` instance (`HYBRID_SPEC.md` §2,
> L1) — for `prove`/`done` specifically, `dataclasses.replace(ctx, n_sources=None, corroboration_
> capped=None, framing=None, siblings=None)`, never a plain dict. `guard`/`commit` compute `action_id`
> per §2's formula. `filter_candidates` receives the real `ctx` and its own real `args` (K3 — not
> I3-restricted). `done` is genuinely executed and performs I2's two clauses itself (K8).
> `dispatch`'s `agent_id` is `f"{role}-{framing}-{uuid4().hex[:8]}"` (§2/§3); the short, human-readable
> names used below (`"historian"`, `"A"`, `"B"`, ...) are illustrative shorthand for that generated
> value, unchanged from v1.3's own convention — Adversarial A below shows the real format once.

> **Harness v1.3 (H8, `HYBRID_SPEC.md` §4 "Claim coverage"):** every `prove` step below already sits
> after a `corroborate` step naming every claim the sequence recorded (UC1 step 8, UC2 steps 11/17,
> UC7 step 13; UC3–UC6 likewise), so no sequence gains a step and no exit line changes. What changes
> is the counterfactual: a sequence that reached `prove` with a recorded claim and no `corroborate`
> for it would now get `RETURN_TO_PLANNER: run corroborate for <claim_id>` instead of a PASS on an
> empty plan, and one with no recorded claim at all gets `RETURN_TO_PLANNER: no claims recorded`.

---

## UC1 — T2, one-line fix + class-level guard (zero dispatch)

```
 1. gate(env, args={name, stop_criterion, difficulty:"LOW", capability:[],
    probe:{"path":"research/stability.py","mode":"read"}})
      hydrate(TaskInput, args) (§2, L2): `probe` is a dict with keys `{path, mode}` — TaskInput's own
      field is typed `probe: ArtifactRef | None`, a dataclass, so hydrate recurses into it:
      `hydrate(ArtifactRef, {"path":"research/stability.py","mode":"read"})` → a real `ArtifactRef`
      instance, not a leftover dict. This is T2's own first tool call, literal — the exact case v1.3's
      L2 finding was reproduced against (naive `TaskInput(**args)` would have left `task.probe` a dict,
      and `stages.gate`'s own `task.probe.mode` read, `stages.py:79`, would have crashed on it).
      → ToolResult(ok=True, value=GateExit(PLAN_NEEDED count=0))
 2. guard(env, args={"action": {"name": "research-and-tests-edit",
    "refs": [{"path":"research/stability.py","mode":"mutate"},
             {"path":"tests/test_research_importable.py","mode":"mutate"}]}})
      hydrate(ActionInput, args["action"]): `refs` is `list[ArtifactRef]` — hydrate maps `hydrate
      (ArtifactRef, item)` over each dict in the list, so `action.refs` is `[ArtifactRef(...),
      ArtifactRef(...)]`, not `[dict, dict]` — the second literal case L2 was reproduced against
      (`stages._ref_paths`, `stages.py:177-178`, reads `.path` off each element).
      → ToolResult(ok=True, value=GuardExit(NO_GATE stakes=1))
      action_id = action_id("mutate", ["research/stability.py","tests/test_research_importable.py"])
      tool_call.args["refs-paths"] = the same two paths — this is what I1′ reads later (K2), matched by
      exact string equality against `git diff --name-only HEAD`, never a directory prefix (M3)
 3. guard(env, args={"action": {"name":"commit-to-master",
    "refs":[{"path":"master","mode":"mutate","verb":"commit"}]}})
      → ToolResult(ok=True, value=GuardExit(GATED stakes=2, checkpoint))
      action_id = action_id("commit", ["master"])
 4. record_check(env, args={claim_id:"import-succeeds", mechanism:"interpreter-import", ...})
 5. record_check(env, args={claim_id:"import-succeeds", mechanism:"pytest-fail-first", pre_fix_result:"FAIL", ...})
 6. record_check(env, args={claim_id:"no-regression", mechanism:"suite-count", expected:274, observed:274})
 7. record_check(env, args={claim_id:"no-regression", mechanism:"git-diff-scope", ...})
 8. corroborate(env, args={"action":"commit-to-master", "claims":[...]})
      → ToolResult(ok=True, value=CorroborateExit(SOURCES 2/2, 2/2))
 9. filter_candidates(env, args={"candidates":[...], "cut":{...}, "follow_on":[...]})
      — env.ctx is the REAL ctx (K3: filter_candidates is not I3-restricted); args carries its own real
        payload, unlike v1.2's dead-JSON case-file bug
      → ToolResult(ok=True, value=FilterExit(kept=3, merged=0, cut=1, follow_on=2))
10. prove(env, args={})
      — env.ctx is `dataclasses.replace(ctx, n_sources=None, corroboration_capped=None, framing=None,
        siblings=None)` — a `Ctx`, not a dict (I3, narrowed to {prove, done}; L1: `stages.prove`'s own
        `ctx.keys_set()` call, `stages.py:671,673`, works normally against this)
      → ToolResult(ok=True, value=ProveExit(PASS)); tool_call.exit_type="PASS" journaled (K5)
11. ★ approval_recorded{gate="checkpoint", action_id="commit:['master']", approver="ej",
      note="checkpoint cleared"} — orchestrator-written, postdates nothing yet (first commit)
12. commit(env, args={"message": "fix research.stability import; add importability test"})
      — no `action_id` argument (§2, dropped — commit self-computes "commit:['master']")
      I1′ (loop pre-check): changed={research/stability.py, tests/test_research_importable.py};
           last_commit_ts=None; covered = args["refs-paths"] from steps 2 ∪ 3 (both in window) ⊇ changed
           → PASS
      I4′(b): both files → R8 (stakes=1, gate=none) → PASS
      commit's own body: checkpoint precondition — approval_recorded from step 11, action_id matches,
           postdates last_commit_ts(None) → PASS → git commit runs → ToolResult(ok=True, value={"hash":"..."})
13. done(env, args={})
      — env.ctx is `dataclasses.replace(ctx, ...)`, a `Ctx` (L1); done is genuinely EXECUTED (K8), not
        skipped by the loop
      (a) freshness: proves=[step 10]; staling = non-refused mutate-side-effect events after step 10's
          ts — none (commit at step 12 is side_effects="commit", categorically excluded) → clause (a) PASS
      (b) clean tree: `git diff --name-only HEAD` after step 12's landed commit → empty → clause (b) PASS
      → ToolResult(ok=True, value="DONE") → loop returns ctx, "DONE"
```

**13 steps**, identical count and outcome to v1.3 — only step 1's annotation and steps 10/13's `env.ctx`
description changed (L1, L2). Zero `dispatch` calls (R6). `live_dispatches` end = 0 trivially.

---

## UC2 — T1, dead-code audit + safe deletion (guard + hub + tripwire)

Unchanged from v1.3 in every step and outcome; `env.ctx` for step 13's `prove` call is `dataclasses.
replace(ctx, n_sources=None, corroboration_capped=None, framing=None, siblings=None)` (a `Ctx`, L1),
not a stripped dict — the only wording change from v1.3.

```
 1. gate(env, args={count-shaped fields for "delete six dead helpers"})
      → ToolResult(ok=True, value=GateExit(PLAN_NEEDED count=1, dispatched))
 2. dispatch(env, args={"role":"researcher","framing":"schema-dispatch-read"})
      → ToolResult(ok=True, value="historian")           — I5′: live 0<3 → PASS, live=1
 3. guard(env, args={"action": {"name":"delete-six-helpers",
    "refs":[{"path":"loop/program_db.py","mode":"mutate","consumers":["loop/program_db.jsonl"]}]}})
      → ToolResult(ok=True, value=GuardExit(GATED stakes=2, hub=["loop/program_db.jsonl"], checkpoint))
      action_id = action_id("mutate", ["loop/program_db.py"]); args["refs-paths"]=["loop/program_db.py"]
 4. ingest_return(env, args={"agent_id":"historian", "fields": {CLAIMS:[six-are-dead]}})
      — I5′: live 1 → 0
 5. record_claim(env, args={author:"MAIN", claim_id:"six-are-dead", actor:"MAIN", framing:"text-reference-scan"})
 6-8. record_check(env, args={claim_id:"journal-untouched", mechanism:"hash-compare", ...}) × 3
      (identical command ⇒ counts once, Z5′)
 9. record_check(env, args={claim_id:"journal-untouched", mechanism:"git-diff-scope", ...})
10. record_claim(env, args={author:"MAIN", claim_id:"journal-untouched", ...bare citation, no expected value})
11. corroborate(env, args={"action":"delete-six-helpers", "claims":[six-are-dead, journal-untouched]})
      → ToolResult(ok=True, value=CorroborateExit(six-are-dead CAPPED 1/2, journal-untouched SOURCES 2/2))
12. filter_candidates(env, args={...})  — real ctx, real args (K3)
      → ToolResult(ok=True, value=FilterExit(...))
13. prove(env, args={})  — env.ctx = dataclasses.replace(ctx, ...), a Ctx (L1)
      → ToolResult(ok=True, value=ProveExit(RETURN_TO_PLANNER)); exit_type="RETURN_TO_PLANNER"
      — default_plan resets to [corroborate, filter_candidates, prove]
14. dispatch(env, args={"role":"researcher","framing":"independent-static-scan"})
      → ToolResult(ok=True, value="static-scanner")      — I5′: live 0<3 → PASS, live=1
15. record_claim(env, args={author:"static-scanner", claim_id:"six-are-dead", framing:"independent-static-scan"})
16. ingest_return(env, args={"agent_id":"static-scanner"})   — I5′: live 1 → 0
17. corroborate(env, args={"action":"delete-six-helpers", "claims":[...]})
      → ToolResult(ok=True, value=CorroborateExit(six-are-dead SOURCES 2/2))
18. prove(env, args={}) → ToolResult(ok=True, value=ProveExit(PASS)); exit_type="PASS"
19. guard(env, args={"action":{"name":"commit-to-master",
    "refs":[{"path":"master","mode":"mutate","verb":"commit"}]}})
      → ToolResult(ok=True, value=GuardExit(GATED stakes=2, checkpoint))
      action_id = action_id("commit", ["master"])
20. ★ approval_recorded{gate="checkpoint", action_id="commit:['master']", approver="ej"}
21. commit(env, args={"message": "delete six dead helpers; drop orphaned Tuple import"})
      I1′: changed={loop/program_db.py}; last_commit_ts=None; covered = args["refs-paths"] from steps
           3 ∪ 19 = {loop/program_db.py, master} ⊇ changed → PASS
      I4′(b): loop/program_db.py → R7 (checkpoint, not owner) → PASS
      checkpoint precondition: approval from step 20 → PASS → ToolResult(ok=True, value={"hash":"..."})
22. done(env, args={})  — env.ctx = dataclasses.replace(ctx, ...), a Ctx (L1)
      (a) freshness: proves=[step 18]; staling — none (commit excluded) → PASS
      (b) clean tree: empty after step 21's landed commit → PASS
      → ToolResult(ok=True, value="DONE")
```

**22 steps**, identical to v1.3's own re-walk in count and outcome — only the `env.ctx` description
changed (L1). `live_dispatches` end = 0. Agents: 2, both returned.

---

## UC7 — debug loop: suite red → localize → fix → re-run, bounded

Unchanged from v1.3 in every step and outcome — `prove`/`done` (steps 14, 17) receive `dataclasses.
replace(ctx, ...)` (a `Ctx`, L1), the only wording change; no `env.ctx`-stripped-dict phrase appeared in
this walk to begin with in v1.3's own text, so nothing else here changes.

```
 1. gate(env, args={difficulty:"LOW", capability:[], tools_required:["python-repl","pytest"], stop_criterion:"suite-green"})
      → ToolResult(ok=True, value=GateExit(PLAN_NEEDED count=0))
      — v1.1: `capability` is C·3's agent count (`decision_tree` = len(capability)); the tools MAIN
        needs go in `tools_required`, else N=2 and execution_status=dispatched, not the N=0 shown
 2. run_suite(env, args={"command":"pytest tests/test_research_importable.py -q"})
      → ToolResult(ok=True, value={"passed":N-1,"failed":1,"output":"...ImportError: cannot import name
        '_WF_GRID' from 'research.sweep'..."})
 3. localize(env, args={"suite_output": "<step 2's output>"})
      → ToolResult(ok=True, value={"test_id":"tests/test_research_importable.py::test_research_module_
        imports[stability]", "file":"research/stability.py", "error_type":"ImportError"})
      — a second shell command, `grep -n _WF_GRID research/*.py`, names the fix (line 46 → research.walkforward)
 4. record_check(env, args={claim_id:"import-succeeds", mechanism:"pytest-fail-first",
    expected:"0 failed", observed:"1 failed", pre_fix_result:"FAIL"})
 5. *(native Edit — outside this registry, D6 — restores line 46)*
 6. guard(env, args={"action":{"name":"fix-stability-import",
    "refs":[{"path":"research/stability.py","mode":"mutate"}]}})
      → ToolResult(ok=True, value=GuardExit(NO_GATE stakes=1))
      action_id = action_id("mutate", ["research/stability.py"]); args["refs-paths"]=["research/stability.py"]
      — placed here, before the green re-run, matching J16's own corrected position
 7. run_suite(env, args={"command":"pytest tests/test_research_importable.py -q"})
      → ToolResult(ok=True, value={"passed":N,"failed":0,"output":"..."})
 8. record_check(env, args={claim_id:"import-succeeds", mechanism:"interpreter-import",
    expected:"exits 0, no ImportError", observed:"exit 0"})
 9. record_check(env, args={claim_id:"import-succeeds", mechanism:"pytest-fail-first",
    expected:"1 failed pre-fix, N passed post-fix", observed:"N passed", pre_fix_result:"FAIL"})
10. run_suite(env, args={"command":"make test"})
      → ToolResult(ok=True, value={"passed":274,"failed":0,"output":"274 passed"})
11. record_check(env, args={claim_id:"no-regression", mechanism:"suite-count", expected:274, observed:274})
12. guard(env, args={"action":{"name":"commit-to-master",
    "refs":[{"path":"master","mode":"mutate","verb":"commit"}],
    "tripwires":{"default-branch-history":"git diff --stat"}}})
      → ToolResult(ok=True, value=GuardExit(GATED stakes=2, checkpoint))
      action_id = action_id("commit", ["master"])
      — v1.1: the tripwire is required — `prove` rebuilds the plan from every guard, and the
        hub-touched-without-tripwire lint fails a hub entry with no tripwire named and run
12b. record_check(env, args={claim_id:"no-regression", mechanism:"git-diff-scope", command:"git diff --stat",
     expected:"exactly research/stability.py, no other files", observed:"1 file, matches"})
      — the tripwire run (AA3′: one event, two roles — also no-regression's second (c) source)
13. corroborate(env, args={"action":"commit-to-master", "claims":[import-succeeds, no-regression]})
      → ToolResult(ok=True, value=CorroborateExit(SOURCES 2/2, 2/2))
14. prove(env, args={})  — env.ctx = dataclasses.replace(ctx, ...), a Ctx (L1)
      → ToolResult(ok=True, value=ProveExit(PASS)); exit_type="PASS"
15. ★ approval_recorded{gate="checkpoint", action_id="commit:['master']", approver="ej"}
16. commit(env, args={"message":"fix research.stability import"})
      I1′: changed={research/stability.py}; covered = args["refs-paths"] from steps 6 ∪ 12
           ⊇ {research/stability.py} → PASS
      I4′(b): research/stability.py → R8 (stakes=1, gate=none) → PASS
      checkpoint precondition: approval from step 15 → PASS → ToolResult(ok=True, value={"hash":"..."})
17. done(env, args={})  — env.ctx = dataclasses.replace(ctx, ...), a Ctx (L1)
      (a) freshness: PASS (commit excluded from staling)
      (b) clean tree: empty after step 16 → PASS
      → ToolResult(ok=True, value="DONE")
```

**18 steps** (v1.1: +12b). Three `run_suite` calls (steps 2, 7, 10), well inside `ceiling`. This is
exactly what `tests/cases/hybrid/UC7.json` executes: a fixture git repo whose `research/stability.py`
imports `_WF_GRID` from the wrong module, real pytest runs (`(passed=1, failed=1)` → `(2, 0)` → `(2, 0)`),
real `localize` output, a real commit.
`live_dispatches` end = 0 trivially (zero dispatches).

---

## Compatibility notes — UC3, UC4, UC5, UC6, UC8, UC9 (unchanged outcomes, notation only)

No rewrite this round; unchanged from v1.3's own compatibility notes, with one blanket clarification
forced by L1: every `prove`/`done` call in these six sequences receives `dataclasses.replace(ctx,
n_sources=None, corroboration_capped=None, framing=None, siblings=None)` as `env.ctx` — a `Ctx`
instance, never a dict — wherever v1.3's own text said "stripped dict," read "`Ctx` with four fields
nulled" instead; no outcome, exit line, or `live_dispatches` value changes in any of the six.

- **UC3, UC4, UC5, UC6** each call `filter_candidates` — unrestricted (K3): real `ctx`, real `args`.
- **UC3, UC4, UC5, UC6, UC7** each call `prove` and `done`, genuinely executed (K8); clause (a) and (b)
  both pass in every one of them, unchanged reasoning from v1.3.
- **UC5 round 2 (v1.1, D-B):** after the fix, the second reviewer (framing `adversarial-review-2`) and
  MAIN's own command-backed claim are two distinct framings under (a); (b) no longer counts MAIN a second
  time (one author, one source). The round-2 line is `Corroborate: spec-accepted: n=2/2; reconciled=agree.`
  — under v1.0's rule it read `n=3/2`.
- **UC4's own `SINGLE_SOURCE` line (closing J15) is unaffected** by anything in v1.4 — `corroborate`
  itself has never been in any restricted set at any point across v1.1–v1.4.
- **UC8 (replay)** — unchanged: `mode="replay"` never calls `run()`/`choose_llm`/`check_invariants`;
  I1–I5 stay structurally inert for the whole walk.
- **UC9 (add a tool at runtime)** — `rebuild_index`'s manifest is unaffected; unchanged outcome.

`live_dispatches` end values, unchanged from v1.3: UC3 = 0, UC4 = 0, UC5 = 0, UC6 = 0, UC8 = 0 (n/a), UC9
= 0 (n/a) — computed the same way Adversarial A shows below, not tracked as separate state (L3).

---

## Adversarial case A — I5′'s boundary, re-walked for the computed `live_dispatches` formula (L3)

**v1.3's own walk showed a mutable `run_state["live_dispatches"]` incrementing/decrementing step by
step — that state no longer exists (`HYBRID_SPEC.md` §5, L3).** Every step below instead shows
`live_dispatches(events, run_id)` — §4's formula, `count(dispatch, non-refused) − count(ingest_return)
− count(dispatch_failed)`, recomputed fresh from the journal at every I5′ check — with the real
`dispatch.agent_id` format shown once (`f"{role}-{framing}-{uuid4().hex[:8]}"`, illustrative suffixes
below).

```
1. gate(env, args={count:1})
2. dispatch(env, args={"role":"x","framing":"a"})
     I5′ check (before executing, journal has 0 tool_call/dispatch, 0 ingest_return, 0 dispatch_failed):
          live_dispatches = 0 − 0 − 0 = 0 < 3 → PASS
     → ToolResult(ok=True, value="x-a-1a2b3c4d")
3. dispatch(env, args={"role":"x","framing":"b"})
     I5′ check (1 non-refused dispatch on record): live_dispatches = 1 − 0 − 0 = 1 < 3 → PASS
     → ToolResult(ok=True, value="x-b-5e6f7a8b")
4. dispatch(env, args={"role":"x","framing":"c"})
     I5′ check: live_dispatches = 2 − 0 − 0 = 2 < 3 → PASS → ToolResult(ok=True, value="x-c-9c0d1e2f")
5. dispatch(env, args={"role":"x","framing":"d"})
     I5′ check: live_dispatches = 3 − 0 − 0 = 3; 3 < 3 is False → **REFUSED** (loop-level, before
          execution) — I5, reason="live_dispatches=3, CAP=3, no slot"
6. ★ dispatch_failed{agent_id:"x-b-5e6f7a8b", reason:"agent B timed out"}
     — orchestrator-written (§6), NOT a `tool_call` event, not one of the 17 tools (L3) — `choose_llm`
       never selects this; the loop's own `for` body never sees `call.tool == "dispatch_failed"`,
       because there is no such call — this event simply exists in the journal from here on, for the
       NEXT `live_dispatches` computation to count
7. dispatch(env, args={"role":"x","framing":"d"})   — retried
     I5′ check: live_dispatches = 3 non-refused dispatch − 0 ingest_return − 1 dispatch_failed (step 6)
          = 2 < 3 → PASS → ToolResult(ok=True, value="x-d-3g4h5i6j")
8. ingest_return(env, args={"agent_id":"x-a-1a2b3c4d"})
     — I5′ is never checked on `ingest_return` itself (I5′ only gates `dispatch`); if `live_dispatches`
       were recomputed right now it would read 4 − 1 − 1 = 2
9. ingest_return(env, args={"agent_id":"x-c-9c0d1e2f"})
     — if recomputed now: 4 − 2 − 1 = 1
10. ingest_return(env, args={"agent_id":"x-d-3g4h5i6j"})
     — if recomputed now: 4 − 3 − 1 = 0
```

`live_dispatches` at the end of the run: `4` non-refused `dispatch` calls (steps 2, 3, 4, 7 — step 5 was
refused, `refused_by="I5"`, and the formula's own `non-refused` filter excludes it) `− 3` `ingest_return`
calls (steps 8–10) `− 1` `dispatch_failed` event (step 6) `= 0`. **Identical numeric outcome to v1.3's
own mutable-counter walk at every single step** — the fix removes the state, not the arithmetic (§12b,
Decision 34′). Demonstrates both of I5′'s decrement paths and the retry-is-first-class pattern.

---

## Adversarial case B — I4′(a)'s owner-gate boundary, extended for the freshness window (K4)

Unchanged from v1.3 — no step, outcome, or formula here depends on `env.ctx`'s shape (L1),
`hydrate`'s recursion (L2, this case's own `refs` are single-element, non-nested-list shapes that never
exposed L2 to begin with), or `dispatch_failed`'s registration status (L3, no dispatch calls occur in
this case).

```
B1 (refused, no approval):
1. gate(env, args={count:0})
2. guard(env, args={"action":{"name":"run-load_holdout-probe",
   "refs":[{"path":"eval.partitions.load_holdout","mode":"invoke"}]}})
     I4′(a) (loop pre-check): registry.lookup matches R3, gate="owner";
          action_id = action_id("invoke", ["eval.partitions.load_holdout"]);
          no approval_recorded{gate="owner", action_id=that} postdating last_commit_ts(None) exists
          → REFUSED, hard_blocked — guard's wrapped function never runs at all (no consumer_check, no
            exit event — matching Case 2's real shape: the probe is never attempted)

B2 (passes, after real clearance):
3. ★ approval_recorded{gate="owner", action_id="invoke:['eval.partitions.load_holdout']",
     approver="ej", note="owner clearance granted, see eval/protocol.json review"}
4. guard(env, args={same as step 2})   — retried
     I4′(a): same lookup; approval now exists, postdates last_commit_ts(None, still no commit this run)
          → PASS → guard's wrapped function runs normally
     → ToolResult(ok=True, value=GuardExit(GATED stakes=3, owner, hub=["eval.partitions.load_holdout"]))

B3 (demonstrates K4's freshness window, closing the reuse bypass):
5. *(elsewhere in this same run: an unrelated action lands via its own guard + approval + commit cycle,
   exactly like UC1's steps 2/3/11/12 — sets last_commit_ts = T1)*
6. guard(env, args={same probe action as step 2, invoked again later in the run})
     I4′(a): the approval from step 3 has ts < T1 (posted before the intervening commit) — it does
          **not** postdate last_commit_ts=T1 → **REFUSED again**, hard_blocked, reason="approval stale
          (predates last commit)" — the exact bypass K4 was constructed against
7. ★ approval_recorded{gate="owner", action_id="invoke:['eval.partitions.load_holdout']",
     approver="ej", note="re-cleared post-commit"}   — fresh, ts > T1
8. guard(env, args={same})   — retried
     I4′(a): fresh approval postdates T1 → PASS → GuardExit(GATED stakes=3, owner) again
```

**Open item, still unresolved (unchanged from v1.3 — not one of round 4's five, not touched):** the
parallel isolating demonstration for I4′(b) still needs the same clarification named in v1.3 — whether
I1′'s `covered` matching is exact-path or also prefix-based. **This is now answered by M3** (`HYBRID_
SPEC.md` §4: exact-path, stated explicitly) — building the I4′(b)-isolating case is now possible in
principle, but doing so was not in this round's scope and is left for a future round if MAIN wants it.

---

## Adversarial case C — I1′'s coverage window

Unchanged from v1.3 in every step; M3 (`HYBRID_SPEC.md` §4) now states in words what this case already
demonstrated in practice — `covered`/`uncovered` below are exact-path string sets throughout, never
prefix matches.

```
1. gate(env, args={count:0})
2. guard(env, args={"action":{"name":"edit-a","refs":[{"path":"a.py","mode":"mutate"}]}})
     → ToolResult(ok=True, value=GuardExit(NO_GATE stakes=1))
     args["refs-paths"] = ["a.py"]
3. guard(env, args={"action":{"name":"commit-to-master",
   "refs":[{"path":"master","mode":"mutate","verb":"commit"}]}})
     → ToolResult(ok=True, value=GuardExit(GATED checkpoint))
     args["refs-paths"] = ["master"]
4. ★ approval_recorded{gate="checkpoint", action_id="commit:['master']", approver="ej"}
5. commit(env, args={"message":"edit a.py"})
     I1′: changed={a.py}; last_commit_ts=None; covered = args["refs-paths"] from steps 2 ∪ 3
          = {"a.py","master"} ⊇ {a.py} → PASS → ToolResult(ok=True, value={"hash":"..."}), ts=T1
6. *(native edit — agent silently re-edits a.py a SECOND time, no new guard call)*
7. guard(env, args={"action":{"name":"commit-to-master",
   "refs":[{"path":"master","mode":"mutate","verb":"commit"}]}})
     → ToolResult(ok=True, value=GuardExit(GATED checkpoint))
     args["refs-paths"] = ["master"]   — a fresh commit-guard; its own refs still don't include a.py
8. ★ approval_recorded{gate="checkpoint", action_id="commit:['master']", approver="ej"}
9. commit(env, args={"message":"typo fix"})
     I1′: changed={a.py}; last_commit_ts=T1; window = guard tool_call events with ts > T1 =
          {step 7 only, args["refs-paths"]=["master"]} — step 2's earlier guard (ts < T1) is now OUT of
          the window → covered = {"master"} ⊉ {a.py} → uncovered={a.py} → **REFUSED**, reason=
          "unguarded changed files: {a.py}"
10. guard(env, args={"action":{"name":"edit-a-again","refs":[{"path":"a.py","mode":"mutate"}]}})
     → ToolResult(ok=True, value=GuardExit(NO_GATE stakes=1))   — fresh, ts > T1
11. commit(env, args={"message":"typo fix"})   — retried
     I1′: covered = {"master"} ∪ {"a.py"} (both now post-T1) ⊇ {a.py} → PASS → {"hash":"..."}, ts=T2
```

---

## Adversarial case D — I1′ over untracked files (v1.1, D-A)

```
1. gate(env, args={count:0})
   *(native edit creates research/new_module.py — untracked; and scratch.log — ignored by .gitignore)*
2. guard(env, args={"action":{"name":"commit-to-master","refs":[{"path":"master","mode":"mutate","verb":"commit"}],
   "tripwires":{...}}})   → GATED checkpoint; args["refs-paths"]=["master"]
3. ★ approval_recorded{gate="checkpoint", action_id="commit:['master']"}
4. commit(env, args={"message":"add research/new_module.py"})
     I1′: changed = ∅ (tracked diff) ∪ {research/new_module.py} (untracked, not ignored) — scratch.log is
          excluded by `--exclude-standard`; covered = {"master"} → uncovered = {research/new_module.py}
          → **REFUSED**, reason="unguarded changed files: ['research/new_module.py']"
5. guard(env, args={"action":{"name":"add-new-module","refs":[{"path":"research/new_module.py","mode":"mutate"}]}})
     → NO_GATE stakes=1; args["refs-paths"]=["research/new_module.py"]
6. commit(env, args={same})   — retried; the approval from step 3 is still in-window (no commit landed)
     I1′: covered = {"master","research/new_module.py"} ⊇ changed → PASS → git add -- research/new_module.py;
     git commit → {"hash": ...}; scratch.log is never staged
```

`tests/cases/hybrid/ADV_D.json`. Consequence worth knowing: pytest's `__pycache__/`/`.pytest_cache/`
are untracked files too — a repo that runs suites needs them in `.gitignore` or every commit is refused.

---

## Full case files — T2 and UC7

Unchanged from v1.3 — neither file's JSON shape depends on `env.ctx`'s type (L1, an implementation
detail the runner handles, invisible at the case-file level), `hydrate`'s recursion algorithm (L2, same
— the case file supplies plain JSON either way; T2's own `probe`/`refs` fields are exactly the nested
shapes UC1's step 1/2 above now show hydrating correctly), or `dispatch_failed`'s tool-vs-event status
(L3 — neither case file dispatches at all).

### T2 (`mode="scripted"`)

```json
{
  "case_id": "T2",
  "task": "fix research.stability import (ImportError: _WF_GRID)",
  "mode": "scripted",
  "ceiling": 44,
  "tool_calls": [
    {"tool": "gate", "args": {"name": "fix research.stability import",
      "stop_criterion": "import-succeeds-plus-smoke-test", "difficulty": "LOW", "capability": [],
      "probe": {"path": "research/stability.py", "mode": "read"}}},
    {"tool": "guard", "args": {"action": {"name": "research-and-tests-edit",
      "refs": [{"path": "research/stability.py", "mode": "mutate"},
               {"path": "tests/test_research_importable.py", "mode": "mutate"}]}}},
    {"tool": "guard", "args": {"action": {"name": "commit-to-master",
      "refs": [{"path": "master", "mode": "mutate", "verb": "commit"}],
      "tripwires": {"default-branch-history": "git diff --stat"}}}},
    {"tool": "record_check", "args": {"claim_id": "import-succeeds", "mechanism": "interpreter-import",
      "command": "python3 -c \"import research.stability\"", "expected": "exits 0, no ImportError", "observed": "exit 0"}},
    {"tool": "record_check", "args": {"claim_id": "import-succeeds", "mechanism": "pytest-fail-first",
      "command": "pytest tests/test_research_importable.py -q",
      "expected": "1 failed pre-fix, 14 passed post-fix", "observed": "14 passed", "pre_fix_result": "FAIL"}},
    {"tool": "record_check", "args": {"claim_id": "no-regression", "mechanism": "suite-count",
      "command": "make test", "expected": 274, "observed": 274}},
    {"tool": "record_check", "args": {"claim_id": "no-regression", "mechanism": "git-diff-scope",
      "command": "git diff --stat",
      "expected": "exactly research/stability.py + tests/test_research_importable.py, no other files",
      "observed": "2 files, matches"}},
    {"tool": "corroborate", "args": {"action": "commit-to-master",
      "claims": [{"claim_id": "import-succeeds", "kind": "executable"},
                 {"claim_id": "no-regression", "kind": "executable"}], "reconciliation": "agree"}},
    {"tool": "filter_candidates", "args": {"candidates": ["import fix", "docstring fix", "importability test", "Makefile change"],
      "cut": {"Makefile change": "tests/ already globbed"},
      "follow_on": [["extend importability pattern to eval/*.py and loop/*.py", "new-task"],
                    ["_scratch_pivot_dense_scan.py runs heavy work at import", "dismissed:out-of-scope"]]}},
    {"tool": "prove", "args": {"gate": "checkpoint"}},
    {"tool": "commit", "args": {"message": "fix research.stability import; add importability test"}},
    {"tool": "done", "args": {}}
  ],
  "injected_events": [
    {"after_step": 9, "event": {"event": "approval_recorded", "action_id": "commit:['master']",
      "gate": "checkpoint", "approver": "ej", "note": "checkpoint cleared"}}
  ],
  "expected_exit_lines": [
    "Gate: plan needed, N=0, execution_status=main_executes, stop=import-succeeds-plus-smoke-test.",
    "Guard: research-and-tests-edit stakes=1, no hub.",
    "Guard: commit-to-master stakes=2, hub=default-branch-history, gate=checkpoint.",
    "Corroborate: import-succeeds: n=2/2; no-regression: n=2/2; reconciled=agree.",
    "Filter: kept=3, merged=0, cut=1, follow_on=2.",
    "Prove: PASS, plan cleared to checkpoint gate."
  ],
  "expected_invariant_events": [
    {"invariant": "I1", "tool": "commit", "refused": false},
    {"invariant": "I4", "tool": "commit", "refused": false}
  ],
  "expected_final": {"agents": 0, "live_dispatches_end": 0, "prove_exit_type": "PASS",
    "tool_outcomes": [{"tool": "commit", "ok": true, "reason": null}, {"tool": "done", "ok": true, "reason": null}]}
}
```

### UC7 (`mode="scripted"`, the debug loop)

```json
{
  "case_id": "UC7-wf-grid",
  "task": "make research.stability importable again after a wrong-module import regresses",
  "mode": "scripted",
  "ceiling": 44,
  "tool_calls": [
    {"tool": "gate", "args": {"name": "fix research.stability import", "stop_criterion": "suite-green",
      "difficulty": "LOW", "capability": [], "tools_required": ["python-repl", "pytest"],
      "probe": {"path": "research/stability.py", "mode": "read"}}},
    {"tool": "run_suite", "args": {"command": "pytest tests/test_research_importable.py -q"}},
    {"tool": "localize", "args": {"suite_output": "<run_suite's stdout from the prior call>"}},
    {"tool": "record_check", "args": {"claim_id": "import-succeeds", "mechanism": "pytest-fail-first",
      "command": "pytest tests/test_research_importable.py -q", "expected": "0 failed", "observed": "1 failed",
      "pre_fix_result": "FAIL"}},
    {"tool": "guard", "args": {"action": {"name": "fix-stability-import",
      "refs": [{"path": "research/stability.py", "mode": "mutate"}]}}},
    {"tool": "run_suite", "args": {"command": "pytest tests/test_research_importable.py -q"}},
    {"tool": "record_check", "args": {"claim_id": "import-succeeds", "mechanism": "interpreter-import",
      "command": "python3 -c \"import research.stability\"", "expected": "exits 0, no ImportError", "observed": "exit 0"}},
    {"tool": "record_check", "args": {"claim_id": "import-succeeds", "mechanism": "pytest-fail-first",
      "command": "pytest tests/test_research_importable.py -q",
      "expected": "1 failed pre-fix, N passed post-fix", "observed": "N passed", "pre_fix_result": "FAIL"}},
    {"tool": "run_suite", "args": {"command": "make test"}},
    {"tool": "record_check", "args": {"claim_id": "no-regression", "mechanism": "suite-count",
      "command": "make test", "expected": 274, "observed": 274}},
    {"tool": "guard", "args": {"action": {"name": "commit-to-master",
      "refs": [{"path": "master", "mode": "mutate", "verb": "commit"}],
      "tripwires": {"default-branch-history": "git diff --stat"}}}},
    {"tool": "record_check", "args": {"claim_id": "no-regression", "mechanism": "git-diff-scope",
      "command": "git diff --stat", "expected": "exactly research/stability.py, no other files", "observed": "1 file, matches"}},
    {"tool": "corroborate", "args": {"action": "commit-to-master",
      "claims": [{"claim_id": "import-succeeds", "kind": "executable"},
                 {"claim_id": "no-regression", "kind": "executable"}], "reconciliation": "agree"}},
    {"tool": "prove", "args": {"gate": "checkpoint"}},
    {"tool": "commit", "args": {"message": "fix research.stability import"}},
    {"tool": "done", "args": {}}
  ],
  "injected_events": [
    {"after_step": 13, "event": {"event": "approval_recorded", "action_id": "commit:['master']",
      "gate": "checkpoint", "approver": "ej", "note": "checkpoint cleared"}}
  ],
  "expected_exit_lines": [
    "Gate: plan needed, N=0, execution_status=main_executes, stop=suite-green.",
    "Guard: fix-stability-import stakes=1, no hub.",
    "Guard: commit-to-master stakes=2, hub=default-branch-history, gate=checkpoint.",
    "Corroborate: import-succeeds: n=2/2; no-regression: n=2/2; reconciled=agree.",
    "Prove: PASS, plan cleared to checkpoint gate."
  ],
  "expected_invariant_events": [
    {"invariant": "I1", "tool": "commit", "refused": false}
  ],
  "expected_final": {"agents": 0, "live_dispatches_end": 0, "prove_exit_type": "PASS",
    "tool_outcomes": [{"tool": "commit", "ok": true, "reason": null}, {"tool": "done", "ok": true, "reason": null}]}
}
```
