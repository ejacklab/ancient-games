# Leftovers run — report (P7)

EJ's request (2026-10-17T15:13Z): "design a workflow to complete all these left over within 3 hours , 3 rounds".
Design: `leftovers-design.md`. Clock: guard deadline D-148e43dc, 15:13Z to 18:13Z. A round is one pass over the
open items (the COO's reading, provisional). The decisions taken in place of EJ's are in `decisions.md`; EJ may
overrule each one.

Labels on conclusions: *measured*, *my reading*, or *not measured*.

## Requirements

| Req | Status at the end | Rounds | Builder | Evidence |
|---|---|---|---|---|
| R1, R2, A5 | MET, no regression in any round | closed before | — | every round check's `--met` |
| A3 | **MET**, closed at round 1, no build needed | 1 | — | `p3/A3-ar1/` |
| L1 | **MET**, closed at round 1 | 1 | opencode, 521 s | `p3/L1-ar1/` |
| A2 | **MET**, closed at round 2 | 2 | opencode (round 1, then the nested-inline fix in round 2) | `p3/A2-ar1/`, `p3/A1+A2+R3-ar2/` |
| A1 | **MET** on the fixtures, the held-out copy and the private opencode cases; closed at round 3 | 3 | opencode (round 1), dsh (round 2), opencode (round 3) | `p3/A1-ar1/`, `p3/A1+A2+R3-ar2/` |
| R3 | **MET** (tool part), closed at round 2 | 2 | — (tool part unchanged) | `p3/R3-ar1-interference/` (void), `p3/A1+A2+R3-ar2/` |
| A6 | **NOT MET** (*measured*): on the final maps, of 188 key claims 107 held (was 82), 41 limited (17), 27 missed (68), 1 wrong (10) | — | — | `p4/judge-*.md`, `p4/judge-final-*.md` |
| L2 | **reported** (round 1 only) | — | — | `p5/l2-report.md` |

## The measurements

- **L2, the map against reading** (`p5/l2-report.md`, *measured*, n = 1 per arm): the map arm was not better.
  - Correct claims: 166 for the map against 172 for reading.
  - Tokens: about equal.
  - Time: the map arm took 2.2 times longer, because the tool rebuilds the type program on every call.
- **P6, integration in a design run** (`p6/p6-report.md`, *measured*): the code-map skill was offered in three design
  runs and never used. The agents explored by reading and grep.
- **P4, maps against the keys** (`p4/judge-*.md`, *measured* on the A5 tool):
  - Of the keys' claims, 82 of 188 held, 17 were limited, 68 missed and 10 wrong.
  - The fault shapes the judges found became A1's round 1 to 3 tests.
  - On the final maps the judges ran again (`p4/judge-final-*.md`): 107 of 188 held, 1 wrong.
  - Still missed with no limit naming why: test reach is not in a map, the ai map does not say packages/core is
    outside its scope, constants and interfaces are not definitions, and one link resolves to a fallback stub only.

## Builder comparison (EJ's request)

`builds/a1-compare.md`. On A1 round 1, opencode and dsh came out level on every check that can fail:
- 293 tests;
- tsgo 0;
- the evaluator;
- the held-out copy, 61 of 70;
- the private core set, 6 of 8.

On real opencode, dsh resolved more links in session (1,327 against 1,267) and opencode more in ai (3,617 against
3,478). The COO picked opencode for round 1. dsh then built A1 round 2 (476 s), and its change merged cleanly with
opencode's L1 change.

## Decisions taken for EJ (provisional; `decisions.md`)

All six experts answered (`experts-leftovers/compare.md`). The COO's picks, in short; the full text is in
`decisions.md`:
1. **A link marked `dynamic`** is not missing when a limit at its site names why. But a limit that contradicts the code
   fails.
2. **Going into a body written straight into a call** adds no level.
3. **"Known"** means "established from repository source or type information". The experts split 3–3 on this.
4. **The interface-required-limit clause:** A5 does not add it.
5. **Layout:** a tool line and an agent line, inside one A2 and one A5.
6. **The fake rule on opencode:** this run passes no `--fake-rule`, so fake-path tests are listed, not counted.
7. **The sibling rule:** one glob per group, chosen by the service-tag rule.
8. **Test files:** the tool has no default. On opencode, the run passes `test/`, `__tests__`, `*.test.ts` and
   `*.spec.ts`.

## What went wrong (logged; `insight.md`)

- **F-d325a7cc.** R3's first check was made void by my setup. The build copies share `node_modules` with
  `code_map/`, and my briefs pointed their output there. Fixed for later briefs.
- **F-f91899ca.** A private case expected a call one level too deep. It was my second case error; the case is
  corrected.
- **Evidence only (R12.2), not failures:**
  - Codex hit its usage limit at 15:35Z, until 20:00Z. Test writing moved to Claude subagents.
  - opencode ran `git stash` and then `git stash pop` during the A2 build. Nothing was lost; later briefs forbid git.
  - The first P5 run used an API key with no credit.
  - Test writers' fixtures failed tsgo three times. The COO fixed each one on the same lines, and the originals are
    kept in `staging/`.

## Not done, and why

- **Source plants** for A1, A3, L1 and R3, and the **expert reviews** (孫子, 范蠡) of each round. Only A2 got plants
  (5 of 5 caught; `evidence/p3-a2-src-plants.txt`). The round checks, held-out sets and private cases ran for every
  close.
- **P5 rounds 2 and 3**: improve the map, then rerun. The main lead is that the tool rebuilds the type program on
  every call.
- **P6 round 2**: an arm told to use the skill.
- **A6**: the four gaps above.
- **Privacy exposure, found while preparing the commit.** My held-out checks and plants ran beside the builds, so the
  builders could see the private paths in the process list. Three build logs name them. No builder log shows a file
  there being read (grep of all nine build logs). Those three logs are kept out of the commit. From now on: no
  held-out run while a build runs. *My reading:* the held-out sets are probably not contaminated, but that is not
  proven.

## For EJ

- Overrule any decision in `decisions.md`. The requirement wording is still yours. The proposals are its rows 1–5.
- Nothing is pushed. The run is in one local commit on master, titled "code-map: the leftovers run"; push waits for you. The R3 test fixture holds a labelled fake key (`sk-live-R3-private-ledger-DO-NOT-EXPORT-…`) that GitHub push protection might flag.
- Waiting for you, unchanged:
  - deleting the private POC folders and session logs;
  - the Source lines in `REQUIREMENTS.md` and `CODE_GRAPH.md`;
  - the four-experts slug fix;
  - the tool's name and location, languages, and `tools/` vs `tools/ts/` (provisional assumptions still in force).

## Score against the criteria written before the work

`criteria-leftovers.yaml`: **9 of 11 met (82%)**, an aim, not a gate. The two not met:
- **C8:** P6 had no blind judge. The skill was never used, so the arms did not differ.
- **The tests item:** mutants ran for A2 only, and A3's and R3's tests passed on the old code from the start.
