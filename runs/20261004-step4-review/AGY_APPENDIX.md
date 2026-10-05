
---

# APPENDIX — inlined evidence (you have NO tools this run)

Tool use is unavailable in this session: agy headless auto-denied `read_file` and produced nothing. Every
excerpt the checklist needs is inlined below, verbatim, with its file:line. Treat these excerpts as your
evidence base and make zero tool calls. Where a check needs a fact not inlined, say so under section 5.

## A1. `docs/WORKFLOW_DESIGN_DIAGRAM.md` lines 36-43 (the third copy of the rule)
```
  EXP --> JOIN
  JOIN --> S4{"4 SIZE, 3.4<br/>up to 3 steps, and nothing unclear<br/>except decisions that have a default?"}
  S4 -->|"yes"| PF2["a prompt file, questions at the top.<br/>risk is judged separately from size:<br/>tiny but risky gets one independent check"]
  S4 -->|"more than 3 steps"| SPLIT["consider a new piece. split only if each part<br/>keeps its own check AND the split changes<br/>how the work is done"]
  S4 -->|"a spot of kind information or unknown,<br/>or a blueprint section missing or incomplete"| DESIGN["a workflow design, always"]
  SPLIT --> S5
  DESIGN --> DF["DEFAULT-FIRST, 3.4<br/>each piece's category row or pipeline in TASK_TYPES.md supplies<br/>pattern, engine, check, sabotage. a CHALLENGER design replaces it<br/>only on a written ≥20%-lower-projected-cost claim AT EQUAL COVERAGE<br/>(coverage is a gate, never an axis). reviewed by design_gate.py (script)<br/>+ one blind checklist pass (sonnet 5.5; different kind when it builds).<br/>every run reconciles its claim in TASK_TYPES_LEDGER.md — n=0 until it fills"]
  DF --> S5["5 CLEAR PIECES RUN AS LOOPS, 3.5<br/>diagram 3. they run WHILE the unclear<br/>spots are still being resolved"]
```

## A2. `docs/TASK_TYPES.md` — the category table header and all rows (lines 84-103)
```
(read-only). Round-1 lesson: a binary column made every diagnostic debugging design look like a lie.

| Category | Touches product | Default pattern | Default engine | Default check | Sabotage (proof the check can fail) |
|---|---|---|---|---|---|
| code generation | yes | evaluator–optimizer loop | opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority) | tests/build pass (script) | break the code → the check goes red |
| code review | no | maker–checker, fresh blind session | risk-tiered: Sonnet 5.5 when nothing builds; different kind from the worker when it builds (EXECUTOR_KINDS rule 5) | fixed checklist; findings with file:line | plant a known defect → the reviewer must find it |
| ui/ux dev | yes | codegen loop + human acceptance checkpoint | opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority) | build/render script + EJ's acceptance (last per 3.5) | break a component → the build fails |
| debugging | mixed | loop with the failing test as objective check (a diagnosis-only run is read-only research with a repro) | opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority) | repro test: red before, green after | revert the fix → red again |
| test data gen | mixed | single node, schema-validated (a validation-only run is read-only) | Sonnet 5.5 / `gemini-3.8-flash` (cheap tier) | schema validation + edge-case coverage list | corrupt a row → the validator rejects |
| test cases gen | yes | single node + review | opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority) | generated tests fail on a broken implementation | a seeded mutant must be caught |
| test script gen | yes | codegen loop | opencode `MiniMax-M3.1-Flash-Preview` + Codex `gpt-6.1-sol` (split: `workload.py`, opencode priority) | script detects a seeded failure | seeded failure → non-zero exit |
| repo scanning | no | parallel sectioning, read-only fan-out | agy (EJ, 2026-10-04) | coverage manifest; findings with paths | plant a marker file → the scan reports it |
| multi step planning | no | plan + gate (this method) | DeepSeek `deepseek-flash` (EJ, 2026-10-04 — the model the catalog names DeepSeek-V41-Flash) | script schema gate + checklist review | an unresolved spot → the gate fails |
| information extraction | no | single node, structured output | DeepSeek `deepseek-flash` (EJ, 2026-10-04) | JSON-schema validation + spot-check vs source | a corrupt source field → flagged, never hallucinated |
| web search | no | single node; voting on contested facts | agy (EJ, 2026-10-04) | dated sources with URLs; claims traceable | ask a nonexistent fact → must return not-found |
| classification | no | routing node | DeepSeek `deepseek-flash` (EJ, 2026-10-04) | schema-valid label + agreement on a labeled sample | an ambiguous sample → unknown/escalate, not a forced label |
| research and reports | no | single node, or sectioning + join | agy (EJ, 2026-10-04) | answers the question; every finding carries both-side citations and a CONFIRMED/INFERRED/GAP/UNPROVEN label; missing proof never reads as PASS; join contradiction = stop | seed a known divergence → it must appear as a row with both citations; seed conflicting sources → the join stops |
| document and explain | mixed | single node + review against source | Sonnet 5.5 | fixed checklist against the source; format constraints honored (audience, .txt vs markdown, LF) | remove a fact from the source → the review flags it missing |
| grade a run | no | single node, fixed rubric | Sonnet 5.5 | rubric verdicts kept separate per dimension; run-directory evidence only; missing proof = UNKNOWN/INVALID_RUN, never PASS | grade an empty run directory → INVALID_RUN, not PASS |
| others | — | no default — the full method from first principles | — | — | — |
```

