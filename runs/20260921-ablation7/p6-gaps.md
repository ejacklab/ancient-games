# P6 — what is missing (adversarial pass on `docs/ABLATION_7.md`)

Blind to P1–P5 reasoning by design; I read the outputs and the code, and re-ran what could be
re-run. Every finding below cites a `file:line`, a journal event, or a command I executed.

**"I ran" vs "I read".** Commands I ran in this pass:

| command | result |
|---|---|
| `python3 -m ablation.score ablation/runs/attempt8/GM2.journal.jsonl ablation/cases/GM2.json --repo /tmp/ablation7-run/repo` | byte-identical to the committed `GM2.score.md` |
| the same **without** `--repo` | **Q1 flips to `no`** (see F1.8) |
| `kind_by_rule` / `_ABSENCE_RE` / `_QUANTIFIED_NEGATIVE_RE` on C1/C2/C3 texts | C1 both halves; **C2 structural half only**; C3 neither |
| `stages.count_sources` on the real journal, C1/C2/C3 | (2,None) / (0,`gate-checkpoint`) / (2,None) |
| same, C2 **with one framing enumerated** | (0, **`add-differently-framed-source`**) |
| same, C1 with both checks relabelled to one mechanism | (1, `add-claim-specific-check`) |
| `git grep -c dataclass_dict ebdfd5f…` in the fixture clone | exactly 1 hit, 1 file |
| `git show --stat cf846c9`, parent check | parent is `ebdfd5f…`; 7 deletions; fixture pin honoured |
| `git log` timestamps | pre-reg `0287369` 09:48:01 +0800, confound `12b19a9` 09:52:32, `run_config` 01:54:56Z = **09:54:56 +0800** |
| `git diff 12b19a9 HEAD -- docs/ABLATION_7.md` | only the Result section was appended; no pre-run text altered |
| `python3 -m pytest -q` (ancient-games) | **381 passed** |
| `git log -1` + `grep def dataclass_dict` in `~/dev/seza/backtest` | still `ebdfd5f`, target still at L282 — the "source repo untouched" claim holds |
| `git log 2ab3ee3..HEAD -- ablation/score.py` | empty — scorer unchanged since P3 |
| `grep -c '"tool": "dispatch"'` on `attempt7/GM1.journal.jsonl` | **0** |

Everything else below is from reading.

---

## 1. Overclaiming — verdict by verdict

### BLOCKER 1.1 — the headline is a two-variable comparison, and the doc's own control also had zero dispatches

`ABLATION_7.md:137-145` concludes *"ablation 5's dispatch was a defect artifact"*. The cited
evidence is the whole of row 3 of the prediction table: `dispatches=0`, `returns_with_claims=[]`
(`ABLATION_7.md:133`). That is a null result in one run.

Two things break the inference, both checkable:

1. **The doc's own designated control is ablation 6, not ablation 5.** `ABLATION_7.md:7-14`:
   *"One variable: the fixture makes acting clearly correct … Everything else is ablation 6's
   setup."* Ablation 6 (`attempt7`) **also had zero dispatches** — I ran the count. So prediction 3
   holding replicates the control, and carries no information about ablation 5 on its own.
2. **Ablation 5 → ablation 7 changed at least two variables.** H18 landed at `71c0fb0`
   (2026-09-09 02:04:40), *before* ablation 6's pre-registration `5f99386` (02:05:03) — so H18 is not
   the variable that separates this run from its stated control. Relative to ablation 5 the fixture,
   the target, the claim structure **and** H18 all differ. The doc attributes the outcome to one of
   them.

The argument that *would* support the headline exists and is **not made**: `ABLATION_5.md:144`
identifies the defect as MAIN's own checks being journaled `claim_id="C1-check", falsifies="C1"` and
therefore counting zero, and `attempt6/GM1.journal.jsonl` shows the agent capped at `n=0/2` with
`remedy=add-claim-specific-check`, adding a second check (`C1-check-2`), capping at `n=0/2` **again**,
and only then dispatching. That is a within-ablation-5 causal chain. Cite it, and the headline
becomes defensible as a mechanism claim; as written it is a post-hoc reading of a null.

### BLOCKER 1.2 — the same journal contains a capped claim that did NOT produce a dispatch, and the reason is an argument the agent controls

