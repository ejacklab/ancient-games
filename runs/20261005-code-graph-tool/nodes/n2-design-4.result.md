---
node: n2-design
attempt: 4
engine: claude
model: claude-opus-5-5
status: ok
started: 2026-10-06T08:49:06.897Z
ended: 2026-10-06T08:50:21.689Z
evidence: none
---
# Spec: code_graph.py

**Location:** `.claude/skills/workflow-design/scripts/code_graph.py`

**Runtime:** Python 3.9 or newer, because it needs `ast.unparse`. Python 3.12.3 is installed here. It uses only the standard library: `ast`, `argparse`, `builtins`, `collections`, `fnmatch`, `json`, `pathlib`, `sys`. Each file is read with `ast.parse`. The tool never imports or runs the code it reads.

**Tier:** `stdlib-ast`, the cheapest of the three tiers in the n1 digest. The tool adds one thing on top of it: imports are resolved by name across the files under ROOT. This is a plain file lookup, not PyCG.

**Digest source:** `runs/20261005-code-graph-tool/nodes/n1-research-1.result.md`. The brief said the digest was included, but it was not, so I read it from the run folder. I read no raw research.

## Nodes
A node is either a **module** or a **function**. Classes are not nodes; their names appear only inside function ids.

- **module**: one `.py` file under ROOT.
  - id: the file's path relative to ROOT, with `/` separators. Example: `ancient_games/gate.py`.
- **function**: one `def` or `async def` at any depth, including methods and nested functions.
  - id: `<module id>::<each enclosing class or def name>::<name>`. Examples: `ancient_games/gate.py::Gate::decide`, `m.py::outer::inner`.
  - When ROOT is the pytest rootdir, a test's id is the same as its pytest node id, for example `tests/test_x.py::TestA::test_b`. That id can be passed straight to `pytest`.
  - If a module defines the same name twice, the **last** definition keeps the plain id. Each earlier one gets the suffix `@<line>`, for example `m.py::f@12`. Calls resolve to the last definition, as they do in Python.

**Test file:** a file whose name matches a `--test-glob` (defaults: `test_*.py` and `*_test.py`), or any file named `conftest.py`.

**Function roles.** Every function has exactly one:
- `test`: it is in a test file, its name starts with `test`, and it is either at module level or a method of a module-level class whose name starts with `Test`.
- `fixture`: it has a `pytest.fixture` or `fixture` decorator, bare or called.
- `test_support`: any other function in a test file.
- `code`: any function that is not in a test file. **Only `code` functions count toward coverage.**

The tool does not read pytest settings in `pytest.ini`, `pyproject.toml` or `setup.cfg` (such as `python_functions` or `python_classes`). It uses the defaults above.

**Fields.** Every node has every field listed for its kind.

| field | kind | type | meaning |
|---|---|---|---|
| `id` | both | str | as defined above |
| `kind` | both | `"module"` \| `"function"` | |
| `file` | both | str | path relative to ROOT, `/` separators |
| `line` | both | int | the `def` line; 1 for a module |
| `end_line` | both | int | `node.end_lineno`; for a module, its last line |
| `is_test_file` | both | bool | the file is a test file |
| `name` | function | str | the bare name, for example `decide` |
| `qualname` | function | str | the enclosing names joined with `.`, for example `Gate.decide` |
| `module` | function | str | the id of the module that contains it |
| `role` | function | `"test"` \| `"fixture"` \| `"test_support"` \| `"code"` | |
| `decorators` | function | list[str] | `ast.unparse` of each decorator, in source order |
| `tested` | function | bool | true when `tested_by` is not empty |
| `tested_by` | function | list[str] | the ids of the `test` functions that reach this function (see Coverage), sorted |

## Edges
Every edge points from `from` to `to`, and both ends are node ids. A call the tool cannot resolve never becomes an edge; it goes to `unresolved_calls` (see Output). There is one edge per `(from, to, kind)`, and `line` is where that edge first occurs.

