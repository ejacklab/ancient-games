# Dave — are P3's checks real: what shows each can fail, and what is its control?

## Answer
**P3: strengthen the check before it runs as a loop. Two parts are not loop-ready as written.** I ran a control (the canned stub) and it shows the evaluator cannot tell a real tool from a lookup table: Codex's 20-line stub, which only reads `eval/cases/fixtures.json` and replays `eval/stub/answers/`, scores 8 of 8 checkable requirements MET (I re-ran it today). The builder may read both of those folders, and the failure feedback hands it "expected against actual". Also, the evaluator command as written exits with an error on every attempt. Line by line:

- **P3 evaluator command: not loop-ready as written.** `bun eval/run.ts --tool "bun src/cli.ts" --cases eval/cases/fixtures.json` has no `--out`. I ran it on the stub and got `Error: --tool and --out are required`, exit 2. A check that always fails tells us nothing. Fix: add `--out runs/20261014-code-map-build/p3/<req>-a<n>/eval`.
- **P3 evaluator as the round's judge: strengthen.** Missed failure: a `src/cli.ts` that matches the 37 known argument lists and prints the canned answers would pass every round. Add a held-out control the builder never sees: a copy of the fixtures with every file shifted down k lines and identifiers renamed, with the expected locations shifted to match. Prediction: the stub drops to mostly NOT MET there and a real tool stays MET. Feedback from this set gives the case id and requirement line only, never the expected values.
- **P3 frozen `bun test`: strengthen.** "Failing before the build" proves almost nothing when `src/` is empty, because every test fails on a missing import. The control is a plant. Once a round passes, the COO plants 3 to 5 one-line faults in `src/` (for example, a test fake counted as an implementation, an off-by-one line, a dropped `seen` stop). The frozen tests plus the evaluator must catch each one. That is the same kind of control that gave the evaluator its 15 of 15.
- **P3 `bunx tsgo --noEmit`: strengthen.** Missed failure: `code_map/tsconfig.json` is not on the "must not change" list and is not hashed. A builder that changes `include` or turns off `strict` makes tsgo pass over broken types. Hash `tsconfig.json`, `package.json`, `bun.lock` and the absence of a `bunfig.toml`. Then plant one type error once to show the check fails.
- **P3 sha256 check: strengthen.** It covers only the frozen tests and `eval/`. A new `bunfig.toml` with a test `preload`, or an edit under `node_modules/typescript`, changes what the tests mean without touching a hashed file. Replace it with a snapshot of every file under `code_map/` outside `src/` (with a lockfile hash standing in for `node_modules`), and show it fails on one planted edit.
- **Round R1 (first): not loop-ready in this position.** The facts say R1's four cases also check map, chain, tests and callers. So a NOT MET on R1 cannot say whether code ran. It will fail for unrelated reasons, the 3 attempts will likely run out, and the "no earlier MET turns NOT MET" protection has nothing to protect. Either judge round 1 on `markerCreated: false` and exit 0 for the four commands (both are already in `report.json`), or move R1 after the A1, A2 and A3 rounds. Control: plant `import("../eval/fixtures/marker/main.ts")` in `src/`. The marker must appear and R1 must go NOT MET. The evaluator's own negative test already shows marker detection works.
- **Rounds R2, A2, A3, A1, L1: strengthen** with the held-out shifted set above. Each has only 4 to 10 cases on 6 small fixtures, so a requirement can reach MET on the cases alone.
- **Round A5: loop-ready as written for the tool part.** Every answer is already checked for "no `map` unless the command is `map`" (`contract.ts` line 79). The agent part stays NOT CHECKED until P6.
- **Round R3 (last): loop-ready as written for what it claims**, with the stated limit that `unshare -rn` does not see a connection failure the tool catches itself. Control: one planted `fetch` that ignores its error. Prediction: R3 stays MET, which is the known blind spot, and it should be reported as one.
- **Reviewers (孫子, 范蠡): strengthen.** They have no control. Plant one diff that hard-codes a fixture answer and see whether either of them returns CHANGE. Per house rules, the plant must not be named in any file the workers read.

## How I decided
1. My #1: for each check I named the result that would show it can fail: a plant it must catch, or a cheat it must reject.
2. My #5: I used what is already measured before asking for anything new. COVERAGE.md has the 15 of 15 plants on the stub, the stub at 8 MET, and the marker negative test. What that shows: the evaluator catches a wrong canned answer. What it does not show: that it catches a tool that is right on the 37 cases and wrong elsewhere.
3. My #2: two cheap runs instead of arguing. The command as written exits 2 (`--out` missing). The stub control scores Requirements MET 8, NOT MET 0, NOT CHECKED 2, and Cases MET 37 of 37.
4. My #4: the stub is the right control for the evaluator, and it passes. So the evaluator alone cannot be the round's judge (my reading of that result).
5. My #4 again: for the frozen tests, "fails on empty `src/`" is not a control, because it fails for the wrong reason. A plant in working code is the control (my reading).
6. My reading, from `code_map/tsconfig.json` and `package.json`: the hashes miss the config files that decide what tsgo and `bun test` check.
7. My #6 and #7: Batesian mimicry, where a harmless species copies a warning signal and predators catch it by testing signals it has not copied. The fit: the stub copies exactly the signals it was shown. The difference: the builder does not mean to deceive, but pressure to pass the tests has the same effect. The mechanism I borrow is novel probes (the shifted copy). The condition holds, so I kept the analogy.
8. My #3: predictions to write down before round 1 are listed under the last section.

## What I need to know
- Can opencode be denied read access to `code_map/eval/` while it builds? If it can, the held-out set is cheaper. If it cannot, the shifted copy has to live outside the repo, and opencode refuses files outside the repo, so the COO runs it.
- Do the frozen tests call `src/` functions or the CLI? If they call the CLI, they can also be run against the stub as a second control.
- Will EJ accept a change to the round order (R1 after A1, A2, A3)? If not, R1's round needs the marker-only judgement instead.

## Costs and risks
- Shifted held-out set (my #4, #8): about one script plus one COO run per round. Risk: a line shift alone is beaten by a tool that matches on names, so renaming is needed too. The shifted copy also loses the R1 marker check, which is tied to the bundled fixture path, so R1 stays on the original fixtures.
- Plants per round (my #4): 3 to 5 extra evaluator and test runs per round, roughly 8 rounds × 5 runs. Risk: plants I write share my blind spots (known-answers note), so a plant passed is only a hint (my #10).
- Wider snapshot hash (my reading): almost free. Risk: false alarms from `bun install` touching `node_modules`. Hash the lockfile, not the folder.
- Moving R1 later (my #1): costs nothing to run, but it changes EJ's order, so it needs their approval.
- Doing nothing (my #9): the loop can report "8 of 8 MET" for a tool that only replays answers. The stub already did that.

## How we would know I was right
Written down before any round (my #3):
- The stub on the shifted set: most cases NOT MET (prediction: 30 or more of 37).
- Each planted fault in `src/`: caught by the frozen tests or the evaluator, reported as "caught n of m".
- The marker plant: R1 NOT MET.
- The tsconfig plant: caught by the new hash.
- The `fetch` plant: R3 stays MET, which confirms the stated blind spot.

I am wrong about the evaluator if the stub stays MET on the shifted set: that would mean the shift is not a real control. Stop date: before round 1 starts. A miss on any plant is reported with the same weight as a pass (my #9). How sure I am: the stub result and the exit-2 result are measured (n=1 each, deterministic). Everything about plants and the shifted set is a prediction, n=0 (my #10).
