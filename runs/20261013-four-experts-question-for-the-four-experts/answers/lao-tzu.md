I'll read the brief first.
# 老子 (Laozi) — how to fix the twenty findings, in what order

## Answer

Fix in four waves: first every place where *nothing there* is read as *something good there* (F3, F1, F5, F17's `done: false`, F11) — 「損之又損，以至於無為」 (my #1); then make absence loud instead of silent (F20, F16, F14, F15, F4); then narrow the run folder and the paths (F12, F13, F10); and leave F6, F7, F2, F8, F9 for a decision rather than for this session — 「少則得，多則惑」 (my #14). Expect the numbers to get worse before they get better, and mourn that as the result rather than beautifying it: 「果而勿矜」 and 「戰勝，以喪禮處之」 (my #13).

## How I decided

1. **The promise is one promise, not five.** "never say PASS without proof" is 「知不知上，不知知病。夫唯病病，是以不病」 — the sickness is not being sick, the sickness is reading not-knowing as knowing (my #8). F1, F5 and F17's `done: false` are that one sickness in three places: absence turned into evidence. They come first because until they are fixed, no count I or EJ read means anything (my #6, 「為之於未有，治之於未亂」 — handle it while it is still small).

2. **F3 first even though it is third on the list, because it is the cheapest and it is what measures the rest.** The evaluator cannot cite its own hyphenated ids, so its own case table is fiction. 「其脆易泮，其微易散」 — the brittle and the minute are the easy ones (my #6). Nothing downstream can be checked until this is.

3. **Do not write a new citation language; make the reader agree with the writer.** spec_parse already decides the id grammar. Take the grammar from where it is born and have one test that exercises both sides (my #5, 「我無為而民自化」 — remove the blockage rather than add machinery).

4. **Every "absence means yes" gets turned into "absence means no".** This is one move repeated: F1's empty `all()`, F5's timeout-equals-fail, F4's `is False`, F17's `done: false`. 「為學日益，為道日損。損之又損」 — the same subtraction in four places, not four designs (my #1).

5. **Reporting fixes come after verdict fixes, and I say why.** F20, F16, F14, F15 change no verdict. They are cheap and safe, but if they land first you will be reading a changed report over an unfixed verdict and you will misread it (my #3, 「功成而弗居。夫唯弗居，是以不去」 — the result stands on its own; do not stand over it narrating).

6. **Containment before capability.** F12, F13, F10 are about making the run folder narrower and the paths unable to escape. Narrowing is my #1's move; the danger of gripping the whole system is my #4's: 「天下神器，不可為也」 and 「去甚，去奢，去泰」 — drop the excessive, do not add to it.

7. **F10 is a delete, not a reset.** Rerunning a runId should remove the run folder. That makes "a model step wrote no file" true by construction, rather than adding a cleanup step to enforce it (my #1).

8. **F4 is two findings wearing one number; take the halves apart.** Treat missing/null `restored` as *not* restored (that half is subtraction, one line, safe). The baseline hash taken *after* the product run is an ordering error, and ordering errors at the end of things are the ones that hurt: 「民之從事，常於幾成而敗之。慎終如始，則無敗事」 (my #7).

9. **F8: stretch before you shrink.** 「將欲歙之，必固張之」 (my #12, `quoted`). Do not begin by adding patterns to the exclusion list — each new pattern is a new thing to be wrong about. First one test that *lists* everything a blind copy can see at any depth (`test_*.py`, `*_test.py`, `conftest.py`, `tests/`, notes), then decide what leaves. The second half — `--exclude` must add to the defaults, not replace them — is pure subtraction and can go with F12.

10. **F2 and F7 are one decision, not two.** If the judge is no longer told where the defect is, then "missed plant → rerun once" stops being a nicety and becomes the thing that keeps the pass rate meaningful. Fixing F2 alone buys a number nobody should quote. So: either both, or neither (my #2, 「知足不辱，知止不殆」 — know what is enough; stopping is not endangered).

11. **F6 and F7 I advise against building this session.** The requirement claims a repair round and a rerun that no step performs and no data contract carries. That gap is itself a false PASS — the requirement asserts a step that does not exist, which is the same sickness as F1 (my #8). The honest move is one of the two, not a middle: make the requirement say what the tool does, or record the step as not done. My #1 and my #14 both point the same way — twenty findings, one session; adding a step is how a session ends with twenty-one open items.

12. **F9 I advise last, or not at all, and never alongside Wave 1.** The mutant writer's sandbox is a flag. The probes running with full user rights is structural: they import the product, write caches, and run model-written code. Decide what the probes may be *before* narrowing them, or you trade a false PASS for a run that cannot finish. My #10 is exactly this warning: 「不敢為天下先」, and the chapter prices it plainly — 「今舍慈且勇，舍儉且廣，舍後且先，死矣！」. Be first with the thing that can destroy the machine and you pay. It must also never move under a measurement, so it cannot share a session with the fixes that change what a run produces.

13. **The acceptance test is the tool turned on itself.** 「知人者智，自知者明。勝人者有力，自勝者強」 (my #16). The product's own tests catch 6 of 6; the evaluator catching 5 of 6 is a comparison, not a verdict. After Waves 1–3 it must produce its own per-case table on its own spec — that table is the measure of the whole repair.

14. **The gains will look like losses for a while, and I will not dress them up.** F1, F5 and F17 will lower the PASS counts, because some of them were false. That is 「戰勝，以喪禮處之」 (my #13) — a victory handled with the rites of mourning, not made beautiful.

15. **The best fixes are where nobody enjoys them.** 「水善利萬物而不爭，處眾人之所惡」 (my #15): the regex, the quoting, the containment, the null checks. Do not start in the verdict that people read.

16. **Take on the reproach, and do not pare away at people.** 「人皆取實，己獨取虛」, 「受天下之詬」, 「以約為紀」, and 「常寬容於物，不削於人」 (my #19, `attributed`). The containment fixes make the tool harder to use and less likely to lie; take the reproach of that. But do not narrow anyone's path that was never the defect.

17. **When the time is not right, drift.** 「且君子得其時則駕，不得其時則蓬累而行」 and 「吾所以告子，若是而已」 (my #18, `attributed`). On F2, F6, F7 and F9 my answer is that this is not the session — and that saying so plainly is the answer, not a deferral.

**Approach, finding by finding (High and Medium):**

- **F1** — Take away the default. `meets` may be true only when there is at least one requirement row *and* every row is PASS. Do not invent a third verdict and do not invent a "nothing to check" state that reads as success. *Cost:* every empty parse now answers "does not meet" instead of "meets"; visible on calibration. *Notice:* sabotage check, and the empty-spec case in the frozen test.
- **F2** — Stop telling. The plant id belongs to the input builder, not to the file the judge reads. Pair with F7 or hold both. *Cost:* the plant-pass rate falls; missed plants make the reading-case verdicts say less. *Notice:* the plant-found count per run, before and after, on the same product.
- **F3** — Take the id grammar from spec_parse; one test exercises the writer and the reader together; F20 lands in the same change so a probe citing a case that does not exist is counted, not ignored. *Cost:* more probes will now be recognised, so the case table will show more than it did. *Notice:* count of probes whose citation resolves, and count of UNKNOWNs, before and after.
- **F4** — Two halves. Null/missing `restored` is not restored. Then move the baseline hash before the product run. *Cost:* the hash half will catch `__pycache__`, `.pytest_cache` and any probe that writes into the copy; if that is noisy it will be ignored, and an ignored check protects nothing. Decide what counts as "the product changed" *before* making it fatal. *Notice:* how many runs a real product trips it, over several runs — not one.
- **F5** — A timed-out run and a run with no report are "not measured", not "fail". A mutant that cannot be run proves nothing about the probe. *Cost:* PASS counts drop; mutant suites that used to hang become UNKNOWN. *Notice:* PASS count down *and* false-PASS tests still red, on the same seeds.
- **F6** — Do not build the repair round this session. Correct the requirement to state the tool's actual behaviour, or state the step as absent. *Cost:* the spec stops describing something EJ wanted. *Notice:* the requirement no longer claims a step that no data contract carries.
- **F7** — Same, and bound to F2. If F2 ships, F7 ships; if neither ships, both stay visible as gaps. *Cost:* a missed plant voids the case instead of being retried. *Notice:* count of plants missed per run.
- **F8** — Inventory first (one test listing everything a blind copy can see, at any depth), then shrink; make `--exclude` additive; have the workflow send its excludes. *Cost:* excluding a `conftest.py` or fixture directory that is not a test can break the copy's imports. *Notice:* the blind copy must still import and still build — that is the test, not the exclusion list.
- **F9** — The writer's sandbox is a flag and can be done. The probes' rights are structural: decide the allowed surface first, then narrow. Not in this session; and never in the same session as Wave 1. *Cost:* if narrowed too far, runs cannot write where pytest needs to and simply fail to complete. *Notice:* E5 and E7 exit codes, not verdicts.
- **F10** — Delete the run folder on rerun; do not reset a subfolder of it. *Cost:* no resume from a crashed long run. *Notice:* "a model step wrote no file" must hold by construction, and no stale `mutants.json` can be visible to the probe writer.
- **F11** — Wrong shape is UNKNOWN and exit 2, with the offending entry named. *Cost:* an output that used to crash will now look like a quiet run. *Notice:* exit code is 2, and the report names the entry.
- **F12** — Contain runId at the point of use: no separator, no `..`, no absolute path. *Cost:* none I can name; it refuses inputs that were never legitimate. *Notice:* `../../x` is refused loudly, and the run lands inside `runs/` or not at all.

**What risks breaking something else, and how we would notice:**

- **The measurement moves under us.** F1/F5/F17 change what a run means. *Notice:* calibration before and after on the same product and the same seeds; 762 tests green; a red-on-undo test per fix (my #6 — a fix with no sabotage test is a comment, not a fix).
- **F4's hash half is the fix most likely to be switched off later**, because it will fire on ordinary caches. If it fires on every run it protects nothing. *Notice:* the flag rate on a real product over several runs.
- **F3 with F20 raises the counts before it lowers them** — probes that were invisible become visible, and renamed or absent groups show up. That the numbers grow first is my reading of what 「將欲歙之，必固張之」 means for a count, not the text's words (my #12).
- **F8's shrink can break imports** if it takes a conftest or fixture directory. *Notice:* the blind copy still imports and still builds.
- **F9 can stop runs completing.** *Notice:* step exit codes.
- **F10 deletes.** *Notice:* never point it at a runId whose model output EJ wants kept; a rerun is a new folder, not an overwrite (my #3, 「功遂身退，天之道」).
- **F12 will refuse a runId someone has been using with a slash,** if such exists. *Notice:* the refusal is loud.

## What I need to know

- **Are the frozen test files per module, and does changing a data contract — adding an "unmeasured" state distinct from FAIL — require a new frozen file?** If yes, Wave 1 is three commits, not one.
- **What does `--exclude` default to today, and does the workflow already hold a list it could send?** (F8's third half is free or is work, and I cannot tell which.)
- **Can the probes be run under restricted rights in this harness at all, or is full user rights a property of the runner rather than a choice?** (F9 — if it is the runner, F9 is not one finding but a platform change, and it leaves this session entirely.)
- **How long does one live run take, and is it reproducible from seed?** If it is not reproducible, the before/after calibration does not exist and the entire ordering has to be argued from the 762 tests alone.
- **On F6 and F7: does EJ want the requirement corrected, or the tool built out?** I have advised correcting it. If the answer is "the requirement is the contract and the tool must meet it", Wave 4 becomes Wave 1 and this is a longer repair than one session.
- **Does anything get committed out of the run folder** — model output, secrets, credentials in prompts? (F10's delete only becomes safe once I know that.)
- **Are hyphenated group ids common in real REQUIREMENTS.md files, or is `EV-P1` a naming this one project chose?** If common, F3 is not a bug fix but a grammar that the tool has always been missing.

## Costs and risks

- **Every "absence means no" change lowers reported PASS**, because some PASSes were false. That is the cost of 「夫唯病病，是以不病」 (my #8) and it will read as a regression to anyone who only watches the count.
- **F4's hash check will be noisy and may be muted.** Muted is worse than absent: it looks like a control. The price of a real check is deciding what counts as a product change — one session-pass (my #7).
- **F6/F7 not being built leaves the tool short of its written requirement.** That is my #1's price, paid deliberately, and my #18's 「吾所以告子，若是而已」 — this is all I have to tell you — is why I state it rather than hide it.
- **F2 without F7 makes the plant pass rate mean less, not more.** Taking away the hint is cheap; it is only honest with the retry in place (my #2).
- **F9 postponed leaves model-written code running with the user's rights.** That is the one cost I would not want carried past the session, and it argues for doing it next, alone, rather than skipping it (my #10).
- **F10's delete ends resume-from-partial.** Small price beside a stale `mutants.json` being read by the probe writer.
- **F8's inventory costs a pass** before it saves one, and 「多則惑」 (my #14) is the reason I do not want three exclusion lists and a fix.
- **A four-wave repair in one session has a real failure mode:** Wave 1 changes what a run means and Wave 2 changes what it says, so if both land and the numbers move, nobody can say which caused it. My #11's fear of doing too much at once. If EJ must choose, choose Waves 1–3 alone and leave everything else untouched.

## How we would know I was right

- **The evaluator, run on its own spec, produces its own per-case table.** Today it cannot — F3 says so. After Waves 1–3, it must, and that table is the acceptance measure for the whole repair (my #16, 「知人者智，自知者明」).
- **Sabotage: each fix in Waves 1–3 has a test that goes red when the fix is undone.** The house rule already says a fix counts only this way; a fix with no red-on-undo test has not been made.
- **Calibration: PASS counts go down and false-PASS tests stay red, on the same product and the same seeds.** If PASS counts stay level after F5, something else is manufacturing proof and my #8 is wrong about this codebase.
- **The frozen tests are not weakened: 762 pass, and every new test is additive.**
- **One-session test: Waves 1–3 land, Wave 4 is untouched, and the open count goes from 20 to about 8 with no step's exit code or verdict changing for a reason I cannot name.**
