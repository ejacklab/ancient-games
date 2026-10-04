# 孫子兵法 — deepseek-v4-pro

Source note: every Chinese line below marked VERIFIED was copied from the full received text at Chinese
Wikisource (zh.wikisource.org/wiki/孫子兵法), which I read in full today, and cross-checked in sense against
Lionel Giles's 1910 translation (Project Gutenberg ebook #132). Chapter names are the standard English ones.
English renderings are my own.

### 1. Know the other side and know yourself
- **Text**: 知彼知己，百戰不殆；不知彼而知己，一勝一負；不知彼不知己，每戰必殆。 — "If you know the other side
  and know yourself, you need not fear the result of a hundred battles; if you know yourself but not the other,
  you will lose one for every one you win; if you know neither, you are endangered in every battle." (Ch. 3,
  Attack by Stratagem)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 謀攻第三)
- **Reading**: Two distinct objects of knowledge are named: the enemy (the situation, the problem) and oneself
  (one's own forces and state). The line is not about omniscience; it is about knowing your own side as hard as
  you know the opponent, and the two knowledge claims are treated as separately necessary.
- **Design rule**: A workflow must model two things with equal care — the task (its real difficulty, inputs,
  and failure modes) and the team's own actual capabilities and state. Do not let either model be assumed.
- **Violated by**: A plan that is written entirely from the task's point of view while the agents' real
  capabilities, quotas, and tool limits are never written down.

### 2. Estimate more and you win; estimate less and you lose
- **Text**: 夫未戰而廟算勝者，得算多也；未戰而廟算不勝者，得算少也。多算勝，少算不勝，而況於無算乎？ — "The side
  that wins has made many calculations in the temple before battle; the side that loses has made few. Many
  calculations, victory; few calculations, defeat — how much more so with none at all?" (Ch. 1, Laying Plans)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 始計第一)
- **Reading**: 廟算 is the pre-campaign reckoning done in the ancestral temple — counting the factors in your
  favour against the enemy's. The claim is comparative and quantitative: the side with the larger pre-committed
  reckoning wins; the side that skips it loses. 算 (counting, tallying) is the operative image.
- **Design rule**: Spend visible effort on up-front estimation and design before committing resources, and let
  the amount of unresolved-unknown accounting be a go/no-go input, not decoration.
- **Violated by**: Dispatching agents on a task whose inputs, acceptance criteria, and failure modes were never
  enumerated, on the assumption that the agents will sort it out.

### 3. Attack the plan, not the force
- **Text**: 是故百戰百勝，非善之善者也；不戰而屈人之兵，善之善者也。故上兵伐謀，其次伐交，其次伐兵，其下攻城。 —
  "To win a hundred victories in a hundred battles is not the acme of skill; to subdue the enemy's army without
  fighting is. The best strategy is to attack the enemy's plans; next, his alliances; next, his army; and worst,
  to lay siege to his cities." (Ch. 3, Attack by Stratagem)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 謀攻第三)
- **Reading**: A ranking of targets by leverage: plans, then alliances, then forces, then fortified positions.
  The higher up the causal chain you intervene, the cheaper the victory. The claim is about cost and leverage,
  not about a moral preference for avoiding conflict.
- **Design rule**: Intervene at the highest-leverage layer available — catch a mistake in the plan or the
  requirements before it becomes running code or a dispatched agent. Prefer killing a bad plan over repairing
  its execution.
- **Violated by**: Letting a flawed plan proceed to execution and then spending many agents' effort patching the
  downstream damage instead of stopping and reworking the plan.

### 4. First make yourself impossible to defeat, then wait for an opening
- **Text**: 昔之善戰者，先為不可勝，以待敵之可勝。不可勝在己，可勝在敵。……故曰：勝可知，而不可為。 — "The skillful
  warriors of old first made themselves impossible to defeat, and then waited for the enemy to become defeatable.
  Being impossible to defeat lies in yourself; being able to defeat the enemy lies in the enemy. Hence it is said:
  victory can be known, but not made." (Ch. 4, Tactical Dispositions)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 軍形第四)
- **Reading**: Two different things are separated: not losing, which is under your control, and winning, which
  depends on the opponent. The text is explicit that you can engineer your own un-loseable position but cannot
  force a win; 勝可知，而不可為 is genuinely ambiguous between "victory can be foreseen but not manufactured" and
  "one may know how to win without being able to do it", and both readings point the same way — success is not
  fully in the planner's hands.
- **Design rule**: Build the defensive invariants first — idempotency, state that cannot be corrupted, bounded
  retries, verification gates — so the worst outcome is "no progress", never "damage". Treat guaranteed success
  as unknowable; guarantee the absence of certain classes of failure instead.
- **Violated by**: A workflow that optimizes for the happy path and has no guard against corrupting the shared
  state or a prior artifact when a step fails midway.

### 5. Seek the configuration, not the person
- **Text**: 故善戰者，求之於勢，不責於人，故能擇人而任勢。 — "The skillful commander seeks victory from the
  configuration, not by demanding it of individual men; thus he is able to choose the right people and set them
  in the right configuration." (Ch. 5, Energy)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 兵勢第五)
- **Reading**: 勢 (configuration, positional advantage, momentum) is the text's central term for the leverage that
  comes from how things are arranged, not from individual effort. The commander's job is to arrange, not to
  exhort; the same people placed differently perform differently.
- **Design rule**: When a run fails, first ask what the workflow structure — ordering, parallelism, handoffs,
  incentives, information flow — made likely, and change that; only after that ask whether an agent erred.
  Design structure so that correct behaviour is the path of least resistance.
- **Violated by**: Blaming and swapping an agent when the graph, the prompt, or the check that produced the
  failure is what actually needs to change.

### 6. Engage with the direct path, win with the indirect one
- **Text**: 凡戰者，以正合，以奇勝。 — "In battle, engage with the direct; win with the indirect." (Ch. 5, Energy)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 兵勢第五)
- **Reading**: 正 and 奇 are a pair — the orthodox/direct and the unorthodox/indirect. 奇 is genuinely ambiguous:
  it covers surprise, the unexpected, and the non-obvious alternative, not merely "novelty for its own sake".
  The two are held together, not opposed: the direct approach fixes the engagement, the indirect approach
  produces the win.
