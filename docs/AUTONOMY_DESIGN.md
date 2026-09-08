# Autonomy modes — design v2 (2026-09-08)

EJ's requirement: *"sometimes a user wants a long running … research to commit, all by the agent,
auto … keep running for hours. But sometimes when exploring, or when not confident yet, he wants
things to run 1 phase by 1 phase. The framework should allow an option here."*

EJ's four decisions: **three modes** (`auto`/`phase`/`step`); phase boundaries **named per task**;
**pre-authorised commit**; deferred decisions **continue-and-queue**.

**v2 supersedes v1 after an adversarial review** (`AUTONOMY_REVIEW.md`, 6 BLOCKER / 22 MAJOR).
v1's §1/§2/§9 stood; §3–§6 are redesigned here. Every v1 claim the review falsified is recorded in
§9 rather than quietly dropped, because the reasons are the useful part.

## 1. The gap this closes

`loop.py`'s own docstring: the stage order is offered as `suggested_next` "and never enforced.
`ceiling` is the one mechanical bound." Human stops are enforced in exactly three places, all
inside the invariant floor — `commit`'s checkpoint body, I4's owner gate, `done`'s
`owner-gate-pending`. Everything else that *reads* like a stop (`NEED_APPROVAL`, `HUMAN_GATE`,
`gate_reason`, `suggested_next`) is prose an agent honours voluntarily. In every ablation the agent
stopped because the **packet text** said to, not because the harness required it — the framework's
own recurring failure mode: a rule alive in commentary, never hardened into code.

## 2. Floor / policy split — the structural guarantee

Fixed order inside `loop.step`, unchanged by this work:

```
check_invariants(...)  -> refusal? return          # FLOOR — I1'-I5'
<autonomy is evaluated BEFORE the call is admitted at all, as a budget>  # POLICY
tools[call.tool].fn(...)                            # EXECUTE
```

**A mode can only ADD a stop, never remove one.** In v2 this is stronger than v1 made it: the
policy layer is not a refusal path at all (§3), so there is no branch in which it could evaluate to
"proceed" against a floor refusal. The review confirmed the ordering holds in the real code and
that `.fn(` has exactly one call site (`loop.py:109`).

The one thing that genuinely removes a stop is §5's pre-authorisation. It is therefore **not a
mode** — separately recorded, separately scoped, never satisfying I4, and §5.4 states its cost.

## 3. Pause = an effective ceiling, not a new refusal

The framework already owns exactly one mechanical, journal-derived, restart-proof stop: the
ceiling. `cli.cmd_call` recomputes the used budget from the journal on every process; `loop.run`
exits `CEILING_REACHED`. Since the CLI is already one process per call, "refuse this call" and
"end this run, re-enter" are operationally the same thing for a real agent.

So autonomy is **one pure function**, and no new refusal path:

```
effective_ceiling(events, rules, ceiling) -> int
    = (ordinal of the first executed call matching a pause rule that has no matching
       approval_recorded{gate:"resume"}) + 1,   else the manifest ceiling
```

`cmd_call`'s existing bound check and `loop.run`'s existing `range()` consume it unchanged.

**`effective_ceiling` is the single bound; `open_boundary` only *classifies* the stop** (so a pause
is distinguishable from an exhausted budget without being a second mechanism). This ordering was
not an aesthetic choice: the first implementation short-circuited on `open_boundary` *before* the
bound check, which made `effective_ceiling` dead code — a sabotage run (replacing its body with
`return ceiling`) passed all 20 cases. Both call sites now go through it, and the same sabotage
fails 3.

This deletes, rather than fixes, four v1 defects: `refused_by="PAUSE:…"` (rejected by the enum, and
overloading the *invariant id* field would manufacture the audit-dishonesty class the framework
already caught once); a paused `done` journaling `invariants_checked` for checks that never ran;
`loop.run` silently dropping a paused scripted call; and the ceiling being double-counted.

**Ordinal is defined once, in code terms:** the count of `tool_call` events for this run — exactly
what `cmd_call` already computes — never the journal file position. Boundary id: `pause:<name>@<ordinal>`.

Resume is `approval_recorded{gate: "resume", action_id: "pause:<name>@<ordinal>"}` — one new enum
member, consumed only by `effective_ceiling`.

