---
node: n2-design
attempt: 3
engine: claude
model: claude-opus-5-5
status: ok
started: 2026-10-06T08:46:24.403Z
ended: 2026-10-06T08:48:51.257Z
evidence: none
---
# Spec: code_graph.py

**Location:** `.claude/skills/workflow-design/scripts/code_graph.py`
**Runtime:** Python 3.9 or newer (it needs `ast.unparse`). Standard library only: `ast`, `argparse`, `builtins`, `fnmatch`, `json`, `pathlib`, `sys`, `collections`. The tool reads each file with `ast.parse`. It never imports the code it reads and never runs it.
**Tier:** `stdlib-ast`, the cheapest of the three tiers in the n1 digest. The tool adds one thing on top: it resolves imports by name across files under ROOT. This is a plain lookup, not PyCG.
**Digest source:** `runs/20261005-code-graph-tool/nodes/n1-research-1.result.md`. The brief said the digest was included, but it was not in the brief, so I read it from the run folder. I did not read any raw research.

## Nodes
A node is either a **module** or a **function**. Classes are not nodes; their names appear only inside function ids.

- **module**: one `.py` file under ROOT.
  - id: the path relative to ROOT, with `/` separators. Example: `ancient_games/gate.py`.
- **function**: one `def` or `async def` at any depth. That includes methods and nested functions.
  - id: `<module id>::<each enclosing class or def name>::<name>`. Examples: `ancient_games/gate.py::Gate::decide`, `m.py::outer::inner`.
  - When ROOT is the pytest rootdir, this format makes a test's id the same as its pytest node id, for example `tests/test_x.py::TestA::test_b`.
  - If a module defines the same name twice, the **last** definition keeps the plain id. Each earlier one gets the suffix `@<line>`, for example `m.py::f@12`. Calls resolve to the last definition, as Python does.

**Test file:** a file whose name matches a `--test-glob` (default `test_*.py` and `*_test.py`), or a file named `conftest.py`.

**Function roles** (exactly one per function):
- `test`: in a test file, the name starts with `test`, and it is either at module level or a method of a module-level class whose name starts with `Test`.
- `fixture`: has a decorator `pytest.fixture` or `fixture`, either bare or called.
- `test_support`: any other function in a test file.
- `code`: every function that is not in a test file. **Only `code` functions are counted in coverage.**

pytest settings in `pytest.ini`, `pyproject.toml` or `setup.cfg` (`python_functions`, `python_classes`) are not read. The defaults above are used.

**Fields.** Every node has all fields of its kind.

| field | kind | type | meaning |
|---|---|---|---|
| `id` | both | str | as defined above |
| `kind` | both | `"module"` \| `"function"` | |
| `file` | both | str | path relative to ROOT, `/` separators |
| `line` | both | int | the `def` line; 1 for a module |
| `end_line` | both | int | `node.end_lineno`; for a module, its last line |
| `is_test_file` | both | bool | the file is a test file |
| `name` | function | str | bare name, for example `decide` |
| `qualname` | function | str | enclosing names joined with `.`, for example `Gate.decide` |
| `module` | function | str | id of the module that contains it |
| `role` | function | `"test"` \| `"fixture"` \| `"test_support"` \| `"code"` | |
| `decorators` | function | list[str] | `ast.unparse` of each decorator, in source order |
| `tested` | function | bool | `tested_by` is not empty |
| `tested_by` | function | list[str] | ids of the `test` functions that reach this function (see Coverage), sorted |

## Edges
Every edge is directed `from` → `to`, and both ends are node ids. A call the tool cannot resolve never becomes an edge; it goes to `unresolved_calls` (see Output). There is one edge per `(from, to, kind)`; `line` is where it first occurs.

| kind | from → to | when |
|---|---|---|
| `contains` | module → function, or function → nested function | The `from` is the nearest enclosing def, or the module if there is none. Methods hang off the module, because classes are not nodes. |
| `import` | module → module | An `import` or `from … import` that resolves to a file under ROOT (resolution rules below). Imports that do not resolve make no edge and are counted in `stats.external_imports`. |
| `call` | function → function, or module → function | A `Call` that resolves to a function node (call resolution below). A call at module level, or in a class body outside any method, comes from the module node. A call inside a lambda belongs to the enclosing def. |
| `fixture` | function (role `test` or `fixture`) → function (role `fixture`) | A parameter name matches a fixture's name. An `autouse=True` fixture also gets an edge from every test in its scope. |

