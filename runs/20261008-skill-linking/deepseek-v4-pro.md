# Should the skills link to the WHOLE Ancient Games, not just the workflow-design method?

## 1. Divergence

**1a. Stale reference: `workflow-authoring` does not exist.**
`.claude/skills/workflow-design/SKILL.md:3` ("the Workflow script API (use workflow-authoring)") and
`.claude/skills/workflow-design/SKILL.md:124` ("`workflow-authoring` is the script API"). No directory named
`workflow-authoring` exists in `~/skills/`, `~/.claude/skills/`, `~/.agents/skills/`, the harness preset skills, or
the repo. (The other four "Related skills" targets resolve: `challenge-mediation`, `task-decomposition-strategies`,
`agent-loop`, `chronos-ledger`.)

**1b. The checklist exists twice, and `workflow-design` points at the file, not the skill.**
`workflow-design` `SKILL.md:96-102` ("Writing a rule down") sends the reader to
`docs/research/20261005-requirement-statements/FINDINGS.md` (§2). Those same eight questions *are* the
`requirement-check` skill (`~/skills/requirement-check/SKILL.md:14-34`), and `FINDINGS.md:5-6` names the skill the
source of truth. `workflow-design`'s "Related skills" (`SKILL.md:119-124`) omits `requirement-check` and
`meaningful-names` entirely. So the framework's own skill keeps its own copy of a rule whose packaged, single-copy
form lives in another skill, and the two do not cross-link.

**1c. `requirement-check` weak-words list drifts from its cited source and from `CLAUDE.md`.**
`~/skills/requirement-check/SKILL.md:27` lists *logical* and *reasonable*. Its cited origin
`docs/research/20261005-requirement-statements/FINDINGS.md:100-101` lists *if possible* and *etc.* instead;
`CLAUDE.md:80` lists neither pair ("…logical, fast, enough, only has to, TBD"). Same rule, three wordings. Minor but
it is exactly "a rule stated differently."

**1d. `requirement-check` "Can it fail" adds `0`.**
`SKILL.md:25-26` adds "`0`" to the failing inputs; `CLAUDE.md:79` and `FINDINGS.md:97` say only
`TBD`/`—`/empty. Trivial drift.

**1e. `meaningful-names` cites the Ancient Games referee without naming it.**
`~/skills/meaningful-names/SKILL.md:58` ("from this project") and `:80` ("this project's own") use the referee's
"one word, one job" split (`check`→`validate`→`verify`→`probe`→`compare`, matching `docs/WORKFLOW_DESIGN_METHOD.md`
Appendix A). For a global skill the referent is unnameable. Not a contradiction — an unnamed provenance.

Not divergences: `workflow-design`'s `docs/blueprint/` references (`SKILL.md:43-44,66-67,108`) are correctly scoped
to the *product's* repo (`docs/WORKFLOW_DESIGN_METHOD.md:108-109`), not this one. The five stage names are consistent
between the brief and `CLAUDE.md:51-52`.

## 2. The linking claim

**Half right.** The author is right about `workflow-design` and wrong about "the skills" as a set.

- **Right:** `workflow-design` *is* the method packaged (`CLAUDE.md:13-15,44-45`), and it under-links. Its own body
  never names the referee or the five stages, yet the method it links to already borrows referee fields
  (`docs/WORKFLOW_DESIGN_METHOD.md:287-293`, "Borrowed from Ancient Games": `KNOWN_FACTS`, `READ_SCOPE.deny`,
  `INTENT`/`STOP`/`OUTPUT`/`SCOPE`, `CLAIMS`/`VERIFY_OUTPUT`/`NOT_ESTABLISHED`, the journal) and cites referee code
  (`:245-248`, `ancient_games/stages.py:109`, `ancient_games/registry.py:24`). The skill presents a *method* whose
  check half (the referee that "clears the plan") is invisible from the skill's own text. The only framework mention
  is the run-folder line (`SKILL.md:109`).
- **Wrong:** the claim does not generalise. `requirement-check` is deliberately self-contained — the decision is
  recorded: "a global skill cannot depend on a path inside one project"
  (`docs/research/20261005-requirement-statements/FINDINGS.md:9-10`). `meaningful-names` is generic Clean Code with a
  borrowed worked example. `coding-discipline` (`~/.agents/skills/coding-discipline/SKILL.md:8-9`), `agent-experience`
  and `cordis-*` are harness skills with no relationship to Ancient Games. Linking these to the framework would be
  wrong.

## 3. The right structure

**Link proportionally to membership, and separate *membership* from *origin*.** The proposed "every skill opens with
'this is part of the Ancient Games: method / referee / knowledge'" is wrong — only one skill is a *part* of the
framework.

- **`workflow-design` — the only member.** Open with one pointer block: this is the *method* half of the Ancient Games
  framework; the *referee* (`ancient_games/`, which clears the plan) and the *knowledge* (`docs/`) are the other
  halves; `CLAUDE.md` is the map. Then keep the existing method links. Also fix 1a/1b: replace `workflow-authoring`
  (or create it), and point "Writing a rule down" at the `requirement-check` skill (add it and `meaningful-names` to
  "Related skills").
- **`requirement-check`, `meaningful-names` — origin pointer, not membership.** Keep the one-line origin
  (`requirement-check/SKILL.md:81` already has it; `meaningful-names/SKILL.md:58,80` should name Ancient Games instead
  of "this project"). Do not link the whole framework; that would break the recorded self-containment decision.
- **`coding-discipline`, `agent-experience`, `cordis-*` — no link.** They are harness skills, not framework parts.

A skill should point at the framework parts it *consumes*: `workflow-design` consumes all three (method, referee
fields, knowledge), so it links all three; the other two consume only their own origin, so they link only that.
