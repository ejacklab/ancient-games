# 孫子 (Sun Tzu) — what memory-check v1 should improve next

## Answer

Put one whole, valid memory through the tool and check every verdict by hand — a real project with `project-memory/` if EJ names one, otherwise a multi-entry fixture built here — before adding anything else. Then record the yes to the session-hook diff already written, and make the report name the places where its working-tree view and its staged view disagree; the 70 green tests have still never judged a real `project-memory/`.

**The five, in order.**

1. **One whole memory, every verdict checked by hand.** Build a valid memory with two or three entries, an `INDEX.md` transcribed from `memory_index.py`, `work/`, `journal/` and a cache, and write the expected report before running the tool (by hand, or by an engine that did not write the code, as T1 says). If EJ names a real project, use it instead — a fixture is the fallback, not the goal.
   - **Serves:** U2 ("each requirement a tool can check is checked, with its id, its level and the evidence") and U6 ("the tool checks the project it is pointed at"); the vision line "tells the user what is there, what is missing and what is wrong."
   - **Case now:** `design-decisions.md:24` records "A real project to calibrate on — none known; fixtures only." The only memory fixture is one entry with a one-line index (`test/fixtures/project.ts:10-36, 53`); the smoke run on this repo is 0 fail / 3 pass / 3 needs a reviewer / 72 not applicable (`smoke-report.md:128`), and its first line says no commit touches `project-memory/`. My probe of the valid one-entry fixture gives 9 pass, 44 needs a reviewer and 22 not applicable among the 75 guideline records (plus F1–F3 passing), exit 0: no run has ever judged a second entry, a second K4.3 transition, or an index longer than one line.
   - **Check done:** the report on that memory has 0 "could not run"; every mechanically decidable MUST is pass, and a second reader confirms each pass and fail against the guideline text; then plant three breaks (a wrong INDEX line, a rewritten claim, a merge that drops a `covers` path) and only their ids fail. The suite stays green.
   - **Cost:** this is the largest piece; if no real project is named, the expected answers still come from the people who wrote the checks — T1 guards only that they are not computed by the check, not that they are right.

2. **Record the yes to the session-start hook.** The diff is written and hand-tried (`settings-diff.md:30-32`); only "Yes recorded: (not yet)" is blank (`settings-diff.md:36`).
   - **Serves:** U3 ("an agent starting work is told, in a few lines, what is missing or failing, without reading the report") and the vision line "Every agent starting a session, which must not start work on memory that is missing, stale or broken without being told."
   - **Case now:** `smoke-report.md:126` says "The session-start hook is not installed"; `bun memory_check/src/cli.ts --warn` on this repo prints nothing and exits 0 (my run from the repo root). U3's minimum acceptance — a hook that prints one line per failing MUST — is unmet, not by a bug but by a missing yes. Its value also waits on #1: no project with memory exists yet to warn about.
   - **Check done:** after the yes, start a session in a fixture repo with a failing MUST and see exactly the `--warn` lines; this repo stays silent; five starts do not hit the 20s timeout; and a test proves `--warn` opens nothing under `.cache/` (the hash method at `acceptance.test.ts:46-54`).
   - **Cost:** one line at every session in every git project without `AGENTS.md` (`settings-diff.md:34`); the warning runs every check including history (R2, `REQUIREMENTS.md:67-69`), so start latency grows with history; `|| true` makes a timeout look like "nothing to warn."

3. **Name the working-tree / staged-state disagreement in the report.** When `project-memory/` is present but unstaged, or staged but deleted from the working tree, add one note saying which view was checked. Do not add it to the warning: U3 says the warning holds nothing else.
   - **Serves:** U1 ("the owner learns which memory exists") and C5 (the report names its snapshot); the vision line "tells the user what is there."
   - **Case now:** presence is decided from `git ls-files --cached` (`checks.ts:99-100`) while F1's table is `existsSync` on the working tree (`locations.ts:74-77`). My probe — a valid entry and `INDEX.md` written after the fixture commit and not staged — gives F1 "present", every SoT record "not applicable", exit 0 and an empty `--warn`. The only warning is a parenthetical inside F1's evidence (`smoke-report.md:21`); a user who has just written memory is told "nothing to check" with no reason in the summary. The review's finding 3 fixed the opposite direction; this direction is left to inference.
   - **Check done:** a test writes a valid `project-memory/` without staging it: the report holds one note naming the unstaged folder and the staged view, exit stays 0, every SoT record stays not applicable; the reverse case (staged memory, deleted working tree, review test 3) gets the other note; `--warn` output is unchanged.
   - **Cost:** a note is easy to miss and does not reach the session-start agent; making the warning speak needs a U3/R2 change (question 2 below).