- **Design rule**: Give every workflow a standard, boring, reliable path that keeps things moving, and
  separately provision at least one non-obvious alternative for when the standard path stalls. Do not bet the
  whole run on a single approach.
- **Violated by**: A single-method pipeline with no alternative route, so one blocked step stalls the entire
  run instead of diverting to a different method.

### 7. Impose your structure; do not have it imposed on you
- **Text**: 故善戰者，致人而不致於人。 — "The skillful combatant moves the other and is not moved by him."
  (Ch. 6, Weak Points and Strong)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 虛實第六)
- **Reading**: 致 means to draw or bring about — the skilled party causes the other to come and act on his terms.
  The emphasis is on retaining the initiative: deciding the time and place of engagement rather than reacting.
  It can be read as "impose" or as the softer "lure"; both are about who sets the agenda.
- **Design rule**: The workflow should set the agenda — its own sequence, its own checkpoints, its own stop
  conditions — rather than letting whichever events or agent outputs arrive first dictate what happens next.
- **Violated by**: A coordinator that reacts to every incoming message in arrival order, so the loudest or
  earliest event sets the direction instead of the plan.

### 8. Prepare everywhere and you are weak everywhere
- **Text**: 故備前則後寡，備後則前寡，備左則右寡，備右則左寡，無所不備，則無所不寡。 — "If you prepare for the
  front, your rear is thin; if for the rear, your front is thin; if for the left, your right is thin; if for
  the right, your left is thin. Prepare everywhere, and you are thin everywhere." (Ch. 6, Weak Points and Strong)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 虛實第六)
- **Reading**: Resources devoted to one point are by definition not at another, so trying to cover every point
  equally means covering none adequately. The line is about concentrating force on the points that matter rather
  than distributing it evenly.
- **Design rule**: Concentrate verification and agent effort on the few outcomes or steps that actually decide
  correctness; do not apply uniform checking to every output. Rank the risks and spend accordingly.
- **Violated by**: A design that runs every artifact through the same heavy verification regardless of its
  consequence, wasting the budget on low-stakes items and leaving the high-stakes ones under-checked.

### 9. No fixed form; adapt like water
- **Text**: 夫兵形象水，水之行，避高而趨下；兵之勝，避實而擊虛。水因地而制行，兵因敵而制勝。故兵無成勢，無恒形，能因敵
  變化而取勝者，謂之神。 — "An army's shape is like water: water avoids the high and runs to the low; victory
  avoids the strong and strikes the weak. Water shapes its course to the ground; an army shapes its victory to
  the enemy. Thus an army has no fixed disposition and no constant form; one who wins by changing with the enemy
  is called spirit-like." (Ch. 6, Weak Points and Strong)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 虛實第六)
- **Reading**: The comparison is precise: water does not decide its shape in advance but takes it from the
  ground, and an army should take its form from the enemy's actual disposition. The principle is adaptation to
  measured reality, not aimless flexibility; the adapting agent still has a goal (running downhill, striking the
  weak).
- **Design rule**: Let the workflow branch on what is actually observed at runtime — measured difficulty,
  verification results, remaining budget — rather than fixing the entire graph up front. Keep the goal fixed and
  the shape variable.
- **Violated by**: A fully pre-specified graph with no conditional branches, which keeps executing its script
  after the situation it was written for has changed.

