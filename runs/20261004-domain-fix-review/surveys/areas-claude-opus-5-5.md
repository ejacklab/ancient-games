# Area survey — claude-opus-5-5

Written blind to the other two surveys. Classical citations are only from `docs/research/20261004-sunzi/` and
carry the chair's principle number (`CANONICAL #n`) with its **Basis** label. Reasoning not from a note is marked
`(not from a note)`.

**What I checked myself, and what I could not.** I read every file and line a verdict below names:
`design_gate.py`, `readiness.py`, `engines.py`, `dispatch.py`, `workload.py`, `intake.js`, `corpus_check.py`,
`mutation_matrix.py`, the method, the skill, the diagram, `EXECUTOR_KINDS.md`, `TASK_TYPES.md`, the blueprint template.
I grepped the 300 emitted designs. I did **not** run the mutation matrix, the gate or any test: in this session
those commands needed an approval I did not get. So every "it now does X" below is *read*, not *ran*, except the
grep counts.

Three facts I found while reading change several verdicts, so they come first:

1. **`intake.js` already holds most of the missing schema.** Its `DESIGN_SCHEMA` piece (`intake.js:169-201`) carries
   `stop`, `check_kind`, `intent`, `returns`, `files_touched`, `must_not_change`, `evidence`, `evidence_file`,
   `state_reads`, `state_writes`, `brief_given` and `brief_withheld`. That covers four of the five things with
   real content, plus the stop. What it lacks is `category`, `engine`, `sabotage` and a `tools` field. So 1.1, 1.3,
   4.5 and 8.3 are not four schema inventions. They are one choice about which format is canonical.
2. **The caps are already enforced in code.** `dispatch.py:41` sets `max_roles 5, max_parallel 3, max_rounds 2,
   max_calls 30`, and `dispatch.py:63,108` refuse plans over the caps. 5.7 is half wrong as written, and 6.2 is
   bounded inside one dispatch but not across replans.
3. **A dispatch plan already carries a per-node `fallback`** (`dispatch.py:97,271`), and `workload.py:168-171`
   already checks a node's `verified_by` against the node's engine. So 8.2 can be closed in code that exists.

## Area 1. The gate cannot reject

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 1.1 | SCHEMA | `five_things` must become an object with content per name. `intake.js:189-199` already has the content fields for context, contract, evidence and state; only `tools` is new. EJ decides whether the gate adopts intake's piece fields (see 4.5). |
| 1.2 | SCHEMA | Design-level `baseline: {command, output_file}`, with a G-rule that rejects `builds: true` and no baseline. EJ has to accept that this turns about 94 of 300 corpus designs red (open-defects). |
| 1.3 | SCHEMA | intake.js has `stop` as one string, checked by a judged verifier (V7). The gate needs it as three named parts (`criteria`, `baseline_holds`, `must_not_change`) so a script can check that each one is there. Same EJ format decision as 1.1. |
| 1.4 | DIRECT | `sabotage` is already read (G9). The fix for `pattern` is the same edit as 1.6: in `design_gate.py`, a building node whose row pattern names a loop must carry `loop`. That is the first real use of `pattern`. Check: a `mutation_matrix.py` row that deletes the code-generation node's `loop` must come back CAUGHT G3. |
| 1.5 | LATER | The contradiction clause is in place (G2, open-defects). What remains cannot be checked before a run: the honest check compares `touched_paths` with the run's `git diff --name-only` afterwards, and no designed run has yet gone through the gate and produced a diff. |
| 1.6 | DIRECT | `design_gate.py` G3: read the row's `pattern` cell. Rows 88, 90, 91 and 94 in `TASK_TYPES.md` name a loop. A building node in one of those rows with no `loop` is a finding, so the rule no longer depends on a loop already existing. Check: the 1.4 mutation; `--self-check` must still report it MISSED when the mutation is neutered. |
| 1.7 | LATER | Fixed for the form that was found: G3 rejects a check that points at the table, and 0 of the 300 emitted designs now contain `TASK_TYPES` (grep). "Executable" needs `check_kind` on the gate's node. intake.js already has that field, so this comes free with 4.5 and is not worth its own edit. |

**Reading.** CANONICAL #14 (VERIFIED, 合於利而動，不合於利而止; design rule: *"a node … whose check can pass either way,
is not ready"*) says the 1.1 and 1.3 holes are not a gate bug. They are designs the method itself would call not ready, which
the gate cannot see because the format has nowhere to say it. 1.5 is the CANONICAL #15 case (VERIFIED,
先知者…不可驗於度，必取於人): G2 reckons from the design's own claims, which is 度, not someone who looked.
No static rule cures that. Only a post-run observation does, so it is LATER, not DIRECT.

