# Gate review — why a check that cannot fail is a defect, and the fix

A 孫子兵法 and game-strategy reading of the 13 "gate cannot reject / test could not fail" defects
(`runs/20261004-defect-register.md` §1–§2). Classical lines are quoted only where they appear in the
three permitted notes; each carries its note's Basis label. Where no classical line genuinely applies,
I say so and reason game-theoretically, labelled `(not from a note)`.

---

### 1.1. G3 checks that five field **names** appear, not their contents

- **Principle**: 故善戰者，求之於勢，不責於人，故能擇人而任勢。 — "The skillful commander seeks victory from
  the configuration, not by demanding it of individual men; thus he is able to choose the right people and set
  them in the right configuration." — **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 兵勢第五);
  from `deepseek-v4-pro.md`, principle 5.
- **Why it applies**: `design_gate.py:146` satisfies G3 when the five *strings* `context, contract, evidence,
  state, tools` appear in `five_things`, and it never looks at what is behind them. A bare-name list is not a
  configuration; it is the design saying "the executor will supply its own tools, contract and evidence" — which is
  責於人, demanding the result of the individual at runtime. The principle says the situation must carry the
  leverage, so the gate must verify the configuration has content, not just labels.
- **The change**: At `design_gate.py:146`, require `five_things` to be a mapping, not a list: each of the five
  keys must map to a non-empty value that is not just the key name repeated. Fail with
  `G3: node {id} five_things are labels, not filled: [...]` when the field is a list, when a key is missing, or
  when a value is empty/whitespace/equal to its own name. Extend `--self-test` with a design whose
  `five_things` are the five bare names and expect a G3 finding.
- **Falsified by**: Two designs that differ only in whether `five_things` values are filled producing identical
  run outcomes, which would show the filled-content rule gates nothing that changes behaviour.

### 1.2. No rule for a **baseline**, though every building node's stop requires one

- **Principle**: 昔之善戰者，先為不可勝，以待敵之可勝。不可勝在己，可勝在敵。……故曰：勝可知，而不可為。 —
  "The skillful warriors of old first made themselves impossible to defeat, and then waited for the enemy to
  become defeatable. Being impossible to defeat lies in yourself; being able to defeat the enemy lies in the
  enemy. Hence it is said: victory can be known, but not made." — **Basis**: VERIFIED (source: Chinese
  Wikisource, 孫子兵法, ch. 軍形第四); from `deepseek-v4-pro.md`, principle 4.
- **Why it applies**: The baseline is the recorded pre-build passing state, and it is precisely the 不可勝 half —
  the thing wholly in the designer's control, established *before* any node builds, that lets the stop tell
  progress from damage. `design_gate.py` has no rule that a building design carries one, so a design whose build
  node can only say "my new check passed" and never "nothing that already passed regressed" sails through. The
  principle's order is the fix: the invariant is built first, and the gate must demand it before anything that
  can break it is allowed to run.
- **The change**: After the `building_cats` computation at `design_gate.py:132`, fail with
  `G3: a building design has no baseline — record the pre-build passing check and its output before any node
  builds` when `builds` is true (or any building category is claimed) and `d["baseline"]` is absent or a
  whitespace-only string. Add a `--self-test` case stripping `baseline` from `_good_design` and expecting G3.
- **Falsified by**: A building design on a brand-new surface with nothing to regress (case D — no behavioural
  baseline yet) being correctly approved by a human reviewer yet rejected by the new baseline rule.

### 1.3. No rule for the **three-part stop** itself

- **Principle**: 合於利而動，不合於利而止。 — "Move when it is to your advantage; stop when it is not." (from the
  full line 主不可以怒而興師，將不可以慍而致戰。合於利而動，不合於利而止。怒可以復喜… in ch. 火攻第十二) —
  **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 火攻第十二); from `deepseek-v4-pro.md`, principle 12.
- **Why it applies**: The algorithm promises every building node a three-part stop — the baseline still passes,
  "must not change" holds, and the new checks pass — and 止 is the part of the line the gate is supposed to
  enforce. What the gate actually enforces at `design_gate.py:144` is only that a `check` string is non-empty;
  the *stop* — the condition under which the node is allowed to stop, not merely the thing it must produce — has
  no rule at all. The principle says the stop decision must be made by an explicit, objective condition, so the
  gate must verify the stop exists and has its parts.
