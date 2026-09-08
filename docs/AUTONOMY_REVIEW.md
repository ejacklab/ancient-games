# Adversarial review — `docs/AUTONOMY_DESIGN.md` (2026-09-08)

Reviewed against the code at `f163f74`, `master`, clean. `python3 -m pytest -q` → **282 passed in
6.06s** (ran). Everything below marked *(ran)* was executed; everything marked *(read)* is a code
citation I did not execute.

Scope: correctness of the proposed control flow, the boundary computation, the pre-authorisation,
the deferral queue, a simpler alternative, and the test list. No code was changed; this file is the
only artifact.

**Summary of ranks:** 6 BLOCKER, 22 MAJOR, 10 MINOR (plus 4 proposed test cases). The floor/policy *split* in §2 is the right
idea and the ordering it names is correct. The plumbing the brief chooses to carry the mode, the
predicate it chooses for `ends_when`, the lifetime it gives a derived approval, and the deferral
whitelist are each wrong in a way that costs rework after implementation.

---

## 1. Correctness of the control flow (`loop.step` and `cli.cmd_call`)

Answer to the direct question: **the §2 guarantee holds for the ordering as written, and fails on
the plumbing.** `check_invariants` → refuse-and-return happens at `loop.py:102-106`, before any
proposed insertion point, and the policy layer genuinely never observes a floor refusal. But the
guarantee is a property of *where the mode is read from*, not only of statement order, and the
brief's stated source for the mode (`ctx`) is writable by every tool body.

I looked for and did **not** find one hole worth recording as clean: no tool invokes another tool's
`fn`. `env.tools` is used only for manifest lookups (`tools/done.py:93-94`); the sole call site is
`loop.py:109` *(ran: `grep -rn "\.fn(" ancient_games` returns loop.py:109 and cli.py:339 only)*.
There is no tool-to-tool path around the floor or the pause.

### A1 — BLOCKER — `autonomy` "mirrored into ctx" is writable by any tool, so a mode CAN remove a stop
**Claim.** §3: "`autonomy` is a run-manifest field, mirrored into ctx." `Ctx` is a plain mutable
dataclass (`ancient_games/ctx.py:105-106`), and for every tool except `prove`/`done` the loop hands
the tool **its own ctx object by reference** (`loop.py:107-108`; HYBRID_SPEC §2 says so explicitly:
"the loop's own object, same reference, mutations visible to the caller"). The CLI then persists
whatever the tool wrote (`cli.py:266 save_ctx`). A tool body — including any tool added later via
`extra_tool_dirs` (UC9) — can set `ctx.autonomy = "auto"` and every subsequent pause disappears.
That is precisely the thing §2 says is impossible.

**Evidence (ran).** A five-line fake tool mutating `env.ctx` through `loop.step`:
```
loop's own ctx after the tool ran: MUTATED-BY-TOOL
```
Second cost, also ran: adding an `autonomy` field to `Ctx` fails the ctx contract —
`ValueError: ctx property 'autonomy' has no set-by/consumed-by entry` (`ctx.py:148-160`, exercised
by `tests/test_ctx.py:14`). So "mirror it into ctx" is not a free line; it needs a `CTX_META` entry
naming a stage that sets it and a field that consumes it, neither of which exists.

**Recommendation.** Delete "mirrored into ctx". Read the mode inside `step` from a source no tool
can write. Two options, in order of preference: (a) `init` journals the autonomy config as an
event, and `step` derives it from `journal.read()` like every other policy input — this also fixes
A7's audit gap and makes the mode visible in the trace; (b) pass it as an explicit parameter to
`step`, sourced from the manifest by both call sites. Either way: **absent or unparsable config
must fail closed (refuse), not default to `auto`.** As written, every failure of the mode-plumbing
— a deleted `.ctx.json`, a manifest without the key, an old manifest — fails *open* to the least
supervised mode. `load_ctx` already returns a fresh `Ctx()` when the file is missing
(`cli.py:110-111`), so this is not hypothetical.

### A2 — BLOCKER — `refused_by = "PAUSE:<boundary>"` cannot be journaled, and if it isn't journaled the CLI breaks and the pause is invisible
**Claim.** §2 proposes `Step(result=None, refused_by="PAUSE:<boundary>")`. The journal's enum is
closed: `_ENUMS[("tool_call","refused_by")] = ("I1","I4","I5", None)` (`journal.py:129`), and a
boundary id is unbounded text, so it can never be an enum member.

**Evidence (ran).**
```
A refused_by=PAUSE REJECTED: tool_call.refused_by must be one of ('I1','I4','I5',None), got 'PAUSE:step:12'
B gate=resume     REJECTED: approval_recorded.gate must be one of ('checkpoint','owner'), got 'resume'
```
If the implementer instead journals *nothing* on a pause, `cli.cmd_call:269` reads
`journal.read()[-1]["reason"]` when `st.result is None`. `approval_recorded` has no `reason` field
(`journal.py:120`), so a pause whose preceding event is an approval raises `KeyError`, caught at
`cli.py:340` and reported as `{"error": ...}` with exit 1 — an *error*, not a pause. And a pause
that writes no event is invisible to the journal, the trace and any post-hoc audit, which
contradicts §3's own "boundaries are computed from the journal".

