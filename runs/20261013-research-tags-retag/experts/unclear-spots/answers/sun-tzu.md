# 孫子 (Sun Tzu) — can the engines, the task, and the ground carry each piece?

## Answer

The task as posed can be done, and the engines and tools for A, B, R1, R2, R3 and R6 are already proved; the leg that is only **half known is the ground** — the workflow file is untracked, so R1's stated source (`git show HEAD:`) cannot speak, and while this call was pending the run already moved: R1, A and B executed at local 21:09–21:10 and wrote passing evidence, yet `state.md` still marks every piece `todo` and its log says nothing ran besides readiness. Engine capability for R4/R5 (`dsh deepseek-flash` on 143 schema-constrained rows) is half known too: one recorded call, never this shape. Spot verdicts:

| Spot | Verdict |
|---|---|
| U1 | Decision known (the four labels, per EJ's "go"); its stated ground is **half known** — the four are quotable only from the working tree, because the file is untracked and `git show HEAD:` exits 128 |
| U2 | **Known** — `docs/RESEARCH_TAGS.md` now names `docs/research/…-r2/` and flags the planted s2 copy (line 81) |
| U3 | **Known** — `runs/20261013-research-tags-retag/` exists and is in use |
| U4 | Decision known; capability **half known** — one `dsh` call ever recorded, no 143-row schema test |
| U5 | **Known as a limit** — 13 leaks listed in `blind/leaks.txt` (R005…R137); read the result as a comparison, as designed |
| U6 | **Known** — accepted limit (taggers see the row text, not the sources) |
| U7 | **Contradicted on disk** — R1/A/B ran at 21:09–21:10 while this expert call is still pending; "experts before the run" was not observed |
| U8 | **Broken mechanism** — `git show HEAD:.claude/workflows/research-agent-memory.js` is impossible; the intent (quote before A edits) was met from the working tree and recorded with a sha256 |
| U9 | **Known** — `tools/export_skills.py` already names six `references/` targets; `skills/workflow-design/references/research-tags.md` now exists |
| **N1** | New — file untracked means no committed baseline for the control quote or for A's "must not change" list |
| **N2** | New — `state.md` contradicts the disk (R1/A/B done, all marked todo; log says nothing ran), so the design's resume point ("the first piece not marked done") would re-run R1 |
| **N3** | New — order inverted: the run began before the experts answered, and `prediction.md` is absent while R1/A/B are done |
| **N4** | New — four files carry uncommitted or untracked state (`.claude/workflows/research-agent-memory.js`, `docs/RESEARCH_TAGS.md` untracked; `tools/export_skills.py`, `docs/workflow-templates/research-file.md` modified), so the end-of-run `git status` comparison has no clean baseline |

Piece by piece, against the three questions:

| Piece | Engines/tools can do it | Task as posed can be done | Ground permits it |
|---|---|---|---|
| A | known | known | **half** — the stated source (`git HEAD`) is impossible; the edit is now on disk and A's three checks pass (`evidence/A.txt`) |
| B | known | known | **half** — `export_skills.py` was already modified against HEAD before B; now regenerated (`evidence/B.txt`) |
| R1 | known | known | **half** — check PASS (143 rows, 94/44/3/2, sabotage exit 1) but the design's quoted mechanism exits 128; the quote came from the working tree, sha256 `fb8ea1c…` |
| R2 | known | known | **known input** (key present), but the fixture is the COO's own — independence half |
| R3 | known | known | **half** — `prediction.md` absent while R1/A/B already ran |
| R4 | **half** | **half** | **half** — rows and definitions present; briefs absent; 143-row schema never tested |
| R5 | **half** | **half** | **half** — same; the definitions exist in two copies now, the brief must quote the one |
| R6 | known | known | **half** — depends on sheets and the R3 time check that do not exist |

## How I decided

1. **Reckon the three legs before committing (my #1).** "夫未戰而廟算勝者，得算多也；未戰而廟算不勝者，得算少也" — I counted each piece's engine, task and ground rather than accepting the plan's word.
2. **Use the half-victory test (my #4).** "知吾卒之可以擊，而不知敵之不可擊，勝之半也" — knowing our side and the task but not the terrain is exactly half. Here the engines and the task are known; the *ground* is the half-known leg.
3. **Do not rely on the other side's good behaviour (my #2).** "無恃其不來，恃吾有以待之" — do not rely on `state.md` staying accurate; rely on the evidence files and the check scripts being able to disagree with it. They do.
4. **Probe, then read the signs (my #17).** "策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處" — I read the row counts, the sha256s, the mtimes and the `git show` exit code rather than the readiness summary. The signs, not the plan, produced every finding above.
5. **Take foreknowledge from the repository, not from the plan (my #11).** "先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人" — readiness is the COO's own report; the git-HEAD claim needed a witness from the repo, and there is none (my reading of the exit-128 probe).
6. **Name the harm before the benefit (my #6).** "是故智者之慮，必雜於利害" — each verdict above carries the failure it permits, not only the passing check.
7. **Fix the cheap thing before the expensive one (my #3).** "上兵伐謀，其次伐交" — updating `state.md` and committing the baseline is cheaper than a mis-run of two tagging passes; it comes first.
8. **Value the result, not the length (my #8).** "故兵聞拙速，未睹巧之久也" — R2/R3 can still run before R4/R5, so the comparison is salvageable; the cost is not.
9. **Order the pieces so the comparison survives (my #2, second half).** The winning army "先勝而後求戰" — the prediction must exist as a file before the taggers start; that condition holds only if R4/R5 have not begun.

## What I need to know

1. Does a snapshot exist of the four-label text the 143 rows were **actually** labelled under? The file is untracked and has no git history. If yes, the control source is sound; if no, the control rests on the working tree plus an assertion.
2. Does "experts before the run" still bind, now that R1, A and B have run at 21:09–21:10? If it does not, R2/R3 can proceed before R4/R5 and the prediction still predates the sheets; if it does, the order breach is a question for EJ.
3. Has `dsh deepseek-flash` ever returned a 143-row schema-constrained sheet? If it has, only R4/R5's tags are unknown; if not, the whole capability risk sits there.
4. Should the untracked/modified baseline be committed before R4/R5, so that "the run may change only these files" means anything at the end?

## Costs and risks

- **Working-tree control** (U1, N1, my #2): a revert or a silent edit changes the control text with no committed witness; the sha256 in `blind/control-defs.md` is the only guard.
- **Stale state file** (N2, my #2): a resume re-runs R1 and can overwrite the passing 143-row sheet with a second, different shuffle.
- **Blind by instruction** (U5, U6, my #6): 13 leaked tag words and a repo the tagger can read; the result compares a rule against tagger drift, not against a clean experiment.
- **Engine risk** (U4, my #4): `deepseek-flash` on 143 schema-constrained rows is unmeasured; one failure is a retry, two send the pass to EJ.
- **Order** (N3, my #8): if R4 begins before `prediction.md`, the "prediction first" clause of `RESEARCH_TAGS.md` is void, and with it the check's stop date.
- **Count independence** (my #11): `count.py` and R6's regeneration are the COO's own scripts; the saved sheets and key are the only path to a hand recount.

## How we would know I was right

- `git show HEAD:.claude/workflows/research-agent-memory.js` exits 128 now; after a commit it exits 0 and prints the four labels (measured now; the fix is a known test).
- A resume that reads only `state.md` and reruns R1 changes `blind/rows.md`'s sha256 or its id set; a resume that reads the evidence files does not. The stability of that sha256 is the test of N2.
- R4/R5 either produce 143 lines with every tag in {verified, reported, unproven, unknown} (or a well-formed split/stuck) within two attempts, or the pass goes to EJ — the design's own stop.
- The R3 time check passes: the recorded prediction time is earlier than the first line time of both sheets.
- EJ can recount any stuck row by hand from the saved key and sheet — the human check that the machinery is meant to leave open.