- **The change**: In the node loop at `design_gate.py:142`, for any building node (category `product == "yes"`,
  or `"mixed"` when `builds`), require a `stop` object with three non-empty parts — `baseline`, `unchanged`,
  `new` — and fail with `G3: node {id} three-part stop is missing {part}` for each absent or empty part. Add a
  `--self-test` case with a building node whose `stop` omits `unchanged`.
- **Falsified by**: A building design whose change is fully covered by a single fresh acceptance check with no
  pre-existing "must not change" surface being rejected for lacking the three-part stop.

### 1.4. `pattern` and `sabotage` are parsed from every category row and **used 0 times**

- **Principle**: 是故智者之慮，必雜於利害。雜於利而務可信也，雜於害而患可解也。 — with 故不盡知用兵之害者，則不能
  盡知用兵之利也。 — "The wise person's deliberation always mixes advantage and harm... One who does not fully
  know the harm of using troops cannot fully know its benefit." — **Basis**: RECALLED (from training); from
  `claude-opus-5-5.md`, principle 12.
- **Why it applies**: The table's `sabotage` cell is the row's own statement of 害 — "the proof the check can
  fail" (break the code → the check goes red). `parse_types` reads it at `design_gate.py:93` and then the whole
  rest of the file never references it, so the gate has no way to know whether a node's check has ever been shown
  to fail. The principle (the note's own design rule says "a node that lists no failure mode is not ready; this
  is close to the project's sabotage check") is that benefit and harm are known together or not at all: a gate
  that discards the harm half cannot tell a real check from a decoration.
- **The change**: In the node loop, require every node to carry proof its check can fail — either its own
  `sabotage` string or the row's non-empty `sabotage` cell (already in `parse_types`'s output) — and fail with
  `G3: node {id} has no proof its check can fail (no sabotage)` when both are empty. Use the `pattern` cell in
  the loop rule (1.6) and the stop rule (1.3) instead of discarding it. Add a `--self-test` case with a node
  whose row sabotage is empty and which supplies none.
- **Falsified by**: A design whose check demonstrably went red on its first real run (proving it can fail) being
  rejected because it carries no pre-written sabotage string.

### 1.5. G2 takes `builds` and `touched_paths` **from the design itself** — self-referential

- **Principle**: 知彼知己，百戰不殆；不知彼而知己，一勝一負；不知彼不知己，每戰必殆。 — "If you know the other
  side and know yourself, you need not fear the result of a hundred battles; if you know yourself but not the
  other, you will lose one for every one you win; if you know neither, you are endangered in every battle." —
  **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 謀攻第三); from `deepseek-v4-pro.md`, principle 1.
- **Why it applies**: G2's job is "category-vs-facts," but both inputs come out of the same JSON: the design
  declares `builds` and `touched_paths`, and the gate checks those declarations against the categories the *same*
  design declares. It is the 不知彼而知己 case — it knows the design's self-report and nothing about the task's
  actual state — so a self-consistent lie (read-only categories + `builds: false`) passes untouched. The
  principle says the facts (彼) must be modelled independently of the self-description (己), or the verdict is a
  coin flip.
