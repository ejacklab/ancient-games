# The settings change for EJ (R12.3: applied only after the owner's yes to this exact diff)

File: `~/.claude/settings.json`, `hooks.PreToolUse[0]` (the harness-guard entry). Nothing else changes.

```diff
   "PreToolUse": [
     {
-      "matcher": "Bash",
+      "matcher": "Bash|Write|Edit|MultiEdit",
       "hooks": [
         {
           "type": "command",
           "command": "bun /home/smoke01/dev/ancient-games/.claude/skills/workflow-design/guard/src/cli.ts hook claude",
           "timeout": 15
         }
       ]
     }
   ]
```

Why: the guard gives the lessons for a file just before a Write or Edit to it (guard SPEC Round 18, L5–L6). Today it
sees only Bash before a call, so file lessons and project facts never reach the main agent.

The same matcher belongs in the installer (`guard/src/install.ts`, EVENTS) so `install --print` prints it — the
crossed review's finding 1. That edit was denied by the auto-mode classifier as self-modification and is not made.

Yes recorded: EJ, 2026-10-17 15:28 — "yes to settings, all follow your picks". Applied by the agent: line 33 of ~/.claude/settings.json, one line changed (diff of the backup ~/.claude/settings.json.bak-20261017-agent-lessons: 1 removed, 1 added), JSON valid. Live at once: the next Edit was held with a lesson. The installer edit (install.ts) then went through and `install --print` prints the same matcher.