## Area 2. The test could not fail

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 2.1 | LATER | The only non-circular input is a design that was not built from the table, meaning intake.js output. That cannot reach the gate until 4.5 joins the two formats. Not fixable before 4.5. |
| 2.2 | DIRECT | No real challenger can exist while the ledger is empty, but the matrix can test G5 properly. By reading, its two G5 rows set `claim`, not `claim_margin` (`mutation_matrix.py:83,87`), so they are caught by the missing-field branch, not by the 0.20 threshold or the arithmetic. Fix those rows to use `claim_margin` with valid estimates. Check: lower the threshold in `design_gate.py` to 0.05 and the 10% row must report MISSED. G7 is already covered by the gate's `--self-test` ledger cases. |
| 2.3 | LATER | Addressed: `mutation_matrix.py` is in the suite and has a `--self-check`. Nothing of its own is left. Each new rule from this survey adds one row to it. |
| 2.4 | DECISION | Running the checklist layer costs model calls, so EJ decides whether to buy one blind fixed-checklist pass. The matrix's three HOLE mutations (no baseline, no three-part stop, bare five_things) are a ready-made planted-defect set for it: they are exactly what `TASK_TYPES.md:284` says that layer catches. Until it runs, that line should say n=0. |
| 2.5 | DOC | Fixed in `runs/20261004-corpus-fulltest/README.md:73-75`. But `testlog.md:34` still prints the bare "codex 90%". One pointer on that line closes it. |
| 2.6 | DIRECT | Sabotage half done. The pattern half closes with the 1.4/1.6 rule: `corpus_check.py:72-74` already emits loops for the loop categories. Check: re-run the corpus emit through the gate with the new rule and expect zero new G3 findings, plus the 1.4 mutation row. |

**Reading.** CANONICAL #8 (VERIFIED, 以正合，以奇勝; design rule: *"provision a small, capped share for a deliberate
alternative, recording its results"*). The 奇 share exists on paper (G5, the ledger). It is unexercised, not broken. That is why 2.2's only
DIRECT part is making sure the matrix tests the threshold, and why "run a real challenger" is not on my list.
For 2.1 `(not from a note)`: when the emitter and the gate read the same table, they are one player, not two.
Their agreement is guaranteed in advance and carries no information. An independent input is the only fix, so it waits on 4.5.

## Area 3. Step 1 — the readiness script

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 3.1 | DIRECT | `readiness.py:197-205` check_blueprint: return MISSING when `README.md` is absent or no section file exists, and VERIFIED only when the map is present. Check: add to `--self-test` and `tests/test_readiness.py` a temp dir holding only `notes.md`; it must not be VERIFIED, and passing it as `--blueprint` must exit 1 (exit_code already hard-fails a MISSING blueprint). |
| 3.2 | DIRECT | `readiness.py:184`: make `absent_status` default to MISSING, which is already in the vocabulary. `exit_code` fails only on required items, so optional directories still exit 0. Check: `tests/test_readiness.py` on an empty temp dir asserts the status is MISSING, not VERIFIED. |
| 3.3 | DIRECT | `readiness.py:204`: count only the eight template names (`01-vision.md` … `08-non-functional.md`, `docs/workflow-templates/blueprint.md:11-18`) and report "k of 8". The map may point elsewhere, so the label must say "template files", not "sections". Check: a test dir with `README.md` and `notes.md` reports 0 of 8. |
| 3.4 | DIRECT | `readiness.py:326` exit_code: a `--require`d item whose status is UNKNOWN fails, as MISSING does. Check: extend `--self-test` with a stub tool that times out; `--require` on it must exit 1. |
| 3.5 | DIRECT | `readiness.py:163`: guard `isinstance(model, dict)`. `readiness.py:139`: require id-shaped lines before VERIFIED. Check: `tests/test_readiness.py` with settings `{"model": "x"}` gives UNKNOWN, not an exception, and a stub `agy` printing an error with rc 0 gives UNKNOWN. |

**Reading.** CANONICAL #3 (VERIFIED, 知彼知己…不知彼而知己，一勝一負; design rule: *"marked reported versus verified … If
either half is empty, treat the outcome as uncertain"*). Readiness is the 己 half. A script that reports `verified`
for an absent directory is worse than one that reports nothing: it fills the 己 half with a false entry. 3.4 is CANONICAL #6
(VERIFIED, 無恃其不來，恃吾有以待之): passing a required tool of unknown state is a plan resting on hope.
Do 3.1, 3.2 and 3.4 as one edit. They are one vocabulary defect, and that edit is the cheapest
DIRECT fix in the register.

