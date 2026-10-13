# Codex review brief — the top 12, second engine

You are an independent reviewer for EJ's Ancient Games project. Another engine (opencode, MiniMax) researched ONE
person and produced their **top 12 mindsets, decision rules or algorithms**. Review it. You are read-only: write
nothing; your final message is your review.

Read:
- the list under review: `runs/20261013-four-seats/top12/<seat>.md` (named in your seat brief)
- the source texts: `runs/20261013-four-seats/sources/<seat>/` (see `sources/README.md`; in the Chinese wikitext,
  `{{*|…}}` is a commentator's note, not the main text). Search them with `grep`/`rg`. You have no web access; if a
  quote's source is not in this folder, say "not checkable here", do not guess.

For each of the 12 items, judge four things:
1. **Quote** — are the quoted words in the source, and spoken by this person (not a commentator, historian or
   another speaker)?
2. **Step** — does the plain-English rule actually follow from the quote, or does it add something the quote does not
   say? This is the main question: a rule that reads well but is not in the words is the failure we are looking for.
3. **Kind** — is "mindset / decision rule / algorithm" right?
4. **Rank** — is it in the right place, or merged with / duplicating another item?

Also check the file's **Gaps** and **Review of the top 10** sections for any claim that the source texts contradict.

## Write exactly this (Markdown, no preamble)

# <seat> — codex review of the top 12

## Per item
| # | Quote | Step | Kind | Rank | Verdict | Why (cite source line or text) |
|---|---|---|---|---|---|---|
One row per item. Quote/Step/Kind/Rank: `ok` · `issue` · `not checkable`. Verdict: `keep` · `change` · `drop`.

## Claims elsewhere in the file that the sources contradict
- ... (or "none found")

## Missing
Anything this person is clearly known for deciding by, that the 12 leave out — only if the source texts here show it.

## Overall
Two or three sentences. Label each conclusion `quoted`, `my reading` or `not measured`.