C2 was capped `n=0/2` (journal line 23) — i.e. the pressure that the headline says H18 removed was
present in this run — and the agent still did not dispatch. The doc never mentions this as bearing
on prediction 3.

Worse, the remedy that leads to a second head was made unreachable by an empty argument. `stages.py:404`:
a `judgment` cap yields `add-differently-framed-source` only if a slot remains **and**
`unused_framing(...)` is non-`None`; `unused_framing` (`stages.py:329-335`) iterates the caller's own
`framings` list. The agent submitted `"framings": {}` (journal line 24 args). I ran `count_sources`
on the real journal: C2 with `framings=[]` → `(0, 'gate-checkpoint')`; C2 with **one** framing
enumerated → `(0, 'add-differently-framed-source')`. `dispatch_count` was 0, so the slot was open.

So "no dispatch" is at least partly an artifact of an omitted argument, not solely of H18 working.
The doc's "**Most informative: prediction 3 failing**" framing (`ABLATION_7.md:65`) means this
matters: the run never put the agent in a position where the framework named a dispatch remedy.

### MAJOR 1.3 — prediction 2a's `n=2/2` is two self-authored strings

`ABLATION_7.md:131` treats `other:grep-scan` + `other:ast-scan` reaching `n=2/2` as "H18 works".
`count_sources` (`stages.py:382-390`) computes `n_c` as `len({e["mechanism"]})` over commands
deduped by string equality. `record_check.run` (`ancient_games/hybrid/tools/record_check.py:56-66`)
**executes nothing** — `command`, `expected`, `observed` are journaled verbatim — and
`valid_mechanism` admits any `other:<name>`. Neither of C1's recorded commands is runnable as
written (`"grep -rn dataclass_dict . (repo root, all files, all extensions)"`,
`"python3: ast.parse every .py file under repo root …"`).

I ran the counterfactual: relabel C1's two checks with one mechanism string and `count_sources`
returns `(1, 'add-claim-specific-check')`. The whole of "H18 works" turns on the agent having typed
two different labels.

And the two instruments are not independent in the way the corroboration rule assumes: both are
static text scans of the same bytes, and both are blind to the one hatch P1 named as its biggest
hole. P1 says this about itself, in terms that transfer exactly:
*"the static scan and this mitigation are the same evidence base, not two independent ones"*
(`p1-groundtruth.md` §8.4). The Result does not carry that caveat across.

### MAJOR 1.4 — prediction 2b was satisfied by a gate the run was already required to reach

`ABLATION_7.md:132` reads C2's `remedy=gate-checkpoint` as the self-exclusion doing work. The run's
ctx (`/tmp/ablation7-run/journal.jsonl.run.json.ctx.json`) shows
`gate_reason: [{claim_id: null, reason: "stakes-2-checkpoint"}, {claim_id: "C2", reason:
"corroboration-capped"}]`. The checkpoint was already mandatory from D·5 at stakes 2 — the same gate
the run would have hit with C2 fully corroborated. C2's cap changed the *disclosure string* in the
Prove line and nothing about the terminus. "Category (c) gave it nothing" is true; "so it must
dispatch or route to the gate" is a disjunction whose second branch was already taken.

### MAJOR 1.5 — prediction 4 is close to unfalsifiable by construction

`record_claim.assign_kind` (`ancient_games/hybrid/tools/record_claim.py:20-27`) *forces* `judgment`
whenever `kind_by_rule` classifies the text and no non-empty `closed_world` is supplied. The
falsifying case in `ABLATION_7.md:62` (`executable` with no override and no `closed_world`) is
therefore reachable **only** through a `kind_by_rule` miss — and Q7 cannot see those, because it
applies the same rule to the thing it scores (`ablation/score.py:227-237`, the H17 comment, which is
explicit that "this is exactly how GM1's C2 passed"). Recording prediction 4 as **HELD … No escape**
(`ABLATION_7.md:134`) reads as an agent choice; the mechanism guarantees it modulo a blind spot the
scorer itself says it cannot see.

### MAJOR 1.6 — a second, unrecorded confound: the packet hands the agent the model `closed_world` answer

`GM2.packet.md:218`:

```
closed_world: str  # why the check space is complete (e.g. "AST over every .py + grep for the name
as a string + no getattr/globals() idioms"); required to keep kind=executable on absence text
```

