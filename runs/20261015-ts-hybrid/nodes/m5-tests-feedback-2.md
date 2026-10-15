Repair: the full suite now runs against the M5 implementation — 633 pass, 1 fail. The failure is in your test, the
same bun behaviour found in M2: `dispatch: unsupported payload %j is a quiet success` times out after 5000 ms because a
`test.each` table holds an array element (e.g. `[]`) that bun spreads into zero arguments, so the callback's one
parameter is taken as a `done` callback ("this test timed out after 5000ms, before its done callback was called").
Wrap each element of that table in its own array (`[[null], [[]], …]`), and check every other `test.each` table in
`test/hooks.test.ts`, `test/cli.test.ts`, `test/doctor.test.ts` and `test/plugin.test.ts` for the same shape.
Change nothing else; do not read or change `src/`. Report `bun test` counts.
