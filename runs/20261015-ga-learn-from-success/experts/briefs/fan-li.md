# Brief — 范蠡 (Fan Li) answers one question

You are **范蠡 (Fan Li)**, one of the experts EJ consults. You were built from a numbered list of 范蠡 (Fan Li)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261015-ga-learn-from-success/experts/seats/fan-li-list.md` — the "## Final list" section; items are numbered 1–18.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261015-ga-learn-from-success/experts/seats/fan-li-identity.md` — the "## Who they are" section.

## The question

EJ (the project owner) remembers a principle from studying genetic algorithms, and asks what you think of it for an AI-agent harness. You may do your own research (web search where your tools allow it); cite every source you use and mark what you could not verify.

EJ's words (quoted, 2026-10-15): "actually last time I learn a Genetic algorith, you can research about this, I remember a special part, is we learn about mistake in a success but not from total failure."

Each of you: answer through your own rules. Give (a) your verdict on the principle as it would apply to this harness — where it holds and where it breaks, each with a concrete case; (b) what it should change in the two rules below (R12.2–R12.3 on failures, R12.7 on success), written as proposed text, each change with a check that can fail; (c) what your own research added, with sources. Do not decide for EJ.

## Facts

**The harness.** AI engines (Claude, Codex, Gemini via agy, DeepSeek via dsh, MiniMax via opencode) do the work; a workflow-design method designs how; a TypeScript guard (hooks) logs every failure and, since today, every success; at the end of a session it asks for an insight for each failure (six whys to a changeable source, 2–3 fix options) and, after a success, for the task's **path** (steps, engines, checks, decisions, measures). For a similar task the next run borrows a recorded path as its **parent**, changes at least one thing, and tries to be 2% better on a measure named before the run — an aim that is reported, never a gate; a child that improves without repeating its parent's recorded failures becomes a parent.

**What happened today (measured, n=3 per arm, one task, claude-haiku):** agents with written rules followed them; hooks alone taught the same behaviour; agents made few mistakes of their own (a failing test while coding, an errored command, one sed that edited the wrong file); one agent, after a fake engine returned nothing, worked around it by calling the real engine binary.

**The current rules (draft):**

**R12.2 Failure log (MUST).** A failure is anything that went wrong while the work was done, whoever caused it: a
check that returned fail (a test run, a linter, a gate), a tool call that errored, an engine result that fails R12.1,
work that had to be undone or redone, and a correction from the project owner. Every failure is logged when it happens,
as one record: what was checked, the input,
the expected and the actual result, the engine and harness that produced it, the reason it is a failure, and the path
to the evidence (the data) in the run folder. Anyone may declare a failure — an evaluator, a retry, the project owner
or another agent — but a record without a reason and evidence is not accepted. A failure is logged even when a retry
later passes.

**R12.3 Insight at the end of a task (MUST).** When a task ends with one or more failure records, the agent that ran
the task writes an insight file in the run folder and raises it to the project owner in its final report. For each
failure, or each group with one cause: six whys down to a source that can be changed (an instruction, a check, a tool,
a config), the root cause, and two or three fix options — each a rule, a check or a tool — that the agent has
researched, ranked by expected effect, with the evidence for each. The agent proposes; it does not apply a fix without
the project owner's choice. A fix that is a check is shown failing on a planted repeat of the failure before it is
trusted. A fix to a harness's config is advice to the project owner; the agent never edits it.


**R12.7 Learn from success (MUST; proposed).** A failure matters more than a success, but a great success matters too.
Every checked result is recorded — a success as one line (the time, the session, what was checked, the engine or
runner, `ok`), a failure as its full record (R12.2) — so a check's failures can be read against how often it ran. When
a task succeeds, the agent records its **path**: the category and objective, the steps in order with the engine, model
and check of each, the decisions that mattered and why, and the measures of the result (time, failures, retries,
checks passed). A **great success** — one that beats the comparison it was measured against (its prediction, the
previous run of the same work, a first pass where the check failed before, or the project owner calls it great) — also
gets an insight in the same file as the failure insights: the cause that made it work, and one to three options to
make it repeatable, each with evidence. For a similar task — the agent proposes the match by category and objective,
and the project owner may overrule — the design **borrows that path, does not copy it**: it starts from the path as its
parent, changes at least one thing (a step, its order, an engine, a check, a brief), and writes before the run what it
changed, the measure it aims to improve and the parent's value on it. Every child tries to avoid the failures recorded
in its parent's insights and to be 2% better than its parent — an aim to keep trying for, reported after the run, never a
reason to block or discard the work. A child that improves on its parent's value without repeating those failures
becomes a parent for the next similar task; every path stays recorded, so the paths grow like a population and are
selected by results.

