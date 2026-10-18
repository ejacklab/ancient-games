# Answer — Two owner choices: send unanswerable questions to the owner at once (Q1), and list Claude Code's own memory in memory-check (Q2)

## Answer
**Q1: pick (a).** Send a question to the owner at once when the agent can name who decides (the owner) and show that no check exists that could fail a wrong choice. Questions that don't meet that test keep the three-trial path.
**Q2: pick (a).** F1 also lists `~/.claude/projects/<path>/memory/`, reported present or absent only, with no format check and no file names or contents in the report.

## How I decided
1. **I checked the facts in the brief.**
   - *Q1:* method 3.8 item 14 says a question goes to the owner "only after three failed trials on it, or once the time the owner gave is used up" (verified: read). A trial is "one provisional choice tried and checked".
   - *Q2:* F1 does look only for `<home>/.claude/agent-memory/<name>/`, plus the project-root locations (verified: read). The Claude Code memory folder holds 49 `.md` files including `MEMORY.md` (verified: counted), so "about 50" is right.
2. **Q1: a trial can only answer a question that has a check.** A failed trial is one that fails its check. If nothing could fail a wrong choice, each trial returns no information, and three of them only delay the question. A threshold only the owner can set is the clearest case.
3. **Q1: the three examples are not equally unanswerable.** "Which location a requirement names" is settled by reading the guidelines. F1 itself says "Who decides: the guidelines". "Whether a real project exists" is settled by looking, unless the project exists only in the owner's world. So the rule needs a test, not the three examples, or the agent will send answerable questions to the owner. That is why I attach the "who decides, and what check would fail a wrong choice" test to (a).
4. **Q1: in a time-boxed run, (a) changes little.** The experts already advise, the main agent already decides provisionally, and the owner already accepts or declines at the end. What (a) adds is that the agent skips trials 2 and 3 on that question, and the owner's end-of-run list marks it "owner-only". The owner then sees which items are theirs alone and which a check already tested. In an untimed run the gain is larger, because nothing else forces the question out. While it waits, the run keeps working on pieces that don't depend on it, as the method already says.
5. **Q2: rule out (b).** The Claude Code folder does not follow the guidelines' entry format, so a format check would fail or skip every file. That would be the tool judging against a rule nobody wrote for it.
6. **Q2: (a) over (c).**
   - F1 already reports a location in the home folder that belongs to the harness. Claude Code has a subagent-memory feature that stores files under `~/.claude/agent-memory/<name>/` (recall, not verified here). So "it is the harness's memory, not the project's" does not separate the two cases cleanly.
   - This folder holds EJ's recorded working rules and decisions for the project. They steer agents but sit outside the repository, unversioned. A present/absent line shows that a memory location exists that the snapshot (C5) cannot see.
   - The cost is one line, and it cannot produce a false failure, because "absent" is not a failure.
7. **Q2: the report must not read the folder.** Some of these files are personal (an investing-context note, a private-work-code note). Listing the folder as present or absent, with no names or contents, keeps them out of a report that may be committed.

## What I need to know
- **Q1: who judges "trials cannot answer"?** I assumed the main agent states it, naming the check it looked for, and the experts can contest it. If the agent alone judges and the owner never audits the list, the escape-hatch risk below grows.
- **Q1: has the three-trial rule ever burned trials on an owner-only question?** I did not look through the run ledgers (not measured). If no run did, (a) fixes nothing yet, and (b) costs nothing. I would still pick (a) because the cost is small and the case is easy to foresee, but that is my reading.
- **Q2: does "agent memory" in the source-of-truth design mean Claude Code's subagent memory?** That is my recall. If the design meant something else, step 6 weakens and (c) gets stronger.
- **Q2: is the memory-check report committed or shared, and should the tool ever cover other harnesses (Codex, opencode, agy)?** If it should, a Claude-Code-only line is a stopgap, and the right design is a list of harness memory locations.

## Costs and risks
- **Q1, escape hatch.** "No trial can answer this" can become a way to skip hard work. Counter: require the stated reason (who decides, which check was looked for and not found) in the state file, and treat a missing reason as the question not qualifying.
- **Q1, gap filled with the agent's own value.** In a time-boxed run, a provisional value for an owner-only threshold is a value the agent chose for the owner. The method already labels it provisional and marks the work that rests on it, so I'd keep that labelling strict for owner-only items.
- **Q1, untimed runs.** An at-once question blocks everything that depends on it until the owner answers. The rule is only as good as the agent's ability to keep other pieces moving.
- **Q2, wording.** F1's "Who decides: the guidelines" is no longer true once Claude Code's folder is added. The owner has to rewrite F1's text, and its "Fails if" clause, to name the second source.
- **Q2, path fragility.** The folder name is derived from the project path with `/` replaced by `-`. I did not verify how Claude Code encodes other characters, such as dots or underscores, in that name. A wrong guess reports "absent" for a folder that exists. `--home` also has to redirect it.
- **Q2, harness bias.** Listing one harness's memory and not the others favours Claude Code in a project that also uses other engines.
- **Q2, drift.** If Claude Code changes where it keeps this memory, the line goes silently wrong.

## How we would know I was right
- **Q1:** over the next few runs, collect every at-once question with its stated reason. Count the ones where the owner's answer was a fact that a read or a trial would have found (a miss), and compare that with the trials saved. Mostly misses mean the "who decides, and which check" test is too loose, so tighten it or go back to (b). Few misses and visible trials saved mean (a) was right.
- **Q2:**
  - A test with `--home` pointing at a temp folder that holds `.claude/projects/<encoded path>/memory/MEMORY.md` reports the location present.
  - The same test without that folder reports it absent, and no check line fails.
  - A real run on this repository reports it present.
  - A report built from a folder containing a sentinel string never contains that string.
  - A reviewer reading the report sees no file names or contents from that folder.
