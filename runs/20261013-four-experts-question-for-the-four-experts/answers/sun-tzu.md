# 孫子 (Sun Tzu) — how to fix the twenty findings

## Answer

Fix what lets it lie before what lets it miss, and fix the causes, not the costumes: F1, then F5, then F3; then F4 and F11 together as one fail-closed rule; then the containment cluster F10, F12, F2, F8, and F9 last, because that is the one most likely to break the pipeline while fixing it; then the two missing loops F6 and F7; then the cheap lows, deferring F18 first. Before each fix, require a reproduced finding and the test that fails when the fix is undone; if the session fills after containment, stop and record what was left.

## How I decided

1. **My #1 — reckon before battle.** The brief confirms 3 of the 20 (F1, F3, F5); the other 17 are one reader's account. Lay each finding out by module, blast radius, test file, engine and cost before touching code — the chain 「地生度，度生量，量生數，數生稱，稱生勝」 (my #1, quoted). A finding with no repro is not yet a fact; a fix with no failing test is not yet a fix.
2. **My #11 — foreknowledge comes from people, and is paid for.** Get the repros from whoever can run the code — the COO ran F1, F3, F5 — not from the review text: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」 (my #11, quoted).
3. **My #20 — judge by what a defect breeds, not by its size.** F1 and F5 breed a false verdict into every result; F3 breeds silent UNKNOWN across a whole class of ids; F10 breeds stale evidence into every downstream step. That ranking, not the High/Medium label, sets the order.
4. **My #2 — make yourself unbeatable first.** The tool's unbeatable state is that it cannot return PASS or FAIL its data does not carry: 「勝兵先勝而後求戰」 (my #2, quoted). **F1 approach:** `meets` requires at least one requirement row and all PASS; an empty parse is a parse failure — exit 2, never MEETS: yes. **F5 approach:** give infrastructure failure its own state; a timeout, collection error or missing report is ERROR/UNKNOWN, never "probe failed", and a red probe is proof only when a report exists. These go first.
5. **My #15 — these are the general's faults, not heaven's.** 「凡此六者，非天之災，將之過也」 (my #15, quoted). The causes sit in `verdict.py` defaults, so fix there; do not answer them with stronger briefs.
6. **My #4 — know yourself and the other side.** **F3 approach:** widen the citation regex so hyphens are allowed inside the group segment, so `EV-P1-F2` is matched, and add the raw id count (F14) so a whole class cannot vanish again. Cheap, confirmed, and it restores the tool's ability to measure itself.
7. **My #10 — avoid the solid, strike the empty.** F4 and F11 are one weakness wearing two faces — missing, null or malformed data taken as proof. **F4 approach:** `restored` must be exactly `True` to count, and take the baseline hash before the product run and compare after. **F11 approach:** validate model JSON at the boundary; wrong shape becomes UNKNOWN plus exit 2, naming the entry. One rule, not two patches. It is also the move for F2: do not show the judge the plant's name — 「形人而我無形」 (my #10, quoted).
8. **My #12 — seek it in the structure, not in the people.** 「求之於勢，不責於人」 (my #12, quoted). A structural default of "unknown unless proven" cannot be forgotten by a branch or a model; a brief can. This is how F6, F8 and F11 should be built.
9. **My #3 — plans first, walled cities last.** 「上兵伐謀…其下攻城」 (my #3, quoted), 「攻城之法，為不得已」 (my #3, quoted). The one-line contract fixes (F1, F3, F10, F12) come before the workspace and sandbox changes (F8, F9), which are the cities.
10. **My #5 and my #6 — move only on advantage; write the harm column first.** 「非利不動，非得不用，非危不戰」 (my #5, quoted), 「智者之慮，必雜於利害」 (my #6, quoted). F9 is last, not first, because F9 alarmed us. **F9 approach:** move isolation out of the briefs into the machinery — the mutant writer gets no write access to the product tree, the probes no write access outside the run folder, verified by a canary — and if the pipeline cannot run under it, narrow it (drop `workspace-write`, restrict `-C`) rather than skip it.
11. **My #17 — probe, then read the signs.** 「角之而知有餘不足之處」 (my #17, quoted). Each finding is reproduced by a probe before it is fixed: an empty spec, a hanging probe, a syntax-error mutant, a deleted report, a stale `mutants.json`, a nested `tests/`, a `../../x` runId, a canary write.
12. **The containment and loop approaches, compactly.** **F10:** on rerun, archive the whole run folder rather than resetting `workspace/`; add a per-run manifest so "the model wrote no file" becomes checkable — that is the ground F17 stands on. **F12:** reject absolute paths, `..` and separators, and assert the resolved path is under `runs/`. **F2:** keep `plant_case` out of `judge-input.json`; the scorer holds ground truth; randomize the plant. **F8:** add safe defaults rather than replace them (nested `tests/`, `test_*.py`, `conftest.py`, build notes), pass `--exclude` from the workflow, and log each exclusion with its reason. **F6:** add the one repair round to the data contract, cap it at one, re-confirm the repaired probe, and require it stays red for its case. **F7:** turn the void into the bounded loop the requirement names — rerun judging once, fresh session, different plant, record both.
13. **My #8 and my #13 — one session, and not every road is taken.** 「兵聞拙速，未睹巧之久也」 (my #8, quoted), 「途有所不由」 (my #13, quoted). Sequence by cost, reuse the 762 tests and the existing calibration runs as your supply, and say plainly which roads you did not take.
14. **My #16 — orders clear first, then enforced.** 「約束不明，申令不熟，將之罪也」 (my #16, quoted). Every fix ships with its contract (the data shape it guarantees) and its sabotage test, or it is not done.
15. **The lows, in this order if time remains:** F13 (quote the repro path), F15 (duplicate classify → human), F20 (report uncited and unknown-case probes), F14 (raw id count), F16 (out-of-scope reason), F17 (`done: false` stops the run; file and model checks), F19 (parse `meets` from `verdict.json`), F18 (cost and time) last — a SHOULD, and the first road not taken.

