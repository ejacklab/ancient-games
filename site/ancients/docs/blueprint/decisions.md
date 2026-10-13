# Decisions

Append only. Template: workflow-design assets/templates/blueprint.md.


## D1 — Keep Cloudflare Web Analytics on ancients.ejai.ai (2026-10-13)

- **Context:** after the live deploy, test N2 failed: Cloudflare Web Analytics on the `ejai.ai` zone (auto-install,
  rule host `*`, created 2026-01-22) injects `static.cloudflareinsights.com/beacon.min.js` and posts to
  `/cdn-cgi/rum`. The workers.dev preview had neither. Evidence: `runs/20261013-ancients-page/nodes/P5-deploy.txt`.
- **Options put to EJ:** (1) exclude only `ancients.ejai.ai` from the analytics rule; (2) keep analytics and widen N2.
- **Decision (EJ, verbatim):** "Cloudflare analytics on ancients.ejai.ai can keep".
- **Consequence:** N2 now allows those two addresses and nothing else; the zone's analytics setting is unchanged;
  the test allows exactly the beacon host and the page's own `/cdn-cgi/rum` path.
