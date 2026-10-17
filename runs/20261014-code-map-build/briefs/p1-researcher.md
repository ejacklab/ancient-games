# Research: how a TypeScript tool should follow calls in opencode, and what already exists

You are the researcher (method 3.8 item 9). Write your findings to
`docs/research/20261014-code-map/FINDINGS.md` and `DIGEST.md`, following `docs/workflow-templates/research-file.md`.
The labels are defined in `docs/RESEARCH_TAGS.md`. Your final message is the digest plus the path.

## Context

We are building a code-map tool in TypeScript (EJ's decision). Its requirements are in
`runs/20261014-code-map-vision-relay/result-trimmed.md`; read R2, A2 and A3 first.

The target is opencode, at `runs/20261014-opencode-code-map/src/opencode/`, commit `6dc4d4e`. Its dependencies are
installed, and `packages/core` compiles with its own TypeScript 5.8.2 (`node_modules/.bin/tsc`, 0 errors). opencode
injects services through Effect, for example `yield* Permission.Service` in
`packages/core/src/tool/plugin/edit.ts:215`, with the interface at `packages/core/src/permission.ts:106` and the
layer at `:121`.

## Questions

1. **The TypeScript LanguageService call hierarchy** (`prepareCallHierarchy`, `provideCallHierarchyIncomingCalls`,
   `provideCallHierarchyOutgoingCalls`):
   - Is it in TypeScript 5.8, and what does it return?
   - For a call on an object typed by an interface, such as `permission.assert(...)`, does it give the interface
     member, the implementation, or nothing?
   - Run a small script against opencode's own TypeScript to see, and save the script and its output under
     `runs/20261014-code-map-build/evidence/p1-*`.
2. **ts-morph** (`findReferences`, `getDefinitions`, `getImplementations`): what does each give for the same call?
   Run it too, if it is quick to install in a scratch folder under `runs/20261014-code-map-build/evidence/`.
3. **Effect's service pattern:** how is an implementation bound to a service tag? Look at `Context.Service`, `Layer`,
   and opencode's `makeLocationNode` / `deps`. What static rule links a call on a service to the function that
   implements it?
4. **Existing tools** that could do part of this, and how well each fits R2, A2 and A3. Name the ones you check, for
   example scip-typescript, dependency-cruiser, madge, or a TypeScript call-graph library.
5. **Cost:** the time and memory to build a LanguageService program over `packages/core`, measured.
6. **Tests:** how opencode's tests are laid out (runner, file pattern), and how a test can be linked statically to
   the functions it reaches.

## Rules

- Measured or quoted claims only. Anything else is labelled `unproven` or written as a gap.
- Do not change any file outside `docs/research/20261014-code-map/` and
  `runs/20261014-code-map-build/evidence/`.
- Do not run opencode itself, its tests, or any network service.
