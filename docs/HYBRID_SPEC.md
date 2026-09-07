# The hybrid tool layer — spec v1.4 (fix pass after `hybrid_review_4.md`, REJECT: 3 BLOCKING)

**This is the last documentary round; a coder starts implementation in parallel from v1.3 +
`DECISIONS_HYBRID_4.md`, per MAIN's own instruction.** v1.3 was rejected on three findings, each
confirmed by executing the spec's own literal text, not by argument: **L1** — the stripped `env.ctx`
v1.3 gave `prove`/`done` was a plain `dict`, but `stages.prove` calls `ctx.keys_set()` on both exit
paths (`stages.py:671,673`), a `Ctx`-only method; every `prove` call in every UC that reaches it
returned `ToolResult(ok=False, reason="internal-error: 'dict' object has no attribute 'keys_set'")`.
**L2** — `hydrate(cls, d)` was named, called once in the `guard` worked example, and never given an
algorithm; the naive, only-stated-consistent reading (`cls(**d)`) does not recurse into nested
dataclass fields, so `gate`'s own `TaskInput.probe: ArtifactRef` and `guard`'s own `ActionInput.refs:
list[ArtifactRef]` — reproduced by execution against literally T2's own step-1 case-file JSON — crash
with `AttributeError` on their first nested field. **L3** — `dispatch_failed` sat in the 18-tool table
with `cost: "—"`, failing R1's own `cost ∈ {cheap, agent, suite}` enum that discovery is stated to
enforce for every tool, while §6 simultaneously described it as orchestrator-written and
not-agent-invocable, exactly like `approval_recorded` (which is explicitly *not* one of the 18); the
loop's own shown decrement branch for it was dead code, since nothing shows `call.tool` ever holding
that value. **M3** (SHOULD-FIX, adopted) states, in words, a fact I1′'s own formula already computed
correctly but never said out loud: coverage matching is exact-path string equality, not a directory
prefix. `dispatch.agent_id`'s generation formula, previously unspecified (SHOULD-FIX, item 9), is
stated. Applying exactly these five, no other changes; `docs/HYBRID_SEQUENCES.md` re-walks Adversarial
A (the `live_dispatches` computation) and UC1's `gate` step (`hydrate`'s recursion) in full; every other
sequence keeps its v1.3 shape with only the mechanical wording swaps these five decisions force.

---

## 1. Overview