## What I need to know

1. Which of F2, F4, F6–F12 are reproduced, and by whom? I can only rank by measured harm, not by the label.
2. Does the live `REQUIREMENTS.md` use hyphenated group ids, or does F3 bite only the evaluator's own spec? That changes F3's rank.
3. Is there an exit-code contract for `verdict.py` — what does the workflow do with exit 2? F1 and F11 both set it.
4. When a frozen test asserts the very behaviour a finding calls a bug, does "do not weaken the frozen tests" allow correcting that assertion, or must the old behaviour stand? This changes the approach for F1, F4, F5, F11 and F15.
5. Who writes each fix's test — a different engine, per the house rules — and is that engine available in the session?
6. Does the workflow parse `meets` from relayed text (F19)? If yes, F19 must be fixed with F1 or the change is invisible.
7. For F9, may probes run as a separate unprivileged user or in a container, or must they run as the current user? That decides which containment is available.

## Costs and risks

- **The plan's price (my #8):** one session; the risk concentrates in F9, F8, F10, F6 and F7, which touch the pipeline, the copy and the loops (my #6).
- **F1:** changes MEETS semantics and exit codes; a caller reading MEETS yes/no can break. *Notice:* a full calibration run, and any rise in PASS must trace to a restored citation or a new faithful red probe.
- **F3:** a wider regex can over- or under-match, shifting the matrix. *Notice:* before/after citation count; no already-cited probe may lose its citation.
- **F5, F4, F11:** honest UNKNOWNs will rise, so some current PASS cases become UNKNOWN. That is the point, but it can hide a real product bug behind UNKNOWN (my #6). *Notice:* the seeded-fault catch stays at ≥5 of 6; every lost PASS carries its reason in the evidence log.
- **F9:** the highest chance of breaking the pipeline — the writer must still write mutants, the runner must still run pytest. *Notice:* one full end-to-end run and a canary write that must fail; revert to narrower containment if it cannot run.
- **F10:** a hard reset destroys the previous run's journal — evidence loss (my #3, whole over broken). *Notice:* archive, and assert the old folder still exists.
- **F8:** over-broad excludes can remove production source or a root `conftest.py` the product needs. *Notice:* product-versus-copy file-list diff; non-test source must be identical.
- **F2:** if ground truth moves to the wrong place, the judge can no longer be scored. *Notice:* the scorer still reports the plant.
- **F6, F7:** new model calls cost money and time (my #8), and a repaired or rerun judgment can be gamed. *Notice:* rounds capped and recorded; cost and catch rate compared before and after.
- **F12, F13, F15, F20:** cheap, low blast radius; the cost is test time, not risk.

## How we would know I was right

- The house sabotage check: every fix has a test that fails when the fix is undone. If any fix lacks one, I was wrong about it.
- The false-verdict probes: empty spec (F1) → exit 2, never MEETS; hanging probe and syntax-error mutant (F5) → never PASS; missing `restored` (F4) → not restored; malformed model JSON (F11) → UNKNOWN, exit 2; stale `mutants.json` (F10) → not seen; nested `tests/` and `conftest.py` (F8) → absent from the copy; canary write (F9) → fails; `../../x` runId (F12) → rejected.
- A calibration rerun: still catches at least 5 of 6 seeded faults; UNKNOWN may rise; PASS does not rise unless a citation was restored or a new faithful red probe appears.
- After F3, the evaluator's own hyphenated cases are cited, and the "cannot evaluate itself" UNKNOWNs disappear.
- `judge-input.json` contains no plant key (F2), and the scorer still detects the plant.
