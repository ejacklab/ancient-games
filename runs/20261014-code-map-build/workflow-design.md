# Workflow design — 20261014-code-map-build

A design, not a run. Sequential and state-file driven. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Product:
`runs/20261014-code-map-vision-relay/result-trimmed.md`, the vision and requirements R1–R3, A1–A3, A5, A6, L1, L2
(not yet accepted by EJ).

## Questions for EJ

| # | Question | Provisional assumption |
|---|---|---|
| Q1 | Which three opencode modules does A6 map? | `core/src/session`, `core/src/tool` + `permission.ts`, `packages/ai` (COO proposal) |
| Q2 | May the COO install `bun` and run `bun install` in the opencode clone? | Yes; without it the type checker cannot see opencode's dependencies, so R2 cannot pass |
| Q3 | Which languages must v1 read? | TypeScript, TSX and JavaScript (one compiler reads all three); Python not in v1 |
| Q4 | Where does the tool live, and under what name? | `code_map/` in this repo (public), a TypeScript package named `code-map`, also installed as a skill |
| Q5 | Accept the vision and requirements as they stand (`result-trimmed.md`)? | P1 may start on the draft; P3 waits for acceptance (method 3.1: a build waits for settled sections) |

## Restatement

**Objective.** A TypeScript code-map tool exists, meets its accepted requirements on opencode, and has its cost
against plain reading measured (L2). It is packaged as a skill, and an integration test shows what it changes when
the workflow-design method runs in Claude Code CLI on real opencode tasks.

**In scope:**
- research;
- answer keys;
- an evaluator;
- the build;
- the three module maps;
- an effectiveness loop;
- packaging as a skill;
- the integration test.

**Out of scope:**
- changing the workflow-design method or its documents (a finding becomes a request to EJ);
- the old Python `code_graph/` (left as it is);
- private code.

**Why** (short): EJ wants to know whether a map beats reading on code too big to read, in the language EJ chose.
The workflow-design method's explorer role (method 3.8 item 10) is where an agent reads existing code. So that is
where the tool must prove itself.

**Category** (inferred): research → test script gen → build → measure → integration test.

## Who does what

| Job | Engine (model) | Why |
|---|---|---|
| Research (web) | `researcher` subagent (Claude) | method 3.8 item 9 |
| Explore opencode, write the answer keys | Claude explorer subagent, read-only | keys made by someone other than the builder, by a different method |
| Evaluator | Codex gpt-6.1-sol, write | the builder must not write its own check |
| Build the tool | opencode (MiniMax-M3.1-Flash-Preview), write | opencode has build priority (EJ, 2026-10-04) |
| Tests for each build step | Codex gpt-6.1-sol, write | tests from a different engine than the code |
| Review each step | 孫子 (dsh) and 范蠡 (agy), read-only, via `four-experts` | they see the diff and the evaluator output, never the builder's reasoning |
| Agent arms (L2, P6) | Claude subagents and `claude -p`, the same model in both arms | the same model on both sides, so only the input differs |
| Run scripts, keep state | the COO | |

## Pieces, in the order they run

### P0 Readiness and baseline
- **Steps:**
  1. Prove `node`, `npm`, `npx`, `bun` (after Q2), `claude -p` and the four engines (canary per engine).
  2. Run `bun install` in the clone at `6dc4d4e`; confirm `tsgo` or `tsc` type-checks one package.
  3. Run this repo's `pytest -q` and save the output.
- **Check:** a script, `readiness.md`.
- **Exit:** a missing tool becomes an unclear spot, back to EJ.

### P1 Research and answer keys
- **Steps:**
  1. **Researcher** → `docs/research/20261014-code-map/FINDINGS.md`. It covers:
     - the TypeScript LanguageService call hierarchy (`prepareCallHierarchy`, incoming and outgoing calls) — *model
       knowledge, to verify*;
     - ts-morph;
     - scip-typescript;
     - dependency-cruiser;
     - how each one resolves Effect `yield* Service` calls.
  2. **Explorer:** for each of the three modules, about 10 fixed questions with answers. The answers come by a method
     other than the tool's:
     - opencode's own tests;
     - `packages/protocol/openapi.json`;
     - `tsgo` failures after a planted change;
     - hand reading with `quote_check.py`.

     The keys go to a COO-only folder until the verdicts.
  3. **Four experts** on the unclear-spots list (method 3.3).
- **Check:**
  - `quote_check.py` passes on every key;
  - each finding has a source and a label.
- **Builds:** no.

