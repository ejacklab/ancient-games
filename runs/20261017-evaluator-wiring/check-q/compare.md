# Six experts — is the requirements evaluator ready to be the judge of every build?

Question: `runs/20261017-evaluator-wiring/check-question.md`. Answers: `check-q/<expert>/answers/<expert>.md`.
Labels: *quoted* (from an answer), *my reading*, *not measured*. The compare step picks no winner and decides
nothing. The main agent decides.

| | Linus | 范蠡 Fan Li | 孫子 Sun Tzu | 老子 Laozi | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | "Not ready as the sole judge of every build"; says it could not read the snapshot | "not ready ... today"; ready after use cases, guard bridge, five states, milestone scoping | "No, not as the sole judge of every build; yes, as one independent check, after five changes" | "Not as *every* build": it reads no use cases, and its parser cannot read this repo's spec grammar | **No usable answer** (timed out after one rerun) | "Not yet ... ready after two changes and one decision from EJ (O8)" |
| Main items used | #2, #7, #3, #18, #9, #5, #13 | #18, #1, #3, #7, #10, #14 | #1, #2, #4, #17, #12, #16, #5, #6, #14 | #1, #8, #2, #4, #16, #18, #19, #6 | — | — |
| Insights cited | — | — | — | — | none (no answer) | — |

All table cells are *quoted*, or for the items *my reading* of what each answer cites as "my #N".

## Where they agree

- **Not ready as the judge of every build.** All five usable answers say so (*quoted*, Answer sections). None says "ready" today.
- **It does not read use cases, and R12.2 names them.** All five (*quoted*: Linus point 3, Fan Li 3, Sun Tzu 3, Laozi 1, Dario 4).
- **The cost blocks "every build".** All five cite about 0.8–1.2M subagent tokens and 20+ minutes per evaluation (*quoted*). Laozi and Dario add that `cost.json` records `"tokens": "not reported"`, so no token limit can be enforced (*quoted*, `model_io.py:400-405`).
- **Three result states are not enough. Memory-check needed five.** Linus, Fan Li, Sun Tzu, Laozi and Dario all say this (*quoted*).
- **Nothing connects `verdict.json` to `guard fail --found-by evaluator`.** Fan Li, Sun Tzu, Laozi and Dario say no adapter exists. Linus proposes one (*quoted*).
- **A crash or timeout never becomes PASS.** Fan Li, Sun Tzu, Laozi and Dario agree. Linus: "I don't know" (*quoted*).
- **A run-level crash ends as `blocked` with no verdict, not as a per-requirement UNKNOWN.** Sun Tzu, Laozi and Dario say this, and Fan Li says "UNKNOWN or BLOCKED" (*quoted*, `evaluate-requirements.js:50-70`, `DATA.md:230-238`).
- **The PASS rule disagrees with EV-C3.2 (backlog O8).** Fan Li, Sun Tzu, Laozi and Dario all note it: the code passes when one probe goes red, while the requirement's words say every probe (*quoted*, `verdict.py:139-144`, `BACKLOG.md:8-11`).
- **Only red probes get the faithfulness check, so a green probe that misreads the sentence can still earn PASS.** Sun Tzu, Laozi and Dario (*quoted*). Fan Li calls the PASS side safe apart from O8 and F5(c) (*quoted*).
- **Run the full evaluator on fewer builds than all of them.** Fan Li says milestone gates, Sun Tzu says acceptance and release builds, Laozi says "the build the owner names, once", Dario asks "only for a finished product", and Linus says an owner-adjudicated pilot first (*quoted*).

## Where they disagree (side by side, quoted; never averaged)

**1. Should use cases come into the evaluator?**
- Fan Li: "Parse `USE_CASES.md` (Must change first)" (*quoted*).
- Linus: "**Now:** ingest canonical use cases and map them to requirements and evidence" (*quoted*).
- Sun Tzu: "Either read `USE_CASES.md` and give each use case its own cases and verdicts, or require every use case to trace to requirement ids and check the trace" (*quoted*).
- Laozi: "**My reading: subtract the third reader.** ... the verdict's coverage manifest should carry one row per accepted use case, reading **"no case serves U3"** — and that row is the owner's to judge" (*quoted*).
- Dario asks it as a question and does not take a side (*quoted*).

**2. Where O8 (the PASS proof rule) ranks.**
- Sun Tzu ranks it first: "Settle the PASS proof rule" (*quoted*).
- Dario puts it in "ready after": "EJ settles O8" (*quoted*).
- Laozi puts it under what can wait: "O8 ... Dave measured that the literal reading loses 71% of PASSes for no extra fault caught" (*quoted*).
- Fan Li also says it can wait: "calibration proved the current in-tree boundaries and Dave's guarded rules function safely in practice" (*quoted*).

