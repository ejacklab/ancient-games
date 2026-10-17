# P4 re-judge — final map (builds/probe-final-tool.json) against the M2 key (Claude opus subagent)

Totals, 64 claims: **held 40, limited 13, missed 6, wrong 0, n/a 5.** On the A5 tool they were held 31, limited 0,
missed 27, wrong 2, n/a 4.

- **Limited (13):** places outside the query, now covered by one limit: "callers written in these folders were not
  searched: src, …".
  - M2.2d and M2.9d count as limited only because they sit inside a wide outside-repo record. Under a stricter
    reading they would be missed.
- **Missed (6):**
  - 4 test claims: the map holds no test links, and no limit names `test/`;
  - 1 constant and 1 interface, which are not definitions.
- **Ten random links:** 10 of 10 correct. 6 of them are easy library calls.
- **Still open:**
  - no entry for `Permission.reply`; its decisions appear only as nearby links;
  - no test reach in the map, with no limit saying so.
