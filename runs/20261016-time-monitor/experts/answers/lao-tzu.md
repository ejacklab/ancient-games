I'll read the brief first.
# 老子 (Laozi) — how often the guard adds the time

## Answer

**(B)** — one line on every tool call, with the fuller block carrying the workers' progress at the marks and at the deadline. Conditional: C2 as currently written ("after tool calls at reminder marks") *is* option (A); if that wording cannot move, then choose (A) knowingly, as the one design no source in F1–F8 tested.

## How I decided

1. Every tested design updates after the call, not at marks. F1 (`verified`): BATS adds its budget block "immediately after each tool response", not at thresholds; F3: Anthropic's update lands after each tool call; F6: a per-turn remaining-time update took closure from 4% to 32%. The research's own closing line says the 50/80/100 marks were "not addressed", and F7 confirms no fraction-based or end-only condition was run. My #13 — 善有果而已，不敢以取強 ("has a result and that is all; he does not dare use it to take strength") — so I take the design that has the result rather than reach for strength the evidence does not give. That declines C as well, whose N nobody has measured, on my #19 — 以約為紀 ("he takes depth as the root, restraint as the rule"; `attributed`).

2. The per-call line is not a cost the research found. F2: with the tracker, budget 10 reached12.8% against the baseline's 12.6% at budget 100, with 40.4% fewer search calls and 31.3% lower cost. My #10 — 二曰儉 ("the second is frugality") — is therefore satisfied at ~20 tokens per call: the frugality that matters here is restraint of form, not the absence of the signal.

3. The signal must arrive while the agent can still act; that is the whole point of it. F6's quote is that "LLMs struggle to internally track elapsed time", and F5 gave 40% control for a prompt-stated budget against 100% with forcing. My #6 — 為之於未有，治之於未亂 ("act on a thing before it exists; order it before it is in disorder") — at the 80% mark the room to re-plan is already spent, which is what rules (A) out for me.

4. Worker progress belongs at the marks, not on every call. My #3 — 持而盈之，不如其已 ("holding it and filling it is not as good as stopping") — and my #17 — 三十輻共一轂，當其無，有車之用 ("in its nothing lies the cart's use"). If progress rode every call, the same facts would be counted twice, once from the worker and once from the guard. B's shape is the one that keeps the use case (progress per small piece) and stays inside the vessel.

5. The line reports; it does not command. My #4 — 為者敗之，執者失之 ("one who acts on it spoils it; one who holds on to it loses it"). F4 (vendor claim, not independent) is the reason: a budget that feels too small can make the model "scope it down aggressively, or stop early". Every call should carry the number; the instruction to wrap up belongs at the marks and after the deadline.

6. The end gets the most, not the least. My #7 — 民之從事，常於幾成而敗之。慎終如始 ("people often fail when they are close to finishing; careful at the end as at the beginning"). The reporting step *is* 幾成, so (A)'s after-deadline line is right and I keep it — bounded by my #2 — 知止不殆 ("knowing to stop, one is not endangered"): the guard states the deadline once it has passed and stops adding. My reading on form: keep the line unemphasised, so it does not contend with the task — my #15 — 水善利萬物而不爭 … 夫唯不爭，故無尤, and 動善時 ("in moving, good is timing"; `quoted`).

## What I need to know

1. Will C2 be amended? As written it says "after tool calls at reminder marks", which is (A). (B) needs "after every tool call, plus the fuller block at the marks". If the criteria are fixed, my answer is (A) with no measured support behind it.
2. How many tool calls does a run make, and does the guard's line share the same context window as the work? At hundreds of calls, 20 tokens each is not nothing (my #3, my #17).
3. Can the agent already ask the guard for the time? If yes, per-call is convenience and marks-only is cheaper; if no, per-call is the only channel it has.
4. Is 11:22 soft or hard — may work continue after it? That decides whether "time is up" repeats on every later call or is said once and then stops.

## Costs and risks

- (B) spends context on every call: that is the vessel's emptiness (#17) and its brim (#3). The lines are pure overhead and compete with the room the agent needs to think.
- A per-call line that instructs rather than reports is the grip that spoils (#4), and F4 names the failure: scope down aggressively, or stop early. A bad report is worse than a late one.
- F2b's tiers are the vendor's own prompt tiers, labelled `reported`, not `verified`; I use them only as the shape of the marks, not as evidence for anything.
- C is declined because its number is unmeasured. If EJ wants it, it must be measured first — the research's own line is that this ground was not addressed.
- My #6 again: at 100% no signal creates time. The guard can only tell the truth while there is still time to act.
- If the measured per-call hook cost (C6) comes back high, the fallback is *not* C. It is a shorter one-line, still on every call.

## How we would know I was right

- Run the same piece of work twice, marks-only and per-call, and count whether the agent's report lands before the deadline. Falsifier: the count does not change — the extra tokens bought nothing and I am wrong.
- Count how often the agent asks the guard for the time. Under (B) it should be ~zero; if it stays high, the line is not being read.
- Watch F4's failure directly. If under (B) the agent begins refusing work, scoping down, or stopping early, the signal is too strong and I am wrong.
- Count duplicated progress lines. If a worker's line appears in more places than the worker wrote it, the design has filled the vessel and (B) has become (A) with extra steps.
