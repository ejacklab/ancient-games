# Findings — Jev (TypeSafe) as a routing layer for agents
Produced 2026-10-03 by the COO (three WebSearch calls, three WebFetch reads). Question asked: what is the "JEV" EJ's
friend uses on the fork layer of his agent setup, and does it fit our method?

All rows are **reported**: every page was read through WebFetch, which returns a model-written summary, and the
sources are a vendor-adjacent site, a third-party blog and a plugin README. Nothing was run.

| id | Finding | Label | Source |
|---|---|---|---|
| J1 | Jev is a typed-decision model by TypeSafe AI, released 2026-09-15 with $40M seed funding; TypeSafe calls it a "System One model, built to make fast decisions inside software". It does not write text or code. | reported | https://flaviocopes.com/jev/ |
| J2 | Three question types: Noul (yes/no, a probability), Choice (one of the options you supply, with the full distribution and a confidence), Score (a calibrated position on a spectrum). Every answer is constrained to the supplied options; the output shape is guaranteed. | reported | https://flaviocopes.com/jev/ ; https://madewithjev.com/jev-multi-agent |
| J3 | A request carries a model name, the state (the data to judge) and a set of questions; all questions run in parallel against the same state, so independent questions go in one call. | reported | https://flaviocopes.com/jev/ |
| J4 | Price $0.042 per million input tokens, output free; latency typically 70–500 ms, mostly about 100 ms. Vendor claim "193.6x faster, 444.6x cheaper" than frontier LLMs on comparable tasks. | reported (vendor numbers) | https://flaviocopes.com/jev/ |
| J5 | Stated weaknesses: arithmetic and counting, dates, measurements and numeric comparison, extracting text values, images/audio/video, contradictory instructions. "Numbers, dates and counting stay in code." | reported | https://flaviocopes.com/jev/ |
| J6 | Hosted API only (TypeSafe direct, OpenRouter, Vercel AI Gateway); no open weights or local deployment — the state you send leaves the machine. | reported | https://flaviocopes.com/jev/ ; https://madewithjev.com/jev-multi-agent |
| J7 | A "fork" is a branching decision in a multi-agent workflow. Five routing forks named: who acts next; is the research good enough (accept/verify/reject); is the objective finished; should this action proceed (allow/confirm/deny); is this command safe (a score). Advice: start with one fork, the routing fork, because it runs at the top of every workflow and its answer is cheap to check. | reported | https://madewithjev.com/jev-multi-agent |
| J8 | The routing menu is built from live state: only workers that exist, tools that are installed, actions the host can run. | reported | https://madewithjev.com/jev-multi-agent |
| J9 | Limits stated by the same site: "the shape is guaranteed, the answer inside is not"; it classifies but must not grant permissions; it does not replace the orchestrator's control of workflow state. | reported | https://madewithjev.com/jev-multi-agent |
| J10 | "Almost none of this has a published benchmark. The measured figures are single-call, and the honest label for the rest is architecture, not result." No published routing accuracy, false-completion or recovery measure. | reported | https://madewithjev.com/jev-multi-agent |
| J11 | A DeepSeek Harness plugin routes routine turns to cheap subagent models with Jev: six questions per turn (task class, effort, blast radius, multi-module, user asked for the main agent, risk), a declarative policy (delegate mechanical/bugfix/research when effort ≤ M–L, blast radius below cross-module, confidence > 0.7, risk < 20%; a "careful" profile needs > 0.85), roles mapped to models (junior → qwen3.8-flash, implementer → deepseek-v4-flash). | reported | https://github.com/vitas/dsh-jev-subagent-dispatch |
| J12 | That plugin fails open: a missing key, timeout, 429 or bad config logs the reason and the main agent keeps the work. Its authors say the recommendation "should earn its place with evidence, not faith", and admit their log cannot see whether a child was spawned or the work redone. | reported | https://github.com/vitas/dsh-jev-subagent-dispatch |
| J13 | Other uses found: Jev-as-root orchestration and judge samples, an action-probability orchestration repo, and a pull request "route subagents with Jev" in a Claude Code mods repository. Not read. | unknown | https://github.com/sakthijas/multiAgent-jev ; https://github.com/prove-ai/jev-orchestration ; https://github.com/Reilley64/mods/pull/106 |

## Fit with our method (COO inference, n=0)

- Jev is a candidate engine for the **classification** row of `docs/TASK_TYPES.md` and for the **routing fork** of the
  dispatcher layer (`TODO.md`): who acts next, delegate to the cheap coder or keep with the COO, task category and
  case (A–D). It is not a coder, researcher, explorer or verifier.
- It must not replace a check. Its own sources say the answer inside the guaranteed shape may be wrong (J9) and
  routing accuracy is unmeasured (J10). Our checks stay scripts and blind reviewers; Jev may only choose *which*
  worker or check runs, with a confidence threshold and a fail-open fallback to the COO (J11, J12).
- It is measurable at almost no cost: the 300-prompt corpus (`tests/fixtures/operator_prompts_r*.jsonl`) with
  `tests/workflows/corpus_check.py` already scored codex at 96% and agy at 76% strict agreement on category labels.
  Running Jev on the same corpus with the same labelling rules would give a direct comparison.

## Open-source and local alternatives (added 2026-10-03, second round)

Same caveat: every row comes through WebFetch summaries, so all are **reported**. Star counts and dates are as the
pages state them and were not checked; one summary dated a JevK5 release "September 2024", which cannot be right
for a project that copies a 2026 model, so treat dates from these summaries as unreliable.