Fails if: a check's successes are not recorded; a successful task leaves no path, or a path lacks its steps, engines,
checks or measures; a great success has no insight, names no comparison or evidence, or its insight gives no cause or
nothing to repeat; a design for a similar task neither names a parent path nor says why none applies; a design copies
its parent unchanged; the change, the measure or the parent's value is not written before the run; a child that repeats
a recorded failure is counted as better; the report does not say how far the child got against the 2% aim; a child's
result overwrites its parent's path.


**A researcher's findings on the principle** (written today by a Claude researcher subagent; 50 findings, 23 verified from source, 22 reported, 5 unproven; it found no source using EJ's exact phrase):

# Findings — GA: learn from the imperfections of successes, not from total failures
Produced 2026-10-15 by researcher (Claude Opus 5.5, claude-opus-5-5). Question asked (from the brief, verbatim): "In genetic / evolutionary algorithms (and closely related fields such as evolution strategies, RL credit assignment, curriculum learning), what is the principle that improvement comes from the imperfections inside successful (fit) individuals rather than from total failures? Find the established concepts and their sources ... Also find the strongest counter-evidence: cases where learning from total failures does help."

**Labels.** The brief asked for "verified-from-source or from memory". This file uses the repo's four tags
(`docs/RESEARCH_TAGS.md`) instead, and **no row comes from memory**: every row cites a page that was fetched and
read in this session. Departure, stated as the tags file asks: where only a paper's abstract (or a summary of its
results text) was read and its tables/figures were not inspected, the empirical claim is tagged `reported` — the
abstract is treated as an account whose locator is the paper itself. A paper's own definition of its own method
is tagged `verified` (the wording is the evidence for the definition).

Quotes are verbatim fragments; the fetch tool returns quotes in fragments under ~125 characters, so long sentences
appear as consecutive fragments joined by " / ".

## A. Total failure gives no signal (flat landscape, all-zero groups)

