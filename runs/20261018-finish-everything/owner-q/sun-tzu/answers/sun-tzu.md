# 孫子 (Sun Tzu) — two choices: owner-only questions, and whose memory counts

## Answer

**Q1: adopt (a)** — a question no trial can answer goes to the owner at once, carrying one line naming the trial the run would have tried and why that trial cannot produce the fact; in a time-boxed run it is decided provisionally at once and listed for the owner, as method 3.8 item 14 already does.

**Q2: pick (a), with its label fixed** — the report lists Claude Code's project memory present-or-absent on a separate "also found" line, named *harness memory for this project*, never as agent memory: it is keyed to one project, not to one agent name. If the owner rules that only memory the guidelines govern is in scope, my answer becomes (c).

## How I decided

### Q1 — owner-only questions

1. **My #1** puts the reckoning first, and its first move is to search the facts out: 「故經之以五事，校之以七計，而索其情」 (quoted, 始計第一). The count wins when it is complete: 「多算勝，少算不勝，而況於無算乎？」 (quoted, 始計第一). A trial adds to the count only when a trial can produce the fact. Three trials of a question whose answer is not in them are the "none" case, paid for three times.

2. **My #11** names this case exactly. Foreknowledge 「不可驗於度，必取於人，知敵之情者也」 (quoted, 用間第十三) — it cannot be verified by measurement; it must be taken from the person who knows. The examples in the question — which location a requirement names, whether a real project exists, a threshold only the owner can set — are not in the ground to be measured. They are held by a person. #11 is not a last resort; it is the named instrument for this kind of fact.

3. **My #4** frames it as a discrimination: 「知可以戰與不可以戰者勝」 (quoted, 謀攻第三). Knowing which questions a trial can settle and which it cannot is the same knowing. Trying an unanswerable question three times is #4's half-victory: the troops are known, the ground is not.

4. **My #17 is why (b) looked right, and it does not reach this case.** Probing does teach — reckon, stir, give form, test in contact. But #17 is a method for what an opponent reveals under pressure. A person's decision does not reveal itself under pressure; it is not a reacting enemy. My reading: #17 governs the ground, #11 governs the person, and the question is on #11's side.

5. **My #8 prices the wait:** 「故兵聞拙速，未睹巧之久也」 (quoted, 作戰第二). In a time-boxed run the clock is the scarce resource; three trials spent on an unanswerable question buy nothing and spend the run's time.

6. **My #2 forbids building on the hope that the third trial comes through:** 「無恃其不來，恃吾有以待之」 (quoted, 九變第八). A piece waiting on an unanswerable question should rest on the owner's answer or stay open — not on the chance that a trial settles it.

7. **My reading of #13** supports the time-boxed form: 「君命有所不受」 (quoted, 九變第八). Not that the run overrides the owner — the owner gave the limit and accepts or declines at the end — but that inside the limit the run acts on its own read and answers for it, rather than stalling. That is the shape 3.8 item 14 already has.

8. **My #6 stops me making it unconditional:** 「是故智者之慮，必雜於利害，雜於利而務可信也，雜於害而患可解也。」 (quoted, 九變第八). Benefit: time saved. Harm: an owner interrupted for every blocked question, and a class that grows until it means "ask whenever stuck". So the gate is one line: *which trial would answer this, and why can it not?* Without that line, (a) is not the rule I am recommending.

9. **Proposed change to the pattern.** The pattern line "A question goes to EJ only after three failed trials on it or once the time is used up" becomes: *after three failed trials, or at once when no trial can answer it (the run records the one line saying why), or once the time is used up.* What it changes: the three-trial gate stays for questions trials can answer, and the owner-only class gets a second route that does not pass through it. Outside a time-boxed run, "at once" means into the next batch of 3.3, not a separate summons; inside one, it means the provisional decision at once plus the listing (3.8 item 14, `docs/WORKFLOW_DESIGN_METHOD.md:555-557`).

### Q2 — whose memory it is

10. **My #20** says judge a house by its land unit, its tax and what they breed — by its structure, not its name. Applied to a folder (*my reading* of #20): judge by what it is keyed to and what it is made of. Checked: the folder is `~/.claude/projects/-home-smoke01-dev-ancient-games/memory/` for `/home/smoke01/dev/ancient-games` — keyed to the project path; it holds `MEMORY.md` plus one file per fact, 48 files including the index (`find memory -type f | wc -l`). Checked: `~/.claude/agent-memory` does not exist on this machine. Keyed to the project, one index, one fact per file: it is project memory in the harness's keeping.

11. **The guidelines' own definition decides it.** Agent memory is "memory belonging to one agent name" (quoted, `docs/memory-system/SOURCE_OF_TRUTH.md:20`), placed at `~/.claude/agent-memory/<name>/` (quoted, `:24`). Claude Code's folder is not that. So the answer to the title is **no, it is not agent memory** — and (b), which would check it as agent memory, would name it something it is not.

