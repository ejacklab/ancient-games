Status: settled (accepted by EJ on 2026-10-13)
Drawn from: 02-requirements.md R6; 08-non-functional.md N2, N3

# Architecture

- **Build:** `site/ancients/build.py` reads `content/ancients.json` and writes one self-contained file,
  `dist/index.html` (Markdown rendered at build time with markdown-it-py; CSS and JS inline). (R6, N2)
- **Content:** `content/ancients.json`, made by P1 and checked by `tools/check_content.py`. (R5)
- **Tests:** `tests/test_mobile.py` (Playwright, Python). (R1–R5, N1)
- **Host — decision record:** a Cloudflare Worker named `ancients` returns `dist/index.html` for every GET, on the
  Workers custom domain `ancients.ejai.ai`. *Why:* the `ejai.ai` DNS is already on Cloudflare and the Cloudflare API
  works from this machine as EJ's account (readiness 2026-10-13); a custom domain creates its own DNS record and
  certificate. *Rejected:* Firebase Hosting like `ejai.ai` (CLI not logged in; needs a DNS verification step);
  Cloudflare Pages (needs wrangler or a direct-upload client not installed here). (N3)