| kind | from → to | when |
|---|---|---|
| `contains` | module → function, or function → nested function | `from` is the nearest enclosing def, or the module if there is none. Methods hang off the module, because classes are not nodes. |
| `import` | module → module | An `import` or `from … import` that resolves to a file under ROOT (see module resolution below). An import that does not resolve makes no edge and is counted in `stats.external_imports`. |
| `call` | function → function, or module → function | A `Call` that resolves to a function node (see call resolution below). A call at module level, or in a class body outside any method, comes from the module node. A call inside a lambda belongs to the enclosing def. |
| `fixture` | function with role `test` or `fixture` → function with role `fixture` | A parameter name matches a fixture's name. An `autouse=True` fixture also gets an edge from every test in its scope. |

**Edge fields:** `from` (str), `to` (str), `kind` (str), and `line` (int: the line of the import, call or `def` in the `from` file).

**Module resolution.** For a dotted name `a.b`, try each location in order and take the first file that exists:
1. In the importing file's own directory: `a/b.py`, then `a/b/__init__.py`. This covers sibling imports inside a scripts directory, as `sys.path[0]` does.
2. Under ROOT: `ROOT/a/b.py`, then `ROOT/a/b/__init__.py`.

A relative import (`from . import x`, `from ..m import y`) resolves against the importing file's directory, going up one level for each extra dot. In `from pkg import name`, `name` resolves to a submodule if that file exists. Otherwise it is a function or class defined in `pkg`.

**Call resolution.** The rules are tried in this order, and the first one that matches wins.
1. **`name(...)`**
   - The lookup order is: functions nested in the enclosing def or defs, then module-level defs and classes in the same module, then names bound by `from m import name [as alias]` where `m` resolves under ROOT.
   - If the name is a **class**, the call resolves to `<class>::__init__` when that method exists on the class or on a base class (see rule 4). If no such method exists, there is no edge and the call is not listed as unresolved.
2. **`mod.name(...)`**: `mod` is bound by `import x.y as mod` or by `from x import mod`, and it resolves to a module under ROOT. The call resolves to `name` in that module, either a function or a class as in rule 1.
3. **`C.name(...)`**: `C` resolves to a class through rule 1 or 2. The call resolves to method `name` on `C`, using rule 4.
4. **`self.name(...)` or `cls.name(...)`** inside a method: the call resolves to method `name` on the enclosing class.
   - Method lookup checks the class first, then its bases. Bases are searched left to right, depth first. Only bases that resolve by name to a class under ROOT are followed. The first hit wins.
5. **Constructor locals.** Inside one def, `x = C(...)` binds `x` to class `C` when `C` resolves by rules 1 to 3. A later call `x.name(...)` in the same def then resolves by rule 4 on `C`. No other assignment is tracked.
6. **External.** The root name is a Python builtin (`dir(builtins)`), or it is bound by an import that does not resolve under ROOT. There is no edge, the call is not listed, and it is counted in `stats.external_calls`.
7. **Anything else** goes to `unresolved_calls` with one reason:
   - `dynamic`: the callee is not a name or an attribute chain, for example `getattr(o, n)()`, `fs[i]()` or `g()()`.
   - `attribute`: `x.name()` where `x` is not tracked by rules 2 to 5.
   - `name`: a bare name that no rule found.

**Fixture lookup.** A parameter `p` of a `test` or `fixture` function maps to the first fixture named `p`.
- A fixture's name is the literal `name=` argument of its decorator if there is one. Otherwise it is the function name.
- The search order is: the same class, then module level in the same file, then `conftest.py` in the file's directory, then `conftest.py` in each parent directory up to ROOT.
- An `autouse` fixture's scope is its own file. When it is defined in a `conftest.py`, its scope also covers everything under that file's directory.
- A parameter that matches no fixture makes no edge. Examples are pytest's built-in fixtures, such as `tmp_path`, and `parametrize` arguments.
- This applies pytest's default lookup rule by name; it does not run pytest. The digest says `ast` cannot map fixtures. That is true of runtime injection, and those cases are listed under *What it cannot see*.

## CLI
```
code_graph.py [ROOT] [--exclude GLOB]... [--test-glob GLOB]...
```
- `ROOT`: the directory to scan. The default is `.`.
- `--exclude GLOB` (repeatable): an `fnmatch` pattern matched against each file's path relative to ROOT. A matching file is skipped.
  - These directories are always skipped: `.git`, `__pycache__`, `.venv`, `venv`, `node_modules`, `.tox`, `.mypy_cache`, `.pytest_cache`, `build`, `dist`.
  - Other dot-directories are scanned, because the skill's scripts live under `.claude/`.
