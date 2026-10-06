#!/usr/bin/env python3
"""code_graph.py -- a static code graph built from Python sources with the stdlib only.

Walks every *.py file under ROOT, records one node per module and one node per
function, and one edge per containment, import, call and fixture injection.  The
code being read is parsed, never imported and never executed.  Coverage is static
reachability from the test functions over call and fixture edges, so it is a
lower bound on what the tests really run.

Two points the spec leaves open, decided here (review findings 2 and 5):

* A role follows where the function lives.  Every function outside a test file is
  `code`, so one decorated `@pytest.fixture` outside a test file counts toward
  `coverage.total`.  The decorator still makes it injectable, and a `fixture`
  edge still points at it; being a fixture is a binding fact, not a role.
* Imports bind module-wide whatever their scope.  A function-local
  `import x.y as mod` binds `mod` in the module's one alias table, so it makes a
  module -> module edge.  This is a whole-module table, not a scope analysis.
"""

from __future__ import annotations

import argparse
import ast
import builtins
import fnmatch
import json
import sys
from collections import defaultdict, deque
from pathlib import Path

SCHEMA = "code_graph/1"
TIER = "stdlib-ast"

BUILTIN_NAMES = frozenset(dir(builtins))

ALWAYS_SKIP_DIRS = frozenset(
    {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        "build",
        "dist",
    }
)

DEFAULT_TEST_GLOBS = ("test_*.py", "*_test.py")
CONFTEST_NAME = "conftest.py"

EDGE_KINDS = ("contains", "import", "call", "fixture")
UNRESOLVED_REASONS = ("dynamic", "attribute", "name")
COVERAGE_FOLLOWS = ("call", "fixture")
FIXTURE_CONSUMERS = ("test", "fixture")
TEXT_LIMIT = 80

RESOLVED = "resolved"
EXTERNAL = "external"
UNRESOLVED = "unresolved"
SILENT = "silent"

DEF_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)


class UsageError(Exception):
    pass


def attribute_parts(expr):
    """Return (root_name, [attr, ...]) for a Name or a pure attribute chain."""
    attrs = []
    current = expr
    while isinstance(current, ast.Attribute):
        attrs.append(current.attr)
        current = current.value
    if not isinstance(current, ast.Name):
        return None
    attrs.reverse()
    return current.id, attrs


def dotted_name(expr):
    parts = attribute_parts(expr)
    if parts is None:
        return None
    root, attrs = parts
    return ".".join([root] + attrs)


def decorator_target(decorator):
    return decorator.func if isinstance(decorator, ast.Call) else decorator


def is_fixture_decorator(decorator):
    name = dotted_name(decorator_target(decorator))
    return bool(name) and name.split(".")[-1] == "fixture"


def is_autouse_decorator(decorator):
    if not isinstance(decorator, ast.Call):
        return False
    for keyword in decorator.keywords:
        if keyword.arg == "autouse":
            try:
                return bool(ast.literal_eval(keyword.value))
            except (ValueError, SyntaxError, TypeError):
                return False
    return False


def has_fixture_decorator(node):
    return any(is_fixture_decorator(d) for d in node.decorator_list)


def fixture_name_of(function):
    for decorator in function.node.decorator_list:
        if not isinstance(decorator, ast.Call) or not is_fixture_decorator(decorator):
            continue
        for keyword in decorator.keywords:
            if keyword.arg == "name":
                try:
                    value = ast.literal_eval(keyword.value)
                except (ValueError, SyntaxError, TypeError):
                    return function.name
                if isinstance(value, str):
                    return value
    return function.name


def parameters(function):
    """Return the declared parameters as (name, line) pairs, receiver excluded.

    The line is the parameter's own `def` line, which is what a `fixture` edge
    reports: an edge's `line` is read in the `from` file.
    """
    args = function.node.args
    declared = list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs)
    if function.is_method and declared and declared[0].arg in ("self", "cls"):
        declared = declared[1:]
    return [(arg.arg, getattr(arg, "lineno", function.node.lineno)) for arg in declared]


