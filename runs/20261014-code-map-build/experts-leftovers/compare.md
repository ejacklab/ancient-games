# Six experts — eight code-map decisions for the opencode run

Question: `runs/20261014-code-map-build/briefs/leftovers/decisions-question.md`. Answers: `<expert>/answers/<expert>.md`
in this folder. Every line is labelled *quoted* (from an answer or the question), *my reading*, or *not measured*.
This file decides nothing; the main agent decides.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) | COO's pick |
|---|---|---|---|---|---|---|---|
| Answer (one line) | "1b, 2a, 3b, 4a, 5b, 6a, 7c, and 8b with a supplied by the opencode run" | Agrees with the COO on 2, 3, 4, 5, 7, 8; "differ on 1 and 6" (1b read through 3c, 6c conditional) | "Take the COO's eight picks — a, a, c, b, b, a, c, b" | COO on 2, 3, 5, 7, 8; 1a "not by 范蠡's route"; 6a "plus one limit"; 4a | COO on six; "differ on two: 3 (b, not c) and 6 (c for now, not a)"; adds a clause to 1 | COO on 1, 2, 4, 5, 7, 8; "disagree on 3 and 6" (3b, 6b `count`) | a, a, c, b, b, a, c, b |
| 1 dynamic limit = missing? | b | b (under 3c; 1a if 3 is a or b) | a | a, no clause | a + "or a limit contradicts the code" | a | a |
| 2 inline body adds a level? | a | a (+ sentence in A2) | a | a (+ sentence in A2) | a | a | a |
| 3 "known" | b | c | c (b if "known" also governs A1/L2) | c | b | b | c |
| 4 A5 interface-required limit clause | a | b | b | a | b, provisional | b | b |
| 5 Fails-if layout | b | b | b | b | b | b | b |
| 6 fake rule on opencode | a (with the `throughFake` predicate corrected) | c, conditional | a | a + one limit naming the number left out | c for this run (no `--fake-rule`) | b (`count`) | a |
| 7 sibling rule | c | c, a's rule chooses the globs | c, a's rule chooses the globs | c | c, a's rule checks each glob | c | c |
| 8 test files | b tool / a run | b tool / a run | b tool / a run | b tool / a run | b tool / a run | b tool / a run | b tool / a run |
| Main items used | #2, #3, #5, #7, #9, #13 | #4, #5, #7, #9, #10, #11, #12, #14, #18 | #1, #2, #3, #4, #5, #6, #8, #13, #14, #16, #17 | #1, #2, #4, #6, #7, #8, #17, #18, #19 | #1–#10 | — | |
| Insights cited | — | — | — | — | `runs/20261014-code-map-build/insight.md#F-60cad515` ("It changed no pick") | — | |

Table rows 1–8 and the items are *my reading* of each answer's table and "How I decided"; the one-line answers are *quoted*.

## Where they agree

- **2a, six of six** *(quoted, each table)*. Reason shared by all six: a level is a call link, and entering a body is
  not one *(my reading)*. Dave and Dario add that under b a rewrite to `Effect.gen` would shift levels, against
  "track changes" *(quoted)*.
- **5b, six of six** *(quoted)*. Shared reason: the evaluator gives one verdict per Fails-if line and the spec already
  separates the tool's part from the agent's (`NOT CHECKED → P6`) *(my reading)*. All say two actor lines inside one
  requirement are not a split *(my reading; 范蠡 says so as a change from his round 2)*.
- **7c, six of six** *(quoted)*. 范蠡, 孫子 and Dave keep a's interface/service-tag rule as the way to choose or check
  the globs; Linus: "use shared interface or service-tag evidence to propose sibling groups" *(quoted)*.
- **8: b in the tool, a as the opencode value, six of six** *(quoted)*.
- **The COO's "about half as far" under 2b is not measured and decides nothing**: Linus, 范蠡, 孫子, 老子, Dave, Dario
  each say so *(my reading of six answers)*.
