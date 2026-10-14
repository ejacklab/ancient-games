# Research file — findings in a file, a digest to the COO

Research is written to files and never poured into the COO's context. Folder: `docs/research/<YYYYMMDD>-<topic>/`
(the repo's existing convention). Two files; the COO reads only the digest. Method §3.8 and §4.

## `FINDINGS.md` — the full record

```
# Findings — <topic>
Produced <date> by <who/what>. Question asked: <the question>.

| id | Finding | Label | Source |
|---|---|---|---|
| F1 | <one claim> | verified / reported / unproven / unknown | <URL, or file:line> |

## Gaps
<what was not read or could not be settled; a search that found nothing, with its query and where>
```

The Label is one of the four tags defined in `docs/RESEARCH_TAGS.md` (EJ, 2026-10-13) — the one copy; read it there.
Reading a primary document that only asserts the claim does not make it `verified`. Never upgrade a label. When
sources disagree, give both rows. An inference or a gap is prose, not a row, and carries no tag.

## `DIGEST.md` — the only part the COO reads (about 15 lines, no more than 20)

```
# Digest — <topic> (<date>)
Full findings: FINDINGS.md. Status: <open | parked | decided | negative result>.

**Answer.** <the answer to the question asked, in a few lines>
**Confidence.** <how many findings are verified / reported / unproven / unknown; what rests on one source>
**Cautions.** <what could make the answer wrong, or risky>
**Gaps.** <what to verify first>
**Decision it triggers.** <what EJ or the COO must decide because of this, or "none">
```

The digest is checked by `validate_result.py FILE --kind digest` (the three bold parts present, length capped). A
design that follows from the research is a decision: it becomes a decision entry in `project-memory/entries/` (method §4).

## Example

See `docs/research/20261002-whale-dolphin-hunting/DIGEST.md` and `docs/research/20261002-mods-plugins/DIGEST.md`.