4. **Compress the report's repetition.** Group the not-applicable rows by absent location (all ids listed, one evidence sentence), and make "Needs a reviewer" a list of ids with their `fails_if` instead of re-printing the evidence already printed above.
   - **Serves:** U1/U2 — the report is how the owner sees what is wrong; R1 still requires every id and U4 still requires the reviewer list.
   - **Case now:** on the valid one-entry memory the report is 173 lines; the 44 reviewer rows are repeated almost verbatim in a 62-line section, and the 22 not-applicable rows carry one identical evidence sentence (my probe). On this repo, 72 of 78 result lines repeat "project-memory/ is absent..." (`smoke-report.md:27-110`). The signal is 12 passes.
   - **Check done:** every C1 id still appears exactly once in the per-record results (the existing count at `acceptance.test.ts:58-63` already checks 75), every reviewer-only id still appears in the reviewer list (`acceptance.test.ts:65-71`), and the valid-memory report is at most 120 lines.
   - **Cost:** a grouped row can hide one failure; the id-count test is the guard, and MUSTs-first order must stay.

5. **Pin the bundled guideline copies to `docs/memory-system/`.** A repo test that compares `memory_check/guidelines/SOURCE_OF_TRUTH_REQUIREMENTS.yaml` and `CACHES.md` byte-for-byte with their sources, failing on the first differing byte.
   - **Serves:** C1 ("the tool's own copy, with its version printed") and U2 (checks are the guidelines' own requirements).
   - **Case now:** they match today (`cmp` on both pairs exits 0), but the guidelines carry their own history of repeated edits (`CACHES.md:1-13`: "Changed 2026-10-12… Then corrected… Finally… Then…"), and the tool prints only a short hash (`smoke-report.md:3`). The first edit after today makes every report check old rules without saying so.
   - **Check done:** the test passes now and fails on a one-byte change to either bundled file.
   - **Cost:** this only guards the copy inside this repo; a copy installed elsewhere (U6) can still drift, and every guideline edit becomes a two-file change — which is the point.

**What I would remove or simplify.**

- **The two static status lines** at `report.ts:75-76`: "The session-start hook is not installed" and "Not calibrated on a real project" are not check results (C2), and each becomes false when #2 and #1 land. Keep the calibration line until the first real report, as `design-decisions.md:15` asks, then delete both; if kept, derive them from an input rather than a constant.
- **The duplicated report text** in #4 — the not-applicable evidence and the reviewer section's re-printed evidence. Same reasoning: the report's job is the signal, not the volume.
- **No new checks.** There are already 75 records (64 SoT + 11 CACHES, `smoke-report.md:4`); on a valid memory only 9 of the 25 SoT MUSTs are mechanically decided and 16 need a person (my probe). More checks would mostly add "needs a reviewer" rows. My #14 — numbers are not valued for their own sake — and my #8 — value victory, not duration — both say stop here and spend the next work on trust.
- **Not proposed, because no use case or vision line names them** (my #5, my reading): JSON output, more cache checks, a CI gate, a narrower hook mode.

## How I decided

1. **my #1 — count before committing.** I counted what the tool has actually met: one real snapshot (this repo: 0 fail, 3 pass, 72 not applicable), no real `project-memory/`, and one entry in every fixture. A count that has never met the thing it counts is not a count: 「多算勝，少算不勝，而況於無算乎？」 (quoted, my #1).
2. **my #4 — know whether you can fight.** The review says its probes "confirm individual code paths, not independent end-to-end behaviour" (`review.codex.md:5`), and 14 findings followed 55 green acceptance tests. So the tool cannot yet show it can win on a whole memory; one whole memory is the probe.
3. **my #2 — make yourself unbeatable first, then seek battle.** 「勝兵先勝而後求戰，敗兵先戰而後求勝。」 (quoted, my #2). Calibration (#1) precedes delivery (the hook, #2): a warning never tested on a whole memory is a battle sought before the win.
4. **my #3 — whole over broken.** One whole valid memory with every verdict checked by hand teaches more than another one-break fixture, and a valid report is the only way to see the 44 "needs a reviewer" rows a real memory produces. This is also why I compress the report instead of adding checks.
5. **my #19 — name the ground, act as prescribed, my reading applied to it.** The two views are two grounds: F1's is the working tree, every verdict's is the staged state. When they differ the report must say so, not let one pass for the other.
6. **my #6 — mix harm into benefit.** Every point above carries its price in the list and below; none is offered as free.
7. **my #14 — choose by the ratio of forces.** The hook is one yes, the note and the report cut are small, the bundle test is tiny; the whole-memory pass is the largest but the only one that raises trust, so it comes first. 「故兵非貴益多也」 (quoted, my #14) — more checks are not more force.
8. **my #8 — value victory, not duration.** 「故兵貴勝，不貴久。」 (quoted, my #8). The tool is built, tested, reviewed and fixed; another month of features is not the win. A verdict the owner trusts and a warning an agent sees is the win.
9. **my #5 — move only on advantage.** I dropped JSON output, more cache checks, a CI gate and a narrower hook: none names a use case or a vision line (my reading).

## What I need to know

1. **Is there a git project with a real `project-memory/` that the main agent may run on?** If not, is the multi-entry fixture acceptable as the calibration target? The answer's #1 changes between "run on a project" and "build the fixture."
2. **Does "missing" in `VISION.md:11` include a `project-memory/` that is written but not staged, or staged but deleted from the working tree?** If yes, #3 should also put a line in the warning — but that changes U3's "nothing else" and R2. If no, the report note is the whole fix.
3. **Should the hook apply everywhere?** The diff lives in `~/.claude/settings.json` and warns in every git project without `AGENTS.md` (`settings-diff.md:34`). If EJ wants that only in projects that have adopted memory, the hook needs a scope condition before the yes.

## Costs and risks

- **#1 (my #1, #4):** a fixture is still not a project; if no real project is named, the calibration proves consistency, not correctness. It is also the longest piece.
- **#2 (my #2, my #8):** a line at every session in every git project without `AGENTS.md`; the hook runs every check including history, so latency grows with history; the 20s timeout with `|| true` turns a hang into silence, the worst failure for a warning.
- **#3 (my #6):** a note can be missed, and the exit stays 0 (correct by C4/R3), so the tool still says "fine" in its code; only a U3 change would tell the agent.
- **#4 (my #3):** compressing can hide a failure; keep the id-count test, MUSTs first, and the counts line.
- **#5 (my #1):** a repo-only guard; an installed copy elsewhere is unprotected.
- **Cross-cutting (my #14):** #1 is the work, #2 is one yes, #3 and #4 are small, #5 is a test. If only one is done, do #1 — or its fixture fallback, which the main agent can start today.

## How we would know I was right

- **#1:** a report on a whole memory with 0 "could not run"; a hand-check that each mechanical pass and fail matches the guideline text; three planted breaks failing exactly their ids; and, within a month, the tool finding a real break in a real project's memory that its owner had not already flagged.
- **#2:** a session in a project with a failing MUST prints exactly the `--warn` lines; this repo prints nothing; five consecutive starts finish inside the timeout.
- **#3:** the unstaged-memory probe shows one note naming both views; after staging, the same memory gets its checks.
- **#4:** the valid-memory report drops from 173 to at most 120 lines with every C1 id still present exactly once.
- **#5:** a one-byte edit to either bundled copy fails the test; the current pair passes.
- **Overall (my reading):** the owner reads one report and does not have to ask "was any of this actually checked?", and an agent's first action in a session changes because of a warning line.

**Top three, in three lines:**
1. Put one whole valid memory through the tool and check every verdict by hand; a fixture will do until a real project is named.
2. Record the yes to the hook diff and start one session to see it.
3. Name the working-tree/staged-state disagreement in the report, then cut the reviewer and not-applicable repetition.
