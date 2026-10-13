Status: settled (accepted by EJ on 2026-10-13)
Drawn from: 01-vision.md

# Non-functional

- **N1** — S25 Ultra size: tests run in Playwright Chromium with viewport 412 × 915 CSS px, device scale factor 3.5,
  `is_mobile` and `has_touch` on, an Android Chrome user agent. These numbers are model knowledge (unclear spot U5),
  not measured; EJ's phone is the final check (P4).
- **N2** — One file, no other requests: the page makes no network request except its own document, Google Fonts
  (`fonts.googleapis.com`, `fonts.gstatic.com`) and Cloudflare Web Analytics, which Cloudflare injects on the
  `ejai.ai` zone (`static.cloudflareinsights.com`, and `/cdn-cgi/rum` on the page's own host). The test records
  requests; any other host or path fails. It sets no cookie (`document.cookie` empty; the live response has no
  `Set-Cookie`). *Changed 2026-10-13 — EJ: "Cloudflare analytics on ancients.ejai.ai can keep" (see decisions.md D1).*
- **N3** — The deploy changes nothing else: the body of `https://ejai.ai/` hashes the same before and after the
  deploy, and the zone's DNS records other than `ancients` are the same before and after.
