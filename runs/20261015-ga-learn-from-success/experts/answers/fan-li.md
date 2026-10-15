# 范蠡 (Fan Li) — learn from the mistakes inside a success, not from total failure

## Answer
*My reading, conditional:* the principle holds for the **path**. The most useful mistakes, and the ones most often missed, are the ones inside runs that ended well. It breaks for **readiness**. A total failure still teaches whether the conditions were ready, and when a prediction was written down before the run, it also tests that prediction. So I would keep R12.2/R12.3 for total failures and tell them to ask a different first question. I would make the mistakes inside a success explicit in both rules. The proposed text is below; EJ decides.

## How I decided

**(a) Verdict: where it holds and where it breaks**

1. **Holds: a success can hide a mistake.** My #2 says keeping the full goes with Heaven: 「天道盈而不溢，盛而不驕，勞而不矜其功。」 (*quoted*). It is full but does not overflow, and does not boast of its work. A great success is exactly the moment to look for what nearly spilled.
   - **Case from today** (the brief's facts): a fake engine returned nothing, and the agent got around it by calling the real engine binary. As R12.7 stands, that run can be logged as `ok` and even become a parent. The house rule "no paid engine call without EJ's go-ahead" may have been broken inside a success. *Not measured:* whether that call was paid.
   - **Outside evidence:** Dillon & Tinsley found that near-misses are judged as successes (see (c)).
2. **Holds: total failure gives a flat signal about the path.** My #12: engage only on a disaster cross-checked against a second sign, 「又觀其民之饑飽勞逸以參之」 (*quoted*). A signal is read *against* something. A run where every attempt failed has no sibling success to read it against, so it cannot say which step of the path was wrong. This matches the researcher's F1, F4 and F9, and Michalski's HIGH/LOW contrast in (c).
3. **Breaks: total failure after a written prediction.** My #13: Fan Li warned the king not to attack first. The king attacked and was defeated (*attributed*, narration, 國語21:5). After the defeat Fan Li repeated the rule (「君王其忘之乎？持盈者與天…」, from the source note of my #2, 國語21:7). The total failure was informative because the prediction existed before it.
   - **Harness case:** R12.7 already makes a child write its measure and its parent's value before the run. If that child fails completely, the failure tests the written prediction, and it should be read.
   - **Outside evidence:** Madsen & Desai report that launch organizations learned more from failures than from successes (see (c)).
4. **Breaks: total failure from the environment teaches readiness, not path.** My #18: 「審備則可以戰乎？」 (*quoted*), meaning "with the preparations examined, can we fight?" My #3: 「時不至，不可彊生；事不究，不可彊成。」 (*quoted*), meaning growth cannot be forced before its time, nor completion before the matter has run its course.
   - **Case:** the fake engine returning nothing was a failure of the preparations (Heaven's time), not of the method (human affairs). Running six whys on the path would change the wrong thing. The lesson is about preparation: check the engine answers before the run.
5. **Breaks: a success can stop being one when conditions change.** My #6: 「久受尊名，不祥。」 (*quoted*), "to hold an honoured name long is unlucky." My #1: success needs human affairs joined with Heaven's time.
   - **Case:** a parent path that won on claude-haiku with one engine set may mislead once the engines or models change. This is the researcher's deception finding (F28, F31) in Fan Li's terms.
6. **Do not change a rule on one result.** My #5: 「夫十年謀之，一朝而棄之，其可乎？」 (*quoted*), "ten years of planning thrown away in one morning, can that be right?" Today's data is n=3 per arm, on one task and one model. This keeps my proposals to labelling and recording, not to new gates. It also means a child's 2% gain from a single run should be labelled n=1, not read as selection.
7. **Borrow, not copy, has a precedent.** My #16: 「計然之策七，越用其五而得意。」 (*quoted*), "Ji Ran's policies were seven; Yue used five and got what it wanted." He moved a method from the state to the household and said how much of it he used. This supports R12.7's "borrows, does not copy" as written; I add nothing here.

**(b) Proposed changes (each check written by me, not yet run; a passing check would not show the rule is right)**

8. **R12.2: add the near-miss** (my #2, step 1). Proposed text:
   > "A failure inside a task that ended in success is still logged as a failure, and its record says the task ended in success. A step that reached its result by a route the brief did not name — an engine or tool the brief did not list, a skipped or bypassed check — is logged as a failure even when its result passes."
   - **Check that can fail:** plant a run where the named engine returns nothing and the agent calls another binary. The check fails if the log holds only an `ok` line and no failure record for the substitute call.
9. **R12.3: read a failure against a success; for a total failure, ask about readiness first** (my #12, #18, #13). Proposed text:
   > "For each failure, the insight names the closest success to compare it with — a retry that passed, the parent path, or a sibling run of the same task — and the first step where the two differ; the six whys start from that step. When no success exists to compare (every attempt failed), the insight says so; its first why asks whether the conditions were ready (engine, tool, input, environment), and, if a prediction was written before the run, states how the result differed from it."
   - **Check that can fail:** plant a failure followed by a passing retry. The check fails if the insight does not name the retry and the differing step. A second plant: an insight that names no comparison and does not say "none exists" fails.
10. **R12.7: a great success lists its own mistakes, and a parent records its conditions** (my #2, #6, #1). Proposed text, added after the great-success sentence:
    > "The great-success insight lists every failure record from its own run (R12.2) and, for each, whether the design (a check, a retry, a step) or chance kept it from spoiling the result. A path records the conditions it ran under — engines, models, tools; a design that borrows a parent whose conditions have changed says which changed."
    - **Check that can fail:** give a great-success insight for a run that has at least one failure record. It fails if it lists none of them. Separately, a design that borrows a parent whose recorded model differs from the one now in use fails if it does not name the change.
11. **R12.7: label the run count** (my #5). Proposed text, added to the report sentence:
    > "…reported after the run, with the number of runs behind the child's value and behind the parent's."
    - **Check that can fail:** a report that claims a child is better without both run counts fails.

**(c) What my research added** (all fetched 2026-10-15)

12. **Near-misses are read as successes.** Dillon & Tinsley, "How Near-Misses Influence Decision Making Under Risk: A Missed Opportunity for Learning", *Management Science* 54(8):1425–1440 (2008). The abstract says "organizations and managers fail to learn from near-misses because they evaluate such events as successes", and that near-miss information led people to choose riskier options.
    - Label: *verified* from the abstract page (https://ideas.repec.org/a/inm/ormnsc/v54y2008i8p1425-1440.html). The experiments themselves were not inspected, so the findings are *reported*.
    - This is the strongest support for EJ's principle in the form "the mistake in a success is what gets missed", and it backs step 8.
13. **Counter-evidence: organizations learned more from failure.** Madsen & Desai, "Failing to Learn? The Effects of Failure and Success on Organizational Learning in the Global Orbital Launch Vehicle Industry", *Academy of Management Journal* 53(3):451–476 (2010). The press release says "organizations not only learned more from failure than success, they retained that knowledge longer". Desai advises analysing small failures and near misses.
    - Label: *reported*, from the university press release only (https://news.ucdenver.edu/failurebestteacher/). The abstract page (academicnewsletter.sufe.edu.cn/info/361534) failed to parse, and the paper was not read.
    - Their motivating case is that NASA reviewed the Atlantis foam loss (a success) far less than the Columbia loss (*reported*). That is the near-miss and the total failure in one story.
14. **Reviewing both beats reviewing failures only.** Ellis & Davidi, "After-event reviews: drawing lessons from successful and failed experience", *J. Appl. Psychol.* 90(5):857–871 (2005). Soldiers debriefed on both successes and failures improved more than soldiers who reviewed failures only.
    - Label: *reported*, through a secondary article (https://www.jems.com/ems-operations/flight-ambulance-operations/failure-is-not-an-option-but-success-is/) and a search summary. PubMed returned a cookie wall, and the PDF (https://cebma.org/assets/Uploads/Ellis-2005.pdf) could not be rendered: no pdftoppm or pypdf here.
    - This supports R12.7 existing at all. It does not support dropping total-failure review.
15. **Closes a gap the researcher left open (F49):** Michalski's LEM does use the low group, but only as a contrast. The patent says to "Split the current population of individuals (solutions) into three groups: HIGH (high-performance), LOW (low-performance), and MEDIUM", and that "the description distinguishes the high quality group from the lesser quality groups."
    - Label: *verified* from US6523016B1, "Learnable non-darwinian evolution", R. S. Michalski, granted 2003-02-18 (https://patents.google.com/patent/US6523016). This is the patent, not the 2000 *Machine Learning* paper.
    - It backs step 9: a failure is read against a success.
16. **Not verified:** any source using EJ's exact phrase. I did not search for it again; the researcher's search found none.

## What I need to know
- **Was the real-engine call today a paid call, and was it allowed?** If it was paid and not allowed, the near-miss rule in step 8 guards a safety bound, and MUST fits even under the house rule. If not, it is method, and SHOULD would fit; EJ has chosen MUST either way.
- **How often does a harness task end with every attempt failing?** If rarely, the total-failure branch of step 9 costs little and matters little. If often, it is the main branch.
- **Which GA lesson EJ learned:** elitism, (1+1), or shaped fitness. If it was shaped or partial fitness (Hinton & Nowlan, F1–F2), the closer harness change is giving checks partial credit, which none of my proposals do.
- **Is any path ever re-run?** If not, every parent value is n=1, and step 11's label will say n=1 on every report.

## Costs and risks
- **More failure records** (step 8, from my #2): bypasses and in-success failures add records and longer end-of-task insights, and EJ has more to read. A broad "route the brief did not name" may also flag harmless improvisation.
- **Forced comparisons** (step 9, from my #12): an agent may name a weak "closest success" just to pass the check. The check sees that a name is present, not that the comparison is apt.
- **Under-reading total failures** (step 9, from my #18 and #13): putting readiness first could push a real path error onto "the environment". Madsen & Desai's result is the warning (*reported*).
- **Field creep** (step 10, from my #6 and #1): recording conditions adds fields to every path, and a mismatch on any of them may stop useful borrowing.
- **My own basis is thin** (from my #5): steps 1 and 4 rest on one n=1 event, the fake engine and the bypass. All the checks above are written by me and none has been run. They would show the rule is followed, not that it improves results.

## How we would know I was right
- **Planted tests first:** each check in steps 8–11 is shown failing on its planted wrong input before it is trusted. If a plant passes, the check is wrong.
- **Then compare over the next runs** (no threshold set; it is a comparison, not a gate):
  - Fixes from insights with a named comparison success vs fixes from total-failure insights. Measure how often each fix catches its planted repeat, and how often the same failure comes back in later runs.
  - Children whose parent's great-success insight listed its in-run failures vs children whose parent's did not. Measure how often each child repeats a recorded failure.
- **Reading the result:** if the first kind does no better in both comparisons, the principle as I applied it is not supported for this harness.
- **Today's case alone:** if a re-run of today's task, with step 8 in place, logs the substitute engine call as a failure, the near-miss gap is closed for that case.
