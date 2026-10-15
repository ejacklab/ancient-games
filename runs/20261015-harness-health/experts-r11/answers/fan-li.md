# 范蠡 (Fan Li) — Review of Eleven Harness Requirements

## Answer
If EJ intends the harness health check to prevent actual dispatch failures rather than audit passive configuration files, the requirements must be split between what the engine owns and what the workflow orchestrator owns, passive file checks must be replaced by active non-zero failure probes, and the R11 80% coverage rule must be judged at Step 2 (algorithm design) rather than forced prematurely at Step 1 (readiness). Checking configuration syntax without probing dynamic behavior mistakes a sprouting symptom for visible form and will continue to let exit-zero failures through to the field.

## How I decided

1. **Readiness is the examination of preparations, not the battle itself.** My #18: 「審備則可以戰乎？」王曰：「巧。」 (`quoted`) — "If the preparations are examined, can we then fight?" The king: "Skilful." Defensive preparations must be close-knit and examined before engagement. But inspecting passive configuration files does not establish that an engine will act when called. A health check that fails zero of seven historical dispatch defects has examined only the court records, not the army's equipment.

2. **A harness engine is not a workflow orchestrator; say who is better at what.** My #14: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 (`quoted`) — "Inside the four borders, the people's affairs: I am not as good as 種. Outside the four borders, dealing with enemy states, matters decided on the spot: 種 is not as good as I." The eleven requirements conflate the harness (the execution engine running inside its process) with the workflow orchestrator (the overarching design method, tracking state, retries, and judges). Forcing task planning, retry policies, and evaluator agents onto the harness misplaces duties across borders.

3. **Passive presence is merely a sprout; do not campaign on it.** My #9: 「逆節萌生。天地未形，而先為之征，其事是以不成，雜受其刑。王姑待之。」 (`quoted`) — "Rebellion against order is sprouting. Heaven and Earth have not yet taken visible form, and to campaign ahead of it — that is why the affair does not succeed, and all together suffer the harm. For now, wait." A line in a configuration file or an existing directory is only a sprout. Treating `reported` as `verified` without an active check that can fail brings shared harm. My #1: 「夫人事必將與天地相參，然後乃可以成功。」 (`quoted`) — "Human affairs must be joined with Heaven and Earth as a three; only then can success be achieved." A requirement passes readiness only when the local static claim is cross-checked with an active check.

