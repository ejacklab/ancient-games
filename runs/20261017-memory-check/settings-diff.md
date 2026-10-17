# The settings change for EJ: the memory-check warning at session start (R2, U3)

R12.3: applied only after the owner's yes to this exact diff. File: `~/.claude/settings.json`, `hooks.SessionStart`.
The guard's existing entry stays; one entry is added after it. Changed after the enhance round
(`enhance-q/compare.md`): it speaks only in projects that have `project-memory/` (no line in every project without
`AGENTS.md`), and says when the tool itself did not finish.

```diff
   "SessionStart": [
     {
       "hooks": [
         {
           "type": "command",
           "command": "bun /home/smoke01/dev/ancient-games/.claude/skills/workflow-design/guard/src/cli.ts hook claude",
           "timeout": 15
         }
       ]
-    }
+    },
+    {
+      "hooks": [
+        {
+          "type": "command",
+          "command": "r=$(git rev-parse --show-toplevel 2>/dev/null) && [ -d \"$r/project-memory\" ] || exit 0; bun /home/smoke01/dev/ancient-games/memory_check/src/cli.ts --project \"$r\" --warn 2>/dev/null; s=$?; [ \"$s\" -gt 1 ] && echo \"memory-check: did not finish (exit $s)\"; exit 0",
+          "timeout": 20
+        }
+      ]
+    }
   ]
```

Tried by hand (`hook-try.sh` in the job's scratch folder, 19:1x): this repo (no `project-memory/`), a plain folder and
a git repo without `project-memory/` print nothing (exit 0); a git repo with `project-memory/` and no `AGENTS.md`
prints `memory-check: AGENTS.md is missing — file: …/AGENTS.md (it is required, F1)` (exit 0). It never fails the
session start; its output becomes session context in Claude Code. The method does not depend on it (3.1 runs the tool
itself).

Yes recorded: EJ, 2026-10-17 — "yes to the hook settings". Applied by the agent: one SessionStart entry added to ~/.claude/settings.json (9 lines added, nothing else changed; backup ~/.claude/settings.json.bak-20261017-memory-check); the saved command run from the JSON prints the AGENTS.md line in a fixture with project-memory/ and nothing in this repo, exit 0 both.