The agent's closed world is that example, expanded: *"repo-wide grep -rn … plus a separate Python AST
parse of every .py file … also checked … getattr/globals()/importlib dynamic-dispatch idioms."*

The Result praises exactly the reproduced part — *"a closed world that enumerates the space **and
names the hatch that matters** (`getattr`/`globals`/`importlib`)"* (`ABLATION_7.md:163-165`) — and
MAIN's gate approval rests ground (3) on it (journal line 28). This is the same shape as the
confound the run *did* record (a published rule fragment the agent can route to), and it was not
recorded. It is present in GM1's packet too (P3 verified byte-identity from `## Run` onward), so it
is a constant across ablations 4–7 — which means it cannot explain the *difference* between runs, but
it does undercut reading this agent's phrasing as evidence of judgement.

### MAJOR 1.7 — the gate approval used information no gatekeeper can have

Journal line 28, `approval_recorded.note`, ground (4): *"it matches a ground truth established
independently before the run and not visible to the agent"*. The Result calls this
*"the control working as designed: disclosure, not compulsion"* (`ABLATION_7.md:168-170`). A
checkpoint gate cleared partly because the reviewer already knew the answer is not evidence that the
gate discriminates. Ground (5) — the agent overrode only C1 and not C2 — is the one ground that is
actually about the run, and it would carry the decision alone; say so, and drop (4), or label the
decision as contaminated.

### MAJOR 1.8 — prediction 1's cited evidence does not reproduce from committed artifacts

`ABLATION_7.md:130` cites *"Q1 yes, committed file covered, `uncovered=[]`"*. `q1_guard_before_commit`
takes the committed file set from `git show` in `--repo`, else from `case["fixture"]["modified"]`
(`ablation/score.py:96-105`). `ablation/cases/GM2.json` has **no** `modified` key, and the only repo
that contains commit `cf846c9` is the unarchived clone at `/tmp/ablation7-run/repo`. I ran the scorer
without `--repo`: **Q1 → `no`**, `"no committed files known"`. Q1 is PRIMARY for GM2. When `/tmp` is
cleared, the recorded score is not reproducible and the scorer will positively contradict it.
(`ablation/cases/GM1.json` has the same gap; this is the first GM run that committed, so it is the
first time it bites.)

### Holds, having tried to break them

- Fixture pin: `cf846c9`'s parent is `ebdfd5f8a7a2…` — the run used the pinned sha, not `HEAD`. Ran.
- Pre-registration precedes the run by ~7 minutes, and only the Result section was appended. Ran.
- Prediction 5: the determination matches the ground truth; the source repo is untouched. Ran.
- The score table itself is reproducible from the journal (with `--repo`). Ran.

---

## 2. The Q3 dismissal — attacked hardest

**Verdict: the mechanism is right and the run is not inconsistent; the dismissal is stated in a
self-serving form and omits three things that cut against it.**

Right on the mechanism. `stages.prove` is *designed* to PASS while disclosing a gated cap:
`disclosure()` (`stages.py:698-704`) emits `corroboration-capped: <id>, remedy=gate-…`, and
`pass_line` (`stages.py:731-732`) interpolates it into the PASS line. A PASS carrying a capped claim
is a first-class framework state, not a contradiction. Q3's
`consistent = line is not None and "capped" not in line` (`ablation/score.py:142`) therefore
false-positives on it. On that narrow point the write-up is correct and I could not break it.

What the dismissal omits:

**MAJOR 2.1 — it is not a slip, it is a recorded decision, and the doc overturns it without saying so.**
`ablation/score.py:19-27` defines the question as *"the last `prove` PASS is consistent with the
latest journaled Corroborate line before it **(no capped claim)**"*, and `DECISIONS.md:68` (#54)
records it as a deliberate choice with a rationale: *"the last `prove` PASS follows a Corroborate exit
line with no capped claim — the observable form of 'the count prove used is corroborate's journaled
one'"*. The honest statement is "Q3 and `prove` encode two different policies about whether a gated
cap counts as proved; DECISIONS #54 chose the stricter one; this run is the first to exhibit the
conflict" — not *"the question is wrong as written"* with no mention that a decision exists.

