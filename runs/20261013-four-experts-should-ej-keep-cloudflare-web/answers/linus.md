# Linus Torvalds — Keep analytics on ancients.ejai.ai?

## Answer

**My reading:** Turn Cloudflare Web Analytics off for ancients.ejai.ai only. That preserves N2 and serves the stated reading use; the price is losing this page’s analytics while it is excluded.

## How I decided

1. **Solve the present need — my #13.**  
   `quoted`: “If it doesn't solve some fairly immediate need, it's almost certainly over-designed.”  
   EJ needs a page to read on a phone. No use for visitor numbers is stated. My reading: possible future sharing does not yet justify collecting them.

2. **Judge the user’s workflow — my #3.**  
   This rule concerns actual user breakage, rather than a document or test alone. My reading: violating N2 does not itself prove that analytics breaks reading. But the supplied facts establish additional requests that conflict with the chosen requirement, without establishing a benefit that warrants widening it.

3. **Keep the decision reversible — my #5.**  
   Excluding one hostname makes this a small configuration decision. My reading: analytics can be reconsidered when EJ has a concrete use for it. Reversing the setting would not recover measurements missed while it was disabled.

4. **Explain any change in purpose — my #11.**  
   This rule asks what a change does and why it belongs. My reading: keeping analytics needs a reason for widening N2. A zone-wide default explains how analytics arrived here; it does not establish why this reading page needs it.

5. **Verify the result — my #2.**  
   This rule demands implementation evidence over claims. My reading: inspect the page’s network requests after exclusion, and check that phone reading still works. I make no measured claim about speed or battery savings.

## What I need to know

What concrete decision would EJ use this page’s analytics to make?

If there is one, reconsider whether its benefit warrants widening N2. If there is none, the recommendation stands.

## Costs and risks

- **Missed measurements — my #5, my reading:** Re-enabling analytics restores future collection, not the missing interval.
- **Configuration upkeep — my #11, my reading:** The hostname exception needs a recorded reason so a future change does not silently remove it.
- **Unproven benefit — my #2:** Removing requests is observable; a meaningful performance improvement is **not measured**.

## How we would know I was right

**Proposed check, written by me, applying my #2 and my #3:** After exclusion, load the page and confirm that neither static.cloudflareinsights.com nor /cdn-cgi/rum is requested, permitted font loading still works, and EJ can still read it normally on the phone. Confirm another subdomain retains analytics.

That establishes the intended behavior. It does not independently prove that visitor data would never be useful.