**3. Is a blocked or crashed run a guard failure?**
- Laozi: "**A blocked run is a failure, not silence.** ... the wiring must log it with `--found-by evaluator`" (*quoted*, citing R12.1).
- Linus: crashes and timeouts "never invoke `fail --found-by evaluator`"; "UNKNOWN and operational errors must be routed to the owner's review policy" (*quoted*).
- Sun Tzu: "could-not-run / blocked → an `R12.1` failure or an owner note, never a pass". He leaves it open and asks it (*quoted*).

**4. How safe is the PASS side?**
- Fan Li: "its core safety invariants hold (it does not report PASS without proof ...)" (*quoted*).
- Sun Tzu: "**But two 'yeses' remain:** the proof can be *partial* ... and the proof can be a *shared misreading*" (*quoted*).
- Laozi: "**A wrong PASS is the dangerous direction here**". He also names one code path, `probe_matrix.py:153` (*quoted*).
- Dario: "Mostly no, with three gaps" (*quoted*).
- Linus: "PASS without proof ...: I don't know" (*quoted*).

**5. What "ready" would take.**
- Sun Tzu: five changes, a per-run budget and "a second-product calibration with 2+ judged cases" (*quoted*).
- Fan Li: four changes (use cases, bridge, five states, milestone scoping), with no second calibration named (*quoted*).
- Dario: spec forms plus use cases, "one calibration on a second product", and O8 (*quoted*).
- Linus: a schema, evidence gates, use cases and an adapter "**Now**", then a pilot (*quoted*).
- Laozi: five items. Item 2 is "One grammar for spec files ... without it every build here blocks at step 1" (*quoted*).

**6. Do the parser's inputs fit this repo?**
- Laozi and Dario: the parser reads one grammar that `memory_check/REQUIREMENTS.md` and `docs/HARNESS_REQUIREMENTS.md` do not use (*quoted*).
- Sun Tzu marks EV-R1.1 "met" and Fan Li says the parser "extracts requirement IDs" (*quoted*). Neither tests it on this repo's specs.
- *My reading:* these answers do not contradict each other. "Met" is judged against the evaluator's own spec, and Laozi and Dario judge fit with the repo.

## What each added that the others did not

- **Linus:** progress records should carry "the requirement ID, current disposition, evidence/reproduction link, and cost". The guard adapter should be versioned and "default to no evaluator-failure command unless the report identity, verdict, evidence, and reproduction validate" (*quoted*).
- **Fan Li:** a pattern change. The builder's fast tests govern ordinary builds, and the evaluator is "the independent external judge triggered at designated milestone reviews". Fan Li also predicts that three consecutive small commits would exceed 3M tokens (*quoted*; the prediction is *not measured*).
- **Sun Tzu:**
  - A per-requirement table: "17 met, 7 partial, 2 not met" (*quoted*; he says it is his reading).
  - **EV-R3.2 is not met:** the judge copy is written to `/tmp/evaluator-judge-<runId>/` (*quoted*). *My reading:* `model_io.py:244` returns `Path("/tmp") / f"evaluator-judge-{name}"`, which matches.
  - The run does not describe itself: no commit, builder, engine or run status.
  - The `guard fail` fields that `verdict.json` cannot fill.
  - Reruns duplicate failures unless keyed on runId and case.
  - A "matched misreading" test.
  - A pattern change: a judge contract and status table before the experts are asked (*quoted*).
- **Laozi:**
  - The spec-grammar block. *My reading, measured by this compare step:* `python3 -I snapshot/tools/evaluator/spec_parse.py --requirements <f> --out /tmp/...` printed "no requirement ids found" and exit 2 for `memory_check/REQUIREMENTS.md` and for `docs/HARNESS_REQUIREMENTS.md`. For `docs/index-md/REQUIREMENTS.md` it printed "10 groups, 33 ids" and exit 0. This matches Laozi's step 7. Dario predicted "MEETS: no" at `verdict.py`; the measured stop is earlier, at spec parse.
  - The empty-JUnit crack at `probe_matrix.py:153`. *My reading:* the line is `return Run(results or {key: "fail" for key in plan}, OK, errors)`, as quoted. Whether it yields PASS end to end is *not measured*.
  - `found_by` defaults to `"cli"` (`journal.ts:222`).
  - A three-line pre-check before the 20-minute run.
  - A pattern change: "a judge reports the coverage it did **not** judge beside the verdict it did" (*quoted*).
- **Dario:**
  - Probes are pytest only, while the newest tools are TypeScript. "Whether pytest probes can drive a bun product, I don't know" (*quoted*).
  - `found_by` is a free string, so "the wiring must make the adapter the only caller" (*quoted*).
  - A cheap re-check after a fix cost about 54k tokens (K1e), and the workflow has no argument for it (*quoted*).
  - `build/evaluator` is unmerged: "Nothing can be wired on master before that" (*quoted*).
- **Dave:** nothing. He has no usable answer, and none is filled in.

## What they need to know (merged, each with its options)

