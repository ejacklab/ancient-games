# Blueprint — <product>

The layout of a product's blueprint. It lives in the product's repository under `docs/blueprint/`. Method:
`docs/WORKFLOW_DESIGN_METHOD.md` §3.1, blueprint check.

## Files

```
docs/blueprint/
  README.md              the map: one row per section, where it lives, its status
  01-vision.md
  02-requirements.md
  03-domain-model.md
  04-business-logic.md
  05-architecture.md
  06-data-model.md       data model, schema design and its decisions
  07-ui-ux.md
  08-non-functional.md
  backlog.md             findings outside the requirements in scope; never worked on inside the run that found them
```

A section kept somewhere else (for example a project's own spec) is not copied: its row in the map points there,
and that project's rules on who may change it still hold.

## The map — `README.md`

| # | Section | Where it is | Status (settled / draft / missing) | Accepted by EJ on |
|---|---|---|---|---|
| 1 | Product vision | 01-vision.md | | |
| 2 | Core requirements | 02-requirements.md | | |
| 3 | Domain model | 03-domain-model.md | | |
| 4 | Business logic | 04-business-logic.md | | |
| 5 | System architecture | 05-architecture.md | | |
| 6 | Data model and schema decisions | 06-data-model.md | | |
| 7 | UI / UX design | 07-ui-ux.md | | |
| 8 | Non-functional requirements | 08-non-functional.md | | |

## Every section file starts with

```
Status: draft | settled (accepted by EJ on YYYY-MM-DD)
Drawn from: <the sections above it that this one serves, e.g. 02-requirements.md R1–R4>
```

Only EJ changes a status to settled. An agent that drafts or edits a section sets it to draft.

## Headings per section

- **01 Product vision** — who it is for; the problem it solves; what it will not do; how we know it works.
- **02 Core requirements** — one block per requirement:

  ```
  ### R1 — <name>
  <what the product must do, in one or two sentences>
  Acceptance criteria:
  - R1.1 <an observable check: a command and its result, or a behaviour someone can see>
  - R1.2 …
  ```

  A criterion that cannot be checked is not a criterion yet; it is a question for EJ.
- **03 Domain model** — the entities, their relations, and the words used for them; each entity names the
  requirements that need it.
- **04 Business logic** — the rules and flows, each naming the requirement it serves and the entities it uses.
- **05 System architecture** — the parts, how they talk, where each runs; each choice with its reason and the
  requirement or non-functional target that drove it.
- **06 Data model and schema decisions** — tables or documents, fields, keys, migrations; one line per decision with
  its reason and the alternative that was rejected.
- **07 UI / UX design** — screens or commands, the flows through them, each naming the requirement it serves.
- **08 Non-functional requirements** — performance, security, cost and operating limits, each with a number or a
  check (N1.1, …), in the same shape as the acceptance criteria.

## Backlog — `backlog.md`

| Date | Run id | Found by | What | Why it is out of scope (no criterion in scope covers it) |
|---|---|---|---|---|
