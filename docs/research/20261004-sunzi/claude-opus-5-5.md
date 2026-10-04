# 孫子兵法 — claude-opus-5-5

Every line below is RECALLED. In this session web fetch and network access were denied, and the repository holds no
copy of the text (a search for 知彼 found nothing). I did not check any line against a source. The Chinese is
written from memory in traditional characters, following the received text (the Song-era line that the 十一家注
editions belong to). The Yinqueshan bamboo slips (excavated 1972) differ from that text in places, and I cannot say
where for any given line. Before anyone quotes these lines as citations, check each one against a real edition
(for example ctext.org, 孫子兵法).

### 1. Decide go or no-go by a written comparison made before you commit, and engage only when it already favours you.
- **Text**: 夫未戰而廟算勝者，得算多也；未戰而廟算不勝者，得算少也。多算勝，少算不勝，而況於無算乎！ — "One who wins the temple calculation before battle has more counting-rods; one who does not, has fewer. More wins over fewer — how much more over none at all!" (計篇 *Laying Plans*). With: 勝兵先勝而後求戰，敗兵先戰而後求勝。 — "The victorious army wins first and then seeks battle; the defeated army fights first and then seeks victory." (形篇 *Dispositions*). And: 合於利而動，不合於利而止。 — "Move when it accords with advantage; stop when it does not." (火攻篇 *Attack by Fire*).
- **Basis**: RECALLED (from training).
- **Reading**: Before a campaign, the court compared the two sides on fixed factors (the five matters and seven assessments listed earlier in 計篇) and counted who came out ahead. The line is ambiguous. 得算多 can mean "more factors scored in our favour" or "calculated more thoroughly". Both readings support the rule below. 形篇 adds that the battle should confirm an advantage you already built, not go looking for one. Merged here: the three lines make one idea, a pre-commitment assessment with an explicit stop condition.
- **Design rule**: Before any agent is dispatched, write the assessment against named criteria (task is clear, inputs exist, check exists, budget fits), and also write the condition that would stop the run. If the assessment does not favour the run, do not start it.
- **Violated by**: Launching the swarm first and finding out from its output whether the task was feasible.

### 2. Secure what is in your control first; the opening for success depends on things you do not control.
- **Text**: 昔之善戰者，先為不可勝，以待敵之可勝。不可勝在己，可勝在敵。……故曰：勝可知，而不可為。 — "The skilled fighters of old first made themselves unbeatable, then waited for the enemy to become beatable. Being unbeatable lies with oneself; being beatable lies with the enemy. … So it is said: victory can be known, but not made." (形篇 *Dispositions*)
- **Basis**: RECALLED (from training).
- **Reading**: Sunzi splits the outcome into two parts. One you control fully: not losing. The other you cannot force: the opponent's opening. 勝可知而不可為 can be read as "you can tell when victory is possible, but you cannot manufacture it", or more weakly as "you can foresee victory but not guarantee it".
- **Design rule**: Build the parts that guard against loss before the parts that try to succeed: rollback, a dry-run or read-only mode, budget caps, a check that can fail. Do not treat success on the hard, uncertain part as something the design can guarantee. The mapping is loose, because a task is not an opponent. What carries over is the split between what you control and what you do not.
- **Violated by**: A workflow that writes to shared state before it has a way to undo the write, on the theory that the change will work.

### 3. Assess both the task and your own executors; knowing only one side gives coin-flip results.
- **Text**: 知彼知己者，百戰不殆；不知彼而知己，一勝一負；不知彼不知己，每戰必殆。 — "Know the other and know yourself, and in a hundred battles you will not be imperilled. Not knowing the other but knowing yourself, one win, one loss. Knowing neither, every battle is peril." (謀攻篇 *Attack by Stratagem*)
- **Basis**: RECALLED (from training).
- **Reading**: The claim is about not being imperilled (不殆), not about always winning. Knowing yourself without knowing the other gives a coin flip. Sunzi does not mention the opposite case, knowing the other but not yourself.
- **Design rule**: A readiness check has two halves, and both must be filled in. 彼: what the task and its environment are actually like. 己: what each engine, tool and budget can actually do, measured or at least marked *reported* versus *verified*. If either half is empty, treat the outcome as uncertain and do not plan as if it were assured.
- **Violated by**: Assigning a node to an engine because it is the default, without having checked what that engine can do on this kind of task.

