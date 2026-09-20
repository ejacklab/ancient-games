# The D-KIND mirror hole — what it actually is, and four ways to close it

Research, not a design. Everything below was measured against `3305896` (F1–F5 landed, 351 tests
green). Reproduction scripts are inline; each finding names the command that produced it.

**Scope note.** `docs/INTERFACE_FIXES_IMPL.md` left this out deliberately: "`ingest_return` still
accepts a dispatched agent's self-declared claim *kind* (D-KIND's remaining hole). F1 narrows the
neighbouring surface — forging now costs a journaled, I5-capped dispatch instead of a typed string —
without closing it." This document establishes what the hole is worth before anyone writes the fix.

---

## 1. What D-KIND is for

`docs/ABLATION_2.md`, the design finding: UC2J's actor claimed "these helpers are dead" — an
open-world absence claim — and declared it `executable`, "which made two of its own checks
sufficient under Y2′." The finding is precise about the mechanism:

> This is not a count being smuggled — I3 held — it is the *kind* being chosen so the count is cheap.

`kind` is load-bearing in exactly one place, `stages.count_sources` category (c): the actor's own
`check_executed` events count, once per distinct mechanism, **only when `kind == "executable"`**. A
`judgment` claim gets nothing from its own checks and needs a differently-framed second head (a) or
a human gate.

The v1.4 fix (`record_claim.assign_kind`): absence text (`ctx.ABSENCE_PATTERNS`) is `judgment` by
rule; the author keeps `executable` only with a non-empty `closed_world` reason; that override sets
`kind_override=True` and is **disclosed** — `commit`'s checkpoint refusal names it verbatim,
`render_trace` tabulates it, `index` stores it, and `autonomy.live_grant` refuses to commit under a
pre-authorisation whose `allow_kind_overrides` is false. The CLI help for that flag states the
intent: "OFF by default: it turns a pre-commit disclosure into a post-commit review."

Every one of those four consumers keys on `journal.kind_overrides()`, which selects
`claim_recorded` events with `kind_override=True`.

---

## 2. The hole is a control bypass, not an omission

`record_claim.run` calls `assign_kind`. `journal.ingest_return` (journal.py:271) passes `c["kind"]`
straight into `claim_recorded` — no rule, no `closed_world` requirement, no `kind_override` flag.
Same claim, same text, same declared kind, both paths:

```
record_claim   -> kind = judgment    kind_override = False   closed_world = None
ingest_return  -> kind = executable  kind_override = False   closed_world = None
```

Because `kind_override` stays `False`, the claim is invisible to all four disclosure consumers. The
consequence, run end to end against a real git fixture with an owner grant of
`allow_kind_overrides: false` and one changed file:

| path | recorded | `kind_overrides()` sees | `commit` |
|---|---|---|---|
| A — MAIN, `executable` + written `closed_world` | executable, override=True | 1 | **refused**: `checkpoint-not-cleared; kind overrides for the gate to accept or reject: C1 (executable by closed_world: 'AST over every .py …'); no live pre-authorisation: grant:1: run carries a closed_world kind override and allow_kind_overrides is false` |
| B — dispatched agent returns the identical claim, `executable`, no reason | executable, override=False | 0 | **committed** `f093f47` |

Read that table twice. The path that **discloses** the override, in writing, is blocked. The path
that asserts the same thing **silently, with no justification at all**, commits unattended. The
mechanism does not merely fail to catch the agent — it penalises disclosure and rewards silence.

An owner who writes `--scope-path ... ` without `--allow-kind-overrides` believes no D-KIND override
can reach an unattended commit. That belief is false today.

*(Reproduction: `$CLAUDE_JOB_DIR/tmp/dkind_bypass.py`, two runs over `fixtures.make_uc2`.)*

### 2.1 The self-certification is cheaper than the forge F1 just closed

At stakes 3, one dispatch plus **one** `ingest_return` call reaches full corroboration with no other
participant:

