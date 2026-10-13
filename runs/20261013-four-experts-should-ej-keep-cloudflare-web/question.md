Should EJ keep Cloudflare Web Analytics on ancients.ejai.ai, or turn it off for that page only?

Facts:
- ancients.ejai.ai is a single public reading page (four historical figures' decision rules) that EJ reads on a phone. It has no login, no forms, no ads, and nothing is sold.
- The page's own requirement N2 said: no network request except Google Fonts, no cookies — "one file, no tracking".
- Cloudflare Web Analytics is switched on for every subdomain of ejai.ai (one zone-wide rule since 2026-01-22). On this page it adds a script from static.cloudflareinsights.com and a request to /cdn-cgi/rum. It sets no cookie.
- Turning it off for this page only is one exclude rule for this hostname; other subdomains keep analytics. Keeping it means widening N2.
- EJ has no stated plan to look at the page's visitor numbers. The page may later be shared with others.