## 4. The rules — one list, named per task

Phases are not a state machine: nothing tracks a current phase, and no phase has membership,
ordering, or an entry condition. One manifest key does all of it:

```json
"autonomy": "phase",
"pause_after": [
  {"name": "research",  "tool": "corroborate"},
  {"name": "implement", "tool": "prove", "exit_type": "PASS"},
  {"name": "land",      "tool": "commit"}
]
```

- `auto` → `pause_after: []`
- `step` → `pause_after: [{"name": "step", "tool": "*"}]`
- `phase` → the per-task list; **`init` refuses `phase` with an empty list.** There is deliberately
  no default list: EJ asked for per-task naming and a default would quietly become the answer.

A rule matches an event when the tool matches (`*` matches any), the call **executed and succeeded**
(`event_ok`: `refused_by is None and reason is None`), and — if the rule names one — `exit_type` equals it.

**`exit_type`, not `ok`, is why this is correct.** `tools/prove.py:37` returns `ok=True`
*unconditionally*; a failed prove is journaled `"ok: …Prove: FAIL … returned to planner"`. A rule
matching on `ok` would hand control back announcing "implement complete" at the exact moment prove
bounced to the planner. Matching `exit_type: "PASS"` is the only correct form for `prove`.

Matching on journaled facts is also the only *unforgeable* form: anything the agent declares is a
condition the agent controls, which is the hole D-KIND exists for.

## 5. Pre-authorised commit

`preauthorization_recorded{approver, scope_paths, max_uses, allow_kind_overrides, note}`, written by
an orchestrator-only CLI verb, never by the agent.

### 5.1 What it does and does not grant
It binds an advance approval **to a set of paths**. That is the part that earns new code: a
single-use, scope-blind advance approval is already expressible today (record
`approval_recorded{checkpoint, "commit:['master']"}` before the run; `last_commit_index` kills it
once the commit lands). Path binding is not expressible today, and it is what makes an unattended
run safe rather than merely possible.

**A pre-authorisation never satisfies I4.** Owner-gated rows stay owner-gated in every mode, grant
or no grant. Tested directly.

### 5.2 No derived approval is ever minted
v1 had the grant write an `approval_recorded` and then commit. The review broke that: every commit
shares the constant action_id `("commit", ["master"])` (`_shared.py:24`), so an approval derived
under a `research/**` grant sits in-window and clears a *later* `engine/` commit — reproduced
against the real `tools/commit.py`.

v2 mints nothing. The grant is evaluated **fresh, against the actual `changed_files`, at every
commit**, and the audit record `approval_derived{…}` is appended **after `git commit` returns 0** —
by a code path that authorises nothing and that branch 1 never reads. Nothing can outlive its scope
check because nothing is stored.

### 5.3 Liveness
All of: uses remaining (`max_uses` − `approval_derived` events for this grant, run-scoped);
**every** changed path covered by some `scope_path` — one unmatched path fails the whole commit,
the same all-or-nothing shape as I1; and, if the run holds a D-KIND `closed_world` override,
`allow_kind_overrides` is true.

**Path matching is segment-aware, not `fnmatch`.** `fnmatch`'s `*` crosses `/` — `research/**`
matches `research/../engine/x.py` and `research*` matches `researchx/y` (both ran). `*` matches
within one segment, `**` matches any number of segments, and any path that is absolute or contains
a `..` segment is rejected outright.

**Wall-clock expiry is dropped.** The framework's documented window rule is journal position, not
`ts` (`_shared.py:157`), and an expiry read at run scope would be meaningless without `read_all()`.
Run scope is the outer bound.

### 5.4 What it costs, stated plainly
A grant converts a **pre-commit disclosure into a post-commit review**. D-KIND's value in
ABLATION_3 came from the override being surfaced verbatim in `commit`'s refusal for MAIN to accept
or reject *before* the commit. Nobody reads that at 3am. `allow_kind_overrides` **defaults to
false**, so a run that produces an override falls back to stopping: the unattended path stays
available for the common case without silently weakening the case D-KIND was built for.

## 6. Deferral — one item, honestly scoped

A decision is deferrable iff **no lint and no invariant reads it** — a question with a citable
answer, not a judgment made at run time. Applying that test to v1's two candidates:

