2026-10-17T15:33Z — locations — done; copied tool: 2 pass, 1 fail (empty sibling table without an explanation)
2026-10-17T15:33Z — source accuracy — done; copied tool: 5 pass, 0 fail
2026-10-17T15:33Z — known items — done; copied tool: 5 pass, 3 fail (silent empty table; shared validation and differing preparation absent)
2026-10-17T15:34Z — full suite and handoff — done; bun test test/a1: 13 pass, 3 fail; all failures explained in staging/a1-tests-report.md
2026-10-17T15:35Z — shape 1: local class built with new — done; map and callees fail: inherited constructor reported outside the repository.
2026-10-17T15:40Z — shape 2: factory value taken with yield* — done; map and callees fail: steps.attempt reported outside the repository (the wrapper type in effect-runtime.ts is named, not the written attempt).
2026-10-17T15:40Z — shape 3: overloaded function through a namespace — done; map, callees and callers fail: overload signature has no body, link unresolved "no implementation of Auth.header was found".
2026-10-17T15:40Z — shape 4: interface with three implementations — done; map and callees fail: ambiguous with 2 of 3 candidates, the object returned by fileTransport() is missing.
2026-10-17T15:40Z — shape 5: linked workspace package — done; map and callees fail: openLedger reported outside the repository (program keeps the node_modules link path, so the file is not source).
2026-10-17T15:40Z — shape 6: edges of the paths given — done; map fails (no src/b caller, no limit naming the scope); callers passes.
