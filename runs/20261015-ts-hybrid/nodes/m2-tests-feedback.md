Repair after the code node ran your tests (89 of 90 pass against the M2 implementation).

1. **A test bug, reproduced by the COO** (`/tmp/bunbug`): `test.each([null, undefined, 7, "failure", [], {}])` — bun
   spreads an array element into arguments, so the `[]` case calls the callback with **zero** arguments; the callback
   declares one parameter, and bun then treats that parameter as a `done` callback and waits 5 s:
   "this test timed out after 5000ms, before its done callback was called". Wrap every element of that table in its
   own array (`[[null], [undefined], [7], ["failure"], [[]], [{}]]`) or use `test.each` with objects, and check no
   other `test.each` table in the file has an array element that is not wrapped.
2. SPEC M2 now says `writeEvidence` and `appendRecord` drop raw-content keys (your tests already expect that) and
   `appendFailure` stores the strings it is given. Check your tests agree; change only a test that contradicts it.

Change nothing else. Run `bun test test/journal.test.ts` — the implementation now exists in `src/journal.ts` (do not
read or change it); report the pass/fail count.
