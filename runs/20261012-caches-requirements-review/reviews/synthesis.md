# Synthesis — three reviews of the caches requirements

Written 2026-10-12 by the COO (Claude `claude-opus-5-5`) from `codex.md`, `opencode.md` and `claude.md` in this
folder. All three: **REPAIR**. Nothing has been changed in `docs/` from these reviews; that waits for EJ.

**Checked by me against the sources** (marked ✓): the S-F9 citation, the V-F13 miss definition, the five trigger
lines in `CACHES.md`, the sibling `INDEX.md` rules, M6's status, and the benchmark's miss rule. The rest is the
reviewers' reading, not re-checked.

## All three agree

| # | Finding | Who | Needs |
|---|---|---|---|
| A | **Two full-text triggers.** B1.1 builds on a comparison; `CACHES.md:70-71`, `:79`, `:193`, `:209` and the vision's "Too many entries" build when `INDEX.md` can no longer list every active entry. ✓ | all | EJ picks one |
| A2 | **That size trigger collides with the sibling design.** `SOURCE_OF_TRUTH.md` K6.1: `INDEX.md` is "one line per active entry"; Rd3.1: it must fit the strictest start-file limit. ✓ Both cannot hold once entries outgrow the limit, and a cache does not fix that. | codex, opencode | EJ |
| B | **K3's cost has no unit.** B1 counts characters read; a rebuild prints nothing, so "includes any rebuild" adds zero. The accepted R8.2 compared time with time; the K3 example table is still in seconds. | all | EJ: time-vs-time, or drop the cost clause |
| C | **The comparison's scoring is undefined.** Per question or a mean? The benchmark leaves misses out of its mean ("A miss is left out, never scored 0", `bench/results.md:28` ✓), so routes are averaged over different question sets; it also had no `INDEX.md` arm. | all | wording, from EJ's choice in A |
| D | **K1.1 cites S-F9 for the content hash.** S-F9 is the mtime check K1.1 rejects ✓; the hash is S-F11 / S-F15. | all | fix citation |
| E | **Code-graph text still around the requirements**: the title, "Rules for all three caches" (cited by B4, K1, K2), the code-graph section and 5W1H. | all | mechanical |
| F | **EJ's build / keep / drop decision is recorded nowhere**, so the Fails-if clauses that check it can only be run by asking EJ. | all | add a decision record, or mark "(judged)" |
| G | **Concurrency and consistency**: two agents rebuilding at once; vector and full-text not required to rebuild in one step (V-F24's failure). | all (gaps) | new requirement |
| H | **The question record cannot replay a comparison**: no search terms, no corpus revision, no rule for which questions count; Rd4's Fails-if passes with one record. | all | tighten Rd4 |

## Two agree, or one with a check

| Finding | Who | Note |
|---|---|---|
| B1.2's miss definition drops "the asker's words share no term with it" from V-F13 ✓ | opencode | the Claude reviewer said it matches; V-F13 line 165-166 has the clause, so opencode is right |
| B1.2 passes on one lucky hit ("at least one") | opencode | the document itself says n=5–6 is too small to act on |
| B1.1's rerun event cannot fire: a miss needs full-text to have missed, and full-text does not exist yet | claude | my reading: correct |
| B4 compares against `INDEX.md`; should be the entries' own `status` | codex, opencode, claude | |
| Rd1 cites M18 (whole tree), not caches at start | opencode, claude | CP6 is closer |
| "Vector index" vs "hybrid index" in the same B1.2 block | claude | |
| Rd3.3 falls back to grep even when full-text works | claude | |
| Grep fallback can return superseded entries | codex | |
| Corpus boundary: `questions/`, `journal/`, `work/` not excluded | opencode | |
| M6 is CONTESTED in its source ✓; B2 and Rd3 don't say so | claude | |
| Items labelled *proposed* beside EJ's "write it" quotes | claude | EJ approved writing them in as proposed |

## Questions only EJ can answer

1. **Full-text trigger (A, A2):** the comparison (B1.1), or `INDEX.md` outgrowing its limit — and if `INDEX.md` must
   always list every active entry and fit, can the size trigger ever fire?
2. **K3 cost (B):** compare rebuild time with reading time saved (the accepted R8.2), or drop the cost clause and keep
   only "keeps passing its trigger"?

Everything else is wording, citations or a new requirement the reviewers spelled out.
