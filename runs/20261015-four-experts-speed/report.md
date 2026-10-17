# Why the experts are slow, why I sound unsure, and ways to speed things up

Measured 2026-10-15 on 13 four-experts runs (2026-10-13/14): `status.json`, engine logs, file times and session
transcripts. The web research is in `research.md` in this folder (43 rows; most are *reported*, from abstracts only).
Scripts and counts were written by Claude, the main agent. The counts are not an independent check.

## Why the experts are slow (measured)

| Cause | Evidence |
|---|---|
| The slowest engine sets the pace | Each engine took 20–272 s. A round waited 96–274 s for all of them, and took 89–326 s from the question to `compare.md`. The relay took 15–19 min. |
| Even a tiny question has a high floor | Round 3 was a 936-byte question with the answer "APPROVE". Each engine took 66–94 s, and Codex used 45,671 tokens. Codex never used fewer than 32k tokens in any run. |
| Each expert reads a large pack | The list file is 38–55 KB and the identity file 16–23 KB. The brief needs only "Final list" (28–45 KB) and "Who they are" (~2 KB). About 25–40% of what they read is research history. The brief also says to re-read the list while working. |
| The answer form is long whatever the question | All five sections are always required. Answers run 2.4–15 KB, and opencode writes 6.5–15 KB. |
| Engines wander with no tool budget | On the approve question, opencode ran `ls`, `rg`, `git log` and `git diff`. Codex ran 5–20 shell commands per answer, and dsh wrote up to 14 reasoning blocks. |
| The caller's own work comes on top | Dave runs as an Opus subagent. Reading about 50 KB of answers and writing the compare took 15–90 s after the last engine. |

## Why I sound unsure (my reading)

1. The house labels (*my reading*, *proposed*, *reported*, n=0) are accurate, but stacked together they read as doubt.
   Over my last 12 sessions there were 443 replies longer than 200 characters. They used "proposed" 146 times,
   "my reading" 87 and "reported" 60.
2. The skill tells me not to pick ("EJ decides; the experts advise. Do not pick a winner by vote count"), so a
   compare ends with questions, not a recommendation.
3. Much of it is genuinely unmeasured.
4. Model side (*reported*, research F37–F41): training rewards guessing, RLHF makes the wording overconfident, and
   hedge words do not track the model's internal certainty. A stated confidence number is better calibrated (F40).
5. I asked EJ questions that were mine to settle (EJ's messages of 2026-10-12).

## Ways to speed it up (proposed)

1. **A short rule card per expert.** One line per rule for the run. The full list stays for `check`. The
   research has no source comparing short and long persona lists, and F1 puts the gain from cutting input at
   1–5% of latency, so the main saving is cost.
2. **Two answer forms.** An approve/change question gets a vote (APPROVE or CHANGE, a few lines, the rule cited).
   All five sections are kept for open decisions. Sources: F1, where output length drives latency, and F30, where
   terse drafts used 7.6% of the tokens.
3. **Early stop on votes.** Stop once enough experts agree. How many is EJ's choice. Sources: F18, F11. Caveat:
   these were tested on one model sampled many times.
4. **Route or cascade.** Choose experts per question type (already done for method 3.3 and 3.5 through `--only`),
   or ask a cheap pair first and call the rest when they disagree. Sources: F22, F23, F12.
5. **A tool budget.** Put every fact in the question and say "read only these files, run no shell". Source: F31.
6. **A confidence number in each answer, and votes weighted by it.** Sources: F20, F40.
7. **One recommendation line from me in each compare,** with a confidence number, while EJ still decides. This
   changes the skill's "do not pick" rule, so it is EJ's decision.
8. **A shorter timeout for vote questions** (now 1800 s), to bound the worst case.
9. **Prompt caching of the fixed persona prefix.** It lowers cost; no source gives a latency figure (F25–F27).
   Little of it can be controlled through the CLIs.
