# P4 judge — map-tool.json (tool + permission) against the M2 key (Claude opus subagent)

## Map shape

The query was `src/tool` and `src/permission.ts`. The map holds:
- 212 definitions;
- 1,767 links;
- 10 entries;
- one sibling group of 15 members, with **0 rows**.

It has two limits:
- permission.ts:42-46, outside-repo;
- tool/mcp.ts:41-120, not-found.

Every link's `from` lies inside the query paths. So callers from outside them are absent, and no limit names them.

## Totals (64 key claims)

| Status | Count |
|---|---|
| held | 31 |
| missed | 27 |
| limited | 0 |
| wrong | 2 |
| n/a | 4 |

## Why claims were missed

| Cause | Claims |
|---|---|
| Callers or files outside the query paths, with no limit naming them | 12 |
| Tests: the map holds no test data | 4 (M2.8a–d) |
| `reply` is not an entry, so its steps are absent | 7 (M2.9a–g) |
| Not recorded: service injections (M2.3a, M2.10c), a plain const (M2.1d), an interface (M2.2a) | 4 |
| The sibling table has no rows, so no difference between read and write is recorded | 1 (M2.10f) |

## Why two claims were wrong

Both have the same cause. A `new X()` of a class defined in the same file carries the reason "implemented outside the
repository". This happens for DeclinedError at permission.ts:233, while the class is at :64. It happens for
BlockedError at :238, while the class is at :70. The same reason sits on every `new` of a local error class:
:142, :210, :269, :279 and :292.

## Ten random links

The judge drew ten links with Python, seed 20261017. 9 are correct and 1 is wrong:
- **#1358, wrong.** At webfetch.ts:109, `ctx.tool.transform` is reported as "implemented outside the repository".
  `ctx` comes from the workspace package `@opencode/plugin`, which is in this repository. At most it is outside the
  package root.
- **#374, correct as reported.** The same kind of call at mcp.ts:41 is reported as "not found", and a limit names it.
  The two reports disagree.

## What this does not establish

- The judge did not audit every link.
- The key is grep-based.
