---
node: n4-test-cases
attempt: 1
engine: codex
model: gpt-6.1-sol
status: ok
started: 2026-10-06T09:12:52.469Z
ended: 2026-10-06T09:13:27.319Z
evidence: none
---
## Cases
- direct_call — positive — `a()` calls local `b()` — call edge `a -> b` present.
- imported_call — positive — `a()` calls `b()` imported from a file under ROOT — import edge and call edge to that file’s `b` present.
- class_method — positive — `C.a(self)` calls `self.b()` — call edge `C::a -> C::b` present.
- nested_function — positive — `outer()` defines and calls `inner()` — nested function node, contains edge, and call edge `outer -> outer::inner` present.
- call_through_variable — negative — `a()` assigns `f = b` then calls `f()` — no call edge to `b`; `f` recorded unresolved with reason `name`.
- getattr_call — negative — `a()` calls `getattr(obj, "b")()` — no inferred method edge; outer call unresolved as `dynamic`; builtin `getattr` counted as external.
- decorator_wrapper — negative — `@deco` replaces `b` with a nested wrapper; `a()` calls `b()` — decorator text recorded and static `a -> b` edge present; no inferred edge from `a` to the replacement wrapper.
- lambda_call — negative — `a()` assigns `f = lambda: b()` then calls `f()` — no lambda node; `f` unresolved as `name`; explicit lambda-body call attributed to `a`, producing `a -> b`.
## Coverage
8 of ~8 expected cases covered = 100%
