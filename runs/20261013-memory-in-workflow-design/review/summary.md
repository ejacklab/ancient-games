# Review of the §4 memory change — four experts

COO (Claude `claude-opus-5-5`), 2026-10-13. Answers in `experts/answers/`. Engines: 范蠡 agy (gemini-3.8-flash-medium),
孫子 dsh, 老子 opencode, **Linus on a Claude subagent** (codex hit its usage limit until 23:27; `logs/linus.log`).
`four_experts.py check`: only "dave: no answer file" (not run). The check was written by Claude; it does not establish
that the advice is right.

**Verdict: all four "accept with changes".** None rejects. All agree on the shape: memory in the node's own fields,
delivered not asked, pointing to the two designs.

## Found by the reviewers, checked by the COO
- `docs/TASK_TYPES.md` L234, 237, 262, 274 still send decisions to `decisions.md` (孫子, 老子, Linus). Verified, grep.
- **Two live products still use the three files**: SEZA (`~/dev/seza/docs/blueprint/` has decisions, changelog,
  lessons) and `site/ancients/docs/blueprint/` (all three). Neither has `project-memory/`. Verified, ls (Linus).
- Contract row would make a build node report its own unfinished work as a mismatch; SoT Rd5.4 exempts it (老子,
  Linus). Verified.
- Context row: "by a start hook" breaks SoT: Rd2.2 puts entry bodies on demand, and Rd2's check fails on a hook
  loading memory outside Rd2.1 (Linus). "never as a sentence" is stricter than SoT Rd2.1, which keeps it as fallback
  (老子, Linus, 孫子). Rd4.1 (read entries covering a file before editing it) is missing (范蠡, Linus).
- State row: journal write is K5.1; end-of-task lessons are W5.2; K5.2's logged read is missing; "check fails if a
  required one is missing" is the method's own rule, not the design's (Linus, 孫子).
- Tools row: full-text and vector have separate questions and triggers (B1.1, B1.2; vector proposed) (老子, 孫子,
  Linus).

## The two calls
- **(b) 老子's rule and Linus's contract left out: keep** (all four). Linus and 老子 note the four rows *are* the
  per-node contract.
- **(a) `changelog.md` dropped:** 孫子, 老子, Linus: right for a product on `project-memory/`, but release notes lose
  their only source. 范蠡: restore it. Linus: a transition line so SEZA and `site/ancients` keep their files until EJ
  moves them.

## For EJ
1. Transition: SEZA and `site/ancients` keep their three files until you move them (Linus's change 1)? 
2. Release notes: still wanted, and from what?
3. (Linus) Does a brief carrying an entry's text break SoT Rd2's "no instruction loads memory outside Rd2.1"?
