"""NEW — `run_suite(command) -> {passed, failed, output, returncode}`; ok=True whenever
the command ran (a red suite is a result, not a failure of the tool)."""
import re
import subprocess

from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "run_suite", "inputs": {"command": "str"}, "outputs": "{passed, failed, output, returncode}",
    "side_effects": "none", "cost": "suite", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        p = subprocess.run(args["command"], shell=True, cwd=env.cwd, capture_output=True, text=True, timeout=600)
        output = p.stdout + p.stderr
        passed = re.search(r"(\d+) passed", output)
        failed = re.search(r"(\d+) failed", output)
        errors = re.search(r"(\d+) error", output)
        return ToolResult(ok=True, value={"passed": int(passed.group(1)) if passed else 0,
                                          "failed": (int(failed.group(1)) if failed else 0) + (int(errors.group(1)) if errors else 0),
                                          "output": output, "returncode": p.returncode})
    except Exception as e:
        return internal_error(e)