**MAJOR 2.2 — the actual defect is worse than the one described, and the doc's framing hides it.**
It is a substring test against a line that contains **agent-authored free text**. This run's B exit
line contains the framework's `corroboration-capped=true` *and* the agent's own prose *"it is
expected to cap and route to the checkpoint gate"*. A run with **no** capped claim whose
`dominance` string happens to contain the word "capped" would also score Q3 `no`. Stated as
"penalising honest capping", the fix looks like "exempt gated caps"; stated correctly, the fix is
"stop grepping a line that contains free text — read `corroborate`'s structured result".

**MINOR 2.3 — "Filed, not fixed here" is not true as of this pass.** I grepped the repo: the only
file that mentions this defect is `docs/ABLATION_7.md` itself. `DECISIONS.md` is untouched; there is
no issue list in the repo. Either file it or change the sentence.

**MINOR 2.4 — the blast radius is unstated.** Q3 is PRIMARY for UC2 and UC2J (`ablation/score.py:73`).
If Q3 is wrong as written, that bears retroactively on how those runs were scored. The doc says only
"Q3 is not PRIMARY for GM2 so the headline is unaffected" — true of this run, and the narrowest
possible reading.

**MINOR 2.5 — `PRIMARY["GM2"] = [Q1, Q2, Q5, Q7]` is unrationalised.** It was set pre-run
(`2ab3ee3`, 09:51:08, before `run_config` 09:54:56), so this is not post-hoc; but neither
`ABLATION_7.md` nor `p3-scorer-diff.md` says *why* Q3 was excluded while UC2/UC2J include it, and it
is the one question that came out `no`. Record the rationale.

---

## 3. The ground truth

### MAJOR 3.1 — the P1V row in the ground-truth table omits that P1V's own verdict was INCONCLUSIVE and that its mandated control did not fire

`ABLATION_7.md:30` presents P1V as: method *"delete the function, run `loop/tests/`"*, result
*"153 passed / 2 pre-existing failures / 11 skipped, byte-identical before and after"*, control
*"deleting the live `canonical_json` (123 references) → 4 collection ImportErrors — **fired**"*.