| candidate | reader | verdict |
|---|---|---|
| kind-override disclosure | none — only `commit`'s refusal text and the trace | **deferrable** |
| follow-on disposition | `lint_follow_on_without_disposition` → `run_all_on_plan` → `stages.prove:734`, and any finding forces `RETURN_TO_PLANNER` | **not deferrable** |

Deferring a follow-on disposition would either do nothing (the lint fires, the run stops anyway, at
a more confusing place) or require suppressing the lint — removing an existing stop through the
deferral door. It is dropped from the whitelist.

So: when a commit proceeds under a grant with `allow_kind_overrides: true`, `commit` appends one
`deferred_decision` per unreviewed override, and `done` reports the count in its `reason` while
still returning `ok=true` and `value="DONE"` — the run continues, which is the point, and the
existing eight exact-match assertions on `ToolResult(True, "DONE", None)` are untouched because no
run without deferrals produces one. `python3 -m ancient_games.hybrid queue` lists them and **exits
non-zero while any deferral is undismissed**, so a wrapper or CI can notice.

**The honest register, per §5.4:** the queue is a record, not a gate. Nothing downstream reads it —
not the next run's `gate`, not a lint (deliberately), not the scorer. A deferred decision is as
durable as a line in a report: recoverable if someone looks, lost if nobody does. The non-zero exit
is the cheapest available teeth that does not touch the floor.

## 7. Resume

Pausing *is* resume: the run stops on an open boundary, someone records the resume approval, the
next call proceeds off the same journal. No run state lives outside it.

For crash-resume (five agents died on rate limits on 2026-09-08 and were resumed by hand),
`init --resume` reuses an existing journal + run_id and refuses to clobber the saved ctx. The
ceiling already counts `tool_call` events from the journal, so it survives a restart unchanged.
`loop.run`'s in-memory `default_plan` is the one piece of state outside the journal; it is
reconstructed by replaying the run's **executed** calls (ok *or* declined — `loop.py:83` pops on
execution, not on success; v1 said "successful" and was wrong about the existing code).

## 8. Where the mode lives

**In the journal, as a `run_config` event written once by `init` — not in ctx.** `Ctx` is a plain
mutable dataclass and `loop.step` hands every non-RESTRICTED tool the loop's *own* object, so a
tool can mutate it (reproduced); and `cli.load_ctx` returns a fresh `Ctx()` when the file is
missing, so every plumbing failure would silently become `auto`. A journal event is append-only: no
tool can unwrite it. A run with no `run_config` event is `auto`, which is exactly today's
behaviour — the backward-compatible reading, and safe because the *floor* is identical in all modes.

## 9. What v1 got wrong (kept, because the reasons are the point)
- `refused_by="PAUSE:…"` is rejected by the enum, and widening it would be audit dishonesty (§3).
- `ends_when {ok: true}` fires on a **failed** prove (§4).
- A derived approval outlives its scope check under the constant commit action_id (§5.2).
- "follow-on disposition" is not deferrable by v1's own rule (§6).
- `fnmatch` crosses `/` (§5.3). Wall-clock expiry contradicts the journal-position window rule.
- The mode in ctx is mutable and fails open (§8).
- "visible in the journal, the trace, and the lints exactly like a human one" — false: `trace.py`
  renders no approvals and `index.py:159` says no lint reads them. §6 no longer claims it.
- New-mechanism count: v1 introduced 10 for EJ's four decisions; v2 introduces 4
  (one manifest key, one enum member, one exit code, the scope binding + its three event types).