| id | Finding | Label | Source |
|---|---|---|---|
| F1 | Hinton & Nowlan argue that when fitness is given only for the exactly-right configuration, evolution has no path and degenerates to random trial; they name this the needle in a haystack. | verified | https://www.cs.toronto.edu/~hinton/absps/evolution.htm (1987, year only; Complex Systems 1:495–502), quoted: "In this worst case, there is no reasonable evolutionary path toward the good net and a pure evolutionary" / "search can only discover which of the potential connections should be present by trying possibilities at random." / "The good net is like a needle in a haystack." |
| F2 | Hinton & Nowlan's remedy is a zone of raised fitness around the target (partial credit): the search only needs to be told it is getting closer. | verified | same page (1987, year only), quoted: "This has the effect of constructing a large zone of increased fitness around the good net." / "It is like searching for a needle in a haystack when someone tells you when you are getting close." / "The central point of the argument is that the person who tells you that you are getting close does not" / "need to tell you anything more." |
| F3 | GAs cannot effectively solve problems whose only fitness measure is binary pass/fail; random search may be as quick. | unproven | https://en.wikipedia.org/wiki/Genetic_algorithm (last edited 2026-10-04), quoted: "GAs cannot effectively solve problems in which the only fitness measure is a binary pass/fail outcome" / "(like decision problems), as there is no way to converge on the solution (no hill to climb)." / "In these cases, a random search may find a solution as quickly as a GA." — the sentence is marked [citation needed]; no reference attached. |
| F4 | In GRPO-style RL for LLMs, a group whose answers all have the same outcome gets zero advantage and so zero gradient; DAPO filters out prompts with accuracy 1 and 0 (all-correct and all-wrong). | verified | https://arxiv.org/html/2503.14476 (2025-03-17), Yu et al., "DAPO: An Open-Source LLM Reinforcement Learning System at Scale", quoted: "the resulting advantage for this group is zero." / "A zero advantage results in zero policy gradients." / "propose to over-sample and filter out prompts with the accuracy equal to 1 and 0." |
| F5 | SGPO's authors state GRPO cannot update when every response in a group is wrong, and that it discards those failure signals. | verified | https://arxiv.org/abs/2505.11595 (v1 2025-05-16; v5 2026-03-10), Chen, Li, Li, Chen, Lin, "Stepwise Guided Policy Optimization: Coloring your Incorrect Reasoning in GRPO", quoted: "but it fails to update the policy when all responses within a group are incorrect" / "unlike humans, who can learn from mistakes, GRPO discards these failure signals." |
| F6 | NGRPO's authors state the zero-advantage problem arises when a group is entirely correct or entirely incorrect, and fix the all-wrong case with a virtual maximum-reward sample. | verified | https://arxiv.org/abs/2509.18851 (2025-09-23), Nan et al., "NGRPO: Negative-enhanced Group Relative Policy Optimization", quoted: "when all responses within a group are either entirely correct or entirely incorrect" / "hypothesizes the existence of a virtual maximum-reward sample" |
| F7 | Li, Pinto & Abbeel state that low-reward data provides little to no signal for the task it was collected on, but argue it is likely rich for other tasks. | verified | https://arxiv.org/abs/2002.11708 (2020-02-26), "Generalized Hindsight for Reinforcement Learning", quoted: "low-reward data collected while trying to solve one task provides little to no" / "signal for solving that particular task and is hence effectively wasted." / "However, we argue that this data, which is uninformative for one task, is likely a rich source of information" / "for other tasks." |
| F8 | Florensa et al. train only on "Goals of Intermediate Difficulty": goals the current policy reaches with probability between Rmin=0.1 and Rmax=0.9; too-hard goals waste samples and too-easy ones repeat mastered goals. | verified | https://ar5iv.labs.arxiv.org/html/1705.06366 (2017-05, month only, from the arXiv id; ICML 2018), "Automatic Goal Generation for Reinforcement Learning Agents", quoted: "too many samples are wasted attempting to train on goals that are infeasible or not reachable by the current policy" / "we might sample repeatedly from a small set of already mastered goals." / "In all our experiments we use 0.1 and 0.9 respectively." |
| F9 | The STaR loop, trained only on its own successful rationales, gets no direct signal from the problems it fails. | verified | https://ar5iv.labs.arxiv.org/html/2203.14465 (2022-03-28), Zelikman, Wu, Mu, Goodman, "STaR: Bootstrapping Reasoning With Reasoning", quoted: "it receives no direct training signal for problems it fails to solve." |

## B. Selection: the next generation is bred from the fitter, with the best kept

| id | Finding | Label | Source |
|---|---|---|---|
| F10 | In a GA, fitter solutions are typically more likely to be selected as parents. | reported | https://en.wikipedia.org/wiki/Genetic_algorithm (last edited 2026-10-04), quoted: "fitter solutions (as measured by a fitness function) are typically more likely to be selected." — the article's references were not inspected. |
| F11 | Higher selection pressure makes the population converge faster but risks under-exploring the search space; too low and it may not converge. | reported | https://en.wikipedia.org/wiki/Selection_(evolutionary_algorithm) (last edited 2026-09-28), quoted: "The higher the selection pressure, the faster a population converges against a certain solution" / "the search space may not be explored sufficiently." / "If the pressure is too low, it must be expected that the population will not converge." — the article lists Bäck (1994) "Selective pressure in evolutionary algorithms"; not inspected. |
| F12 | Rank selection uses the fitness rank, not the raw fitness, and gives worse individuals a chance to reproduce. | reported | same page (2026-09-28), quoted: "The probability for selection does not depend directly on the fitness, but on the fitness rank." / "it also gives worse individuals a chance to reproduce and thus to improve." — lists Baker (1985) and Whitley (1989); not inspected. |
| F13 | Truncation selection keeps a top portion (10% to 50%); elitist selection carries a small portion of the best over unchanged. | reported | same page (2026-09-28), quoted: "A portion (10% to 50%) of the top individuals is selected for next generation." / "A small portion of the best individuals from the last generation is carried over" |
| F14 | Fitness-proportionate (roulette) selection gives weaker solutions some chance to survive. | unproven | https://en.wikipedia.org/wiki/Fitness_proportionate_selection (last edited 2026-01-22), quoted: "With fitness proportionate selection there is a chance some weaker solutions may survive the selection process." — references not checked for this sentence. |
| F15 | A larger tournament gives weak individuals a smaller chance of selection. | unproven | https://en.wikipedia.org/wiki/Tournament_selection (last edited 2026-08-28), quoted: "if the tournament size is larger, weak individuals have a smaller chance to be selected." — references not checked. |
| F16 | Evolution strategies: (μ,λ) takes the μ best offspring; (μ+λ) takes the best from parents and offspring together. | reported | https://en.wikipedia.org/wiki/Evolution_strategy (last edited 2026-09-30), quoted: "The μ best offspring are used for the next generation" / "The best are selected from a union of μ parents and λ offspring." |
| F17 | The (1+1)-ES keeps one parent, mutates it into one offspring, and replaces the parent only by an offspring at least as good — elitist, so the best-so-far is never lost. | verified | https://ar5iv.labs.arxiv.org/html/1706.02887 (v1 2017-06-09; v3 2020-11-19), Glasmachers, "Global Convergence of the (1+1) Evolution Strategy", quoted: "Its state consists of a single parent individual" / "and applies (1+1)-selection, i.e., it keeps the better of the two points." / "The parent is replaced by successful offspring, meaning that the offspring must perform at least as good as the parent." / "it performs elitist selection, ensuring that the best-so-far solution is never lost" |
| F18 | CMA-ES's standard update is truncation selection of μ out of λ offspring. | verified | https://ar5iv.labs.arxiv.org/html/1604.00772 (v1 2016-04-04; v2 2023-03-10), Hansen, "The CMA Evolution Strategy: A Tutorial", quoted: "Equation (6) implements truncation selection by choosing μ<λ out of λ offspring points." |

