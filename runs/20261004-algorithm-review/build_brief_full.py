"""The FULL algorithm review brief — everything the algorithm is, inlined.

Pass 1 (`brief-overall.txt`) inlined only the three prose renderings: method, skill, diagram (899 lines). That is
under a third of the algorithm. The method delegates constantly — per-category pattern/engine/check/sabotage to
`TASK_TYPES.md`, who may run a node and how to prove it to `EXECUTOR_KINDS.md`, the shape of each artefact to the
templates, and its own enforceable rules to `design_gate.py`, which is the thing that actually refuses a design.
A reviewer cannot check "the step says X" against a table it cannot see, so pass 1 could not answer whether the
algorithm's delegations are honoured.

This adds 2405 lines to the 899: the tables, the templates, the gate, the ledger rules and the runnable form.

Run: python3 build_brief_full.py > brief-full.txt
"""
import pathlib

ROOT = pathlib.Path("/home/smoke01/dev/ancient-games")

PARTS = [
    ("docs/WORKFLOW_DESIGN_METHOD.md", "THE METHOD — sections 3.0 to 3.8, then 4 and 5"),
    (".claude/skills/workflow-design/SKILL.md", "THE SKILL — the same algorithm packaged, with its trigger"),
    ("docs/WORKFLOW_DESIGN_DIAGRAM.md", "THE DIAGRAMS — the same algorithm drawn, plus its step-numbering table"),
    ("docs/TASK_TYPES.md", "THE CATEGORY TABLE — what 3.4 delegates to: pattern, engine, check, sabotage per category, "
                           "the 20% challenger rule, the seeded pipelines"),
    ("docs/EXECUTOR_KINDS.md", "WHO RUNS A NODE — the engines, the canary, read-only vs write, the fallback, the "
                               "routing, and the traps"),
    ("docs/TASK_TYPES_LEDGER.md", "THE CHALLENGER LEDGER — its row rules"),
    (".claude/skills/workflow-design/scripts/design_gate.py", "THE GATE — the rules that actually refuse a design"),
    (".claude/workflows/intake.js", "THE RUNNABLE FORM — the algorithm as a script"),
    ("docs/workflow-templates/readiness.md", "TEMPLATE — readiness"),
    ("docs/workflow-templates/blueprint.md", "TEMPLATE — blueprint"),
    ("docs/workflow-templates/prompt-file.md", "TEMPLATE — prompt file"),
    ("docs/workflow-templates/node-brief.md", "TEMPLATE — node brief"),
    ("docs/workflow-templates/research-file.md", "TEMPLATE — research file"),
    ("docs/workflow-templates/explorer-file.md", "TEMPLATE — explorer file"),
]

INSTRUCTIONS = """You are reviewing a complete workflow-design algorithm IN ONE PASS. The whole thing is inlined below.
Do not read anything from disk and do not call any tool — your evidence is here.

The algorithm is not one document. It is nine kinds of artefact that are supposed to agree:

  * `docs/WORKFLOW_DESIGN_METHOD.md`      the method: 3.0 understand, 3.1-3.8 the steps, 4 state, 5 the qualities
  * `.claude/skills/workflow-design/SKILL.md`   the same algorithm packaged as a skill
  * `docs/WORKFLOW_DESIGN_DIAGRAM.md`     the same algorithm drawn, plus a method-vs-skill numbering table
  * `docs/TASK_TYPES.md`                  the per-category defaults step 3.4 delegates to
  * `docs/EXECUTOR_KINDS.md`              which engine may run a node, the canary, the fallback, the routing
  * `docs/TASK_TYPES_LEDGER.md`           the challenger ledger's row rules
  * `scripts/design_gate.py`              the gate: the rules that actually refuse a design
  * `.claude/workflows/intake.js`         the algorithm as a runnable script
  * `docs/workflow-templates/*.md`        the shape of each artefact a design must produce

Answer these, and label every finding with the letter:

A. COMPOSITION. Do the steps compose — does each step's output become the next step's input? Name any join where
   it does not.
B. DUPLICATION AND GAPS. Work specified in two places, or required in one and missing in another.
C. UNREACHABLE WORK. A section, step, rule or template present in one artefact and absent from another. The
   renderings are numbered differently (method 3.0-3.8 vs skill steps 1-8) — does the mapping hold?
D. SILENCES. What the algorithm never decides that it must decide for a run to succeed. Most valuable question.
E. SELF-CONSISTENCY. The algorithm's promises about itself — every check can fail, every node carries five things,
   a run ends at the acceptance criteria, an engine is named for every category, a design is refused when wrong.
   Does each hold across all artefacts, or is one broken somewhere?
F. ORDER. Are the steps in the right order? Is a step doing work that belongs to a later one?
G. ENFORCEMENT. Does `design_gate.py` enforce what the steps require, and does it require anything the steps do not
   state? A rule the steps state but the gate cannot check is a promise with no mechanism; a rule the gate enforces
   but no step states is a surprise. Name each mismatch.
H. DELEGATION. The steps delegate to `TASK_TYPES.md` and `EXECUTOR_KINDS.md`. Does each table actually supply what
   the steps assume of it — the pattern, engine, check and sabotage for every category the steps name? Name any
   category, rule or field a step assumes and a table does not provide.
I. TEMPLATES. Does each template carry every field the steps require a design to state? Name a field a step
   demands and a template omits.

Output EXACTLY this format, nothing else — no preamble, no summary, no headings:

FINDING 1: <file>:<line> | <A-I> | <high|med|low> | <one sentence: what is wrong> | QUOTE: <the exact text of that line, copied verbatim from below>
FINDING 2: ...
VERDICT: <one sentence on whether the algorithm holds together>

Rules, enforced mechanically after you answer:
* Every finding needs a file, a line number, a letter A-I, and a QUOTE copied verbatim from the inlined text. A
  finding missing any of these is discarded unread.
* Cite only the inlined text below.
* Three sharp findings beat ten vague ones. Do not report wording or formatting preferences.
* An empty findings list is an acceptable answer if the algorithm holds.
"""


def inline(path: str) -> str:
    text = (ROOT / path).read_text(errors="replace").splitlines()
    width = len(str(len(text)))
    body = "\n".join(f"{i:>{width}}: {l}" for i, l in enumerate(text, 1))
    return f"\n===== FILE: {path} ({len(text)} lines) =====\n{body}\n"


if __name__ == "__main__":
    out = [INSTRUCTIONS]
    total = 0
    for path, why in PARTS:
        out.append(f"\n########## {why}\n")
        out.append(inline(path))
        total += len((ROOT / path).read_text(errors="replace").splitlines())
    out.append(f"\n########## END OF EVIDENCE — {total} lines, {len(PARTS)} artefacts\n")
    print("".join(out))