## 10. Tests (e2e, per EJ's standing rule)
1. `step` pauses after every call; one resume approval clears exactly one boundary and no more.
2. `phase` runs a whole phase then pauses; a **refused** call matching a rule does not close a phase.
3. `prove` returning `RETURN_TO_PLANNER` does **not** satisfy `{"tool":"prove","exit_type":"PASS"}` (B2).
4. `auto` is byte-identical to today on an existing case journal (backward-compat pin).
5. Floor is unmovable — asserted where the grant code actually runs: a grant covering the changed
   path, on an **owner-gated** path, still refused by I4. (v1's version could not fail: I4 runs in
   the loop before `commit`'s body, so the grant code never executed.)
6. A grant covering `research/**` does not authorise a commit that also touches `engine/`.
7. `research/**` does not match `research/../engine/x.py`; `research*` does not match `researchx/y`.
8. `max_uses` exhaustion falls back to `checkpoint-not-cleared`.
9. `allow_kind_overrides: false` + a `closed_world` override → grant not live → run stops.
10. `allow_kind_overrides: true` → commit proceeds, one `deferred_decision` per override, `done`
    returns ok with the count in `reason`, `prove` still passes, `queue` exits non-zero.
11. No `approval_recorded` is ever written by the grant path; `approval_derived` postdates the commit.
12. `autonomy: "phase"` with an empty `pause_after` → `init` refuses.
13. Crash-resume: re-`init --resume` mid-run; ceiling count and ctx survive.
14. A `run_config` event cannot be overridden by a tool mutating ctx.
15. The manifest reports the *resolved* rules (never a misleading `[]` for `step`), and a
    `--resume` whose flags contradict the run adopts the journal's mode, not the flags'.

**Verified by sabotage, not by assertion** (the project's standing bar): breaking each guarantee in
turn must fail a case. `rule_matches` ignoring `exit_type` → 1 fail; `scope_covers` falling back to
`fnmatch` → 3; `live_grant` ignoring scope → 1; the audit record written before `git commit` → 1;
`effective_ceiling` never lowering the budget → 3. For §12: deferrals not outranking `DONE` → 2;
`DONE_WITH_DEFERRALS` exiting 0 → 2; a failing chooser read as no-choice → 1; `default_plan_from`
ignoring `RETURN_TO_PLANNER` → 1 (the first version of that case was degenerate and passed the
sabotage — with only `gate, guard` popped the remaining plan already equals `REPLAN`, so the case
now walks the plan to `prove` first). Full suite 318 passed.

## 12. The unattended supervisor (`ancient_games/hybrid/supervise.py`)

Built after the modes, because "runs for hours" needs something that *keeps* running and something
that decides when it may stop. Two pieces, deliberately separate:

**`terminal_state(events, rules, ceiling)`** — the oracle, from the journal alone:
`RUNNING | PAUSED | CEILING_REACHED | DONE | DONE_WITH_DEFERRALS`. Because every input is
journal-derived, a fresh process after a crash gives the same answer the dead one would have. That
is what makes a long run *resumable* rather than merely long. Order matters: a finished run
outranks a pause (a boundary after `done` has nothing left to gate), and deferrals outrank `DONE`
so an unattended run cannot end silently with disclosures nobody read.

**`drive(...)`** — `loop.run` with the one `[LLM]` cell moved out of process. A chooser *command*
receives the observation on stdin and answers with one `{"tool", "args"}` object on stdout, so the
supervisor is testable without a model (a three-line script is a valid chooser) and an LLM-backed
chooser is just one such program. Every iteration re-derives state from the journal, so killing the
process and re-running it resumes. `--max-calls` bounds one invocation without being a terminus.

**The queue gate.** `status` and `drive` exit **0 only** when the run finished with nothing
outstanding: `DONE`=0, `PAUSED`=3, `DONE_WITH_DEFERRALS`=**4**, unfinished=1. §6 keeps the queue
out of the invariant floor on purpose, so this exit code is the only teeth it has — enough for a
wrapper or CI to notice, and nothing the floor depends on.

```
python3 -m ancient_games.hybrid drive  --chooser 'python3 my_chooser.py' [--max-calls N]
python3 -m ancient_games.hybrid status         # same oracle, runs nothing
python3 -m ancient_games.hybrid queue          # the deferrals themselves
```

**Two limits, stated.** A journal records result *summaries*, not return values, so `last_results`
is empty under `drive` and `scripted`'s `{"$from": ...}` does not work there — an external chooser
reads the journal, which is the durable record. And `drive` fails loudly if a step journals
nothing, because a terminus derived from the journal would otherwise be unreachable and the loop
would spin (a sabotage that stopped it re-reading hung the suite instead of failing it).

## 11. Open, deliberately not built
- A phase whose exit is semantic rather than a journaled `exit_type` (§4: make it a tool).
- Wall-clock bounds. `ctx.time_box` exists and is unconsumed; nothing has asked for it.
- Anything downstream *reading* the deferral queue (§6 states why it does not).