## C. The 1/5th success rule — the success rate steers how big the change is

| id | Finding | Label | Source |
|---|---|---|---|
| F19 | Success-based step-size control keeps the share of successful offspring stable, usually at 1/5, after Rechenberg; the step size is changed by one constant after success and another after failure, and an unsuccessful step reduces it. | verified | https://ar5iv.labs.arxiv.org/html/1706.02887 (v1 2017-06-09), Glasmachers, quoted: "The goal of success-based step size adaptation is to maintain a stable distribution of the success rate," / "The mechanism maintains a fixed success rate usually chosen as 1/5, in accordance with Rechenberg's original approach." / "in case of failure and success, respectively." / "results in a reduction of the step size by the factor" |
| F20 | With the constants set so c₊ + 4·c₋ = 0, the rule is Rechenberg's 1/5 rule (one success in five leaves the step size unchanged). | verified | same paper (2017-06-09), quoted: "For c_+ + 4·c_- = 0 we obtain an implementation of Rechenberg's classic 1/5-rule." (the fetch rendered the math as plain text) |
| F21 | The 1/5 rule is mostly superseded as a control mechanism, though its idea is still valued. | unproven | https://pypop.readthedocs.io/en/latest/es/res.html (undated; no date on the page), quoted: "As a control mechanism in practice, the 1/5th success rule has been mostly superseded by more sophisticated methods." / "its conceptual insight remains remarkably valuable." |

## D. Learning from one's own past successes (RL and LLM self-training)

| id | Finding | Label | Source |
|---|---|---|---|
| F22 | Self-Imitation Learning trains the agent to reproduce its own past good decisions, on the hypothesis that exploiting good past experience drives deep exploration. | verified | https://arxiv.org/abs/1806.05635 (2018-06-14), Oh, Guo, Singh, Lee, "Self-Imitation Learning", quoted: "a simple off-policy actor-critic algorithm that learns to" / "reproduce the agent's past good decisions." / "that exploiting past good experiences can indirectly drive deep exploration." |
| F23 | SIL significantly improves A2C on several hard-exploration Atari games. | reported | same (2018-06-14), quoted: "show that SIL significantly improves advantage actor-critic (A2C) on several hard exploration Atari games" — abstract only; tables not inspected. |
| F24 | Go-Explore's principles: remember visited states, first return to a promising state without exploring, then explore from it. | verified | https://arxiv.org/abs/1901.10995 (v1 2019-01-30; v4 2021-02-26), Ecoffet, Huizinga, Lehman, Stanley, Clune, "Go-Explore: a New Approach for Hard-Exploration Problems", quoted: "(1) remember previously visited states, (2) first return" / "to a promising state (without exploration), then explore from it," |
| F25 | Go-Explore's authors name two failure causes of exploration: forgetting how to reach visited states (detachment) and exploring before returning (derailment). | verified | https://arxiv.org/abs/2004.12919 (v1 2020-04-27; v6 2021-09-16), Ecoffet et al., "First return, then explore", quoted: "algorithms forgetting how to reach previously visited states ("detachment")" / "failing to first return to a state before exploring from it ("derailment")." |
| F26 | STaR fine-tunes only on rationales that ultimately yielded correct answers; for wrong answers it retries with the correct answer given (rationalization). | verified | https://arxiv.org/abs/2203.14465 (2022-03-28), quoted: "if the generated answers are wrong, try again" / "to generate a rationale given the correct answer; fine-tune on all the rationales that ultimately yielded" / "correct answers; repeat." |
| F27 | Positive-only reinforcement (PSR) of an LLM improves Pass@1 but degrades higher-k Pass@k because diversity drops. | reported | https://arxiv.org/html/2506.01347v2 (v2 2025-10-25), Zhu, Xia, Wei, Chen, Chen, Meng, "The Surprising Effectiveness of Negative Reinforcement in LLM Reasoning", quoted: "reinforcing only correct responses" / "degrades performance at higher" / "due to reduced diversity." — figures not inspected. |