**Recommendation.** Decide, in the brief, one of: (i) a new event type `paused{boundary, reason}`
with its own `SHAPES` entry — clean, auditable, and it keeps `refused_by` meaning "an invariant
refused this"; or (ii) adopt §5's alternative E2 below, where a pause is an effective-ceiling stop
and the existing CEILING_REACHED path already handles it. Do **not** widen the `refused_by` enum:
`tool_call.refused_by` is currently a three-value audit field that a reader can trust to mean
"floor", and mixing policy into it destroys exactly the distinction §2 is built on.

### A3 — MAJOR — a paused `done` would journal `invariants_checked: ["I2","I3"]` for checks that never ran
**Claim.** `loop.py:97` computes `checked = invariants_for(call)` once, and `invariants_for`
returns `LOOP_CHECKED + ELSEWHERE_CHECKED` (`invariants.py:45-49`); for `done` that is `("I2","I3")`
— I2 runs *inside `done`'s body* (`invariants.py:30-36`). Today `done` can never be stopped before
its body, because no loop invariant applies to it, so the record is honest. A pause makes it
stoppable, and the journaled event would claim I2 ran on a call where `done`'s body never executed.
This is a new instance of the exact defect class the house rules flag (`invariants_checked` once
named I5 on a call where it never ran).

The existing pin does not catch it: `tests/test_review_b_fixes.py:143-152` asserts the *table* is
self-consistent (`invariants_for(call) == evaluated + ELSEWHERE_CHECKED[...]`), not that a
particular journaled event's list matches what ran on that call.

**Recommendation.** On a pause (and on any future pre-body stop), journal
`invariants_checked = ` the ids the floor actually evaluated for that call — i.e.
`evaluate_loop_invariants(...)[0]`, which already returns them — and never the `ELSEWHERE_CHECKED`
half. Add the assertion to the test named in §8 (see T-new-3).

### A4 — MAJOR — `loop.run` drops a paused call; there is no `PAUSED` status
**Claim (ran).** `scripted` pops the queue inside `choose` (`loop.py:128-133`) *before* `step` runs,
and `run` treats `result is None` as `continue` (`loop.py:76-77`). A refused call is therefore never
re-offered. Demonstrated with an I5 refusal, which takes the identical control path a pause would:
```
step 0: tool=dispatch          refused_by=I5  result=None
step 1: tool=lookup_registry   refused_by=None result=ran
status: NO_CHOICE
```
So in `step` mode a scripted case loses one call per pause, and §8's case 1 ("`step` mode pauses
after every call; the resume approval clears exactly one boundary") cannot be written as stated
without either re-listing every call twice in `tool_calls` or changing `run`. Separately,
`RunResult.status` has no `PAUSED` member (`loop.py:37-40`), so a run that stopped at a boundary
reports `CEILING_REACHED` — a misleading audit record.

**Recommendation.** State the retry rule explicitly. If the pause stays a per-call refusal, `run`
must re-offer the same `Call` on the next iteration rather than calling `choose` again, and
`RunResult` needs a `PAUSED` status carrying the boundary id. E2 below removes the problem instead
of solving it.

### A5 — MAJOR — a journaled pause silently halves the ceiling in `step` mode
**Claim.** `cli.cmd_call:261` counts `tool_call` events to enforce the ceiling, and `loop.run`
consumes one `range(ceiling)` iteration per refusal. If a pause is journaled as a `tool_call`
(the only shape the brief names), a `step`-mode run of N real calls consumes 2N of a budget whose
default is derived from *free-agent journals recorded in `auto` mode* (`cli.default_ceiling`,
`cli.py:58-69`). The mode that is supposed to be strictly *more* supervised gets half the work
budget, silently. `ceiling` is the framework's one mechanical bound; changing its meaning as a side
effect of a policy knob deserves an explicit decision, not an emergent one.

**Recommendation.** Whichever event a pause writes, exclude it from the ceiling count, and say so in
the brief. (Under E2 this inverts into a feature: the ceiling *is* the mechanism.)

### A6 — MAJOR — the resume approval is written by a verb the agent is only *told* not to call
**Claim.** §1 correctly diagnoses "a rule alive in commentary, never hardened into code", then
builds the new stop's *release* on exactly such a rule. `approve` is orchestrator-only by docstring
(`cli.py:23-25`: "The subagent under ablation must NOT call `approve`") and nothing enforces it: the
only writer is `cmd_approve` (`cli.py:281-286`) *(ran: `grep -rn approval_recorded` shows one writer
and no guard)*, and the ablation scorer never inspects approvals (`ablation/score.py` contains no
`approv*` reference, ran). An agent in `step` mode that wants to run unattended can clear its own
boundary with one shell command.

This is not a regression — the checkpoint and owner gates have the same property — but §1 and §2
claim a *category* change ("a property of the control flow, not of a test"), and for the pause
specifically the property is weaker than claimed: the stop is unskippable but self-clearable.

**Recommendation.** State the honest guarantee: *the pause cannot be skipped, and clearing it is
recorded with an approver name.* Then add the one cheap hardening the framework already has a slot
for: have `approve` refuse (or mark the event) when it is invoked from the agent's own process —
e.g. require an `--approver` that matches a value fixed in the manifest at `init` time, so a
self-approval is at minimum a *forged approver name* and not merely an undocumented convention.
If that is judged not worth it, say so explicitly in §2 rather than leaving the stronger reading.

