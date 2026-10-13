# 孫子 (Sun Tzu) — where my rules help in the workflow-design method

## Answer

Give me three places, in this order.

**1. 3.1 readiness — the tools check and the information check.** Ask me: *"For each tool this node calls and each fact this design leans on: what was actually run, not read; what is sourced to a file or a person; and what does the design own if it does not answer?"* This is my most reliable ground because every answer is an observable — a command with its output, or a finding id — not an opinion. Price: it costs one probe per tool and one source per build-driving fact, and it will demote things called "known" into preparation pieces. That is the method's own instruction ("Run it; do not assume"), paid for early.

**2. 3.2 write the algorithm / 3.3 list the unclear spots.** Ask me: *"For this piece, which of the three do we know — that our engines and tools can do it, that the task as posed can be done, and that the ground (files, blueprint, information) permits it — and which is only half a victory?"* Price: it adds a known/unknown line per piece and will put pieces the method called "clear" back on the unclear list. That is exactly what the method wants caught before a confident algorithm is trusted.

**3. 3.5 loops / 3.6 the node's quality control.** Ask me: *"Where is this node's 勢 — the check it cannot edit, the contract, the state, the information boundary — and what has been left to the worker's good character?"* Price: it forces a node whose only control is an instruction to be rewritten as contract + check; if no such check can be named, the node is not loop-ready and the design is rewritten now rather than a failed attempt later.

