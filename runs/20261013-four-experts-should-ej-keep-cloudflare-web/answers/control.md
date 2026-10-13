# Control — Keep Cloudflare Web Analytics on ancients.ejai.ai?

## Answer
Turn it off for ancients.ejai.ai only (the one-hostname exclude rule). Keep it only if EJ decides they want visitor numbers for this page — and if so, widen N2 deliberately and in writing, rather than letting the requirement quietly bend to a setting that came from elsewhere.

## How I decided
1. **The page has a requirement that settles this unless someone changes it.** N2 says "no network request except Google Fonts, no cookies — one file, no tracking." The analytics script adds two requests (the script from static.cloudflareinsights.com and the beacon to /cdn-cgi/rum). So the page as served breaks N2 today. Setting no cookie only satisfies half of N2; the request part is still broken.
2. **Nobody chose analytics for this page.** It arrived through a zone-wide rule from 2026-01-22, before this page existed. N2 was the decision made for this page. When a page's own requirement conflicts with a blanket default, the page-specific decision should win unless someone overrides it on purpose.
3. **There is no benefit to keeping it right now.** EJ has no stated plan to look at the numbers. Collecting data nobody reads has no upside, while the page still pays for the extra script, the third-party request, and the broken "no tracking" claim.
4. **Turning it off is cheap and reversible.** One exclude rule, other subdomains untouched, and it can be undone by deleting the rule.
5. **The possible future sharing raises the stakes for "off", not "on".** Once other people read the page, "no tracking" becomes a promise to them, not just a description of EJ's own reading.
6. **So the default is off.** The one thing that would flip it is EJ deciding they want the numbers (see below); even then, the right move is to change N2 first, then keep it — not to leave the conflict standing.

## What I need to know
- **Does EJ want to know how many people read the page once it is shared?** If yes, keeping analytics is reasonable — provided N2 is reworded (e.g. "no request except Google Fonts and Cloudflare Web Analytics, no cookies"). If no or not yet, turn it off.
- **Does the page itself tell readers "no tracking"?** If it does, keeping analytics makes a visible statement false, which makes "off" close to required unless the wording changes too.
- **Is the hostname proxied through Cloudflare?** The /cdn-cgi/rum request suggests it is, but that is my reading, not a given fact. If so, Cloudflare's dashboard may already show basic request counts without any page script, which would remove most of the reason to keep the script — but I have not checked what those counts show.
- **Will the zone-wide rule be edited later?** If someone rewrites or replaces it, the per-host exclude could be lost or overridden. I do not know how Cloudflare orders these rules, so treat this as a question, not a fact.

## Costs and risks
- **Turning it off:**
  - You lose visitor data for this page from now on. If EJ later wants to know how a share went, there is no history for the time it was off.
  - One more rule lives in the Cloudflare config, and someone has to remember it exists and why.
  - Small risk the exclude rule is set up wrong (wrong hostname, or it does not apply) and the script silently stays on.
- **Keeping it:**
  - The page breaks its own N2 unless N2 is reworded. A reworded N2 sets the precedent that a requirement yields to whatever the infrastructure already does.
  - Each visit makes a third-party script request plus a beacon. Cloudflare receives each reader's request, even without a cookie.
  - If the page or its README ever says "no tracking", that becomes false — which matters once others read it.
  - Small page-weight and load-time cost on a phone (not measured).
- **Doing nothing (keeping it without changing N2):** the requirement and the deployed page silently disagree. This is the worst option, because the next person to read N2 will trust it and be wrong.

## How we would know I was right
- **Direct check after the change:** load https://ancients.ejai.ai on a phone or desktop with the network panel open. No request to static.cloudflareinsights.com and none to /cdn-cgi/rum; the only third-party requests are to Google Fonts; no cookies set. Load one other ejai.ai subdomain the same way and confirm its analytics script is still there.
- **N2 passes as written,** with no rewording needed.
- **Over time:** if after the page is shared EJ never asks how many people read it, "off" cost nothing. If EJ does ask and wishes they had the data, the call was wrong for their needs — and the fix is to delete the exclude rule and widen N2, both minutes of work.

<!-- saved by the main session from a Claude subagent (Opus 5.5) run via --claude-by-caller; pronouns for EJ changed from he/his to they/their; otherwise as returned -->
