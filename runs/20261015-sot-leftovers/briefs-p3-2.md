# Brief — p3-review, attempt 2 (the repairs only)

A first review of a design change found three contradictions, now repaired. Judge only whether each repair fixes its
contradiction without making a new one. Do not fix anything; write nothing to disk.

- **C2** "a merge conflict in an entry is only in the lines added to it" was wrong once an entry's `covers` may be
  corrected in place. Repaired in W6.3a's text and in the prose's "Merge conflicts" paragraph.
- **C3** "Paths in this file are relative to its own folder" was wrong for `tools/`, `docs/index-md/` and the
  project's own paths. Repaired in the YAML's `kit` key.
- **C4** The limit a MUST (Rd3.1a) is checked against lived only in a guidance record (Rd3.1b). Repaired by stating
  the interim numbers in Rd3.1a.

Read only, in /home/smoke01/.claude/jobs/7d643882/tmp/review-sot-2: `SOURCE_OF_TRUTH.md`,
`SOURCE_OF_TRUTH_REQUIREMENTS.yaml` (both after the repair) and `full.diff` (the whole change, of which the repairs
are part). Nothing else.

Final message:

```
| contradiction | repaired? yes/no | evidence (file:line, quoted) |
|---|---|---|
## New problems the repairs made (or "none")
```
