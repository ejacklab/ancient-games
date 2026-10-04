# Gate review through 孫子兵法 — claude-opus-5-5

Scope: register §1 (1.1–1.7) and §2 (2.1–2.6). Classical lines are quoted only from the three notes in this folder,
each with that note's Basis label. Game-theoretic reasoning that is not from a note is marked `(not from a note)`.

**How the gate's behaviour was established.** I read `design_gate.py` in full. I could not run Python in this
session (permission denied), so every claim below about what the gate passes is **read from the code, not run**.
Each one can be checked with a few lines that call `validate_design` directly.

## The finding, plainly

I agree with the register, with one qualification. The gate does reject things. Its self-test has 13 negative cases,
and run 2 produced 2 real findings. What it rejects is **a wrong label or a broken graph**: an unknown category, a
cycle, a same-kind reviewer, a challenger margin under 20%. What it cannot reject is **a design that has the outward
form of every promise and none of the content**. And the 300-design run never gave it one of those to try.

The notes make one distinction that says what a check is for. 「不可勝在己，可勝在敵」 — "the unbeatable lies with
oneself; the beatable lies with the enemy" (minimax, VERIFIED; deepseek, VERIFIED). A script gate cannot judge
whether a design will succeed, because that half lies with the task. It **can** judge whether the designer has done
everything that was in the designer's power before dispatch: a stated stop, a recorded baseline, a check that can run,
a named way to make that check fail. Those are exactly the things this gate does not look at. A check exists so that
「不合於利而止」 — "stop when it does not accord with advantage" (deepseek, VERIFIED) — can actually happen. Its whole
value is in the designs it can halt.

---

### 1.1. G3 accepts the five names with nothing behind them
- **Principle**: 「是故方馬埋輪，未足恃也；齊勇如一，政之道也」 — "to harness the horses and bury the wheels is not yet
  to be relied on; to make their courage uniform as one is the way of good government." Design rule: "commit a node
  by its contract and its check, not by a paragraph of rationale. The integration lives in the interface, not in the
  briefing." — minimax-m3.1-flash #13, **VERIFIED**.
- **Why it applies**: Tethering the horses and burying the wheels is a visible sign of commitment, and the text says
  plainly that it cannot be relied on. The list `["context","contract","evidence","state","tools"]` is the same kind of
  sign. It shows the designer knows the five words, and nothing about whether any node can run, be checked, or be
  resumed. The note puts integration in the interface. The method says the same: an edge is "the earlier node's
  *returns* and *evidence* becoming the later node's context". The gate checks `needs` and never checks that interface.