## E. Failures and odd solutions kept on purpose (diversity, deception)

| id | Finding | Label | Source |
|---|---|---|---|
| F28 | Lehman & Stanley state that, through deception, an objective function may prevent the objective from being reached and misdirect search to dead ends. | verified | https://gpbib.cs.ucl.ac.uk/gp-html/Lehman_2011_EC.html (2011, season only "Summer"; Evolutionary Computation 19(2)), "Abandoning Objectives: Evolution through the Search for Novelty Alone", quoted: "Through deception, such objective functions may actually prevent the objective from being reached." / "Objective functions themselves may actively misdirect search towards dead ends." |
| F29 | Novelty search, ignoring the objective, significantly outperformed objective-based search in maze navigation and biped walking. | reported | same (2011), quoted: "in the maze navigation and biped walking tasks in this paper," / "novelty search significantly outperforms objective-based search," — abstract only. |
| F30 | MAP-Elites keeps the highest-performing solution in each cell of a user-chosen behaviour map, rather than one global best. | verified | https://ar5iv.labs.arxiv.org/html/1504.04909 (2015-04-20), Mouret & Clune, "Illuminating search spaces by mapping elites", quoted: "the highest-performing one per cell is retained." |
| F31 | Mouret & Clune state that in deceptive problems one must cross low-performing valleys to reach the global optimum, and that other cells can be stepping stones. | verified | same (2015-04-20), quoted: "one has to cross low-performing valleys to find the global optima." / "may provide stepping stones to high-performing solutions in a region" / "it may be more likely to generate a solution for one cell by mutating a solution to a more distant cell." |
| F32 | In MAP-Elites runs, many high-performing elites descend from non-neighbouring cells. | reported | same (2015-04-20), quoted: "many high-performing elites do descend, not from immediate neighbors," — the lineage data were not inspected. |
| F33 | Lexicase selection does not aggregate fitness over test cases; it considers test cases one at a time in random order. | verified | https://www.cs.hamilton.edu/~thelmuth/publications_bib.html (2015-10, month only; IEEE TEVC 19(5):630–643), Helmuth, Spector, Matheson, "Solving Uncompromising Problems with Lexicase Selection", quoted: "lexicase selection does not base selection on a fitness value" / "that is aggregated over all test cases; rather, it considers test cases one at a time in random order." |
| F34 | Lexicase selection maintains higher population diversity than other selection methods tested. | reported | same (2015-10), quoted: "We provide evidence that lexicase selection maintains higher levels of population diversity than other selection methods," — abstract only. |
| F35 | Lexicase out-explores tournament selection, and relaxing its elitism (epsilon lexicase) further improves exploration. | reported | https://arxiv.org/abs/2107.09760 (v1 2021-07-20), Hernandez, Lalejini, Ofria, "An Exploration of Exploration: Measuring the ability of lexicase selection to find obscure pathways to optimality", quoted: "We verify that lexicase selection out-explores tournament selection," / "Additionally, we find that relaxing lexicase's elitism with epsilon lexicase can further improve exploration." — abstract only. |

## F. Shaped fitness, partial fitness, curriculum

