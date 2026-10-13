# Four experts — keep Cloudflare Web Analytics on ancients.ejai.ai?

Written by Claude (main session), 2026-10-13. First run of the `four-experts` skill. Note: EJ had already decided
this question ("Cloudflare analytics on ancients.ejai.ai can keep", decisions.md D1) before the experts were asked;
the question was a test, and the experts' advice does not change that decision unless EJ says so.

| | Linus (Codex) | 范蠡 (agy) | 孫子 (dsh) | 老子 (opencode) | Control (Claude) |
|---|---|---|---|---|---|
| Answer | off for this page | off for this page | off, unless EJ will act on the numbers | off, unless EJ names a purpose first | off, unless EJ wants the numbers |
| Main items | #13, #3, #5, #11, #2 | #5, #7, #3, #2, #18 | #19, #16, #1, #2, #6, #5, #3, #13, #10 | #1, #13, #5, #3, #2, #12 | — |
| Time | 67.7 s | 75.6 s | 53.7 s | 47.7 s | subagent |

## Where they agree (quoted from the answers)

- **All five: turn it off for this hostname only, and keep it only if EJ will actually use the numbers.** None found
  a benefit in the facts given: "EJ has no stated plan to look at the numbers" appears in every answer in some form.
- **If kept, widen N2 deliberately and in writing — never leave it silently false.** 孫子: "the honest move is to keep
  the script and rewrite N2 deliberately"; control: "the worst option" is keeping it without changing N2.
- **Same verification:** load the page with the network panel open — no request to static.cloudflareinsights.com or
  /cdn-cgi/rum — and check another subdomain still has analytics (all five).

## Where they differ

- **Strength:** Linus and 范蠡 say "off", flat; 孫子, 老子 and the control make it conditional on EJ's purpose.
- **Style:** Linus is shortest (444 words) and marks most steps "my reading"; 范蠡 quotes heavily, and two
  applications are stretches (*my reading*): #18 「審備則可以戰乎」 read as "tighten the perimeter", and the 「用力甚少」
  line used for a config rule.

## What the experts added over the control (*my reading*)

The control reached the same answer with most of the same reasons. Points it did not make:

1. **孫子 #2:** "no cookie" is Cloudflare's present behaviour — the page's privacy rests on someone else's restraint,
   not on anything EJ owns. 孫子 calls this the strongest single reason.
2. **老子 #13:** the RUM beacon is also a health signal — "a page that fails on a phone fails quietly" without it.
   A cost of turning it off that no one else named.
3. **老子** flagged the weakness of its own seat: the items it leaned on most have no Guodian witness, and #18–#19
   are attributed.
4. **孫子 #11:** visitor counts are 度 (measurement), and foreknowledge "must be taken from people" — ask readers,
   not dashboards.

So on this question the experts mostly confirmed the control and added two or three angles. n=1; not a measure of
whether they help in general.

## What they need to know (merged, for EJ)

1. Will you use this page's visitor numbers for a decision, now or after sharing? (all five)
2. Does the page or README promise readers "no tracking"? (control, 孫子)
3. Without the beacon, how would you notice the page breaking on a phone? (老子)

## Check

- Engines as designed; agy answered, no fallback (`status.json`). Control run as a Claude subagent (`--claude-by-caller`).
- `four_experts.py check`: **1 failure** — 孫子 wrote 「趙毋失其故法」 where its list has 「赵毋失其故法」 (1 character,
  traditional for simplified; same line, not invented). Every cited item number exists. `--sabotage`: 3 failures
  reported (an altered quote and #99), so the check can fail. The check was written by Claude; it does not establish
  that a rule was applied correctly.
- 孫子's answer calls EJ "he" (its brief predates the they/them line, added during this run); 老子's answer starts with
  a stray "I'll read that brief first." line.

## Added later the same day: Dave (the control)

EJ then made **Dave** the control (experiments, data-driven, nature-inspired; 10 rules from EJ) and removed the plain
control; `answers/control.md` above stays as evidence of the first run only. Dave ran as a Claude subagent
(`--only dave --claude-by-caller`); `check`: Dave passes (the one failure is still 孫子's 趙/赵).

- **Dave's answer:** off for this page; flip back on if EJ wants numbers — widen N2 in writing first and write the
  prediction down (his #1, #3, #4, #8). Same direction as the other four.
- **What Dave added that no one else did** (*my reading*):
  1. **#9, report the failure:** the page did not meet N2 as served — and he asked *how N2 was checked: against the
     file or the served page?* That is exactly what happened: the local test passed, the live test found the
     beacon. A real blind spot, named by Dave alone.
  2. **#5, data you already have:** Cloudflare has probably been counting the page since it went live and nobody
     looked — the existing count is itself evidence about whether EJ uses it.
  3. **#3, write the prediction first,** with EJ setting the stop date (he declined to set it himself).
  4. **#6/#7 worked as designed:** he tried a nature analogy (cave animals losing unused organs), checked the fit,
     found the key condition differs, and **dropped it as evidence**.
