# Readiness — 20261014-code-map-build (P0, 2026-10-14)

| Item | Status | Evidence |
|---|---|---|
| node 22.22.1, python3 3.12.3, git, claude 2.1.299, codex 0.160.0, agy 1.3.5, opencode 1.18.34 | verified | `evidence/p0-readiness-inventory.md` (readiness.py) |
| dsh | verified by use | the relay and the expert runs today, exit 0 (`runs/20261014-code-map-vision-relay/step-3-sun-tzu/status.json`) |
| Engines run a task (codex, agy, dsh, opencode) | verified by use | every one ran today with exit 0 and answered |
| bun | verified | `npm install -g bun` → 1.4.3. opencode pins `bun@1.4.2`; the patch version differs |
| opencode dependencies | verified | `bun install --frozen-lockfile`: 2,161 packages in 12.35 s, node_modules 3.1 GB (`evidence/p0-bun-install.txt`) |
| opencode core type-checks (tsgo) | verified | `bun run typecheck` in packages/core, exit 0 |
| opencode core compiles with the TypeScript 5.8.2 compiler API | verified | `tsc -p tsconfig.json --noEmit`, exit 0, 0 errors, 18.3 s (`evidence/p0-core-tsc58.txt`). The API ts-morph uses can load core |
| This repo's baseline | verified | `pytest -q`: 685 passed in 40.25 s (`evidence/p0-pytest.txt`) |
| Pinned commit | verified | opencode `6dc4d4e` (2026-10-13) |

Unknown: Codex quota at run time (it ran out on 2026-10-13).