- **A false `dynamic` label on a link the type checker resolves must not pass.** Linus ("a `dynamic` label explains a
  limitation but does not restore the link"), 范蠡 ("marking it `dynamic` is false"), 孫子 ("a false `dynamic` label on
  a static link must fail as a false limit"), Dave ("a on its own lets any `dynamic` label excuse a direct call"),
  Dario ("The why must be true") *(quoted)*. They differ on which line charges it — see decision 1 below. 老子 does
  not raise this case; he reads a dynamic site as never checker-established *(my reading)*.
- **The fake-path problem on decision 6 is the spec's `throughFake` predicate.** Linus, 范蠡, Dave and Dario each read
  the spec's "candidates include a test fake" as marking tests that may wire the real implementation *(my reading of
  four answers; none checked the code — 范蠡: "I did not check it in the code"; Dario: "I did not read the code")*.
  孫子 and 老子 do not raise it.

## Where they disagree (side by side, quoted; never averaged)

**Decision 1 — is a known link marked `dynamic` a miss?**
- Linus (b): "An independently established link remains required for understanding logic; a `dynamic` label explains
  a limitation but does not restore the link."
- 范蠡 (b through 3c): "Under c a known link is one the type checker establishes, so marking it `dynamic` is false …
  The COO's pair (3c + 1a) would excuse only false limits." And: "If the owner picks 3b or 3a instead … I pick 1a."
- 孫子 (a): "A named `dynamic` limit is a sign, not a silent gap; only an unstated miss should fail A2." Guard: "a false
  `dynamic` label on a static link must fail as a false limit (L1/A5), or the carve-out becomes a hiding place."
- 老子 (a, no clause): "Under 3c a dynamic site is not a link the type checker establishes, so it cannot be a
  *missing* link; R2 and L1 already own it."
- Dave (a + clause): "a known link within the depth is missing with no limit at its site naming why, or a shown link
  **or a limit** contradicts the code."
- Dario (a): "L1 already lists 'dynamic behaviour' as a valid reason to stop, so a link with a limit at its site
  naming why is reported, not missing."
- *My reading:* 范蠡 (1b) and 老子 (1a) both pick 3c and both leave A2's missing-link line with **no added clause**;
  their letters differ, their proposed A2 text does not.

**Decision 3 — "known"**
- c (范蠡, 孫子, 老子): 范蠡: "It puts 'known' on the same ground as the vision … and R2"; 老子: "the code or description
  owns a place, the type checker owns a link"; 孫子: c, but "If it must govern A1 and L2 … I withdraw c for b."
- b (Linus, Dave, Dario): Linus: "Evidence outside this tool's successful lookup must be able to expose a missing
  relationship"; Dave: "c's link half makes the type checker judge the tool's links, so links the type checker cannot
  see, such as a callback passed as a value, drop out of A2 with no flag"; Dario: "c lets the tool's own method
  decide what counts as known."
- Against b, 范蠡: "'established from repository source' rules out nothing in a TypeScript repository."
- 老子 concedes the b side's point: "they are right that it is a real narrowing."
- Dave on how sure: "low" *(quoted)*; where b and c differ on opencode is *not measured*.

**Decision 4 — A5 clause**
- a (Linus, 老子): Linus: "A focused answer needs required qualifications even when no branch stops early"; 老子:
  "Under (b) no requirement charges the missing `{reason: "other", text: "no test-file pattern given"}`."
- b (范蠡, 孫子, Dave, Dario): 范蠡: "The clause would tie the requirement's meaning to the spec's text"; 孫子: "a second
  sentence creates a second owner for one duty"; Dave: "No failure on record shows that 'its limits' misses an
  interface-required limit"; Dario: the requirements never define "interface" *(paraphrase of his reason)*.
- 老子, Dave and 范蠡 name the same planted-copy test to settle it *(my reading)*.

**Decision 6 — fake rule on opencode**
- a (Linus, 孫子): Linus: "A test whose path substitutes a fake does not establish a path to the real function", but
  "decision 6 requires correcting the spec's test-path classification"; 孫子: "counting it would overstate reach".
