# INDEX.md changes to the design (codex)

*proposed* — This is a proposal for EJ to decide. No files were changed and no tests were run. All new **Fails if** checks below are written by codex; they are review criteria, not independent evidence that the implementation meets them.

*design* — Sources: the [accepted memory design](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md), [settled vision](/home/smoke01/dev/ancient-games/docs/memory-system/vision-statements/source-of-truth-memory-vision-statements.md), and the INDEX.md [requirements](/home/smoke01/dev/ancient-games/docs/index-md/REQUIREMENTS.md) and [design](/home/smoke01/dev/ancient-games/docs/index-md/DESIGN.md).

*proposed* — Requirement check: **source, unit, can it fail, basis and links — PASS** with the labels, citations and checks below. **One thing — FAIL** in the combined regeneration/commit and size/check statements; these are separated below. **Weak words — FAIL** where the ID form and reader limits remain unspecified; both remain explicitly open. **Level — PASS** when output consistency is treated as a requirement and the commands describe its method. The recommendations are design judgement, **not measured**; reconsider them when EJ decides this set.

## 1. K6.2 and When to write

*proposed* — **Recommendation:** Make the proposed change for every entry creation or edit, but require matching committed index content rather than an index diff when regeneration produces identical bytes.

*design* — **Reason:** K6.1 says, “one line per active entry, showing its id, kind and one-line claim”; this includes lessons, observations and hypotheses, and a status change can remove a line.

*proposed* — **Replace K6.2:** “After any entry is created or changed, whoever writes it regenerates `INDEX.md` immediately. This applies to every kind and every status change.”

*proposed* — **Add a separate sentence to K6.2:** “The commit containing the entry change contains the index generated from that commit’s entries. If regeneration produces identical bytes, no index file change is required.”

*proposed* — **K6 Fails if:** “Regenerating the index from a committed snapshot produces different bytes from that snapshot’s `INDEX.md`, or the index lists a superseded or retired entry. For K6.2’s timing, it also fails if a reviewer observes entry writing completed without regeneration.”

*proposed* — **When to write — replace the Immediately row’s What cell:** “Decisions and facts, before the code. A human correction. The state of unfinished work before a handoff, an interruption or a context reduction.”

*proposed* — **When to write — add a row:** **When:** “Immediately after any entry is created or changed.” **What:** “Regenerate `INDEX.md`, for every kind and every status change.”

*proposed* — **Add after the table:** “The entry change and its matching generated index are committed together (K6.2). Regeneration that produces identical bytes requires no index diff.”

*proposed* — **Replace K6’s Open line:** “Generator: `python3 tools/memory_index.py`, run by whoever creates or changes an entry. Stage new entries before running it. Stage the regenerated index before committing. The script does not stage or commit files.”

*proposed* — **Add implementation guidance under K6:** “The committed git hooks run the snapshot check when enabled for a clone. They are a convenience, not the guarantee. The tests also check the committed snapshot when the test suite runs.”

*proposed* — **Replace Still open under When to write:** “`INDEX.md` generation is described in K6; entry-file conflict resolution is described in W6. Whether a changed decision is edited in place or superseded remains proposed in K4.3.”

## 2. K6.3, never hand-merge

*proposed* — **Recommendation:** Add K6.3 as proposed and name whoever is carrying out the merge as the entry-conflict resolver.

*design* — **Reason:** K6.1 already says, “It is never edited by hand”; resolving a conflict by editing generated lines would bypass that rule.

*proposed* — **Add K6.3:** “`INDEX.md` is never hand-merged. When it conflicts, resolve the entry files first, then regenerate `INDEX.md` from those entries, stage it and complete the merge.”

*proposed* — **K6.3 Fails if:** “A reviewer observes conflict resolution by hand-editing `INDEX.md`, or the merged index differs from regeneration over the merged entries.”

*proposed* — **Replace W6’s Open line:** “Whoever carries out the merge resolves conflicts in the entry files and records entry changes under W4.2. This does not override Rd5.3: a reader who discovers a decision/code mismatch reports it for EJ to decide.”

*proposed* — **W6 Fails if:** “An edit to an entry is lost without a conflict. It also fails if conflict resolution changes an entry without the `changed:` line required by W4.2.”

*proposed* — Regeneration resolves the generated file’s content; it does not establish that the merged entries agree in meaning.

## 3. Rd3.1, who checks the size

*proposed* — **Recommendation:** Make the proposed wording change, while keeping the actual reader limits explicitly open.

*design* — **Reason:** INDEX.md requirement C2.1 says, “`tests/test_memory_index.py` runs under the repo’s `pytest`”; this names an existing check path without inventing a build step.

*proposed* — **Replace the matching line before Core requirements:** “`INDEX.md` must fit the strictest start-file limit of the agents that read it (Rd3). The generator checks its size. The tests exercise that check.”