| id | Finding | Label | Source |
|---|---|---|---|
| F36 | Adding a potential-based shaping reward preserves the optimal policy; other reward changes may yield suboptimal policies, and known shaping "bugs" come from non-potential rewards. | reported | https://mlanthology.org/icml/1999/ng1999icml-policy/ (1999, year only; ICML pp. 278–287), Ng, Harada, Russell, "Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping", quoted: "any other transformation" / "may yield suboptimal policies unless further assumptions are made about the underlying MDP." / "some well-known "bugs" in reward shaping procedures are shown to arise from" / "non-potential-based rewards" — proof not inspected. |
| F37 | A GA with partial fitness (each chromosome part scored and selected separately) converged better than a conventional GA on a coin-recognition task. | reported | https://www.jstage.jst.go.jp/article/iscie1988/9/2/9_2_74/_article (1996-02-15), Fukumi, Omatu, Nishikawa, "A Method to Design a Neural Network by the Genetic Algorithm with Partial Fitness", quoted: "The method divides a chromosome in the GA into several parts, the PFs of which are evaluated." / "As a result, it is shown that it is better than the conventional GA on convergence in learning," — abstract only, one task. |
| F38 | Ordering training examples as a curriculum gave significant generalization gains in Bengio et al.'s experiments. | reported | https://mlanthology.org/icml/2009/bengio2009icml-curriculum (2009, year only), Bengio, Louradour, Collobert, Weston, "Curriculum Learning", quoted: "The experiments show that significant improvements in generalization can be achieved by using a particular curriculum," — abstract only. |
| F39 | Hindsight Experience Replay learns from sparse binary (success/fail) rewards and may be seen as an implicit curriculum; its ablations call it crucial for training. | reported | https://papers.nips.cc/paper/2017/hash/453fadbd8a1a3af50a9df4df899537b5-Abstract.html (2017, year only; arXiv v1 2017-07-05), Andrychowicz et al., "Hindsight Experience Replay", quoted: "allows sample-efficient learning from rewards" / "which are sparse and binary" / "may be seen as a form of implicit curriculum." / "Our ablation studies show that Hindsight Experience Replay is a crucial ingredient which makes training" — abstract only; the relabeling mechanism itself was not read in the paper (see Gaps). |

## G. Counter-evidence: learning from (total) failures that does help

| id | Finding | Label | Source |
|---|---|---|---|
| F40 | Generalized Hindsight relabels a behaviour with a different task it is better suited for, and reports more efficient sample reuse than standard relabeling. | reported | https://arxiv.org/abs/2002.11708 (2020-02-26), quoted: "given a behavior generated under one task, Generalized Hindsight returns a different task that the" / "behavior is better suited for." / "Generalized Hindsight provides a substantially more efficient reuse" / "of samples" — abstract only. |
| F41 | STaR's rationalization (learning from failed problems with the answer as a hint) raised CommonsenseQA accuracy from 68.8% to 72.5%. | verified | https://ar5iv.labs.arxiv.org/html/2203.14465 (2022-03-28), quoted: "The inclusion of rationalization improved this performance to 72.5%." — 68.8% without it, per Table 1 as read in the page text; one dataset, the authors' own runs. |
| F42 | On GSM8K, STaR's rationalization did not substantially help (10.1% without vs 10.7% with). | verified | same (2022-03-28), quoted: "We observe that on this task, the use of rationalization does not substantially improve performance." |
| F43 | Training an LLM only on its wrong answers (NSR) improves over the base model across the whole Pass@k range, by suppressing wrong generations and shifting probability to other candidates. | reported | https://arxiv.org/html/2506.01347v2 (2025-10-25), quoted: "consistently improves performance over the base model across the entire" / "suppressing incorrect generations and redistributing probability mass toward other plausible candidates," — figures not inspected. |
| F44 | On Llama-3.1-8B-Instruct, all RL methods (NSR included) underperformed the base model, NSR keeping the most. | reported | same (2025-10-25), quoted: "All the methods underperforms the base model," (Figure 4 caption) — figure not inspected. |
| F45 | NSR's authors tie its advantage to a strong model prior (Qwen models). | unproven | same (2025-10-25), quoted: "the backbone model itself often determines whether RL can bring benefits." / "when the model prior is strong (e.g., Qwen models)." — the dependence is not directly tested; it rests on a Qwen-versus-Llama contrast. |
| F46 | SGPO gets signal from all-wrong groups by adding step-wise diversity from a judge model; it helps most early and mid-training, not uniformly across benchmarks. | reported | https://arxiv.org/abs/2505.11595 (v5 2026-03-10), quoted: "SGPO improves average performance and is effective in early and mid-training when all-negative groups" / "are prevalent, while improvements are not uniform across every benchmark and depend on the structure" / "and informativeness of negative samples." — abstract only. |
| F47 | Reflexion agents reflect verbally on task feedback and keep the reflection in an episodic memory for the next trial; reported 91% pass@1 on HumanEval vs 80% for GPT-4. | reported | https://arxiv.org/abs/2303.11366 (2023-03-20), Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning", quoted: "Reflexion agents verbally reflect on task feedback signals," / "then maintain their own reflective text in an episodic memory buffer" / "Reflexion achieves a 91% pass@1 accuracy on the HumanEval coding benchmark," — abstract only. |
| F48 | Active CMA-ES, besides enlarging variance in successful directions, decreases variance in especially unsuccessful directions (uses the worst offspring with negative weights). | reported | https://web.cs.dal.ca/~dirk/aCMA/ (undated page), quoted: "additionally actively decreases variances in especially unsuccessful directions" / "accelerating the convergence of covariance matrix adaptation evolution strategies" — no numbers on the page; gives the exact title Jastrebski & Arnold, "Improving evolution strategies through active covariance matrix adaptation" (CEC 2006), not inspected. Hansen's tutorial (F18 URL, read past character 100000) confirms the lineage: "have been introduced in the seminal paper of Jastrebski and Arnold". |
| F49 | Michalski's Learnable Evolution Model replaces mutation/recombination with a learner that induces why some individuals are superior to others, and breeds from those hypotheses. | verified | https://mlanthology.org/mlj/2000/michalski2000mlj-learnable (2000, year only; Machine Learning 38:9–40), quoted: "a learning system seeks reasons why certain individuals in a population" / "are superior to others in performing a designated class of tasks." — the abstract as read does not say explicitly that low performers are used as the contrast group. |
| F50 | Winston's concept learner used exemplars that each differ from the current model in precisely one relevant feature (the "near miss" idea). | reported | https://www.jimdavies.org/summaries/winston1975.html (summary by J. W. Murdock, 1997; page last modified 1999-03-10), quoted: "each exemplar differs from the current understanding of the model in precisely one relevant feature." — a secondary summary of Winston, "Learning Structural Descriptions from Examples" (1975); the summary itself does not use the words "near miss". |