- `--test-glob GLOB` (repeatable): the first use **replaces** the default list (`test_*.py`, `*_test.py`). `conftest.py` is always a test file.
- Output: the JSON object on stdout, printed with `json.dumps(obj, indent=2, sort_keys=True)`.
- Exit codes:
  - `0`: done, and `errors` is empty.
  - `1`: done, but `errors` is not empty. The full JSON is still printed.
  - `2`: usage error, such as ROOT not being a directory. Nothing goes to stdout; a message goes to stderr.
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
- `nodes` by `id`.
- `edges` by `(from, to, kind)`.
- `unresolved_calls` by `(from, line, text)`.
- `untested` and `tested_by` are sorted.

**Unresolved call text:** `ast.unparse(call.func)`, cut to 80 characters.

**A file that does not parse** gets one `errors` entry and no nodes, and the scan carries on.

**`errors` can also hold** a duplicate module id, which can only come from a symlink.

## Coverage
**The query** (transitive, decided 2026-10-05): a `code` function F is **tested** when some function T with `role == "test"` has a path T → … → F of one or more edges, each of kind `call` or `fixture`. `tested_by(F)` is the sorted set of those T.

**How it is computed:**
1. Build an adjacency list from the `call` and `fixture` edges only.
2. For each test T, run a breadth-first search from T, keeping a visited set so that cycles end. Add T to the `tested_by` of every function node the search reaches.
3. Set `tested = bool(tested_by)` on every function node.
4. Fill in the totals:
   - `coverage.total`: the number of nodes with `role == "code"`.
   - `coverage.tested`: how many of those have `tested` true.
   - `coverage.ratio`: `round(tested / total, 4)`, or `null` when `total` is 0.
   - `coverage.untested`: the ids of the `code` nodes that are not tested.

The search can pass through `test_support`, `fixture` and other `code` functions. It does **not** follow `contains` or `import` edges: importing a module does not count as testing its functions. Module-level calls are not starting points.

**What the numbers mean:**
- **"Untested" means "no static path was found", not "no test runs it".** Every gap listed below can make a function show as untested when a test does run it.
- **A false "tested" is also possible.** A call edge on a branch that never runs still counts.

### What it cannot see
These are known v1 blind spots. Each one leaves an edge out, so the function on the far end can show as untested.

1. **Code that a test runs in a subprocess.** A test that runs a script with `subprocess` instead of importing it creates no edge, so that script's functions show as untested. This repo does that in many tests, for example `tests/test_validate_result.py`, `tests/test_quote_check.py` and `tests/test_dispatch.py`. Accepted as a v1 blind spot (decided 2026-10-05).
   - **Future fix, not in v1:** an edge kind `runs` (test → module). It would be added when the test's source names that script's path in a string literal or in a `Path(...)` expression, and coverage would then follow `runs` into the module's functions.
2. **Imports that depend on a `sys.path` change made at runtime.** For example, `tests/test_dispatch.py` does `sys.path.insert(0, str(SCRIPT.parent))` and then `import engines`. Neither module-resolution location finds `engines.py`, so the import makes no edge (it is counted in `external_imports`), and calls through it are counted as external.
3. **Dynamic dispatch:** `f = helper; f()`. Only the constructor-locals rule (rule 5) tracks an assignment (digest).
4. **`getattr(obj, "x")()`**, and calls through containers or callbacks such as `fs[i]()` and `map(f, xs)`. These go to `unresolved_calls` or are counted as external (digest).
5. **What decorators do.** Decorators are recorded as text, but a decorator that wraps, replaces or registers a function is not followed (digest).
6. **Fixtures pytest injects at runtime**, beyond the name rule above: `request.getfixturevalue`, fixtures from plugins, `usefixtures` marks, and parametrized indirect fixtures (digest).
7. **`monkeypatch` and mocks.** The edge points at the real function even when a test replaces it.
8. **Calls on objects the tool does not track**, such as an object passed in as a parameter or returned by a function. These are listed with reason `attribute`.
9. **pytest naming settings** in config files (`python_functions`, `python_classes`, `python_files`) are not read.