1. **Use cases in the evaluator.** Options:
   - (a) a third input with a verdict per use case (Fan Li, Linus; Fan Li also asks: model-judged, executable probes, or both);
   - (b) every use case traced to requirement ids, and the trace checked (Sun Tzu);
   - (c) use cases stay out, and the owner judges a coverage row per use case (Laozi).
   Dario also asks whether use cases' `Fails if` lines count as requirements.
2. **The PASS proof rule (O8).** Options:
   - (a) the literal EV-C3.2: every probe red on its mutant;
   - (b) one red is enough, as the code and `DATA.md:164` do today, and EV-C3.2 is amended;
   - (c) defer it to a pre-registered six-plant experiment (Laozi, citing Dave's proposal).
3. **One spec grammar.** Options:
   - (a) widen the parser, which changes EV-R1.1 and the DATA rules;
   - (b) write specs in the evaluator's grammar.
   Dario: "one or the other, not both". Laozi and Dario ask this.
4. **What "every build" means, and the budget.** Options:
   - (a) every agent build;
   - (b) acceptance, release or milestone builds only;
   - (c) only a build the owner names.
   The budget is either none or a named limit. A named limit needs token reporting first, because tokens are "not reported". Asked by Fan Li, Sun Tzu, Laozi and Dario.
5. **A blocked or crashed run.** Options:
   - (a) a guard failure `--found-by evaluator`, which owes an insight (Laozi);
   - (b) a distinct R12.1 record (Sun Tzu);
   - (c) an owner note or the owner's review policy, never a failure (Linus).
6. **What each state that is neither PASS nor FAIL does** (UNKNOWN, not applicable, needs a reviewer, could not run, missing output). Options: block, request review, retry, or approve (Linus). Sun Tzu also asks whether any UNKNOWN should ever be a failure.
7. **The write boundary (EV-R3.2).** Options:
   - (a) amend it to allow a named, cleaned scratch folder outside `runs/<runId>/`;
   - (b) move the judge copy inside the run folder and accept the F2 plant leak (Sun Tzu).
8. **Merging `build/evaluator`.** Options:
   - (a) merge before any wiring (Dario: nothing can be wired on master before that);
   - (b) wait until the contract changes are settled (Sun Tzu).
9. **TypeScript products.** Options:
   - (a) judge only Python products;
   - (b) extend the probes to drive bun/TypeScript.
   Dario asks; the files do not answer it.
10. **The first product to judge** (Laozi). Options:
    - (a) one already in the evaluator's grammar, such as `docs/index-md`;
    - (b) `memory_check` or a harness-style spec, which puts question 3 first.

Not asked, because it has a stated default: whether a non-git product may use the workspace manifest hash as its "named commit". Sun Tzu's default is yes (*quoted*).

## Check

- **Results from the experts-decide run (*quoted* from the step's input and each `check.txt`):**
  - Linus, Fan Li, Laozi, Dario: pass.
  - Sun Tzu: fail, on one quote: 「形之而知死地之地」, where the nearest line in the list is 「形之而知死生之地」 (1 character differs).
  - Dave: fail on every section ("missing section ## Answer" and four more), "loaded insights but cites none", and "cites no item at all".
- *My reading:* each `check.txt` also lists "no answer file" for the other five experts. Each check ran inside one expert's own subfolder, so those lines are expected and are not failures of those experts.
- **Engines, from each `status.json` (*quoted*):**
  - Linus: mcode `minimax/MiniMax-M3.1-Flash-Preview`, **a fallback from codex** ("codex has 1% left (20% or less)"), 76 s.
  - Fan Li: agy `gemini-3.8-flash-medium`, 246 s.
  - Sun Tzu: dsh `deepseek-flash`, 442 s.
  - Laozi: opencode `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, 176 s.
  - Dave: claude `claude-opus-5-5`, exit 124, "timeout after 540 s". His answer file and log are both 0 bytes after one rerun. **He has no usable answer.**
  - Dario: claude `claude-sonnet-5-5`, 222 s.
- **What the check did not catch (*my reading*):**
  - Linus passed the check, but his answer says "the snapshot contents were neither pasted nor readable in this session". Every one of his file citations reads `line unavailable`, so his points rest on the question's own facts, not on the files. The check does not test whether a cited path was read.
  - Laozi's answer file starts with two lines of engine narration ("I'll read the brief first.") before its heading.
- **Who wrote the check:** Claude wrote the check script. It establishes that the sections are present, that items are cited, and that each Chinese quote matches its list. It does not establish that an expert applied a rule correctly, or that a `file:line` citation says what the expert claims.
- **What this compare step checked itself (*my reading*):**
  - It read `probe_matrix.py:150-153`, `model_io.py:240-244` and `verdict.py:139-144` in the snapshot. Each matches the expert's quote.
  - It ran `spec_parse.py` on three spec files, with the results under Laozi above.
  - Every other expert claim is *not measured* here.