```
CLAIMS = [ C1  kind=executable  "the helpers are dead",
           C1  falsifies=C1  mechanism=other:ast-scan     expected/observed,
           C1  falsifies=C1  mechanism=other:grep-sweep   expected/observed,
           C1  falsifies=C1  mechanism=other:import-probe expected/observed ]

-> Corroborate: C1: n=3/3; reconciled=agree.
```

`actor == author == adv-1`, so categories (a) and (b) contribute **zero**. The entire count is (c),
unlocked by the self-declared `kind` and multiplied by three self-chosen `other:` mechanism labels.

The mechanism multiplication itself is **by design** and is not a defect: §4 B·1 (c) says checks
count "regardless of who ran it", `other:<name>` is deliberately open, and Z5′ already dedups
identical commands. That is precisely why `kind` carries the whole load — it is the only thing
standing between "this claim needs a second head" and "this claim can be self-certified by running
more commands with different labels."

### 2.2 The same function leaks two more defects of the shape F2 just fixed

`ingest_return` mirrors `record_check` as well, and that mirror is unguarded too:

```
record_check  bad mechanism -> exit 2, "invalid-args: mechanism must be one of …"
ingest_return bad mechanism -> exit 0, "internal-error: check_executed.mechanism must be one of …"
```

That is F2's defect verbatim — a caller error reporting success — surviving in the mirror. Same for
`expected`/`observed` types.

And the writes are not atomic. A three-entry CLAIMS list whose third entry is invalid:

```
tool result: ok=False   internal-error: check_executed.mechanism must be …
journal now holds: ['dispatch', 'return', 'claim_recorded', 'claim_recorded']
```

The caller is told the call failed while two claims and the `return` event are already on disk. A
retry duplicates them. F1's author guard was deliberately placed *before* `journal.ingest_return`
for exactly this reason; per-entry errors still fall inside it.

### 2.3 Blast radius: the path has never fired in a live run

Every `*.jsonl` in the repo, scanned: **2 `return` events, 0 CLAIMS entries, 0 claims that would
reclassify.** The two live returns (`ablation/runs/attempt4/UC3`) carry ad-hoc fields —
`strongest_attack`, `verdict`, `factual_errors`, `bears_on_C4` — and no `CLAIMS` key at all. The
agent's claims were recorded separately, by MAIN, under MAIN's own authorship (confirmed by F1's
replay test: authors ⊆ {MAIN} for every stored journal).

Two consequences, pulling in opposite directions:

- **Urgency is low.** No stored result changes; no live behaviour regresses. There is no fire.
- **Confidence is low too.** This is spec'd, shipped, unit-tested code that free agents have never
  exercised. It is not battle-tested; it is untouched. Its first real use would be the test.

It also means the *historic practice* — MAIN re-recording an agent's claims under its own name — is
already the shape of the strictest option below, adopted informally by two free agents.

---

## 3. One tempting option, and why it is wrong

**"Stop asking. Derive `kind` from the journal."** A claim is executable iff a
`check_executed{claim_id=X, falsifies=X}` exists naming a concrete `expected` the observation could
have missed — `journal.classify_event` already does something of this shape for routing evidence.
Nobody declares anything; the journal's own contents decide; the self-declaration disappears from
the trust boundary entirely.

It fails on the actual case. UC2J's agent **did** run checks with concrete expected values. Its
checks were real; they simply did not close the space — nothing in `loop/program_db.py` reported a
caller, and reflective idioms were never enumerated. Derivation-from-checks would classify UC2J
`executable`, which is the answer D-KIND exists to prevent.

The generalisation worth keeping: **executability is a claim about coverage of a space, and coverage
is not observable from the journal.** That is why `closed_world` is prose read by a human, and why
`ABLATION_2` calls the keyword rule "a keyword floor, not a proof". No mechanical classifier can
close this hole. Every viable option is about *who attests* and *where the attestation is disclosed*
— never about computing the answer.

---

## 4. The options

