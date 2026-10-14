# Excerpts — Claude Developer Platform docs, "Memory tool"

URL: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (fetched 2026-10-13; no page date).
How read: WebFetch returned what has the form of the full page text (frontmatter, every SDK code sample, every error
string intact). That it is a pass-through and not a model's reproduction is my reading of its form; it was not saved to
disk by the harness. Copied here verbatim from that return.

"When the memory tool is enabled, Claude automatically checks its memory directory before starting a task. As it works,
Claude stores what it learns in files under `/memories` and reads them back in later conversations to continue earlier
work."

"The memory tool operates client-side: Claude requests file operations, and your application executes them."

## Prompting guidance (verbatim)

"When the memory tool is present in your request's `tools`, the API automatically adds this instruction to the system
prompt. You don't need to send it yourself:"

```
IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE.
MEMORY PROTOCOL:
1. Use the `view` command of your `memory` tool to check for earlier progress.
2. ... (work on the task) ...
   - As you make progress, record status / progress / thoughts etc in your memory.
ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory.
```

"Claude's tool description already tells it to keep the memory directory organized, so you don't need to repeat that
instruction. If Claude still creates cluttered memory files, you can reinforce it in your prompt:"

"Note: when editing your memory folder, always try to keep its content up-to-date, coherent and organized. You can
rename or delete files that are no longer relevant. Do not create new files unless necessary."

"You can also guide what Claude writes to memory. For example: "Only write down information relevant to \<topic> in your
memory system.""

## Security considerations (verbatim, partial)

"Claude usually refuses to write sensitive information to memory files. For stronger guarantees, add validation that
strips sensitive data before your handler writes the file."

"Periodically delete memory files that haven't been accessed in a long time."

## Multisession software development pattern (verbatim)

"For software projects that span multiple agent sessions, set up memory files deliberately instead of writing them ad
hoc as work progresses. The following pattern turns memory into a recovery mechanism: each new session resumes from the
state the last one recorded."

"1. **Initializer session:** The first session sets up the memory files before any substantive work begins. This
includes a progress log (tracking what has been done and what comes next), a feature checklist (defining the scope of
work), and a reference to any startup or initialization script the project needs."

"2. **Subsequent sessions:** Each new session opens by reading those memory files. …"

"3. **End-of-session update:** Before a session ends, it updates the progress log with what was completed and what
remains. …"

"Work on one feature at a time. Mark a feature complete only after end-to-end verification confirms it works, not when
the code is written."