### 10. The circuitous route is the direct route
- **Text**: 軍爭之難者，以迂為直，以患為利。 — "The difficulty of maneuvering lies in making the circuitous route
  direct, and turning misfortune into advantage." (Ch. 7, Maneuvering)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 軍爭第七)
- **Reading**: 迂 (the roundabout way) and 直 (the straight way) are treated as convertible, not opposed: the
  longer path that avoids resistance arrives first. Likewise a present hardship can be the means to an advantage.
- **Design rule**: Prefer the path that looks longer but is reliable — the extra verification step, the
  explicit intermediate artifact, the checkpoint — over the shorter path that keeps hitting resistance and being
  redone. Count total time to a correct result, not apparent directness.
- **Violated by**: Skipping the intermediate check or artifact to "save time", then spending more total time on
  rework than the check would have cost.

### 11. Prepare for what you hope will not happen
- **Text**: 故用兵之法，無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。 — "In war, do not rely on the
  enemy not coming; rely on being ready for him. Do not rely on the enemy not attacking; rely on holding a
  position that cannot be attacked." (Ch. 8, Variation in Tactics)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 九變第八)
- **Reading**: The text forbids resting a plan on the hope that the bad event will simply not occur. Readiness
  is the only permitted basis: either you are prepared to receive the event, or you have made it impossible or
  harmless. Hope is explicitly ruled out as a planning premise.
- **Design rule**: Assume each dependency can fail and each agent can err, and design the failure path rather
  than hoping it will not happen. Every premise of the form "X will not fail" must be replaced by "here is what
  happens when X fails".
- **Violated by**: A workflow with an unhandled single point of failure (one agent, one service, one file) that
  is simply assumed to succeed.

### 12. Act only on advantage, and know when to stop
- **Text**: 主不可以怒而興師，將不可以慍而致戰。合於利而動，不合於利而止。怒可以復喜，慍可以復悅，亡國不可以復存，
  死者不可以復生。 — "A ruler must not raise an army in anger; a general must not join battle in resentment.
  Move when it is to your advantage; stop when it is not. Anger can turn back to joy and resentment to
  contentment, but a destroyed state cannot be restored, and the dead cannot come back to life." (Ch. 12,
  The Attack by Fire)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 火攻第十二)
- **Reading**: The ground for acting is advantage (利), never an emotional state, and the same test applies to
  stopping as to starting. The argument for restraint is irreversibility: the losses you take while acting from
  anger cannot be undone. The same chapter states the threshold compactly as 非利不動，非得不用，非危不戰 ("do not
  move unless advantageous, do not commit unless there is gain, do not fight unless critical").
- **Design rule**: Give every loop and every run an explicit, objective stop condition, and let the decision to
  stop be made by that condition, not by sunk cost, impatience, or frustration. The mapping to agent orchestration
  is close: loops and retries are where emotion-in-costume usually hides.
- **Violated by**: A retry loop whose only exit is "a human got tired" or "the budget ran out", with no
  objective "we are no longer gaining" condition to stop on.

### 13. Foreknowledge must come from people who know, not from divination
- **Text**: 先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。 — "Foreknowledge cannot be
  obtained from spirits or gods, cannot be obtained by analogy with past events, cannot be obtained by
  measurement or calculation; it must be obtained from people — those who know the enemy's situation." (Ch. 13,
  The Use of Spies)
- **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 用間第十三)
- **Reading**: Three sources of supposed knowledge are ruled out one by one — the supernatural, analogy to
  precedent, and a priori calculation — in favour of a single admissible source: people who have observed the
  actual situation. The text is, unusually, an explicit statement of evidence discipline.
- **Design rule**: Ground claims about the task or the world in an actual observation or a read source, not in
  a model's prior, an analogy, or an estimate. Where a claim cannot be traced to something actually observed,
  label it as such and treat it as untrusted input.
- **Violated by**: A workflow that accepts an agent's confident unverified assertion as fact and passes it to
  the next step as if it had been checked.

## What I would not claim
- That "all warfare is based on deception" (兵者，詭道也) transfers into a rule for honest agent teams. The line is
  in the text (Ch. 1), but it is about deceiving an adversary on a battlefield. I would not claim it licenses
  misleading one's own agents or one's users, and I would not import it as a workflow principle.
- That Sun Tzu is a pacifist because of 不戰而屈人之兵. "Subdue the enemy without fighting" is a claim about
  winning at lower cost, not a preference for not winning. Treating it as a moral preference for peace overstates
  the text.
- That the popular maxims "Opportunities multiply as they are seized", "Strategy without tactics is the slowest
  route to victory; tactics without strategy is the noise before defeat", and "Every battle is won before it is
  fought" are Sun Tzu. I cannot find the first two anywhere in the received text I read; the closest thing to the
  third is 勝兵先勝而後求戰 (Ch. 4), which says something narrower. Treat these as unattributable.