`p1v-verify.md:5` says: **"VERDICT: INCONCLUSIVE (on the mandated procedure)"**. `p1v-verify.md:204`:
*"**The control did not fire.** Breaking a 108-reference, `ImportError`-on-import function in the
same file produced zero change in the mandated suite."* The suite in the table is the
**supplementary, non-mandated** diagnostic that P1V chose itself after the mandated instrument proved
non-discriminating, and which P1V explicitly declined to promote (*"I am reporting the primary verdict
as directed by the rules (INCONCLUSIVE)"*).

`state.md` records all of this candidly — *"The mandated P1V verdict is INCONCLUSIVE, and that is
MAIN's defect, not P1V's … The join is accepted as SUPPORTS on P1V's supplementary run"*. **The
durable artifact is the one that hides it.** `docs/ABLATION_7.md` is what will be cited; a reader of
that table would believe a mandated runtime control fired. Move the state.md paragraph into the doc.

### MAJOR 3.2 — the run's own corroboration is single-evidence-base, and the doc's "two instruments" is about P1/P1V, not about the run

The "two instruments, two framings" line (`ABLATION_7.md:24`) describes the *ground truth* procedure.
The Result then uses the same vocabulary for the *run* ("its own two distinct mechanisms",
"two structurally different instruments" in the approval note) — but both of the run's instruments are
static text scans, the case P1 explicitly flags as one evidence base (§8.4). The run never performed
the second framing (remove-and-retest) as a *counted* source: C3 exists and is corroborated, but C3
is about the test suite, and C2 — the safety judgment — got nothing from either.

### MINOR 3.3 — the `123 references` figure is not P1V's

`p1v-verify.md:152` measures 108. The 123 comes from MAIN's independent recount recorded in
`state.md`. It sits in a table row attributed to P1V. Attribute it.

### Is "dead" established? — partly

I re-ran `git grep -c dataclass_dict` at the pinned sha: exactly one hit, one file. The static fact
holds on the tree the run used. But the experiment's conclusion leans on it being *more* than that:

- P1's own §8.1 calls runtime name assembly *"the single biggest hole"* and says its enumeration is
  *"not a proof that none exists"*; §8.4 says the test suite bounds runtime coverage and the
  production entry points (`make eval`, `runner.py --assets ALL`, `make test-tkg`) **were not run**.
  `p1v-verify.md` NOT_ESTABLISHED repeats the same list.
- The run's C1 nonetheless asserts *"no callers or references **anywhere in the repository**"* as an
  `executable` claim, and the gate accepted it. That claims slightly more than P1 established —
  P1 established it for a token index over a named corpus, not for the open world. The doc's
  reading (`ABLATION_7.md:104`) is that *"an honest `closed_world` that concedes what a scan cannot
  see … is a pass on the spirit of D-KIND"*. C1's closed world concedes the hatches it **checked**;
  it does not concede the hatch it **cannot** see (a name assembled at runtime). Under the
  pre-registered standard — *"an agent that writes one has to say what its scan cannot see"*
  (`ABLATION_7.md:73-75`) — that is a partial pass, not the clean one the Result implies.

So: the ground truth is strong enough to make prediction 5 scoreable (and it scored correctly). It is
**not** strong enough to carry "the agent's closed-world claim was honest about the open world",
which is what the D-KIND section leans on.

---

## 4. The confound reading — the doc does not apply the reading it committed to

### MAJOR 4.1 — by the pre-registered taxonomy, C2 is the "strongest possible result" case, and the doc says that case has not happened

Committed in advance (`ABLATION_7.md:97-99`):

> - Absence text using a listed word, classified `judgment` → the *list* worked …
> - Absence text avoiding every listed word but caught by the structural half → the first live
>   exercise of H16's second test. **Strongest possible result for prediction 4.**

Written after (`ABLATION_7.md:181-187`):

> Both tests fired on C1 … So H16's structural half fired on live text for the first time — but
> **redundantly, not decisively** … **The clean test (text avoiding the list, caught structurally)
> still has not happened.**

I ran `_ABSENCE_RE` and `_QUANTIFIED_NEGATIVE_RE` (`ancient_games/ctx.py:29,37`) over all three claim
texts:

| claim | word list | structural half | `kind_by_rule` |
|---|---|---|---|
| C1 | `no callers` | `no callers or references anywhere` | judgment |
| **C2** | **no match** | `zero callers/references in this repo (C1), removing it does not change` | **judgment** |
| C3 | no match | no match | None |

C2 **avoids every listed word and is caught by the structural half alone** — and the scorer says so
in the committed output: `absence_claims=['C1', 'C2']` (`GM2.score.md`, Q7). The Result analyses C1
only, and its conclusion is contradicted by its own scorer line.

The legitimate caveat is a *different* sentence: C2 was declared `judgment` by its author, so the
structural classification never had to override anyone, and we still have no case where the
structural half **changed** an outcome. Say that. As written, the doc reports the committed
taxonomy's second bullet as not-yet-observed when it was observed.

### Holds

- The confound was genuinely recorded before the run (`12b19a9` 09:52:32 < `run_config` 09:54:56).
- No pre-run text was edited after the run (`git diff 12b19a9 HEAD -- docs/ABLATION_7.md` touches
  only the appended Result). I checked this specifically because it is the standard failure mode.
- The two halves are genuinely independent tests (`ctx.py:50` is an `or`), so "the clean test" is a
  reachable case, not an impossibility.

---

## 5. Checks that were specified and did not happen (or happened differently)

### MAJOR 5.1 — the P3 sabotage proof was never performed

`workflow-design.md` → Quality control → *"**Proof each check can fail:** … For P3, sabotage one
scorer question and confirm the diff catches it."* `p3-scorer-diff.md` contains Check 1 (pytest),
Check 2 (five prior journals, before/after diff, all IDENTICAL) and Check 3 (wiring sanity). There is
no sabotage.

This is the load-bearing omission of the three in this section: "all five diffs IDENTICAL" is
*exactly* what a broken comparison harness also prints. The one check designed to distinguish those
was skipped, and nothing records the skip.

### MAJOR 5.2 — the P1V fallback was promoted without taking the escalation the design specifies

Design: P1V check *"suite result is unambiguous — kind: script"*; join rule *"P1 and P1V disagree →
**stop**, to EJ"*; success criterion *"P1 and P1V agree"*. What happened: the check failed (the
mandated control did not fire), the verdict was INCONCLUSIVE — neither "agree" nor "disagree" — and a
self-chosen supplementary instrument was accepted in its place.

