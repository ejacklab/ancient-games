import importlib.util, json, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
run = Path(tempfile.mkdtemp()) / "run"
(run / "workspace/product").mkdir(parents=True)
(run / "workspace/product/calc.py").write_text("def add(a, b):\n    return a + b\n")
(run / "probes").mkdir()
(run / "probes/test_env.py").write_text(
    "import os\n\ndef test_env():\n    '''X1-F1 — env'''\n"
    "    open(os.path.join(os.environ['EVAL_PRODUCT'], '..', 'seen.json'), 'w').write("
    "__import__('json').dumps([os.environ['HOME'], os.environ['TMPDIR']]))\n")
spec = importlib.util.spec_from_file_location("pm", ROOT / "tools/evaluator/probe_matrix.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(json.dumps(m.build_matrix(run, timeout=30))[:600])
print((run / "workspace/seen.json").exists())
