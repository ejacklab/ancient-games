#!/usr/bin/env bash
# Check of the `gate` node: the full suite per test, then feature_gate.py against the baseline; the diff for review.
set -u
R=runs/20261003-node-workdir
env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider --junitxml=$R/now.xml > $R/suite.out 2>&1
tail -1 $R/suite.out
python3 .claude/skills/workflow-design/scripts/feature_gate.py check --plan $R/gate-plan.json \
  --base-ref "$(cat $R/checkpoint.ref)" --baseline $R/baseline/baseline.json --junit $R/now.xml
code=$?
git diff db1fad2 -- .claude/skills/workflow-design/scripts/dispatch.py tests/test_dispatch.py > $R/diff.patch
exit $code
