# Dave — where lessons live and how they reach each agent

## Answer
Keep the lessons in this repo as one skill linked into both skill roots, one file per lesson, each with an `agents:` field and a `trigger:` field. Project facts go in a lessons file in the code's folder, keyed by path. Lessons are delivered when their trigger is met, not by having agents read the store: the guard adds a lesson's one line when a Write, Edit or Bash command matches its trigger, and a script fills each engine's brief with only the lessons that match that engine and that brief. One condition: if lessons will be filed from EJ's private work projects, the lesson files cannot sit in this public repo (see "What I need to know").

## How I decided
1. **What would change my mind (my #1).** The measure is a repeat: a failure whose lesson was already written down before it. If repeats happened because a lesson was stored where the agent couldn't reach it, the store's location decides. If the agent could reach it but nothing showed it at the moment of the action, delivery decides.

2. **The data we already have (my #5).** I searched the `insight.md` files for "again", "repeat" and "second time". That found 6 repeats. How I sorted them is *my reading*; I did not audit all 56 sections.
   - **2 were lessons already in the main agent's memory that it did not apply:**
     - `runs/20261016-four-experts-what-counts-as-change/insight.md#F-4981093a`. Its root cause: "a rule held only in memory, with no check where the read happens".
     - `…/insight.md#F-d8221199`: "the memory note says to run the Python suite after the commit, and I did not apply it".
   - **2 had a fix that was never chosen:**
     - `runs/20261016-time-monitor/insight.md#F-84636a96` repeated in `…what-counts-as-change/insight.md#F-2cc835e3`: "whose options were not applied either, so it repeated".
     - F-15cf1278 repeated as `#F-98c2c4c9`.
   - **2 were spec-writing habits repeated within a day,** where the lesson existed only in a run's `insight.md`:
     - `runs/20261016-integrate-r11-r13/insight.md#F-05a1b440` repeats F-4cbb2f4b.
     - `…#F-2cdebf3b` repeats F-b7c8635f.
   - **One delivery that worked:** the quote-script rule went into the experts' brief in commit 740c842 (2026-10-16 14:19). In the three later runs I checked, none shows a quote failure for Sun Tzu: `six-experts/trial` passed 6 of 6, and in `workflows/mark-q` and `insight-level/level-q` the only failures are other experts' missing files. That is n=3 with no control, so a hint and not a law (my #10).
   - **What it shows:** none of the 6 repeats was caused by where a lesson was stored. Two came from a store loaded at session start as background, and two from fixes nobody had chosen.
   - **What it does not show:** whether `~/.agents/` or a skill would make any difference. There is no data on that.
   - **What this changed:** delivery decides more than location.

3. **How nature solves it (my #6): immune memory.** The body does not keep every antibody high everywhere; that would be the flood. Memory cells rest and are re-activated when they meet the antigen they were made against. Borrowed mechanism: each lesson carries a trigger (a path glob, a command word, an engine name or a task category) and is shown only when that trigger is met.

4. **Does the analogy fit (my #7)?**
   - **Same:** the problem is recalling a past threat when it comes back, without keeping every memory active.
   - **Different:** antigen matching is automatic. Here a person writes the trigger, and a wrong trigger never fires, silently.
   - **Key condition:** there must be a point where the trigger can be seen before the action. For the main agent, there is: the guard sees every Write/Edit path before it runs, and Bash as a command line (fact). For engines, there is too: the main agent writes every brief (fact). Inside an engine mid-run, I don't know of one (I did not check whether Codex has hooks). So I keep the analogy for those two points only.

5. **Q1, the store (my reading).** opencode and agy read only their brief and their repo (fact), so neither option is read by those engines. The store is read by the main agent and by the brief-filling script.
   - **Option (b), a skill in this repo, wins on:** version history, commit-hash citations, links that already exist in both roots, and one copy.
   - **Option (a), `~/.agents/insights/`, wins only on privacy**, because this repo is public (fact).
   - **One-type versus all-agents lessons:** use an `agents:` field, not folders. One lesson can belong to two engines, for example "a headless engine can exit 0 having done nothing; check its output" applies to both opencode and agy. Folders would need two copies.
   - **Insight used:** `runs/20261016-integrate-r11-r13/insight.md#F-682702da` (the skill export skipped a file). A store kept as a skill goes through the same export, so its files must be covered by the export check. This added a cost line.

6. **Q2, the project place (my reading).**
   - **A comment at the line** is seen only when that file is read, and several of these facts span more than one file. F-d8221199 is about a test and a hook together.
   - **The code map** is not built (fact), so it cannot hold anything today. A path-keyed entry uses the same key the code map would use, so entries can move into it later.
   - **A lessons file in the folder** can be found by walking up from the edited path, which the guard already sees.
   - **When the chosen fix is a test or a check, the test is the memory.** The entry only names the test. The basis is F-4981093a: the written rule failed, and a guard check now holds the read. This keeps text out of agents' context.

7. **Q3, delivery.**
   - **Main agent:** the guard matches each Write/Edit path and each Bash command word against the triggers and adds the matching lesson's one line, with its id, before the action.
   - **Engines:** a script with fixed rules and no LLM fills the brief's Lessons section. It takes lessons whose `agents` field matches the engine or says all, and whose trigger matches a path or task category named in the brief.
   - **Use what exists (my #5):** the six-experts runner already loads insights by category into my brief. But this brief got the whole 56-line index because no category was named. That is the noise the owner wants less of, and a trigger match would cut it.
   - ***Proposed change to the pattern:*** deliver a lesson from the day it is written, marked "open", not only after its fix is chosen. Two of the 6 repeats had unchosen fixes. What it would change: today an insight sits in its run folder until EJ picks a fix.

8. **Test before arguing (my #2, #8, #3, #4).** A paper replay costs minutes: for each of the 6 repeats, would the proposed trigger have fired before the repeating action? *My reading:*
   - **Yes, by spec-file path:** both spec habits.
   - **Yes, by command word:** F-d8221199.
   - **Yes, as a check:** F-4981093a.
   - **Yes, through the brief:** F-84636a96.
   - **No:** F-15cf1278. It needed a fix to exist, not a delivery.

   Then build on one path first: the brief part, which already exists for the experts. The guard part comes second. Write down the metric, the expected result and the stop date before starting. Compare against the current way as the control: per-project memory for the main agent, nothing for engines.

No category was named in my brief; I chose these insights from the index.

## What I need to know
- **Will lessons be filed from EJ's private work projects?** If yes, the lesson files go in a private user-global folder and the repo skill holds only the matcher. If no, the whole store goes in the repo skill.
- **Do Codex or dsh run their own hooks at the moment of action?** If yes, a trigger can fire inside the engine. If no, the brief is the only delivery point. I don't know.
- **Does the main agent's per-project memory (60+ files) move into the store, or stay where it is?** This sets the first store's size and how many triggers have to be written.
- **The prediction's numbers (my #3):** the expected repeat rate and the stop date. These are EJ's to set, not mine.

## Costs and risks
- **A wrong trigger never fires, silently (my #7).** The defence is to log every time a trigger fires. A repeat with no fire before it marks a wrong or missing trigger.
- **Bash writes are seen only as a command line (fact),** so a path trigger misses files written through Bash (my #7).
- **The guard needs new code:** a matcher and a context line on every Write/Edit.
- **Option (b) makes every lesson public.** A lesson that carries a project fact leaks it. Option (a) loses version history and hash citations (my #5 / my reading).
- **A store kept as a skill can be skipped by the export,** as F-682702da showed.
- **Per-folder lessons files scatter and go stale** when a later fix removes the trap. Pointing an entry to a test keeps it honest, because the test fails if the trap comes back (my reading).
- **Delivering "open" lessons adds lines before EJ has chosen a fix:** more noise, for 2 of 6 repeats (my #9).
- **The evidence is small (my #10):** 6 repeats by my own sorting, n=3 for the brief success, and no control.

## How we would know I was right
- **Replay first (my #2):** I predict 5 of the 6 repeats would have hit a trigger. If fewer than half do, triggers are the wrong design, and the store's location matters more than I think. That would change my answer (my #1).
- **After building on one path (my #8):**
  - Count repeats per insight section from the start date to a stop date written down first (my #3), against the current way (my #4).
  - Count lesson lines per brief against today's whole-index brief; that is the noise measure.
  - Every repeat whose lesson was filed but did not fire gets reported as a failure (my #9).

**Recommended version:**
1. **Store:** one `lessons` skill in this repo, linked into both roots; one file per lesson with `agents:` (all, or named types) and `trigger:` (path glob, command word or task category). If any lesson comes from private work, the files live in a private `~/.agents/` folder and the skill holds only the matcher.
2. **Project place:** a lessons file in the code's folder, keyed by path, each entry pointing to its insight id. When the fix became a test or check, the entry just names the test.
3. **Main agent:** the guard matches Write/Edit paths and Bash command words against triggers and adds the one matching line before the action.
4. **Engines:** a fixed-rule script fills the brief's Lessons section with only the lessons whose `agents` and `trigger` match that engine and the brief's paths or category.
5. **Order:** replay the 6 repeats on paper, build the brief part first, then the guard part.
