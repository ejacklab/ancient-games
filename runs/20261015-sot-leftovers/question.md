Method 3.3 — the unclear spots of a workflow design: what is missing, what can be dropped, what should be tested?

Asked of: Linus, 孫子, 老子, Dave (`--only linus,sun-tzu,lao-tzu,dave`). Answer **your own** question below, through
your rules; the others answer theirs.

- **Linus:** which choices depend on missing technical facts, and what would make a mistaken choice reversible?
- **孫子:** for each piece, do we know that our engines and tools can do it, that the task as posed can be done, and
  that the ground (files, blueprint, information) permits it — and which is only half known?
- **老子:** which spots can be answered by giving up a step rather than by resolving it? (Say what would be lost.)
- **Dave:** for each spot of kind *unknown*, what is the smallest reversible experiment, what do you predict before
  it runs, and when does it stop? Leave any threshold EJ has not given open.

In "Answer", list spot ids (existing ones, or new ones you raise as N1, N2 …) with your verdict for each. Do not
decide for EJ: a spot to drop is a question for EJ, not a removal.

Facts (filled in by the COO):
- **The challenge and its restatement:** EJ, 2026-10-15: *"fix the item 10 leftovers with a proper designed
  workflows"*. Objective: five leftovers of a review of the source-of-truth memory design are fixed in its three
  files (`SOURCE_OF_TRUTH.md` prose, `SOURCE_OF_TRUTH_REQUIREMENTS.yaml` requirements, release notes), or settled as
  decisions and recorded. The five: L1 W6.3b says `check: tool` but K6.3b, which it points to, says `reviewer` (the
  tool cannot see whether a merge was done by hand, only whether the result matches); L2 K4.3 says that after its
  first commit an entry only gains a `changed:` line, a new `status`, the `superseded_by` link and `done:`, so a stale
  `covers` path can only be fixed by superseding the whole entry; L3 the YAML's `basis` and two records point to
  `vision-statements/source-of-truth-memory-vision-statements.md` and `CACHES.md`, which exist only in this repo's
  `docs/memory-system/`, though the design is meant for any project; L4 a prose typo ("When the work a decision to
  build something is complete"); L5 Rd3.1a (MUST: `INDEX.md` fits the strictest start-file limit among the agents
  that work on the project; the check fails when it does not) has `who_decides: unassigned` for which agents work on
  the project, while `tools/memory_index.py` hard-codes `MAX_LINES = 200` and `MAX_BYTES = 24_000`, commented as "the
  design's example, not a measurement"; `docs/index-md/` B4.1 says the same. In scope: the three design files and
  the YAML's build script. Out of scope: the tool, `docs/index-md/`, measuring engine limits, `CACHES.md`.
- **The algorithm:** `runs/20261015-sot-leftovers/workflow-design.md` — P1 experts and EJ's decisions; P2 the COO's
  edits (L1, L4, L3; then L2; then L5), checked by the YAML's build script (loads, one shape, unique ids, all 46
  requirements covered, links resolve) and a path check; P3 a blind Claude Sonnet review of the diff against L1–L5
  with one planted contradiction; P4 close (release note, state, commit on EJ's word).
- **The unclear-spot list:**

  | id | What is unclear | Kind | Blocks | Provisional assumption |
  |---|---|---|---|---|
  | U1 | May `covers`, `source`, `depends_on` change after the first commit, each with a `changed:` line (claim, id, kind still never change)? | decision | the L2 edit | yes |
  | U2 | Who decides which agents work on the project (Rd3.1a)? | decision | the L5 edit | the project owner |
  | U3 | Does the tool keep the example limit (and Rd3.1a says so), or is it built to read limits from a file? | decision | the L5 edit | keep it; the build goes to the backlog |
  | U4 | Each engine's real start-file limit | unknown | nothing in this run (out of scope) | backlog |
  | U5 | Make paths relative to the design's folder, keeping the vision file and `CACHES.md` as siblings? | decision | the L3 edit | yes |

- **The blueprint status:** the design is EJ's accepted product; its requirements were reviewed twice by the four
  experts in the last two days. Not a code change.
- **Tools proved in readiness:** the YAML build script ran and passed on 2026-10-15 (64 records). The four expert
  engines ran on 2026-10-15 (`runs/20261015-sot-final-review/`). A Claude Sonnet subagent ran on 2026-10-14.