### Option 1 — port the rule (minimal, symmetric)
`ingest_return` applies `assign_kind` per CLAIMS entry; an agent keeps `executable` on rule-matched
text only by supplying `closed_world` in the entry; `kind_override` is set accordingly.

- **Restores all four disclosure consumers.** `kind_overrides()` already returns `author`, so the
  gate reads "adv-1 (executable by closed_world: '…')" and knows whose word it is.
- Strictly narrows today's authority: an agent's override now *blocks* an `allow_kind_overrides:
  false` grant instead of sailing past it.
- ~10 lines, reuses a tested helper. Zero stored-data impact (§2.3).
- **Cost:** a dispatched agent can mint an override MAIN never wrote. Disclosed, attributed, and
  gate-controlled — but under `--allow-kind-overrides` it would clear an unattended commit on the
  agent's own prose.

### Option 2 — returns may not mint an override (strictest)
An agent's returned claim is never `executable` on rule-matched text, full stop. If MAIN wants
executable, MAIN records it with MAIN's own `closed_world`.

- The authority to declare a check space closed stays with the party accountable at the gate.
- Codifies what both free agents already did (§2.3), so the friction is theoretical.
- **Cost:** the agent's reasoning has no channel and is silently dropped, unless paired with
  Option 4. Loses information the human might have wanted.

### Option 3 — derive `kind` mechanically
Rejected in §3. Recorded so it is not re-proposed.

### Option 4 — agent proposes, MAIN countersigns
Record as `judgment`, and journal a `deferred_decision{kind: "kind-override-proposed", payload:
<the agent's reason>}`. MAIN either re-records with its own `closed_world` or leaves it.

- Uses machinery that already exists and is already used for this exact concept: `commit.py:83`
  writes `deferred_decision{kind: "kind-override"}` when a grant let an override through unread, and
  `cli.cmd_queue` / `done` / `status` already refuse to call a run finished while a deferral stands.
- Nothing lost, no authority granted, and the "disclosure with nobody reading it" case already has a
  home.
- **Cost:** more moving parts than 1 or 2; needs a payload shape decision.

### Option 5 — dissolve the mirror (structural)
Stop having two writers. `journal.ingest_return` stops mirroring; `ingest_return.run` appends the
`return` event and then delegates each CLAIMS entry to `record_claim.run` / `record_check.run` — the
guarded writers — routed by `classify_event` as today.

- Every guard written once, at one site, and every future guard inherited for free. The F1 author
  gate, the F2 validators, D-KIND's rule and anything added later apply to returns by construction
  rather than by remembering.
- Lets F1's AST pin shrink from two sanctioned `claim_recorded` writers to one, which is a stronger
  invariant than the pin itself.
- Fixes §2.2's exit code (delegation returns `invalid-args`) as a side effect.
- **Cost:** to also fix atomicity, `record_claim` and `record_check` need their validation split from
  their write — `validate(args) -> ToolResult | None`, with `run = validate + write`. `corroborate`
  already has exactly this shape (`_validate`), so it is a conformance move, not an invention.
  Larger than 1–4, and it touches three tools instead of one.

---

## 5. Recommendation

**Option 5, carrying Option 1's policy** — and, if the owner wants the stricter answer,
Option 2+4 is a policy change on top of the same structure rather than a different structure.

The reasoning is the repeat-offender count, not elegance. `journal.ingest_return` is now the site of
**three** defects of one shape: the author was unguarded (F1, fixed), the `kind` is unguarded (this
document), and the field validation is unguarded with a partial write on failure (§2.2). Three
instances is where patching the third one stops being the cheaper move. The mirror exists so that
returns write the same events as the direct tools; it should therefore *call* those tools, not
reimplement the half of them that is convenient.

The urgency argument cuts the same way. §2.3 says nothing is on fire and no stored result moves, so
there is no reason to take the fast patch over the right one.

Suggested sequence, one commit each, in the house style (each ends green, each independently
revertible):

