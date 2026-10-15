Your two CONTRADICTS are resolved in SPEC.md M5 (re-read `src/doctor.ts` and `src/plugins/opencode.ts`): `doctor`
now takes `DoctorOptions = { home, projectRoot, healthScript?, run? }` and the files it reads are listed; the plugin's
default export `HarnessGuardPlugin(ctx: { directory })` returns `{ "tool.execute.before": (input, output) => … }`.

Add the pending tests in **`test/doctor.test.ts`** (new file) and **`test/plugin.test.ts`** (new file), from SPEC.md
alone, with temporary `home`/`projectRoot` folders and a fake `run`: installed / absent / unknown per harness (a hook
command containing `harness-guard`; a settings file without it; an unreadable or unparseable file); `answers` true from
the planted trap; `health` from a fake `run` (exit 0 with `{"findings":[…]}` → ok and `"<n> findings"`; non-zero, or
output that is not JSON → not ok; the script's text never appears in the report — plant `SECRET-PLANT-7f3a9c` in the
fake output and in a settings value). Plugin: a bash `codex exec` without a redirect throws with the trap id in the
message; a clean command and a non-bash tool do not throw.

The implementation is being written now by a different engine; do not read or change `src/`. Change nothing else.
