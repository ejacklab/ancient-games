# Step 1 (Readiness) — four-engine review, 2026-10-04

Reviewing `.claude/skills/workflow-design/SKILL.md` step 1 against the step it is supposed to be: is it correct,
complete, and consistent with its own method, script and template?

## How it was run

Four engines, **blind to each other**, all read-only, given one brief (`brief.txt`) naming the five artifacts that
*are* step 1 and nothing else:

| engine | model | mode | time | findings |
|---|---|---|---|---|
| codex | `gpt-6.1-sol` | `-s read-only` | 101 s | 4 |
| claude | `claude-opus-5-5` | `--permission-mode plan` | 79 s | 10 |
| opencode | `MiniMax-M3.1-Flash-Preview` | `--agent plan` | 234 s | 10 |
| **agy** | `gemini-3.8-flash-high` | `--mode plan` | 12 s | **0 — produced nothing** |

**agy failed, and its reason matters.** Exit 0, empty stdout, and this on stderr:

> a tool required the "command" permission that headless mode cannot prompt for, so it was auto-denied. Add an
> allow-rule under permissions.allow in settings.json … Alternatively, re-run with `--dangerously-skip-permissions`

So under `--mode plan`, headless, agy cannot read files at all without an allow-rule — and the suggested escape is
the flag [EXECUTOR_KINDS](../../docs/EXECUTOR_KINDS.md) rule 3 forbids. Rule 2 routes `repo scanning`, `web search`
and `research and reports` to agy; this says agy cannot do a read-only review headlessly as configured. **That is a
routing finding in its own right, independent of step 1.**

## The join

Every finding had to carry a file:line and a quote copied verbatim. `verify.py` checks each quote against the named
file and discards anything it cannot find.

**24 findings, 24 quotes located, 0 fabricated.** All three engines quoted accurately, which is worth recording:
these are not hallucinated reviews. `verify.py`'s clustering was too coarse to claim corroboration (it merged
different findings that happened to cite the same line), so the join below is by hand, as the method requires.

One caveat before reading them: **a verifier that reviews its own author's work is not a verifier.** Two of the
sentences under review were written by me today, so I checked every high finding by re-reading the code and, where
possible, by re-running it. Findings I have not independently checked are marked *(unchecked)*.

## Confirmed — defects in the script

**1. The blueprint check cannot fail.** `readiness.py:197-205`

```python
if not p.is_dir():
    return Check(..., MISSING, "directory not found", ...)
...
return Check("Skills and workflows", item, VERIFIED,      # <- always VERIFIED if the dir exists
             f"{len(files)} sections, map {'present' if has_map else 'MISSING'}: ...")
```

A blueprint directory that exists is **always `VERIFIED`**, even when the script's own detail string says
`map MISSING` or `0 sections`. `exit_code` only fails a blueprint when the *directory* is absent, and `--self-test`
never calls `check_blueprint` at all — it exercises `check_binary` only. So the one check whose job is "is the
blueprint there and complete" cannot report anything but success. This is the house rule broken: *proof each script
check can fail*. Found by opencode; corroborated by claude from the other side (`:204`, the README-map count).

**2. Absent and empty directories report `verified`.** `readiness.py:184` — `absent_status: str = VERIFIED`, and
two of its callers use the default. Verified by **running it** in an empty directory:

```
| project skills    | verified | absent (/tmp/..../.claude/skills)    |
| workflow scripts  | verified | absent (/tmp/..../.claude/workflows) |
| project instruction files | verified | present: none; absent: CLAUDE.md, AGENTS.md, ... |
```

rc=0. A project with no skills, no workflows and no instruction files passes readiness **entirely verified**.
Readiness is the step whose whole job is separating *verified* from *unknown*, and it reports *verified* for things
that are not there. Found by opencode; claude reached the same family through the template (`readiness.md:9`).

**3. `--require` passes a tool that is `UNKNOWN` rather than `MISSING`.** `readiness.py:326` —
`if r in missing or r not in known: return 1`. `check_binary` returns `UNKNOWN` on a timeout or a non-zero exit, so
a tool that is present-but-broken satisfies `--require`, which exists to prove a tool works. Found by codex.