## Area 4. The three renderings disagree

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 4.1 | DOC | `SKILL.md:175` has the engine split; `WORKFLOW_DESIGN_METHOD.md` (3.6/3.8) and `WORKFLOW_DESIGN_DIAGRAM.md` do not. **Settle 8.1 first.** Copying the rule into the method now would copy a rule that can defeat rule 5. |
| 4.2 | DOC | `SKILL.md:165` says "all three" and lists four; `WORKFLOW_DESIGN_METHOD.md:476` says three. The engine split is a node-engine rule, not a design quality. Move it from the quality checklist to step 7 and both files say three. Do it in the same edit as 4.1. |
| 4.3 | DOC | `WORKFLOW_DESIGN_DIAGRAM.md:213` says "no step", but `SKILL.md:49-53` (step 1) and `SKILL.md:122-131` (step 7) carry 3.8. Rewrite the row to "steps 1 and 7, as reference". |
| 4.4 | DOC | `EXECUTOR_KINDS.md:63` (and `:17`) route classification to agy/gemini-3.1-pro-high; `EXECUTOR_KINDS.md:156` routes it to deepseek-flash. `:156` is the newer decision (EJ, 2026-10-04) and wins. Correct `:63` and `:17`. |
| 4.5 | SCHEMA | The gate reads `nodes` and intake.js emits `pieces`. Pick one format, don't add an adapter. Recommendation: intake's piece, because it is the richer one (fact 1 above). Add `category`, `engine`, `sabotage` and `tools` to it, and have `design_gate.py` read it. EJ decides, because this changes the format the corpus is built in. |
| 4.6 | DOC | Method 3.1 (`WORKFLOW_DESIGN_METHOD.md:76-80`) lacks the two rules in `SKILL.md:51-57`: prove the binary that will make the call, and CLI first, provider second. The first is already in method 3.8 (line 348); the second is in no method section. |
| 4.7 | DOC | `TASK_TYPES_LEDGER.md:7` says "Coverage outcome"; `design_gate.py:39` LEDGER_KEYS says `coverage_result`. The parse is positional (`design_gate.py:248`), so rename the header. Nothing else moves. |
| 4.8 | DOC | `TASK_TYPES.md:63` (use case 2 lists `information extraction`) contradicts `TASK_TYPES.md:120` (rule 2: extraction only when the deliverable is the structured data). The labelling rule is the more tested of the two (it is the one the expected labels were scored on), so drop or qualify the use-case cell. |

**Reading.** CANONICAL #7 (VERIFIED, 求之於勢，不責於人) fits 4.8 exactly. The models were marked down for following the
table, so the fault was in the configuration, not in the individuals. 4.5 is the case of CANONICAL #9 (**RECALLED**,
single source, 分數…形名; design rule: *"one state-file schema every node reads and writes"*): two formats for one
design is two signalling codes in one army. The verdict does not rest on that line, though. Rule 7 of the house
rules (pick one, never blend) gives the same answer with better evidence.

## Area 5. Composition — work with no owner

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 5.1 | DECISION | Naming the producer is easy (a baseline step before the first building node; intake.js already takes a snapshot at step 1). The real choice is EJ's: what a baseline that is **already red** means. (a) Stop, because "still passes" cannot be proved. (b) Freeze the red list in state, and stop-part 2 becomes "no new reds". I recommend (b). |
| 5.2 | SCHEMA | Method 3.6 (line 312) says every node names its **role**, but the gate's node has no `role` field. Add it, with a value for the final "what is missing" pass, and a G-rule that a design that builds has exactly one such node, needing every building node. |
| 5.3 | DECISION | EJ chooses: (a) step-5 loops may start before the graph, and go through `dispatch.py` from the first call so its caps (`dispatch.py:41`) bind them; or (b) step 5 only marks pieces loop-ready and nothing runs until step 7. I recommend (a). |
| 5.4 | DOC | `WORKFLOW_DESIGN_METHOD.md:131` says a non-product task carries no acceptance criteria, while `SKILL.md:132` and `WORKFLOW_DESIGN_DIAGRAM.md:47` say every run ends at them. The stop for that class already exists, in method 3.0's why #6 (line 51). Step 8 should say "the acceptance criteria, or for a non-product task the 3.0 why-6 stop". intake.js already requires `success_criteria`. |
| 5.5 | DECISION | EJ chooses whether the tiny exit must still record a baseline (one test command and its output in the prompt file) when it changes product code. That adds cost to the path §2 promises stays cheap, so it is EJ's call. I recommend yes, for building tasks only. |
| 5.6 | DECISION | `EXECUTOR_KINDS.md:164` already marks it open. EJ names an engine for `others`, or rules that `others` runs on the COO herself. The whale rule favours the second. |
| 5.7 | DOC | The caps half is wrong as written: `dispatch.py:41,63,108` enforce them in code, and `SKILL.md:128` points there. What is really missing is item 12 (no finding id, so it may not drive a building node): it is in `WORKFLOW_DESIGN_METHOD.md:424-427` only, and `SKILL.md` step 7 needs one sentence. |

