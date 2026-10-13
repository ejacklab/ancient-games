# Brief — plain answer (the control)

Answer the question below as yourself, with no persona and no borrowed rules. Your answer is the **control**: EJ
compares it with four experts' answers to see whether the experts added anything a plain answer does not.

## The question

Should EJ keep Cloudflare Web Analytics on ancients.ejai.ai, or turn it off for that page only?

Facts:
- ancients.ejai.ai is a single public reading page (four historical figures' decision rules) that EJ reads on a phone. It has no login, no forms, no ads, and nothing is sold.
- The page's own requirement N2 said: no network request except Google Fonts, no cookies — "one file, no tracking".
- Cloudflare Web Analytics is switched on for every subdomain of ejai.ai (one zone-wide rule since 2026-01-22). On this page it adds a script from static.cloudflareinsights.com and a request to /cdn-cgi/rum. It sets no cookie.
- Turning it off for this page only is one exclude rule for this hostname; other subdomains keep analytics. Keeping it means widening N2.
- EJ has no stated plan to look at the page's visitor numbers. The page may later be shared with others.

## How to answer

1. Answer directly, with your reasoning in numbered steps.
2. **Do not invent facts.** If the answer depends on something you were not given, list it under "What I need to
   know" and answer conditionally: "if … then …".
3. Say what each recommendation costs or risks.
4. Write in plain English Markdown. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# Control — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps>

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each risk or price>

## How we would know I was right
<a test, a measure, or an observable result>
