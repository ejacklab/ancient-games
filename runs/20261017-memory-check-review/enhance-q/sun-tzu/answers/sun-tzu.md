# 孫子 (Sun Tzu) — what memory-check should improve next

## Answer

If this round's accepted findings are fixed: first refuse any `--out` path that falls inside memory, because today the report can overwrite `project-memory/INDEX.md`; second make every input that cannot be read a named `could not run`, never a pass, closing the class four of this round's raw findings belong to; third drop the report's static claim that the session-start hook is not installed.

## How I decided

1. **My #1 — count before you commit** (「多算勝，少算不勝，而況於無算乎？」). The brief's facts point at `runs/20261017-memory-check-review/findings.md` and `nodes/fix-r*.result.md`; neither file exists, and `nodes/review-enhance.progress.md:7` shows only `judge-r1` started at 23:11:34. So I counted what does exist: the two reviewer files, the source, and the previous round's `enhance-q/compare.md` and `report.md`. None of my three repeats what that round applied (the could-not-run warning, the unstaged count, the final Not applicable section, the scoped hook).

2. **My #2 — make yourself unbeatable first** (「先為不可勝，以待敵之可勝」). A checker's own ground is its inputs. My reading of this round's raw findings: `review/r1-codex.md` 1 (`checks.ts:111`, a failing `git ls-files` becomes "not applicable", exit 0), 5 (`cachechecks.ts:67`, the working tree is read while the report claims the staged blob), 10 (`cachechecks.ts:68`, an unreadable settings file still gives Rd1 a pass), and `review/r1-agy.md` 1 (`tools/memory_index.py:483`, an unborn HEAD skips the staging check and exits 0) are one class: the input the verdict rests on was not read, or was the wrong one, and the verdict is still clean. Fixing the four instances does not close the class.

3. **My #5 — the irreversible cannot be restored** (「亡國不可以復存，死者不可以復生。」). The tool has one action that can destroy what it checks: `command.ts:118` writes to whatever `--out` names, with no containment check. `VISION.md:22` says it changes no memory; `USE_CASES.md:35-38` (U5, proposed) says a run leaves no change but the report. A report written onto `INDEX.md` is not its own report. A wrong verdict can be corrected; memory overwritten before it is committed cannot.

4. **My #17 — probe, then read the signs** (「策之而知得失之計」). I ran the tool on a throwaway git fixture with `--out project-memory/INDEX.md`; the index's sha256 changed and `git status --short` showed `M project-memory/INDEX.md`. That is measured by me, not recall, and it is the case that shows the hole is live.

5. **My #15 — the general's own faults** (「凡此五者，將之過也，用兵之災也。」). `report.ts:101` prints "The session-start hook is not installed"; `runs/20261017-memory-check/settings-diff.md:38` records EJ's yes and that the global SessionStart entry was applied, and commit `7f1f67a` says the same. No check computes the line. The previous round's 孫子 proposed removing the two static lines (`runs/20261017-memory-check/enhance-q/compare.md:86`); it was not applied, and the hook has since been installed, so the hook line now has a case.

6. **My #6 — mix harm into benefit** (「智者之慮，必雜於利害」). I costed each item below; the top one is the one whose harm is irreversible, not the one that is largest.

7. **My reading — the ranking.** Evidence: measured (the `--out` write), four raw findings (the fail-open class), one contradiction (the hook line). Work: a containment check, a matrix test, one line. I put the irreversible action first, the class second, the false line third.

## What I need to know

- **Which findings were accepted, and have the fixes landed?** The brief cites `findings.md` and `nodes/fix-r*.result.md`; neither exists, and `nodes/review-enhance.progress.md:7` has `judge-r1` started at 23:11:34. If the fixes are not in yet, my #2 is the fix round's own work and should follow it; if they are, my #2 is the class test described below.
- **May `--out` ever point inside `project-memory/`?** No use case or vision line asks for it; if the owner does want that, it is a different command with its own risk, not the report path.
- **Should the report state the hook's presence at all?** If yes, the tool must read the harness settings (a new input outside the project); if no, drop the line. I propose drop.

## Costs and risks

- **#1, the `--out` guard** (my #5, my #6): a containment check and a usage-error path; risk of rejecting a legitimate report path inside the project but outside memory, and a symlink can resolve back in. Test the normal `--out report.md` path too.
- **#2, the fail-closed invariant** (my #2, my #17): a matrix test is more work than the four per-finding tests and can pin the mechanism; keep the assertion at the outcome ("no MUST passes when an input cannot be read") and inject at the process boundary. A false `could not run` is possible, but it is visible in the warning (U3) and exits 1, so it fails safe.
- **#3, the hook line** (my #15): one line; the cost is losing a reminder when the hook is absent. The tool never checked the line, so the reminder was not evidence; if the owner wants it computed, that adds a read of the harness settings.

## How we would know I was right

- **#1:** a test creates a fixture with `project-memory/INDEX.md`, runs `--out project-memory/INDEX.md`, and expects exit 2 with the file's bytes unchanged and `git status --short` empty; it fails on HEAD (the bytes change) and passes after the guard. The same for an entry and `AGENTS.md`; `--out report.md` still writes.
- **#2:** a table of every input the tool reads (git index, history, `INDEX.md`, entry files, `settings.json`, `AGENTS.md`, `.gitignore`), each with an injected read failure; every affected MUST is `fail` or `could not run`, none `pass`, exit 1. On HEAD it is red for the four cited cases; after the fixes it is green, and a mutation that returns `pass` on a read failure makes it red again.
- **#3:** no report contains "the session-start hook is not installed"; a text test pins it, and the oracle is `settings-diff.md:38` (the entry was applied).
- **Overall:** the next review round finds no new finding in the fail-open class, and the owner can read the report's "This run" section as a list of computed facts.

**Top one:** refuse `--out` paths inside memory — a checker must not be able to overwrite what it checks.