## A3. `docs/TASK_TYPES.md` lines 1-3 and 26-40 (the 20% rule as TASK_TYPES states it)
```
# Task types — default patterns, combination pipelines, and the 20% rule

Agreed with EJ 2026-10-01. **n=0**: every default here is a working value until `TASK_TYPES_LEDGER.md` has
...
   Checked against facts per piece: a piece that touches product code, schema, UI or config is never labelled
   read-only. A wrong label is a **stop and replan**, not a repair (the blueprint kind-guard's shape).
2. **Default-first.** For each labelled piece look up its row (or the combination's pipeline), adapt it to the
   specifics, then run the normal gates. Steps 2–4 of the method still run. `others` has no default: the full
   method from first principles.
3. **Challenger (the 20% rule).** A bespoke design replaces the default only with a written claim **before the
   run**: ≥20% lower projected run cost (tokens / agents / wall time) **at equal coverage** — same acceptance
   criteria ids, same checks, same blindness. Coverage is a gate, never an axis; nobody trades completeness for
   speed. "Ask three times, get three different answers" is variance, not signal — the default stands unless
   the margin is claimed and proven on paper first.
4. **Two-layer review of the decision.**
   - **Script layer (free, deterministic):** `scripts/design_gate.py` — structure, category-vs-facts, label agreement (G8: the design's
     categories equal the categories its nodes carry; the in-run review node is exempt), the
     margin arithmetic, coverage equality, pipeline well-formedness, the reviewer-kind rule, ledger rows.
   - **Checklist layer (cheap judgment):** a Sonnet 5.5 subagent, fresh session, blind to the designer's
```

## A4. `docs/TASK_TYPES_LEDGER.md` — measured state, counted by the COO on 2026-10-04
```
data rows (lines starting '| 2026'): 8
design_source column: 8 default, 0 challenger
final (Reconciled) column values:
-  yes
-  no — token cost not measured
-  no — token cost not measured
-  no — token cost not measured
-  no — token cost not measured
-  no — token cost not measured
-  no — token cost not measured
-  no — token cost not measured
```

