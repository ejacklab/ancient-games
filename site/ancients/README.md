# ancients.ejai.ai — the four seats, read like a Kindle page

One page: swipe left/right to change person (范蠡, 孫子, 老子, Linus Torvalds), scroll up/down to read their
mindsets, decision rules and algorithms. Built for a Galaxy S25 Ultra. Live at https://ancients.ejai.ai.

Spec: `docs/blueprint/` (start at `README.md`). Run that built it: `runs/20261013-ancients-page/`.

## Rebuild and test (after the lists in `runs/20261013-four-seats/final-opus/` change)

    make -C site/ancients          # extract → check quotes → build dist/index.html → 14 phone tests

Needs Python 3 with `markdown-it-py` and `playwright` (Chromium). Run without `python3 -I`.

## Deploy

    cd site/ancients && npx --yes wrangler@4 deploy --domain ancients.ejai.ai

Needs `npx --yes wrangler@4 login` once. Then check the live page:

    python3 site/ancients/tests/test_mobile.py --url https://ancients.ejai.ai/
