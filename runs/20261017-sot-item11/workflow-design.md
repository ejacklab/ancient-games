# Workflow design — 20261017-sot-item11

A design, not a run. Sequential. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. Written 2026-10-17 by the COO
(`claude-opus-5-5`) at EJ's request: *"design a workflow to use the 6 experts to research and fix item 11"*. State:
`state.md`. Nothing here has run. Same shape as run `20261017-w36-worth-scripting`, which worked (15 of 60 minutes).

## Item 11 (from `runs/20261014-sot-yaml-review/state.md`)

- **A. Merge and removed paths.** W6.3a keeps "every `covers` path either side wrote"; its `fails_if` says "a `covers`
  path that one side added". Does a path one side removed stay removed?
- **B. The kit.** The kit (SOURCE_OF_TRUTH.md, the YAML, CACHES.md, vision-statements/) leaves out
  `tools/memory_index.py` and `docs/index-md/`, which every `check: tool` record needs.
- **C. Recording the limit.** Rd3.1a: the project owner records measured limits — where, and in what form? The
  interim numbers now sit in three places: Rd3.1a, Rd3.1b and the tool's two constants.
- **D. Which agents.** The Rd3 title and the prose say "agents that read it"; Rd3.1a says "agents that work on the
  project". Not the same set.
- **E. Deferred last time.** Build the tool to read limits from a file; measure each engine's start-file limit.

## Questions for EJ

| # | Question | Provisional assumption |
|---|---|---|
| Q1 | Time for the run? | 60 minutes |
| Q2 | Apply the majority directly and show you after, as for item 13? | yes |
| Q3 | E: if the majority says to build the tool change (read limits from a file), is that its own later run (a code change with tests, crossed-build-check), or inside this one? | its own run; this run decides and records only |

## Restatement (method 3.0)

**Objective.** A–D are decided and written into the design (YAML through `build_requirements.py`, the prose, the
release note), each by the six experts' majority after research; E is decided (build or not, and where the limits
come from) and, by Q3's default, handed to its own run. **Out of scope:** changing `tools/memory_index.py` or
`docs/index-md/` in this run; `CACHES.md` (another design's document: a needed change is written as a request, never
made here); every other TODO item.

**Whys.** (1) Problem: four inconsistencies and one deferred build left by the last review. (2) Now: the design is
otherwise settled. (3) Shape: four small decisions plus one research question (the real start-file limits per engine).
(4) Failure: low; nothing is live. (5) Stop: at A–E decided. (6) Done: the checks pass; EJ sees what went in.

**Provisional category** (*inferred*): decisions with research — the `experts-decide` workflow.

## The algorithm (method 3.2)

| # | Step | Check |
|---|---|---|
| 1 | Research from the web: each engine's documented limit on files loaded at session start (Claude Code, Codex, agy/Gemini, opencode, dsh, Qwen), checked against `CACHES.md`'s table, including its agy conflict (W-4) | each finding labelled verified (source opened) or not, with its link |
| 2 | Six experts, one round, on A–E with the research added | `six_experts.py check` per expert; one rerun for an unusable answer; `compare.md` |
| 3 | The COO takes the majority on each of A–E (a point without a majority stays as it is and is listed) and applies it: the YAML records, the prose, the release note, item 11 in the TODO | the YAML's build script, `yaml_check.py`, `paths.py` pass; commit and push in the same step |
| 4 | If E's majority is "build": write the request for that run in the TODO (what to build, the criteria) | it names the criteria and the files |

## Pieces

### P1 — Research and experts (`experts-decide`)
`.claude/workflows/experts-decide.js` with `{run: "runs/20261017-sot-item11", question:
"runs/20261017-sot-item11/question.md", out: "experts", needsWeb: true, research: "<step 1's question>"}`. 范蠡 runs on
Claude (web). Not `approveOrChange`: open choices. Evidence: `research/experts.md`, `experts/compare.md`. Its checks:
the workflow's (`six_experts.py check`, written by Claude: sections and citations, not whether a rule was applied
well).

### P2 — Apply the majority (COO)
Edit `runs/20261014-sot-yaml-review/build_requirements.py` (W6.3a, the `kit` key, Rd3 title, Rd3.1a/b as decided),
the prose, the release notes; rebuild; run the three checks; record the majority table in `nodes/p2.result.md`; strike
item 11 in the TODO, adding E's follow-up run if the majority says build; commit and push. **Must not change:**
`tools/`, `docs/index-md/`, `CACHES.md`, any other record.

## Joins, parallel, predictability

- Join: P2 reads every answer and the research together; a split point is listed, never averaged.
- Parallel: none outside the workflow.
- Agents: 1 research, 6 experts (+ reruns), 1 compare, small check steps. Cost (*not measured*, from the item-13
  run): about 15–20 minutes, 0.8M subagent tokens. Success: A–D written, E decided, checks pass.

## Debuggability and quality control

- The workflow's per-step files and progress file; `state.md`; one commit.
- Script checks: the three design checks (shown able to fail in run `20261015-sot-leftovers`). Judged: the experts.
  EJ's: Q1–Q3 and the overrule after.
- Experts on this design's unclear spots: **not asked** — the run is itself a six-expert round on the open points.
