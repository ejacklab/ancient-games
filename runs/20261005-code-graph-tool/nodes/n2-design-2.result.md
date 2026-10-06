I've checked how this repo's tests import the skill scripts. Writing the spec now.

---
node: n2-design
attempt: 2
engine: claude
model: claude-opus-5-5
status: ok
started: 2026-10-06T08:43:01.665Z
ended: 2026-10-06T08:44:34.020Z
evidence: none
---
# Spec: code_graph.py

**Location:** `.claude/skills/workflow-design/scripts/code_graph.py`
**Dependencies:** Python 3.10 or newer, standard library only (`ast`, `argparse`, `json`, `pathlib`, `fnmatch`, `collections`, `sys`). The tool reads each file with `ast.parse` and never imports or runs the code it reads.

**Tier:** `stdlib-ast`, as in the n1 digest. On top of that tier, the tool resolves imports by name across files. This is a simple lookup, not PyCG.

**What it cannot see:** anything that only shows up when the code runs. That means `f = helper; f()`, `getattr(...)()`, what decorators do, and pytest fixture injection. These calls are recorded as `resolved: false`, coverage does not follow them, and they are listed under Coverage as blind spots.

## Nodes
There are two node kinds. Classes are not nodes; they only appear in function ids.

- **`module`**: one `.py` file under ROOT.
  - Its id is the file path relative to ROOT, with `/` separators. Example: `ancient_games/gate.py`.
- **`function`**: one `def` or `async def` at any depth. That includes methods and nested functions.
  - Its id is `<module id>::<each enclosing class or def name>::<name>`. Examples: `ancient_games/gate.py::Gate::decide`, `m.py::outer::inner`, `tests/test_gate.py::TestGate::test_x`.
  - This is the same format as a pytest node id, so a test id in `tested_by` can be passed straight to `pytest`. It also avoids the ambiguity that dotted ids have under directories such as `.claude/`.
  - If one file defines the same id more than once (a `@x.setter` beside `@property x`, or a `try`/`except` with two versions of a def), those defs are **merged into one node**:
    - `line` is the first def's line.
    - `end_line` is the largest end line.
    - `decorators` is all of them, in source order.
    - The node's outgoing calls are the union of the calls from all of them.

Every node has every field:

| field | type | meaning |
|---|---|---|
| `id` | str | as above |
| `kind` | `"module"` \| `"function"` | |
| `file` | str | path relative to ROOT, `/` separators |
| `line` | int | the `def` line, or 1 for a module |
| `end_line` | int | `end_lineno` of the def, or the file's last line for a module |
| `test` | bool | function: it is a test function (Coverage rule 2). Module: it is a test file (Coverage rule 1). |
| `fixture` | bool | at least one decorator, with any call removed, unparses to `fixture` or ends in `.fixture` |
| `decorators` | [str] | `ast.unparse` of each decorator, in source order; always `[]` for a module |

## Edges
Edges are directed **from the code that does something to the thing it acts on**.

**Fields:**
- `from`: a node id.
- `to`: a node id, or the raw source text when `resolved` is false.
- `kind`: one of the three kinds below.
- `line`: the line of the first occurrence.
- `resolved`: bool.

There is one edge per `(from, kind, to)`. Repeat occurrences are merged into the first one.

**Kinds:**

- **`contains`**
  - From a module to its top-level functions and to the methods of its top-level classes.
  - From a function to the functions defined in its body, and to the methods of classes defined in its body.
  - Always resolved.