| id | Finding | Label | Source |
|---|---|---|---|
| J14 | There is no open-source Jev itself; there are many open alternatives (directories list dozens). | reported | https://madewithjev.com/open-source-jev ; https://systemonemodels.org/examples/alternatives/ |
| J15 | **JevK5** (Apache-2.0): Qwen3.5-4B or 9B; a softmax over the answer letters' next-token logits, one forward pass, no generated tokens; noul / choice / score. About 9 GB VRAM for 4B (bf16), 19 GB for 9B; GGUF builds run on CPU at about 0.25 s (2B) and 0.6 s (4B) per short decision; a DeBERTa-v3 "Lite" for CPU. Its server **accepts the TypeSafe-style `/v1/systemone` request shape**. Stated: JevBench hard tier 0.784 accuracy, ECE 0.054 (v0.3); H100 p50 13.2 ms; judging answers got worse (0.76 → 0.65); English only; refuses inputs over 16,384 tokens; weak at multi-step, temporal and numeric reasoning. | reported | https://github.com/allebee/jevk5 |
| J16 | **Laya** (Apache-2.0): a 421M fine-tuned encoder with a decision head (322M multilingual); T4 GPU 33–40 ms, CPU 193–464 ms; Jev-style choice/score/noul in one forward pass; "ECE 0.081 after temperature fitting, from 0.466 as shipped". | reported | https://systemonemodels.org/examples/alternatives/ ; https://shop.zimaspace.com/blogs/tech-ai-hub/laya-open-source-decision-model-local-ai |
| J17 | **Von** (Apache-2.0): a 395M encoder scoring each option, non-autoregressive, about 23 ms on an A10G, "sealed ECE 0.107", described as a local drop-in alternative. | reported | https://github.com/wfzyx/von ; https://systemonemodels.org/examples/alternatives/ |
| J18 | **open-alternative-jev** (`so1`, Apache-2.0): a library, not a model — reads option probabilities from any open Qwen model's next-token logits; HF and vLLM; **not** API-compatible (in-process Python). Stated on a shared 400-case benchmark: Qwen3.6-27B 73.7% at 582 ms per case versus Jev's reported 72.7% at 710 ms; raw probabilities over-confident (temperature scaling needed); reversing options moved a 4B model's yes/no accuracy by 13.5 points; below 4B, 2–8 points worse; it documents its own earlier flawed speed claim. | reported | https://github.com/ikermoel/open-alternative-jev |
| J19 | Other entries: Kev (LoRA on Qwen3.5-Base, 0.8B/4B/9B), NanoJev (0.6B from scratch, no metrics), CLM (Qwen3-8B encoder plus a head), OpenDecision (CPU zero-shot NLI wrapper; "confidence measures concentration, not correctness"), mini-jev (frozen Qwen3-4B logit reader, "not calibrated"), and Jevstiller, which distils Jev's outputs into a local model. | reported | https://systemonemodels.org/examples/alternatives/ ; https://www.theregister.com/ai-and-ml/2026/09/29/open-source-tool-distills-jev-so-you-can-run-it-locally/5299856 |
| J20 | This machine has an NVIDIA RTX 4070 Ti SUPER with 16 GB, 9 CPU cores and 25 GB RAM (WSL): enough for JevK5-4B in bf16, Laya or Von on GPU or CPU, and so1 with a Qwen model up to about 7B. | verified | `nvidia-smi`, `nproc`, `free -g` on 2026-10-03 |
| J21 | **Laya, in more detail.** Convai Innovations; Apache-2.0; ModernBERT-large encoder (about 395M) plus a two-layer decision head and an act/escalate part, 421M in all, about 1 GB; non-autoregressive. Checkpoints: English (512-token input), multilingual on mmBERT-base (322M, 1,024 tokens, 100+ languages), and a "typed-decisions" checkpoint fine-tuned on that benchmark's own training split. Runs from PyTorch/Transformers (pip `laya`), with ONNX (Node.js) and MLX ports and a GGUF build. | reported | https://huggingface.co/convaiinnovations/laya ; https://aiweekly.co/alerts/convai-ships-laya-a-421m-modernbert-decision-model-apache-20 ; https://shop.zimaspace.com/blogs/tech-ai-hub/laya-open-source-decision-model-local-ai |
| J22 | **Laya's numbers depend on fine-tuning.** Base Laya zero-shot about 0.36 against a random baseline of about 0.318 — "only slightly above the random baseline in zero-shot use". The fine-tuned typed-decisions checkpoint: 0.766 against Jev 1.13.0's 0.727, p50 32.8 ms against Jev's 236–276 ms — but trained on that benchmark's own training split, so in-domain. ECE 0.466 as shipped, 0.081 after temperature fitting; the project says to calibrate on your own domain. Weak on close ordinal scales (1–5), choice lists should stay under about 20 options. | reported | same as J21 |

**For the dispatcher (COO inference).** JevK5 is the closest drop-in: open weights, the Jev request shape, fits the
16 GB GPU. Laya or Von are the light option (CPU-capable, tens of ms on GPU), but Laya is barely above random until it is fine-tuned on your own labelled decisions (J22). so1 is the most honest about its
weaknesses (position bias, over-confidence) and those weaknesses apply to every logit-reading alternative. None has
been measured on our task labels; the 300-prompt corpus with `corpus_check.py` is the test, run locally, so no prompt
leaves the machine.

## Gaps

No primary TypeSafe documentation was read, only summaries. Accuracy on our labels is unknown. Whether the
corpus prompts may be sent to a hosted API is EJ's call (J6). No API key exists on this machine (not checked).
