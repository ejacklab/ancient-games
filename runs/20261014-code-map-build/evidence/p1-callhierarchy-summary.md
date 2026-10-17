# Probe summary: TypeScript 5.8 LanguageService on opencode core (run by the COO, 2026-10-14)

Script: `p1-callhierarchy-probe.cjs`. Output: `p1-callhierarchy-probe-output.txt`. Target: `packages/core`
(tsconfig), commit `6dc4d4e`. The call site is `packages/core/src/tool/plugin/edit.ts:275`, `permission.assert(...)`.

| Probe | Result (measured) |
|---|---|
| Build the program | 425 root files, 2,259 source files, 2.1 s, about 663 MB heap |
| `getDefinitionAtPosition` | `permission.ts:106`, the interface member `readonly assert: (...)` |
| `getImplementationAtPosition` | `permission.ts:231`, `const assert = Effect.fn("Permission.assert")(...)`: the real implementation, through the Effect service |
| `findReferences` on the interface member | 19 references in 17 files, 12 ms |
| `prepareCallHierarchy` at the call site, the interface member, and the implementation | nothing: the stock call hierarchy does not handle property signatures or `Effect.fn` constants |

**My reading:**
- R2 (follow calls by type) is reachable with the stock LanguageService: references for the callers, implementation
  lookup for the target.
- The built-in call hierarchy is not usable for opencode's Effect style, so the tool must build its call edges from
  references and implementations itself.
- The 19 references were not checked one by one against the code.