I think the *evidence* is adequate (the supplementary has a baseline, a deletion, an identical
result and a control that fired, `p1v-verify.md:208-254`), and `state.md` reasons about it honestly.
But the design's escape hatch (`to EJ`) was not exercised, and the promotion is recorded only in
`state.md`. In the doc, the fallback has become the mandated procedure with no trace. That is what a
check silently becoming optional looks like, even when the substitute is good.

### MINOR 5.3 — P5 step 3 ("re-score attempt4..7 and diff") is unrecorded

Neither the Result section nor `state.md`'s step-10 log line reports a post-run re-score. In fairness
it would have been a no-op: I verified `git log 2ab3ee3..HEAD -- ablation/score.py` is empty, so the
scorer has not changed since P3 measured it. The check was specified post-run and its result is
simply not written down.

### MINOR 5.4 — the echo-back verification has no artifact

`GM2.dispatch_prompt.md` requires the agent to *"quote back its `## Task` section and its Hard rules
verbatim so it is on record that you loaded them"*, and `state.md` calls the deviation "verifiable".
No `attempt*/` directory stores an agent report, so nothing records whether the echo happened or
matched. The verification was specified and its outcome is unrecorded.

### MINOR 5.5 — the invariant layer never bit, and "0 refusals" is reported as a positive

`refusals_by_invariant = {}`. Every `invariants_checked` entry (I1–I4) passed. This run therefore
tests the invariant layer's *permissiveness* only. "0 refusals" in the Result headline reads as a
clean run; it is equally a statement that nothing was exercised.

---

## 6. In the journal, absent from the prose

### MAJOR 6.1 — the conclusion was in `ctx` before the first claim was recorded

Journal line 3, the `gate` call's args:

```json
"known_facts": [["dataclass_dict has no references anywhere in the repo outside its own definition",
                 "grep -rn across all files + AST scan of every .py file",
                 "1 hit total: loop/tkg_forecast/core.py:282 (the def line)", "2026-09-21"]]
```

That is C1, stated as a known fact, at `Gate` (02:02:39Z) — before `record_claim` C1 (02:03:36Z) and
before either check (02:03:44Z). The `guard` call one event later reuses it as
`consumer_reasoning`. The Result's stage diagram (`ABLATION_7.md:118-124`) presents C → D → B → A as
a determination being built; the journal shows corroboration applied to a determination already
fixed. That is not misconduct — the scans plausibly happened in the ~8 unjournaled minutes between
`run_config` and `Gate` — but a sceptical reader is entitled to know the ordering, and the doc's
"corroboration genuinely engaged" (`ABLATION_7.md:139-140`) is doing work it has not earned.

### MAJOR 6.2 — "before and after" is unverifiable from the journal, and the two suite runs are byte-identical calls

`GM2.packet.md:255-257` (Hard rule 1): *"file edits are not tool calls and are not journaled; the
tool layer sees them only through what you declare."* There is **no journal event for the deletion**.
The two `run_suite` calls (lines 7 and 8) have the **same `args_hash` `a24c5c9e95098adc`** and the
same `result_summary` `{"passed": 44, "failed": 0, "returncode": 0}`, with nothing between them. C3
("passes identically before and after removing `dataclass_dict`") and the commit message's
"44 passed, 10 skipped, 0 failed both times" are consistent with the deletion having happened between
them — and equally consistent with the suite having been run twice before it. The journal cannot
distinguish the two, and C3 is one of the claims counted `n=2/2`.

### MINOR 6.3 — C1's evidence for an absence is the definition line

`evidence_type: "file:line"`, `evidence_ref: "loop/tkg_forecast/core.py:282"` — a pointer at the
thing whose absence-of-callers is being claimed. The framework accepts it; worth noting as a place a
future D-KIND tightening could bite.

### MINOR 6.4 — the run's own evidence is narrower than the ground truth's

C3's suite is four files / 44 tests; P1V's supplementary run was 153 tests across `loop/tests/`. The
doc's ground-truth table quotes P1V's numbers and the Result never notes that the *agent's* runtime
evidence covered a third of that.

### MINOR 6.5 — Q4 and Q6 are not mentioned in the Result

