# Source-of-truth memory — product vision statement

> **Status: settled** (accepted by EJ on 2026-10-12). EJ's words: *"ok the vision is confirm"*. Drafted 2026-10-12 by the COO, at EJ's request (*"ok same way, which I think
> is the better way we define the vision first"*), from what EJ has already decided about this memory. Each line
> names its basis:
> - **[EJ]**: EJ's decision or words, with the date and the record that holds it;
> - **[design]**: text of `SOURCE_OF_TRUTH.md` that EJ revised, but not his own sentence;
> - **[proposed]**: the COO's wording, which EJ has not said.
>
> **Whose it is.** The product vision is EJ's (*"an agent may only write down what EJ has said"*, blueprint template).
> He settled it on 2026-10-12.
>
> **Drawn from:** `docs/memory-system/SOURCE_OF_TRUTH.md`, the design this vision serves, and its run record
> `runs/20261011-source-of-truth-design/` (decisions in `DESIGN-detailed-2026-10-12.md`).

The source-of-truth memory is the project's written memory: plain markdown files kept in the repo with the code,
which every agent and every person reads and may change [design, l.19–22]. It holds what the code cannot tell you
[design, l.35]:
- the **decisions and facts** the code must follow, written **before** the code;
- what was **learned** after: lessons, observations and hypotheses.

[EJ, 2026-10-12, DESIGN-detailed l.27–29]

**Who it is for.**
- Every agent and every person working on the project. There are no owners and no approval gate: anyone may change
  any entry, and every change is logged with when and which model or person made it [EJ, 2026-10-12, header l.8–9;
  *"log when and which model changed it"*, agent-memory notes l.65].
- Not one person's memory across projects (user memory), and not one agent's own memory (agent memory). Both live
  outside the repo, in the home folder [EJ, 2026-10-12, agent-memory notes l.63, l.85].

**The problem it solves.** The context window is cleared at the start of every session, so anything learned is lost
unless it is written down. A private agent store is invisible to the other agents [design, l.19, l.91].

**What it will never do.**
- It never copies what can be read directly from the code, the tests or the commit log, such as what a function does,
  which test covers it, or what a commit changed. A copy goes stale when the code changes. The memory itself lives in
  git; the rule is about what an entry says, not where it is stored [design, l.84, reworded after EJ's correction on
  2026-10-12: *"the memory will be in git also right?"*].
- It never needs a private store, a database or an outside service to be read. The caches are optional and rebuilt
  from these files [design, l.21–22; CACHES.md, accepted].
- An entry is never held back for approval. An entry is a memory once it is written [EJ, 2026-10-12: *"for example a
  lesson learn, is it a memory, why got proposed and active?"*].
- The code never moves ahead of a decision or fact unnoticed. The decision or fact changes first, then the code. When a
  decision or fact no longer matches the code, the background subagent reports it to EJ and does not edit it
  [EJ, 2026-10-12, DESIGN-detailed l.27, l.31].
- Nothing is lost between sessions. Task and project memory keep a journal, and an agent reads it at each milestone
  and writes what is worth keeping as entries [EJ, 2026-10-12: *"task and project memory need a journal"*; *"an agent
  will go read the journal when hit each milestone"*].

**How we know it works.** [proposed] A fresh session with only a clone of the repo can carry on from where the last
one stopped:
- It reads `AGENTS.md`, `INDEX.md` and its task's `state.md`, and follows the recorded decisions without asking
  again.
- Every change to an entry shows who made it and when.
