# P4 judge — map-ai.json against the M3 key (Claude opus subagent)

## Map shape

- **Query:** `src` in packages/ai.
- **Definitions:** 1,655.
- **Links:** 8,961 in all — 3,049 resolved, 31 ambiguous and 5,881 unresolved.
- **Entries:** 0.
- **Siblings:** one group of 7 chat protocols, with **0 rows**.
- **Limits:** 3.
- **Not in the map:** no file under packages/core, and no file under `test/`.

## Totals (63 key claims)

| Status | Count |
|---|---|
| held | 25 |
| missed | 20 |
| limited | 9 |
| wrong | 6 |
| n/a | 3 |

**Missed (20).** 11 lie outside the package: 8 in packages/core and 3 test files. No limit declares that scope. The
other 9 are inside it:
- constants and interfaces, which are not definitions in the map;
- a decision step (no entries);
- sibling rows.

## Wrong claims (6)

- **Calls to overloaded functions, 4 of the 6.** They come out unresolved with "no implementation of X was found".
  The judge checked four functions:
  - `Auth.header` (route/auth.ts:129);
  - `Auth.bearer` (:122);
  - `makeTool` (tool.ts `make`, :167);
  - `canCompact` (client.ts).

  Each is defined in the repository and listed in the map's own definitions. A rough count by the judge (not an
  exact measure) found 162 unresolved links whose target name has several definitions. The largest groups are
  `Route.make` (50) and `route.with` (22).
- **Calls dispatched through an interface, 2 of the 6.** They resolve to one implementation only, not to all of
  them:
  - `transport.prepare` at client.ts:414 resolves to gemini.ts only. It misses http.ts:85 and websocket.ts:455.
  - `transport.execute` at :426 does the same.

## Random links

- 10 links drawn at random: all 10 correct. 9 of them are easy library calls.
- 10 resolved links drawn at random: all 10 correct.

The samples check that a link is precise, not that the map is complete.