**Edge fields:** `from` (str), `to` (str), `kind` (str), `line` (int: the import, call or `def` line in the `from` file).

**Module resolution** for a dotted name `a.b`. Try each location in order and take the first file that exists:
1. In the importing file's own directory: `a/b.py`, then `a/b/__init__.py`. This covers sibling imports in a scripts directory, the way `sys.path[0]` does.
2. Under ROOT: `ROOT/a/b.py`, then `ROOT/a/b/__init__.py`.

A relative import (`from . import x`, `from ..m import y`) resolves against the importing file's directory, going up one level per extra dot. In `from pkg import name`, `name` resolves to a submodule if that file exists; otherwise it is a function or class defined in `pkg`.

**Call resolution.** The rules are tried in this order; the first one that matches wins.
1. **`name(...)`**
   - Look in this order: functions nested in the enclosing def(s), then module-level defs and classes in the same module, then names bound by `from m import name [as alias]` where `m` resolves under ROOT.
   - If the name is a **class**, the call resolves to `<class>::__init__` when that method exists on the class or on a base class (see rule 4). If no such method exists, there is no edge and the call is not listed as unresolved.
2. **`mod.name(...)`**: `mod` is bound by `import x.y as mod`, or by `from x import mod`, and resolves to a module under ROOT. The call resolves to `name` in that module, either a function or a class as in rule 1.
3. **`C.name(...)`**: `C` resolves to a class through rules 1 or 2. The call resolves to method `name` on `C`, using rule 4.
4. **`self.name(...)` or `cls.name(...)`** inside a method: resolves to method `name` on the enclosing class.
   - Method lookup goes through the class first, then its bases. Bases are searched left to right, depth first, and only bases that resolve by name to a class under ROOT are followed. The first hit wins.
5. **Constructor locals**: inside one def, `x = C(...)` binds `x` to class `C` when `C` resolves by rules 1–3. Later calls `x.name(...)` in the same def then resolve by rule 4 on `C`. No other assignment is tracked: `f = helper; f()` stays unresolved, as the digest says.
6. **External**: the root name is a Python builtin (`dir(builtins)`), or it is bound by an import that does not resolve under ROOT. There is no edge, the call is not listed, and it is counted in `stats.external_calls`.
7. **Anything else** goes to `unresolved_calls`, with one reason:
   - `dynamic`: the callee is not a name or an attribute chain. Examples: `getattr(o, n)()`, `fs[i]()`, `g()()`.
   - `attribute`: `x.name()` where `x` is not tracked by rules 2–5.
   - `name`: a bare name that no rule found.

**Fixture lookup.** A parameter `p` of a `test` or `fixture` function maps to the first fixture named `p`.
- A fixture's name is the literal `name=` argument of its decorator if there is one; otherwise it is the function name.
- Search order: the same class, then module level in the same file, then `conftest.py` in the file's directory, then `conftest.py` in each parent directory up to ROOT.
- An `autouse` fixture's scope is its file, plus everything under its directory when it is defined in a `conftest.py`.
- Parameters that match no fixture (pytest built-ins such as `tmp_path`, or `parametrize` arguments) make no edge.

## CLI
```
code_graph.py [ROOT] [--exclude GLOB]... [--test-glob GLOB]...
```
- `ROOT`: the directory to scan. Default `.`.
- `--exclude GLOB`: can be repeated. An `fnmatch` pattern matched against each file's path relative to ROOT; a matching file is skipped. These directories are always skipped: `.git`, `__pycache__`, `.venv`, `venv`, `node_modules`, `.tox`, `.mypy_cache`, `.pytest_cache`, `build`, `dist`. Other dot-directories are scanned, because the skill's scripts live under `.claude/`.
- `--test-glob GLOB`: can be repeated. Each use **replaces** the default list `test_*.py`, `*_test.py`. `conftest.py` is always a test file.
- Output: the JSON object on stdout, printed with `json.dumps(obj, indent=2, sort_keys=True)`.
- Exit codes:
  - `0`: done, and `errors` is empty.
  - `1`: done, but `errors` is not empty. The JSON is still printed in full.
  - `2`: usage error (ROOT is not a directory). Nothing goes to stdout; a message goes to stderr.
- Files are walked in sorted path order. Two runs on the same tree give byte-identical output.

