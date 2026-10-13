# 孫子 (Sun Tzu) — turn analytics off a page that promised none

## Answer
If N2 is EJ's own requirement and he does not plan to act on visitor numbers, turn Cloudflare Web Analytics off for ancients.ejai.ai only and leave the zone-wide rule in place for the other subdomains. If he does plan to use those numbers, the honest move is to keep the script and rewrite N2 deliberately — not to leave the page's stated law quietly false.

## How I decided

1. **Name the ground before prescribing for it (my #19).** My #19: identify the ground by the conditions, then act as prescribed — "the variations of the nine grounds, the advantage of drawing in or extending, the pattern of human feelings: these must be examined" (「九地之變，屈伸之利，人情之理，不可不察也。」, quoted). The given conditions are one public page, no login, no forms, no ads, nothing sold, read on a phone by EJ alone, with its own requirement N2 ("one file, no tracking"). On that ground the fitting action is the one made for a small private page, not the zone-wide default made for public sites.

2. **A page whose orders and behaviour disagree is the general's fault (my #16).** My #16's rule is orders clear first, then enforced, and if they are clear and still not followed the fault lies elsewhere. N2 is a clear order. A script from static.cloudflareinsights.com plus a request to /cdn-cgi/rum is the page quietly not following it.

3. **I counted both sides (my #1).** My #1 is the reckoning: "More wins, fewer does not, how much less none at all?" (「多算勝，少算不勝，而況於無算乎？」, quoted). Keep: one third-party script and one extra request, in exchange for aggregate counts EJ has no stated plan to read. Off: one hostname rule, other subdomains untouched. The count is not close, because the benefit side has no named user.

4. **Do not rest a guarantee on the other side's good behaviour (my #2).** My #2: "Do not rely on their not coming; rely on having the means to meet them. Do not rely on their not attacking; rely on having what cannot be attacked" (「無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。」, quoted). "It sets no cookie" is Cloudflare's present behaviour — someone else's restraint. The page's "no tracking" then rests on that restraint, not on anything EJ owns. An exclusion rule is something EJ owns. **My reading:** this is the strongest single reason, and it does not depend on how mild the script is.

5. **I wrote the harm column too (my #6).** My #6: the wise mix benefit and harm in deliberation, and "whoever does not fully know the harm of using troops cannot fully know its benefit" (「故不盡知用兵之害者，則不能盡知用兵之利也。」, quoted). Benefit: someday knowing whether sharing worked. Harm: N2 becomes half-true, and a stated requirement that is quietly not enforced is where drift starts.

6. **Do not move without advantage (my #5).** My #5: "Do not move without advantage, do not use troops without gain, do not fight unless in danger" (「非利不動，非得不用，非危不戰。」, quoted), and move only when it accords with advantage (「合於利而動，不合於利而止。」, quoted). Keeping the script is the move that adds a load with no matching advantage; removing it costs only an unused feed.

7. **Keep the whole by taking the cheap option; decline the standing order for this page (my #3, my #13).** My #3 prices the costly option and ranks it last — "attacking walled cities is the method for when there is no alternative" (「攻城之法，為不得已。」, quoted) — so the cheapest effective action is preferred. The exclude rule is that: it leaves the zone-wide setting whole for every other subdomain. My #13 covers the local refusal of a standing order — "There are roads one does not take … ruler's commands one does not accept" (「途有所不由…君命有所不受。」, quoted): the blanket rule is made for the many subdomains, not necessarily for this one. **My reading** of my #14: the force ratio is one line of configuration against no stated gain, so the outcome is not in doubt.

8. **Leave the door open, because the ground may change (my #10).** My #10: water shapes its course by the ground and an army shapes its victory by the enemy; it has no fixed 勢 and no constant form (「水因地而制行，兵因敵而制勝。故兵無成勢，無恒形」, quoted). The exclusion is per-hostname and reversible, so if the page is later shared and usage becomes a real question, the ground has changed and the decision can change with it. My #20 reads the same the other way: the houses that widened their base fell, while "Zhao has not lost its old laws" (「趙毋失其故法」, attributed) and held. N2 is this page's old law, and keeping it costs nothing today.

9. **What I checked and did not use (my reading).** No opponent is named here, so my #7 (deception) does not bite. Nothing in the facts shows anger or wounded pride, so my #5's anger clause and my #15 (the general's five dangers) do not bite. There is no enemy to probe, so my #17 does not bite. And a count of visitors is measurement — 度 — which my #11's own words exclude as a source of foreknowledge: it "cannot be verified by measurement; it must be taken from people" (「不可驗於度，必取於人」, quoted; 李筌 glosses 度 as number). **My reading:** even if kept, the numbers would not tell EJ whether the page works for a reader; people would.

## What I need to know
- **Who set N2, and who is it a promise to?** If N2 is EJ's own setting, turning the script off is cheap and reversible. If N2 is a stated promise to readers, keeping the script breaks it, which raises the cost of keeping.
- **Does EJ plan to act on visitor numbers, now or after sharing?** If yes, keeping the script has a real advantage side and my #1's count changes; if no, it does not.
- **Can the exclusion be verified after the fact?** If neither EJ nor I can confirm that the script and /cdn-cgi/rum actually stop for that hostname, then "N2 restored" is unproven, and the choice is between two unverified states.
- **What does "no tracking" mean in N2 — no cookies, or no third-party requests at all?** The brief reads the second way ("no network request except Google Fonts"). If those words are narrower than intended, the weight of my answer shifts.

## Costs and risks
- **Turning it off (my #5):** the advantage side is nil today, but if the page is later shared and used, the counts will not exist — that is the price of the off choice, paid only if the future use is real. **My reading:** it is also one more config line to maintain and verify (my #16).
- **Keeping it (my #2, my #6, my #16):** the guarantee rests on Cloudflare's present no-cookie behaviour rather than on anything EJ controls; N2 stays half-true; and an unenforced stated rule is exactly what my #16 assigns to the general's fault.
- **Keeping it, specifically (my #20; my reading):** a page whose whole premise is "one file, no tracking" now carries a third-party request it does not mention, and widening a rule once makes the next widening look normal.

## How we would know I was right
Load ancients.ejai.ai in a phone browser's network panel and confirm no request to static.cloudflareinsights.com and none to /cdn-cgi/rum, with Google Fonts the only external request. Then load one other subdomain of ejai.ai and confirm the analytics script is still there, so the zone-wide rule was not broken. If the page is later shared, the second test is to ask the people who read it whether it worked — per my #11, that is where foreknowledge comes from, not from 度.
