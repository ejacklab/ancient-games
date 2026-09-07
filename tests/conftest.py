import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))  # `import cases`

# The whole suite runs the §8 lints in `differential` mode (docs/STORE_DESIGN_DECISION.md §Tests): every
# case test exercises both the Python oracle and the SQL backend, and any disagreement fails the test with
# `lints.LintBackendDivergence`. Set at import so CLI subprocesses inherit it too. Tests that need another
# backend pass `backend=` explicitly or `monkeypatch.delenv("AG_LINT_BACKEND")`.
os.environ["AG_LINT_BACKEND"] = "differential"
