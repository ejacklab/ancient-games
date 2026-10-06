"""Regression suite for `code_graph.py`, the stdlib-ast call graph.

Each test writes a tiny project into `tmp_path`, runs the tool as a subprocess,
and asserts on the JSON it prints. Nothing here re-derives the graph: the tool is
the only source of truth, so a regression in the tool fails the test that covers it.

The cases and their expected results come from
`runs/20261005-code-graph-tool/nodes/n4-test-cases-1.result.md`:
`direct_call`, `imported_call`, `class_method` and `nested_function` must produce
a call edge; `call_through_variable`, `getattr_call`, `decorator_wrapper` and
`lambda_call` must record what the tool can and cannot see, and must not invent
an edge it cannot justify.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parent.parent / "code_graph.py"


def run_tool(tmp_path, files):
    """Write `files` ({relative path: source}) under tmp_path and return the tool's JSON."""
    for rel, source in files.items():
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"tool exited {proc.returncode}: {proc.stderr}"
    payload = json.loads(proc.stdout)
    assert payload["errors"] == [], f"tool reported parse errors: {payload['errors']}"
    return payload


def node_ids(payload):
    return {n["id"] for n in payload["nodes"]}


def function_names(payload):
    return {n["id"]: n["name"] for n in payload["nodes"] if n["kind"] == "function"}


def edges_of_kind(payload, kind):
    return {(e["from"], e["to"]) for e in payload["edges"] if e["kind"] == kind}


def call_edges(payload):
    return edges_of_kind(payload, "call")


def contains_edges(payload):
    return edges_of_kind(payload, "contains")


def import_edges(payload):
    return edges_of_kind(payload, "import")


def decorator_texts(payload, node_id):
    for n in payload["nodes"]:
        if n["id"] == node_id:
            return n["decorators"]
    raise AssertionError(f"no node {node_id} in {node_ids(payload)}")


def unresolved_from(payload, source):
    return [u for u in payload["unresolved_calls"] if u["from"] == source]


def unresolved_reasons(payload, source):
    return [u["reason"] for u in unresolved_from(payload, source)]


def unresolved_texts(payload, source):
    return [u["text"] for u in unresolved_from(payload, source)]


# --------------------------------------------------------------------------
# Positive cases: a call edge the tool must find.
# --------------------------------------------------------------------------


def test_direct_call_links_caller_to_local_function(tmp_path):
    payload = run_tool(tmp_path, {"mod.py": "def b():\n    pass\n\n\ndef a():\n    b()\n"})
    assert ("mod.py::a", "mod.py::b") in call_edges(payload)
    assert unresolved_from(payload, "mod.py::a") == []
    assert payload["stats"]["external_calls"] == 0


def test_imported_call_links_caller_to_imported_function(tmp_path):
    payload = run_tool(
        tmp_path,
        {
            "callee.py": "def b():\n    pass\n",
            "caller.py": "from callee import b\n\n\ndef a():\n    b()\n",
        },
    )
    assert ("caller.py", "callee.py") in import_edges(payload)
    assert ("caller.py::a", "callee.py::b") in call_edges(payload)
    assert unresolved_from(payload, "caller.py::a") == []


def test_class_method_call_links_methods_of_one_class(tmp_path):
    payload = run_tool(
        tmp_path,
        {
            "mod.py": "class C:\n"
            "    def b(self):\n        pass\n\n"
            "    def a(self):\n        self.b()\n"
        },
    )
    assert {"mod.py::C::a", "mod.py::C::b"} <= node_ids(payload)
    assert ("mod.py::C::a", "mod.py::C::b") in call_edges(payload)
    assert unresolved_from(payload, "mod.py::C::a") == []


def test_nested_function_gets_node_and_call_edge(tmp_path):
    payload = run_tool(
        tmp_path,
        {"mod.py": "def outer():\n    def inner():\n        pass\n    inner()\n"},
    )
    assert "mod.py::outer::inner" in node_ids(payload)
    assert function_names(payload)["mod.py::outer::inner"] == "inner"
    assert ("mod.py::outer", "mod.py::outer::inner") in contains_edges(payload)
    assert ("mod.py::outer", "mod.py::outer::inner") in call_edges(payload)


# --------------------------------------------------------------------------
# Negative cases: what the tool must not claim, and what it must report instead.
# --------------------------------------------------------------------------


def test_call_through_variable_is_not_resolved_and_marked_name(tmp_path):
    payload = run_tool(
        tmp_path,
        {"mod.py": "def b():\n    pass\n\n\ndef a():\n    f = b\n    f()\n"},
    )
    assert ("mod.py::a", "mod.py::b") not in call_edges(payload)
    assert call_edges(payload) == set()
    assert unresolved_reasons(payload, "mod.py::a") == ["name"]
    assert unresolved_texts(payload, "mod.py::a") == ["f"]


def test_getattr_call_is_dynamic_and_counts_getattr_external(tmp_path):
    payload = run_tool(
        tmp_path,
        {
            "mod.py": "class C:\n"
            "    def b(self):\n        pass\n\n\n"
            "def a(obj):\n    getattr(obj, 'b')()\n"
        },
    )
    assert call_edges(payload) == set()
    assert ("mod.py::a", "mod.py::C::b") not in call_edges(payload)
    assert unresolved_reasons(payload, "mod.py::a") == ["dynamic"]
    assert payload["stats"]["external_calls"] == 1


def test_decorator_wrapper_records_decorator_and_keeps_static_edge(tmp_path):
    payload = run_tool(
        tmp_path,
        {
            "mod.py": "def deco(fn):\n"
            "    def wrapper(*args):\n        return fn(*args)\n"
            "    return wrapper\n\n\n"
            "@deco\ndef b():\n    pass\n\n\n"
            "def a():\n    b()\n"
        },
    )
    assert decorator_texts(payload, "mod.py::b") == ["deco"]
    assert ("mod.py::a", "mod.py::b") in call_edges(payload)
    assert ("mod.py::a", "mod.py::deco::wrapper") not in call_edges(payload)


def test_lambda_call_attributes_explicit_body_call_to_enclosing_function(tmp_path):
    payload = run_tool(
        tmp_path,
        {
            "mod.py": "def b():\n"
            "    pass\n\n\n"
            "def a():\n    f = lambda: b()\n    f()\n"
        },
    )
    assert not any("lambda" in name for name in function_names(payload).values())
    assert "mod.py::lambda" not in node_ids(payload)
    assert ("mod.py::a", "mod.py::b") in call_edges(payload)
    assert unresolved_reasons(payload, "mod.py::a") == ["name"]
    assert unresolved_texts(payload, "mod.py::a") == ["f"]