**4. "N sections" is not the section count.** `readiness.py:204` counts every `.md` in the directory — the README
map, `backlog.md`, `decisions.md`, `changelog.md`, `lessons.md` — not the eight blueprint sections the method
defines. Found by opencode (high) and claude (low).

## Confirmed — my own edit contradicts itself

**5. `SKILL.md:51` and `:54` disagree.** The two sentences I added today:

- `:51` — *"Prove the binary that will make the call, and record its version — **not the version on `PATH`**."*
- `:54` — *"**Call the CLI first** … the binary on `PATH` is the one that updates."*

If the CLI is the caller, the `PATH` binary **is** the binary that will make the call, and its version is exactly
what should be recorded. The "not on `PATH`" clause is only true of *provider* calls, which is what the rest of the
paragraph is about. Found by claude (high) — and it is the single clearest thing this review produced, because I
wrote both halves and did not see it.

**6. The method never got either rule.** Method 3.1 (`docs/WORKFLOW_DESIGN_METHOD.md:72-167`) contains neither
sentence, so the skill's step 1 and the method it defers to now say different things about readiness. Found by
claude. Confirmed by construction: I edited only `SKILL.md`.

## Confirmed — vocabulary that does not match

**7. Four statuses in the script, three in the skill, two in the template.** `readiness.py:41-44` defines
`verified`, `reported`, `unknown` and `MISSING` (note: the fourth is upper-case, the rest lower). `SKILL.md:46`
promises three. `workflow-templates/readiness.md:9` offers a Result column of "works / missing" and has no version
column at all — which is also why finding 5's "record its version" has nowhere to go. Found by opencode (two
findings) and claude (one), from three different artifacts.

## Plausible, not yet checked by me

- `readiness.py:139` — any `rc == 0` with non-empty output counts as a verified model list, so `Please log in`
  would verify a model. *(codex)*
- `readiness.py:163` — a non-object `model` value raises an uncaught `AttributeError`, aborting the inventory
  instead of reporting `UNKNOWN`. *(codex)*
- `WORKFLOW_DESIGN_METHOD.md:156` — a blueprint piece "drafts the section from the sections above it", which sits
  awkwardly with line 115's *"An agent may only write down what EJ has said"*. *(codex)*
- `SKILL.md:47` — "what it cannot prove stays unknown and needs the canary" is not true of every unknown; the agy
  model list is settled by re-running with `--net`. *(opencode)*
- `SKILL.md:58` — readiness is told to require every node's role, engine, exact model and effort, but nodes do not
  exist until steps 2-6. *(claude)*
- `SKILL.md:62` — the skill gives the blueprint layout as `blueprint.md` but never names the map
  `docs/blueprint/README.md` that the method requires and the script checks. *(claude, opencode)*
- `readiness.py:47` — `check_dir_listing` also reports `verified` for an *empty* directory, not just an absent one.
  *(mine, from reading — the same root cause as finding 2)*

## What this says about the step, not just the bugs

Step 1 is the step that decides whether a run may start, and its two centrepieces — the blueprint check and the
inventory's status vocabulary — both report success in cases where nothing was proved. The prose is in better shape
than the code: three of the four script defects are the same mistake (a status that cannot express "absent" or
"unknown"), and the skill text inherited the confusion rather than causing it.

The one prose defect that matters most is mine: two sentences added hours apart, each true on its own, contradicting
each other when read together.

## Files

- `brief.txt` — exactly what all four engines were given
- `run.sh` — the four calls, with the read-only mode and model for each
- `verify.py` — quote verification and the (too coarse) clustering
- `codex.md`, `claude.out`, `opencode.out`, `agy.err` — raw, unedited

## Not done

Nothing was fixed. This is a review, and the step needs a decision before editing: which of the confirmed items to
change, and whether step 1's rework belongs before or after the other seven steps are reviewed the same way.
