#!/usr/bin/env bash
# Commit only the verifier's cases, so the gate's tamper check can see the dev change them later.
set -e
git add tests/test_dispatch_workdir.py
git commit -q -m "Run 20261003-node-workdir: verifier's blind cases (checkpoint before the gate)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git rev-parse --short HEAD > runs/20261003-node-workdir/checkpoint.ref
echo "checkpoint $(cat runs/20261003-node-workdir/checkpoint.ref)"