def class_by_node(module, node):
    for klass in module.classes:
        if klass.node is node:
            return klass
    return None


def function_by_node(module, node):
    for function in module.functions:
        if function.node is node:
            return function
    return None


class FunctionInfo:
    def __init__(self, node, module, container, enclosing_def_node, enclosing_class, qualname, name_path):
        self.node = node
        self.module = module
        self.container = container
        self.enclosing_def_node = enclosing_def_node
        self.enclosing_def = (
            function_by_node(module, enclosing_def_node) if enclosing_def_node is not None else None
        )
        self.enclosing_class = enclosing_class
        self.qualname = qualname
        self.name_path = list(name_path)
        self.name = node.name
        self.line = node.lineno
        self.end_line = getattr(node, "end_lineno", node.lineno)
        self.decorators = [ast.unparse(d) for d in node.decorator_list]
        self.is_method = isinstance(container, ast.ClassDef)
        self.id = ""
        self.role = "code"
        self.tested = False
        self.tested_by = []
        self.nested = {}
        self.ctor_locals = {}

    def scope_chain(self):
        chain = []
        current = self
        while current is not None:
            chain.append(current)
            current = current.enclosing_def
        return chain


class ClassInfo:
    def __init__(self, node, module, enclosing_def, qualname):
        self.node = node
        self.module = module
        self.enclosing_def = enclosing_def
        self.qualname = qualname
        self.name = node.name
        self.methods = {}
        self.bases = list(node.bases)


class ModuleInfo:
    def __init__(self, path, rel, line_count, tree, is_test_file):
        self.path = path
        self.rel = rel
        self.id = rel
        self.line_count = line_count
        self.tree = tree
        self.is_test_file = is_test_file
        self.is_conftest = rel.rsplit("/", 1)[-1] == CONFTEST_NAME
        self.functions = []
        self.classes = []
        self.module_functions = {}
        self.module_classes = {}
        self.alias_modules = {}
        self.external_aliases = set()
        self.from_names = {}
        self.calls = []
        self.local_fixtures = []
        self.autouse_fixtures = []
        self.contains = []

    def dir_parts(self):
        return self.rel.split("/")[:-1]