- **The change**: Stop trusting `d["builds"]` and `d["touched_paths"]` as facts. Require the design to carry a
  `facts` record produced outside the JSON (the readiness step's observed paths), and have G2 compare categories
  against `facts`; where feasible cross-check `touched_paths` against the filesystem — fail with
  `G2: builds=true but no touched_paths entry exists on disk` when `builds` is asserted with no existing path,
  and fail when a declared read-only design lists product paths that exist. Add a `--self-test` case with
  `builds: false` + an existing product `touched_paths` entry.
- **Falsified by**: Designs being validated as plans before any file exists, so a filesystem cross-check rejects
  every forward-looking design — meaning the facts must come from the readiness step's record, not from disk at
  gate time.

### 1.6. Loop rules run only if a loop already exists

- **Principle**: 故兵聞拙速，未睹巧之久也。夫兵久而國利者，未之有也。 — with 故兵貴勝，不貴久。 — "In war one
  hears of clumsy speed; one has not seen cleverness that lasts long. There has never been a prolonged war that
  benefited the state... So in war, value victory, not duration." — **Basis**: RECALLED (from training); from
  `claude-opus-5-5.md`, principle 5.
- **Why it applies**: `design_gate.py:150` gates the loop's fields only inside `if lp is not None`, so the gate
  can never reject a node that *should* iterate but carries no loop — the very defect the bound exists to
  prevent. The principle's design rule is blunt about this: "every loop gets a hard cap and a stop condition
  before it starts; if a node has no cap, the design is not finished." The gate currently inverts that
  obligation, treating the loop as optional decoration to be validated when present instead of a required cap to
  be demanded where the pattern calls for iteration.
- **The change**: Drive the loop requirement from the row's `pattern` cell (fixing 1.4 at the same time): when
  the node's category pattern contains "loop" (or the category is a loop-default like `code generation`),
  require `n["loop"]` to be a dict with an int `limit >= 1`, non-empty `exit` and non-empty `feedback`, and fail
  with `G3: node {id} pattern {pattern} requires a bounded loop, but none is present` when it is missing. Keep
  the existing field checks for when a loop is present; derive `corpus_check.py`'s hardcoded `LOOP_CATS` set from
  the same pattern column instead of hand-keeping it.
- **Falsified by**: A pattern's loop being a retry capacity that is legitimately optional for a single-shot,
  fail-fast-to-EJ design, so requiring the loop object rejects designs that correctly decline to iterate.

### 1.7. The check string only has to be non-empty, not executable

- **Principle**: 非利不動，非得不用，非危不戰。 — "Do not move without advantage; do not employ troops without
  obtaining; do not fight unless at risk." (from minimax's merged principle 9, also carrying 合於利而動，不合於利而止) —
  **Basis**: VERIFIED (source: Wikisource 孫子兵法, fetched 2026-10-05); from `minimax-m3.1-flash.md`, principle 9.
- **Why it applies**: The gate accepts `"default check for code generation (TASK_TYPES.md)"` — the string every
  corpus design actually carries — because `design_gate.py:144` only tests non-emptiness. That string names no
  state change and sees none; the note's rule is explicit that "a node must name the state it changes and the
  check that will see the change — a node whose check can pass either way is not a node, it is a ritual." A
  pointer to where the real check *might* be found is exactly a ritual, and the gate must refuse it.
- **The change**: Replace the non-empty test at `design_gate.py:144` with two rules: fail `G3: node {id} has no
  check` on empty, and fail `G3: node {id} check is a pointer to the table, not a check` when the string matches
  the `default check for {category} (TASK_TYPES.md)` template or contains no runnable/observable element (a
  command, a script path, or a named state transition). Require the design to carry the row's real check, not a
  reference to it; add a `--self-test` case using the placeholder string and expect G3.
- **Falsified by**: A plain-English check with no command token ("reviewer finds no open finding") passing a
  human review, showing executability is the wrong test and the right test is whether the check names an
  observable state change.

### 2.1. **Circular**: designs are emitted from the same TASK_TYPES cells the gate parses

- **Principle**: 先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。 — "Foreknowledge cannot be
  obtained from spirits or gods, cannot be obtained by analogy with past events, cannot be obtained by
  measurement or calculation; it must be obtained from people — those who know the enemy's situation." —
  **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 用間第十三); from `deepseek-v4-pro.md`, principle 13.
- **Why it applies**: `corpus_check.py:build_design` builds every design from `ENGINES` and `FIVE`, both parsed
  from `docs/TASK_TYPES.md` — the same file `design_gate.py` parses. The "0 bugs in 300 designs" is therefore
  驗於度: a number obtained by calculation from the table's agreement with itself, never 取於人, an observation of
  a design someone produced independently. The principle forbids exactly this as evidence: a pass only counts
  when the thing being checked came from a source that did not share the checker's input.
- **The change**: In `corpus_check.py`, stop reporting table-synthesized designs as "bugs: 0." Keep `build_design`
  only as an explicit self-consistency check of the harness, and gate a separate corpus of independently produced
  designs — the engines' actual classifier outputs rendered into full designs, plus hand-authored good and bad
  ones — against `validate_design`. The test's headline "0 bugs" must come from that independent corpus, not from
  the machinery run.
- **Falsified by**: Independently produced designs passing the gate at the same rate as table-derived ones,
  showing the circularity was not inflating the result and the corpus source was not the problem.

### 2.2. All 300 designs are `design_source: "default"`, so G5 and G7 never execute

- **Principle**: 凡戰者，以正合，以奇勝。 — "In battle, engage with the direct; win with the indirect." —
  **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 兵勢第五); from `deepseek-v4-pro.md`, principle 6.
