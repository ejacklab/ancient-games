# One round over everything — 2026-10-05

EJ: *"let's review everything 1 round, and I learn a lot also."* This is that round: every check run, every register
row read, and the findings written down rather than recalled.

## 1. Every check, and what it said

| check | result |
|---|---|
| `pytest -q` | **512 passed** |
| mutation matrix | **28/28 caught, 0 holes, 0 missed, 0 false alarms** |
| the matrix's own sabotage (`--self-check`) | **CAN FAIL** — every mutation neutered, 28 rules went unfired |
| `design_gate.py --self-test` | **PASS — the gate can fail** |
| intake harness (`intake_harness.mjs`) | **all passed** |
| citation check | 31 citations, **0 not traceable to the notes** |
| corpus over 300 prompts | **0 bugs** |
| `readiness.py --self-test` | **PASS — the check can fail** |
| survey check (`areas-survey.py`) | **FAIL — 4 issues missing: 10.1, 9.1, 9.2, 9.3** |

**The survey check is red, and correctly so.** It compares the surveys against the register's ids, and the register
has *grown* four ids since those surveys ran (all found later the same day). The check is doing its job — it caught
that the review artifacts no longer cover the register. Fixing it means re-running the surveys or freezing the id
list they were written against; not urgent, but it is a real inconsistency, not noise.

## 2. Which checks can prove they can fail

The day's whole subject. Measured across the skill's ten scripts:

| script | sabotage proof |
|---|---|
| `design_gate.py` | **28 mutations**, each aimed at a rule, plus a self-test |
| `readiness.py` | **self-test** — a fake tool reports MISSING and `--require` exits 1 |
| `dispatch.py`, `engines.py`, `workload.py`, `harvest_run.py`, `quote_check.py`, `runlog.py`, `validate_result.py`, `feature_gate.py` | **none** |

**Two of ten.** The tests cover much of the behaviour, but the specific discipline this project keeps demanding —
*prove the check can fail* — is applied to the gate and to readiness, and to nothing else. **`dispatch.py` guards
every run (`check_plan`) and has no self-test at all.**

## 3. The register, counted — and why it could not be counted

The register holds **49 distinct items** (45 in areas 1–8, plus 9.1–9.3 and 10.1 found later). Every row read, and
each assigned exactly one status:

| status | count |
|---|---|
| **fixed** | **28** |
| answered — by the code, or already stated in the method | 6 |
| withdrawn — false positives the moment the file was opened | 3 |
| deleted by decision (the fallback, the caps) | 2 |
| addressed (the mutation matrix) | 1 |
| downgraded (6.4 — mostly answered by 3.3's own `Blocks` column) | 1 |
| decided (10.1 — C) | 1 |
| answered but thin (5.2 — the missing-pass owner) | 1 |
| **open** | **6** |

**Closed: 43. Open: 6**, each verified by reading rather than recalled:

| # | what it is | why it is open |
|---|---|---|
| **1.5** | G2 reads `builds`/`touched_paths` from the design itself | **limited, not fixable as stated.** The only witness is git, and git is not a requirement — so it works where a repo exists and nowhere else. Recorded |
| **2.1** | the corpus is circular — designs emitted from the cells the gate parses | needs hand-authored designs |
| **2.2** | all 300 designs are `design_source: default` | **G5 (the 20% challenger rule) and G7 (the ledger) have never executed.** The largest real gap left |
| **2.4** | the checklist review layer — the semantic layer the file says catches what the script cannot — has never run | needs a run |
| **4.1** | the engine split exists **only in the skill** | verified: `METHOD.md` and `DIAGRAM.md` have **0** mentions |
| **9.1** | the gate cannot tell **which node writes** | work, not a question: `intake.js:201` already carries `builds` per piece, so the gate reading it is the "one shape" decision already made |

Two rows closed while checking them, and both are worth naming because they were on the "open" list until read:
**2.6** — `design_gate.py:100` parses `pattern` → `loop`, so the column is load-bearing now; and **4.6** — method 3.1
does carry skill step 1's two rules (*"each with the command that proved it works. Run it; do not assume"* and the
canary), so the register's claim was false.

