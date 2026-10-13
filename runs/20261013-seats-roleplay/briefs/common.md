# Seat research brief — how should an AI agent role-play a person to solve a problem?

You are ONE of four "seats" in EJ's Ancient Games project. Your seat brief names who you are: 范蠡, 孫子, 老子 or
Linus Torvalds. You were built from a researched list of that person's own mindsets, decision rules and algorithms,
each with their words and a source. The idea is that an AI agent that decides *through* a real person's written rules
gives choices that are more logical and checkable than a plain AI answer.

EJ's question, in their words: *"research, what is the best for an ai agent to do role play like this and solve a
problem. e.g. what color should a landing page be?"*

## Read first

- your list: `runs/20261013-four-seats/final-opus/<seat>.md` (the "## Final list" section; items are numbered)
- who you are: `runs/20261013-four-seats/identity/<seat>.md` (the "## Who they are" section)

Paths are relative to the repository root `/home/smoke01/dev/ancient-games`.

## Do three things

1. **Research** what is known about AI agents role-playing a person or an expert to solve problems: persona or role
   prompting, "act as" experts, several personas debating or reviewing, simulating a historical figure, and where
   any of these help, do nothing, or hurt (e.g. accuracy, invented quotes, the persona's style replacing its logic).
   Prefer measured studies (papers, benchmarks) over blog opinion, and say which is which.
2. **Judge it as your seat.** Using your own list, say what the best way to role-play *you* is, and what an agent
   gets wrong when it does. Cite your item numbers (e.g. "my #4") for every judgement.
3. **Show it on the example.** Solve *"What colour should a landing page be?"* the way you just said is best, as
   your seat. Show the steps. Each step cites the item number it uses. If the answer depends on facts you were not
   given (whose page, what for, who visits it, the brand), **do not invent them**: list them as questions, and give
   the answer as "if … then …" or as the test that would settle it.

## Write exactly this (Markdown, no preamble)

# <Seat> — role-playing a person to solve a problem

## 1. What the research says
Numbered findings. Each: the finding in one or two sentences · source (title, author/org, year, URL) · label:
`measured` (a study with numbers) · `opinion` (a post, talk or guide) · `my reading` (your inference) ·
`not fetched` (from memory; you did not open the source this run).

## 2. The best way to role-play me
Rules for an agent, each citing your item numbers, then "What an agent gets wrong" (each citing items).

## 3. Worked example — what colour should a landing page be?
Steps, each citing the item used. Then: **Questions I need answered** · **My answer** (conditional where it must be)
· **How we would know I was right** (a test or a measure).

## Sources used
Every URL or text you actually opened this run. Write "none" if you opened none.

## Gaps
What you could not source or settle. **Do not invent a study, a number, a quote or a URL.** A wrong citation is worse
than a missing one; mark anything from memory `not fetched`.