- **`import`**: module → module, for every `import` statement anywhere in the file. One edge per imported name.
  - **Resolving the target:**
    - **Relative import** (`level > 0`, e.g. `from . import x` or `from ..a import b`): look it up from the directory of the importing file, going up `level - 1` directories.
    - **Absolute dotted name `a.b`**: try each of these in order. The first one that hits wins.
      1. ROOT
      2. the directory of the importing file (Python puts a script's own directory on `sys.path`)
      3. each `--path` directory, in the order given

      In each of these, look for the file `a/b.py`, then `a/b/__init__.py`.
  - **`from M import n`** points to the submodule `M.n` if that is a module. Otherwise it points to `M`.
  - If nothing is found (standard library, third-party, or a missing path), the edge is `to` = the dotted name, `resolved: false`.

- **`call`**: one edge per `ast.Call`.
  - **Where `from` comes from:**
    - A call inside a function belongs to that function. A call inside a nested def belongs to the nested def, not to the outer function.
    - A call at module level, or in a class body outside any def, belongs to the module.
  - **Resolving the callee:** try each of these in order. The first match wins.
    1. **Bare name `f`.** First look for a def named `f` in an enclosing function scope, innermost first. Then look for a module-level def `f` in the same file.
    2. **Bare name bound by an import.** `f` is bound by `from M import f` or `from M import f as g`, where M resolves (import rules above) and `M::f` is a function node.
    3. **Module alias.** The call is `alias.f(...)`, where `alias` is bound by `import M` or `import M as alias`. It resolves to `M::f`. For `import a.b`, the call `a.b.f(...)` resolves to `a/b.py::f`.
    4. **`self` or `cls`.** The call is `self.f(...)` or `cls.f(...)` inside a method, and `f` is a method of the **same** class. Base classes are not searched.
    5. **Class name.** The call is `C.f(...)` or `C(...)`, where `C` is a class defined in this file or bound by an import as in steps 2 and 3. `C.f(...)` resolves to `C::f`. `C(...)` resolves to `C::__init__` if it exists. Otherwise the call is unresolved.
  - **Anything else** is recorded with `to` = `ast.unparse(call.func)` and `resolved: false`. That includes `obj.method()` on an object of unknown type, builtins, `getattr(...)()` and calls through a local variable.
  - **Not tracked:** a local name that shadows a def or an import. This is a stated limit of this tier.
  - **Decision (was UNCLEAR in attempt 1):** unresolved edges are **always** written to the output; there is no flag to switch them on. They are how a reader sees where this tier stops seeing, and `stats.unresolved_calls` counts them. A consumer that only wants resolved edges filters on `resolved`.

## CLI
```
code_graph.py [ROOT] [--path DIR ...] [--exclude GLOB ...] [--indent N]
```
- **`ROOT`**: the directory to scan. The default is `.`. The tool walks every `*.py` file under ROOT in sorted path order.
- **`--path DIR`** (repeatable): an extra import root, the same as a `sys.path` entry. A relative DIR is relative to ROOT.
  - This repo needs it. Its tests do `sys.path.insert(0, SCRIPTS)` and then `import workload`, so the scan here should use `--path .claude/skills/workflow-design/scripts --path tests`.
  - The tool does not try to discover `sys.path.insert` calls on its own.
- **`--exclude GLOB`** (repeatable): matched with `fnmatch` against the relative path of each file and against the name of each directory.
  - These are always excluded: `.git`, `__pycache__`, `.venv`, `venv`, `node_modules`, `.mypy_cache`, `.pytest_cache`.
  - Other hidden directories, such as `.claude`, are **not** excluded.
- **`--indent N`**: JSON indent. The default is no indent (one line).
- **Output:** the JSON object goes to stdout. The tool writes nothing to disk.
- **Exit codes:**
  - `0`: ok. A file that fails to parse is listed in `errors` and still exits `0`.
  - `2`: usage error. ROOT or a `--path` directory is missing or is not a directory.

## Output
One JSON object, written with `json.dumps(obj, sort_keys=True, indent=N)`.
- Nodes are sorted by `id`.
- Edges are sorted by `(from, kind, to)`.
- `untested` is sorted, and so is every list in `tested_by`.

```
{"tool": "code_graph.py", "version": 1, "tier": "stdlib-ast", "root": "<ROOT as given>",
 "paths": ["<each --path as given>"],
 "nodes": [{"id": "pkg/mod.py::f", "kind": "function", "file": "pkg/mod.py", "line": 12, "end_line": 20,
            "test": false, "fixture": false, "decorators": []},
           {"id": "pkg/mod.py", "kind": "module", "file": "pkg/mod.py", "line": 1, "end_line": 40,
            "test": false, "fixture": false, "decorators": []}],
 "edges": [{"from": "pkg/mod.py", "to": "pkg/mod.py::f", "kind": "contains", "line": 12, "resolved": true},
           {"from": "tests/test_mod.py", "to": "pkg/mod.py", "kind": "import", "line": 1, "resolved": true},
           {"from": "tests/test_mod.py::test_f", "to": "pkg/mod.py::f", "kind": "call", "line": 5, "resolved": true},
           {"from": "pkg/mod.py::f", "to": "getattr(obj, name)", "kind": "call", "line": 15, "resolved": false}],
 "coverage": {"tested": 3, "total": 10,
              "untested": ["pkg/mod.py::g"],
              "tested_by": {"pkg/mod.py::f": ["tests/test_mod.py::test_f"]},
              "modules": {"pkg/mod.py": {"tested": 1, "total": 2}}},
 "errors": [{"file": "bad.py", "line": 3, "message": "invalid syntax"}],
 "stats": {"files": 4, "parsed": 3, "nodes": 14, "edges": 22, "unresolved_calls": 5, "unresolved_imports": 2}}
```
- `tested_by` has a key only for counted functions that are tested.
- `modules` has a key only for modules that contain at least one counted function.
- A file listed in `errors` gets a module node, with `end_line` set to 1 and no other nodes or edges.

## Coverage
This is **static reachability** over the graph. It is not line coverage, and it is **transitive** (decided 2026-10-05).

1. **Test file.** The basename matches `test_*.py`, `*_test.py`, or is `conftest.py`. These are pytest's default patterns.
2. **Test function** (`test: true`). A function in a test file whose name starts with `test`, and which is either:
   - at module level, or
   - a method of a top-level class whose name starts with `Test`.
3. **Counted functions** (`total`). Every function node whose file is **not** a test file. Helpers and fixtures in test files are not counted.
4. **Tested.** A counted function is tested if a test function reaches it through a path of **resolved `call` edges** of any length (one or more).
   - Do one breadth-first search from each test function, over resolved `call` edges only.
   - Add the test's id to `tested_by[f]` for every counted `f` that the search reaches.
   - `contains` and `import` edges are not followed. Code that is only defined or imported has not been reached.
5. **Rollups.**
   - `tested`: the number of counted functions that have a `tested_by` entry.
   - `total`: the number of counted functions.
   - `untested`: the counted functions that are not tested.
   - `modules[m]`: the same two counts, but only for the counted functions in file `m`.
6. **Blind spots.** Because of these, `tested` is a **lower bound**:
   - **Fixtures.** Code reached only through a pytest fixture is not followed. A test's parameters are not linked to fixture functions.
   - **Unresolved calls** are not followed. That includes calls through a variable, `getattr`, dynamic dispatch, and inherited methods.
   - **Decorators.** Code that only a decorator reaches, or code it registers, is not seen.
   - **Module-level calls** in a test file are not counted as tests.
   - **Missing `--path`.** A test that imports through a `sys.path` entry that was not passed as `--path` has unresolved imports, so the calls through them are unresolved too. `stats.unresolved_imports` shows when this has happened.
