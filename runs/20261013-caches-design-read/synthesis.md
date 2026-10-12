# Synthesis — three rounds, four readers, the caches design

Written 2026-10-13 by the COO (Claude `claude-opus-5-5`) from `reviews/r1-*`, `r2-*` and `r3-*`. Nothing in `docs/`
has been changed from this run.

**Who took part:** claude (subagent), codex, opencode, agy in rounds 1 and 2. **Round 3 had three readers:** codex
failed with *"You've hit your usage limit … try again at 2:00 AM"* (`reviews/r3-codex.stderr.txt`), so codex's last
word is its round-2 discussion.

**Verdict:** all four said REPAIR in round 1. Nothing found changes a requirement's intent; every fix is wording,
a citation, or a leftover from today's changes. claude's round-3 list has 30 fixes (6 medium), opencode's 28, agy's 24.

## Agreed by all readers (medium)

| # | Where | What misleads | Fix |
|---|---|---|---|
| 1 | Rules, "Fall back when absent" | says a missing embedding model falls back to grep; Rd3.3 says full-text first | point at Rd3.3's order |
| 2 | Rd4.1 vs B1.1 | B1.1 runs when an agent notes "read through many hits", but Rd4.1 says every question other than a miss goes unrecorded — so that note can never be written | **EJ's call — see below** |
| 3 | Costs paragraph | the 226K tokens cites S-F13, which measured no tokens; the `INDEX.md` 0.01 s figure cites `SOURCE_OF_TRUTH.md`, which has no timing (it is opencode's, unresolved D4) | correct the citations |
| 4 | "Still unresolved" | "for memory entries all six stay open": D6 (triggers are comparisons) and D5 are settled, D1 answered by the proposed hybrid rule | say D2–D4 stay open |
| 5 | SEZA "my reading" | "K2 matters more here" — K2 checks the index against its files; SEZA's problem was outdated *content*, which K2 cannot catch; also "three stores" | reword |
| 6 | B1.1 example reading | "full-text wins much earlier: on SEZA-sized memory…" — its own SEZA source says *"n=5, no verdict"* | reword to match the source |

## Agreed, low (about 20)

Leftovers ("three caches", "three stores", the header note on Part 2); K2.3 needs "when both are built"; B1.2's "the
B1.1 question set" vs Rd4.2; the vector 5W1H When row lacks B1.0; the vector How row cites option A, which rebuilds
per hash (B3 forbids it); the "Rules" line "same set as `INDEX.md`" vs B4.1; and citations: V-F20 → V-F23 (absence),
S-F9 → S-F11 (hash), G-F18 (not a repo map), `G-F5 drift` at Rd3.4, M17 CONTESTED, Cursor's 12.5% vs the 1,000-file
figure, V-F6/V-F7 are code not memory, W-18 is an oracle not retrieval, the BM ids' sources, benchmark caveats (corpus
moved during the build; rg time ~16% high), the loader-cap "if", and the corpora list in "Not known".

## Still disputed after round 3 (all low)

K3.2's rerun events for full-text (3 hold, codex rejects); a noted miss whose entry is later superseded (3 hold, agy
rejects); the loader-cap cells (2–2); top 5 for the unranked `INDEX.md` arm (3 hold, agy rejects). The
"Unresolved after review" table: BM-9 settled (only a disclosure left), discovery-vs-exhaustive settled 3–1, corpus
snapshot and the audit's low findings still open.

## Needs EJ

**#2 only.** EJ dropped the question log and kept only misses. B1.1's run event ("an agent notes many hits") was
written in the same change and now has no place to be written. Either Rd4.1 also allows that one note, or B1.1 runs
only when EJ asks.
