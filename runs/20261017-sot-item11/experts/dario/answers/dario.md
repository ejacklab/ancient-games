# Answer — Five open points in the memory design's requirements (A–E)

## Answer
A: a merge keeps a removal that one side made and the other did not touch. B: the kit carries the tool and `docs/index-md/`. C: the project owner records the agents and their limits in one small limits file, not in `AGENTS.md` or the tool's constants. D: the set is the agents that load `INDEX.md` at session start. E: change the tool to read that file now, in its own run, and measure engines later, agy first, triggered by a comparison.

## How I decided
1. **A, merge and a removed path.**
   - W6.3a says "keeps both sides … every `covers` path either side wrote". That covers additions only, so a removal is unspecified.
   - A literal merge could bring the stale path back, because the untouched side still lists it.
   - The removal is never unexplained. K4.3 requires a `changed:` line for a correction, and W6.3a keeps both `changed:` lines, so the merged entry still says why the path went.
   - Wording for W6.3a: "Whoever does the merge applies both sides' changes to the common ancestor: both `changed:` lines, both links, every `covers` path either side added, and every `covers` path either side removed or replaced that the other side did not touch. If both sides changed the same path differently, the merger keeps the path that exists in the repository and says so in a `changed:` line."
   - Add to its `fails_if`: "… or a path one side removed or replaced, and the other side did not touch, is back in the merged entry."
2. **B, the kit.**
   - About a dozen records use `check: tool`, and K6.2 names the tool. Without the tool those records cannot be checked.
   - The YAML already treats `tools/` and `docs/index-md/` as paths in the repository root. So the design already assumes the tool is there, and the kit should say so.
   - Wording for `kit`: "The kit also carries `tools/memory_index.py` and `docs/index-md/` (its requirements and design). A record with `check: tool` is checked only by running the tool. Where the tool is not installed, that record is reported as not checked, never as passed."
   - A separate install would leave the design's checks depending on something it does not ship, and two copies would drift.
3. **C, where the limit is recorded.**
   - Use a small YAML file kept by the project owner, next to the index. The owner picks its name and location. The requirements are already YAML.
   - It has one entry per agent: the start file it loads, the limit with its unit, where the limit comes from (*measured on the engine*, *documented* with the page, or *the design's example*), and whether the agent loads `INDEX.md` at start (D).
   - Not `AGENTS.md`: it is prose the tool would have to parse, and agents load it at start, so it would spend the budget it describes.
   - Not the tool's constants: the owner would edit code to record a decision, and a reviewer could not see the sources.
   - The interim example applies while any entry's source is `example` or an agent has no entry. The tool prints which limit applies and from which source, so a reviewer sees when the interim stops.
   - Wording for Rd3.1a, replacing its second sentence: "The limits are read from the project's limits file, which the project owner keeps with one entry per agent that loads `INDEX.md` at session start, each with its unit and where the limit comes from. For an agent with no entry, the tool uses the example in Rd3.1b and says so in its output."
   - Rd3.1a then carries no numbers. Rd3.1b is the one place the example is written. The tool's two constants become the fallback, with a comment pointing to Rd3.1b.
   - The tool can count lines, bytes and characters. It cannot count tokens (agy's 20,000-token budget) or combined budgets (Codex, dsh). Those entries are recorded as such and reported "not checked by the tool", not guessed.
4. **D, which agents count.**
   - Choose the agents that load `INDEX.md` at session start. The limit exists so that an agent's start-file cut does not truncate the index. An agent that does not load it at start is not harmed by it.
   - Three places already say "read it": the Rd3 group title, the prose at `SOURCE_OF_TRUTH.md:157`, and the tool's own comment ("the agents that read it"). Only Rd3.1a says "work on the project", so it is the one to align.
   - Wording for Rd3.1a: "`INDEX.md` fits the strictest start-file limit among the agents that load it at session start."
   - In the limits file, an agent with no mark on whether it loads the index counts as loading it. A missing mark then makes the limit stricter, not looser.
5. **E, tool change and measuring.**
   - Change the tool now, in its own run. The change is small and testable, and it is what ends the three-place record of the numbers.
   - Tests: file present, file absent (falls back to the example and says so), file malformed (fails loud), and strictest taken per unit.
   - Measure later, by a comparison rather than a date: measure an engine when `INDEX.md` outgrows the lowest figure for that engine that is only *reported*, not verified.
   - Today that engine is agy. The official page says 24,000 bytes (*verified*), and one third-party page says 12,000 characters (*reported*). Which agy version either applies to is not measured.
   - The other engines have verified figures at or above the example. The research says the 200-line / 24,000-byte example is at or under every verified per-file figure. Codex and dsh limits are combined across files, so measuring them needs the real start-file set, not `INDEX.md` alone.

## What I need to know
- How big is a generated `project-memory/INDEX.md` today, compared with the lowest reported figure (12,000 characters)? I found no `INDEX.md` in this repo's own memory folder to check. If a real one is already above it, agy should be measured now, and the example is not safe for agy.
- Which agents actually load `INDEX.md` at start, and how: an import, a pointer in `AGENTS.md`/`CLAUDE.md`, or by hand? If none do, D's set is empty. Then "agents that work on the project" is the only set left, and the limit is really a read-tool limit.
- Does the tool already check that `covers` paths exist? If not, A's rule "keep the path that exists in the repository" has to be checked by the merger.
- Are projects given the kit by copy or by reference to this repository? That decides how bad drift is in B.

## Costs and risks
- **A:** the merger needs the common ancestor. A removal that was a mistake gets kept, though its `changed:` line makes it visible.
- **B:** the kit becomes code plus documents, so versions can drift between projects. A project without the tool has weaker guarantees. They are visible, but they are weaker.
- **C:**
  - One more file to keep, and it can be wrong. The tool trusts what the owner records, so a limit is only as good as its source label.
  - Token and combined-budget limits stay unchecked by the tool.
  - Rd3.1a, Rd3.1b, the tool comment and the `INDEX.md` prose must change together, or the numbers stay in three places.
- **D:** counting an unmarked agent as a loader can keep the limit stricter than needed. If an agent starts loading the index after a config change and nobody updates the mark, the limit is silently too loose.
- **E:**
  - The tool change touches `memory_index.py`, which has its own scope and tests, so it needs its own run.
  - A measurement costs engine runs and holds only for the installed version, with n=1 per engine.
  - Skipping it leaves agy's conflict open. If 12,000 characters is real, an index within the 24,000-byte example could be truncated on agy without any error.

## How we would know I was right
- **A:** a test with an ancestor entry `covers: [x, y]`. Branch 1 removes `y` with a `changed:` line. Branch 2 adds `z` with its own `changed:` line. The merged entry has `[x, z]` and both `changed:` lines. A merged entry with `y` back fails the new `fails_if`.
- **B:** copy the kit into an empty project. Every `check: tool` record either runs or prints "not checked", and none passes silently.
- **C:** searching the limits file for `example` shows the open interim. Changing one entry's source to measured changes the tool's printed source. Searching the design and tool for `24,000` and `200` finds only Rd3.1b and the tool's fallback.
- **D:** Rd3.1a, the Rd3 title, the prose and the tool comment all say the same thing. A test with two agents, one marked as not loading the index, gives the other agent's limit.
- **E:**
  - The tool tests above pass.
  - For agy, put a marker line at the end of a rule file longer than 12,000 characters and shorter than 24,000, and ask agy to quote the last line. If it can, the reported 12,000 does not bind the installed version. If it cannot, agy's entry in the limits file takes the lower figure.
