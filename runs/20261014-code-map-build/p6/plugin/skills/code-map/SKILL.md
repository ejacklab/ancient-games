---
name: code-map
description: Answer one question about a TypeScript code base from its types — where something is defined, what calls it, what it calls, the call chain through one place, which tests reach a function, or a module map — each answer with file:line evidence and the limits where the analysis stopped. Use when exploring existing TypeScript code before a change, instead of reading many files, especially code that calls through injected services (Effect). NOT for running code, and NOT a proof that something is absent.
---

# code-map

One command per question:

    bun /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p4/tool-a5-src/cli.ts <command> <query> --project <package>/tsconfig.json --root <package> --tests 'test/**' [--json]

| Command | Answers |
|---|---|
| `where <name>` | where it is defined |
| `find "<code or words>"` | the places matching exact code, or ranked matches for a description; flags `ambiguous` |
| `callers <file:line or name>` | one level up, with each call site |
| `callees <file:line or name>` | one level down, with each call site |
| `chain <file:line> [--up N] [--down N]` | caller and callee chains, default 6 levels each way |
| `tests <file:line or name> [--fake-rule count\|exclude]` | the tests linked to it through the code, with the path for each |
| `map <path>... [--siblings <glob>]` | a whole module map; only when a module map is what you need |

- `<query>` paths are relative to `--root`.
- Every answer carries evidence (file:line) and `limits`: where and why it stopped (depth, dynamic, outside the
  repository, not found). An empty answer means this analysis found nothing, never that nothing exists.
- When `find` flags several places as ambiguous, pick the one that fits the question, build its chain, and name
  the others.
- Check a surprising answer by reading the cited lines.