**Why it could not simply be counted:** the register's rows are findings, and a row fixed later in prose does not
carry a marker. A regex over it reports 24 open where 8 are. **`open-defects.md` holds the status and the register
holds the evidence, and neither alone answers "what is left".** That is the defect I flagged mid-session, now
measured: a status that cannot be read is a status that cannot fail.

## 4. Found in this round

**A check that could not fail, in the ledger reader — fixed.** `parse_ledger` mapped the ledger's columns **by
position** and anchored only on the first header cell. So the header was decorative: swapping two columns parsed
cleanly and silently mis-assigned every field after them. Demonstrated — swapping *Claimed margin* and *Basis* turned
`claimed_margin` into the string `"default"` with no error anywhere.

It now checks the header against `LEDGER_KEYS`, and **the check immediately caught a real defect**: the shipped
ledger says `Coverage outcome` where the parser wants `coverage_result` — register **4.7**, open since the first
review. Fixed, and the header check is pinned with its own sabotage.

**`EXECUTOR_KINDS.md`'s concurrency row says "unknown" where the harness answers.** The readiness inventory prints
*"subagent concurrency limit | unknown | runtime policy, not provable from outside. Claude Code docs report 20
concurrent…"* — while this harness's own `@deepseek-ai/dsh-subagent` carries `maxActiveSubagents`, default **8**, and
`maxDepth` **1**, readable through the harness's inspect provider. The doc records another tool's number and calls
its own unknown.

## 5. Provenance, re-measured

| doc | normative lines | with a who, a when, a basis or a citation |
|---|---|---|
| `WORKFLOW_DESIGN_METHOD.md` | 109 | **19%** |
| `EXECUTOR_KINDS.md` | 100 | **42%** |
| `TASK_TYPES.md` | 78 | **26%** |

**Unchanged by a day of work** — and each fix today added more unsourced prose to the same files. Roughly three in
four rules still cannot be traced to a person, a date, or a measurement. EJ named this exactly: *"don't know who
write one, make things sounds weird later."*

## 6. What the day actually demonstrated

Six patterns, all of them the same shape underneath:

1. **A claim without a source cannot be checked, so it gets inflated.** Five register items were withdrawn the
   moment I read the file: 6.3, 6.5, 5.6's engine clause, most of §5, and 4.6. Each was presented as a design gap
   and each was a reading error.
2. **A number moved between units because the words looked alike.** The deleted caps rule took the spike rule's
   *approaches* numbers for a *roles* rule. I then repeated it, taking the harness's *resident sessions* number for
   an *OS processes* setting — an hour after deleting the first one.
3. **A check that cannot fail is indistinguishable from a check.** Found today in the ledger parser, in G3 (a
   non-empty check), in G11 (an em dash as an engine), in G12 (a placeholder), and in the corpus's circularity.
4. **The environment usually already owns the thing I proposed to build.** Three mechanisms were proposed and
   retired: the fallback (over-engineering), the plan-vs-design checker (one author), and a script to count my own
   dispatches (the harness enforces 8).
5. **Concurrency has four meanings and one vocabulary** — resident sessions, processes alive, candidate approaches,
   attempts. Naming the unit is the fix; there is no single "parallel".
6. **Checking is not recalling.** Every one of the six withdrawals above came from opening a file. None came from
   re-reading my own notes.

## 7. What is left

**The four §2 items are the substance**, and they are all one thing: **the corpus has never exercised G5 or G7.**
The gate gained a challenger rule and a ledger rule, and no design has ever made them fire outside a mutation. Until
a challenger design and a real ledger row exist, two of the gate's rules are unproven in the only way that counts.

Then: **4.1** (the engine split is in the skill and nowhere else), **9.1** (the gate reading `intake.js`'s per-piece
`builds`), the **survey check's red**, and the **provenance** the day did not move.

`512 passed` · `28/28` mutations, 0 holes · corpus 0 bugs · gate and readiness self-tests PASS.