### A7 — MAJOR — nothing in the journal records which mode a run ran in
**Claim.** The mode lives in the manifest (and, per the brief, in ctx). Neither is in the journal.
Post hoc, an auditor reading a journal cannot tell whether a run claimed `step`, `phase` or `auto`,
and therefore cannot tell whether an absent pause means "the policy allowed it" or "the policy was
not applied". That is the audit-record defect class again, one level up.

**Recommendation.** `init` journals the autonomy config (mode + phase list + grant references).
This also gives A1 its tamper-resistant source and gives §8's case 3 something to assert against.

### A8 — MAJOR — §2's guarantee rests on statement order with no test that can detect a swap
**Claim.** If a future edit hoists `autonomy_pause` above `check_invariants` — a plausible
"optimisation", since the pause is cheaper than `changed_files()`'s two `git` subprocesses
(`_shared.py:307-324`) — a call that should be journaled as `refused_by: "I4"` would instead be
journaled as a pause, and the I4 record would be lost. §8 case 4 cannot detect this (see T4 below).

**Recommendation.** Add the order-detecting case in T-new-3.

### A9 — MAJOR — §7's `default_plan` reconstruction rule is wrong about the existing code
**Claim.** §7: "reconstructed by replaying the run's **successful** calls through the same
pop/`REPLAN` rule." The actual rule pops on *executed* calls regardless of `ok`: `loop.py:76-84`
returns early only when `result is None` (a floor refusal); the `elif default_plan and call.tool ==
default_plan[0]: default_plan.pop(0)` branch at `loop.py:83-84` runs for a declined
(`ok=False`) result too. A reconstruction that replays only successful calls yields a different
`suggested_next` after a resume than the same run would have had without a crash.

**Recommendation.** Restate as "every call that executed (result is not None), ok or declined",
and pin it with the crash-resume case (§8 case 11) asserting `suggested_next` across the restart.

### A10 — MINOR — `init --resume` would silently re-derive the ceiling
`write_manifest` always writes a fresh ctx (`cli.py:91`) — so `--resume` needs a real change, as the
brief says — but also: `cmd_init` recomputes `default_ceiling()` from `ablation/runs/**` when
`--ceiling` is absent (`cli.py:232, 58-69`), and that directory grows with every ablation. A resume
must inherit the *original* manifest's ceiling, not re-derive it. Say so.

### A11 — MINOR — unknown-tool calls bypass both layers
`loop.py:98-101` returns before `check_invariants`, so an unknown tool is journaled during a pause
too. Harmless (nothing executes), but if the pause is meant to be "no call proceeds", the brief
should say the unknown-tool branch is deliberately outside it.

---

## 2. The boundary computation (§3)

**What is sound, briefly:** index stability under a *shared* journal file holds. `Journal.read()`
filters by `run_id` while preserving file order (`journal.py:208-212`), and the file is append-only
with positions of past events immutable, so another run interleaving events cannot shift this run's
run-scoped indices. The replay path is the one unscoped reader (`hybrid/runner.py:84`,
`read_events`) and it never calls the loop (`runner.py:80-86`), so no boundary is ever computed on
unscoped indices. Deriving boundaries rather than storing them is the right call and matches I5.

That is conditional on one thing the brief does not say:

### B1 — MAJOR — `<event_index>` is ambiguous between two live numberings that disagree
**Claim.** The repo has two indices. (i) *Journal position* — what `last_commit_index` and
`approvals_after` use (`_shared.py:280-291`). (ii) *Tool-call ordinal* — `loop.step`'s own `index`
parameter (`loop.py:88`), computed in the CLI at `cli.py:261` and printed as the field literally
named `"step"` at `cli.py:267`. An implementer writing `step:<event_index>` will reach for
`Step.index`, because it is right there and it is called "step".

**Evidence (ran)**, on the two real free-agent journals:
```
ablation/runs/attempt4/UC2J.journal.jsonl  total=108  tool_call=62
ablation/runs/attempt4/UC3.journal.jsonl   total=85   tool_call=47
```
The two numberings diverge by ~40% on real runs. If a boundary id is minted with one and looked up
with the other, resume approvals silently never match — the run pauses forever, or (worse, if the
mismatch goes the other way) an unrelated approval clears a boundary.

**Recommendation.** Define the id in code terms in the brief: *`<event_index>` is the 0-based
position in `Journal.read()`* — and add "never `Step.index`, never `cli.cmd_call`'s `step`" as an
inline note, since that is the mistake a reader will make.

### B2 — BLOCKER — `ends_when: {"tool": "prove", "ok": true}` fires on a **failed** prove
**Claim.** `tools/prove.py:37` returns `ToolResult(ok=True, value=_prove(...))` unconditionally —
`ok` reports "the adapter ran", not "the proof passed". A `RETURN_TO_PLANNER` exit is `ok=True`.
The brief's own example phase list (§4) therefore closes the `implement` phase on a prove that
*failed and returned to the planner*, which is the exact moment you least want to hand back control
saying "phase complete".

**Evidence (ran).** Real journals contain the shape:
```
"result_summary": "ok: RETURN_TO_PLANNER"   # ablation/runs/attempt4/UC3.journal.jsonl, and 4 more
```
Note also that the codebase already has three distinct notions of "went fine" and `ends_when`'s
`ok` matches none of them cleanly: `event_ok(e)` = `refused_by is None and reason is None`
(`_shared.py:275-276`), `refused_by is None` alone, and `exit_type == "PASS"`. `done` uses the third
(`tools/done.py:130-131`).

