"""Build the overall algorithm review brief, with the artifact inlined.

Why inline instead of letting each engine read the files: a tool-capable engine and a tool-less one then review the
*same* evidence base, so their findings are comparable and a disagreement is about judgement rather than about who
could open which file. It also sidesteps agy entirely — headless agy auto-denies the `command` permission it needs
to read, so it produces nothing when the evidence is on disk (see runs/20261004-step1-review/README.md). The
technique is another session's, from runs/20261004-step4-review/AGY_APPENDIX.md.

Every inlined line is prefixed with its number, so a finding's `file:line` and its quote are both checkable.

Run: python3 build_brief.py > brief-overall.txt
"""
import pathlib

ROOT = pathlib.Path("/home/smoke01/dev/ancient-games")

# The algorithm, as prose. Line ranges are the whole file unless noted.
PARTS = [
    ("docs/WORKFLOW_DESIGN_METHOD.md", None, "the method: 3.0 understand, 3.1-3.8 the steps, 4 state, 5 the qualities"),
    (".claude/skills/workflow-design/SKILL.md", None, "the skill: the same algorithm packaged, with its trigger"),
    ("docs/WORKFLOW_DESIGN_DIAGRAM.md", None, "the same algorithm as diagrams, plus its own step-numbering table"),
]

INSTRUCTIONS = """You are reviewing a complete workflow-design algorithm IN ONE PASS. The whole thing is inlined below;
do not try to read anything from disk, and do not call any tool — the evidence you need is here.

The algorithm exists as three documents that are supposed to be three renderings of one thing:
  * `docs/WORKFLOW_DESIGN_METHOD.md` — the method (sections 3.0 to 3.8, then 4 and 5)
  * `.claude/skills/workflow-design/SKILL.md` — the same algorithm packaged as a skill
  * `docs/WORKFLOW_DESIGN_DIAGRAM.md` — the same algorithm as diagrams, plus a step-numbering table

You are reviewing the ALGORITHM, not the prose. Specifically:

A. COMPOSITION. Do the steps compose? Does each step's output become the next step's input? Name any join where
   it does not.
B. DUPLICATION AND GAPS. Is any work specified in two places, or required in one and missing in another?
C. UNREACHABLE WORK. Is any section, step or rule present in one rendering and absent from another? The three
   documents are numbered differently (the method has 3.0-3.8; the skill has steps 1-8) — does the mapping hold?
D. SILENCES. What does the algorithm never decide that it must decide for a run to succeed? This is the most
   valuable question. Be concrete: name the decision and the step where it should be made.
E. SELF-CONSISTENCY. The algorithm makes promises about itself — that every check can fail, that every node carries
   five things, that a run ends at the acceptance criteria, that an engine is named for every category. Does each
   hold across all steps, or is one broken somewhere?
F. ORDER. Are the steps in the right order? Is any step doing work that belongs to a later one?

Output EXACTLY this format, nothing else — no preamble, no summary, no headings:

FINDING 1: <file>:<line> | <A|B|C|D|E|F> | <high|med|low> | <one sentence: what is wrong> | QUOTE: <the exact text of that line, copied verbatim from below>
FINDING 2: ...
VERDICT: <one sentence on whether the algorithm holds together>

Rules, enforced mechanically after you answer:
* Every finding needs a file, a line number, a letter A-F, and a QUOTE copied verbatim from the inlined text. A
  finding missing any of these is discarded unread.
* Cite only the inlined text below.
* Three sharp findings beat ten vague ones. Do not report wording or formatting preferences.
* An empty findings list is an acceptable answer if the algorithm holds.
"""


def inline(path: str, lo: int | None) -> str:
    text = (ROOT / path).read_text(errors="replace").splitlines()
    if lo:
        text = text[lo[0] - 1:lo[1]]
    width = len(str(len(text)))
    body = "\n".join(f"{i:>{width}}: {l}" for i, l in enumerate(text, 1))
    return f"\n===== FILE: {path} ({len(text)} lines) =====\n{body}\n"


if __name__ == "__main__":
    out = [INSTRUCTIONS]
    for path, lo, why in PARTS:
        out.append(f"\n########## {why}\n")
        out.append(inline(path, lo))
    print("".join(out))
