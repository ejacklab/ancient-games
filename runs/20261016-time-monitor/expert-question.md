A decision in a time-boxed run (workflow-design method 3.8 item 14): the owner gave a time and is not asked until it
ends, so the main agent decides from your advice — provisionally, and the owner accepts or declines it at the end.

Rules for this question:
- Keep the vision and the use cases in view: an option that serves no use case is wrong, however good.
- Rest each point on the research below (a finding id) or on a measurement; a point you have only from memory is
  labelled *recall*, and recall alone does not decide.

Facts:
- Vision / use cases (the owner's request, this run): the agent cannot feel time pass; a guard (code run by the
  harness after every tool call) must tell the agent how much of the owner's time limit is used, so it finishes and
  reports within the time; workers return timestamped progress per small piece so the agent sees progress, not only
  the end. Criteria: `runs/20261016-time-monitor/criteria.yaml`.
- Research: `runs/20261016-time-monitor/research/reminders.md` (F1–F8).
- The decision: how often the guard adds the time to the agent's context.
  (A) only at marks 50%, 80%, 100%, then every call after time is up;
  (B) a one-line status on every tool call (≈20 tokens), plus a fuller block with the workers' progress at the marks;
  (C) every N calls or every N minutes.
  What each changes: (A) is quiet but untested in the research; (B) matches every tested design but adds context on
  every call; (C) is in between, with a number nobody has measured.
- Time left: deadline 11:22 +0800; answer within 15 minutes.