**Recommendation.** Make `ends_when` a match against the journaled `tool_call` event with an
explicit, checkable predicate: `{"tool": ..., "ok": true}` means `event_ok(e)`, and add an optional
`"exit_type"` key so the `implement` phase is
`{"tool": "prove", "ok": true, "exit_type": "PASS"}`. Have `init` **refuse** `ends_when` on `prove`
without an `exit_type`, because the unqualified form is always wrong for that tool. Fix the §4
example.

### B3 — MAJOR — two phases naming the same `ends_when` tool is undefined
**Claim.** The id is `phase:<name>@<event_index>`. Two phases whose `ends_when` names the same tool
produce two ids at the same index (`research@12` *and* `design@12`). Both open ⇒ two resume
approvals for one call; first-match-wins ⇒ the second phase silently never fires. The brief picks
neither.

**Recommendation.** `init` refuses a `phases` list with a duplicate `ends_when` tool (cheapest, and
consistent with §4's "no default phase list" strictness). This ambiguity disappears entirely under
E1 below.

### B4 — MAJOR — `ends_when` naming a tool that is never called (or does not exist) degrades that phase to `auto`, silently
**Claim.** The run is not stuck — nothing waits on a phase — it just never pauses there, which is
the failure direction that loses supervision without announcing it. A typo (`corroborrate`) buys
`auto` for that phase. `cmd_init` does not load tools today (`cli.py:231-235`), so nothing would
catch it.

**Recommendation.** `init` validates each `ends_when.tool` against `load_tools(*tool_dirs)` and
refuses on an unknown name — the same shape as §4's "`phase` with no `phases` → `init` refuses".
A never-*called* (but valid) tool cannot be caught statically; state explicitly that such a phase
never pauses, so nobody reads silence as supervision.

### B5 — MINOR — phase re-opening on replan is unstated
On `prove → RETURN_TO_PLANNER → …replan… → prove` a second `ends_when` match mints a *new* id at a
new index, so the phase pauses again. That is almost certainly right, but say it: a reader of §3
can equally conclude a phase closes once.

### B6 — MINOR — a boundary at the last call has no consumer
If the final phase ends at `commit`, the run pauses after `commit` and needs a resume before `done`.
Fine, but the H15 owner-gate terminus (`tools/done.py:135-139`) already stops there; the brief
should say which stop the operator sees first.

---

## 3. The pre-authorisation (§5)

This is where the design actually removes a stop, and it has the review's most serious defect.

### C1 — BLOCKER — a derived approval outlives the scope check that justified it, and clears a later out-of-scope commit
**Claim.** §5.1 says `commit` appends `approval_recorded{gate: "checkpoint", action_id: aid}`
**before** committing, and that branch 1 (explicit in-window approval) is tried *first* on every
subsequent call. But `aid` is the constant `commit:['master']` (`_shared.py:177`,
`tools/commit.py:35`) and branch 1 is scope-blind: `approvals_after(events, "checkpoint", aid,
last_commit_index(events))` (`commit.py:36`). If the commit that derived the approval does **not**
land — `git add` or `git commit` fails (`commit.py:40-45`: pre-commit hook, index lock, nothing-to-
commit), or the CLI process dies between the append and the commit — `last_commit_index` does not
advance, the derived approval stays in-window, and the *next* commit takes branch 1 and never
consults the grant's scope at all.

**Evidence (ran).** Real `tools/commit.py` against a real git repo. An approval derived while the
changed set was `research/b.md` under a `research/**` grant; the commit does not land; the agent
then changes `engine/x.py` and commits:
```
commit action_id: commit:['master']
changed at derivation: ['research/b.md']
changed now: ['engine/x.py']
checkpoint cleared for THIS commit? True
commit result ok=True reason=None value={'hash': '8a5cf1e...'}
8a5cf1e out of scope
 engine/x.py | 1 +
```
`engine/x.py` was committed on the authority of a grant scoped to `research/**`. Note that I1 does
not backstop this: I1 requires a *guard* covering the changed file (`invariants.py:90-101`), and
`guard` is a call the agent makes itself, so I1 is satisfiable by the agent. The grant's scope was
the only scope authority, and it was bypassed.

**Recommendation (fixes C1 and C3 together).** Do not write `approval_recorded` from the grant path
at all. Write a distinct event — `approval_derived{action_id, grant, scope_matched, changed}` — and
have `commit`'s branch 1 read only `approval_recorded` (unchanged code, unchanged meaning: a human
said yes). Branch 2 then re-evaluates the grant, including the scope match, on **every** commit,
because there is no derived artifact for it to short-circuit on. Additionally, write the derived
event only after `git commit` returns 0, so a failed commit leaves no authorisation residue. Both
changes are cheap; each alone closes the demonstrated hole; together they also make the use-count in
C4 exact.

### C2 — BLOCKER — every journal event §5 proposes is rejected by the current validator
**Evidence (ran).**
```
B gate=resume       REJECTED: approval_recorded.gate must be one of ('checkpoint','owner')
C derived_from      REJECTED: approval_recorded event carries undeclared fields ['derived_from']
D preauthorization_recorded REJECTED: unknown event type 'preauthorization_recorded'
```
(`journal.py:120,125-131,144-167`.) The brief names three new journal shapes and mentions none of
the `SHAPES`/`_ENUMS` work. Also relevant: `_OPTIONAL` (`journal.py:124`) exists precisely so
pre-existing journals still read; any field added to an existing shape needs an `_OPTIONAL` entry or
every ablation journal under `ablation/runs/**` stops validating — which would break the replay
cases and `ablation/score.py`.

