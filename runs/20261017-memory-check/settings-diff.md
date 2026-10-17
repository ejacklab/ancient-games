# The settings change for EJ: the memory-check warning at session start (R2, U3)

R12.3: applied only after the owner's yes to this exact diff. File: `~/.claude/settings.json`, `hooks.SessionStart`.
The guard's existing entry stays; one entry is added after it.

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
+          "command": "bun /home/smoke01/dev/ancient-games/memory_check/src/cli.ts --project \"$(git rev-parse --show-toplevel 2>/dev/null || pwd)\" --warn 2>/dev/null || true",
+          "timeout": 20
+        }
+      ]
+    }
   ]
```

Tried by hand (18:5x): in this repo it prints nothing (exit 0); outside a git repo nothing (exit 0); in a git repo with
no `AGENTS.md` one line, `memory-check: AGENTS.md is missing — file: …/AGENTS.md (it is required, F1)` (exit 0). It
never fails the session start. Its output becomes session context in Claude Code.

What you will see: in every git project of yours without an `AGENTS.md`, that one line at each session start; any
failing MUST of a project that has `project-memory/`.

Yes recorded: (not yet)
