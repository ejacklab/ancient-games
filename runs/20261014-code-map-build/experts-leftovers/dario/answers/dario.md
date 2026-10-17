# Answer — eight code-map decisions for opencode

## Answer
I agree with the COO on 1, 2, 4, 5, 7 and 8, and disagree on 3 and 6. On 3 I pick b, not c, because c lets the tool's own method decide what counts as known. On 6 I pick `count`, not `exclude`, because `exclude` would likely hide real tests, at least by my reading of the spec.

| # | Pick | Reason |
|---|---|---|
| 1 | a | L1 already lists "dynamic behaviour" as a valid reason to stop, so a link with a limit at its site naming why is reported, not missing. |
| 2 | a | A2 counts levels by call links, and a body written into a call is not a call, so the same call should sit at the same level whether it is written inline or in a named function. |
| 3 | b | R1 already says "source and type information", and b gives the answer-key writer a definition that does not depend on the tool's method (L2). |
| 4 | b | "Its limits" already means all limits that apply to the answer. The clause would make A5 depend on the word "interface", which the requirements never define. |
| 5 | b | The spec already gives the tool's part and the agent's part separate verdicts, so each needs its own line. |
| 6 | b (`count`) | The tool cannot see which service layer a test provides, so `exclude` would drop real-layer tests, and `count` keeps them with `throughFake: true`. |
| 7 | c | The spec takes globs and A1 says the user sets the rule, so a is a way to choose the globs, not a tool feature. |
| 8 | b in the tool; a as the opencode value | The spec says the user sets test files and the tool has no default. R2 and A3 use "test file" without saying who decides, and the run needs a value. |

## How I decided
1. **I read the requirements, the spec, the round-2 `compare.md` and all four round-2 answers.** I did not read the code, so every claim about what the tool does comes from the spec or the experts, not from running it.
2. **Decisions 1 and 3 are a pair.**
   - Under 3c, a link is known only if the type checker establishes it. That is the tool's own method, which conflicts with L2's "by a method other than the tool's" for answer keys. 孫子 said the same in round 2 (*"if the tool is the only reader … the check and the tool still share one reading"*, quoted). The COO's reason for c, that it settles decision 1, is also its weakness: the tool can then never fail on a link it cannot see.
   - Under 3b, a link is known if the source or types establish it. Then decision 1 is needed, and 1a settles it: a dynamic link is known, but the tool is not charged if a limit at its site names the reason. The line becomes 范蠡's: "a known link within the depth is missing with no limit at its site naming why."
   - Linus's worry (*"a `dynamic` label cannot become a blanket exemption"*, quoted) is handled by the words "naming why". The why must be true.
3. **Decision 2.**
   - Linus: *"Each level requires a call link; ownership alone does not establish a callback invocation"* (quoted).
   - With b, a refactor that moves a body from inline to a named function would change the levels, which breaks the vision's "track changes" use.
   - The COO's "about half as far" is not measured. My pick does not depend on it.
4. **Decisions 4 and 5.**
   - For 4, "its limits" already covers the required limits. A clause pointing at "the interface" would misread, because the requirements do not define that word.
   - For 5, the tool's part is checked by the evaluator, while the agent's part is `NOT CHECKED → P6` (spec lines 162–164). One line for two actors would force one verdict for two parts.
   - A labelled bullet inside A2 or A5 does not split the requirement: it stays one requirement with two bullets (孫子, 老子, Linus, all agreeing).
5. **Decision 6.**
   - The spec says `throughFake` is true when the path passes a `service-call` link whose candidates include a test fake. It also says the tool has no rule for Effect wiring, and that fakes stay in `candidates`.
   - My reading is that candidates are program-wide. At the 20-implementation site, every test through it would then be marked `throughFake`, including tests that use the real layer.
   - `exclude` would drop all of those. That is the A3 failure "a test with a known path is missing", and it hides the tests an agent most needs to run.
   - `count` may over-list tests that use a fake. Each carries its evidence path and `throughFake: true`, and A3 already says static links are never called coverage.
   - Option c is not a rule the spec offers. The nearest thing is the no-rule mode, which A3 does not allow as a final state.
6. **Decision 7.** The tool takes one glob per sibling group. The COO's plan, a's rule choosing the globs and the user (EJ) owning them, fits that. The globs for this run are provisional, and EJ may overrule them.
7. **Decision 8.**
   - Keep the tool free of defaults, as the spec says.
   - Pass `test/` and `__tests__` folders plus `*.test.ts` and `*.spec.ts` for opencode.
   - R2's "an implementation in a test file" should read "a file the user names as a test file", so it does not suggest the tool knows. This is the only requirement wording change from 6–8, and the owner decides it.

## What I need to know
1. **Decision 6: does `candidates` on a `service-call` link list every implementation in the program, or only those a test's own layers provide?** If it is narrowed per test, `exclude` becomes right. The spec's "no rule for Effect service wiring" makes me assume program-wide, but I did not read the code.
2. **Decision 8: does opencode have non-test files under `test/` or `__tests__`, or fakes and tests outside those names?** This changes the glob value, not the pick. A fake outside the globs would be unlabelled and would make a target look ambiguous.
3. **Decision 7: do `session` and `ai` have sibling groups at all?** If a module has none, the spec's limit "no sibling rule given" would misstate it.

## Costs and risks
- **1a:** the line text changes, so every evaluator case's `line` field must be re-mapped before a round can be read (范蠡 and 老子 flagged this).
- **1a:** it only works if the limit's reason is true. A resolvable call wrongly marked dynamic must still fail.
- **3b:** "established from source" is broad (范蠡's objection), and 1a is what makes it workable. A1 also uses "known". If the definition is written only "in A2", the word has two senses.
- **2a:** a body's calls appear one level from the surrounding function, so a reader must look at `from`, not the heading.
- **4b and 5b:** a required limit missing from an answer is caught only by the exact-shape A5 cases, so those cases carry the line.
- **6b:** the count may include tests that swap in a fake. Reading the count without the `throughFake` flags would mislead. This is not measured.
- **7c:** the globs are a human's judgment per module. A wrong glob gives a wrong sibling table that still looks complete.
- **8:** the run's value is a convention, not a fact. A 20-fakes site shows what a wrong pattern costs.

## How we would know I was right
- **1:** a fixture with a computed-member call and a dynamic limit at its site passes A2. The same fixture with the limit removed fails. A fixture where the type checker resolves the target but the tool says dynamic fails. If no existing case covers the last one, add it.
- **2:** `chain --down` from a function reaches the same links whether a call sits in an inline `Effect.gen` body or in a named function with the same body.
- **3:** a different agent writes the opencode answer key from the source by a method other than the tool's. Every key item then either appears in the tool's output or carries a limit naming why.
- **4 and 5:** a planted answer that omits the "no test-file pattern given" limit fails A5. The report shows A2 and A5 as "tool part MET, agent part NOT CHECKED → P6".
- **6:** at the 20-implementation site, a key written by another agent lists which tests use the real layer. `count` lists all of them, and the ones that swap in a fake carry `throughFake: true`. Also run `exclude`, and the number of key tests that vanish shows what it would cost. If almost none vanish, my pick is wrong and `exclude` is fine.
- **7:** for each of the three modules, a different agent reading the code names the sibling groups. They match the globs, and every row has file and lines.
- **8:** a plain grep for `test(` and `it(` calls in opencode finds no test file outside the globs, and no listed test sits in a non-test file.
