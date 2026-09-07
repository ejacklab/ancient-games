# Hybrid tool layer — design brief (v0, for EJ's review before drafting)

**Style rule, above everything:** simple yet effective. The smallest registry and the smallest invariant set that pass the use cases below. A tool is a function plus a manifest. Nothing exists without a use case that reads it (the third-graph test). No abstraction for a single tool.

## Objectives
| # | Objective | Comes from |
|---|---|---|
| O1 | A main agent chooses the next action from a **dynamic tool registry** — research, code, test, debug, or any tool added later — without the loop being edited | the AI-native design EJ saw |
| O2 | Three safety properties hold **regardless of what the agent chooses**: guard before any irreversible act; prove before done; corroboration counted by a tool, never by the agent | F1–F4 ablation; T1's self-corroboration; Y2′ |
| O3 | Testable by **one curated e2e case set** — the eight traces plus constructed adversarial cases — with every failing case self-localized by its journal | EJ's rule: e2e over pyramid; the trace journal |
| O4 | Cheap on easy tasks: a T2-shaped task runs with zero dispatches | Gate's `count=0` exit, measured |
| O5 | Extensible two ways with no loop change: add a tool (manifest + function) or add a rule (registry/schema row or invariant predicate) | schema §4; "convert the walls" |
| O6 | Supports the loop shape the stage design lacks: test fails → localize → fix → re-test, bounded | UC7; why the hybrid exists |

## Use cases — the ones we want, each a real shape of work from this session
| UC | Shape | Real instance | What it exercises |
|---|---|---|---|
| UC1 | One-line fix + class-level guard | T2 (`3390749`) | zero dispatch; TDD idiom; prove |
| UC2 | Dead-code audit + safe deletion on a journal-adjacent file | T1 (`34c7bf6`) | guard + registry hub + tripwire; 2 non-actor sources; checkpoint |
| UC3 | Research → owner recommendation on a governance-gated decision | T3 | `actor=none`; 3 framings isolated; owner gate; write boundary |
| UC4 | Research wave: N framings → merged findings under a dominance rule | principles research; store waves | isolation; shared template; merge |
| UC5 | Design → adversarial review → fix → re-review, until accepted | V3 → V3.6 | sequential agents; reviewer isolation; MAIN decisions as inputs |
| UC6 | Implement from an accepted spec | coder passes 1–2 | closure floor; acceptance gate; commit policy; SCOPE_DELTA |
| UC7 | **Debug loop**: suite red → localize → fix → re-run, until green or stop criterion | (not yet run under the framework) | bounded iteration; stop criterion; the tool-agent's strength |
| UC8 | Replay a past case as a regression (conformance) | the 8-case suite | journal replay; e2e runner |
| UC9 | Add a tool at runtime and have the agent use it without a process change | SQLite index; `import-linter`; `mutmut` | dynamic registry |

Not use cases (out of scope): long-running autonomous loops without a human gate; multi-orchestrator coordination; anything that needs the graph layer.

## Requirements — numbered, each checkable by an e2e case
- **R1 Registry.** Each tool declares: `name`, `inputs`, `outputs`, `side_effects ∈ {none, read, invoke, mutate, commit}`, `cost ∈ {cheap, agent, suite}`, `participates_in` (invariant ids). Discovered from a directory of manifests at start. Adding a tool = adding a manifest + function.
- **R2 Invariants** — the non-delegable layer, checked by the tool layer *before* executing any call; a refused call is journaled with the invariant id:
  - I1 a tool with `side_effects ∈ {mutate, commit}` or `invoke` on a registry hub requires a prior `guard` result for that action in this run
  - I2 `done` requires `prove` = PASS in this run
  - I3 any corroboration count used by the agent comes from `corroborate`'s journal event; an agent-reported count is ignored
  - I4 a call whose target matches a `gate = owner` registry row with no owner approval on record is refused (`hard_blocked`)
  - I5 no more than 3 concurrent dispatches (CAP); `dispatch_count` tracked by the layer
  - Ceiling: five, unless an e2e case forces a sixth.
- **R3 Main-agent loop.** observe (ctx + journal) → choose tool → invariant check → execute → journal → repeat until `done`. The stage order (C→D→B→E→A) is the **default plan**, offered as a suggested sequence the agent may deviate from. Bounded by Gate's stop criterion and an iteration ceiling; no unbounded loops.
- **R4 Journal.** Every tool call is one event (`tool_call{tool, args_hash, result_summary, invariants_checked, refused_by}`); the existing seven events and the stage exit lines remain. Absolute path, single writer.
- **R5 Tests.** A case = (task input, expected outcome, expected invariant events). The suite = eight traces + adversarial cases; pass = outcomes match and no invariant violated. Cases are files; one added per real failure. Every lint has a case that makes it fail.
- **R6 Cost.** UC1 executes with zero dispatches. UC7 stops at the stop criterion or ceiling.
- **R7 Adapters.** Existing `stages.py`/`lints.py`/`registry.py`/`index.py` functions become tools by **wrapping, not rewriting**.
- **R8 Boundaries.** Stdlib-only Python; no LLM call inside the tool layer; the main agent is an LLM (a Claude Code session or a subagent) calling tools through a thin interface — the walls/holes rule.

## Scope
**In:** registry + manifest format · invariant predicates · loop + default plan · `tool_call` journal event · adapters for existing functions · e2e runner + case file format · the ablation harness (a subagent as main agent on UC1–UC3, tool-call log scored against the traces).
**Out:** new store features (decided separately) · graph layer · UI · tool sandboxing beyond the `side_effects` declaration · LLM API integration · multi-orchestrator.

## Assumptions to confirm
- A1 The main agent is a Claude Code session (as now) or a dispatched subagent (for the ablation); tools are called as Python functions / CLI, not through an API loop.
- A2 "Dynamic" = discovered from manifests at start of a run; hot-adding mid-run is not required.
- A3 UC7 (debug loop) is in scope even though no run has exercised it — it is the reason for the hybrid.
- A4 Existing stage functions are wrapped as tools, not redesigned.

## Process after this brief is approved
draft spec (registry format, invariant predicates, loop pseudocode, case format) → adversarial review with constructed cases → fix → coder → run the eight cases + the ablation → decide invariant thickness from the ablation's three yes/no answers.
