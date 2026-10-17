# P4 re-judge — final map (builds/probe-final-ai.json) against the M3 key (Claude opus subagent)

Totals, 63 claims: **held 37, limited 5, missed 18, wrong 0, n/a 3.** On the A5 tool they were held 25, limited 9,
missed 20, wrong 6, n/a 3.

- **Missed (18):**
  - 11 lie outside the map's scope (packages/core and `test/`), and no limit records that scope;
  - 7 lie inside it: an interface and constants, which are not definitions; one decision step (no entries); and no
    sibling comparison of the providers (the chat protocols group was the one given).
- **Wrong:** the earlier wrong links are all resolved now:
  - `Auth.header` and `Auth.bearer` resolve, and so does `Tool.make`;
  - `transport.prepare` and `transport.execute` are ambiguous, listing the implementations.
- **Ten random links:** 10 of 10 correct. 7 of them are easy library calls.