- **The change**: In G3, reject `five_things` when it is a list (finding: "five_things is a list of names; give each
  one its content"). Require an object with: `tools` (a non-empty list); `context.given` (a non-empty list) and
  `context.withheld` (the key must exist, the list may be empty); `contract.intent`, `contract.stop`, `contract.output`
  and `contract.must_not_change` (each non-empty); `evidence.file` (a path); and `state.reads` and `state.writes`
  (each non-empty). Add an edge rule (G4): for every `dep` in `node.needs`, `nodes[dep].five_things.evidence.file`
  must appear in `node.five_things.context.given`. If it does not, the finding is "edge {dep}→{id} carries no
  evidence into context".
- **Falsified by**: Designs that pass the structured rule fail at run time for missing context, or at a join, as often
  as list-form designs did. That would mean the content can be faked as cheaply as the names.

### 1.2. No baseline rule, though part 2 of every building node's stop is the baseline
- **Principle**: 「不可勝在己，可勝在敵。……勝兵先勝而後求戰，敗兵先戰而後求勝。」 — "The unbeatable lies with oneself;
  the beatable lies with the enemy. … The army that wins makes its victory first and then seeks the battle." Design
  rule: "A workflow may guarantee that evidence was gathered, that the check ran, and that the loop stopped; it may
  not guarantee the conclusion." — minimax-m3.1-flash #8, **VERIFIED** (the same line is deepseek #4, VERIFIED).
- **Why it applies**: "What passed before still passes" is the 不可勝 half of a building run. It is not losing ground
  you already held, and it is the one outcome fully in the designer's control. It also has to be secured **before**
  the engagement (先勝而後求戰), since a baseline taken after the first build is a record of the damage. The gate has
  no field for it, so a design can promise the three-part stop while holding nothing that part 2 could be measured
  against.
- **The change**: New rule G9. When `builders` (as G6 already computes them) is non-empty, the design must carry
  `baseline: {command, record_to, if_red}`:
  - `command` must be non-empty and not a placeholder (the same placeholder test as 1.7);
  - `record_to` must be a state-file path;
  - `if_red` must be `"stop"` or `"carry"`. With `"carry"`, `baseline.known_failing` must be a non-empty list.
    This gives register 5.1's open question a forced answer at design time.

  Add a `--pre-dispatch STATE` mode that fails unless `record_to` exists and contains the command, an exit code and
  output. That mode runs after the baseline is recorded and before the first building node starts.
- **Falsified by**: Across the next several building runs, part 2 of the stop never catches a regression, and no
  `if_red` branch is ever taken. In that case the baseline is cost without effect at this project's scale.

### 1.3. No rule for the three-part stop
- **Principle**: 「合於利而動，不合於利而止。」 — "Move when it is to your advantage; stop when it is not." Design rule:
  "Give every loop and every run an explicit, objective stop condition, and let the decision to stop be made by that
  condition, not by sunk cost, impatience, or frustration." — deepseek-v4-pro #12, **VERIFIED**.
- **Why it applies**: The line treats stopping as an action with its own test, equal to starting. In this method, that
  test for a building node is the three-part stop, and it is what lets a run end (method 3.6: "This is what lets a run
  end"). The gate checks that a loop has a `limit` and an `exit`, which say when to give up. It never checks that a
  node says when it has **succeeded**, so a building design that passes the gate has no objective way to finish.
- **The change**: In G3, every builder must carry `contract.stop` as an object:
  - `criteria`: a non-empty list, each id matching `^[RN]\d+\.\d+$`;
  - `baseline`: must equal `true`, and the design must carry G9's `baseline`;
  - `must_not_change`: non-empty.

  The design must carry `criteria_in_scope`, and the union of the builders' `stop.criteria` must include every id in
  it (finding: "criterion {id} is in scope but no building node covers it"). A non-builder that carries
  `stop.criteria` is a finding. A blueprint piece uses `proposes` instead. When a builder's `check.kind` is
  `"checklist"`, its items must be exactly the three parts. Method 3.6 says a judged stop "is a fixed checklist of
  those three parts, never an open-ended review."
- **Falsified by**: Building runs whose designs pass this rule still fail to end, with reviewers still finding "more
  to do" that the backlog rule should have absorbed. That would mean the stop was stated correctly and the leak is
  somewhere else.

### 1.4. The `pattern` column is parsed and never used
(The `sabotage` half of this defect is answered under 2.6, so it is not repeated here.)
- **Principle**: 「凡戰者，以正合，以奇勝。」 — "In battle, engage with the direct; win with the indirect." Reading: "the
  direct approach fixes the engagement, the indirect approach produces the win." — deepseek-v4-pro #6, **VERIFIED**.
- **Why it applies**: The default-first rule maps onto 正 and 奇. The category's default pattern is the 正. A challenger
  is a declared 奇, and it is held to the 20% rule. G5 polices only a design that **calls itself** a challenger.
  Every design reaches the gate with `design_source: "default"` and a node shape the gate never compares with the
  pattern. So a design can depart from the 正 and still claim to be it, and that 奇 escapes the challenger rule
  entirely. 正 and 奇 are only distinct if someone checks which one is in front of them.
- **The change**: New rule G10, which runs only when `design_source == "default"`. For each node, read its category's
  `pattern` cell and require the shape it names:
  - the pattern contains `loop` (code generation, ui/ux dev, debugging, test script gen): the node has `loop`;
  - the pattern contains `+ review` or `review against source`: some `code review` node lists this node in `reviews`;
  - the pattern contains `human acceptance checkpoint`: a node with `engine` matching `EJ` `needs` this node;
  - the pattern contains `single node`: the category appears on exactly one non-review node.

  A mismatch gives the finding "default design departs from the {category} pattern — declare it a challenger". Keep
  the pattern-to-shape map as a constant in the gate, and make `--self-test` fail if any category's pattern string
  matches no key, so that a new table row cannot slip past the rule.
- **Falsified by**: Real designs labelled `default` trip G10 mostly on wording, with legitimate shapes the map does
  not cover, rather than on undeclared departures. That would mean the pattern column is prose, not a specification
  a script can read.

### 1.5. G2 believes the design's own `builds` and `touched_paths`
- **Principle**: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」 — "Foreknowledge cannot be
  obtained from spirits or gods, cannot be obtained by analogy with past events, …; it must be obtained from people —
  those who know the enemy's situation." — deepseek-v4-pro #13, **VERIFIED**. With claude-opus-5-5 #13's reading
  (**RECALLED**): the chapter "implies many sources that are checked against each other."
- **Why it applies**: G2 is the gate's guard against a wrong category. It decides whether the design builds by asking
  the design. Read from the code: a design with categories `["research and reports", "debugging"]`,
  `builds: false`, no `touched_paths` and a debugging node with **no reviewer** passes clean. `debugging` is
  `mixed`, so with `builds` false it is not counted as a builder, and G6 never fires. The text's requirement is a
  second source that has actually looked. Here no second source exists, so the gate only confirms what the design
  already said. I lean on 必取於人 and 不可象於事 only. The notes disagree on 度 (claude #13 reads it as astrological
  reckoning, deepseek as "measurement or calculation"). On deepseek's reading the line would rule out the gate itself
  as a source of foreknowledge, and I do not want to rest the change on a word the notes contest.
- **The change**: In G2, stop reading `builds` as given:
  - compute `builds_effective = builds or any(node.five_things.contract.may_change)`, plus any node whose category
    has `product == "yes"`;
  - require `touched_paths` to equal the union of the nodes' `may_change`;
  - a mismatch in either is a finding: "the design says builds={builds} but node scopes say otherwise";
  - every `mixed`-category node in a design that does not build must set `contract.must_not_change` to `["*"]`, so
    that read-only is stated where a reviewer will hold the node to it, not only in a top-level boolean;
  - with `--repo PATH`, every `touched_paths` entry must exist under the repo or appear in `new_paths`.
- **Falsified by**: Designs where the derived and declared `builds` disagree turn out, on inspection, to be right in
  their declared value most of the time. That would mean the node scopes are the less reliable witness.

### 1.6. Nothing is checked about failure unless a loop exists
- **Principle**: 「故用兵之法，無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。」 — "do not rely on the enemy not
  coming; rely on being ready for him." Design rule: "Every premise of the form 'X will not fail' must be replaced by
  'here is what happens when X fails'." — deepseek-v4-pro #11, **VERIFIED**.
- **Why it applies**: G3's loop rules are about what happens when a check fails. They run only if the designer chose
  to write a `loop`. Read from the code: delete the `loop` from `_good_design()`'s code-generation node and the
  design passes clean. A node with a check and no failure path rests on exactly the premise the text forbids, that
  the check will pass the first time. The gate should ask about failure on every node that has a check, not only on
  the nodes where the designer already thought of it.
- **The change**: In G3, every node with a check must carry either `loop` (the existing limit, exit and feedback rules
  apply) or `on_fail: {action: "stop" | "replan", report_to}`. If it has neither, the finding is "node {id} does not
  say what happens when its check fails". Also give `limit` an upper bound: it must be at most `design.max_attempts`,
  and `max_attempts` is required when any loop exists. Today a limit of 10⁹ passes. 「兵貴勝，不貴久」 ("war values
  victory, not duration", minimax #3, **VERIFIED**) is the reason a bound with no ceiling is not a bound.
- **Falsified by**: In real runs, nodes that declared `on_fail: stop` behave no differently on failure from nodes that
  declared nothing. That would mean the field is read by no one and the rule is paperwork.

### 1.7. A check only has to be a non-empty string
- **Principle**: 「非利不動，非得不用，非危不戰。」 — "Do not move without advantage; do not employ troops without
  obtaining." Design rule: "Every node in a design must name the state it changes and the check that will see the
  change. … A node whose check can pass either way is not a node, it is a ritual." — minimax-m3.1-flash #9,
  **VERIFIED**.
- **Why it applies**: Every check in the 300 designs is `"default check for <category> (TASK_TYPES.md)"`. Read from
  the code, `"."` would pass as well. Such a string cannot fail, because nothing executes it and nothing defines what
  "pass" means. By the note's rule, every one of those nodes is a ritual. The gate certified 300 designs made of
  rituals.
- **The change**: In G3, `check` must be an object `{kind, command | items, pass_when}`:
  - `kind` is one of `script`, `checklist`, `owner`;
  - `script`: `command` is non-empty, its first token resolves (`shutil.which`, or a path that exists under
    `--repo`), and `pass_when` names an exit code or an output pattern;
  - `checklist`: `items` is a non-empty list of yes/no questions;
  - a category whose table check is marked `(script)` must use `kind: script`;
  - reject any check whose text matches `^default check for`, or equals the category's table cell verbatim. The
    table cell names a kind of check; it is not a check.
- **Falsified by**: Script checks that pass this rule still turn out, at run time, not to test what the node's
  contract promises. That would mean "executable" was the wrong bar and the bar has to be the sabotage proof (2.6).

### 2.1. The test is circular: its designs come from the table the gate reads
- **Principle**: 「知彼知己，百戰不殆；不知彼而知己，一勝一負；不知彼不知己，每戰必殆。」 — "If you know yourself but not
  the other, you will lose one for every one you win." Design rule: "A workflow must model two things with equal
  care — the task … and the team's own actual capabilities." — deepseek-v4-pro #1, **VERIFIED**.
- **Why it applies**: The test knew only itself (己). `corpus_check.build_design` writes designs from the same
  TASK_TYPES rows that `parse_types` reads, so the gate was matched against its own reflection. The 彼 for a gate is
  a design it did not help write: one from the real designer, or a bad one. The test met neither. The real designer
  is `intake.js`, and its output is not even in a form the gate reads (register 4.5: it emits `pieces`). Read from
  the code: a design with no `nodes` raises no node rule at all. `{"categories": ["code generation"], "builds":
  true, "touched_paths": ["x"]}` passes clean, and so does `{}`. Feed the gate intake.js output today, and at most a
  top-level G1 or G2 can fire. Nothing it says about the pieces themselves gets checked.
- **The change**:
  - New rule G0: a design with a missing or empty `nodes` list is a finding ("no nodes — not a design the gate can
    judge"). It is one line. It turns every real intake.js output from an unchecked pass into the gate's first
    contact with the 彼.
  - Add an optional top-level `designed_by`. In a batch run (see 2.2), if every design's `designed_by` is the table
    generator, print "CIRCULAR: n/n designs derived from the parsed table — not evidence about the gate" and exit 3.
- **Falsified by**: When the gate is run over designs intake.js actually produces (once 4.5 is joined), it finds
  nothing that it did not already find in the generated corpus. That would mean the circle hid nothing.

### 2.2. G5 and G7 never ran, because every design was `default`
- **Principle**: 「凡戰者，以正合，以奇勝。」 — deepseek-v4-pro #6, **VERIFIED**. With claude-opus-5-5 #7's "Violated by"
  (**RECALLED**): "running only the default forever with no challenger, or treating every run as an experiment so
  there is no stable baseline to compare against."
- **Why it applies**: The claude note names this exact state as its violation case: only the 正 was ever fielded. A
  run that never fields the 奇 says nothing about how the 奇 is governed. There is a further gap that the line points
  to. G5's arithmetic compares `estimate` against `default_estimate`, and the challenger writes both. So even when
  G5 runs, both sides of its comparison come from one author. And the self-test has no challenger that **passes**,
  so G5 is not known to admit a legitimate challenger either.
- **The change**:
  - Add `--batch DIR`: run every design and count, per rule, how many designs met that rule's precondition (G5 when
    `design_source` is an object; G6 when builders exist; G7 per ledger row). Exit 1 with "G5 never evaluated — this
    batch is not evidence for the challenger rule" when any rule's count is 0, unless `--allow-unexercised G5` is
    given.
  - Add one passing challenger to `self_test`.
  - Require `default_estimate.source` to name a ledger `run_id` or a default design file, and give a finding when it
    is absent ("the default's cost is the challenger's own number").
- **Falsified by**: Real challenger designs, once they exist, are rejected by G5 mostly on arithmetic rounding or
  bookkeeping rather than on margin or coverage. That would mean the rule's live surface is clerical and the batch
  counter was measuring the wrong thing.

### 2.3. Nothing bad was ever fed in, so the test cannot show the gate rejects
- **Principle**: 「夫未戰而廟算勝者，得算多也；……多算勝，少算不勝，而況於無算乎？」 — "Many counts win, few do not — how
  much less, none at all." Design rule: "scoring it against named criteria … A plan that cannot be scored is not
  started." — minimax-m3.1-flash #1, **VERIFIED**.
- **Why it applies**: 廟算 compares two sides on fixed factors before the battle. The corpus run counted one side
  only: 300 passes, and no known-bad design whose rejection could be counted. On the question "can this gate
  reject?" that is 無算, no count at all. The self-test does have 13 negative cases, which is to its credit. But they
  are hand-built against one good design, and none of them targets the substance rules this register says are
  missing. So even the self-test cannot score 1.1–1.7.
- **The change**: Add `--mutate DESIGN`. It applies a fixed list `MUTANTS` that lives in `design_gate.py`, not in
  TASK_TYPES, so that the mutations do not share the table's blind spots. Each entry is `(name, transform,
  expected_rule)`, and the list covers:

  | mutation | expected rule |
  |---|---|
  | drop all nodes | G0 |
  | blank each of the five contents | G3 |
  | drop `baseline` | G9 |
  | empty `stop.criteria` | G3 |
  | placeholder check | G3 |
  | remove `loop` from a loop-pattern node | G10 |
  | set `builds: false` while a node keeps `may_change` | G2 |
  | point `reviews` at a node that does not exist | G6 |
  | same-kind reviewer | G6 |
  | challenger claim of 0.19 | G5 |
  | drop one coverage criterion | G5 |

  Print the kill matrix, and exit 1 if any mutant survives. `--self-test` runs `--mutate` on `_good_design()`.
  `--batch` runs it on every design in the batch, so every real gate run is also a measurement of the gate.
- **Falsified by**: Every mutant is killed, yet real designs the checklist layer later rejects still pass the script
  gate. That would mean the mutant list encodes what the gate's author can imagine, not what designers actually get
  wrong.

### 2.4. The checklist layer never ran, though the script gate's docstring leans on it
- **Principle**: 「故備前則後寡，備後則前寡，……無所不備，則無所不寡。」 — "Prepare everywhere, and you are thin
  everywhere." — deepseek-v4-pro #8, **VERIFIED**. With claude-opus-5-5 #9's design rule (**RECALLED**): "Write down
  the risks the design deliberately leaves unchecked."
- **Why it applies**: The gate's docstring divides the guard in two: "Judgment is NOT done here: the second layer is
  a fixed-checklist reviewer". That is a legitimate split, a front and a rear. But the rear was never manned, and the
  gate's output does not say so. It prints `PASS`, which a reader takes for both layers. The text's point is that
  guarding one side leaves the other thin. The rule drawn from it is that the thin side must be named, so that no one
  mistakes it for covered ground.
- **The change**:
  - Never print a bare `PASS`. Print `SCRIPT-PASS (G0–G10)` and then a constant `NOT_CHECKED` list: recheck verbs as
    their own node (TASK_TYPES); whether the check measures the contract; whether the decomposition is right; and
    "checklist layer: NOT RUN".
  - Add `--final --review FILE`. It exits 0 only if `FILE` exists, records the sha256 of the design file under
    review, and answers every item of the fixed checklist. Otherwise the finding is "G11: checklist layer not run on
    this design". Callers that gate dispatch must use `--final`.
- **Falsified by**: The checklist layer, once run on real designs, rejects nothing the script gate passed. That would
  mean the rear was empty because there was nothing there to guard.

### 2.5. — omitted
The reported accuracies have no denominator. That is an arithmetic and reporting defect in the test log, and no
principle in the three notes adds anything to "report the denominator". The nearest candidate is 知己, knowing your
own executors. Pressed into service here, it would be decoration. No edit to `design_gate.py` touches the defect
either, because the gate does not compute those numbers.

### 2.6. Sabotage was never exercised, and the gate ignores the sabotage column
- **Principle**: 「是故智者之慮，必雜於利害。」 — "the wise person's deliberation always mixes advantage and harm." With
  「不盡知用兵之害者，則不能盡知用兵之利也」 — "One who does not fully know the harm of using troops cannot fully know its
  benefit." Design rule: "Each node's design names its expected payoff and its specific failure mode, plus how that
  failure would be noticed, side by side." — claude-opus-5-5 #12, **RECALLED**. (No verified note carries this line.
  The note itself calls the likeness to the sabotage check "a resemblance and not support from the text", and I keep
  that caveat.)
- **Why it applies**: Each TASK_TYPES row puts the two side by side: the `check` (the payoff, "this proves it worked")
  next to the `sabotage` (the harm, "this proves the check can see it not working"). The gate reads both cells and
  throws the harm side away. The corpus designs carry only a placeholder for the payoff side and nothing for the
  harm. By the line, knowing only the benefit is not knowing the benefit. A check whose failure mode was never named
  is not known to measure anything.
- **The change**: In G3, every node whose category row has a non-`—` sabotage cell must carry
  `sabotage: {action, expect, when}`:
  - `action` is non-empty and not equal to the table cell verbatim (the cell is a kind of sabotage, not this node's
    instance);
  - `expect` must name the same check, as `check.command` or a checklist item id;
  - `when` is `"before_first_trusted_pass"`.

  A missing or incomplete sabotage gives the finding "node {id} names no way its check could be shown to fail". The
  2.3 mutant list gains "drop sabotage → G3".
- **Falsified by**: At run time, nodes whose sabotage was declared and executed have checks that miss real defects as
  often as nodes without one. That would mean that a check which can fail on a planted defect still fails to see the
  defects that actually occur.

---

## Found while reading, outside the register

Read from the code, not run. These belong to the same family, and the 2.3 mutant list should include them:

- **G6 passes a reviewer whose `reviews` names a node that does not exist.** The target set is then empty, so
  `constraint` is empty and any reviewer kind is "different". G4 validates `needs`, but not `reviews`.
- **G6 checks each reviewer's own targets, not that every builder is covered.** A reviewer with `reviews: ["n1"]`
  pointed at the research node satisfies G6 while the code-generation node goes unreviewed. The change: the union of
  all reviewers' targets must include every builder id.

## Where the analogy breaks

1. **The gate has no enemy, and that changes what 彼 means, except in one case.** All three notes refuse to carry
   「兵者，詭道也」 into a cooperative system, and I agree. The designs the gate meets are mostly the designer's
   *accidents*, not an opponent's moves, and so most of 孫子兵法's reasoning about an adaptive adversary
   (致人而不致於人, 形人而我無形) has nothing to act on. The one exception is `(not from a note)`: an LLM designer that
   reads the gate's findings and retries will learn to satisfy the letter of each rule. That is Goodhart's law, and it
   is the only adversary the gate has. It argues for checking content that is costly to fake: the edge-evidence rule
   in 1.1, a resolvable check command in 1.7, and an executed sabotage in 2.6. It does not argue for deception or
   concealment.
2. **"No fixed form" applies to the workflow, never to its referee.** 「兵無成勢，無恒形」 (minimax #6, deepseek #9,
   both VERIFIED) is the most quoted idea in all three notes, and it is the wrong one for this file. A gate is useful
   because its verdict is the same every time: Ancient Games' own rule is "fixed rules, no LLM calls". The workflow
   may change shape with the ground; the gate checks that it said what its shape is. Anyone who brings "water" to
   the gate itself is making the gate a judge that bends, which defeats its purpose.
3. **「備前則後寡」 assumes fixed strength, and a script's rules cost almost nothing to run.** Adding G9, G10 or G11
   does not thin G3. Compute is not the scarce budget. The scarce budgets are the designer's attention, spent filling
   in more required fields, and the rate of false rejection. So I use the line only for its second half, *say what is
   unguarded* (2.4). I do not use it to argue that the gate should have fewer rules. Taken literally, it would argue
   against most of the changes above, and that literal reading does not transfer.

## The one change

**1.3, the three-part stop as a structured, checked field on every building node.** It carries part 2 of 1.2's
baseline with it. Method 3.6 states plainly that this stop "is what lets a run end", and that is the promise EJ added
the blueprint for after "several projects never ended". The gate is the only mechanical place that promise is
enforced, and today it does not enforce it at all. The other changes make the gate harder to fool. This one is
different: it is the gate checking the single thing that is entirely in the designer's power before dispatch
(不可勝在己), namely a written, objective definition of done. Without that, 「不合於利而止」 has no condition to stop on.
