A decision in a time-boxed run (workflow-design method 3.8 item 14): EJ gave 4 hours or 6 rounds and is not asked
until it ends, so the main agent decides from your advice — provisionally; EJ accepts or declines it at the end.

Rules for this question:
- Keep the vision and the use cases in view: an option that serves no use case is wrong, however good.
- Rest each point on the research below (a finding id) or on a measurement in it; a point you have only from memory
  is labelled *recall*, and recall alone does not decide.

Facts:
- **Vision (EJ, today):** "what makes a person very powerful is the insight". Today an insight (six whys → root cause
  → 2–3 fix options) is written when a task fails and then left in its run folder; nothing reads it again, so
  failures repeat (this session: a hidden test result twice, a spec mixing instructions into literal values twice).
  So the expert **Dave** keeps his ten rules and **also loads the insights, sorted into 6 categories, reading the
  categories related to each task**. A plain control, **Dario** (no rules, no insights, same engine as Dave), measures
  what the rules and insights add. Plan: `runs/20261016-six-experts/plan.md`.
- **Use cases:** (U1) before an expert answers, it reads the past insights that apply to the question and cites their
  ids; (U2) a failure answered by an insight does not repeat in later work; (U3) the insight load fits the engine's
  context with room for the question and the answer, now and as insights grow.
- **The material:** `runs/20261016-six-experts/research/insight-sections.txt` — all 62 insight sections (file ·
  failure id and title · Source). The Source field already sorts them: instruction 22, check 18, tool 14, config 8.
  Task categories exist too: `docs/TASK_TYPES.md` (the method's task types).
- **Size and growth (measured):** all insights ≈ 93 KB ≈ 25k tokens; ≈ 40–50 KB added per working day (by the date
  each file was first committed) — 1M tokens (≈ 4 MB) is ≈ 80–100 working days away at that rate.
- **Engines:** `runs/20261016-six-experts/research/context-windows.md` (context window, price, long-context notes per
  engine, labelled). Codex has 0% quota left today.

**Decision 1 — the 6 categories, and how "related to this task" is picked.** Propose six categories that every one of
the 62 sections fits into exactly one of (say how a section is placed: by its Source, by the task type, by what went
wrong, or a mix), and how the insights related to a question are chosen: (a) the main agent names the categories when
it writes the question; (b) Dave reads a one-line-per-section index and picks; (c) both. Test your six against the
62 titles: name any section that fits none or two.

**Decision 2 — which engine and model runs Dave** with the insight load, given the research, the size today and the
growth: what it costs per question, and when the choice must be revisited.

Time left in the run: the deadline is 18:17 +0800; answer within 20 minutes.