1. **5a** — split `validate` from `run` in `record_claim` and `record_check`. Pure refactor; the
   existing F1/F2 tests must pass untouched, which is the proof it changed nothing.
2. **5b** — `ingest_return.run` validates every CLAIMS entry up front, then writes: the `return`
   event and every mirrored claim, or nothing. Pins §2.2's partial write with a test.
3. **5c** — delete the `journal.ingest_return` mirror; delegate to the guarded writers. Shrink the
   F1 AST pin to a single sanctioned writer.
4. **5d** — the policy decision below, applied at the one remaining site.

Steps 1–3 are mechanical and owner-neutral. Step 4 is the only one needing ratification.

---

## 6. The question for the owner

**May a dispatched agent mint a D-KIND override at all?**

- *Yes, with a written `closed_world`* (Option 1) — the gate sees it, attributed to the agent, and
  `allow_kind_overrides: false` blocks it. Cheapest, strictly better than today.
- *No; MAIN countersigns* (Option 2+4) — matches what both free agents actually did, keeps the
  attestation with the party at the gate, and queues the agent's reasoning rather than dropping it.

Neither is a code question. Both sit on the same structure from §5, so **5a–5c can proceed before
this is decided.**

Secondary, and genuinely open: should `record_check`'s `other:<name>` mechanism labels stay
unbounded? §2.1 shows three self-chosen labels are three sources for an executable claim. That is
the spec's deliberate choice (B·1 (c), "regardless of who ran it") and is *only* dangerous when
`kind` is wrong — so it needs no action if D-KIND holds on every path. Flagged, not proposed.

---

## 7. What would change the recommendation

- **A live run that uses the CLAIMS channel.** §2.3's "never fired" is the load-bearing fact behind
  "no fire, do it properly". One free-agent run that actually returns CLAIMS would make the fast
  patch (Option 1 alone) the right call, and 5a–5c a follow-up.
- **`record_claim`/`record_check` growing per-call state.** The delegation in 5c assumes both are
  pure functions of `(env, args)`. They are today.
- **A decision to let agents write events directly**, rather than through MAIN's tool calls, would
  make the mirror the right abstraction after all and this whole document moot.


---

## 8. Outcome (landed)

Ratified by the owner: **helpers may override, only in writing** (Option 1's policy), on
**Option 5's structure** (one door). Landed as `5a` and `5b/5c/5d`.

`journal.ingest_return` is gone; `journal.returned` writes the `return` event and nothing else.
`hybrid/tools/ingest_return` classifies each CLAIMS entry with `classify_event` and delegates it to
`record_claim.run` / `record_check.run` — the guarded writers — after validating the **whole batch**.
There is now exactly one writer of `claim_recorded` in the tree, and F1's AST pin says so.

What §2's table looks like now, from the same reproduction script:

| path | recorded | `commit` |
|---|---|---|
| A — MAIN, `executable` + written reason | executable, override | refused by the grant |
| B — helper, `executable`, no reason | **judgment**, no override | commits (nothing is being claimed as self-sufficient) |
| C — helper, `executable` + written reason | executable, override, author `adv-1` | **refused by the same grant** |

A and C are now identical, which is the point: the honest path and the silent path get the same
answer, and the silent path no longer buys a cheaper count.

§2.1's self-certification collapses with it — the same one-dispatch, one-call sequence that reached
`n=3/3`:

```
before: Corroborate: C1: n=3/3; reconciled=agree.
after:  Corroborate: C1: n=0/3, capped, remedy=gate-owner; reconciled=agree, corroboration-capped=true.
```

§2.2's two adjacent defects are fixed as a side effect of delegating: a bad field is now
`invalid-args: fields.CLAIMS[i].<field>` and exits 2, and a bad entry anywhere in the list writes
nothing at all — not even the `return` event.

**Not done, deliberately:** §6's secondary question (unbounded `other:<name>` mechanism labels) needs
no action while D-KIND holds on every path, which it now does. §2.3 still stands — the CLAIMS channel
has never fired in a live run, so its first real use remains its first real test.