- **Why it applies**: The 20% challenger rule is the algorithm's 奇 — a bounded, deliberately different share that
  exists to test whether the default (正) is still right. `build_design` hard-codes `design_source: "default"`
  (`corpus_check.py:111`), so the corpus runs the orthodox path 300 times and never once exercises the
  alternative; G5 and G7 are dead code, and the rule that was meant to keep the default honest is itself never
  tested. The principle says the two are held together: a force that only ever fights 正 has no 奇, and a test
  that only ever runs the default has never proven the challenger path works.
- **The change**: Add challenger fixtures to the corpus — designs with
  `design_source: {"type":"challenger", "claim_margin":…, "basis":…}` plus `estimate`/`default_estimate` and
  `coverage`/`default_coverage` — and a `--ledger`/`--ledger-row` invocation over `docs/TASK_TYPES_LEDGER.md`.
  Assert the run actually produces at least one G5 finding on a planted-bad challenger (claim < 0.20, margin
  arithmetic lie, coverage not equal) and one G7 finding on a bad row, so the challenger and ledger paths are
  proven to execute and to reject.
- **Falsified by**: Running challenger cases and finding the G5/G7 rules already fire correctly on the first
  try, showing the path was dead code but not a correctness hole.

### 2.3. No mutation/negative controls: the test has never rejected anything

- **Principle**: 故用兵之法，無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。 — "In war, do not rely on
  the enemy not coming; rely on being ready for him. Do not rely on the enemy not attacking; rely on holding a
  position that cannot be attacked." — **Basis**: VERIFIED (source: Chinese Wikisource, 孫子兵法, ch. 九變第八);
  from `deepseek-v4-pro.md`, principle 11.
- **Why it applies**: The test's unstated premise is "the gate will reject a bad design" — and it rests that
  premise on the bad design *never arriving* (無恃其不來), because nothing ever plants one. A gate whose
  reject-power has never been observed is indistinguishable from a gate that cannot reject; the principle forbids
  resting the whole claim on the failure's non-arrival and requires instead 有以待之 — a demonstration, in hand,
  that the position actually stops an attack.
