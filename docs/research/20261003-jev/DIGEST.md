# Digest — Jev (TypeSafe) on the fork layer (2026-10-03)
Full findings: `FINDINGS.md` (same folder). Status: **open** — nothing run.

**Answer.** Jev is TypeSafe AI's typed-decision model (released 2026-09-15): it answers yes/no, choice and score questions about a state you send, with probabilities and a confidence, in about 100 ms, at $0.042 per million input tokens; it writes no text or code. A "fork" is a decision point in a multi-agent flow — who acts next, is the research good enough, is the objective done, may this action proceed, is this command safe. Your friend's layer most likely uses it for the routing fork. It fits our dispatcher layer and the classification row, not checks: its own site says the answer may be wrong and routing accuracy has no published benchmark.
**Confidence.** 13 findings: 12 reported (summaries of a vendor-adjacent site, a blog, a plugin README; vendor numbers unverified), 1 unknown; nothing verified or run.
**Cautions.** Hosted API only, so the state leaves the machine. Weak at numbers, dates and counting. Use with a confidence threshold and fail-open to the COO, never as the check itself.
**Gaps.** No primary docs read; accuracy on our task labels unknown; no API key checked.
**Decision it triggers.** EJ: whether to trial Jev on the 300-prompt corpus with `corpus_check.py` (cost about a cent; needs an API key and agreement to send those prompts to a hosted API) against codex 96% and agy 76%.