4. **Verdict on R1 (Clear context delivery): Change (a question for EJ).**
   - *Reasoning:* My #2: 「天道盈而不溢，盛而不驕，勞而不矜其功。」 (`quoted`) — "Heaven's way is full but does not overflow, flourishes but is not arrogant, labours but does not boast of its work." Checking merely that `AGENTS.md` or `CLAUDE.md` exists checks only whether a storehouse has a door, not whether it overflows the context budget.
   - *Readiness checkability:* Can be checked at readiness without quota.
   - *Check that can fail:* Check file existence AND verify character/token count falls below an explicit threshold bound. Plant a file exceeding the budget or remove the file; the check must fail. Note: whether the engine actually ingests the file at dispatch remains an unverified sprout (my #9) until execution.

5. **Verdict on R2 (Well-designed tools): Split (a question for EJ).**
   - *Reasoning:* My #14 (boundaries of competence) and my #3: 「時不至，不可彊生；事不究，不可彊成。」 (`quoted`) — "When the time has not come, growth cannot be forced; when the matter has not run its course, completion cannot be forced."
   - *Readiness checkability:* Split into two parts: (a) Tool schema syntax, argument validation, and executable permissions can be checked at readiness with zero quota by running local schema linters and binary `--help` probes; fail if malformed or non-executable. (b) Tool error comprehension and recovery guidance cannot be checked at readiness without dispatching model calls, which spends quota and violates house rules; this belongs to runtime verification.

6. **Verdict on R3 (Planning and task structure): Change (a question for EJ).**
   - *Reasoning:* My #5: 「夫謀之廊廟，失之中原，其可乎？…贏縮轉化，後將悔之。天節固然，唯謀不遷。」 (`quoted`) — "To plan it in the temple hall and lose it on the central plain — can that be right? … Advance and retreat change into each other; later you would regret it. Heaven's rhythm is like that; only the plan does not move." Planning and done-criteria belong to the temple hall of workflow design, not the raw engine harness (my #14).
   - *Readiness checkability:* The harness engine cannot be checked at readiness for task adherence (historical failure #5 proved `agy` plan mode stopped at a plan despite configuration). Readiness can only check that the project repository provides a structured task ledger template and done-criteria parser; fail if the task specification parser is absent or fails on a malformed task file.

7. **Verdict on R4 (State and memory across sessions): Keep.**
   - *Reasoning:* My #3: 「田野開闢，府倉實，民眾殷。」 (`quoted`) — "Fields opened, storehouses full, people numerous." Physical storage and progress records are ground matters (節事者與地, my #2).
   - *Readiness checkability:* Can be checked at readiness without quota.
   - *Check that can fail:* An active probe must create, write, read, and delete a marker file in the designated progress/checkpoint path. Fail if write access is denied or isolation blocks heredoc writes (catching historical failure #7). A passive check that merely observes directory existence is rejected (my #9).

8. **Verdict on R5 (Independent verification): Split (a question for EJ).**
   - *Reasoning:* My #1: 「夫人事必將與天地相參，然後乃可以成功。」 (`quoted`) and my #12: 「必因天地之災，又觀其民之饑飽勞逸以參之。」 (`quoted`) — cross-checking multiple independent signals.
   - *Readiness checkability:* Split into two parts: (a) Mechanical verifiers (pytest, linters, structural checkers) must be checked at readiness by running them on planted invalid syntax or failing fixtures; fail if the tool exits 0 on bad input or is not installed. (b) Independent evaluator agents require dispatching model quota, which cannot be forced at readiness (#3) without spending paid tokens.

9. **Verdict on R6 (Guardrails and permissions): Change (a question for EJ).**
   - *Reasoning:* My #13: 「夫勇者，逆德也；兵者，凶器也；爭者，事之末也。」 (`quoted`) — "Courage goes against virtue; weapons are ill-omened instruments; contention is the last of affairs." Autonomous tools are ill-omened instruments; permissions must be tight. But current checks mark four engines `unknown` and observe unverified config flags on the rest.
   - *Readiness checkability:* At readiness, probe whether permission restrictions hold on non-model execution (e.g. attempting to touch a file outside repository bounds or execute a denied command); fail if the forbidden action succeeds without intercept. Where active probing is impossible, mark `unknown` and forbid running without human waiver. Treating unverified config as safe violates my #18.

10. **Verdict on R7 (Recovery and retries): Change (a question for EJ).**
    - *Reasoning:* My #10: 「臣聞古之善用兵者，贏縮以為常，四時以為紀，無過天極，究數而止。」 (`quoted`) — "Those of old who used troops well took advance and retreat as their constant and the four seasons as their rule; they did not pass Heaven's limit, and stopped when the count was exhausted." Step retries and rollback points belong to the workflow controller (my #14).
    - *Readiness checkability:* The harness does not execute rollback; the repo environment does. At readiness, verify that workspace rollback mechanics work: introduce a scratch file, run the workspace reset/clean command, and assert zero git diff. Fail if the rollback script leaves dirty files or git locks prevent recovery.

11. **Verdict on R8 (Human-in-the-loop gates): Keep.**
    - *Reasoning:* My #2: 「定傾者與人」 (`quoted`) — steadying the tilting goes with people; and my #8: 「肆與大夫觴飲，無忘國常。」 (`quoted`) — "drink freely with the officers, but do not forget the state's standing rules." When the system tilts or reaches dangerous boundaries, human judgment must not be bypassed.
    - *Readiness checkability:* Can be checked at readiness. Parse harness invocation wrappers and environment settings; fail if bypass mode or auto-approval flags are set on production workflows without explicit authorization.

12. **Verdict on R9 (Observability): Keep.**
    - *Reasoning:* My #3: 「以度天下…必有以知天地之恆制」 (`quoted`) — "take the measure of the world... know the constant measures of Heaven and Earth"; and my #10: 「究數而止」 (`quoted`) — "stopped when the count was exhausted."
    - *Readiness checkability:* Can be checked at readiness. In addition to verifying that the log folder exists, verify that the logging pipeline is writable and run the log-ingestion parser against a dummy transaction. Fail if log path is unwritable or the parser rejects standard log fields.

13. **Verdict on R10 (Feedback loop improving harness): Change (a question for EJ).**
    - *Reasoning:* My #16: 「計然之策七，越用其五而得意。既已施於國，吾欲用之家。」 (`quoted`) — "Ji Ran's policies were seven; Yue used five of them and got what it wanted. Since they have been applied to the state, I want to use them for the household." Proven fixes must become permanent rules. My #6: 「蜚鳥盡，良弓藏」 (`quoted`) — "When the flying birds are gone, the good bow is put away." Scaffolding built for temporary model weaknesses must be retired when conditions change.
    - *Readiness checkability:* An ongoing feedback loop cannot be observed operating at readiness. Check only that the permanent rule files (`CLAUDE.md`, `AGENTS.md`) and harness hooks exist and pass syntax checks; fail if hook scripts fail validation or exit non-zero on test invocation.

14. **Verdict on R11.1 & R11.2 (Prompt judge coverage and fast first signal): Keep, but resolve the timing conflict.**
    - *Reasoning:* My #7: 「未可也。蠡聞之，上帝不考，時反是守，彊索者不祥。…有奪，有予，有不予，王無蚤圖。夫吳，君王之吳也，王若蚤圖之，其事又將未可知也。」 (`quoted`) — "Not yet. I have heard: when the Lord on High has not completed it, keep watch for the time to turn; one who seeks by force is unlucky. … Do not plan early. Wu is Your Majesty's Wu; if you plan for it early, the matter will again be unknowable." Demanding that readiness (Step 1) count prompts that are only written in Step 2 is planning early (蚤圖). It forces what has not yet come (my #3: 時不至，不可彊生).
    - *Placement:* At readiness (Step 1), inspect the storehouse of available judges (my #3: 「府倉實」; my #18: 「審備」) — verify that test commands, linters, and rule checkers exist and can fail. Count the 80% coverage only at Step 2 (Algorithm/Design Gate) once prompts are drafted.
    - *On R11.2:* Keep as SHOULD. My #4: 「從時者，猶救火、追亡人也，蹶而趨之，唯恐弗及。」 (`quoted`) — follow the time like fighting fire. A fast check that fails immediately saves time and prevents committing to long verdicts. And my #9: an early signal can reject failure, while final acceptance still requires full corroboration.

15. **Answer to Q1 (Prompts vs Acceptance Criteria): Count over acceptance criteria (my reading).**
    - *Reasoning:* My #3: 「事不究，不可彊成。」 (`quoted`) — "when a matter has not run its course, completion cannot be forced." If a single prompt covers four acceptance criteria and only one is checked, the matter has not run its course. Counting by prompt allows an author to bundle three unverified risks under one trivial check, claiming 80% compliance while critical criteria remain exposed. My #18: preparations must be close-knit.

16. **Answer to Q2 (Design standards as judges): Only standards that return pass or fail count (my reading).**
    - *Reasoning:* My #9: 「逆節萌生。天地未形，而先為之征，其事是以不成，雜受其刑。」 (`quoted`). A design document sitting silently in `docs/` has taken no visible form in the world. House rules state that every check must be able to fail on planted bad input before it is trusted. A prose standard that cannot reject an output cannot be a judge.

17. **What the list misses: N1, N2, and N3.**
    - **N1 — Zero-Quota Dispatch Channel Probe (a proposal for EJ).**
      - *Rule:* My #18 (「審備則可以戰乎？」) and my #1 (「天時不作，弗為人客；人事不起，弗為之始」).
      - *Failure caught:* Catches hang on stdin without `/dev/null` (failure #1), SQLite lock contention on concurrent starts (failure #2), out-of-tree file rejection (failure #3), and transient authentication/login failures (failure #6). Readiness must run a dry non-model CLI command (e.g. `codex --version < /dev/null`) to prove the invocation pipeline functions.
    - **N2 — Empty-Output & Silent Exit-Zero Vacuum Trap (a proposal for EJ).**
      - *Rule:* My #9 (confusing sprouting exit-0 with visible success) and my #3 (completion cannot be forced).
      - *Failure caught:* Catches `agy` soft-denial returning exit 0 with empty stdout (failure #4), `agy` stopping at a plan without generating code (failure #5), and subagent heredoc write suppression (failure #7). Harness health must require that output streams have verified bytes and meet non-empty contract criteria.
    - **N3 — Domain Boundary Governance (a proposal for EJ).**
      - *Rule:* My #14 (「四封之內…四封之外…」).
      - *Failure caught:* Catches operational ambiguity where the harness is blamed for missing retry loops or task tracking that belong to the workflow orchestrator, leaving neither layer responsible for enforcing them.

## What I need to know

1. Does EJ allow zero-token CLI dry-run invocations (such as running `--version` with `< /dev/null`, or checking write permissions with a temporary scratch file) during the readiness step, or must readiness strictly inspect files without executing engine binaries? If binary execution is forbidden, N1 and active failure probing cannot be established at readiness.
2. In EJ's workflow designs, are acceptance criteria formally enumerated and parseable (e.g. in a YAML/Markdown ledger), or are they embedded as prose in prompts? If they are not parseable entities, calculating the 80% denominator over acceptance criteria will require an explicit extractor tool.
3. Does EJ intend the harness health check to grade raw CLI tools independently, or to grade an engine only when wrapped by `ancient_games` orchestration scripts?

## Costs and risks

1. **Active probing adds execution latency and environmental fragility.** Testing active failure probes at readiness requires running local commands, which risks transient failures if local process tables or file locks are busy (from my #18 「審備」: defensive inspection demands continuous maintenance).
2. **Postponing R11 coverage evaluation to Step 2 risks late design rejection.** Shifting the 80% check from readiness to the design gate means a workflow may be designed before discovering that available judges cover only 60% of its criteria (from my #7 「無蚤圖」: refusing to plan early requires the patience to absorb late adjustments when conditions mature).
3. **Restricting judges to binary pass/fail disqualifies subjective guidance.** Barring passive design standards from counting toward the 80% threshold increases the burden on authors to write concrete evaluation scripts or rubrics before sending prompts (from my #3: removing harms and establishing constant measures requires upfront labor before profit is realized).
4. **Separating engine duties from workflow duties leaves standalone CLI invocations unshielded.** If an engine is run directly without Ancient Games wrappers, workflow-level safeguards (R3, R7) will not be present (from my #14: dividing tasks inside and outside borders means neither specialist can govern the other's domain).

## How we would know I was right

1. **Historical defect backtest:** Run the revised readiness and dispatch probe against synthetic reproductions of the seven historical harness failures. The revised check must detect and block at least five of the seven failures before task dispatch (raising the score from 0/7 to at least 5/7).
2. **Planted failure verification:** Plant an unparseable schema in R2, a read-only directory in R4, and a planted syntax error in R5; the readiness check must reliably exit with failure on all three.
3. **Coverage measurement trial:** On a test workflow design, calculate R11 coverage by prompts versus by acceptance criteria. If a prompt bundling multiple unchecked criteria passes under prompt-counting but fails under criteria-counting, the criteria-based rule is verified as preventing unmonitored risk.