## Output
```json
{
  "schema": "code_graph/1",
  "tier": "stdlib-ast",
  "root": "<ROOT exactly as given on the command line>",
  "nodes": [
    {"id": "pkg/gate.py", "kind": "module", "file": "pkg/gate.py", "line": 1, "end_line": 120, "is_test_file": false},
    {"id": "pkg/gate.py::Gate::decide", "kind": "function", "file": "pkg/gate.py", "line": 40, "end_line": 61,
     "is_test_file": false, "name": "decide", "qualname": "Gate.decide", "module": "pkg/gate.py",
     "role": "code", "decorators": [], "tested": true, "tested_by": ["tests/test_gate.py::test_decide"]}
  ],
  "edges": [
    {"from": "tests/test_gate.py::test_decide", "to": "pkg/gate.py::Gate::decide", "kind": "call", "line": 9}
  ],
  "unresolved_calls": [
    {"from": "pkg/gate.py::Gate::run", "line": 77, "text": "getattr(self, name)", "reason": "dynamic"}
  ],
  "coverage": {
    "rule": "transitive",
    "follows": ["call", "fixture"],
    "tested": 3,
    "total": 10,
    "ratio": 0.3,
    "untested": ["pkg/gate.py::Gate::reset"]
  },
  "stats": {
    "files": 12, "modules": 12, "functions": 40, "tests": 9, "fixtures": 2,
    "edges": {"contains": 40, "import": 15, "call": 60, "fixture": 4},
    "unresolved": {"dynamic": 1, "attribute": 30, "name": 2},
    "external_calls": 210, "external_imports": 18
  },
  "errors": [{"file": "pkg/broken.py", "line": 3, "message": "SyntaxError: invalid syntax"}]
}
```

**Sort order:**
- `nodes`: by `id`.
- `edges`: by `(from, to, kind)`.
- `unresolved_calls`: by `(from, line, text)`.
- `untested` and `tested_by`: sorted.

**Unresolved call text:** `ast.unparse(call.func)`, cut to 80 characters.

**A file that does not parse:** it gets an `errors` entry and no nodes, and the scan carries on.

**Other contents of `errors`:** a duplicate module id, which can only come from symlinks.

## Coverage
**The query:** a `code` function F is **tested** when some function T with `role == "test"` has a path T → … → F of one or more edges, every one of kind `call` or `fixture`. `tested_by(F)` is the sorted set of those T.

**How it is computed:**
1. Build an adjacency list that holds only `call` and `fixture` edges.
2. For each test T, run a BFS from T with a visited set, so cycles end. Add T to `tested_by` of every function node the BFS reaches.
3. Set `tested = bool(tested_by)` on every function node.
4. Totals:
   - `coverage.total`: the number of nodes with `role == "code"`.
   - `coverage.tested`: the number of those with `tested` true.
   - `coverage.ratio`: `round(tested / total, 4)`, or `null` when `total` is 0.
   - `coverage.untested`: the ids of the `code` nodes that are not tested.

The BFS can pass through `test_support`, `fixture` and other `code` functions. `contains` and `import` edges are **not** followed: importing a module does not count as testing its functions. Module-level calls are not starting points.

**What the numbers mean:**
- **"untested" means "no static path found", not "no test runs it".** A false *untested* comes from everything listed under rule 7 (`unresolved_calls`). It also comes from:
  - decorators that wrap or register functions;
  - `monkeypatch` and mocks;
  - calls through containers or callbacks;
  - code run in a subprocess.
- **A false *tested* is possible too.** A call edge on a branch that never runs still counts.

UNCLEAR: Many tests in this repo run the skill scripts as subprocesses (for example `tests/test_validate_result.py` calls `subprocess` on the script path). These tests produce no edges, so every function in `.claude/skills/workflow-design/scripts/` will show as untested even though tests run it. / Best guess: accept this for v1 and list it as a blind spot. A later `runs` edge kind (test → module when the test's source names that script's file in a string literal) could close it.

UNCLEAR: Rule 5 (constructor locals) and the `fixture` edge kind go a little beyond the digest. The digest says ast "cannot map" fixtures; this spec maps them by pytest's own default name rule. / Best guess: keep both. Without rule 5, nearly every method called on an object in a test (`g = Gate(); g.decide()`) is unresolved, and coverage would mean very little. A reviewer who wants the plain digest tier can remove both.
