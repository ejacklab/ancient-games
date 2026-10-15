# 孫子 (Sun Tzu) — what our hands can do, and what the ground allows

## Answer

Read against my three-part test — *can our troops do it, can the enemy be attacked, does the ground permit it* — the design's four pieces are whole at **doing** (P1: the four expert engines ran on 2026-10-15; P2: the COO and the build script both ran, the script passing on 2026-10-15) but half at **knowing**: P3 because the reviewer's power to find a thing is asserted, not shown, and P4 because its baseline is moving. The spots carrying the half are **U3/U4** (Rd3.1a's MUST rests on `MAX_LINES = 200`, `MAX_BYTES = 24_000`, which the code itself calls "the design's example, not a measurement"), **U2** (the owner is a role with no fallback), **U5** (the two sibling files exist only in this repo), plus **N1** (no shown plant-finding), **N2** (the checker may be edited by the hand it checks) and **N3** (the baseline already has a failure from another session); **U1** is half in means only. None of them is a reason to stop — *if* EJ answers U1–U5, has Rd3.1a say the limit is provisional until U4 is measured, and has the edited build script and the blind reviewer each shown able to fail before P2 runs.

## How I decided

1. The question is my **#4**, read in its own order: 「知吾卒之可以擊，而不知敵之不可擊，勝之半也…知敵之可擊，知吾卒之可以擊，而不知地形之不可以戰，勝之半也」 (quoted) — knowing our troops can attack but not the enemy; knowing the enemy and our troops but not the ground, is each *half a victory*. Its close gives the standard: 「知彼知己，勝乃不殆；知天知地，勝乃可全」 (quoted). So of each piece I ask: are the **means** able, is the **task** able, does the **ground** permit — and I mark *whole*, *half*, or *not known* on each of the three.

2. I reckoned the four pieces first, as my **#1** requires: 「多算勝，少算不勝，而況於無算乎？」 (quoted).

   - **P1 (experts, EJ):** means known, task known, ground known — the seats and briefs exist, the engines ran, the COO filled the facts. Whole, with two spots inside it (U2, U4).
   - **P2 (edits, COO):** means known, task known, ground known — but P2 cannot make itself *known done*: its own design says the build script "does not establish that the text is right; P3 judges that." That is my **#2**: 「不可勝在己，可勝在敵」 (quoted) — being unbeatable lies with oneself, being beatable with the enemy. P2 can make the files well-shaped; it cannot make the fix right. Whole at doing, half at knowing.
   - **P3 (blind review):** task known, ground half (the plant is withheld — good — but chosen and held by the COO, the party whose edit is on trial), means half (a Sonnet subagent *ran* on 2026-10-14; nothing shows it can find a planted contradiction). See N1.
   - **P4 (close):** means known (COO, git, text), task known, ground half — the design's own baseline is "993 passed, 1 failing from another session's skill edits." See N3.

3. **U1** (may `covers`, `source`, `depends_on` change after the first commit, each with a `changed:` line?) — task known (EJ can decide; the fields exist), ground known, **means half**: the facts do not show the build script's "one shape" check treats a `changed:` line on a header field as valid; if it does not, the L2 edit is carried by the run's own repair loop instead of by a reckoned means. My **#17**: 「角之而知有餘不足之處」 (quoted) — test in contact to know where there is shortage. Put one such line on one header and run the script *before* P2.

4. **U2** (who decides which agents work on the project?) — task known, means known, **ground half**. Writing the value is trivial; "the project owner" is a role, not a person, and the design is for any project — nothing says where a foreign project records its owner, so the unowned value can reappear wherever no owner is written down. This run also decides, among other things, who decides this run's agents. My **#16** puts the fault on the unclear order: 「約束不明，申令不熟，將之罪也」 (quoted). Ask EJ to name the role **and** the fallback when no owner is recorded.

5. **U3** (keep the example limit, or build the reader?) — means known, task known, **ground half — the sharpest half in the set.** Keeping the example is free and the reader is its own run (a road not taken: my **#13**, 「途有所不由」, quoted). But Rd3.1a's MUST then rests on numbers the code itself calls "the design's example, not a measurement," and U4 is out of scope: our means and the task are in hand, the terrain is not — my **#4**'s third clause exactly. My **#2** is the remedy: 「無恃其不來，恃吾有以待之」 (quoted) — rely on what we hold. What we hold is honest text: keep the example *and* say in Rd3.1a that it is provisional until measured. My **#3** prefers the whole to the broken, and my **#8** keeps the measuring out of this run: 「兵聞拙速，未睹巧之久也」…「兵貴勝，不貴久」 (quoted).

6. **U4** (each engine's real limit) — **not known, and correctly not attempted here.** The ground for it is visibly contested (`CACHES.md` W-4 on agy). My **#11** forbids substituting analogy or arithmetic for people who know: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也」 (quoted). It does not block this run *provided* U3's text admits the dependence.

7. **U5** (paths relative to the design folder?) — means known, task known, **ground half**. The path check resolves from `docs/memory-system/` and that is proved; the edit is a text edit. But "for any project" is a claim about ground we do not have: the vision file and `CACHES.md` exist only here, so a foreign project gets a link to a file it may not have. My **#19** says name the ground: 「九地之變，屈伸之利，人情之理，不可不察也」 (quoted). Ask EJ whether the two files ship with the design or are optional, and make the wording say which.

8. **N1 (new) — P3's plant is a promise, not a shown means.** Engine runs (known); detection not shown (half); the plant is authored by the COO. My **#12**: 「求之於勢，不責於人」 (quoted) — the review's ability to fail should come from a fixture, not from the reviewer's care. *My reading:* without a probe, "the plant was found" proves the plant was easy at least as readily as it proves the review is good.

9. **N2 (new) — the checker sits inside the changeable set.** P2 *may change* `build_requirements.py`, and the only evidence the script can fail belongs to the old script. My **#2** (make the check unbeatable before use) and my **#16** (clear first, then enforced) both say: after the edit, re-show its three failures — missing id, dangling link, second shape — or leave the script out of scope. *My reading:* otherwise the run's only scripted check may be weakened by the hand it checks.

10. **N3 (new) — the baseline is moving.** A failing test owned by another session means P4's "baseline unchanged" cannot tell our breakage from theirs. My **#1** (the reckoning includes one's own force) and my **#6**: 「不盡知用兵之害者，則不能盡知用兵之利也」 (quoted). *My reading:* pin the failing test's id before P2 and compare that, not the raw count.

11. I would drop or defer nothing here. U4 is already the road not taken, and my **#14** warns against valuing numbers for their own sake: 「兵非貴益多也，惟無武進」 (quoted). Every other spot changes the shape of the work only if EJ leaves it unanswered.

## What I need to know

- **U3/U4:** May Rd3.1a's text call 200/24,000 an *example* and make the MUST provisional until measured? If EJ wants the MUST to stand as measured, then U4 is a blocker, not a backlog.
- **U2:** Who is the project owner in a project that has not named one, and may the design carry a fallback value?
- **U5:** Do the vision file and `CACHES.md` ship with the design, or must a foreign project supply them?
- **U1:** Does the build script's shape check already accept a `changed:` line on a header field?
- **N2:** Must `build_requirements.py` change at all for L1–L5? If not, take it out of the changeable set.
- **N1:** Is there a contradiction a blind reviewer has found before, or may we run a one-shot probe?
- **N3:** Which single test is the failing one?

## Costs and risks

- **U3 provisional wording** — a MUST that is honest but unchecked against reality until U4; the price of a whole requirement is a number that is not yet a measurement. (my #4, #3)
- **Not measuring engines now (U4)** — the design's limit requirement stays provisional as long as the backlog is not done; measuring now is the long war this run should not fight. (my #8)
- **N1 probe** — one extra reviewer call (the design itself estimates 40–80k tokens); skip it and a found plant proves little. (my #12, #17)
- **N2 re-show** — a few minutes; skip it and the only scripted check may be silently weakened. (my #2, #16)
- **N3 pinning** — cheap; skip it and "unchanged" is misread. (my #1, #6)
- **U2 role plus fallback** — a longer requirement; skip it and the unowned value returns in every project. (my #16, #1)
- **U5 sibling paths** — the design gains a stated assumption; skip it and foreign links dangle. (my #4, #19)
- **The COO authors P3's plant** — the author sets the test; the design's mitigations are withholding it and the one rerun. (my #2, #12)

## How we would know I was right

- **U3/U4:** Rd3.1a reads as provisional; when U4 is later measured, only its numbers change, not its shape.
- **N1:** the blind probe finds the known contradiction; and in the real P3 a miss triggers the rerun already written into the design.
- **N2:** after any build-script edit, running it on a missing id, a dangling link and a second shape still fails on all three.
- **N3:** the same single test is the only failure before and after the run, or a new failure is named to this run.
- **U2/U5:** a project other than this one can fill the owner and resolve the links without asking us — a foreign test we cannot run today (my #4).
- **Overall:** the build script's output, the P3 verdict with file:line findings, and a second project's use of the design are the observables; until then, the design's state is *half known on the ground*, by my own test.
