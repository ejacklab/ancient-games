#!/usr/bin/env bash
# Full test-suite wall time (3 runs) and per-test coverage contexts, as independent gold for test-impact questions.
# Writes only under this run folder (COVERAGE_FILE, -p no:cacheprovider).
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-caches-routing
cd /home/smoke01/dev/ancient-games
for i in 1 2 3; do
  s=$(date +%s.%N); env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider > "$R/cov/suite-run-$i.txt" 2>&1; rc=$?
  e=$(date +%s.%N); echo "run=$i exit=$rc seconds=$(echo "$e - $s" | bc)" >> "$R/cov/suite-timing.txt"
done
export COVERAGE_FILE="$R/cov/.coverage"
env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider --cov=. --cov-context=test --cov-report= > "$R/cov/coverage-run.txt" 2>&1
echo "coverage exit=$?" >> "$R/cov/suite-timing.txt"
python3 -m coverage json --show-contexts -o "$R/cov/coverage-contexts.json" >> "$R/cov/coverage-run.txt" 2>&1
echo "json exit=$?" >> "$R/cov/suite-timing.txt"
