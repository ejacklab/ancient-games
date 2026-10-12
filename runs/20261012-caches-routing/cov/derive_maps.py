"""Reduce coverage-contexts.json (per-test line contexts) to two maps used as independent gold:
file -> test files that execute it, and path::function -> test files that execute any of its lines.
Coverage sees in-process Python only (a test that runs code in a subprocess leaves no context)."""
import ast, json, sys, collections, os
REPO = '/home/smoke01/dev/ancient-games'
d = json.load(open(sys.argv[1]))
file_tests = collections.defaultdict(set); func_tests = collections.defaultdict(set)
for path, v in d['files'].items():
    rel = os.path.relpath(os.path.join(REPO, path), REPO) if not path.startswith('/') else os.path.relpath(path, REPO)
    spans = []
    try:
        tree = ast.parse(open(os.path.join(REPO, rel)).read())
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                spans.append((n.lineno, n.end_lineno, n.name))
            if isinstance(n, ast.ClassDef):
                for m in n.body:
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        spans.append((m.lineno, m.end_lineno, f'{n.name}.{m.name}'))
    except Exception:
        pass
    for ln, ctxs in v.get('contexts', {}).items():
        tests = {c.split('::')[0] for c in ctxs if '::' in c}
        if not tests: continue
        file_tests[rel] |= tests
        ln = int(ln)
        for a, b, name in spans:
            if a <= ln <= b:
                func_tests[f'{rel}::{name}'] |= tests
out = {'note': 'derived from pytest-cov --cov-context=test, 2026-10-12; in-process Python only',
       'file_tests': {k: sorted(v) for k, v in sorted(file_tests.items())},
       'func_tests': {k: sorted(v) for k, v in sorted(func_tests.items())}}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print('files', len(out['file_tests']), 'functions', len(out['func_tests']))
