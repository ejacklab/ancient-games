# 范蠡 (Fan Li) — review of the memory workflow enhancement

## Answer
I recommend **accept with changes**: accept the four-field memory table, the cache constraints, and the omission of both Linus's per-node contract and 老子's keep-when-named rule, but restore `changelog.md` to the product blueprint as a run and release output, correct the citation for covered paths, and establish `project-memory/` before directing workflows to write into it.

## How I decided

1. **Does it do what EJ asked?** EJ asked to *"enhance the workflow design algorithm to remind the ai agent when and how to use memory more effectively. both the source-of-truth and caches"*. The COO's change places memory requirements into four existing node fields (Context, Contract, State, Tools) and specifies delivery by brief, import, or start hook rather than relying on optional agent reads. This joins external timing with execution: as my #1 states, 「夫聖人隨時以行，是謂守時。天時不作，弗為人客；人事不起，弗為之始。」 (`quoted`) — "The sage moves with the time; this is called keeping to the time. When Heaven's time has not arisen, do not be the guest [the attacker]; when human affairs have not arisen, do not be the one who begins." Delivering memory from outside provides the timing the model lacks, while leaving execution to the node.

2. **Grounding in existing fields avoids excess.** Placing memory into Context, Contract, State, and Tools follows my #2: 「夫國家之事，有持盈，有定傾，有節事。」/「持盈者與天，定傾者與人，節事者與地。」/「天道盈而不溢，盛而不驕，勞而不矜其功。」 (`quoted`) — "In the affairs of a state there is keeping the full, steadying the tilting, and regulating affairs." / "Keeping the full goes with Heaven; steadying the tilting goes with people; regulating affairs goes with Earth." / "Heaven's way is full but does not overflow, flourishes but is not arrogant, labours but does not boast of its work." Regulating affairs goes with Earth: anchoring memory in concrete fields already present in every node regulates work without overflowing into redundant abstractions.

3. **Call (b) — Linus's per-node contract.** The COO left out Linus's separate per-node memory contract. That call should be **kept**. Repeating the full rules of `SOURCE_OF_TRUTH.md` inside every node creates a second copy that will drift. In my #11, 「用力甚少而名聲章明，種亦不如蠡也。」 (`quoted`) — "very little force is used and the name shines — in this 種 is not as good as I." A concise reference in the existing fields uses very little force; a bespoke per-node contract structure is more force than the work requires.

4. **Call (b) — 老子's keep-only-when-named rule.** The COO left out 老子's rule. That call should be **kept**. `SOURCE_OF_TRUTH.md` was accepted by EJ on 2026-10-12, with W4.1 establishing that anyone may write with no owner and no approval, and K5.2 establishing that the agent writes what is worth keeping. 老子's rule contradicts those accepted requirements. In my #5, 「夫謀之廊廟，失之中原，其可乎？王姑勿許也。…贏縮轉化，後將悔之。天節固然，唯謀不遷。」 (`quoted`) — "To plan it in the temple hall and lose it on the central plain — can that be right? For now, do not accept. … Advance and retreat change into each other; later you would regret it. Heaven's rhythm is like that; only the plan does not move." A plan accepted at court should not shift in the field without EJ's explicit command; to introduce an unapproved gate invites contention, and in my #13, 「爭者，事之末也。」 (`quoted`) — "contention is the last of affairs."

5. **Call (a) — dropping `changelog.md`.** The COO dropped `changelog.md` along with `decisions.md` and `lessons.md`. That call must be **changed**. As method §4 already states, a release note is an output for users, not memory, and `changelog.md` records which run changed what, criteria covered, baseline results, and user release notes. `SOURCE_OF_TRUTH.md` does not track runs or release notes, and W3.1 explicitly excludes commit logs from memory entries. Dropping `changelog.md` strips the product blueprint of its run record and release-note generator without human affairs asking for it. Per my #1, 「人事不起，弗為之始。」 (`quoted`) — "when human affairs have not arisen, do not be the one who begins." EJ asked about memory, not about abolishing the run changelog.

6. **Fidelity to requirement ids.**
   - `CACHES Rd1`, `B1`, `Rd2`, and `CACHES § When to use which store` are cited accurately and match `docs/memory-system/CACHES.md`.
   - `SoT Rd5`, `W5.1`, `W5.3`, `K5.2`, and `K6.2` match `docs/memory-system/SOURCE_OF_TRUTH.md`.
   - In `docs/WORKFLOW_DESIGN_METHOD.md` §4 (table row **Context**, diff line 86), the text cites `(SoT Rd2.1)`. Rd2.1 governs session-start loading; selecting entries covering a path is **Rd4.1** (`covers`). Rd2.1 establishes delivery ("never as a sentence asking it to read them"). It should cite `(SoT Rd2.1, Rd4.1)`. (my reading)

