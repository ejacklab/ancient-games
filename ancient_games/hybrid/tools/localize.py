"""NEW — `localize(suite_output) -> {test_id, file, line, error_type}` by regex over pytest output."""
import re

from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "localize", "inputs": {"suite_output": "str"}, "outputs": "{test_id, file, line, error_type}",
    "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}

# Harnesses set FORCE_COLOR/PY_COLORS, so a captured pytest run arrives with SGR escapes and
# every ^-anchored pattern below misses (UC7 went red-then-green correctly while localize
# reported "no failure located"). Strip them before matching.
_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_FAILED = re.compile(r"^(?:FAILED|ERROR) (\S+?)(?: - (.*))?$", re.M)
_FRAME = re.compile(r"^([\w./-]+\.py):(\d+): ", re.M)
_ERR = re.compile(r"^E\s+(\w+(?:Error|Exception|Failed)\b)", re.M)


def run(env, args):
    try:
        out = args.get("suite_output") or ""
        out = _ANSI.sub("", out)
        failed = _FAILED.search(out)
        frames = _FRAME.findall(out)
        err = _ERR.search(out)
        if not failed and not frames:
            return ToolResult(ok=False, reason="no failure located in suite output")
        error_type = err.group(1) if err else None
        if error_type is None and failed and failed.group(2):
            m = re.match(r"(\w+)", failed.group(2))
            error_type = m.group(1) if m else None
        file, line = (frames[-1][0], int(frames[-1][1])) if frames else (None, None)
        return ToolResult(ok=True, value={"test_id": failed.group(1) if failed else None, "file": file, "line": line,
                                          "error_type": error_type})
    except Exception as e:
        return internal_error(e)