- a + limit (老子): "exclude them, **and** carry one limit naming the number left out; no list of them."
- c (范蠡, Dave): 范蠡: "`exclude` hides tests that may reach the function, and `count` claims tests that may not";
  Dave: "Run with no `--fake-rule`; the spec's undecided path already gives c … Switch to a once that is measured."
- b (Dario): "`exclude` would drop real-layer tests, and `count` keeps them with `throughFake: true`."
- Against c: 孫子: "a third behaviour beside the user's `count|exclude` rule, and the spec's `TestsAnswer` has no field
  for it"; Dario: "Option c is not a rule the spec offers"; 范蠡 himself: "on paper A3's 'a fixed rule the user sets'
  is not met."

## What each added that the others did not

- **Linus:** keep `exclude` as the meaning but fix the predicate: "candidate membership does not establish
  substitution … where substitution cannot be established, report uncertainty and its limit" *(quoted)*.
- **范蠡:** the exact A2 text his picks produce (老子's "known" sentence + "Going into a body written straight into a
  call adds no level") *(quoted)*; the library-call question (question 3 below); a pattern change: "When two decisions
  in one question are linked … the brief shows the requirement text the COO's picks produce together" *(quoted)*;
  risk on 8: "A real implementation in a `test/` folder, or named `*.spec.ts`, would be labelled a test fake"
  *(quoted)*.
- **孫子:** the scope test for 3 (does "known" govern A1 and L2) *(quoted)*; a pattern change: "When the owner overrules
  a pick, write the reversing condition beside the pick in the run's state file" *(quoted)*.
- **老子:** decisions 6–8 are values, not text: "1–5 are *text* … 6–8 are *values*" *(quoted)*; full A2 and A5 text
  *(quoted, his answer)*; the fake-path limit text "N tests reach this function only through a test fake" *(quoted)*;
  three pattern changes (ask the experts only on text; every number carries its source in the question; the owner's
  reason beside a pick against the experts) *(quoted)*; risk on 2: a body run by `xs.map(cb)` or a framework handler
  "is reached by no link, so that branch of the chain ends early" *(quoted)*; risk on 8: with no `--tests`, "19 fakes
  look like implementations and the target reads ambiguous" *(quoted)*.
- **Dave:** the widened contradicts-the-code clause on 1 *(quoted)*; a flip condition per decision; he moved off his
  own P1 pick on 7: "my P1 pick (a) does not fit the interface as built" *(quoted)*; pattern change: after two wording
  rounds with the same split, "make the next trial a planted-copy or counting experiment" *(quoted)*.
- **Dario:** R2 wording: "an implementation in a test file" should read "a file the user names as a test file"
  *(quoted)*; the only expert who rests 3b on R1's "source and type information" *(my reading)*.

## What they need to know (merged; each with its options)

1. **Decision 6 — does `throughFake` (the `candidates` list) mark every test whose path crosses a fake-bearing call
   site, or only tests whose own setup wires the fake?** (范蠡 1, Dario 1, Dave 1, Linus 2)
   - Every crossing test (program-wide candidates): `exclude` drops real-layer tests → 6c (范蠡, Dave), 6b (Dario), or
     6a with the predicate corrected first (Linus).
   - Only tests that wire the fake, or none of the crossing tests wire the real one: 6a (范蠡, Dave and Dario say they
     would switch).
2. **Decision 3 — does the "known" definition govern only A2, or also A1's checked example and L2's answer keys?**
   (孫子; Dave 2 asks the measurable form: are there links an independent reader establishes from source that the
   type checker does not?)
   - Only A2 / no such links: 3c stands (孫子); Dave "would not hold out against c".
   - Also A1 and L2 / such links exist: 3b (孫子 withdraws c; Dave, Linus, Dario).
3. **Decision 1 — when a call leaves the repository, does the tool show the link to the checker-established
   declaration and stop, or leave only a limit?** (范蠡 2)
   - Shows the link: 1b under 3c holds with no clause.
   - Only a limit: under 3c A2 fails on every library call; the missing-link line needs an exception for a link that
     leaves the repository, "never one for `dynamic`".
4. **Decision 2 — is a level always a call link, including a body the framework invokes and no code calls?** (老子 3)
   - Yes: 2a.
   - No: 2b, and A2 must say so in words.
5. **Decision 4 — does the evaluator's A5 line charge an answer that drops a required limit ("fake rule not set
   (A3)" or "no test-file pattern given")?** (Dave 3, 老子 4)
   - Yes: 4b stands.
   - No: 4a (Dave switches); or L1's "another stated reason" must own it, shown in the report (老子).
6. **Decision 7 — can `--siblings` exclude a file, as in "`tool/*.ts` minus the registry"?** (老子 1, Dave 4)
   - Yes: c as written.
   - No: the spec gains exclusion (an `--exclude`), or the registry is passed as its own glob, or the group is given
     file by file.
7. **Decision 7 — which interface or service tag do the siblings in each of the three A6 modules implement; do
   `session` and `ai` have sibling groups at all?** (Linus 1, 范蠡 3, Dario 3)
   - A group exists: its glob is chosen by a's rule.
   - None: no table and the "no sibling rule given" limit (范蠡) — which Dario says "would misstate it".
8. **Decision 8 — are there opencode tests or fakes outside pattern a, or non-test files under `test/`; which pattern
   did the probe use for 63/7/1?** (老子 5, Dario 2, Dave 5)
   - None outside: pass a (老子: or the `test/` folders alone if there are no `*.test.ts` beside source).
   - Some: widen a for opencode.
9. **Decision 6, 老子's limit only — is the fake-path count per function or per module?** (老子 2)
   - Per function (his assumption): the limit sits on the `tests` answer for the function asked.
   - Per module: the limit's text changes and `tests --per-function` must state the same number.

Facts given in the question without a source — 63 of 71, the 20-implementation site, "most function bodies are written
straight into a call" — 范蠡 and 老子 note they carry no file:line *(quoted)*. *Not measured* in this run.

## Check

- **Results** *(quoted from the workflow and each `check.txt`)*: linus pass, fan-li pass, sun-tzu pass, dave pass,
  dario pass; lao-tzu **fail**: "Chinese not found in its list: 以深為根 (nearest in the list: 以深爲根, 1 character(s)
  differ)" and the same for 以約為紀 / 以約爲紀. *My reading:* 為 and 爲 are variant forms of one character; both lines
  come from 老子's item #19, which he marks `attributed`. The fail does not touch any pick.