### 4. Prefer the cheapest resolution; a full multi-agent assault is the last resort.
- **Text**: 是故百戰百勝，非善之善者也；不戰而屈人之兵，善之善者也。故上兵伐謀，其次伐交，其次伐兵，其下攻城。攻城之法，為不得已。 — "Winning a hundred battles out of a hundred is not the best of the best. Subduing the enemy's army without fighting is the best of the best. So the highest form strikes at plans, next at alliances, next at armies, and the lowest besieges walled cities. Siege is done only when there is no alternative." (謀攻篇 *Attack by Stratagem*)
- **Basis**: RECALLED (from training).
- **Reading**: The text ranks ways to get the result by how much they cost, and siege, the most expensive, comes last. 伐謀 is ambiguous. It can mean "attack the enemy's plans" (break their strategy) or "attack by means of planning". The ranking holds under either reading.
- **Design rule**: Go up a fixed ladder of cost, and record why each cheaper rung was not enough before moving to the next. The rungs: remove the need for the task (ask, reuse, find that it is already done); then one main agent; then one agent plus an independent checker; and only last, a multi-agent graph. The mapping is loose: there is no enemy here, only cost.
- **Violated by**: Designing a ten-node workflow for something a single question to the owner, or one existing function, would have settled.

### 5. Bound every repetition, and prefer a crude result that ends over a refined one that drags on.
- **Text**: 故兵聞拙速，未睹巧之久也。夫兵久而國利者，未之有也。 — "In war one hears of clumsy speed; one has not seen cleverness that lasts long. There has never been a prolonged war that benefited the state." With: 故兵貴勝，不貴久。 — "So in war, value victory, not duration." (作戰篇 *Waging War*)
- **Basis**: RECALLED (from training).
- **Reading**: The chapter's point is that a campaign's costs pile up the longer it lasts (supplies hauled a thousand li, a thousand pieces of gold a day). 拙速 is ambiguous. One reading praises speed even at the cost of finesse. A narrower reading says only that quick campaigns are known to work, while clever long ones are never seen to, and leaves clumsiness neither praised nor blamed.
- **Design rule**: Every loop gets a hard iteration or budget cap and a stop condition, set before it starts. When the cap is hit, the loop ends and reports its state; it does not ask for "one more pass". If a node has no cap, the design is not finished.
- **Violated by**: A verify-and-repair loop that runs until the reviewer is satisfied, with no limit on rounds.

### 6. Scale comes from fixed units and a fixed signalling protocol, not from headcount.
- **Text**: 凡治眾如治寡，分數是也；鬥眾如鬥寡，形名是也。 — "Governing many is like governing few: it is a matter of divisions and numbers. Fighting with many is like fighting with few: it is a matter of forms and names." (勢篇 *Energy / Momentum*)
- **Basis**: RECALLED (from training).
- **Reading**: 分數 is the organisation into units of fixed size under fixed commanders. 形名 is usually read as the signals: flags seen and gongs and drums heard, as 軍爭篇 says when the voice cannot carry. Some read 形名 more abstractly as "forms and their names", meaning a defined vocabulary that matches commands to formations. Under either reading, a large force is controlled through structure and a shared code. The general does not talk to each soldier.
- **Design rule**: Do not add agents until the unit structure (who reports to whom) and the message format (a fixed schema or state-file layout that every node reads and writes) are defined. If the design cannot run two agents through that protocol, it will not run ten.
- **Violated by**: Fanning out to many subagents that each return free-form prose for the orchestrator to reconcile by hand.

