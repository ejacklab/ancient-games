---
node: n1-readiness
attempt: 4
engine: claude
model: claude-opus-5-5
status: partial
started: 2026-10-09T12:58:00.124Z
ended: 2026-10-09T12:58:48.433Z
evidence: none
---
## Root cause
The sandbox fixture built HOME from pytest's `tmp_path`. pytest's basetemp is now under `/home/smoke01`, so `sandbox.home` contains the real home. rt_01's check that the real home is absent (line 120) then conflicts with its own checks that the proof column holds the absolute `sandbox.home` paths (lines 128–140). This is the cause decided on 2026-10-09. I have not seen it in a test run myself.
## Fix
readiness.py is unchanged. All changes are in `tests/test_readiness.py`, in the `sandbox` fixture (lines 31–75):
- The sandbox root is now `Path(tempfile.mkdtemp(dir="/tmp"))` instead of pytest's `tmp_path`. So `sandbox.home` is `/tmp/...` and overlaps neither the real home nor the repo root.
- The fixture now `yield`s the namespace and then removes the sandbox with `shutil.rmtree(..., ignore_errors=True)`.
- Added `import shutil` and `import tempfile`, plus a one-line comment explaining why the sandbox is under `/tmp`.
- Nothing else changed: no test and no probe.
## Verified
Not verified, neither red before nor green after. Every Python and git command needed approval in this session and was blocked:
- `env -u NO_COLOR /usr/bin/python3 -m pytest tests/test_readiness.py -q`
- `python3 -m pytest … -p no:cacheprovider`
- `python3 -m py_compile tests/test_readiness.py`
- `git diff`

The only check was rereading the edited file (lines 1–76). The imports are present, the fixture is a valid generator fixture, and no other test in the file uses `tmp_path`, so the other tests get the same sandbox through the same fixture.

To verify, run: `env -u NO_COLOR /usr/bin/python3 -m pytest tests/test_readiness.py -q`

Two lines of the brief contradict its Decided paragraph:
- The Template line "Fix: what changed in readiness.py".
- The Standard line "Only `readiness.py` changes".

I followed the Decided paragraph, which says the test-fixture fix replaces the readiness.py-only rule. So readiness.py is untouched and only the test file changed. The Standard needs updating to match.

UNCLEAR: Can pytest be allowed for this node, or can someone run the command above and attach the output to `runs/20261009-fix-tests/` as evidence? / Best guess: rt_01 passes and the other RT tests do not regress, because none of them depend on where the sandbox is created.