12. **My #4 rules out (b) on its own:** 「知彼知己，百戰不殆」 (quoted, 謀攻第三). The check can verify present or absent; it cannot verify that entries follow a format they do not follow. Checking it as agent memory would produce false failures.

13. **My #3 keeps the check whole:** 「全國為上，破國次之」 (quoted, 謀攻第三). (b) is the walled city — a format check against a wall the folder was never built to defend. (a) with present-or-absent only leaves F1's MUST untouched and adds one line.

14. **My #16 says the order must be clear before it is enforced:** 「約束不明，申令不熟，將之罪也」 (attributed, 《史記》卷六十五; my #16). "Agent memory" would be a wrong order, inherited by every reader of the report. Hence the label is part of the pick, not a detail. The cheapest form is a separate "also found" line — path, present or absent, a count, no pass or fail — because F1's charter is "every memory location the guidelines name" (quoted, `memory_check/REQUIREMENTS.md:9-13`), and this one is not named.

15. **My #1 also decides against (c):** 「多算勝，少算不勝」 (quoted, 始計第一). F1's count is meant to be the memory a project has; a count that omits 48 facts an agent will actually load is short. (c) keeps F1 compliant and leaves the tool blind to a store its own vision says it should find ("finds which memory it has", my reading of `memory_check/VISION.md`).

## What I need to know

- **Q1:** Is "no trial can answer it" a closed list (the three examples) or an open class, and who decides membership? If it is open and the run decides, I would add a second reader for the call; if closed, no.
- **Q1:** Does "at once" mean out of band, or into the current batch? My answer assumes the batch outside a time-boxed run and the provisional decision inside one.
- **Q1:** Is the owner the only source, or may a run decide provisionally outside a time-boxed run too? If the owner is often away, at-once stalls runs, and I would extend 3.8 item 14's provisional route to every run — a larger change than (a).
- **Q2:** Is the harness's project memory in the tool's scope at all? If the owner says the report covers only memory the two guidelines govern, my answer becomes (c).
- **Q2:** May the line name files, or only count them? `MEMORY.md` opens with personal facts (checked: "User investing context" is its second line), so present-or-absent plus a count is the safe default.
- **Q2:** Is Claude Code the only harness to list? If the principle is "list every store an agent will load", opencode, Codex and agy keep state too, and the change is one adapter per harness, not one line. If only Claude Code, the basis needs a reason (my #1: one count, one basis).

## Costs and risks

- **Q1 — the owner becomes a shared, interruptible resource.** A loose class turns every blocked agent into an interruption; that is the harm side of my #6, and the reason for the one-line gate.
- **Q1 — premature closure.** A question wrongly classed unanswerable stops the run's own search, so a trial that would have taught is never run (my #17).
- **Q1 — waiting.** Outside a time-boxed run, "at once" still means waiting, and pieces resting on the answer stall; the pieces that do not rest on it must go on meanwhile (my #2).
- **Q1 — the three-trial rule was a shield.** Removing it for a class reopens the risk of escalating on the boundary between the classes (my #15: 「愛民，可煩也」, quoted — care for the owner can itself become the excuse for not asking).
- **Q2 — a durable mislabel.** A report line saying "agent memory" is read by owners and agents long after the run (my #16).
- **Q2 — false failures if it is checked as agent memory.** The entry format does not apply, so the failures would be the check's, not the memory's (my #3, #4).
- **Q2 — charter creep.** F1 would grow from "the locations the guidelines name" to "the locations we happen to know", and two runs could no longer be compared on the same count (my #1).
- **Q2 — privacy.** The folder holds personal facts; a per-file listing would put them in a report (my #6, harm side).
- **Q2 — precedent.** Listing one harness's store invites listing all, or invites the question why not (my #16).

## How we would know I was right

**Q1.** Write the check before the change; this test is mine and has not been run. For the next three time-boxed runs, each owner question's state or log must show either the "no trial can answer it: &lt;why&gt;" line or three failed trials. Measure: (i) questions that ran trials although no trial could produce the fact — target 0; (ii) owner escalations per run — not more than one above the baseline of the last three runs, or the class is too loose and my filter was wrong; (iii) time from question to answer for owner-only questions — should fall from three trials to one ask. Re-check against `runs/20261017-memory-check` (research-q item 16): re-classifying its owner questions should put the location, existence and threshold ones in the at-once class. Falsifier: a question sent at once that a trial could have answered.

**Q2.** Run memory-check on this repo: the report should show the harness folder present, with a count, on its own line, with no pass/fail line and no file name; on a fixture without the folder, absent; F1's existing lines and tests unchanged. This test is mine and has not been run. Falsifier: the line is useless without a format check, or F1's own tests have to change.
