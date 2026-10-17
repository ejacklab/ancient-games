# Brief — answer one question

## The question

# Question — deliver a lesson with the edit's result, or hold the first edit?

A decision in a time-boxed run (workflow-design method 3.8 item 14): the owner gave 3 hours and is not asked until it
ends, so the main agent decides from your advice — provisionally; the owner accepts or declines it at the end.

Rules for this question:
- Rest each point on a fact below (each carries its source); a point from memory only is labelled *recall* and does
  not decide alone.
- Keep the owner's aims in view: lessons that make agents repeat fewer code and testing mistakes, with less noise.

## Facts
- Decided (`~/.claude/plans/agent-lessons-version-b.md`, section 3): the guard's PreToolUse hook, registered for
  Write/Edit/MultiEdit and for Bash, gives the main agent the lessons that match the path (or command word) — each
  lesson once per session. Source: the plan file.
- Claude Code's hooks reference: PreToolUse output may carry `hookSpecificOutput.additionalContext`, "String added to
  Claude's context alongside the tool result". Whether it is shown *before* the tool runs: "not found in docs".
  Source: https://code.claude.com/docs/en/hooks.md, "PreToolUse: decision control" (via a docs agent's WebFetch,
  quotes close but not byte-checked).
- Exit 0 with no `permissionDecision`: "the tool call continues through the normal permission flow". Source: same page.
- `additionalContext` is capped at 10,000 characters. Source: https://code.claude.com/docs/en/hooks-guide.md.
- The guard already denies some Bash calls before they run with `permissionDecision: "deny"` and a reason the agent
  reads, then retries (`guard/src/hooks.ts`, `handlePreToolUse`; e.g. the read-missing hold of Round 13). A deny writes
  no journal record ("nothing ran"). Source: `guard/src/hooks.ts:106-128`.
- Nothing can be tested live in this session: the hook settings are the owner's to change (R12.3). Source:
  `docs/HARNESS_REQUIREMENTS.md` R12.3.

## The decision
Option A — **context**: return `additionalContext` and let the call run; the lesson reaches the agent with the call's
result (before its next step, maybe after the first edit).
Option B — **hold once**: the first time a lesson matches in a session, deny the call with the lesson as the reason;
the agent reads it and retries; later matches of that lesson add nothing.
Option C — another you can defend.

Which, and what would show it was the wrong choice? Answer within about 8 minutes of work; end with your choice in one
line.

## How to answer

Answer the question as well as you can. If the answer depends on something you were not given, list it under "What I
need to know" and answer conditionally. Write in plain English Markdown. Refer to EJ as they/them. Do not write files;
your final message is the answer.

## Write exactly this (no preamble)

# Answer — <the question in a few words>

## Answer
<your recommendation in one or two sentences>

## How I decided
<numbered steps>

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each risk or price>

## How we would know I was right
<a test, a measure, or an observable result>