A main agent (an LLM) drives a loop: observe, choose a tool, have the loop pre-check three invariants
(I1, I4, I5) before executing, execute, journal, repeat until `done` — itself a real, executed tool —
reports success. The registry is populated once at run start from a directory of tool modules, each a
plain function plus a `MANIFEST` dict (R1). **18 tools now share one entrypoint shape** (§2) — the §3
table's 19 rows minus `dispatch_failed`, which is a journal event, not a tool (L3, §3; v1.1 corrects the
v1.4 count of "17" to match the code, `ancient_games/hybrid/tools/`) — this is the single biggest structural change in v1.3 and remains so
in v1.4: there is no longer a positional-argument calling convention for `ctx`/`journal` to collide with
`call.args` inside. Five stage functions become five tools, wrapped not rewritten (R7); most of the
rest wrap one existing function directly; `commit`, `run_suite`, `localize`, `rebuild_index` are
genuinely new; `dispatch`/`prove`/`done` still do real reconstruction work beyond a thin call, inside
each adapter's own `run(env, args)` body. **Five invariants, same ids, same ceiling, enforcement point
unchanged from v1.3:** I1 (commit's file-coverage), I4 (owner-gate/undeclared-mutation), I5 (dispatch
cap) remain loop-level pre-execution checks. I2 lives entirely inside `done`'s own tool body. I3 is
fully static (a discovery-time signature check plus the loop's choice of `env.ctx`) — and, as of v1.4,
that choice is **a real `Ctx` instance with four fields nulled out** (`dataclasses.replace`, L1), not a
`dict` — the difference that made `prove` crash under v1.3's literal text.

---

## 2. Tool manifest format

**Fields, unchanged (R1's six plus `entrypoint`):** `name`, `inputs`, `outputs`, `side_effects`,
`cost`, `participates_in`, `entrypoint`.

**The uniform calling convention (unchanged from v1.3):**

```python
@dataclass(frozen=True)
class ToolEnv:
    run_id: str
    journal_path: str
    ctx: Ctx          # ALWAYS a real Ctx instance (L1, v1.4) — the loop's own object, same reference,
                        # mutations visible to the caller, for every ordinary tool; for `prove`/`done`
                        # specifically, `dataclasses.replace(ctx, n_sources=None, corroboration_capped=
                        # None, framing=None, siblings=None)` — still a Ctx, so `stages.prove`'s own
                        # `ctx.keys_set()` call (stages.py:671,673) works; the four corroboration fields
                        # read back as `None`, so an accidental read fails loudly (AttributeError-shaped
                        # misuse of a None, or an obvious falsy check) instead of silently returning a
                        # count — I3′'s guarantee is unchanged: counts come only from `corroborate`'s
                        # journaled result, never from `ctx`, whether `ctx` is stripped-as-dict (v1.3,
                        # broken) or nulled-as-Ctx (v1.4, fixed)

@dataclass(frozen=True)
class ToolResult:
    ok: bool
    value: "Any"            # the real return object (GuardExit, ProveExit, an agent_id str, ...) when ok
    reason: "str | None"    # populated on any decline, ok=True or ok=False

# every entrypoint, no exceptions:
def run(env: ToolEnv, args: dict) -> ToolResult: ...
```

Every tool constructs its own `Journal(env.journal_path, env.run_id)` — never receives a live `Journal`
object — and reads/mutates `env.ctx` in place (it is always a `Ctx`, v1.4). `args` carries whatever the
tool needs, plain-JSON-shaped. **Tools never raise across this boundary:** every adapter's own body is
wrapped in `try/except`, converting any internal exception into `ToolResult(ok=False, reason=
f"internal-error: {e}")`.

**Discovery, updated:**

1. **Malformed-manifest rejection — unchanged** (required fields, enum membership).
2. **I3′'s static half, universal, not tool-specific.** At discovery, the loader calls
   `inspect.signature` on **every** bound `entrypoint` and requires it to equal exactly `(env, args)` —
   no `*args`/`**kwargs`, no defaults. A manifest whose entrypoint doesn't match this never registers,
   for any of the 18 tools, not just `prove`/`done`. I3′'s own remaining content: the loop passes a
   `Ctx` with four fields nulled (above, L1) as `env.ctx` for `prove`/`done` specifically (§4).
3. **JSON→dataclass hydration, now with a stated algorithm (closes L2 — the naive `cls(**d)` reading
   never worked; this is the actual recursion):**

```python
def hydrate(cls, d):
    if d is None:
        return None
    hints = typing.get_type_hints(cls)          # {"refs": list[ArtifactRef], "name": str, ...}
    fields = {f.name: f for f in dataclasses.fields(cls)}
    kwargs = {}
    for key, value in d.items():
        if key not in fields:
            raise ValueError(f"{cls.__name__}: unknown key {key!r}")
        hint = hints[key]
        origin, targs = typing.get_origin(hint), typing.get_args(hint)
        if dataclasses.is_dataclass(hint) and isinstance(value, dict):
            kwargs[key] = hydrate(hint, value)                              # nested dataclass → recurse
        elif origin is list and targs and dataclasses.is_dataclass(targs[0]) and isinstance(value, list):
            kwargs[key] = [hydrate(targs[0], item) for item in value]       # list[dataclass] → per element
        else:
            kwargs[key] = value                                            # scalar/plain → assign as-is
    return cls(**kwargs)   # missing keys use the dataclass's own field default, unchanged Python behavior
```

~20 lines, stdlib only (`dataclasses`, `typing`). A fixed lookup table (`{"ActionInput": ActionInput,
"ArtifactRef": ArtifactRef, "Claim": Claim, "TaskInput": TaskInput, ...}`) names which dataclass each
manifest `inputs` entry expects; every adapter imports `hydrate` and calls it on its own `args` entries
before touching the wrapped stage function — this is what makes `gate`'s `TaskInput.probe:
ArtifactRef|None` and `guard`'s `ActionInput.refs: list[ArtifactRef]` actually construct real objects
instead of leaving nested dicts for `stages.py`'s own code to crash on (`HYBRID_SEQUENCES.md`'s UC1
walk shows this concretely against T2's own `gate` call, §8).

**`action_id`, unchanged from v1.3:**

```
action_id(verb: str, refs: list[str]) -> str:
    return f"{verb}:{sorted(refs)}"
```

`guard` computes this from its own action's `(verb, ref_paths)`; `commit` computes the same formula on
its own fixed target (`verb="commit"`, `refs=["master"]`) — no caller-supplied `action_id` parameter.

**`dispatch.agent_id`, stated (new, closes item 9's SHOULD-FIX — no other rewrite):**

```
agent_id = f"{role}-{framing}-{uuid4().hex[:8]}"
```

Generated inside `dispatch`'s own adapter body (§3), never supplied by the caller — the design space
was small and uncontroversial (any unique string works, nothing downstream parses the format); this is
the one MAIN picked, stated once here and reused wherever `dispatch`'s signature is shown (§3).

**Full example — `guard` (unchanged from v1.3; now correctly executes, since `hydrate` recurses per
above — `action.refs` is a real `list[ArtifactRef]`, not a list of dicts):**

```python
# ancient_games/tools/guard.py
from ancient_games.stages import guard as _guard, ActionInput
from ancient_games.journal import Journal
from ._hydrate import hydrate
from ._action_id import action_id

MANIFEST = {
    "name": "guard", "inputs": {"action": "ActionInput"}, "outputs": "GuardExit",
    "side_effects": "read", "cost": "cheap", "participates_in": ["I1", "I4"], "entrypoint": "run",
}

def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        action = hydrate(ActionInput, args["action"])         # action.refs is now list[ArtifactRef]
        result = _guard(env.ctx, action, journal)
        aid = action_id(action.refs[0].verb or action.refs[0].mode, [r.path for r in action.refs])
        return ToolResult(ok=True, value=result, reason=None)   # aid is journaled by the loop (§6)
    except Exception as e:
        return ToolResult(ok=False, value=None, reason=f"internal-error: {e}")
```

**Full example — `done` (unchanged from v1.3 — it never touches `env.ctx` at all, so L1 never affected
it; only `prove`'s own call site did):**

```python
# ancient_games/tools/done.py
from ancient_games.journal import Journal
from ._git import diff_name_only_head

MANIFEST = {
    "name": "done", "inputs": {}, "outputs": "ToolResult(ok, reason)", "side_effects": "none",
    "cost": "cheap", "participates_in": ["I2", "I3"], "entrypoint": "run",
}

def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        events = [e for e in journal.read() if e["run_id"] == env.run_id]
        proves = [e for e in events if e["tool"] == "prove" and e.get("exit_type") == "PASS"
                  and e["refused_by"] is None]
        if not proves:
            return ToolResult(ok=False, value=None, reason="no-prove-pass")
        latest = max(e["ts"] for e in proves)
        staling = [e for e in events if TOOLS[e["tool"]].manifest["side_effects"] == "mutate"
                   and e["refused_by"] is None and e["ts"] > latest]
        if staling:
            return ToolResult(ok=False, value=None, reason=f"prove-stale: {staling[-1]['tool']}")
        changed = diff_name_only_head()
        if changed:
            return ToolResult(ok=False, value=None, reason=f"uncommitted-changes: {changed}")
        return ToolResult(ok=True, value="DONE", reason=None)
    except Exception as e:
        return ToolResult(ok=False, value=None, reason=f"internal-error: {e}")
```

---

## 3. The tool set

**18 tools** (v1.1: the count as implemented — `dispatch_failed` is not one of them, L3; it is a journal
event, written by the orchestrator, exactly like `approval_recorded`; neither is registered, neither has
a `MANIFEST`, neither can be `choose_llm`'s selection). Every `fn` is `(env, args) -> ToolResult`. Each
tool is one module `ancient_games/hybrid/tools/<name>.py` with `MANIFEST` + `run`: `gate`, `guard`,
`corroborate`, `filter_candidates`, `prove`, `dispatch`, `ingest_return`, `record_claim`, `record_check`,
`lookup_registry`, `run_lint`, `render_trace`, `read_journal`, `commit`, `run_suite`, `localize`,
`rebuild_index`, `done` (18); shared plumbing lives in `_shared.py` (action_id, git, journal windows,
`tool_call_event`) and `_plan.py` (journal → `Plan` reconstruction for `prove`/`run_lint`).

| tool | wraps (file:line) or NEW | `side_effects` | `cost` | `participates_in` | read by |
|---|---|---|---|---|---|
| `gate` | `stages.gate` (stages.py:71) | none | cheap | — | UC1–UC7 |
| `guard` | `stages.guard` (stages.py:181) | read | cheap | I1, I4 | UC1,2,3,5,6,7 |
| `corroborate` | `stages.corroborate` (stages.py:406) | read | cheap | I3 (producer, ordinary signature) | UC1,2,3,4,5,6 |
| `filter_candidates` | `stages.filter_candidates` (stages.py:539) | read | cheap | — (not I3-restricted, K3) | UC1,2,3,4,5,6 |
| `prove` | `stages.prove` (stages.py:641) | read | cheap | I2 (producer), I3 (consumer — `env.ctx` is a `Ctx` with 4 fields nulled, §2, L1) | UC1,2,3,5,6,7 |
| `dispatch` | `journal.dispatch`/`stages.dispatch_source`; generates its own `agent_id` (§2 formula) | invoke | agent | I5 | UC2,3,4,5,6,7,9 |
| `ingest_return` | `journal.ingest_return` (journal.py:218) | none | cheap | I5 | UC2,3,4,5,6 |
| `record_claim` | `journal.claim_recorded` (journal.py:208) | none | cheap | — | UC2,3,4,5,6,7 |
| `record_check` | `journal.check_executed` (journal.py:202) | none | cheap | — | UC1,2,3,5,6,7 |
| `lookup_registry` | `registry.lookup` (registry.py:159) | read | cheap | — | UC1, UC9 |
| `run_lint` | `lints.run_all_on_plan` + nine `lint_*` | read | cheap | — | UC7,8,9 |
| `render_trace` | `trace.render_trace` (trace.py:70) | none | cheap | — | UC8 |
| `read_journal` | `journal.read` (journal.py:189) | read | cheap | — | every UC's observe step |
| `commit` | NEW — full signature below | commit | cheap | I1, I4 | UC1,2,5,6,7 |
| `run_suite` | NEW — `{command: str} -> {passed, failed, output}` | none | suite | — | UC6,7 |
| `localize` | NEW — regex over `run_suite` output → `{test_id, file, line, error_type}` | none | cheap | — | UC7 |
| `rebuild_index` | NEW — wraps `rebuild(journal_path, db_path)`, decided-not-yet-built | mutate | cheap | — | UC9 |
| `done` | NEW — real, executed tool (§2's full example); runs I2's two clauses | none | cheap | I2, I3 (consumer — `env.ctx` is a `Ctx` with 4 fields nulled) | UC1,2,3,5,6,7,8 |

**Two more journal events, written by the orchestrator, outside this table entirely — never registered,
never `choose_llm`-selectable:** `approval_recorded` (unchanged from v1.3) and **`dispatch_failed`**
(reclassified in v1.4, was row 8 of v1.3's 18-row table). §6 states both shapes and writers; §4's I5′
formula reads `dispatch_failed` events directly from the journal (below), with no manifest, no
`side_effects`/`cost` enum to violate — closing L3's own contradiction by removing its premise (it was
never truly one of "the tools" that R1's enum constraint governs).

**`commit`, in full — unchanged from v1.3:**

```
commit(message: str) -> ToolResult(ok, value={"hash": str}|None, reason: str|None)
```
Runs `git diff --name-only HEAD` (I1′'s `changed`). Checks I1′ and I4′(b) loop-level, before `commit`'s
own body runs at all. If both pass, computes `action_id = action_id("commit", ["master"])` and checks
its checkpoint precondition: an `approval_recorded{gate="checkpoint", action_id=<that value>}` event
postdating the last executed commit must exist; absent ⇒ `ToolResult(ok=False, reason=
"checkpoint-not-cleared")`, `git commit` never runs. Only then `git commit -m <message>`; non-zero exit
⇒ `ToolResult(ok=False, reason=<git's own stderr>)`, never raises.

**`dispatch`, in full (updated — `agent_id` generation stated, §2):**
```
dispatch(env, args={"role": str, "framing": str, "payload": dict|None, "counts_toward_cap": bool=True})
    -> ToolResult(ok=True, value=agent_id: str)     # agent_id = f"{role}-{framing}-{uuid4().hex[:8]}"
```

---

## 4. Invariants I1–I5

**Loop-level pre-execution invariants remain exactly three — I1, I4, I5 — checked before a tool
executes. I2 lives inside `done`'s own body; I3 is fully static. Unchanged from v1.3.**

```
I1′  scope match at commit — reads real data (unchanged formula from v1.3, K2):
     checked only when tool == "commit"
     changed  = git diff --name-only HEAD  ∪  git ls-files --others --exclude-standard
                # v1.1 (D-A): untracked files not ignored by .gitignore are in `changed` too — a brand-new
                # file needs its own guard exactly like a modified one (Adversarial D, §8)
     last_commit_ts = ts of the most recent tool_call(tool="commit", refused_by=None) event this run,
                       or None if this is the first commit
     covered  = ∪ { path for path in g.args["refs-paths"] : g ∈ events, g.tool=="guard",
                    g.refused_by is None, (last_commit_ts is None or g.ts > last_commit_ts) }
     uncovered = changed − covered
     pass iff uncovered == ∅; else refuse(I1, reason="unguarded changed files", files=uncovered)
     I1′ coverage matching is EXACT PATH (new, closes M3 — MAIN's sentence, verbatim): a guard's
     `refs-paths` are concrete file paths and match `changed` entries (tracked diff ∪ untracked) by string
     equality; directory patterns are the registry's business inside `guard` (`registry.py`'s own
     `_matches_key` dir-kind prefix logic), never coverage's — I1′ never calls `registry.lookup` at all.
     → still: every commit-ending UC needs its own dedicated guard(..., verb="commit") call, and I1′'s
       own math does not itself enforce that (J7/J16's disposition stands)

I2   done's own two clauses (unchanged from v1.3, executed inside `done`'s adapter body, never in
     `check_invariants`):
     (a) freshness: the latest non-refused `prove` PASS postdates every non-refused `mutate`-side-effect
         tool_call — `commit` is categorically never in this set (side_effects=="commit", not "mutate")
     (b) clean tree: `changed` (I1′'s own set — tracked diff ∪ untracked not-ignored files, v1.1 D-A)
         must be empty; non-empty ⇒ decline with reason="uncommitted-changes", naming the files
     → (a) alone can only ever be tripped by `rebuild_index` — the sole `side_effects=="mutate"` tool
       among 18 (`dispatch_failed` is not a tool, L3) — since every real native file edit is off-registry (D6); (b) is what actually
       catches an uncommitted native edit

I3   fully static:
     static (loader, §2): every entrypoint's signature is `(env, args)`, uniformly
     runtime (loop, §5): for `prove` and `done` **only**, the loop passes
         `dataclasses.replace(ctx, n_sources=None, corroboration_capped=None, framing=None,
         siblings=None)` as `env.ctx` — **a `Ctx` instance, not a `dict` (L1, v1.4's own fix)** — the
         four corroboration fields read back `None`; any accidental read fails loudly rather than
         silently succeeding, and `stages.prove`'s own `ctx.keys_set()` call (stages.py:671,673) works
         normally, since a `Ctx` is still a `Ctx`
     tool-internal: `prove` re-derives n_available per claim from the journal, never from `ctx`;
         `corroborate` keeps ordinary, unrestricted access — it is I3's sole producer; `prove`'s
         claim list is the run's *recorded* claims, and a recorded claim with no corroborate result
         is a RETURN_TO_PLANNER finding (H8, below) — the count must exist before prove can read it
     trust boundary (§11): nothing in the loader validates that a differently-named tool computing a
         corroboration-shaped number must adopt this pattern — an [LLM] judgment call at tool-add time

I4′  reads approval_recorded, windowed (v1.2 states the read exemption; the formula is otherwise v1.3's):
     (a) at guard, over the declared refs with mode ∈ {invoke, mutate} ONLY — a ref with mode=read is
         never looked up (S2: reads are never gated; H1, ABLATION_1): refuse (hard_blocked) iff those
         refs match a gate=="owner" row AND no approval_recorded{gate="owner", action_id=<computed>}
         event postdating the last executed commit exists. A consumer declared on an invoke/mutate ref
         counts as a match (D2′ hub union) — declaring an owner-gated file as a consumer owner-gates the
         action; the refusal reason names each owner row and whether it matched direct or via consumer.
     (b) at commit: for every f in I1′'s own `changed` set: row = registry.lookup([f, mutate]); if
         row.gate=="owner": refuse iff no approval_recorded{gate="owner", action_id=row.id} postdating
         the last executed commit exists
     → one approval clears one landing; J3 (SHOULD-FIX, unchanged, still stated not closed): (b) only
       ever sees direct registry matches, never a `.consumers`-declared hub

I5′  live, now computed at check-time, no stored counter (unchanged formula shape from v1.3; L3 removes
     the loop's own mutable `run_state` and its dead `dispatch_failed` decrement branch — nothing else
     about I5′'s meaning changes):
     def live_dispatches(events, run_id):
         d = count(e in events: e.event=="tool_call", e.tool=="dispatch", e.run_id==run_id,
                    e.refused_by is None)
         r = count(e in events: e.event=="tool_call", e.tool=="ingest_return", e.run_id==run_id)
         f = count(e in events: e.event=="dispatch_failed", e.run_id==run_id)
         return d - r - f
     dispatch: pass iff live_dispatches(journal.read(), run_id) < 3, checked fresh every time — no
         `+= 1`/`-= 1` anywhere; the count IS the journal, read on demand
     ctx.dispatch_count (cumulative, frozen spine) remains untouched by I5′
```

**Loop-level refusal priority, unchanged from v1.3:** `I4 > I1 > I5`. `check_invariants` takes `TOOLS`/
`registry`; it no longer takes a `run_state` parameter at all (L3 — there is no mutable state left for
it to read).

**Ceiling: five, unchanged.** I4′(a)'s alias-declaration trust boundary and I3's differently-named-tool
trust boundary remain open, both documented in §11, neither closed by a sixth invariant.

**D·4 tripwires (H5, ABLATION_1).** `prove` accepts a hub's tripwire as run only when a `check_executed`
event's `command` string-matches the command `guard` declared for that hub, exactly. So declare the
tripwire in the form it will be run at prove time: a scope check declared pre-commit as
`git diff --stat HEAD` is wrong once the commit has landed (the tree is clean); the post-commit form
is `git diff --stat HEAD~1 HEAD`. `guard` may be re-called to correct a mis-declared tripwire — the
later non-refused guard's declaration is the one the journal-rebuilt plan carries. A tripwire may be
keyed by the hub element's name or by the path of a ref that matched into it (H6).

**Claim coverage (H8, ABLATION_1; harness v1.3).** The plan `prove` evaluates is built from this run's
recorded claims, not from whatever `corroborate` happened to be called on: `recorded = ` every
`claim_recorded` or `check_executed` claim_id with `run_id == env.run_id`, deduped in first-seen
order (a claim with a stated expected value is journaled as a check, Z2′ — still a recorded claim);
`hub-integrity:<hub>` is a D·4 tripwire run (AA3′), never a claim. For each recorded claim with no
executed `corroborate` tool_call naming it in `args.claims` → finding
`RETURN_TO_PLANNER: run corroborate for <claim_id>`; a run with `recorded == []` → finding
`RETURN_TO_PLANNER: no claims recorded`. The findings are carried on the plan (`Plan.findings`,
`tools/_plan.claim_coverage_findings`) and `stages.prove` reports them first, in its ordinary
`Prove: FAIL, N=…` line with the A exit journaled as usual; only claims with a corroborate result are
scored, and a capped one routes exactly as before. `prove` still never counts — it only checks that
`corroborate`'s journaled result exists for every claim — so an empty plan can no longer PASS (UC2
attempt 2's journal, replayed, now returns
`Prove: FAIL, N=1 finding (RETURN_TO_PLANNER: run corroborate for C1), returned to planner.`).

---

## 5. Main-agent loop

```
def run(task, TOOLS, choose_llm, case, registry):
    ctx = Ctx()
    journal = Journal(case.journal_path, case.run_id)
    default_plan = ["gate", "guard", "corroborate", "filter_candidates", "prove"]
    RESTRICTED = {"prove", "done"}                                        # I3
    for i in range(case.ceiling):
        events = journal.read()
        obs = {"ctx": ctx.as_dict(), "events": events, "suggested_next": default_plan}
        call = choose_llm(obs, TOOLS)
        refusals = check_invariants(call, ctx, journal.read(), TOOLS, registry)  # I1, I4, I5 only —
                                                                                    # I5′ computed fresh
                                                                                    # from the journal
                                                                                    # inside this call (§4);
                                                                                    # no run_state anywhere
        if refusals:
            refused_by = pick_by_priority(refusals)                        # I4 > I1 > I5
            journal.append(tool_call_event(call, refused_by=refused_by, reason=refusal_reason(refused_by)))
            continue
        ctx_for_call = (dataclasses.replace(ctx, n_sources=None, corroboration_capped=None,
                        framing=None, siblings=None) if call.tool in RESTRICTED else ctx)   # L1: a Ctx,
                                                                                               # never a dict
        env = ToolEnv(run_id=journal.run_id, journal_path=journal.path, ctx=ctx_for_call)
        result = TOOLS[call.tool].fn(env, call.args)                       # uniform, closes K1
        journal.append(tool_call_event(call, result))                      # refused_by=None here;
                                                                              # result.ok/.reason captured
        if call.tool == "done" and result.ok:
            return ctx, "DONE"
        if call.tool == "prove" and getattr(result.value, "exit_type", None) == "RETURN_TO_PLANNER":
            default_plan = ["corroborate", "filter_candidates", "prove"]
        elif default_plan and call.tool == default_plan[0]:
            default_plan.pop(0)
    return ctx, "CEILING_REACHED"
```

**Removed from v1.3, deliberately, per L3:** `run_state = {"live_dispatches": 0}` and both of its
`+= 1`/`-= 1` branches. `dispatch_failed` is never a value `call.tool` can hold (it is orchestrator-
written, out-of-band, §6) — v1.3's own decrement branch for it was dead code the loop's own `for` body
could never reach; v1.4 doesn't patch that branch, it deletes it, because I5′ no longer needs any
mutable state to consult at all (§4's `live_dispatches(events, run_id)` reads the journal directly,
every time). `ctx.stop_criterion` remains advisory-only; `ceiling` the loop's one mechanical bound.
`choose_llm` in `mode="scripted"` — unchanged: a closure popping `case.tool_calls`, ignoring `obs`.

---

## 6. Journal

**Three event shapes, literal `SHAPES`/`_ENUMS` dict entries, unchanged from v1.3:**

```python
SHAPES["tool_call"] = {
    "tool": str, "action_id": (str, type(None)), "args": dict, "args_hash": str,
    "result_summary": str, "exit_type": (str, type(None)),
    "invariants_checked": list, "refused_by": (str, type(None)), "reason": (str, type(None)),
}
SHAPES["approval_recorded"] = {"action_id": str, "gate": str, "approver": str, "note": str}
SHAPES["dispatch_failed"] = {"agent_id": str, "reason": str}

_ENUMS[("tool_call", "refused_by")] = ("I1", "I4", "I5", None)     # I2/I3 never populate this
_ENUMS[("approval_recorded", "gate")] = ("checkpoint", "owner")
```

`dispatch_failed` has a `SHAPES` entry (it is a real, typed, validated journal event) but **no
`MANIFEST`** — the two are different registries (event shapes vs. tool discovery, §2/§3) and v1.3
conflated them by also giving `dispatch_failed` a table row with tool-shaped fields (`side_effects`,
`cost`) it could never legitimately carry (L3). v1.4 states this distinction once, here: an event can
be journaled without being a tool; `approval_recorded` already worked this way cleanly in every prior
round, `dispatch_failed` now matches it.

**`args`, `exit_type`, `action_id`'s dual convention, `args_hash` — all unchanged from v1.3.**

**`dispatch_failed`'s writer and trigger — unchanged from v1.3:** the orchestrator — in a live run, the
loop itself, on receiving a failed or timed-out dispatch-task notification (in a Claude Code session:
MAIN, on that notification). Not agent-invocable. **Its effect on I5′ (updated, L3):** no code path
"decrements a counter" — `live_dispatches` is recomputed from the journal every time §4's formula runs,
and a `dispatch_failed` event simply subtracts one from that computation the next time anyone asks,
automatically, with no separate wiring needed in the loop, the orchestrator's handler, or the case-file
runner's `injected_events` processor. This closes the exact gap the reviewer traced in checklist item
10 ("the mechanism by which `live_dispatches` reaches 0... is unspecified") — there is no mechanism to
specify beyond "the formula reads the journal," which is already fully stated in §4.

**`approval_recorded`'s writer — unchanged from v1.3:** the orchestrator, directly, outside all 17
tools; no tool in §3 can write it.

**`args_hash` — unchanged**, dedup only.

---

## 7. Case file format

Unchanged from v1.3 in shape. One clarifying note, forced by L3: `expected_final.live_dispatches_end`
is asserted using the exact same formula §4 states (`live_dispatches(events, run_id)`) — the runner
does not maintain any separate tracking for this either; it is one journal read, same as the checker's
own I5′ evaluation.

```json
{
  "case_id": "string", "task": "one-line description", "mode": "scripted | replay",
  "ceiling": "int, required", "journal_path": "absolute path, required when mode=replay",
  "tool_calls": [{"tool": "gate", "args": {"...": "literal JSON, hydrated by each adapter, §2"}}],
  "injected_events": [
    {"after_step": 9, "event": {"event": "approval_recorded", "action_id": "commit:['master']",
                                 "gate": "checkpoint", "approver": "ej", "note": "checkpoint cleared"}}
  ],
  "expected_exit_lines": ["bare canonical §4 lines"],
  "expected_invariant_events": [{"invariant": "I1", "tool": "commit", "refused": false}],
  "expected_final": {"agents": 0, "live_dispatches_end": 0, "prove_exit_type": "PASS",
                      "tool_outcomes": [{"tool": "done", "ok": true, "reason": null}]}
}
```

`after_step` is 0-indexed into `tool_calls`; the runner injects the event immediately after executing
that step and before choosing the next.

---

## 9. Ablation harness

Unchanged from v1.3.

---

## 10. Extensibility

Unchanged from v1.3, except the tool count in its own prose (17, not 18) — adding a tool means writing
it against `(env, args) -> ToolResult` (§2); the loader's uniform `inspect.signature` gate catches a
malformed one at discovery.

---

## 11. Out of scope

Unchanged from v1.3: new store features · the graph layer · a UI · tool sandboxing beyond
`side_effects` · LLM API integration inside the tool layer · multi-orchestrator coordination ·
long-running autonomous loops without a human gate. Trust boundaries (I4′(a)'s alias gap, I4′(b)'s
consumer-match blind spot, I3's differently-named-tool gap) unchanged from v1.3.

---

## 12. Decisions

### 12a. Closing `hybrid_review_4.md` (L1–L3, M3, `dispatch.agent_id`)

| finding | severity | disposition |
|---|---|---|
| L1 | BLOCKING | **Applied, MAIN's text.** `ctx_view = dataclasses.replace(ctx, n_sources=None, corroboration_capped=None, framing=None, siblings=None)` — a `Ctx`, not a `dict`; `stages.prove`'s `ctx.keys_set()` call now works (§2, §4, §5). Verified (Rule 9): `stages.prove`'s own body never reads `ctx.n_sources`/`corroboration_capped`/`framing`/`siblings` directly at any point — it reads `plan.entries[].claims[].capped`, built from the journal by `prove`'s own adapter (§2's discovery item 3 discussion, unchanged from v1.3) — so nulling these four fields cannot leak a stale value into anything `stages.prove` actually consults. |
| L2 | BLOCKING | **Applied, MAIN's algorithm.** `hydrate(cls, d)` stated in full in §2 — dataclass fields recurse, `list[dataclass]` fields recurse per element, everything else assigns as-is; unknown keys raise. |
| L3 | BLOCKING | **Applied, MAIN's ruling.** `dispatch_failed` removed from the tool table — 18 tools remain (§1, §3; v1.4 miscounted 17, corrected in v1.1). `live_dispatches` is computed at every I5′ check from the journal (`count(dispatch, non-refused) − count(ingest_return) − count(dispatch_failed)`), not tracked as loop-local state; the loop's own dead decrement branch is deleted, not patched (§4, §5). |
| M3 | SHOULD-FIX | **Applied, MAIN's sentence, verbatim, inserted immediately after I1′'s `uncovered = changed − covered` line (§4).** |
| `dispatch.agent_id` | SHOULD-FIX (item 9) | **Applied, MAIN's formula.** `f"{role}-{framing}-{uuid4().hex[:8]}"`, stated in §2 and §3. |

### 12b. Closing `hybrid_review_3.md` (K1–K14, 25′–27′) — historical, unchanged, not re-opened

Carried forward verbatim from v1.3 — see that document's own §12a for the full table (K1 uniform
signature; K2 `tool_call.args`; K3 `filter_candidates` unrestricted; K4 approval freshness window;
K5–K14 the SHOULD-FIX/LOW items; 25′/26′/27′ the three named-decision rulings). None of round 4's
findings reopen any of these; L1–L3 are new manifestations of the same finding *class* (K1's own header
already named it: "the loop's own pseudocode does not execute") in the surface v1.3 itself introduced.

### 12c. Decisions carried from v1.2/v1.3 (updated where superseded) plus new ones

Unchanged, still hold: manifest = dict; discovery mechanism; D6 (file edits off-registry); no
`record_consumer_check` tool; `run_lint` as one tool; `read_journal` wrapper; no `plan`/`observe` tool;
`commit`/`rebuild_index`/`run_suite`/`localize` as the four genuinely-new tools with no function to
wrap; `dataclasses.asdict()`-style `args_hash` rule; D13 (checkpoint clearance is `commit`'s own
precondition); the cumulative-vs-live dispatch-count split; UC4's `SINGLE_SOURCE` arithmetic; UC5's real
instance; `ctx.stop_criterion` advisory-only; `max_runs` cut; `action_id`'s computed formula (§2);
`hydrate`/`action_id` as shared helper modules, not duplicated per-adapter (31′); `commit`'s `action_id`
parameter dropped, not kept-and-ignored (32′); the loop-level refusal priority narrowed to `I4 > I1 >
I5` (30′).

**34′. New: `run_state` is removed from the loop entirely, not merely emptied.** v1.3's `run_state =
{"live_dispatches": 0}` is gone (§5) — L3's fix isn't "decrement it correctly," it's "there is nothing
left to decrement," since I5′'s own formula (§4) now reads the journal fresh at every check. This is a
strict simplification, not a behavior change: every worked case's `live_dispatches` progression in
`HYBRID_SEQUENCES.md` produces the identical numbers under the computed formula as it did under the
mutable counter (verified by re-walking Adversarial A, §8) — the fix removes a piece of state that was
never load-bearing once the formula itself is correct.

**35′. New: `dispatch_failed` and `approval_recorded` are named, together, as "the two orchestrator-only
journal events" (§3, §6) rather than `dispatch_failed` living in the tool table with an ad hoc `cost:
"—"` escape value that was never a real member of R1's own enum.** This is the structural fix L3 asked
for — not a special-cased manifest, a removal of the premise that it needed one.

**36′. New: the `hydrate` pseudocode (§2) is stated as the algorithm to implement, not literal
production code** — `typing.get_type_hints`/`get_args` behavior on `from __future__ import annotations`-
style string annotations (which `ctx.py`/`stages.py` already use, per those files' own headers) is a
real implementation detail a coder must handle correctly (`get_type_hints` resolves string annotations
via the defining module's own globals automatically; this is stdlib-guaranteed behavior, not something
this spec needs to re-derive) — noted so the pseudocode above isn't mistaken for something to paste
unmodified.

**37′. Deviation from the generic harness reminder** (prefer Bash cat/sed over Read/Write): this
revision was produced via `Read` (to load exact current file content before any edit, a tool
requirement) and `Write` (for the final, complete file), consistent with every prior round's identical
justification under this dispatch's own `PRECEDENCE` clause — noted again per that clause's own
requirement, matching the round-4 reviewer's own identical disclosure in `hybrid_review_4.md`'s header.