- Each `check.txt` also lists "no answer file" for the five other experts. *My reading:* each check ran inside one
  expert's subfolder, so the others' answers were not there; the workflow counted each as pass on its own expert.
- 老子's answer file begins with three lines of narration before its heading ("I'll read that brief first.") *(quoted)*.
- **Engines** *(quoted from each `status.json`)*: Linus — codex, gpt-6.1-sol, 56 s. 范蠡 — claude, claude-opus-5-5,
  430 s, **fallback from agy, reason "task needs web"**. 孫子 — dsh, deepseek-flash (dsh headless profile), 206 s.
  老子 — opencode, minimax-coding-plan/MiniMax-M3.1-Flash-Preview, 118 s. Dave — claude, claude-opus-5-5, 366 s.
  Dario — claude, claude-sonnet-5-5, 138 s. All exit 0, ok true.
- *My reading:* with 范蠡 on the fallback, three of six answers ran on Claude models (范蠡, Dave, Dario), so agreement
  among those three is less independent than it looks.
- **What the check does not establish:** the check script was written by Claude; it compares quoted Chinese against
  each expert's list. It does not establish that an item was applied correctly, that a quoted spec or requirement
  line says what the expert claims, or that any pick is right. All six briefs share one question, which carries the
  COO's picks and reasons, so agreement with the COO is not independent evidence *(my reading)*.