### P2 Spec and evaluator
- **Steps:**
  1. The COO writes `spec.md`: the CLI contract and the JSON shape for each requirement.
  2. Codex builds `code_map/eval/`: one check per **Fails if**. It reports MET, NOT MET or NOT CHECKED, with totals.
  3. The COO plants faults: a broken copy of the tool for each requirement, kept away from workers.
- **Check (script):** the evaluator flags every planted fault on its own requirement.
- **Attempt limit:** 3, then EJ.

### P3 Build loop, one requirement per round
- **Order:**
  1. R1;
  2. R2 (type-resolved calls; the core);
  3. A5 (one question, one answer);
  4. A2;
  5. A3;
  6. A1;
  7. L1;
  8. R3.
- **Each round:**
  1. Codex writes failing tests for the requirement.
  2. opencode builds until those tests and the evaluator's check pass, and no MET requirement regresses.
  3. 孫子 and 范蠡 review: APPROVE, or CHANGE tied to a requirement line.
- **Attempt limit:** 3 per requirement. Then the requirement goes to EJ as blocked, and the loop moves on.
- **Experts on the loop check:** method 3.5 (`linus,fan-li,sun-tzu,dave`) before the first round.
- **Must not change:**
  - `code_map/eval/`;
  - the tests during a build;
  - `docs/`;
  - `code_graph/`.
- **Commits:** none until EJ says so.

### P4 The three module maps (A6)
- **Steps:**
  1. Run the tool on the three modules.
  2. Run the evaluator.
  3. A blind check against the P1 keys.
- **Check:**
  - A1 MET for each map;
  - wrong, missed and correct counts against the keys;
  - map size compared with source size.

### P5 Effectiveness loop (L2)
- **Steps:** on each module's fixed questions, run two arms on the same model:
  - the agent with the map;
  - the agent with read and grep only.

  Measure:
  - correctness against the keys;
  - total tokens, including the map build;
  - time.
- **Improve and rerun:**
  - map size;
  - which layers are shown;
  - one-question answers.
- **Stop:** a round improves neither correctness nor tokens, or 3 rounds. The result is reported as measured, wins and
  losses alike.

### P6 Integration test with workflow-design in Claude Code CLI
- **Steps:**
  1. Package the tool as a `code-map` skill: `SKILL.md` plus scripts run with `node` or `npx`. Link it into
     `~/.claude/skills` and `~/.agents/skills` the same way as the other skills.
  2. Pick three real change tasks on opencode, one per module. For example, "add a tool that needs the edit
     permission".
  3. For each task, run `claude -p` with the workflow-design skill twice: once with `code-map` installed, once
     without. Same model, fresh session, prompt in a file.
  4. Compare the two runs on:
     - the explorer file: `quote_check.py` pass rate, and claims correct against the keys;
     - the design's unclear-spots count;
     - tokens from `claude -p --output-format json`;
     - time;
     - whether the transcript shows the skill being used.
- **Check:**
  - a script for the counts;
  - a blind Claude judge for claim correctness.
- **Must not change:** the method, the skill text and the templates. A finding becomes a request to EJ.

### P7 Report → EJ
- `report.md`:
  - requirements met, with totals;
  - L2 numbers;
  - the P6 comparison;
  - what the results do not establish (n, one model, one target).
- EJ accepts or sends pieces back.

## Joins and stops

- **P3 starts only after:**
  - P2's evaluator has caught its planted faults;
  - EJ has accepted the requirements (Q5).
- **P5 and P6 run only on a tool whose R2 and A5 are MET.**
- **A contradiction** between a key and the evaluator stops the piece and goes to EJ.

## Parallel candidates

None. Each piece needs the one before it. The three modules inside P4 and P5 could run side by side, but they share
one clone and one tool build, so they stay sequential.

## Cost (my estimate, not measured)

| Piece | Estimate |
|---|---|
| P1 | about 6 agent runs |
| P2 | 2–6 |
| P3 | 8 requirements × 3 engine calls × 1–3 rounds: about 25–70 |
| P4 | about 3 |
| P5 | 3 modules × 2 arms × up to 3 rounds: up to 18 |
| P6 | 3 tasks × 2 arms, plus a judge: about 7 |
| **Total** | **about 60–110 engine calls, over several days of wall time** |

Codex quota is the likely limit.

## Predictability, debuggability, quality control

- **Predictable:** a fixed order; one requirement per round; attempt limits; stops at the evaluator and at EJ.
- **Debuggable:**
  - one `state.md` line per step (the `state-entry` skill);
  - evidence in `runs/20261014-code-map-build/evidence/`;
  - briefs in `briefs/`.
- **Quality control:**
  - keys made by a different method, before the build;
  - an evaluator proven by planted faults;
  - the builder never writes its tests, the evaluator or its review;
  - every measurement has a plain-reading control.