Separately: `approver: "<approver> (preauthorized)"` stuffs structured data into a free-text field.
The repo's own standard is structured fingerprints, not string mangling; the derived-ness belongs in
a typed field on a typed event (which C1's fix provides).

**Recommendation.** Enumerate the journal-schema delta in the brief: the new event type(s), their
`SHAPES` entries, the `_ENUMS` addition for a `resume` gate, and `_OPTIONAL` where an existing shape
grows. This is a five-line change but it is load-bearing and currently invisible in the plan.

### C3 — MAJOR — §5.1 has a tool writing `approval_recorded`, which HYBRID_SPEC §6 forbids
**Claim.** HYBRID_SPEC §6: "`approval_recorded`'s writer — unchanged from v1.3: the orchestrator,
directly, outside all 17 tools; **no tool in §3 can write it**." §5.1 has `commit` write one. And —
the irony is worth naming — that spec sentence is itself prose that was never hardened: the only
writer today is `cli.cmd_approve` (`cli.py:281-286`) *(ran: grep)* and nothing prevents a tool from
appending one. So nothing will stop the implementer, and the reviewable invariant "an
`approval_recorded` means a human decided" is lost quietly.

**Recommendation.** As C1: separate event type. Then the spec sentence stays true and *becomes*
testable — add the pin (T-new-1 asserts no tool writes `approval_recorded`).

### C4 — MAJOR — "visible in the journal, the trace, and the lints exactly like a human one" is false for the trace and vacuous for the lints
**Evidence (read).** `trace.render_trace` (`trace.py:74-106`) renders stage exits, corroboration,
kind overrides, consumer checks and dispatches — **no approvals section at all**, human or derived.
`index.py:159`, verbatim: "dispatch, exit, tool_call, approval_recorded, dispatch_failed, rule_fire:
no lint reads them — not projected." So the equality claim holds only in the sense that both are
equally invisible.

**Recommendation.** Either build the trace section (one table, ~6 lines in `trace.py`) and say the
lints do not and will not read approvals, or correct §5.1 to "visible in the journal" and drop the
other two. As written it is an audit claim about a surfacing that does not happen — the second
flagged defect class.

### C5 — MAJOR — wall-clock expiry contradicts the documented ordering rule and is meaningless at the scope the grant actually has
**Claim, three parts.**
(a) The repo's stated ordering rule is explicit: "'postdates' is journal position, not `ts` — the
journal is append-only with one writer, so position is the order it actually guarantees"
(`_shared.py:157-160`). §5 introduces the first predicate in the system that depends on wall clock.
(b) The clock source is unspecified. `journal._now()` uses `time.gmtime()` (`journal.py:291-292`) —
the process clock, in a process the agent's own tooling launches. I rate the "agent manipulates the
clock" threat **low (60% confident it is not worth defending)**: it needs `libfaketime` or root, and
an agent with that much reach has easier paths. What would settle it: decide whether the ablation
agent's shell is in the trust boundary; if it is, say so once and stop defending against it
anywhere.
(c) The part that is not speculative: **a grant is per-run whether you intend it or not.** Any
journal lookup that respects run-scoping (`Journal.read()`, `journal.py:208-212`) cannot see a grant
recorded under another `run_id`. So an 8-hour expiry buys nothing a per-run grant does not already
give — *unless* the implementer reaches for `read_all()` to make cross-run grants work, which is
exactly the run-scoping defect class the house rules flag (and would let a grant recorded for run A
authorise run B's commits in a shared journal file).

**Recommendation.** Drop wall-clock expiry. Scope the grant to the run (`init --resume` reuses the
`run_id`, §7, so crash-resume keeps working) and bound it with `max_uses`, which is already
journal-derivable. If a genuine multi-hour multi-run grant is later needed, that is a separate
design with its own trust argument. Add an explicit line to §5: **the grant lookup and the use count
both use `Journal.read()`, never `read_all()`.**

### C6 — MAJOR — `fnmatch` does not treat `/` specially, so `scope_path` is looser than it reads
**Evidence (ran).**
```
fnmatch('research/../engine/x.py', 'research/**') = True
fnmatch('docs/deep/nested/secret.md', 'docs/**')  = True
fnmatch('researchx/y',              'research*')  = True
fnmatch('research',                 'research/**')= False
fnmatch('engine/x.py',              'research/**')= False   # the intended case does work
```
`*` crosses `/` in `fnmatch`, so `research/**` matches a `..` traversal, and the shorthand
`research*` matches the sibling directory `researchx/`. Today the traversal is unreachable in
practice because `changed` comes from git, which emits normalised repo-relative paths
(`_shared.py:307-324`) — but nothing in the code *asserts* that, and the all-or-nothing scope rule
is the grant's only containment.

Two related path facts worth one line each in §5: with `core.quotePath` at its default, git prints
non-ASCII paths as `"research/\303\251.py"` including the quotes, which will fail to match any scope
pattern — fail-closed, so safe, but it will look like a mysterious refusal. And a worktree rename
appears as a deleted tracked path plus an untracked new path, so both must be in scope; the
all-or-nothing rule handles it correctly.

**Recommendation.** Normalise and validate before matching: reject any `changed` path or
`scope_path` containing a `..` segment or an absolute prefix, and match with
`PurePosixPath(p).match(pat)` or an explicit "exact path, or pattern ends in `/**` and `p` starts
with the prefix" rule. State in §5 that a pattern must be an exact path or end in `/**` —
`research*` should be refused at grant time.

### C7 — MINOR — §5.2's I4 claim is true, but for a reason that makes §8 case 4 vacuous
The claim holds in the real code: I4 at commit runs in the **loop** (`invariants.py:65-70`, called
from `loop.py:102`) before `commit`'s body executes, so the grant code cannot run at all on an
owner-gated commit. There is no ordering in which a derived approval is written and then I4 refuses.
But that also means the corresponding test cannot fail — see T4.

### C8 — MINOR — kind-override liveness is run-wide and never clears
`kind_overrides(events, run_id)` (`journal.py:283-288`) is run-scoped but not commit-windowed, so
once a run produces one override, the grant is dead for the rest of the run even after a human
inspects and clears it at the resulting stop. That is the right default (fail closed), but §5.3
should state it, because the operator will hit it and read it as a bug.

### C9 — MINOR — `changed` is computed twice; the scope check must use `commit`'s own copy
`invariants.evaluate_loop_invariants` calls `changed_files(cwd)` (`invariants.py:66`) and
`commit.run` calls it again (`commit.py:38`) — two `git` invocations at different times. The scope
check must use the same list that is passed to `git add`, i.e. computed inside `commit` immediately
before staging, or a file that appeared in between is committed unscoped.

---

## 4. The deferral queue (§6)

### D1 — BLOCKER — "follow-on disposition" fails the brief's own deferrability rule; deferring it either does nothing or removes a stop
**Claim.** §6's rule is "deferrable **iff** nothing downstream depends on it", and its whitelist
puts "follow-on disposition" in the deferrable column. Something downstream depends on it, and it is
`prove`:
- `lint_follow_on_without_disposition` (`lints.py:58-68`) emits a Finding for any follow-on whose
  disposition is not `fixed | new-task | dismissed:reason | escalated:owner`;
- it runs inside `run_all_on_plan` (`lints.py:285-287`, and the SQL path at `lints.py:308`);
- `stages.prove` calls `run_all_on_plan` (`stages.py:734`) and **any** finding forces
  `RETURN_TO_PLANNER` (`stages.py:735-742`).

So a deferred follow-on disposition has exactly two possible implementations, both bad: (i) the
lint still fires, `prove` returns to the planner, and the "queue" bought nothing — the run stops
anyway, at a confusing place; or (ii) the implementer suppresses the lint when a `deferred_decision`
covers it, which **removes an existing stop** — the precise thing §2 promises modes can never do,
arriving through the deferral door rather than the mode door.

**Recommendation.** Remove "follow-on disposition" from the deferrable column, or redefine the
deferrable item as something the lint does not read (e.g. "a follow-on may be dispositioned
`new-task` and queued" — which is already legal today and needs no new mechanism, since `new-task`
*is* a disposition). More generally: the whitelist must be derived by asking, for each candidate,
"which lint or invariant reads this?" — and the answer must be cited in the brief. The one
remaining entry (kind-override disclosure) does pass that test: no lint reads `kind_override`
(`index.py:159`), only `commit`'s refusal text (`commit.py:19-26`) and the trace (`trace.py:90-95`).

### D2 — MAJOR — the queue is advisory and the brief oversells it
**Claim.** "continue-and-queue" implies the decision is preserved. Mechanically, a
`deferred_decision` event is written, `done` returns `ok=true`, `RunResult.status` becomes
`DONE_WITH_DEFERRALS`, `render_trace` grows a section, and a `queue` verb lists it. Nothing ever
reads it again — not the next run's `gate`, not a lint (§6 forbids that on purpose), not
`ablation/score.py`. A deferred decision is exactly as durable as a line in a report: recoverable
if someone looks, lost if nobody does.

**Recommendation.** Say that, in §6, in §5.3's honest register: *the queue is a record, not a gate;
a deferred decision is lost if no human reads the trace.* Then, if teeth are wanted without blocking
`prove`, the cheap non-blocking option is an **exit code**: `queue` exits non-zero while any
deferral in the run is undismissed, so a wrapper script or CI can notice. That is one line and it
does not touch the floor.

### D3 — MAJOR — `deferred_decision` and `DONE_WITH_DEFERRALS` need declared surfaces the brief does not name
`deferred_decision` needs a `SHAPES` entry (ran: unknown event types are rejected outright,
`journal.py:144-146`). `DONE_WITH_DEFERRALS` needs `loop.run`'s status branch (`loop.py:78-80`),
`RunResult`'s docstring enum (`loop.py:39`), and the case runner's `expected_final.status` compare
(`hybrid/runner.py:141-142`) — which is how §8 case 8 would assert it.

### D4 — MINOR — "the clearing tool appends" makes `commit` a policy-event writer
Same architectural point as C3: the tools currently write only `tool_call`-adjacent and stage
events. If `commit` writes `deferred_decision`, say so as a deliberate change to §6's writer rule.

---

## 5. A simpler alternative

**Ranking rule, fixed before I evaluated anything.** Between designs that satisfy all four of EJ's
decisions (three modes; phases named per task; pre-authorised commit; continue-and-queue), prefer
the one with (1) fewer *new mechanisms* — counting: new event types, new refusal paths, new enum
members, new CLI verbs, new `Step`/`RunResult` semantics; then (2) more of the guarantee carried by
an existing, already-tested path; then (3) fewer places a rule lives in prose. Ties go to the
smaller diff.

The brief as written introduces: 2 new event types, 1 new refusal path with a new `refused_by`
namespace, 2 new enum members, 3 new CLI verbs (`preauthorize`, `queue`, `init --resume`), a new
`RunResult` status, a new manifest section, and a new ctx field. **Count: 10.**

### E1 — MAJOR — phases are not a state machine; collapse §3+§4 into one list
**Observation.** Nothing in the design tracks *which phase is current*. A phase has no membership,
no ordering constraint, no entry condition. `phases` is, operationally, a set of tools after which
the run pauses; names appear only inside the boundary id and the resume message; `step` is the same
thing with "every tool". The phase abstraction is doing no work that the list is not.

**Delete from the brief:** the `phase:<name>@<index>` / `step:<index>` id split, and with it B3's
duplicate-name ambiguity, and §4's implication that phases are sequential.

**Replace with:** one manifest key,
```json
"pause_after": [{"name": "research", "tool": "corroborate", "ok": true},
                {"name": "implement", "tool": "prove", "ok": true, "exit_type": "PASS"}]
```
`step` mode is `pause_after: [{"name": "step", "tool": "*"}]`; `auto` is `[]`. One id shape
(`pause:<name>@<index>`), one predicate, EJ's per-task naming preserved verbatim, and `init`'s
validation (B4) becomes a loop over one list. **Saves: 1 id shape, 1 ambiguity, ~half of §4.**

### E2 — MAJOR — express the pause as an *effective ceiling*, not a new refusal path
**Observation.** The framework already owns exactly one mechanical, journal-derived, restart-proof
stop: the ceiling. `cli.cmd_call:261-263` recomputes the used budget from the journal on every
process; `loop.run` exits `CEILING_REACHED`; §7 already argues that pausing and resuming needs no
state outside the journal, and the CLI is *already* one process per call — so "refuse this call" and
"end this run, re-enter" are operationally the same thing for the real agent.

**Proposal.** One pure function:
```
effective_ceiling(events, config) -> int
    = (index of the last executed call satisfying a pause_after rule that has no matching
       approval_recorded{gate:"resume"}) + 1,  else the manifest ceiling
```
`cmd_call`'s existing bound check and `loop.run`'s existing `range()` do the rest.

**Delete from the brief:** `refused_by = "PAUSE:<boundary>"` (and with it A2's enum problem and A3's
`invariants_checked` dishonesty, since no pre-body stop event is minted at all), the new
`Step`/`RunResult` pause semantics (A4), and the ceiling double-count (A5). **Keep:**
`approval_recorded{gate: "resume", action_id: <boundary_id>}` as the audit record — one enum member,
consumed by `effective_ceiling`.

**Honest costs, stated.** (a) A pause ends the run rather than refusing one call, so `loop.run`
reports `CEILING_REACHED` where a reader might want `PAUSED` — worth one extra status, derived from
whether an open boundary exists. (b) The scripted case runner expresses resumption as a second
`loop.run` over the same journal instead of an injected event mid-run — which I claim is *better*
for §8, because it exercises resume-from-journal, the property that actually matters, instead of an
in-memory continuation the real CLI never performs. (c) The CLI currently reports a ceiling stop as
`ValueError` → exit 1 (`cli.py:262-263, 340-342`); a pause deserves its own message and probably its
own exit code. That is one branch.

**New-mechanism count for E1+E2: 3** (one manifest key, one enum member, one exit code) against the
brief's 10 for the same two EJ decisions.

### E3 — MAJOR — §5's grant earns *scope*; it does not earn `max_uses` or expiry
**Observation.** A single-use pre-authorisation is *already expressible today*: record
`approval_recorded{checkpoint, "commit:['master']"}` before the run and the next commit clears
(`commit.py:36`); after that commit lands, `last_commit_index` advances and the approval is dead —
one approval, one landing, which is exactly the documented K4 semantics. What today's mechanism
cannot express, and what genuinely justifies new code, is **binding an advance approval to a set of
paths**. That is the part of §5 that earns itself.

**Recommendation.** Build the scope binding (with C1's separate derived event and C6's path rules).
Keep `max_uses` if multi-commit unattended runs are a real requirement — it is cheap once the
derived event is typed — but drop wall-clock expiry (C5) and let run scope be the outer bound.

### E4 — verdict on whether the mechanism earns itself
`autonomy` modes: **yes, but at a third of the proposed cost** (E1+E2). Pre-authorised commit:
**partly** — the scope binding earns itself, the expiry does not (E3). Deferral queue: **not as
specified** — its only non-vacuous whitelist entry is the kind-override disclosure (D1), and for
that single case the mechanism is one journal event plus a trace section; `DONE_WITH_DEFERRALS`,
a `queue` verb and a `RunResult` status for one deferrable item is more machinery than the item
justifies. Consider shipping the kind-override deferral as a journaled event + trace row only, and
adding the verb when a second deferrable item exists.

---

## 6. The tests (§8)

### T4 — MAJOR — "floor is unmovable" cannot fail, in any of the three modes
Case 4 asserts an owner-gated commit is refused by I4 with a grant present. I4 at commit runs in the
loop (`invariants.py:65-70` via `loop.py:102`) and returns before `commit`'s body — where all the
grant code lives — ever executes. The case would pass identically against a build in which the grant
code is deleted, or catastrophically wrong. It tests an ordering guaranteed by a different file.

**Make it real:** assert on the *journal*, not just the refusal — that the refused call produced no
derived-approval event of any kind — and add the case where I4 can actually interact with a
consumed grant: a first commit clears via the grant, then a second commit touches an owner-gated
path (I4(b), `invariants.py:134-145`) and must still refuse.

### T3 — MAJOR — "byte-identical" is unachievable, so the pin will be weakened at implementation time
`ts` is minted per event from the wall clock (`journal.py:291-292`) and `commit`'s
`result_summary` embeds the git hash (`commit.py:46`, `_shared.py:245-257`), which varies with
commit time. No two runs produce byte-identical journals. Restate the backward-compat pin as: the
sequence of `(event, tool, refused_by, exit_type)` tuples and the `exit_line` list are identical to
the recorded case. That is checkable, and it is what the case runner already compares
(`hybrid/runner.py:104-141`).

### T2 — MAJOR — right idea, wrong edge
"`ends_when` on a **refused** call does not close a phase" tests the easy half. The defect is B2:
`ok=True` with `exit_type=RETURN_TO_PLANNER`. Extend case 2 to cover all three outcomes of the same
tool: refused (`refused_by` set), declined (`ok=False`, `reason` set), and executed-but-failed
(`ok=True`, `exit_type=RETURN_TO_PLANNER`). Only the fourth (`ok=True`, `PASS`) may close a phase.

### T8 — MINOR — vacuous as written, useful with one change
"`prove` still passes" with a deferral present asserts the absence of a coupling nobody built. It
becomes the highest-value case in the list if the deferred item is a **follow-on disposition**, at
which point it fails and exposes D1. Use it that way, or drop the clause.

### T6 — MINOR — expiry test tests the mock
With no clock seam, the only way to test expiry is to monkeypatch time, which tests the patch. If
C5 is accepted and wall-clock expiry is dropped, this case becomes `max_uses` exhaustion only, which
is journal-derivable and genuinely testable.

### Failure modes with no case at all — four additions, ranked

**T-new-1 (catches C1, the BLOCKER).** Grant scoped `research/**`; derive an approval; make the git
commit fail (a `pre-commit` hook exiting 1 is the cleanest fixture); then change `engine/x.py`,
guard it, and commit again. Assert the second commit is **refused/declined** and that no
`approval_recorded` event was written by any tool in the run. Without C1's fix this test commits
`engine/x.py` — I ran that exact sequence against the real `tools/commit.py` and it committed.

**T-new-2 (catches the run-scoping and index-numbering defects, B1 + C5c).** One journal file, two
runs (`R1` then `R2`) interleaved, plus non-`tool_call` events (a `claim_recorded`, an
`approval_recorded`) between calls so that journal position and tool-call ordinal diverge — they
diverge by ~40% on the real journals. Assert: `R2` does not see `R1`'s grant; a boundary id minted
in `R1` is not clearable by an approval recorded under `R2`; and the boundary id resolves to the
same event after `R2` has appended.

**T-new-3 (catches A3 and A8, the order-swap and the dishonest audit record).** One call that is
*both* at an open boundary and refusable by I4. Assert the journaled event names `I4` and not the
pause, and — on a paused `done` — that `invariants_checked` does **not** contain `I2`. This is the
only case in the list that can detect a future reordering of the two layers, which is the whole of
§2's guarantee.

**T-new-4 (catches the CLI/loop asymmetry, A2's `KeyError` and the parity hole).** Every case in §8
is loop-side; the real agent drives `python3 -m ancient_games.hybrid call` one process at a time,
where ctx round-trips through disk (`cli.py:104-113`) and the ceiling is recomputed from the journal
(`cli.py:261`). Run a `step`-mode pause, a resume and a grant consumption entirely through the CLI,
asserting exit codes and the printed JSON. This is also the case that catches A1: delete the
persisted `.ctx.json` between calls and assert the run does **not** silently become `auto`.

---

## Verdict

**Redesign — narrowly scoped.** §2's floor-then-policy split is the right structure and the ordering
it names is correct in the real `loop.step`; EJ's four decisions are all satisfiable; §7's
crash-resume story is sound apart from one wrong sentence (A9). But four things must change before
code is written, and each is a design decision rather than an implementation detail: the mode must
not live in a tool-writable `Ctx` and must fail closed (A1); `ends_when`'s `ok` predicate is wrong
for the one tool the brief's own example applies it to, because `prove` returns `ok=True` on
failure (B2); a derived approval as specified outlives its scope check and lets an out-of-scope
commit land — demonstrated against the real `tools/commit.py` (C1); and "follow-on disposition" is
not deferrable under the brief's own rule, so §6 either does nothing or removes a stop through a
side door (D1). I would also take the E1+E2 simplification before implementing rather than after:
it satisfies the same two EJ decisions with three new mechanisms instead of ten, deletes the
`refused_by` enum problem, the dropped-call problem and the `invariants_checked` dishonesty outright
rather than fixing each, and puts the pause on the one bound this framework has already tested to
death. Re-review the revised §3–§6; §1, §2 and §9 can stand as written with A6's wording corrected.
