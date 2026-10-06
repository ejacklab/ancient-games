---
node: n1-research
attempt: 1
engine: agy
model: gemini-3.1-pro-high
status: ok
started: 2026-10-06T08:39:58.103Z
ended: 2026-10-06T08:41:02.395Z
evidence: none
---
# Research: code-graph generation

## The three tiers
- **stdlib `ast`**: Tool: `ast` module; Precision: low (single-file structural syntax); Cost: very low/fast (https://docs.python.org/3/library/ast.html).
- **Import-resolved**: Tool: PyCG/Pydeps; Precision: medium (cross-file static imports and call mappings); Cost: moderate (https://github.com/vitsalis/PyCG).
- **Language-server**: Tool: Pylsp/Pyright; Precision: high (type-aware semantic intelligence and cross-project resolution); Cost: high/heavy background indexing (https://langserver.org/).

## What stdlib `ast` can and cannot see
- **can:** Detect static definitions (classes, functions), explicit assignments, and the literal presence of decorators within a single file, because it parses raw source text into a structural tree without executing it (https://docs.python.org/3/library/ast.html).
- **cannot (dynamic dispatch):** `f = helper; f()` — The callee is evaluated at runtime; AST lacks the data-flow analysis to trace variable reassignments back to the original function, so the edge is absent (https://lwn.net/Articles/932594/).
- **cannot (`getattr`):** `getattr(obj, "attr")()` — The attribute name is resolved dynamically; static analysis cannot determine which object or method is actually invoked without runtime context (https://pylint.pycqa.org/en/latest/faq.html).
- **cannot (decorators):** `@wrap` — AST sees the decorator name but cannot execute it; it remains completely blind to how the decorator might modify, replace, or register the function at runtime (https://peps.python.org/pep-0318/).
- **cannot (pytest fixtures):** `def test(db):` — AST sees a parameter but cannot map it to a `@pytest.fixture` definition, because `pytest` framework injects these dependencies dynamically at runtime (https://docs.pytest.org/en/latest/how-to/fixtures.html).

## Existing tools worth knowing
- **PyCG**: A tool that generates practical, static call graphs for Python, resolving cross-module calls without code execution (https://github.com/vitsalis/PyCG).
- **Pydeps**: A dependency graph generator that visualizes module-level import structures to find architectural coupling (https://github.com/thebjorn/pydeps).
- **Pylsp**: A Python language server (often using Jedi) that powers deep IDE features like cross-project semantic resolution and "go to definition" (https://github.com/python-lsp/python-lsp-server).

## Digest
Generating reliable Python code graphs requires balancing speed against semantic accuracy (https://microsoft.github.io/language-server-protocol/). The standard library `ast` module is fast and deterministic, but it is strictly file-bound and analyzes only syntax structure (https://docs.python.org/3/library/ast.html). A pure `ast` script cannot resolve edges for dynamic behaviors like `getattr`, dynamic dispatch, or decorator mutations, nor can it map `pytest` fixtures, because it fundamentally lacks data-flow analysis and cannot execute code (https://lwn.net/Articles/932594/). To connect nodes across files, tools must step up to the "import-resolved" tier (like PyCG), mapping cross-module dependencies via custom static analysis (https://github.com/vitsalis/PyCG). For maximum precision, including type inference and alias resolution, Language Servers maintain deep semantic indexes at a higher performance cost (https://langserver.org/). Therefore, an `ast` script must only claim to extract local structural nodes; robust project-wide edges require LSP-level intelligence (https://arxiv.org/abs/2401.07681).
