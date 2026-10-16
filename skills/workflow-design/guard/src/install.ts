// M5: install advice (SPEC.md M5). Prints a snippet and nothing else: no file is read, no file is written, so no
// config value and no secret can pass through here.

export type Harness = "claude-code" | "codex" | "qwen" | "opencode";

export const HARNESSES: readonly Harness[] = ["claude-code", "codex", "qwen", "opencode"];

const GITIGNORE = "Add .harness-guard/ to the repository .gitignore: the guard's journal and evidence are yours, not the project's.";

// Where each harness reads its hook settings from, and how far that is verified.
const SETTINGS: Record<Exclude<Harness, "opencode">, { file: string; reported: boolean }> = {
  "claude-code": { file: "~/.claude/settings.json", reported: false },
  codex: { file: "~/.codex/hooks.json", reported: true },
  qwen: { file: "~/.qwen/settings.json", reported: true },
};

function hookCommand(guardDir: string): { type: "command"; command: string } {
  return { type: "command", command: `bun ${guardDir}/src/cli.ts hook claude` };
}

function entry(matcher: string | null, guardDir: string): Record<string, unknown> {
  const hooks = [hookCommand(guardDir)];
  return matcher === null ? { hooks } : { matcher, hooks };
}

// The event list the handler dispatches on, with the tools each event watches.
const EVENTS: [string, string | null][] = [
  ["PreToolUse", "Bash"],
  // Round 10: every tool, so the clock reaches Read, Grep and web calls too; the older checks filter by tool inside.
  ["PostToolUse", null],
  ["PostToolUseFailure", null],
  ["Stop", null],
  ["SubagentStop", null],
  ["SessionStart", null],
  ["UserPromptSubmit", null],
];

function settingsSnippet(harness: Exclude<Harness, "opencode">, guardDir: string): string {
  const where = SETTINGS[harness];
  const lines = [`# Merge this into ${where.file} (keep the rest of the file). ${GITIGNORE}`];
  if (where.reported) {
    lines.push(`# The event names and matchers below are reported from this harness's documentation, not verified here.`);
  }
  const hooks: Record<string, unknown[]> = {};
  for (const [event, matcher] of EVENTS) hooks[event] = [entry(matcher, guardDir)];
  return [...lines, "", JSON.stringify({ hooks }, null, 2)].join("\n");
}

// opencode loads a plugin file by path, so the advice is the one-line file itself, importing the adapter by absolute
// path (round 3, C15): a copy in a plugins folder outside the package still resolves and still blocks a trap.
function opencodeSnippet(guardDir: string): string {
  return [
    `# Save the one line below as harness-guard.ts in a plugins folder opencode loads, e.g.`,
    `#   ~/.config/opencode/plugins/harness-guard.ts`,
    `# or your own project's .opencode/plugin/harness-guard.ts. ${GITIGNORE}`,
    "# opencode blocks a command by an exception from the plugin hook, as its docs report.",
    `export { default } from "${guardDir}/src/plugins/opencode.ts";`,
  ].join("\n");
}

export function installSnippet(harness: Harness, guardDir: string): string {
  return harness === "opencode" ? opencodeSnippet(guardDir) : settingsSnippet(harness, guardDir);
}