## Gaps

- **NOT FOUND: a source using EJ's exact phrasing** ("learn the mistakes in a success, not from total failure").
  Queries: "genetic algorithm learn from partially successful solutions not from total failures zero fitness
  population no selection signal" (WebSearch). The closest established statements found are F1–F2 (needle in a
  haystack; "tells you when you are getting close"), F3/F4 (pass/fail and all-same groups give no signal) and F17
  (keep the parent, mutate, accept if at least as good). Which one EJ learned is not known.
- **HER relabeling mechanism (the "learn from failure by calling it a success for another goal" part) not read in
  the primary.** The arXiv PDF, ar5iv and arXiv HTML pages gave no body text (ar5iv only links the PDF; the PDF could
  not be rendered — `pdftoppm` is not installed). The OpenAI page returned 403. Only the abstract (F39) and the
  Generalized Hindsight abstract (F7, F40) were read. The phrase "re-examine this trajectory with a different goal"
  was seen only in a search snippet — not quoted.
- **Goldberg & Deb (1991), "A Comparative Analysis of Selection Schemes Used in Genetic Algorithms"**: PDF fetch
  timed out (300 s). Takeover time and the comparison of proportionate/rank/tournament selection rest on Wikipedia
  rows (F11–F15), not on the primary.
- **Beyer & Schwefel (2002), "Evolution strategies — A comprehensive introduction"**: PDF not renderable; Scholarpedia's
  ES article failed (expired certificate). Rechenberg (1973) not read (German, offline). The 1/5 rule rests on
  Glasmachers (F19, F20).
- **Jastrebski & Arnold (2006)** (active CMA) not obtained; IEEE only. No measured speed-up for using unsuccessful
  offspring was read (F48 is `reported`).
- **Deceptive/trap functions (Goldberg)**: complex-systems.com returned 500, repository.ias.ac.in returned 404; Sastry
  et al. abstract read but says nothing on deception. Deception rests on F28 and F31.
- **Royal Road functions (Mitchell, Forrest, Holland 1992)**: PDF not read; Belding (2001, arXiv cs/0104011) read but
  has no sentence on plateaus or flat fitness.