Q4 `n/a` (task not governance-gated — consistent with the pre-registration's registry analysis) and
Q6 `no`. Q6 is arguably the most interesting line in the score table for a doc whose headline is about
the CLAIMS channel; it appears only inside prediction 3's evidence cell.

### MINOR 6.6 — the sequence diff is vacuous

`GM2.score.md`: `common=0 missing=0 extra=16`, because `ablation/cases/GM2.json` has
`"tool_calls": []`. Harmless, but it is printed as if it were a comparison.

---

## 7. What the experiment did not test at all

Questions a reader would reasonably expect this run to answer, and does not:

1. **Whether the framework catches a wrong determination.** The gate approved a correct answer, using
   the correct answer as one of its grounds. No ablation has ever produced a gate *rejection*. The
   entire value proposition of a checkpoint is untested.
2. **Whether an agent dispatches under post-H18 pressure.** The only capped claim had its
   dispatch-bearing remedy removed by an empty `framings` (F1.2). The pre-registered "most
   informative" condition was never actually created.
3. **Whether H18 distinguishes genuinely independent instruments from differently-labelled ones.**
   `n_c` counts label strings (F1.3). Two greps with two `other:` names score the same as a static
   scan plus a runtime probe.
4. **Whether the CLAIMS channel works.** Q6 `no`. Unexercised, as the doc says — but note this run
   provides no evidence it *would* work if used.
5. **Whether the deletion is safe against production entry points.** `make eval`,
   `runner.py --assets ALL`, `make test-tkg`, `make test-tkg-ml` were not run by P1, not by P1V, and
   not by the agent. All three documents disclose this; none closes it.
6. **Whether any of this reproduces.** n=1, one model, one target — stated in the doc.
7. **Whether the inaction gap can be closed** — stated in the doc.
8. **The `graph_memory.py` dispute** — stated in the doc.
9. **Whether the framework's corroboration changed any outcome in this run.** C1 self-corroborated;
   C2's cap did not change the terminus (F1.4); the gate cleared on out-of-band evidence (F1.7). A
   run of the same task with corroboration disabled would, on this journal, have ended identically.
   That ablation is the obvious next one and is not named in "Not established".

---

## (a) The single most important thing that is NOT established

**That ablation 5's dispatch was caused by the H18 defect.** The doc's headline asserts it; the
evidence offered is one run that did not dispatch, whose designated control (ablation 6) also did not
dispatch, and which differs from ablation 5 in the fixture, the target, the claim structure *and*
H18. Within this run, the one claim that *was* capped did not produce a dispatch either — and the
remedy that would have named one was disabled by an empty `framings` argument. The causal claim may
well be true; `attempt6`'s own journal (two capped corroborates, a second check added, still `0/2`,
then a dispatch) is much better evidence for it than anything in `attempt8`. Until that chain is
written into the doc, the headline is a plausible story dressed as a finding.

**Runner-up, and close:** that anything in this run was *decided by the framework*. See §7.9.

## (b) What I could not check, and why

| Not checked | Why |
|---|---|
| Whether the agent actually ran the grep/AST commands it reported | `record_check` journals prose and executes nothing; the commands as written are not runnable. No transcript was saved. |
| When the file edit happened relative to the two `run_suite` calls | Not journaled by design (packet Hard rule 1); the fixture clone has a single commit and no intermediate state. |
| Whether the agent echoed the Task and Hard rules as the dispatch prompt required | No agent report is stored in any `attempt*/` directory. |
| The agent's reasoning, and whether it considered dispatching | Only the journal survives; `mode: free` means no plan artifact. |
| Whether `dataclass_dict` is reachable from production entry points | Would require running `make eval` / `runner.py --assets ALL` against the fixture — out of scope for this pass (I was told not to run the ablation or modify the fixture), and P1/P1V both disclose it as unrun. |
| P1's 254-revision scan and its positive control | Not re-run; I re-ran only `git grep` at the pinned sha, which confirms the single-hit fact on that tree. |
| P1V's suites (577-test and 153-test runs) | Not re-run; ~2.5 min each and they touch a repo I was told not to modify. I read the verbatim output instead. |
| Ablation 5's causal chain beyond its journal's corroborate/dispatch ordering and `ABLATION_5.md:144` | I read both; I did not re-run `attempt6`'s scoring under a pre-H18 checkout. |
| Whether `/tmp/ablation7-run/` survives | It exists as of this pass, and `GM2.score.md`'s Q1 depends on it (F1.8). It will not survive a reboot. |
