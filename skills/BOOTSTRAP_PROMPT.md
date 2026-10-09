# Bootstrap prompt — adopt the Ancient Games workflow-design + orchestration style

Copy the block below into a fresh agent session **in the project that is adopting the style**, and replace `<PATH>`
with a **local path** to the Ancient Games repo. The skills are copied from disk, so a link alone is not enough —
clone it first if that is all you have. The agent reads the Ancient Games, installs its skills, and writes the
adopting project's own `AGENTS.md` and `orchestration.mdc`.

---

````
Adopt the Ancient Games workflow-design and orchestration style for this project.

The Ancient Games is at <PATH> (a local path). This session's working directory is the adopting project's root;
keep its outputs there. Treat <PATH> as a read-only source, not as the destination project.

1. Locate the four complete skill folders under <PATH>/skills/. Install them into the skill root your harness
   scans (`~/.claude/skills/` for Claude Code, `~/.agents/skills/` for the DeepSeek Harness / Codex).
   Replace both placeholders below with actual paths and quote them; <SKILL_ROOT> is the chosen skill root.
   Before copying, inspect any existing destination folder or symlink: reuse an identical install, otherwise show
   the differences and obtain authorization to replace it. Do not merge into or write through an existing symlink.
   For destinations that do not yet exist:

       mkdir -p "<SKILL_ROOT>"
       cp -r "<PATH>/skills/workflow-design" "<SKILL_ROOT>/workflow-design"
       cp -r "<PATH>/skills/requirement-check" "<SKILL_ROOT>/requirement-check"
       cp -r "<PATH>/skills/meaningful-names" "<SKILL_ROOT>/meaningful-names"
       cp -r "<PATH>/skills/bootstrap" "<SKILL_ROOT>/bootstrap"

   `README.md` and `BOOTSTRAP_PROMPT.md` in the bundle are documentation, not skills. Verify each installed
   `SKILL.md` and workflow-design's referenced files resolve. If the harness has no skill-loading command, read
   `SKILL.md` directly. If this session cannot write the usual root, use a supported project-local skill root and
   record it, or report installation as blocked; do not claim an unreadable skill is installed.

2. Load the `bootstrap` skill and follow it: read this project's blueprint (ask for what is missing — never invent
   it), then write this project's `AGENTS.md` and root `orchestration.mdc`. Read the sources listed in bootstrap,
   including the full method, task types, executors, feedback templates and blueprint layout, before drafting.

   - Read all existing instruction files, their pointers and orchestration rules first. Keep project-specific
     instructions and show me the proposed diff and why before overwriting, unless I already authorized it.
     Keep one canonical instruction file; other harness files point to it without a cycle.
   - Send me everything the blueprint cannot answer as one batch, with your provisional assumption next to each
     question and what it blocks. Where a unit, threshold or test is missing, it stays open — do not fill it in.
     Read the mapped blueprint sections, not just the map. Unaccepted sections and unanswered choices keep their
     dependent work blocked; any output that still depends on them is a draft.
   - Make both files read on every session: put "Read orchestration.mdc before starting work in every session."
     in the canonical instructions. Keep the files short, gloss unfamiliar terms, and link resolved references.
   - Use the project's actual commands and verify engine/model/effort/read-write capability locally before marking
     an engine verified. Copy only applicable defaults with their source and unit; leave missing values open.
     Instantiate task mappings, all five referee decisions, worker-owned returns, node contracts, state/evidence
     paths, checks before handoffs, failure feedback and limit-hit exits as specified by bootstrap.

3. Then, in this project:
   - use `workflow-design` to design workflows or decide none is needed; keep a checked sequence and declare each
     piece's inputs, outputs and withheld context (DAG means directed acyclic graph; topology alone is no check);
   - evaluate every rule, requirement and threshold through `requirement-check` (source, one thing, unit, can it
     fail, weak words, level, basis, links);
   - name every function, field and concept through `meaningful-names` (one word, one job).

Keep one copy per rule: point at the installed skills, never paste their bodies into this project. The exception
is these four standing rules: copy them verbatim into BOTH generated files (the canonical target if AGENTS.md
is only a pointer). Add glosses separately; do not paraphrase the rules:

- **Every field has one writer** — a return template is the worker's; a verdict is the human's. Name who fills it.
- **Evidence lives in the project** (`runs/<run-id>/` by default, SHOULD — a written reason may override); scratch in `/tmp` is fine, the refer-back artifact must not stay there.
- **A workflow is a checked sequence** — each step's result is verified, then becomes the next step's input. Not a
  DAG for its own sake.
- **The knowledge graph is declared** — each piece's needs and outputs, and what each must not see.

Before calling it finished, follow the instruction/reference paths as a fresh session would, check the four rules
in each file, and trace one representative task through input, check, evidence, state, handoff and failure exit.
Mark planned paths with their creator and creation step; do not leave unresolved project/model/command placeholders
in finished files. Documented path patterns such as runs/<run-id>/ remain patterns, including in the standing rules.

When you are done, report: the files you wrote and whether they are finished or drafts, the installed skill root,
checks you actually ran, unresolved questions and blocked types, every path you named that does not exist yet,
and every number carried over from the Ancient Games' defaults with its unit and source.
````
