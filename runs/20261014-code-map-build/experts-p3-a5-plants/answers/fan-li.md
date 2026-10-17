# 范蠡 (Fan Li) — Whether the planted faults justify closing round A5

## Answer
Closing round A5 now is not justified: four of the five planted faults escaped round A5's own evaluator checks, showing that the round's defense is hollow and incomplete. The checks must be strengthened before round A5 can close.

- `limits-dropped`: not enough; caught only by earlier requirements (R2, A1, A2, A3, L1) and frozen tests while A5 marked MET because `A5-specific-answer` tests only `where leaf` which expects empty limits, completely missing an answer returned without its limits.
- `where-inside-dump`: enough; caught under A5 because exact array equality on `matches` rejected the full program dump on `where leaf`.
- `site-dropped`: not enough; caught under earlier requirements (R2, A1, A2, L1), but A5 marked MET because A5 has no test verifying link call-site locations on specific queries, missing an answer returned without its evidence.
- `callers-unasked-map`: not enough; caught under A1 and A2, but A5 marked MET because no A5 check asserts that specific queries (`callers`, `callees`, `chain`) omit the module map, missing a whole map produced unasked.
- `not-found-limit-dropped`: not enough; caught only under L1, while A5 marked MET because A5 does not verify that an empty or missing specific answer carries its required limit.

**STRENGTHEN**:
- Tied to A5's Fails-if line ("without its evidence or limits"): add evaluator cases for specific queries (`callees`, `callers`, `chain`) asserting that missing link `site` locations or missing required `limits` (such as depth or test-pattern limits) fail requirement A5 directly.
- Tied to A5's Fails-if line ("or a whole map is produced unasked"): add evaluator cases asserting that specific queries (`callers`, `callees`, `chain`, `tests`) fail requirement A5 directly if `map` or program-wide definition dumps are attached.

## How I decided
1. Examine the preparations (my #18: 「審備則可以戰乎？」王曰：「巧。」, `quoted`). 韋昭 glosses this as defensive preparations so close-knit that they cannot be broken into (備，守禦之備; 巧，審密不可攻入也). Reviewing the COO's evidence (`p3-a5-src-plants.txt`), four of the five planted faults were marked MET under A5 itself; they were tripped only by tests written for earlier rounds (R2, A1, A2, A3, L1) or the frozen test suite. A defensive line where four out of five planted breaches penetrate the specific gate unflagged is not close-knit (*my reading*).
2. The plan agreed in the council chamber must not be lost on the battlefield (my #5: 「夫謀之廊廟，失之中原，其可乎？王姑勿許也。…贏縮轉化，後將悔之。天節固然，唯謀不遷。」, `quoted`). In the chamber (`runs/20261014-code-map-vision-relay/result-trimmed.md`), EJ and the team fixed A5's rule: it fails if "an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked." In the field (`code_map/eval/cases/fixtures.json`), Codex wrote only two fixture cases (`A5-specific-answer` and `A5-default-text`), both probing `where leaf`. Three of the four failure conditions from the chamber (missing evidence, missing limits, unasked whole map) are completely unverified by A5's own checks. Accepting round completion while three-quarters of the requirement's contract is absent from the check abandons the plan (*my reading*).
3. When the time has not come, growth cannot be forced; when the matter has not run its course, completion cannot be forced (my #3: 「時不至，不可彊生；事不究，不可彊成。自若以處，以度天下，待其來者而正之，因時之所宜而定之。」, `quoted`). Round A5 has not run its course (事不究). Closing the round now because earlier rounds caught the COO's faults is forcing completion (不可彊成). The COO's plants revealed the opening and the blind spots (事將有閒); the rule is to take the measure of what came and set it right (待其來者而正之), settling the checks as the situation demands (*my reading*).
4. Do not plan early, and do not seek by force (my #7: 「未可也。蠡聞之，上帝不考，時反是守，彊索者不祥。…王若蚤圖之，其事又將未可知也。」, `quoted`). The COO noted: "What this does not establish: the plants are the COO's and share the COO's blind spots." If round A5 is closed early while its own evaluator cases test only `where leaf`, any future builder fault specific to A5 that does not collide with R2 or A1 will slip through undetected, making the true reliability of the code unknowable again (其事又將未可知也) (*my reading*).
5. Wait until human affairs and external verification join together (my #1: 「人事至矣，天應未也，王姑待之。」 / 「天應至矣，人事未盡也，王姑待之。」…「夫人事必將與天地相參，然後乃可以成功。」, `quoted`). The builder's implementation (attempt 1) is ready, but the external verification checks for A5 are incomplete (人事未盡, 天應未也). When one is present and the other is not, the rule is clear: wait (王姑待之) (*my reading*).
6. Having obtained the opening, finish the work without slackening (my #4: 「得時無怠，時不再來，天予不取，反為之災。」 / 「得時不成，天有還形。天節不遠，五年復反，小凶則近，大凶則遠。」, `quoted`). The COO's probe exposed the exact gap in the evaluator. Failing to complete the checks now leaves a latent defect that will turn back as a failure later when downstream agents or users rely on unasked dumps or missing limits (*my reading*).

## What I need to know
- If EJ's operating rule is that any round passes whenever the overall test suite exits 0 and earlier rounds catch the fault (treating requirement attribution as secondary), then round A5 could be closed administratively on the condition that A5's coverage gap is recorded in the ledger; if each round's gate requires that the round's own requirement check independently catches failures of its own contract, then round A5 cannot close until strengthened (*my reading*).
- Whether the 8 private opencode core cases were designed to exercise A5 queries. Currently, the core set baseline already had A1 and A2 NOT MET, and only `site-dropped` was distinguishable from baseline; if private cases for A5 exist, their specific reports would show whether real repository code catches what fixture cases missed (*my reading*).

## Costs and risks
- Delaying the round closure and expending work to write evaluator test cases for specific commands costs immediate velocity in the build pipeline (from my #3: staying as you are, caring for the work, and waiting: 「自若以處…撫民保教以須之」).
- Risk of over-checking or creating brittle fixtures that overstep necessary limits (from my #10: 「無過天極，究數而止」).
- Risk of inaction: if the opening is not seized and the checks are not finished now, calamity returns later when real modules encounter unhandled unasked dumps or missing limits (from my #4: 「得時不成，天有還形…天予不取，反為之災」).

## How we would know I was right
- When new evaluator cases are added for specific command limits, call sites, and unasked map omission, re-running the evaluator on the four escaping plants (`limits-dropped`, `site-dropped`, `callers-unasked-map`, `not-found-limit-dropped`) will cause requirement **A5** itself to be reported as **NOT MET** directly.
- Attempt 1 clean source continues to evaluate as MET on all bundled, held-out, and valid private cases.