*proposed* — **Replace Rd3.1:** “`INDEX.md` fits the strictest start-file limit among the agents that read it.”

*proposed* — **Add separate checking sentences to Rd3.1:** “`tools/memory_index.py` checks the index against the configured size limits; its check mode fails on overflow. `tests/test_memory_index.py` exercises the size check and checks the committed snapshot when the tests run.”

*proposed* — **Add an Open line under Rd3:** “Which agents and load paths read `INDEX.md`, the units those paths limit, and their measured limits. The examples in `CACHES.md` are examples, not measured acceptance limits.”

*proposed* — **Rd3 Fails if:** “`INDEX.md` exceeds a reader’s measured start-file limit. It also fails if check mode accepts an index above a configured limit, or the tests do not exercise rejection of an oversized index.”

*design* — INDEX.md requirement B4.1 explicitly says its current constants come from the design’s example “until” the readers’ load paths are measured.

*proposed* — Passing the script’s configured limits therefore does not yet establish that every reader can load the index. The existing test suite was inspected, not executed; its authorship was not established by this review.

## 4. W1.1, the id

*proposed* — **Recommendation:** Add the branch-independent allocation rule and duplicate rejection, leaving the identifier form open for EJ.

*design* — **Reason:** W6.2 says, “Each agent works on its own branch or worktree”; choosing the next free number from a branch’s entries cannot account for additions on another branch.

*proposed* — **Append to W1.1:** “An entry’s `id` is non-empty and unique across all entries, including superseded and retired entries.”

*proposed* — **Add a separate allocation sentence:** “Writers choose new IDs without coordination between git branches; an ID is never allocated as ‘the next free number’ from the entries visible on one branch.”

*proposed* — **Add a separate checking sentence:** “The index generator rejects duplicate IDs in the snapshot it reads.”

*proposed* — **Add an Open line under W1:** “The form and local generation method of an entry ID.”

*proposed* — **W1.1 Fails if:** “An entry has an empty ID, two entries share an ID, or a writer allocates an ID by taking the next free number from its branch. The existing filename, prefix and kind checks still apply.”

*proposed* — This separates allocation from validation: checking one branch cannot establish uniqueness against unseen entries on another branch. A locally generated form still needs duplicate rejection when branches meet.

## 5. W1.2 and W1.3, the format

*proposed* — **Recommendation:** Adopt the explicit header boundaries and literal section markers, while retaining every existing field and section requirement.

*design* — **Reason:** W1.3 already says, “The body is the claim in one or two sentences, then **Why:**, then **How to apply:**”; specifying their literal markdown spelling makes that structure readable by both people and the generator.

*proposed* — **Append to W1.2:** “The file begins on its first line with `---`. The header ends at the next line containing exactly `---`.”

*proposed* — **Add a separate field-format sentence:** “Header fields use `key: value` form. The `id`, `kind` and `status` fields are unindented top-level fields with their values on the same line.”

*proposed* — **Add a separate parsing sentence:** “For these three fields, the generator removes surrounding whitespace and one matching pair of surrounding single or double quotes.”

*proposed* — **W1.2 Fails if:** “A required field is missing, the opening or closing header delimiter is missing, or `id`, `kind` or `status` appears only as an indented field rather than a top-level field.”

*proposed* — **Replace W1.3:** “The body begins after the closing header delimiter. It contains one claim in one or two sentences.”

*proposed* — **Add separate section sentences:** “The claim ends at the first line beginning with the literal markdown `**Why:**`. The reason follows that marker. A later line begins with the literal markdown `**How to apply:**`, followed by how to apply the claim.”

*proposed* — **W1.3 Fails if:** “The claim is empty, a reviewer finds more than one claim, or either section marker is missing, indented, spelled differently or placed out of order.”

*proposed* — **What will be put in — replace its body-description sentence:** “Its header uses the delimiters and field format in W1.2. Its body contains the claim, then the literal `**Why:**` marker, then the literal `**How to apply:**` marker, as specified in W1.3.”

*proposed* — The generator’s limited validation does not reduce W1’s requirements. In particular, accepting an entry for indexing does not establish that its author, evidence, change log and How to apply section are present.

## What could go wrong

*proposed* — Two branches edit the same decision: one changes its claim and the other changes its How to apply section. Git merges the different lines cleanly. Regeneration produces a matching index and the snapshot check passes, but the entry now gives contradictory instructions.

*design* — The accepted design warns, “a clean merge does not mean the file is consistent.”

*proposed* — This case requires reading the merged entry. Neither regeneration nor a matching index proves semantic consistency.

## Questions for EJ

*proposed* — What locally generated ID form should W1.1 name—for example, a randomly generated UUID? The form remains open in this proposal.

*proposed* — Which agents and load paths must read `INDEX.md`? Their measured limits and counting units would replace Rd3’s open line and the script’s example limits.
