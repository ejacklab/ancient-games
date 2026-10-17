Method 3.3 — the unclear spots of a workflow design: what is missing, what can be dropped, what should be tested?

Asked of: Linus, 孫子, 老子, Dave (`--only linus,sun-tzu,lao-tzu,dave`). Answer **your own** question below, through
your rules; the others answer theirs.

- **Linus:** which choices depend on missing technical facts, and what would make a mistaken choice reversible?
- **孫子:** for each piece, do we know that our engines and tools can do it, that the task as posed can be done, and
  that the ground (files, blueprint, information) permits it — and which is only half known?
- **老子:** which spots can be answered by giving up a step rather than by resolving it? (Say what would be lost.)
- **Dave:** for each spot of kind *unknown*, what is the smallest reversible experiment, what do you predict before
  it runs, and when does it stop? Leave any threshold EJ has not given open.

In "Answer", list spot ids (existing ones, or new ones you raise as N1, N2 …) with your verdict for each. Do not
decide for EJ: a spot to drop is a question for EJ, not a removal.

Facts (filled in by the COO, 2026-10-14):
- **The challenge and its restatement:** see `runs/20261014-code-map-build/workflow-design.md`, Restatement.
  Objective: a TypeScript code-map tool that meets its requirements on opencode, has its cost measured against plain
  reading, and is integration-tested with the workflow-design method in Claude Code CLI. In scope: research, keys,
  evaluator, build, three module maps, an effectiveness loop, skill packaging, the integration test. Out of scope:
  changing the method, the old Python code_graph, private code.
- **The algorithm:** pieces P0–P7 in `runs/20261014-code-map-build/workflow-design.md`. The interface is in
  `runs/20261014-code-map-build/spec.md`. The requirements are in
  `runs/20261014-code-map-vision-relay/result-trimmed.md`.
- **Research done:** `docs/research/20261014-code-map/DIGEST.md` and `FINDINGS.md`, and the COO's probe
  `runs/20261014-code-map-build/evidence/p1-callhierarchy-summary.md`.
- **The unclear-spot list:**

| Id | What is unclear | Kind | Blocks | Depends on |
|---|---|---|---|---|
| U1 | EJ has not yet accepted the vision and requirements (result-trimmed.md) | decision | P3 | — |
| U2 | How often `getImplementationAtPosition` misses an Effect service implementation, so that the static Effect rule (Layer.effect / Service.of → property → Effect.fn body) is needed; checked on one call site only | unknown | P3 (R2) | — |
| U3 | How a test links to the implementation it reaches when its file swaps a service for a mock (`Permission.node.replace(Layer.mock(...))`) | unknown | P3 (A3) | U2 |
| U4 | What counts as an "entry flow" of a module (spec: functions nothing in the module calls, or exported and used outside) | decision (proposed in spec) | P3 (A1), P4 | — |
| U5 | How siblings are detected (spec: files in one folder exporting the same shape) | unknown | P3 (A1), P4 | — |
| U6 | How `find` locates a place from a description in words, and whether its ranking is good enough | unknown | P3 (A2) | — |
| U7 | The answer keys were made by an explorer reading the code (43 claims confirmed by grep, 145 read). A plain-reading control can share their blind spot | unknown (risk) | P4, P5 | — |
| U8 | Codex quota at run time (it ran out on 2026-10-13) | information | P2, P3 | — |

- **Blueprint status:** the vision and requirements are a draft (relay result, trimmed), not yet accepted. The spec
  is v0, by the COO.
- **Tools proved in readiness** (`runs/20261014-code-map-build/readiness.md`): node 22, bun 1.4.3, `bun install` in
  opencode (2,161 packages), opencode core type-checks with tsgo and with tsc 5.8.2 (0 errors), and the four engines
  ran today. The LanguageService over core: 2.1 s, about 663 MB.
