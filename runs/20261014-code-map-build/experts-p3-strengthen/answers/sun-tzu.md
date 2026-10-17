# 孫子 (Sun Tzu) — strengthening the A5 and A2 checks

## Answer

Strengthen by **clause**, not by command: A5 has one compound Fails-if line holding four failures, and A2's line 2 and line 3 each hold two (a tool half and an agent half), so add one case per clause, make the report mark a clause with no case **NOT CHECKED**, and cut the cases that restate another requirement's fact. Below, each change names the clause or line it is tied to. No requirement wording is changed; the wording proposals at the end are for EJ.

### A5

A5's Fails-if line is one string with four failures: **(a)** the answer comes only inside a dump, **(b)** without its evidence, **(c)** without its limits, **(d)** a whole map is produced unasked. Today's bundled A5 cases are only two `where` runs — `A5-specific-answer` (which asserts `limits: []`) and `A5-default-text` — so (b), (c) and (d) are exercised only for one command, and (d) not at all in the bundled set.

**Keep**
- (b) The link-`site` evidence case on `callers`/`callees`/`chain`/`tests` [COO A5 #1]. **Keep.** It is the one A5 case that exercises a link command; the same assertion already exists in the frozen test's `expectLink`, so the frozen test is the stronger home.
- (d) The case that fails when `map`, or a section the command does not own, rides on a link command [COO A5 #3]. **Keep, but in the frozen test** (`expectFocused`), and keep the exemption the COO named: an ambiguous name legitimately answers with `matches` and no links.
- (c) `A5-specific-answer`'s `equals{limits: []}`. **Keep.** It is the only guard against a tool passing "has limits" by attaching a blanket limit to every answer.
- (a) `A5-default-text` [COO A5 #4]. **Keep the intent, rewrite the check** (see Cut).

**Cut**
- [COO A5 #2] the "run with no `--tests`" case. **Cut.** That limit is A3's fact and is already charged to `R2-no-tests-pattern` and to the frozen test "callees without test classification keeps its stated limit". It adds a second home for one fact and charges A5 for A3's rule (my #13, 「途有所不由」, "there are roads not to be taken").
- [COO A5 #4] as phrased: "the text carries places the question did not ask for". **Cut the phrasing.** "Did not ask for" has no owner and no test. Replace with the fixture's known unrelated definitions: in `service-dispatch`, `archiveMeteorite`, `polishMeteorite` and `duplicatedDesk` must not appear in a `where`/`callers` answer (my #11: name what the check can actually establish).
- Any further case that repeats a command without adding a clause. **Cut** (my #14: act by the ratio of forces — two to one, divide; do not mass on the same spot).

**Add**
- (b) A `find` case: every match carries `file` and `line`. No bundled A5 case uses `find` at all today.
- (c) A `chain` depth case (`--up 0 --down 1`) asserting `{reason:"depth"}` appears — A5's own answer's limit, not another requirement's.
- (c) A `not-found` case on a link command (`callees missingNebulaDispatch`): the command stops, and the answer carries the reason.
- (c) For every limit-bearing case, an exact `equals` on the limit, not only `limitReasons`; presence alone is satisfiable by noise.
- (d) A frozen assertion that no command other than `map` returns map content in its **text** output, with the envelope check extended to the new commands (`find`, `tests --file`).
- (clause coverage) The report must list the clauses of A5's line and mark one with no case **NOT CHECKED** (my #1, 「多算勝，少算不勝，而況於無算乎？」 — the reckoning is only usable when the counts are laid out).

**Wording proposal for EJ.** Current: *"A specific question gets that answer with its evidence and limits… A whole map is produced only when the user asks for a module map. Fails if: an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked."*
- Add: "…with the limits this run reached; an answer with no limit carries none."
- Split the third clause by who acts: **tool** — "no command other than a module map returns map content"; **agent (P6)** — "the agent runs `map` only when the user asked for a module map."
- Rephrase (a) as: "the answer is returned by the command's own output, not only buried in other content."

### A2

A2's Fails-if lines are: **(1)** a known place is not found; **(2)** an ambiguous match treated as certain, or an unbuilt candidate not named; **(3)** a known link within the depth missing, or a shown link contradicting the code; **(4)** a link lacks its kind or location; **(5)** a function reached twice is shown twice. COVERAGE already has a case for every line; what is missing is the second half of line 3, the up direction, and the agent half of line 2.

**Keep**
- (line 3) The anonymous-body chain cases at level 2 or deeper, both ways [COO A2 #1]. **Keep, but assert `file` and `line`, not the holder `name`** — see Linus.
- (line 3) The `Effect.fn`-held step reached through a service [COO A2 #2]. **Keep, conditional on the real shape being supplied** (see "What I need to know"). It is the only proposed check aimed at the two known private failures.
- (all lines) The existing per-line cases in COVERAGE. **Keep** — they are the least that makes each line fire.

**Cut**
- [COO A2 #3] "make A2's own line fire". **Cut.** Every A2 line already has a case. The gap is the *second half* of line 3 and the *agent half* of line 2, not a whole-line case.
- [COO A2 #4] "the frozen tests include these shapes". **Cut as a check** — it is a condition on the round's frozen tests, not a check. Fold it into the keeps.

**Add**
- (line 3, "contradicts") An `excludes` case: a call that resolves only to a same-named helper or a test fake must not be shown as a real link. The only exclusion today is `A2-default-six-down` (my #4, 「知彼知己，百戰不殆」 — check the other side's link as well as your own).
- (line 3, "missing") Fix `--up` and `--down` explicitly in the anonymous/`Effect.fn` cases and add the **up** direction; the private failure is in `callers` and `callees`, so down-only leaves half the line untested.
- (line 5) One case where the same anonymous body is reached twice, with `stop:{reason:"seen", ref}`.
- (line 4) Assert `kind` and `site` on the anonymous link itself — an unnamed body is the easiest place to lose them.
- (line 2, tool half only) Two same-named `Effect.fn` steps in different files: `ambiguous: true` and every matching candidate listed with its location. The agent's half stays **NOT CHECKED (P6)**.
- (all) Clause coverage in the report: line 3 has two halves, line 2 has a tool half and an agent half. Mark each.

**Wording proposal for EJ.**
- "a known place is not found" → "a place the type checker can establish is not found" ("known" has no owner; my #11, 「必取於人，知敵之情者也」 — foreknowledge must come from a named source).
- Line 2, split by who acts: **tool** — "an ambiguous match is not flagged, or a matching candidate is not listed with its location"; **agent (P6)** — "an ambiguous match is treated as certain, or a candidate the agent did not build is not named."
- "a known link within the depth is missing" → "a link the type checker establishes within the depth is missing."

## How I decided

1. I read my list and the allowed evidence, then counted the ground before committing, as my #1 requires: A5 = one line, four failures; A2 = five lines, two of them compound. My reading of the tool (`commands.ts`, `links.ts`, `nodes.ts`) and the evaluator (`matcher.ts`, `case-file.ts`, `requirements.ts`) is that the evaluator's `requirements.ts` keeps A5 and A2 line 3 as **one string each**, so a compound line is reported **MET** as a whole even when one half has no case. That is the load-bearing finding.
2. **Linus — could the strengthened checks still pass while A5 or A2 is wrong?** Yes, five ways.
   - A5: clause (c) is checked only by presence, so a tool that appends a blanket `{reason:"other"}` limit passes every limit case, and the one `limits: []` guard covers a single `where` run (my #15, 「凡此五者，將之過也」 — the check's own faults are the handle against it).
   - A5: the case format cannot assert an **absent** key (`selectPath` returns `[]` for a missing key, so `equals` sees `undefined` and `excludes` always passes), and `textIncludes` has no exclusion. Written as eval cases, COO A5 #3 and #4 pass the very dump they aim at (my #1: the instrument must measure the thing).
   - A5: the held-out copy is a rename-and-shift of the bundled cases, so "not NOT MET on held-out" is not independent evidence — it has the bundled set's blind spots (my #2, 「勝兵先勝而後求戰」 — you can make your own side unbeatable, not the enemy's).
   - A2: line 3's "contradicts" half is not exercised by presence-only cases; an invented same-named-helper link passes (my #7, 「兵者，詭道也」 — a false link is the deceit the check must catch).
   - A2: an expectation on an anonymous holder's `name` (`"Effect.gen callback"`) is **not** renamed by `rewriteLocations` — its `/^[\w$.]+$/` test rejects the space — so the strengthened case either fails on held-out for the wrong reason or is written to avoid names and then cannot catch a wrong holder.
   - A2/A5: both requirements carry the agent's obligation in the same Fails-if line as the tool's, and the evaluator marks it NOT CHECKED. "A2 MET" or "A5 MET" can be read as the agent's duty done (my #13: 「君命有所不受」 — the check does not accept every command laid on it).
3. **范蠡 — the least before A5 closes and A2 starts, and what can wait.** Before A5 closes: make the report clause-aware, then add only the cases for clauses with no bundled case — one link-command evidence case (b), one chain-depth limit case (c), one not-found limit case (c), one bounded-text case (d), keeping the `limits: []` guard. Re-run the five plants; if A5's own line still fires, it does not close. Before A2 starts: the real opencode shape for an `Effect.fn` step reached through a service, from the COO (my #11: 「必取於人」 — purchase the foreknowledge), plus the decision that line 2's agent half is P6. Can wait: varying the held-out generator's structure if the private set covers the shape; the `find`-by-label case; the wording proposals to EJ (my #8, 「兵聞拙速，未睹巧之久也」 — the cheap decisive move now, the long polish later; my #13).
4. **孫子 — which checks are readable by the builder only, and how is that covered.** The frozen tests and the bundled cases are readable by the builder, so every shape put there can be special-cased (my #7: the builder sees the form you show). The held-out copy is generated from the bundled set, so it hides only names and lines, not shapes; only the 10 private real-code cases are an independent probe (my #17, 「策之而知得失之計」 — learn them by probing; my #2). So put the **shape** in the bundled fixture (the builder needs the rule to implement) and the **instances** in the private set, with new names and real code. Do not rest A5/A2 on the held-out rename: it cannot cover a shape the bundled set lacks (my #10, 「兵無成勢，無恒形」).
5. **老子 — what is more than needed, and the small change that does more.** More than needed: COO A5 #2 (A3's fact), COO A5 #4's unrestricted phrasing, COO A2 #1 and #2 as two separate efforts when one fixture with an `Effect.fn` step whose body holds an anonymous `Effect.gen` callback covers both, COO A2 #3 (already true), COO A2 #4 (a process note) (my #5, 「非利不動，非得不用，非危不戰」 — do not move without advantage). The small change that does more: **mark coverage per clause, not per compound Fails-if line.** A5 was about to close on two `where` cases with the line reported MET; clause marking would have shown three clauses NOT CHECKED, and the same single change fixes A2 line 3 (missing/contradicts) and line 2 (tool/agent) with no new fixture (my #1: ground → measure → quantity → number → weighing; the report is the number that makes the count usable).
6. On the wording question: **A5's clause (d) lets a failure pass that no tool check can catch** — the tool never sees "the user asked", only the command `map`; P6 explicitly marks it NOT CHECKED. **A5's clause (c) lets a boilerplate limit pass** unless the wording says the limit must be the one this run reached. **A2's line 2 second half** is the agent's and is NOT CHECKED; **A2's "known link"** has no owner, so a check cannot be independent of whoever declares it known. The proposals above are for EJ, not for the checks.

## What I need to know

- Does the private set of 10 real-code cases contain A5 cases, or only A2? If only A2, A5's shapes rest entirely on the builder-readable set. (my #17)
- Can the eval case format be extended with `textExcludes` and an absent-key assertion, or must COO A5 #3/#4 live only in `test/a5`? The answer decides where those checks go. (my #1)
- Will the COO supply the real opencode `Effect.fn`/service shape for the bundled fixture, or only describe it? Without the shape, COO A2 #2 is a guess. (my #11)
- Is a NOT MET on the private set a round blocker, or advisory? If advisory, the strongest probe does not gate. (my #2)
- Who declares a link "known" for a new shape — the check author or the owner's private answers? If the check author, the check and the tool share one fallible reading. (my #11)

## Costs and risks

- **Clause-level reporting** (my #1): costs a report change and upkeep; risks over-fitting the report to today's clause list. Its benefit is that it catches the current blind spot.
- **Exact `equals` on limits** (my #6, 「智者之慮，必雜於利害」 — mix the harm in): risks false failures when a legitimate extra limit appears; the case must pin the run, not the whole reason set.
- **Anonymous-body cases with `name` assertions** (my #4): risk of a held-out false failure from the space-in-name rewrite. Price: fix `rewriteLocations` or assert locations only.
- **Adding private-set shapes** (my #11): costs the COO's time to mine and maintain them; without that payment the shape regresses silently.
- **Cutting COO A5 #2 and A2 #3** (my #5/#8): the failures they aimed at lose a named case; the clause report is the compensation.
- **Charging the agent's half to the tool** (my #13): risk that the owner reads MET as the agent's duty done; the price is a requirement rewording, which is EJ's to make.
- **Fixing the A2 tool before the shape is fixed** (my #2): risk of building on the wrong shape; the price is rework.

## How we would know I was right

- **A test:** re-run the A5 evaluator on attempt 1 and on a deliberately dumping variant; with clause marking, every clause shows a case, and the dumping variant turns the map clause NOT MET. If any clause with zero cases still reads MET, I was wrong.
- **A test:** plant a same-named helper link and a dropped `from`/`to` in the A2 fixtures; the contradiction and kind/location checks must fail.
- **An observable:** on the next private-set run, the two failing cases (callers and callees of the `Effect.fn` step through a service) pass, and no held-out case fails for a renamed anonymous holder name.
- **The cheapest observable:** the next report lists clauses for A5 and A2, and a clause with no case is **NOT CHECKED**, never MET.