class GraphBuilder:
    def __init__(self, root_arg, excludes, test_globs):
        self.root_arg = root_arg
        self.root = Path(root_arg)
        self.excludes = list(excludes)
        self.test_globs = list(test_globs)
        self.modules = []
        self.by_id = {}
        self.lines = {}
        self.errors = []
        self.unresolved = []
        self.edges = {}
        self.files_seen = 0
        self.external_calls = 0
        self.external_imports = 0

    def run(self):
        self.scan_files()
        self.collect_definitions()
        self.assign_ids()
        self.add_contains_edges()
        self.collect_imports()
        self.collect_calls()
        self.collect_ctor_locals()
        self.resolve_calls()
        self.resolve_fixtures()
        return self.render()

    def scan_files(self):
        if not self.root.is_dir():
            raise UsageError(f"not a directory: {self.root_arg}")
        rels = []
        for path in self.root.rglob("*.py"):
            rel = path.relative_to(self.root).as_posix()
            parts = rel.split("/")
            if any(part in ALWAYS_SKIP_DIRS for part in parts[:-1]):
                continue
            if any(fnmatch.fnmatch(rel, pattern) for pattern in self.excludes):
                continue
            rels.append(rel)
        for rel in sorted(rels):
            path = self.root / rel
            try:
                data = path.read_bytes()
            except OSError as exc:
                self.errors.append({"file": rel, "line": 0, "message": f"read error: {exc}"})
                continue
            self.files_seen += 1
            try:
                tree = ast.parse(data, filename=rel)
            except SyntaxError as exc:
                message = f"SyntaxError: {exc.msg}" if exc.msg else "SyntaxError"
                self.errors.append({"file": rel, "line": exc.lineno or 0, "message": message})
                continue
            except ValueError as exc:
                self.errors.append({"file": rel, "line": 0, "message": f"ValueError: {exc}"})
                continue
            if rel in self.by_id:
                self.errors.append({"file": rel, "line": 1, "message": "duplicate module id"})
                continue
            lines = len(data.decode("utf-8", "replace").splitlines())
            info = ModuleInfo(path, rel, lines, tree, self.is_test_file(rel))
            self.by_id[rel] = info
            self.modules.append(info)

    def is_test_file(self, rel):
        if rel.rsplit("/", 1)[-1] == CONFTEST_NAME:
            return True
        return any(self.matches_test_glob(rel, pattern) for pattern in self.test_globs)

    def matches_test_glob(self, rel, pattern):
        if fnmatch.fnmatch(rel.rsplit("/", 1)[-1], pattern):
            return True
        return "/" in pattern and fnmatch.fnmatch(rel, pattern)

    def collect_definitions(self):
        for info in self.modules:
            self.walk_containers(info, [info.tree], [])
            for function in info.functions:
                if function.is_method:
                    klass = class_by_node(info, function.container)
                    if klass is not None:
                        klass.methods[function.name] = function
            for function in sorted(info.functions, key=lambda f: f.line):
                info.contains.append((function, function.enclosing_def))
                decorated_as_fixture = has_fixture_decorator(function.node)
                if decorated_as_fixture:
                    info.local_fixtures.append(function)
                    if any(is_autouse_decorator(d) for d in function.node.decorator_list):
                        info.autouse_fixtures.append(function)
                if not info.is_test_file:
                    # Location wins: the spec calls every function outside a test
                    # file `code`, and only `code` is counted, so a fixture living
                    # outside one stays in the total. Being a fixture makes the
                    # function injectable, not a different role.
                    function.role = "code"
                elif decorated_as_fixture:
                    function.role = "fixture"
                elif self.is_test_function(info, function):
                    function.role = "test"
                else:
                    function.role = "test_support"

    def walk_containers(self, info, nodes, stack):
        for node in nodes:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, DEF_NODES):
                    self.add_function(info, child, stack)
                    self.walk_containers(info, [child], stack + [("def", child)])
                elif isinstance(child, ast.ClassDef):
                    self.add_class(info, child, stack)
                    self.walk_containers(info, [child], stack + [("class", child)])
                else:
                    self.walk_containers(info, [child], stack)

    def add_function(self, info, node, stack):
        container = stack[-1][1] if stack else None
        enclosing_def_node = None
        enclosing_class = None
        for kind, parent in reversed(stack):
            if kind == "def" and enclosing_def_node is None:
                enclosing_def_node = parent
            if kind == "class" and enclosing_class is None:
                enclosing_class = parent
        name_path = [parent.name for _, parent in stack] + [node.name]
        qualname = ".".join(name_path)
        function = FunctionInfo(
            node, info, container, enclosing_def_node, enclosing_class, qualname, name_path
        )
        info.functions.append(function)
        if container is None:
            info.module_functions[node.name] = function
        elif not isinstance(container, ast.ClassDef):
            owner = function_by_node(info, container)
            if owner is not None:
                owner.nested[node.name] = function
        return function

    def add_class(self, info, node, stack):
        enclosing_def = None
        for kind, parent in reversed(stack):
            if kind == "def":
                enclosing_def = parent
                break
        qualname = ".".join(parent.name for _, parent in stack + [("", node)])
        klass = ClassInfo(node, info, enclosing_def, qualname)
        info.classes.append(klass)
        if not stack:
            info.module_classes[node.name] = klass
        return klass

    def is_test_function(self, info, function):
        if not info.is_test_file or not function.name.startswith("test"):
            return False
        if not function.is_method:
            return True
        klass = class_by_node(info, function.container)
        return klass is not None and klass.name.startswith("Test") and not klass.enclosing_def

    def assign_ids(self):
        for info in self.modules:
            groups = defaultdict(list)
            for function in info.functions:
                groups[function.qualname].append(function)
            for qualname, group in groups.items():
                group.sort(key=lambda f: f.line)
                last = group[-1]
                for function in group:
                    path = "::".join(function.name_path)
                    if function is last:
                        function.id = f"{info.id}::{path}"
                    else:
                        function.id = f"{info.id}::{path}@{function.line}"
            self.lines[info.id] = 1
            for function in info.functions:
                self.lines[function.id] = function.line

    def add_contains_edges(self):
        for info in self.modules:
            for function in info.functions:
                parent = function.enclosing_def
                source = parent.id if parent is not None else info.id
                self.add_edge(source, function.id, "contains", function.line)

    def add_edge(self, source, target, kind, line):
        key = (source, target, kind)
        if key not in self.edges:
            self.edges[key] = line
        else:
            self.edges[key] = min(self.edges[key], line)

    def add_import_edge(self, info, target, line):
        if target != info.id:
            self.add_edge(info.id, target, "import", line)

    def module_candidates(self, base_parts, dotted):
        prefix = base_parts + [part for part in dotted.split(".") if part]
        if not prefix:
            return []
        return ["/".join(prefix) + ".py", "/".join(prefix + ["__init__.py"])]

    def find_module(self, base_parts, dotted):
        if not dotted:
            return None
        for candidate in self.module_candidates(base_parts, dotted):
            if candidate in self.by_id:
                return candidate
        return None

    def resolve_absolute_module(self, info, dotted):
        found = self.find_module(info.dir_parts(), dotted)
        if found is not None:
            return found
        return self.find_module([], dotted)

    def resolve_relative_base(self, info, level):
        parts = list(info.dir_parts())
        for _ in range(max(level - 1, 0)):
            if parts:
                parts.pop()
        return parts

    def package_base(self, module_id):
        if module_id.endswith("/__init__.py"):
            return module_id[: -len("/__init__.py")].split("/") if "/" in module_id else []
        if module_id.endswith("__init__.py") and "/" not in module_id:
            return []
        head = module_id.rsplit("/", 1)[0] if "/" in module_id else ""
        return [part for part in head.split("/") if part]

    def collect_imports(self):
        """Bind every import in the file, wherever it sits.

        `ast.walk` reaches imports inside functions and classes too, on purpose.
        The tool keeps one alias table per module, so a function-local
        `import x.y as mod` binds `mod` module-wide exactly as it does here; the
        spec binds by `import x.y as mod` and does not restrict the statement to
        module level. Only the binding, never the executing module, is recorded.
        """
        for info in self.modules:
            for node in ast.walk(info.tree):
                if isinstance(node, ast.Import):
                    self.handle_import(info, node)
                elif isinstance(node, ast.ImportFrom):
                    self.handle_import_from(info, node)

    def count_external_import(self):
        """Count one external import per statement, not per name.

        `from x import a, b` that resolves nowhere is one external import, and
        `from x import *` is one too, whatever the name it binds.
        """
        self.external_imports += 1

    def handle_import(self, info, node):
        unresolved = False
        for alias in node.names:
            bound = alias.asname or alias.name.split(".")[0]
            target = self.resolve_absolute_module(info, alias.name)
            if target is None:
                unresolved = True
                info.external_aliases.add(bound)
                continue
            info.alias_modules[bound] = target
            self.add_import_edge(info, target, node.lineno)
        if unresolved:
            self.count_external_import()

    def handle_import_from(self, info, node):
        if node.level and node.level > 0:
            base = self.resolve_relative_base(info, node.level)
            if node.module:
                module_id = self.find_module(base, node.module)
                if module_id is None:
                    self.resolve_missing_package(info, [base + node.module.split(".")], node)
                    return
                self.bind_from_names(info, module_id, self.package_base(module_id), node)
                return
            package = "/".join(base + ["__init__.py"])
            if package in self.by_id:
                self.bind_from_names(info, package, base, node)
            else:
                self.resolve_missing_package(info, [base], node)
            return
        if not node.module:
            return
        module_id = self.resolve_absolute_module(info, node.module)
        if module_id is None:
            self.resolve_missing_package(info, [info.dir_parts(), []], node)
            return
        self.bind_from_names(info, module_id, self.package_base(module_id), node)

    def resolve_missing_package(self, info, bases, node):
        """The package has no file of its own; the names may still be submodules."""
        unresolved = False
        for alias in node.names:
            bound = alias.asname or alias.name
            found = None
            for base in bases:
                found = self.find_module(base, alias.name)
                if found is not None:
                    break
            if found is None:
                unresolved = True
                info.external_aliases.add(bound)
                continue
            info.alias_modules[bound] = found
            self.add_import_edge(info, found, node.lineno)
        if unresolved:
            self.count_external_import()

    def bind_from_names(self, info, module_id, base_parts, node):
        target = self.by_id[module_id]
        is_package = module_id.rsplit("/", 1)[-1] == "__init__.py"
        for alias in node.names:
            bound = alias.asname or alias.name
            submodule = self.find_module(base_parts, alias.name) if is_package else None
            if submodule is not None:
                info.alias_modules[bound] = submodule
                self.add_import_edge(info, submodule, node.lineno)
                continue
            if alias.name in target.module_functions or alias.name in target.module_classes:
                info.from_names[bound] = (module_id, alias.name)
            self.add_import_edge(info, module_id, node.lineno)

    def collect_calls(self):
        for info in self.modules:
            self.walk_calls(info, [info.tree], None)
            for function in info.functions:
                self.walk_calls(info, function.node.body, function)

    def walk_calls(self, info, nodes, owner):
        """Record every call under `nodes`, one node per entry.

        An entry may be a statement, an expression from a decorator list, a
        default value or a keyword value, so the entry itself is checked before
        its children.
        """
        for node in nodes:
            if isinstance(node, ast.Call):
                info.calls.append((owner, node))
            if isinstance(node, DEF_NODES):
                self.walk_calls(info, node.decorator_list, owner)
                defaults = list(node.args.defaults) + [d for d in node.args.kw_defaults if d]
                self.walk_calls(info, defaults, owner)
                continue
            if isinstance(node, ast.ClassDef):
                extras = list(node.decorator_list) + list(node.bases)
                extras += [k.value for k in node.keywords]
                self.walk_calls(info, extras, owner)
                self.walk_calls(info, list(node.body), owner)
                continue
            for child in ast.iter_child_nodes(node):
                self.walk_calls(info, [child], owner)

    def collect_ctor_locals(self):
        for info in self.modules:
            for function in info.functions:
                self.record_ctor_locals(info, function.node.body, function)

    def record_ctor_locals(self, info, nodes, function):
        for node in nodes:
            if isinstance(node, DEF_NODES + (ast.ClassDef, ast.Lambda)):
                continue
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                self.bind_ctor(info, function, node.targets, node.value)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.value, ast.Call):
                self.bind_ctor(info, function, [node.target], node.value)
            self.record_ctor_locals(info, list(ast.iter_child_nodes(node)), function)

    def bind_ctor(self, info, function, targets, call):
        klass = self.resolve_class(info, function, call.func)
        if klass is None:
            return
        for target in targets:
            if isinstance(target, ast.Name):
                function.ctor_locals[target.id] = klass

    def owner_id(self, info, owner):
        return owner.id if owner is not None else info.id

    def resolve_calls(self):
        for info in self.modules:
            calls = sorted(
                info.calls, key=lambda item: (getattr(item[1], "lineno", 0), item[1].col_offset)
            )
            for owner, call in calls:
                source = self.owner_id(info, owner)
                verdict, payload = self.resolve_callee(info, owner, call.func)
                if verdict == RESOLVED:
                    self.add_edge(source, payload.id, "call", call.lineno)
                elif verdict == EXTERNAL:
                    self.external_calls += 1
                elif verdict == UNRESOLVED:
                    self.unresolved.append(
                        {
                            "from": source,
                            "line": call.lineno,
                            "text": ast.unparse(call.func)[:TEXT_LIMIT],
                            "reason": payload,
                        }
                    )

    def resolve_callee(self, info, owner, callee):
        if isinstance(callee, ast.Name):
            return self.resolve_bare_name(info, owner, callee.id)
        parts = attribute_parts(callee)
        if parts is None:
            return UNRESOLVED, "dynamic"
        root, attrs = parts
        if len(attrs) == 1:
            verdict = self.resolve_single_attribute(info, owner, root, attrs[0])
            if verdict is not None:
                return verdict
        if self.is_external_root(info, root):
            return EXTERNAL, None
        return UNRESOLVED, "attribute"

    def resolve_single_attribute(self, info, owner, head, name):
        enclosing_class = self.enclosing_class_of(info, owner)
        if head in ("self", "cls") and enclosing_class is not None and owner is not None:
            method = self.lookup_method(enclosing_class, name)
            if method is not None:
                return RESOLVED, method
        module_id = info.alias_modules.get(head)
        if module_id is not None:
            return self.resolve_member_of_module(self.by_id[module_id], name)
        if owner is not None:
            local_class = owner.ctor_locals.get(head)
            if local_class is not None:
                method = self.lookup_method(local_class, name)
                if method is not None:
                    return RESOLVED, method
        klass = self.resolve_class(info, owner, ast.Name(id=head, ctx=ast.Load()))
        if klass is not None:
            method = self.lookup_method(klass, name)
            if method is not None:
                return RESOLVED, method
        return None

    def resolve_bare_name(self, info, owner, name):
        if owner is not None:
            for scope in owner.scope_chain():
                if name in scope.nested:
                    return RESOLVED, scope.nested[name]
        if name in info.module_functions:
            return RESOLVED, info.module_functions[name]
        if name in info.module_classes:
            return self.constructor_target(info.module_classes[name])
        if name in info.from_names:
            module_id, original = info.from_names[name]
            target = self.by_id[module_id]
            if original in target.module_functions:
                return RESOLVED, target.module_functions[original]
            if original in target.module_classes:
                return self.constructor_target(target.module_classes[original])
        if name in info.external_aliases or name in BUILTIN_NAMES:
            return EXTERNAL, None
        return UNRESOLVED, "name"

    def constructor_target(self, klass):
        init = self.lookup_method(klass, "__init__")
        if init is None:
            return SILENT, None
        return RESOLVED, init

    def resolve_member_of_module(self, target, name):
        if name in target.module_functions:
            return RESOLVED, target.module_functions[name]
        if name in target.module_classes:
            return self.constructor_target(target.module_classes[name])
        return UNRESOLVED, "attribute"

    def is_external_root(self, info, name):
        return name in BUILTIN_NAMES or name in info.external_aliases

    def enclosing_class_of(self, info, owner):
        if owner is None or owner.enclosing_class is None:
            return None
        return class_by_node(info, owner.enclosing_class)

    def resolve_class(self, info, owner, expr):
        if isinstance(expr, ast.Call):
            return self.resolve_class(info, owner, expr.func)
        parts = attribute_parts(expr)
        if parts is None:
            return None
        root, attrs = parts
        if not attrs:
            return self.lookup_class_by_name(info, owner, root)
        if len(attrs) != 1:
            return None
        module_id = info.alias_modules.get(root)
        if module_id is not None:
            return self.by_id[module_id].module_classes.get(attrs[0])
        if root in info.from_names:
            module_id, original = info.from_names[root]
            return self.by_id[module_id].module_classes.get(original)
        return None

    def lookup_class_by_name(self, info, owner, name):
        if owner is not None:
            for scope in owner.scope_chain():
                if name in scope.ctor_locals:
                    return scope.ctor_locals[name]
        if name in info.module_classes:
            return info.module_classes[name]
        if name in info.from_names:
            module_id, original = info.from_names[name]
            return self.by_id[module_id].module_classes.get(original)
        return None

    def lookup_method(self, klass, name, seen=None):
        seen = set() if seen is None else seen
        if id(klass) in seen:
            return None
        seen.add(id(klass))
        method = klass.methods.get(name)
        if method is not None:
            return method
        for base in klass.bases:
            base_class = self.resolve_class(klass.module, self.scope_of(klass), base)
            if base_class is None:
                continue
            found = self.lookup_method(base_class, name, seen)
            if found is not None:
                return found
        return None

    def scope_of(self, klass):
        for function in klass.module.functions:
            if function.enclosing_class is klass.node:
                return function
        return None

    def resolve_fixtures(self):
        """Give every consuming test or fixture an edge to each fixture it gets.

        The far end is decided by the decorator, not by the role: a fixture
        declared outside a test file keeps role `code` and is still injected.
        """
        for info in self.modules:
            for function in info.functions:
                if function.role not in FIXTURE_CONSUMERS:
                    continue
                for fixture, line in self.fixtures_for(info, function):
                    self.add_edge(function.id, fixture.id, "fixture", line)

    def fixtures_for(self, info, function):
        """Return (fixture, line) pairs, `line` read in the consumer's own file.

        A parameter's line is where the injection is written; an autouse fixture
        has no parameter, so the consumer's own `def` line stands for it.
        """
        found = []
        seen = set()
        for name, line in parameters(function):
            fixture = self.lookup_fixture(info, function, name)
            if fixture is not None and id(fixture) not in seen:
                seen.add(id(fixture))
                found.append((fixture, line))
        if function.role == "test":
            for fixture in self.autouse_in_scope(info):
                if id(fixture) not in seen:
                    seen.add(id(fixture))
                    found.append((fixture, function.line))
        return found

    def lookup_fixture(self, info, function, name):
        if function.is_method:
            klass = class_by_node(info, function.container)
            if klass is not None:
                for method in klass.methods.values():
                    if has_fixture_decorator(method.node) and fixture_name_of(method) == name:
                        return method
        for fixture in info.local_fixtures:
            if fixture_name_of(fixture) == name:
                return fixture
        for conftest in self.conftests_above(info):
            for fixture in conftest.local_fixtures:
                if fixture_name_of(fixture) == name:
                    return fixture
        return None

    def conftests_above(self, info):
        found = []
        parts = info.dir_parts()
        for index in range(len(parts), -1, -1):
            rel = "/".join(parts[:index] + [CONFTEST_NAME])
            conftest = self.by_id.get(rel)
            if conftest is not None:
                found.append(conftest)
        return found

    def autouse_in_scope(self, info):
        found = list(info.autouse_fixtures)
        for conftest in self.conftests_above(info):
            prefix = conftest.rel.rsplit("/", 1)[0] if "/" in conftest.rel else ""
            if prefix and not info.rel.startswith(prefix + "/"):
                continue
            found.extend(conftest.autouse_fixtures)
        return found

    def compute_coverage(self):
        adjacency = defaultdict(list)
        for source, target, kind in self.edges:
            if kind in COVERAGE_FOLLOWS:
                adjacency[source].append(target)
        tested_by = defaultdict(set)
        for info in self.modules:
            for function in info.functions:
                if function.role != "test":
                    continue
                start = function.id
                visited = {start}
                queue = deque([start])
                while queue:
                    current = queue.popleft()
                    for neighbour in adjacency.get(current, ()):
                        if neighbour in visited:
                            continue
                        visited.add(neighbour)
                        tested_by[neighbour].add(start)
                        queue.append(neighbour)
        for info in self.modules:
            for function in info.functions:
                function.tested_by = sorted(tested_by.get(function.id, ()))
                function.tested = bool(function.tested_by)
        code = sorted(
            (f for info in self.modules for f in info.functions if f.role == "code"),
            key=lambda f: f.id,
        )
        total = len(code)
        tested = sum(1 for function in code if function.tested)
        return {
            "rule": "transitive",
            "follows": list(COVERAGE_FOLLOWS),
            "tested": tested,
            "total": total,
            "ratio": round(tested / total, 4) if total else None,
            "untested": [function.id for function in code if not function.tested],
        }

    def render(self):
        coverage = self.compute_coverage()
        nodes = []
        for info in self.modules:
            nodes.append(
                {
                    "id": info.id,
                    "kind": "module",
                    "file": info.rel,
                    "line": 1,
                    "end_line": info.line_count,
                    "is_test_file": info.is_test_file,
                }
            )
            for function in info.functions:
                nodes.append(
                    {
                        "id": function.id,
                        "kind": "function",
                        "file": info.rel,
                        "line": function.line,
                        "end_line": function.end_line,
                        "is_test_file": info.is_test_file,
                        "name": function.name,
                        "qualname": function.qualname,
                        "module": info.id,
                        "role": function.role,
                        "decorators": function.decorators,
                        "tested": function.tested,
                        "tested_by": function.tested_by,
                    }
                )
        nodes.sort(key=lambda node: node["id"])
        edges = [
            {"from": source, "to": target, "kind": kind, "line": line}
            for (source, target, kind), line in self.edges.items()
        ]
        edges.sort(key=lambda edge: (edge["from"], edge["to"], edge["kind"]))
        unresolved = sorted(
            self.unresolved, key=lambda item: (item["from"], item["line"], item["text"])
        )
        edge_counts = {kind: 0 for kind in EDGE_KINDS}
        for edge in edges:
            edge_counts[edge["kind"]] += 1
        unresolved_counts = {reason: 0 for reason in UNRESOLVED_REASONS}
        for item in unresolved:
            unresolved_counts[item["reason"]] += 1
        functions = [f for info in self.modules for f in info.functions]
        return {
            "schema": SCHEMA,
            "tier": TIER,
            "root": self.root_arg,
            "nodes": nodes,
            "edges": edges,
            "unresolved_calls": unresolved,
            "coverage": coverage,
            "stats": {
                "files": self.files_seen,
                "modules": len(self.modules),
                "functions": len(functions),
                "tests": sum(1 for f in functions if f.role == "test"),
                "fixtures": sum(1 for f in functions if f.role == "fixture"),
                "edges": edge_counts,
                "unresolved": unresolved_counts,
                "external_calls": self.external_calls,
                "external_imports": self.external_imports,
            },
            "errors": self.errors,
        }


def build_parser():
    parser = argparse.ArgumentParser(
        prog="code_graph.py",
        description="Build a static code graph from Python sources (stdlib ast only).",
    )
    parser.add_argument("root", nargs="?", default=".", help="directory to scan (default: .)")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        help="fnmatch pattern matched against each file's path relative to ROOT; repeatable",
    )
    parser.add_argument(
        "--test-glob",
        action="append",
        default=None,
        metavar="GLOB",
        help="test file pattern; the first use replaces the defaults; repeatable",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    test_globs = list(args.test_glob) if args.test_glob else list(DEFAULT_TEST_GLOBS)
    builder = GraphBuilder(args.root, args.exclude, test_globs)
    try:
        payload = builder.run()
    except UsageError as exc:
        print(f"code_graph.py: {exc}", file=sys.stderr)
        return 2
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 1 if payload["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())