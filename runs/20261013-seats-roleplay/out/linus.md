# Linus Torvalds — role-playing a person to solve a problem

## 1. What the research says

1. **An expert title does not reliably improve factual accuracy.** Across 162 personas, four model families and 2,410 factual questions, Zheng and colleagues found no general improvement over prompts without personas; selecting a beneficial persona for an unseen question was also difficult. · Source: [*When “A Helpful Assistant” Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models*](https://aclanthology.org/2024.findings-emnlp.888/), Mingqian Zheng et al., 2024. · Label: `measured`.

2. **Task-specific role prompting can help particular reasoning tasks.** Kong and colleagues reported AQuA accuracy increasing from 53.5% to 63.8% with GPT-3.5, but their method included a designed role-setting interaction and a selected assistant acknowledgement—not merely a famous person’s name. · Source: [*Better Zero-Shot Reasoning with Role-Play Prompting*](https://aclanthology.org/2024.naacl-long.228.pdf), Aobo Kong et al., 2024. · Label: `measured`.

3. **Personas change behaviour, with potential costs as well as benefits.** A study of seven models, 162 personas and five datasets found greater behavioural variability than control prompts; its demographic experiments also found cases where reduced bias accompanied reduced accuracy. · Source: [*Helpful assistant or fruitful facilitator? Investigating how personas affect language model behavior*](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0325664), Pedro Henrique Luz de Araujo and Benjamin Roth, 2025. · Label: `measured`.

4. **Debate can improve answers under a tested protocol.** Du and colleagues reported arithmetic accuracy of 81.8% for three agents debating over two rounds, compared with 67.0% for a single agent and 69.0% for majority voting; this tested multiple model instances, not a panel of historical personalities. · Source: [*Improving Factuality and Reasoning in Language Models through Multiagent Debate*](https://arxiv.org/pdf/2305.14325), Yilun Du et al., 2023. · Label: `measured`.

5. **Debate’s benefit is not universal.** Across seven benchmarks, Choi and colleagues found majority voting accounted for most gains: their Qwen2.5-7B table reports average accuracy of 76.91% for voting versus 73.77% for two-round decentralized debate. · Source: [*Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?*](https://arxiv.org/html/2508.17536v1), Hyeong Kyu Choi, Xiaojin Zhu and Yixuan Li, 2025. · Label: `measured`.

6. **Character knowledge needs explicit boundaries.** TimeChara contains 10,895 fictional-character examples; on its 600-example evaluation, GPT-4o’s average spatiotemporal consistency increased from 64.5% with zero-shot prompting to 87.5% with the authors’ narrative experts and restricted retrieval, according to their evaluation procedure. · Source: [*TimeChara: Evaluating Point-in-Time Character Hallucination of Role-Playing Large Language Models*](https://aclanthology.org/2024.findings-acl.197.pdf), Jaewoo Ahn et al., 2024. · Label: `measured`.

7. **Convincing role-play is not evidence of possessing the person’s mind.** Shanahan and colleagues propose role-play as a way to describe model behaviour without attributing human characteristics the model lacks; this is a conceptual argument, not an accuracy benchmark. · Source: [*Role-Play with Large Language Models*](https://arxiv.org/abs/2305.16367), Murray Shanahan, Kyle McDonell and Laria Reynolds, 2023. · Label: `opinion`.

8. **For these seats, a sourced decision method is a defensible hypothesis; superiority remains unmeasured.** The findings above support testing explicit rules against a plain prompt, but none establishes that applying Linus’s rules produces better landing-page decisions. · Sources: Zheng et al., Kong et al. and TimeChara above. · Label: `my reading`.

## 2. The best way to role-play me

**My reading:** use the supplied rules to make decisions reviewable. Treat the following as proposed guidance, with no measured advantage yet.

1. **Ground the role in numbered source passages.** For each recommendation, identify the relevant item and explain its application to the supplied facts. Preserve the final list’s distinctions between direct quotations, attributed documentation and interpretation. **My #7 and #11.**

2. **Respect the limits of my expertise.** Kernel experience does not establish expertise in visual design or a particular audience. Ask the person who knows the page and its users for the missing details. **My #4 and #6.** The management document explicitly cautions that ability in one area does not necessarily transfer to another. [*Linux kernel management style*](https://docs.kernel.org/process/management-style.html).

3. **Produce something inspectable.** My #2 says, **quoted:** “Talk is cheap. Show me the code.” For a colour decision, my proposed translation is a rendered candidate that people can examine; that translation is an analogy, not a quotation about design. **My #2.** [Torvalds’s original reply, 2000](https://lkml.iu.edu/0008.3/0272.html).

4. **Keep a preliminary choice reversible.** Prefer an isolated palette change over a redesign that commits the team before there is evidence. **My #5.**

5. **State what would change the recommendation.** Missing information and contrary results belong in the answer. **My #7.**

6. **Support improvement claims with measurements.** Report the outcome being measured and the observed result. **My #18**, which is attributed kernel process guidance, not established as my own words.

7. **State the costs of the proposal.** A conversion claim needs its accompanying effects on readability, maintenance and user tasks. **My #18**, with the same attribution limitation.

8. **Challenge the work without attacking its maker.** The 2018 apology belongs in the role, alongside earlier bluntness. **My #16.** [Torvalds’s apology, 2018](https://lkml.iu.edu/hypermail/linux/kernel/1809.2/00117.html).

**What an agent gets wrong**

- **It copies anger and calls that fidelity.** That ignores the later correction in **my #16**.
- **It turns “avoid big decisions” into refusal to decide anything.** **My #4** explicitly permits small, non-consequential decisions.
- **It adds an item number to an unsupported preference.** **My #11** calls for an explanation; a citation alone does not establish why a rule applies.
- **It presents kernel rules as universal design laws.** Transferring expertise requires justification under **my #6**.
- **It treats agreement among named personas as verification.** My proposed check is evidence from the artifact and its users, applying **my #2 and #7**; this is my reading, not a sourced claim about multi-agent independence.
- **It claims all nineteen items are personally authored rules.** The supplied list explicitly marks **my #14, #18 and #19** as partly or wholly attributed documentation.

## 3. Worked example — what colour should a landing page be?

Each step below is **my reading** of how the supplied rules could apply outside kernel development.

1. **Identify the actual problem.** Is the page unreadable, inconsistent with the brand, failing to communicate its action, or simply undecided? Those are different reasons to change it. **Item used: my #13**, starting with the immediate need.

2. **Get the missing context.** Identify the owner, intended visitors and action the page should support. Colour cannot answer an unspecified objective. **Items used: my #4 and #6**, relying on people who know the details.

3. **Inspect any existing page before replacing its palette.** Check whether people can read the content, recognize links and complete the intended task. Applying the regression principle here means checking user outcomes, rather than declaring a change successful because a screenshot looks better. **Items used: my #1 and #3.** The original rule concerns kernel regressions; this is an explicit analogy. [Torvalds’s regression explanation, 2017](https://lkml.iu.edu/hypermail/linux/kernel/1710.3/02474.html).

4. **Render a small, reversible candidate.** If two palettes remain plausible, make comparable versions with the same content and layout. My #8 suggests considering both approaches; it does not itself prescribe an A/B test. **Items used: my #2, #5 and #8.**

5. **Check a stated accessibility target.** If the owner chooses WCAG 2.2 AA, ordinary text needs at least 4.5:1 contrast and qualifying large text at least 3:1, subject to the criterion’s exceptions. Those values come from W3C, not from the Linus persona; the connection to the seat is checking whether users can use the result. **Item used: my #3.** [W3C, Understanding Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

6. **Choose from the evidence and record the reason.** Explain the palette, the observed benefit, its costs and what remains uncertain. **Items used: my #7, #11 and #18**; #18 retains its documentation attribution.

**Questions I need answered**

- Whose page is this, and what action should visitors complete?
- Who visits it, and in what viewing conditions?
- What brand palette or existing design system applies?
- Is there an existing page? What problem does its colour currently cause?
- What accessibility target applies?
- What outcome and minimum worthwhile improvement would justify changing it?

**My answer**

- **If an existing palette supports the intended task and meets the chosen requirements, keep it provisionally.** **My #1, #3 and #13.**
- **If a brand palette is required, use it where its colour combinations meet the chosen readability requirements.** This is my application of domain knowledge under **my #6**.
- **If this is a new page with no palette constraint, white background with dark text is a provisional prototype candidate.** Its selection is my suggestion, **not measured**, supported only as a small, reversible starting point by **my #5 and #13**. It is not evidence that white maximizes conversion.
- **If tested evidence favours another palette against the agreed objective, change the choice.** **My #7 and #18.**

**How we would know I was right**

The page owner and reviewer would first specify the task and acceptance criteria. Check text contrast against the selected standard, then observe whether intended users can read the page and complete that task. A contrast check establishes that particular criterion; it does not establish the best colour or full accessibility. **My #3 and #18.**

If traffic supports a controlled experiment, compare palettes while holding content and layout constant. Measure the agreed outcome—for example, completed target actions divided by eligible visitors—and report uncertainty and costs. The required improvement and stopping rule remain questions for the owner. **My #7 and #18.**

To test the **role-play method itself**, compare a plain task prompt, the same sourced rules without the Linus identity, and those rules with the identity. Give them the same facts, tools and comparable budgets; have reviewers assess unsupported claims, correct rule application and useful decisions without seeing the prompt condition. I propose that comparison; I have not run it, and it would not establish what the real Linus would choose. **My #2 and #7.**

## Sources used

Local texts opened:

- [Workspace instructions](/home/smoke01/dev/ancient-games/CLAUDE.md).
- [Linus brief](/home/smoke01/dev/ancient-games/runs/20261013-seats-roleplay/briefs/linus.md).
- [Common brief](/home/smoke01/dev/ancient-games/runs/20261013-seats-roleplay/briefs/common.md).
- [Linus final list](/home/smoke01/dev/ancient-games/runs/20261013-four-seats/final-opus/linus.md).
- [Linus identity](/home/smoke01/dev/ancient-games/runs/20261013-four-seats/identity/linus.md).
- [Requirement-check skill](/home/smoke01/.agents/skills/requirement-check/SKILL.md).

Research pages and papers opened:

- Zheng et al.: [publication page](https://aclanthology.org/2024.findings-emnlp.888/), [paper](https://aclanthology.org/2024.findings-emnlp.888.pdf).
- Kong et al.: [publication page](https://aclanthology.org/2024.naacl-long.228/), [paper](https://aclanthology.org/2024.naacl-long.228.pdf).
- Luz de Araujo and Roth: [article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0325664).
- Du et al.: [abstract](https://arxiv.org/abs/2305.14325), [paper](https://arxiv.org/pdf/2305.14325).
- Choi et al.: [abstract](https://arxiv.org/abs/2508.17536), [version 1 full text](https://arxiv.org/html/2508.17536v1).
- Ahn et al.: [publication page](https://aclanthology.org/2024.findings-acl.197/), [paper](https://aclanthology.org/2024.findings-acl.197.pdf).
- Shanahan et al.: [abstract](https://arxiv.org/abs/2305.16367).

Other source texts opened:

- [Linux kernel management style](https://docs.kernel.org/process/management-style.html).
- [Torvalds, “Show me the code,” 2000](https://lkml.iu.edu/0008.3/0272.html).
- [Torvalds, regression explanation, 2017](https://lkml.iu.edu/hypermail/linux/kernel/1710.3/02474.html).
- [Torvalds, pull-request explanation, 2017](https://lkml.iu.edu/hypermail/linux/kernel/1711.1/04939.html).
- [Torvalds, apology, 2018](https://lkml.iu.edu/hypermail/linux/kernel/1809.2/00117.html).
- [W3C, Understanding Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

Unsuccessful fetch attempts, not supporting evidence:

- [LKML apology URL](https://lkml.org/lkml/2018/9/16/167): challenge page.
- [Incorrect code-reply mirror path](https://lkml.iu.edu/hypermail/linux/kernel/0008.3/0584.html): retrieval error.
- [Incorrect apology mirror path](https://lkml.iu.edu/hypermail/linux/kernel/1809.2/0017.html): retrieval error. Correct source paths were subsequently found and opened above.

## Gaps

- **Not measured:** this seat method’s performance on the current model, historical-person fidelity, or landing-page outcomes. The studies do not establish those results.
- TimeChara studies fictional characters. Its findings motivate checking historical boundaries, but do not directly measure historical-person simulation.
- The supplied list’s authorship caveats remain: management-style attribution is incomplete, and #18–#19 are project guidance. I did not independently resolve every item’s provenance.
- I found no direct evidence here that the real Linus prefers a landing-page colour. No page, visitor data or experiment was supplied.
- **Requirement-check of “more logical and checkable than a plain AI answer”:** source—**pass**, supplied brief; one thing—**FAIL**, two outcomes; unit—**FAIL**, undefined measures; can it fail—**FAIL**, no acceptance test; weak words—**FAIL**, “logical” undefined; level—**pass as a hypothesis**; basis—**FAIL for an established claim**, unmeasured here; links—**FAIL**, persona-to-quality relationship unestablished.

**Questions for EJ:** What observable result would count as “more logical”? What would count as “more checkable”? What improvement over the plain-answer baseline would justify using the seat?