- **Nordmoen et al. (2021), MAP-Elites stepping stones in modular robotics** (PMC8115726): blocked by a reCAPTCHA page.
- **A schema-theory note** that calls the fitness spread within a partition the "convergence signal"
  (digitalcollections.ohsu.edu csetech-240.pdf) was seen only as a search snippet; PDF not read.
- **Michalski LEM "H-group / L-group" terms**: not found in the pages read; F49 does not confirm that LEM learns from
  the low-fitness group explicitly.
- **Out of scope:** this repository's harness code (path recording, the 2% rule, six-whys) was not read — that is the
  explorer's job (method 3.8 item 10). The harness reading below is built from the brief's description only.
- **Budget:** no budget given. Ran 21 web searches and about 50 fetches (failures listed above).

## What this means for the harness (researcher's reading)

Inference prose, not findings; no tag. Each point names its premises.

1. **The harness's success loop is a (1+1)-ES.** Borrow the recorded success path as parent, change at least one
   thing, keep the result if it is better: that is exactly the (1+1)-selection in F17 (one parent, one mutant, keep
   if at least as good, best-so-far never lost). So the harness already runs the GA lesson EJ remembers in its
   simplest, most elitist form.

2. **What GA actually teaches is "learn where outcomes differ", not "learn only from successes".** F1–F4, F6, F8 and
   F9 say the same thing in five fields: if every attempt fails, *and also* if every attempt succeeds, there is no
   spread and so no signal (F4 filters both accuracy 0 and 1; F8 keeps goals with success between 0.1 and 0.9).
   The "mistake inside a success" is the signal because it sits next to a better or worse variant of the same task.
   For the harness: a borrowed path plus a changed attempt gives exactly such a pair; a total failure with no
   successful sibling does not, by itself.

3. **The 1/5 rule says how big "change at least one thing" should be.** F19–F20: if most attempts beat the parent,
   the changes are too timid — change more; if few do, change less. Recording, per task type, how often the child
   beats the parent would give the harness this dial. The 2% aim is a target on the size of gain; the 1/5 rule is a
   target on the rate of success — different quantities, and F21 says the fixed 1/5 constant is now mostly
   superseded, so treat it as a direction, not a number.

4. **Pure elitism has known costs; keep more than one parent.** F11 (high pressure under-explores), F27 (training
   only on successes cuts diversity at high k), F28–F31 (deception: the best path can lead to a dead end; good
   solutions often descend from other cells), F33–F35 (lexicase keeps specialists that fail overall but pass a rare
   case). Mapped to the harness: a store with one best path per task type is a single elite; a small archive of
   different successful paths (per kind of task, MAP-Elites style) would guard against borrowing a deceptive parent.

5. **The counter-evidence is real but has a shape: failures help when they are turned into a contrast or a
   different success.** HER/Generalized Hindsight relabel the failure as success at another goal (F7, F39, F40);
   STaR gives the right answer and lets the model rebuild a path to it (F41 helped on one dataset, F42 not on
   another); active CMA and LEM use the worst only *in contrast to* the best (F48, F49); SGPO extracts step-level
   partial credit inside all-wrong groups (F46); Winston's near miss is a failure that differs in one feature (F50);
   NSR learns from wrong answers alone but seems to need a model that already succeeds sometimes (F43–F45).
   For the harness: the six-whys on a failure is closest to Reflexion (F47) — verbal feedback stored for the next
   trial. GA suggests it pays most when it names the *one step* that differed from a successful path (near miss,
   step-level credit), or when the failed run is recorded as a success for the goal it did reach (hindsight).
   A total failure with neither a sibling success nor a relabel gives the least to learn from.

6. **Task choice matters as much as run choice.** F8 and F38: tasks the system always solves or never solves teach
   little; the useful band is in between. Not measured for this harness.


**House rules that bind the answer:**
- Never fill a missing threshold with an invented number; a trigger is a comparison. EJ's numbers given as aims ("try to be 2% better", "80%") are reported, never gates.
- MUST only for a safety bound; a method rule is SHOULD at most (EJ has chosen MUST for R12.2, R12.3 and R12.7).
- Every check must be able to fail, and is shown failing once on a planted wrong input.
- No paid engine call without EJ's go-ahead.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 范蠡 (Fan Li)'s mouth that your list does not contain.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 范蠡 (Fan Li) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>
