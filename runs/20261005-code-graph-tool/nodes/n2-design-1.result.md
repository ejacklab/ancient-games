---
node: n2-design
attempt: 1
engine: claude
model: claude-opus-5-5
status: ok
started: 2026-10-06T08:41:02.413Z
ended: 2026-10-06T08:42:25.439Z
evidence: none
---
# Spec: code_graph.py

Location: `.claude/skills/workflow-design/scripts/code_graph.py`. Python 3 stdlib only: `ast`, `argparse`, `json`, `pathlib`, `fnmatch`, `sys`. It parses source with `ast.parse` and never imports or runs the code it reads. Tier: **stdlib-ast**, as described in the n1 digest. Calls that only show up when the code runs are not resolved. They are recorded as `resolved: false` and left out of coverage.

## Nodes
A node is either one **module** (one `.py` file) or one **function** (a `def` or `async def` at any depth, including methods and nested functions). Classes are not nodes. A method's id goes through its class name.

- **Module id:** the file's path relative to ROOT, with `.py` removed and `/` replaced by `.`. A trailing `.__init__` is dropped, so `pkg/__init__.py` becomes `pkg`.
- **Function id:** `<module id>.<enclosing class or def names>.<name>`, for example `ancient_games.gate.Gate.decide` or `m.outer.inner`.
- **Duplicate ids** (for example `a.py` next to `a/__init__.py`): keep the first one in sorted path order and record the second in `errors`.

Fields (every node has all of them):

| field | type | meaning |
|---|---|---|
| `id` | str | as above |
| `kind` | `"module"` \| `"function"` | |
| `file` | str | path relative to ROOT, posix separators |
| `line` | int | the `def` line (1 for a module) |
| `end_line` | int | `node.end_lineno` (a module uses its last line) |
| `test` | bool | the function is a pytest test, or for a module: the file is a test file (see Coverage) |
| `fixture` | bool | the function has a decorator named `fixture` (`@pytest.fixture`, `@fixture`, with or without a call) |
| `decorators` | [str] | `ast.unparse` of each decorator expression, in source order. Always `[]` for modules. Recorded because decorator effects are invisible to `ast`. |

## Edges
An edge is directed **from the code that does something to the target**. Fields: `from` (node id), `to` (a node id, or the raw source text when not resolved), `kind`, `line` (the line of the first occurrence in `from`), `resolved` (bool). There is one edge per `(from, to, kind)`: later occurrences of the same edge are merged into it.

Kinds:
- **`contains`**: module → its top-level functions and its class methods; function → its nested functions. Always resolved.
- **`import`**: module → module, for every `import X` / `from X import ...` anywhere in the file. `from pkg import sub`, where `pkg.sub` is a module node, points to `pkg.sub`. Otherwise it points to `pkg`. The target is looked up in this order, and the first hit wins:
  1. An absolute name that is a module id under ROOT.
  2. The same name taken from the importing file's directory. This is a sibling script; Python puts a script's own directory on `sys.path`.
  3. A relative import (`from . import x`, `from ..a import b`), resolved against the importing module's package.

  If nothing matches (stdlib or third-party), the edge gets `to` = the dotted name and `resolved: false`.
- **`call`**: function → function, for every `ast.Call` in the function's own body. Calls inside nested defs belong to the nested function. Calls at module level have `from` = the module id. The callee is looked up in this order, and the first match wins:
  1. A bare name `f` that is a def in an enclosing function scope, then a module-level def in the same module.
  2. A bare name bound by `from M import f [as g]`, where M resolves (import rules above) and `M.f` is a function node.
  3. `alias.f(...)` where `alias` is bound by `import M [as alias]`, and `alias.a.f` for `import a.b`. Resolves to `M.f`.
  4. `self.f(...)` / `cls.f(...)` inside a method, where `f` is defined in the **same** class. Inheritance is not followed.
  5. `C.f(...)` where `C` is a class defined in, or imported into, this module. Calling `C(...)` resolves to `C.__init__` if it is defined.

  Anything else, such as `f = helper; f()`, `getattr(...)()`, `obj.method()` on an unknown object, or builtins, is recorded with `to` = `ast.unparse(call.func)` and `resolved: false`. Local rebinding that hides a name is not tracked. That is a stated limit of this tier.