This is conditional. If a wrong design is cheap to redo and the uncertainty is a fixed system rather than a reacting opponent, place 1 still holds, place 3 becomes a restatement of the method, and my reckoning rules (#1, #5) are priced too high.

## How I decided

1. I read the brief's facts, the eight steps in `.claude/skills/workflow-design/SKILL.md`, and the detail in `docs/WORKFLOW_DESIGN_METHOD.md`, then re-read my list while working (my reading — not a rule).
2. **3.1** fits my **#17** (learn the other side by acting on it: 「故策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處。」, quoted) against the method's "Run it; do not assume" for tools. My **#2** fits the stance: "Do not rely on the enemy not coming or not attacking; rely on having the means to meet them and on having what cannot be attacked" (quoted) — a node that rests on an engine returning is a plan resting on the enemy not coming; it must own the canary, the baseline and the blocked-node exit. My **#11** fits the information check: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」 (quoted) — a build-driving fact must come from a named source or person, not from ghost (model knowledge), likeness (analogy to an earlier run) or measurement (arithmetic alone). That is method 3.8 item 12's finding-id rule, so I am testing the method against itself, not importing a foreign test.
3. **3.2 / 3.3** fits my **#4**: its five ways to know victory and the half-victory passage 「知吾卒之可以擊，而不知敵之不可擊，勝之半也…」 (quoted) give three independent knowns — our means, the other's attackability, the ground. The method's only test at 3.2 is "can I name a check?"; #4 catches a written check that stands on an uncounted factor. My **#1** fits the empty-list warning: 「多算勝，少算不勝，而況於無算乎？」 (quoted) — an unclear-spot list with no items on a non-tiny challenge is the 無算 case, not a clean design.
4. **3.5 / 3.6** fits my **#12**: 「故善戰者，求之於勢，不責於人，故能擇人而任勢。」 and 「勇怯，勢也」 (quoted) — the method's "a check the worker cannot edit" (3.5 item 5) and "a label is not a node … must pay for itself" (3.2) are the same instruction: build the 勢, choose the person, then rely on the position, not on the person's will. #12 also fits "every node names its role, engine, exact model and effort": choosing the agent is 擇人, but correctness still has to come from 勢.
5. I looked for the same fit at 3.4 size, 3.7 concurrency and 3.0 vision and did not find it — my #14 has no unit that transfers to agents or tokens, my #7 assumes a reacting enemy, and my #20 is an `attributed` narrative, not a requirements method. Those became the risks below (my reading, with the items named).
6. Every recommendation is conditional on facts I was not given — the stakes, whether the uncertainty is an adversary or a fixed system, and the thresholds. The brief's rule 2 requires that, so they are under "What I need to know" (my reading).

## What I need to know

1. **Can a wrong design be cheaply redone?** If yes, my reckoning (#1) and "never from anger" (#5) are over-priced here; if the change is one-shot or hard to reverse, they are the first thing to use. I was given the method's "designing is cheap; running agents is not," not EJ's stakes for this task.
2. **Is the uncertainty an adapting "other side," or a fixed, inspectable system** (files, engines, a spec)? If fixed, my #7/#9/#10 do not transfer and must not be used; #17 still does, because its four probes are just controlled contact.
3. **What is the unit and threshold for "known enough" at 3.2/3.3 and "advantage" at 3.4?** The method supplies one threshold I saw — a challenger design replaces the default only on "a written claim of ≥20% lower projected run cost at equal coverage." I was given none for the three knowns, and I will not supply it.
4. **Does this design build a product** (code, schema, UI, configuration)? If it does, my #2 has a baseline and blueprint sections to protect; if it only researches or answers, #11 carries more of the load and #2 is mostly a stance.
5. **Whose vision and requirements is the design for?** The method says the vision is EJ's and every result has one maker; my text has no rule for eliciting it. That is my biggest gap (my reading).

## Costs and risks

1. **3.4 size, and every number — not reliable.** My #14 is a force ratio: 「十則圍之，五則攻之，倍則分之…」(quoted). It is a ratio of military force, and I was not given that it transfers to agents, tokens or wall-clock. Asking me "how many agents" invites me to fill a missing unit with my own value, which the method forbids. Use EJ's or the ledger's measured numbers.
2. **3.7 concurrency and the graph's shape — not reliable through #7 (and #10's concealment).** My #7 says 「兵者，詭道也。故能而示之不能…」(quoted); it assumes an opponent who reacts and whom you deceive. A workflow's workers are not an enemy. Method 3.6 does withhold information (a verifier never sees the worker's reasoning), but that is blindness for independence, not deception for advantage; asked to design asymmetry against workers or verifiers, I would give an answer that corrupts the shared state. The part that does transfer is my #9, 「故善戰者，致人而不致於人。」 (quoted) — the design, not the agents, sets the schedule — and I should be held to that part only.
3. **3.0 vision and acceptance criteria — not reliable.** My list has no rule for whose product this is, who uses it, or a criterion some input can fail. My closest item, #20, is an `attributed` dialogue about which of six houses falls first; it is a judgment, not a method, and using it for requirements would put words in 孫子's mouth. Leave 3.0's vision and requirements to EJ.
4. **The stakes economy as a whole — conditionally not reliable.** My text is written for one-shot, irreversible, expensive war: 「亡國不可以復存，死者不可以復生。」 (#5, quoted) and 「日費千金」 (#8, quoted). A design step is cheap and resumable. Without the stakes I will over-count (from #1/#5), or, pulled by #8's 「兵聞拙速」, under-count and rush a change that should have been reckoned. My #8 and my #1 point opposite ways; which applies is EJ's call, not mine.

## How we would know I was right

Take the next non-tiny challenge and write my three questions' answers into the design before anything runs, then measure against the method's own records:

- **from 3.1:** the count of nodes dispatched on a tool with no run-output, or on a build-driving fact with no source id (or no *model knowledge* mark). My prediction is 0.
- **from 3.2/3.3:** each piece's three knowns are written, and the unclear-spot list holds at least one item the "step has a check" test alone would have missed. If the list stays empty on a non-tiny challenge, #1 says the reckoning never happened.
- **from 3.5/3.6:** the count of nodes whose verification is an open-ended review rather than a check the worker cannot edit (a failing count for the design, not for me).

It is falsifiable in both directions: if a node later fails on a factor that was available at design time and was not written, my contribution failed there; if asking the three questions changes no piece, adds no spot and proves no tool, the help was zero. The cost side comes from `harvest_run.py`'s token record compared with the failures the questions caught — the threshold is EJ's, not mine, and I will not invent one. The method already carries the warning instrument (trial 1's ≈309k-token record for a one-line README fix), so no new tool is needed.