**Reading.** CANONICAL #6 (VERIFIED, 先為不可勝，以待敵之可勝; design rule: *"Build the defensive invariants first … a check
that can fail"*). The baseline is the purest 不可勝在己 item in the method: entirely in the designer's control, and
the thing every stop rests on. That is why 5.1 is the most serious defect, and why its open question
(a red baseline) is the one that needs EJ, not the producer. For 5.3, CANONICAL #2 (VERIFIED, 兵貴勝，不貴久;
*"every loop … gets a hard cap … set before it starts"*) argues that the caps should bind from the first loop, not
for or against early loops as such. CANONICAL #12 (VERIFIED, 兵無成勢，無恒形) actually favours starting clear work early.

## Area 6. Decisions the algorithm never makes

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 6.1 | SCHEMA | The defaults exist in code (`engines.py:157` DEFAULT_FALLBACKS, `dispatch.py:41` max_rounds 2, the dispatch plan's per-node `fallback`), but the design format carries none of them. Add node `fallback` and `escalation_model` so the gate sees them before dispatch. 8.2 depends on this. |
| 6.2 | DECISION | `max_calls 30` (`dispatch.py:41`) bounds one dispatch, but a replan starts a new one. EJ names a run-wide replan count. I recommend 1, then EJ. |
| 6.3 | LATER | The ordering problem is real, but no challenger has ever been proposed (ledger empty, 2.2), so it cannot bite yet. When the first challenger appears, move the claim after 3.6. |
| 6.4 | DOC | `WORKFLOW_DESIGN_METHOD.md:199-200` (3.2 records "the node it merges into") vs `WORKFLOW_DESIGN_METHOD.md:272` (3.6: nodes are right-sized pieces). `SKILL.md:83-84` copies the 3.2 column. Rename the column "provisional node" and say 3.6 fixes it. |
| 6.5 | DOC | `WORKFLOW_DESIGN_DIAGRAM.md:34-37` sizes after spots are *resolved* (JOIN → S4); `WORKFLOW_DESIGN_METHOD.md:221-225` sizes on spot *kinds*, which are known once spots are listed. The diagram's own rule (line 220) says the method wins, so redraw S3 → S4. The method half (`:213`) describes both outcomes and needs no change. |

**Reading.** CANONICAL #14 (VERIFIED, 合於利而動，不合於利而止; *"stopping is decided by that condition, not by sunk
cost"*) is the right line for 6.2. A replan that renews its own budget never meets the stop test. The number
itself is outside the text (CANONICAL, "what this domain cannot supply", item 3), so it is a DECISION.

## Area 7. The runnable form, `intake.js`

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 7.1 | DIRECT | `intake.js:618-623` opens with readiness. Put 3.0's restatement (objective, in scope, out of scope) first in the step-1 prompt, as a required `restatement` field of READY_SCHEMA. No new agent, because 3.0's cost guard forbids one. Check: a sabotage case in `tests/workflows/intake_harness.mjs` where readiness returns no restatement must fail the run at step 1. The tiny test stays with the caller, which the intake skill's description already says. |
| 7.2 | SCHEMA | Waits on 1.2's `baseline {command, output_file}`. The git snapshot at `intake.js:506` is not wrong. It is the evidence for stop-part 3 (must not change, V6), labelled as part 2. Keep it under that name and record the test command and output as the baseline. |
| 7.3 | DIRECT | `intake.js:381`: accept 3.5 item 4's first exit (a fresh node on a stronger tier), provided the same text also names the final fallback to the unclear list or EJ. Check: two `intake_harness.mjs` cases. "fresh node on a stronger tier, then the unclear list" passes; "another round" still fails. |
| 7.4 | DOC | Already fixed in code, and not in intake.js: the emitter is `corpus_check.py:69`, which now emits the row's own check, and 0 of 300 emitted designs contain `TASK_TYPES` (grep). What is wrong now is prose: `runs/20261004-open-defects.md` has no status for 7.4, and `runs/20261004-defect-register.md` files it under intake.js. |

**Reading.** CANONICAL #6 (VERIFIED, as above) separates 7.2's two snapshots cleanly. The git status protects
what must not change, and the test output proves what still passes. Both are defensive; they are not the same defence.

## Area 8. My own construction, observed failing

| issue | verdict | what would fix it, or what blocks it |
|---|---|---|
| 8.1 | DECISION | Two of EJ's rules conflict. The role map makes Codex the reviewer, and the opencode-priority split makes Codex a coder. EJ chooses: (a) a split build is reviewed by a third kind (Claude or DeepSeek); or (b) the gate runs on the per-module plan after `workload.py --write`, where `workload.py:168-171` already enforces rule 5 per node. After that, `engine_kind` in `design_gate.py` should return every kind a cell names, checked by a mutation with a `codex` reviewer on an "opencode + Codex" node. |
| 8.2 | DIRECT | `workload.py:168-171` compares the verifier only with the worker's engine. It should also compare it with the worker's resolved fallback: the plan's `fallback`, or `engines.DEFAULT_FALLBACKS`. Check: a case in `tests/test_workload.py` with a codex node verified by a claude node, and no plan fallback, must report rule 5. A design-time version waits on 6.1. |
| 8.3 | SCHEMA | Same field as 1.1. Once five_things has content, `corpus_check.py:70` must emit it, and G3 checks that it is not empty. |

**Reading.** CANONICAL #3 (VERIFIED) gives the exact violation for 8.2: *"Assigning a node to an engine because it is
the default, without checking what that engine can do"*. DEFAULT_FALLBACKS assigns by default, and nothing checks the
result against the verifier. For 8.1 `(not from a note)`: a review is worth something because the reviewer's errors are
not correlated with the author's. A Codex reviewer on code Codex partly wrote shares the author's blind spots on
exactly the part it wrote, so G6 passing there says nothing about independence.

## What I would fix first

1. **Get one decision from EJ: intake.js's piece becomes the design format the gate reads** (4.5, Rule 7). It is
   the cheapest rung that clears the most (CANONICAL #4, VERIFIED, 上兵伐謀): with fields added, it unblocks 1.1, 1.3,
   8.3 and 7.2, and gives 2.1 its first non-circular input. **Check:** the matrix rows "no three-part stop" and
   "five_things names only" move from HOLE to CAUGHT, and an intake-shaped fixture from
   `tests/workflows/intake_harness.mjs` passes `design_gate.py`. (1.2's baseline still needs its own field.)
2. **Fix the readiness vocabulary: 3.1, 3.2 and 3.4 in one edit to `readiness.py`.** It is wholly DIRECT, costs no model
   calls, and it is the 己 half of readiness reporting false knowledge. **Check:** `readiness.py --self-test` and
   `tests/test_readiness.py` cases for an empty dir, a blueprint dir with no map, and a required tool that times
   out. All three must stop reading VERIFIED or exit 0, and each case must fail when the old line is restored.
3. **Close 8.2 in `workload.py`.** It is a live rule-5 hole in code that runs, and its fix uses fields that exist today.
   **Check:** a `tests/test_workload.py` case where a codex node with a claude verifier and no plan fallback is
   refused, and it passes again only when the plan names a non-claude fallback.

The pattern-driven loop rule (1.4/1.6/2.6) would be fourth. It is DIRECT and closes three rows, but it widens the
gate, while items 2 and 3 fix checks that currently report the wrong thing.

## Where 孫子兵法 does not help

- **3.5** — an uncaught `AttributeError` on a non-object `model`, and rc 0 treated as proof. This is input validation;
  no principle in the notes says anything about it, and finding one would be the manufactured principle the brief warns against.
- **4.7** — a ledger header that says "Coverage outcome" where the code says `coverage_result`. Clerical drift. The fix is
  a rename.
- **2.5** — a percentage quoted without its denominator. This is reporting arithmetic. Rule 8 of the house rules covers
  it; the text does not.

More generally, the notes' own limit applies to everything in Area 4: CANONICAL "what this domain cannot supply",
item 3 — *"a concrete org chart, message format, or decision protocol … must be supplied by the designer"*. 孫子兵法
can say that two formats for one design is a fault (4.5). It cannot say which fields the one format should have.