## CLI
```
code_graph.py [ROOT] [--exclude GLOB ...] [--indent N]
```
- `ROOT`: the directory to scan. The default is `.`. It walks every `*.py` file under ROOT in sorted path order.
- `--exclude GLOB`: can be repeated. It is matched with `fnmatch` against each relative path and against each directory name. The default excludes are always applied: `.git`, `__pycache__`, `.venv`, `venv`, `node_modules`.
- `--indent N`: JSON indent. The default is none (one line).
- The JSON object goes to stdout. Nothing is written to disk.
- Exit codes: `0` ok. Files that fail to parse still give `0` and are listed in `errors`. `2` is a usage error: ROOT is missing or not a directory.

## Output
One JSON object with keys sorted (`json.dumps(..., sort_keys=True)`). Nodes are sorted by `id`. Edges are sorted by `(from, kind, to)`.
```
{"tool": "code_graph.py", "version": 1, "tier": "stdlib-ast", "root": "<ROOT as given>",
 "nodes": [{"id": "pkg.mod.f", "kind": "function", "file": "pkg/mod.py", "line": 12, "end_line": 20,
            "test": false, "fixture": false, "decorators": []}],
 "edges": [{"from": "pkg.mod", "to": "pkg.mod.f", "kind": "contains", "line": 12, "resolved": true},
           {"from": "tests.test_mod.test_f", "to": "pkg.mod.f", "kind": "call", "line": 5, "resolved": true},
           {"from": "pkg.mod.f", "to": "getattr(obj, name)", "kind": "call", "line": 15, "resolved": false}],
 "coverage": {"tested": 3, "total": 10,
              "untested": ["pkg.mod.g"],
              "tested_by": {"pkg.mod.f": ["tests.test_mod.test_f"]},
              "modules": {"pkg.mod": {"tested": 1, "total": 2}}},
 "errors": [{"file": "bad.py", "line": 3, "message": "invalid syntax"}],
 "stats": {"files": 4, "nodes": 14, "edges": 22, "unresolved_calls": 5}}
```
`untested` and every list in `tested_by` are sorted. `modules` has an entry only for modules that contain at least one counted function.

## Coverage
This is static reachability over the graph, not line coverage.

1. **Test file:** the basename matches `test_*.py` or `*_test.py`, or the basename is `conftest.py`. These are pytest's default patterns.
2. **Test function (`test: true`):** a function in a test file whose name starts with `test`, and which is either at module level or a method of a class whose name starts with `Test`.
3. **Counted functions (the `total`):** every function node that is **not** in a test file. Helpers, fixtures and anything else in test files are left out.
4. **Tested:** a counted function is tested when some test function reaches it through a path of **resolved `call` edges**, of any length. Use breadth-first search from each test function. `tested_by[id]` lists the test functions that reach it.
5. **Rollups:** `tested` = number of tested counted functions; `total` = number of counted functions; `untested` = counted functions minus tested ones. `modules[m]` gives the same counts restricted to functions whose `file` is module m's file.
6. **Known blind spots, written down rather than guessed:**
   - Code reached only through a pytest fixture is **not** counted, because injected parameters are invisible to `ast`.
   - Unresolved calls are not followed.
   - Code reached through decorators, `getattr` or dynamic dispatch is not counted.

   So `tested` is a lower bound.

UNCLEAR: should "tested" mean any distance from a test (transitive) or only a test's direct calls? / Best guess: transitive (step 4). `tested_by` holds the test ids, so a direct-only view can be added later if it is wanted.
UNCLEAR: should unresolved call edges always appear in `edges`, or only behind a flag? / Best guess: always, with `resolved: false`. They are how a reader sees this tier's limits, and `stats.unresolved_calls` counts them.
