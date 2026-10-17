# Answer — is the requirements evaluator ready to be the judge of every build?

## Answer
Not yet. The verdict script is careful, and a crash or timeout never turns into PASS. But the evaluator cannot read the spec forms this repo now writes, it ignores use cases, and it has been calibrated on one Python product. A full run costs about 0.8M subagent tokens and 20+ minutes. It could be ready after two changes and one decision from EJ (O8, below).

## How I decided
Paths below are under `snapshot/` unless they start with `runs/` or `.claude/`. "Reading" means I inferred it from the code and did not run it. I did not rerun the tests. The 177 passed comes from `runs/20261017-evaluator-wiring/nodes/evaluator-tests.txt`.

1. **I compared the vision's "never" list (`docs/evaluator/VISION.md:30-40`) with what `tools/evaluator/verdict.py` does.**

   What works, with evidence:
   - **EV-P1.3, the script decides.** `verdict.py` computes every case and `meets` (lines 83-150, 229-237). A model's text is never the verdict.
   - **EV-P1.2, no MEETS with a gap.** `meets` is false with any non-PASS row, with no in-scope rows, or with unparsed ids. A missing optional input counts as no evidence, so the case lands on UNKNOWN (lines 23-28, 85-89).
   - **Safety mutants.** Seven mutants of `verdict.py` were all caught. They included PASS without a red mutant, FAIL without a faithful confirmation, a missed plant, and MEETS with an UNKNOWN (`state.md:61`).
   - **EV-R1.3.** A planted requirement with no Fails if came back UNKNOWN (`state.md:70`).
   - **EV-R2.1.** The planted marker in the product's tests was never seen (`state.md:70`).
   - **Real defect found.** The evaluator found a real defect (B1-F2) and later showed it fixed (`state.md:83`, `:85`).
   - **EV-C3 on seeded faults.** It turned 5 of 6 seeded faults from PASS to FAIL, each on the right case. The product's own tests caught 6 of 6 (`state.md:73`).

2. **Can it report PASS without proof?** Mostly no, with three gaps.
   - **O8 is unresolved.** EV-C3.2 reads "a probe that stays green on its mutant is unproven". The code gives PASS when one probe goes red on the mutant (`verdict.py:131,141-142`). The requirement and the code disagree, and EJ deferred the question (`BACKLOG.md:8-11`; `state.md:87`).
   - **A single-probe mutant run is not checked for "everything went red".** Without a recorded `runs` status, it still counts as proof (`verdict.py:132-134`; `BACKLOG.md:21-22`).
   - **Only red probes get the faithfulness check (EV-C4).** A green probe that checks less than the requirement sentence can still earn PASS if it goes red on the mutant. This is my reading. K2's one miss was the opposite case, a probe that checked too much (`state.md:73`).

   A judged PASS is a single Sonnet "yes" with quoted evidence and a plant check. That plant check was exercised with at most one judged case (`BACKLOG.md:42-44`), and no judged cases ran in K1d (`state.md:83`).

3. **Crash or timeout.**
   - **Probe timeout.** A timeout makes every probe red. `probe_matrix.py:124-125` records the status, and `verdict.py` turns it into UNKNOWN "unproven: the mutant run was not healthy". `tests/test_evaluator_r1.py:218-227` tests this for timeout and no-report.
   - **Product-side timeout (reading).** It leaves no failure output. `model_io.py:204-206` voids that confirmation, so the case ends UNKNOWN, not FAIL.
   - **Engine call fails.** A failed engine call, an empty result, or a missing model file blocks the step (`model_io.py:174-177`; `evaluate-requirements.js:64-70,139-141`). The run returns `{status:'blocked'}` and writes no `verdict.json`. That matches EV-C6.2, but it is "blocked", not UNKNOWN.
   - **Result.** Nothing I found turns a crash or timeout into PASS. A consumer must still read both "UNKNOWN row" and "blocked run" as "not evaluated", never as "no failures".

4. **Inputs.**
   - **Use cases are not read.** The spec is `REQUIREMENTS.md` plus `VISION.md` only (`workspace.py`, `spec_parse.py`). R12.2 says failures are judged against vision, use cases and requirements (`.claude/skills/workflow-design/guard/src/insight.ts:361-364`).
   - **The parser needs one exact form.** That form is `**ID — Title**` group headings, `- **id**` bullets and `- **Fails if**` bullets (`spec_parse.py:26-31`; `DATA.md` E1 rules 1-3 and 7). Vision lines are read only under a bold `**What it will never do` line.
   - **The repo's newest spec uses a different form.** `memory_check/REQUIREMENTS.md:9` writes `**F1 (MUST) The locations.** … Fails if: …` as a paragraph. `memory_check/VISION.md:20` uses a `## What it will never do` heading. `USE_CASES.md:6` uses `## U1 —` headings.
   - **Likely result on memory_check (reading, not run).** I expect zero groups and zero vision lines. `verdict.py:233-234` would then give "MEETS: no — no in-scope requirements". That fails loudly, but it is useless.
   - **Python only.** Probes are pytest and stdlib only (`docs/evaluator/briefs/probes.md:5,29`). The newest tools here (`memory_check`, guard, code map) are TypeScript. Whether pytest probes can drive a bun product, I don't know. The files don't say.