- **The change**: Add the mutation run (the register's own "cheapest decisive step") to `design_gate.py
  --self-test` and to the corpus: take the passing `_good_design` and apply each of the 13 defects from §1–§2
  (bare five_things, missing baseline, missing stop part, no sabotage, self-contradictory builds, missing loop,
  placeholder check, wrong category, same-kind reviewer, bad margin) and assert a finding for every mutation; the
  run fails if any planted defect passes. This is the control that makes every rule in 1.1–1.7 falsifiable at
  all.
- **Falsified by**: A mutation run that plants every known defect and finds the gate rejects each, showing the
  gate could always reject and the missing controls were merely unrecorded, not a real failure.

### 2.4. The checklist review layer — the semantic layer the file says catches what the script cannot — never ran

- **Principle**: 故備前則後寡，備後則前寡，備左則右寡，備右則左寡，無所不備，則無所不寡。 — "Guard the front and
  the rear is thin; guard the rear and the front is thin; guard the left and the right is thin; guard the right
  and the left is thin. Guard everywhere, and everywhere is thin." — **Basis**: RECALLED (from training); from
  `claude-opus-5-5.md`, principle 9.
- **Why it applies**: The note's rule has two halves: concentrate on a few checks, *and write down the risks the
  design deliberately leaves unchecked*. The algorithm did the second half honestly — `TASK_TYPES.md:284` names
  the recheck-verb class and writes "the script gate cannot see this; the checklist layer exists for exactly this
  class" — but the layer then never ran. A risk written down and pointed at a guard that never fires is not
  covered; it is papered over, which is the thin-everywhere failure wearing the costume of a declared division of
  labour. The declaration substituted for the guard.
- **The change**: This is not a `design_gate.py` edit and should not be faked as one — the second layer is
  judgment by design. The change is to the harness: add a checklist pass to the corpus/validation pipeline that
  actually invokes the Sonnet 5.5 fixed-checklist reviewer on a sample including the recheck-verb class, records
  its verdicts, and fails the run if the layer never executes. A gate cannot see this class; only running the
  layer proves the class is guarded.
- **Falsified by**: Running the checklist layer and finding it produces no verdict that changes any design,
  showing the semantic layer was decorative and skipping it cost nothing.

### 2.5. The reported accuracies had no denominator (codex's 90% drops r1, which mismatched 25 of 25)

- **Principle**: 兵者，詭道也。…故兵以詐立，以利動，以分合為變者也。 — "War is the way of deception... In war the
  army stands on deception, moves on advantage, and takes its variation in splitting and joining." — **Basis**:
  VERIFIED (source: Wikisource 孫子兵法, fetched 2026-10-05); from `minimax-m3.1-flash.md`, principle 4.
- **Why it applies**: I use this line only as its own boundary, which the note itself draws: `minimax-m3.1-flash.md`
  flags that hiding state from your own side is "abusing the line rather than obeying it," and `claude-opus-5-5.md`
  "What I would not claim" says deception turned on one's own record "destroys the information the design depends
  on." Dropping r1 to report 90% is 詐 aimed at the project's own test log — the exact record whose whole purpose
  (the ledger, the n-count) is honest reconciliation. The principle applies as its negation: deception is for the
  enemy, never for your own ledger.
- **The change**: In `corpus_check.py`'s reporting (the `agree/total` lines at 213–214 and any summary), report
  every round's denominator and the combined `sum(agree)/sum(total)` over all three rounds, never a subset; add an
  assertion that any emitted accuracy carries a denominator equal to the count of classified prompts across all
  rounds, and fail the run if a round is omitted. The number must cover the rounds it claims to cover.
- **Falsified by**: Recomputing the accuracy with r1 included and finding the corrected number would not have
  changed any decision, showing the dropped round was noise rather than a disguised failure.

### 2.6. Sabotage and the pattern column are never exercised by the corpus run

- **Principle**: 先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。 — "Foreknowledge cannot be
  obtained from spirits or gods, cannot be obtained by analogy with past events, cannot be obtained by
  measurement or calculation; it must be obtained from people — those who know the enemy's situation." —
  **Basis**: RECALLED (from training); from `claude-opus-5-5.md`, principle 13.
- **Why it applies**: The corpus never runs a sabotage, so the claim "this check can fail" is carried as an
  inference from the table's promise, never as an observation of a check actually going red — the note's rule says
  a claim about current state "counts only if a node actually read or ran it in this run, with the evidence
  attached." The same holds for `pattern`: the corpus never confronts a design with the structural template its
  row names, so conformance is assumed, not observed. The note's discipline is the fix: run the planted defect
  and watch the check fail, or the proof is not evidence.
- **The change**: Add sabotage fixtures to the corpus — for each exercised category, one design where the planted
  defect from the row's sabotage cell is applied and the check must go red — and assert at least one red result
  per category; add pattern-conformance cases that verify a design's structure matches its row's pattern. Couple
  this with the 1.4/1.6 gate edits so the gate actually consumes the `sabotage` and `pattern` cells being
  exercised.
- **Falsified by**: The sabotage cases all producing green (the planted defect never turns the check red), which
  would show the checks themselves cannot fail and that the exercise is what exposes the real defect.

## Where the analogy breaks

1. **There is no enemy.** Every line above is written for a campaign against an opponent with independent will,
   whose plans you attack and whose openings you must wait for. A script validating JSON has no adversary: "the
   gate cannot reject" is not a defeat inflicted by a clever enemy, it is the absence of a mechanism in the
   designer's own table. The half of the text that points at the opponent — 可勝在敵, 因敵變化, 知敵之情 — has no
   counterpart here, and I have not pretended it does.
2. **The budget is not scarce in Sunzi's sense.** 備前則後寡 is a claim about a finite army being spread thin; its
   force comes from men and supplies that genuinely run out. A deterministic script can add checks for almost
   nothing, so the real cost of the fixes above is not soldiers but *designer attention and false-positive rate*:
   every new rule must be exactly right or it rejects good designs. That is why the register's mutation run
   matters more than adding all thirteen rules at once — the binding constraint is correctness, not capacity, and
   Sunzi does not speak to that.
3. **The deception line must be read backwards here.** 兵者，詭道也 is central to the text and aimed outward at an
   enemy; the notes themselves refuse to import it into a cooperative system. The only defects where it appears
   in this review (2.5, and the self-referential 1.5/2.1 by extension) are cases of the system deceiving *itself*,
   which is exactly the use the notes say is an abuse. I cite it as a boundary, not as a transferable rule.

## The one change

If only one of the thirteen could be made, it is the mutation run — defect 2.3. Every fix in 1.1–1.7 is a
*claim* about what the gate should reject, and until a planted-bad design is put through the gate and observed to
fail, none of those claims is falsifiable and the gate's reject-power is still an inference from a table that
agrees with itself. The mutation run is also the cheapest decisive step — it costs no model calls — and it
converts the whole "gate cannot reject" family from assertion into measurement, after which the surviving rules
can be added one at a time against a control that is known to work.