7. **Examining the preparations.** In my #18, 「審備則可以戰乎？」王曰：「巧。」 (`quoted`) — "'If the preparations are examined, can we then fight?' The king: 'Skilful.'" In `docs/WORKFLOW_DESIGN_METHOD.md` line 474 (diff line 47), line 500 (diff line 56), and line 530 (diff line 88), the method directs nodes to write decision entries to `project-memory/entries/` and regenerate `INDEX.md`. However, `project-memory/` does not yet exist in this repository. In my #3, 「時不至，不可彊生；事不究，不可彊成。」 (`quoted`) — "When the time has not come, growth cannot be forced; when the matter has not run its course, completion cannot be forced." Before ordering workflows into the field, the preparation must be examined: either `project-memory/entries/` must be initialized on disk, or an interim note must instruct designers to initialize the directory prior to the first run that writes to it.

### Exact changes required

**Change 1 — Restore `changelog.md` to `docs/workflow-templates/blueprint.md`**
In the directory tree (lines 18–20):
```markdown
  backlog.md             what a run found that neither its acceptance criteria nor its baseline covers; never
                         worked on inside the run that found it
  changelog.md           append-only: one entry per run that builds; release notes come from it
```
And restore its section below `backlog.md`:
```markdown
## Run log and release notes — `changelog.md`

Append-only: one entry per run that builds, written by the COO from the state file. Release notes, when needed, are generated from its `Release note` lines.

| Date | Run id | What changed | Criteria covered | Commits | Baseline result | Release note (optional, for users) |
|---|---|---|---|---|---|---|
```

**Change 2 — Fix citation in `docs/WORKFLOW_DESIGN_METHOD.md` §4**
In `docs/WORKFLOW_DESIGN_METHOD.md` §4 table, row **Context**:
Replace:
```markdown
| **Context** — memory in | The entries the node needs, named by id or by the paths they cover, and how they reach it: in the brief, by an import, or by a start hook, never as a sentence asking it to read them (SoT Rd2.1). What it must not receive: a verifier gets no worker's reasoning, and no entry or journal that carries it. |
```
With:
```markdown
| **Context** — memory in | The entries the node needs, named by id or by the paths they cover, and how they reach it: in the brief, by an import, or by a start hook, never as a sentence asking it to read them (SoT Rd2.1, Rd4.1). What it must not receive: a verifier gets no worker's reasoning, and no entry or journal that carries it. |
```

**Change 3 — Note store initialization in `docs/WORKFLOW_DESIGN_METHOD.md` §4**
Immediately before the table in §4, append:
```markdown
Where `project-memory/` is not yet initialized in a repository, the designer ensures `mkdir -p project-memory/entries` is staged before running a workflow that writes memory entries.
```

## What I need to know
1. Does EJ intend for `project-memory/` to hold a record of run completions and user release notes, or does `changelog.md` remain the dedicated build output beside the blueprint? If EJ intends project memory to absorb run records, a new entry kind or requirement must be added to `SOURCE_OF_TRUTH.md` first; if not, `changelog.md` remains in the blueprint as proposed above.

## Costs and risks
1. **Retaining `changelog.md` keeps two recording locations** (my #2): run summaries live in `docs/blueprint/changelog.md` while decisions and lessons live in `project-memory/entries/`. The price is maintaining the distinction between a build output and project memory.
2. **Omitting Linus's contract relies on designer discipline** (my #11): without a rigid per-node template, a careless designer might fail to populate Context or State with memory paths. The price is catching omissions during plan review rather than enforcing them mechanically in every brief.
3. **Waiting on store creation pauses automated memory emission** (my #3, my #18): until `project-memory/entries/` is created, nodes cannot commit entries or regenerate `INDEX.md`.

## How we would know I was right
1. **Run changelog test:** In the next build run, verify that run results, criteria covered, and user-facing release notes are preserved in `docs/blueprint/changelog.md` without polluting `project-memory/entries/` with commit-level churn.
2. **Delivery verification:** Inspect the next designed workflow to confirm that required memory entries appear directly in node briefs or imports (with citation to Rd2.1 and Rd4.1), with zero prompts asking the agent to search for them unguided.
3. **Store integrity:** Running `python3 tools/memory_index.py --check` on a repository with initialized `project-memory/entries/` passes cleanly with no missing-directory error.