5. **Cost and runs.**
   - **Cost per run.** K1 took 822k tokens, 21 minutes and 14 agents. K1b took 774k tokens, 24 minutes and 14 agents. K1d took about 1.24M tokens and 36 agents over two legs (`state.md:69,71,83`). That is about the cost of building the evaluator's pieces: 0.5–1M tokens (`workflow-design.md:209`).
   - **Cost is not recorded.** `cost.json` writes tokens "not reported" and models "requested, not verified" (`model_io.py:402`; `BACKLOG.md:27-28`). EV-P3's limit is still open.
   - **Cheap re-check is manual.** Reusing the probes and mutants after a fix cost about 54k tokens (K1e, `state.md:85`). The workflow has no argument for it.
   - **Codex is a hard dependency.** The mutant step is hardcoded to Codex, and EV-C6.2 forbids a fallback. Codex hit its usage limit twice in the build (`state.md:51,79`).
   - **Engines differ from EV-C6.1.** Confirm and judge are always Sonnet (`evaluate-requirements.js:75,84,86`). EV-C6.1 says Codex when Claude built the product.
   - **Where it lives.** It exists only on `build/evaluator`, which is unmerged and unpushed (`runs/20261013-calibration/report.md:88-91`).

6. **How a FAIL becomes a guard failure.**
   - **The pieces exist.** `guard fail --check --input --expected --actual --reason --evidence --found-by evaluator` exists (`cli.ts:37`). A `verdict.json` FAIL row has the id, the reason and the repro command, and `requirements.json` has the case text.
   - **Nothing connects them.** No adapter exists.
   - **The guard trusts the label.** `found_by` is a free string (`journal.ts:222`), so any caller can write `evaluator`. Judged failures stay open until an insight answers them (`insight.ts:361-373`).
   - **A false FAIL costs real work.** It forces an insight. Evidence on FAIL precision so far:
     - K1: 0 of 28 FAILs reproduced (`state.md:69`).
     - K1b: one of two FAILs was false (`state.md:71`).
     - K1d: 2 of 2 were real (`state.md:83`).
     - That is one product only.

7. **Result states.** The evaluator has PASS, FAIL, UNKNOWN and out of scope. The reason is free text ("needs EJ", "no probe", "judging void: plant missed"). Memory-check needed five states. A "could not run" outcome exists only as a blocked run with no file.

## What I need to know
1. **Which products must it judge?** Only those whose specs use the evaluator's form, or every project here, including the TypeScript tools? This decides whether the parser changes or the spec templates do. It should be one or the other, not both.
2. **Should use cases be a third input?** R12.2 names them. If so, should their `Fails if` lines count as requirements?
3. **Is evaluating at about the cost of building acceptable for every build,** or only for a finished product, with a cheap re-check after each fix?
4. **O8.** Does "proven" mean one probe red on the mutant (the code today) or every probe (the requirement's wording)? Dave measured that the literal reading drops 71% of PASSes and catches no extra fault (`state.md:87`).
5. **Will `build/evaluator` be merged?** Nothing can be wired on master before that.
6. **Can a pytest probe check a bun/TypeScript product?** The files don't answer this.

## Costs and risks
- **The first run on a new product has been costly.** The first live run found 4 bugs (K1). K1b and the blind review found more, including 20 findings in criteria. A second product will likely find more.
- **Spec form mismatch gives a useless run** (reading, not run). The evaluator may report "no in-scope requirements" for every recent tool.
- **A false FAIL costs EJ's and the agent's time.** It becomes an open insight in the guard, and precision is measured on one product.
- **Codex limits can stop the whole evaluation** (no fallback), so it is a poor gate for every build.
- **Blindness is narrowed, not enforced** (`BACKLOG.md:15-19`). Reads outside the workspace folders are not prevented.
- **Self-labelling in the guard.** Any caller can write `--found-by evaluator`, so the wiring must make the adapter the only caller.
- **O8 is open,** so "MEETS" and every PASS rest on a rule EJ has not settled.

## How we would know I was right
Run the evaluator on `memory_check` at a fixed commit, using its vision, use cases and requirements. Set the checks before the run:
1. The manifest lists every requirement id in `REQUIREMENTS.md`.
2. Six seeded faults, each in one requirement, give not-MEETS and a FAIL on the right requirement.
3. Every FAIL reproduces from its printed command, and EJ agrees each is real.
4. Tokens and time are recorded.

If that run needs repair rounds, like K1 did, a second-product calibration was needed. If it passes cleanly, the calibration was cheaper than I think. The spec-form claim is checked by one command: run `spec_parse.py` on `memory_check/REQUIREMENTS.md` and count the groups.

Ready: no, not as the judge of every build today.
Ready after: (1) it reads the repo's spec forms plus use cases, (2) one calibration on a second product where every FAIL reproduces and is real, and EJ settles O8.
Not ready because: it cannot parse the current specs (reading), it has been calibrated on one Python product, it costs about 0.8M tokens per run, and its PASS rule still disagrees with EV-C3.2.
