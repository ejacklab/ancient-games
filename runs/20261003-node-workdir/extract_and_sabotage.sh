#!/usr/bin/env bash
# Check of the `sabotage` node: write the verifier's latest cases to tests/test_dispatch_workdir.py, then prove they
# FAIL against the old dispatcher (db1fad2). Exit 0 only when they fail there (pytest exit 1).
set -u
R=runs/20261003-node-workdir
latest=$(ls -t $R/nodes/cases-*.result.md 2>/dev/null | head -1)
[ -n "$latest" ] || { echo "no cases result"; exit 1; }
python3 - "$latest" <<'PY' || exit 1
import re, sys, pathlib
t = pathlib.Path(sys.argv[1]).read_text()
m = re.search(r"```python\n(.*?)```", t, re.S)
if not m:
    print("no python block in the cases result"); sys.exit(1)
code = m.group(1)
if "DISPATCH_SCRIPT" not in code:
    print("cases do not read DISPATCH_SCRIPT"); sys.exit(1)
pathlib.Path("tests/test_dispatch_workdir.py").write_text(code)
print("cases written:", len(re.findall(r"^def test_r\d", code, re.M)), "tests")
PY
old=$(mktemp -d)
for f in dispatch.py runlog.py validate_result.py; do git show db1fad2:.claude/skills/workflow-design/scripts/$f > $old/$f; done
DISPATCH_SCRIPT=$old/dispatch.py env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider tests/test_dispatch_workdir.py > $R/sabotage.out 2>&1
code=$?
tail -3 $R/sabotage.out
if [ $code -eq 1 ]; then echo "SABOTAGE OK: the cases fail on the old dispatcher"; exit 0; fi
echo "SABOTAGE FAILED: pytest exit $code on the old dispatcher (want 1: tests ran and failed)"; exit 1
