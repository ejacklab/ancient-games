# Four experts and Dave — "learn from the mistakes in a success, not from total failure"

Question: `../expert-question.md` (with the researcher's 50 findings). Answers: `answers/`. Web research allowed;
范蠡 and Dave ran on Claude for it (`--needs-web`).

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| One line | learn from a working path, but keep total failures that carry reproducible evidence; reuse unchanged allowed with a reason | holds for the path, breaks for readiness: a total failure teaches whether conditions were ready | the signal is a contrast between two attempts that differ in one step; recombine trusted steps from several successes | holds only if the in-success mistake is joined to its step; a pass/fail measure has no hill to climb | holds narrowed: near misses are the best teachers; total failures still teach (error text) |

## Where they agree (all five)
- **The principle holds in a narrower form: learning comes from a contrast** — a failing attempt next to a passing one
  of the same work (a near miss). A run where everything failed has no sibling to read against (researcher F1, F4).
- **"Not from total failure" is wrong as a blanket rule.** A harness failure carries an error text and evidence, which a
  GA's zero fitness does not; keep R12.2 logging every failure. It teaches readiness (范蠡), reproducible evidence
  (Linus), or a relabelled goal (老子, 孫子: STaR, HER).
- **The mistake inside a success is what the rules miss now.** Today's agent called the real codex binary after the fake
  one returned nothing; the task passed and the bypass would be copied into every child. *Quoted* Dave: "This is the
  'mistake inside a success' in its sharpest form, and today R12.7 does not ask a path to record it."
- **A path must carry its mistakes, linked to the step** (Dave A, 范蠡 step 10, 孫子 change C, 老子's "join").
- **One run is noise:** a child's "2% better" at n=1 should carry its run count, or be confirmed against the parent's
  own run-to-run spread (Dave B, 范蠡 step 11, Linus step 5).

## Where they disagree (side by side)
| Point | Positions |
|---|---|
| Must a child change something? | Linus: no — reuse unchanged with a stated reason, SHOULD · the others keep "change at least one thing" |
| The unit borrowed | 孫子: **steps**, recombined from several paths ("building blocks"; the in-success mistake is "hitchhiking") · Dave: one parent, but list the other matching paths · 范蠡, 老子: one path, with its conditions recorded |
| The workaround | 范蠡: log a route the brief did not name as a **failure** even when it passes · 孫子, Dave: mark the step **workaround** in the path |
| A total failure's insight | 范蠡: first why asks whether conditions were ready · 孫子: say the check never passed; name no root cause you cannot contrast · Linus: evidence-backed diagnosis, else label it a hypothesis · Dave: label near miss / total and name the contrast |
| Change size | 孫子 alone: follow the share of children that beat their parent (the 1/5 rule's idea) |
| Levels | Linus: method clauses SHOULD · EJ has chosen MUST |
| Measure | 老子 alone: a pass/fail measure cannot show "2% better"; the named measure must be able to differ |

## What their research added
Dillon & Tinsley 2008 — near misses are judged as successes, so organisations fail to learn from them (范蠡, verified
abstract) · Madsen & Desai 2010 — launch organisations learned more from failure (范蠡, reported) · Ellis & Davidi 2005 —
reviewing successes and failures beats failures only (范蠡, reported) · Michalski's LEM patent — the low group is used
only as a contrast to the high (范蠡, verified) · building-block hypothesis and genetic hitchhiking (孫子, secondary) ·
germinal centres, dopamine prediction error, ant-colony evaporation, NASA ASRS (Dave, secondary/abstract).

## Questions for EJ (merged)
1. Record the mistakes inside a success in the path — each step marked trusted / workaround / untested, failures linked to their step? (all five)
2. A failure insight names its contrast — the nearest passing attempt — or says none exists? (all five, in different words)
3. A workaround (an engine or tool the brief did not name): a failure, or a marked step?
4. May a child reuse its parent unchanged with a stated reason? (Linus)
5. Borrow steps from several paths, not one whole path? (孫子)
6. Label a child's gain with its run count, and confirm a parent against run-to-run spread (paid repeat runs)?

## Check
`four_experts.py check`: 1 failure — 老子 wrote 戰勝以喪禮處之 where its list has 勝，以喪禮處之 (the fuller chapter text
adds 戰; read as a quote-form variant, not an invention). `--sabotage`: failures as required. Engines: linus codex ·
sun-tzu dsh · lao-tzu opencode · 范蠡 and Dave Claude subagents (web).
