# E2 — round 2 (commit 2c1af3d)

```
{
 "bash_calls": 3677,
 "crude_engine_like": 284,
 "recognized": 161,
 "crude_but_not_recognized": 123,
 "recognized_but_not_crude": 0,
 "recognized_with_output_file": 123,
 "byEngine": {
  "four-experts": 63,
  "codex": 50,
  "dsh": 3,
  "opencode": 24,
  "agy": 14,
  "claude": 7
 },
 "denies": 14,
 "byTrap": {
  "trap:codex-stdin": 6,
  "trap:opencode-parallel": 10
 }
}
```

Denies 14, the same 14 real ones as round 1 (6 codex-stdin, 8 distinct opencode-parallel starts; 0 false). Recognised calls 158 → 161: the 3 `for … do timeout N opencode run` calls are now recognised (C19). Remaining crude-but-not-recognised (123) are heredoc/quoted text, `--help` calls, grep/pgrep/echo text and 2 `dispatch.py run` calls (not in scope) — the same categories as round 1.