## A5. `.claude/skills/workflow-design/scripts/design_gate.py` lines 166-210 (G5 and G6 as implemented)
```
    src = d.get("design_source", "default")
    if isinstance(src, dict):
        if src.get("type") != "challenger":
            f.append("G5: a design_source object must be type 'challenger'")
        claim = src.get("claim_margin")
        if not isinstance(claim, (int, float)) or isinstance(claim, bool) or claim < 0.20:
            f.append("G5: challenger claim must be a number >= 0.20")
        if not (src.get("basis") or "").strip():
            f.append("G5: challenger claim has no basis")
        est = (d.get("estimate") or {}).get("tokens")
        dest = (d.get("default_estimate") or {}).get("tokens")
        if isinstance(est, (int, float)) and isinstance(dest, (int, float)) and dest > 0:
            recomputed = (dest - est) / dest
            if recomputed < 0.20:
                f.append(f"G5: recomputed margin {recomputed:.2f} < 0.20")
            elif isinstance(claim, (int, float)) and abs(claim - recomputed) > 0.01:
                f.append(f"G5: margin arithmetic: claim {claim} != recomputed {recomputed:.3f}")
        else:
            f.append("G5: challenger without estimate/default_estimate tokens — the arithmetic cannot be checked")
        cov, dcov = d.get("coverage") or {}, d.get("default_coverage") or {}
        if (set(cov.get("criteria", [])) != set(dcov.get("criteria", []))
                or set(cov.get("checks", [])) != set(dcov.get("checks", []))):
            f.append("G5: coverage differs from the default — coverage is a gate, not an axis")
    builders = [n for n in nodes
                if known.get(_cat(n), {}).get("product") == "yes"
                or (builds and known.get(_cat(n), {}).get("product") == "mixed")]
    if builders:
        reviewers = [n for n in nodes if _cat(n) == "code review"]
        if not reviewers:
            f.append("G6: a design with building nodes has no review node")
        else:
            builder_ids = [b.get("id") for b in builders]
            for r in reviewers:
                rk = engine_kind(r.get("engine", ""))
                targets = r.get("reviews") or builder_ids  # no pairing → reviewed against all builders
                t_nodes = [n for n in nodes if n.get("id") in set(targets)]
                t_kinds = {engine_kind(t.get("engine", "")) for t in t_nodes}
                yes_kinds = {engine_kind(t.get("engine", "")) for t in t_nodes
                             if known.get(_cat(t), {}).get("product") == "yes"}
                # a reviewer must be a different kind from what it reviews; when its targets span
                # kinds, the pure builders are the constraint (round-3, p195)
                constraint = t_kinds if len(t_kinds) == 1 else (yes_kinds or t_kinds)
                if rk == "unknown" or rk in constraint:
                    f.append(f"G6: reviewer engine {r.get('engine')!r} is not a different kind from "
                             f"what it reviews ({sorted(constraint)})")
```

## A6. `docs/EXECUTOR_KINDS.md` — reviewer/model rows and the code-review routing row
```
| Planner, and any node whose contract asks for high thinking | Codex | `gpt-6-astra` (the high-thinking model) |
| Coder | Codex | `gpt-6.1-sol`, high effort (*verified* 2026-10-03 on the CLI) |
| Reviewer, verifier | Codex, fresh session, never the coder's | `gpt-6.1-sol`, default effort; `gpt-6-astra` when the review is a high-thinking one |
| `code review` | the engine that did **not** build it | rule 5; risk-tiered — Sonnet 5.5 when nothing builds |
| `debugging` | opencode **and** codex split for the fix; **Opus 5.5** when it is complex debugging or root-cause analysis | rule 1, plus rule 3's escalation. The phrase *"complex debugging and root-cause analysis"* is rule 3's wording, not a category, and it lives in **this** row |
| `agy` | `gemini-3.8-flash-medium` and up | `dispatch.py`, engine `agy` | none — no provider exists, so this is CLI-only |
| `opencode` + MiniMax | `minimax-coding-plan/MiniMax-M3.1-Flash-Preview` | `dispatch.py`, engine `opencode` | `claude` / `claude-sonnet-5-5` — the engine default; no DSH provider for opencode exists |
```

## A7. The three anchors, verbatim with line numbers
```
107:    count = decision_tree(task.difficulty, task.capability)
108:    # C·4
109:    if count > 3:
110:        fired.append("C·4")
111:        k = math.ceil(count / 3)
112:        groups: list[GateExit] = []
...
22:from .ctx import ArtifactRef
23:
24:CAP = 3
25:
...
307:@dataclass
308:class CapState:
309:    """cap_state = (ctx.dispatch_count, CAP=3) — §2 Z1′; a slot remains iff dispatch_count < 3."""
310:
311:    dispatch_count: int = 0
312:    cap: int = CAP
313:
314:    @property
315:    def slot_remains(self) -> bool:
316:        return self.dispatch_count < self.cap
```

## A8. Where CAP is actually applied (for judging the stages.py:309 anchor)
```
120:        # CapState(0), slot_remains was always True and a capped judgment claim was always handed
123:        # Ctx.validate; the plan-wide total lives in dispatch_count, which cap_state reads).
309:    """cap_state = (ctx.dispatch_count, CAP=3) — §2 Z1′; a slot remains iff dispatch_count < 3."""
315:    def slot_remains(self) -> bool:
338:def count_sources(claim: Claim, events: list[dict], cap_state: CapState, framings: list[str]) -> tuple[int, str | None]:
401:    # "kind=judgment ⇒ remedy=add-differently-framed-source only if cap_state's
404:    if cap_state.slot_remains and unused_framing(claim, events, framings) is not None:
465:    cap_state = CapState(ctx.dispatch_count)
491:        n_avail, remedy = count_sources(c, events, cap_state, fr)
```