### 7. Run the main line on the orthodox, proven pattern; reserve a bounded share for the unorthodox.
- **Text**: 凡戰者，以正合，以奇勝。 — "In all battle, engage with the orthodox; win with the extraordinary." With: 奇正相生，如循環之無端，孰能窮之？ — "The extraordinary and the orthodox give rise to each other, like a ring without end; who can exhaust them?" (勢篇 *Energy / Momentum*)
- **Basis**: RECALLED (from training).
- **Reading**: 正 is the expected, frontal force that holds the enemy. 奇 is the unexpected force that decides the battle. The pairing is ambiguous. Some commentators (Cao Cao's gloss is the one usually cited) take 正 as whoever engages first and 奇 as whoever comes in later from the side, so the roles depend on position and timing, not on what kind of unit it is. The second line says the two turn into each other: a 奇 that works becomes the new 正.
- **Design rule**: Most capacity goes to the default pattern for the task's category. A small, capped share goes to a deliberate alternative, and its results are recorded so a winning alternative can replace the default. The mapping is loose: Sunzi's 奇 means surprising an opponent, while here it means exploring alternatives. The project's 20% challenger rule has the same shape, which is a parallel and not evidence for it.
- **Violated by**: Either running only the default forever with no challenger, or treating every run as an experiment so there is no stable baseline to compare against.

### 8. Get reliability from the configuration, not from demands on the individual agent.
- **Text**: 故善戰者，求之於勢，不責於人，故能擇人而任勢。 — "So the skilled fighter seeks it in the configuration of forces (勢), and does not demand it of individuals; thus he can select people and rely on 勢." (勢篇 *Energy / Momentum*)
- **Basis**: RECALLED (from training).
- **Reading**: 勢 is the potential that a situation's arrangement creates. The chapter illustrates it with logs and round stones rolled down a steep mountain. The general builds the slope, and does not urge each stone. 擇人 is ambiguous. The plain reading is "choose the right people and then rely on 勢". I recall, but cannot check, a reading that takes 擇 as 釋, "let go of the individual and rely on 勢".
- **Design rule**: When a node keeps failing, change the structure around it (its inputs, its check, its contract, its stop condition). Do not add exhortations to its prompt ("be careful", "double-check"). A design that relies on one agent's diligence instead of a gate is wrong by this rule.
- **Violated by**: Answering a recurring error by adding "IMPORTANT: verify your work" to the prompt instead of adding an independent check.

### 9. Whoever guards everything is thin everywhere; choose where to be strong and say what is left unguarded.
- **Text**: 故備前則後寡，備後則前寡，備左則右寡，備右則左寡，無所不備，則無所不寡。 — "Guard the front and the rear is thin; guard the rear and the front is thin; guard the left and the right is thin; guard the right and the left is thin. Guard everywhere, and everywhere is thin." (虛實篇 *Weak Points and Strong*)
- **Basis**: RECALLED (from training).
- **Reading**: With fixed strength, covering more ground lowers the strength at each point. The same chapter has the other side of this: 我專為一，敵分為十 ("I concentrate into one; the enemy divides into ten"). This is about how a fixed budget gets spread, and that is the part that carries over.
- **Design rule**: Choose a small number of checks and spend real effort on each. Write down the risks the design deliberately leaves unchecked. A design that lists a shallow check for every imaginable risk fails this rule.
- **Violated by**: A review stage that asks one agent to check security, performance, style, correctness and docs in a single pass with the same budget it would have for one of them.

### 10. The plan has no fixed form; re-plan from the observed state at each checkpoint.
- **Text**: 夫兵形象水，水之形，避高而趨下；兵之形，避實而擊虛。水因地而制流，兵因敵而制勝。故兵無常勢，水無常形；能因敵變化而取勝者，謂之神。 — "The form of an army is like water. Water avoids the high and flows to the low; an army avoids the solid and strikes the empty. Water shapes its flow by the ground; an army shapes its victory by the enemy. So an army has no constant configuration, as water has no constant shape. One who can win by changing according to the enemy is called divine." (虛實篇 *Weak Points and Strong*)
- **Basis**: RECALLED (from training).
- **Reading**: The army's form is set by the ground and the enemy, not fixed in advance. 避實擊虛 adds that effort goes where resistance is weakest. The line does not say to abandon planning. The same text opens with planning (principle 1). It says the plan's *form* follows the conditions.
- **Design rule**: At each checkpoint, the next step is chosen from the current state file, not read off a fixed list. Every checkpoint has an explicit option to re-plan. Effort goes to the pieces the evidence shows are tractable. Contested pieces get set aside for later, not attacked head-on.
- **Violated by**: A fixed linear script that runs step 5 even though step 3's output showed the assumption behind step 5 was false.

### 11. The executor closest to the ground needs authority to deviate inside set bounds; the orchestrator must not steer blind.
- **Text**: 將能而君不御者勝。 — "Where the general is able and the ruler does not interfere, there is victory." (謀攻篇 *Attack by Stratagem*, one of the five ways to know victory). With: 塗有所不由，軍有所不擊，城有所不攻，地有所不爭，君命有所不受。 — "There are roads not to be taken, armies not to be struck, cities not to be attacked, ground not to be contested, and commands of the ruler not to be obeyed." (九變篇 *Variation of Tactics*)
- **Basis**: RECALLED (from training).
- **Reading**: 謀攻篇 also names how a ruler harms his army: ordering an advance or retreat without knowing whether the army can make it (縻軍, "hobbling the army"). The authority rests on knowledge. The general has it because he can see the ground and the distant ruler cannot. The text does not say the general answers to no one. The scope is "some commands", in a specific list.
- **Design rule**: The orchestrator sets the objective, the bounds and the check, and does not script the executor's steps. The executor may depart from the given steps when what it observes contradicts them, but it must record the departure and the reason in the state file. Irreversible or outward-facing actions stay outside this authority and still need owner approval. That limit is the designer's, not Sunzi's.
- **Violated by**: An orchestrator that dictates exact steps to a subagent and treats any deviation as a failure, even when the subagent has seen that the step cannot work.

### 12. Weigh benefit and harm together, for every move, in the same place.
- **Text**: 是故智者之慮，必雜於利害。雜於利而務可信也，雜於害而患可解也。 — "So the wise person's deliberation always mixes advantage and harm. Mixing in advantage, the task can be relied on. Mixing in harm, the trouble can be resolved." (九變篇 *Variation of Tactics*). With: 故不盡知用兵之害者，則不能盡知用兵之利也。 — "One who does not fully know the harm of using troops cannot fully know its benefit." (作戰篇 *Waging War*)
- **Basis**: RECALLED (from training).
- **Reading**: Merged here: both lines say that benefit and harm are known together or not at all. The second clause of the 九變篇 line is somewhat ambiguous. It can mean "considering advantage even in adversity, you can carry out your aim", or "considering the benefit in your plan, it becomes credible". I give the second reading tentatively.
- **Design rule**: Each node's design names its expected payoff and its specific failure mode, plus how that failure would be noticed, side by side. A node that lists no failure mode is not ready. This is close to the project's sabotage check, which is a resemblance and not support from the text.
- **Violated by**: A design document that lists what each stage will produce and nothing about how each stage could go wrong silently.

### 13. Foreknowledge must come from someone who has actually looked, not from analogy, expectation or calculation.
- **Text**: 故明君賢將，所以動而勝人，成功出於眾者，先知也。先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。 — "What lets the enlightened ruler and the wise general move and conquer, and achieve beyond the ordinary, is foreknowledge. Foreknowledge cannot be got from ghosts and spirits, cannot be inferred by analogy with past events, cannot be verified by calculation of 度; it must be got from people who know the enemy's situation." (用間篇 *Use of Spies*)
- **Basis**: RECALLED (from training).
- **Reading**: The chapter rejects divination, analogy to precedent, and 度. 度 is usually read as astronomical or astrological reckoning. It does not mean measurement in our sense, so this line should not be read as distrust of measurement. What it requires is information from an agent who is actually in contact with the thing. The chapter goes on to the five kinds of spies and to turning the enemy's spies, which implies many sources that are checked against each other.
- **Design rule**: A claim about the current state (a file's contents, a tool's behaviour, an API's availability) counts only if a node actually read or ran it in this run, with the evidence attached. A claim inferred from how similar systems usually behave is marked unverified. Where it matters, it needs a second, independent source.
- **Violated by**: A planning node that asserts what a function does from its name and from the usual convention, without opening the file.

### 14. When a run fails, look at the design before the environment; mismatched strength between workers and controllers has its own failure modes.
- **Text**: 故兵有走者、有弛者、有陷者、有崩者、有亂者、有北者。凡此六者，非天之災，將之過也。……卒強吏弱，曰弛；吏強卒弱，曰陷；……將弱不嚴，教道不明，吏卒無常，陳兵縱橫，曰亂。 — "An army may flee, be slack, sink, collapse, fall into chaos, or be routed. These six are not disasters from Heaven; they are the general's faults. … Strong soldiers with weak officers: slackness. Strong officers with weak soldiers: sinking. … A weak, lax general, unclear instruction, officers and men without fixed roles, troops drawn up every which way: chaos." (地形篇 *Terrain*)
- **Basis**: RECALLED (from training).
- **Reading**: The six failures are placed explicitly on the commander, not on fate. Two of them are about mismatch. Strong troops under weak officers become insubordinate and slack. Strong officers over weak troops push them into collapse. 亂 is caused by unclear instruction and the lack of fixed roles (吏卒無常).
- **Design rule**: A post-mortem first asks which design choice allowed the failure, before it blames the model or the task. Match controller strength to worker strength. An orchestrator or verifier weaker than its workers cannot hold them to a contract. One much stronger than weak workers will push them into tasks they cannot do. Every node has a fixed role. The mapping of 卒/吏 to worker/controller is loose.
- **Violated by**: A cheap, weak verifier set to review the output of a strong coding agent, whose failures are then written off as "model flakiness".

## What I would not claim
- **That Sunzi says "a hundred battles, a hundred victories" (百戰百勝) for knowing yourself and the enemy.** As I recall the text, the 知彼知己 line ends 百戰不殆, "not imperilled". 百戰百勝 does appear in 謀攻篇, but as something that is *not* the best of the best. Popular versions that promise certain victory misstate it. Separately, sayings often credited to Sun Tzu, such as "keep your friends close and your enemies closer" and "opportunities multiply as they are seized", are not in any of the thirteen chapters as I recall them. That is a check from recall, not from the text.
- **That the text is a single author's work from one date, or that my wording matches the earliest version.** Whether a historical Sun Wu wrote it, and when, is disputed. Dates proposed range from the late Spring and Autumn to the Warring States period. The Yinqueshan slips show that an early Han version differed from the received text in places. I quote the received text from memory and cannot say which of my lines have known variants.
- **That 兵者，詭道也 ("war is the way of deception") carries over to agent workflows as a design rule.** The line is real (計篇) and central to the text, but the deception it describes is aimed at an enemy. Inside a cooperative system, deceiving your own agents or your own record destroys the information the design depends on. The line might fit a red-team or adversarial-testing node, but I would not generalise from it.
