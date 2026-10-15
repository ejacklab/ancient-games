// M5: the opencode adapter (SPEC.md M5). opencode calls the hook before a tool runs; a finding is reported by
// throwing. Blocking by throwing is what opencode's docs report, not something verified here.

import { guardRoot } from "../journal.ts";
import { lintCommand } from "../traps.ts";

interface PluginInput {
  tool: string;
}

interface PluginOutput {
  args: { command?: string };
}

const BASH = "bash";

const HarnessGuardPlugin = (ctx: { directory: string }): Promise<{
  "tool.execute.before": (input: PluginInput, output: PluginOutput) => Promise<void>;
}> =>
  Promise.resolve({
    "tool.execute.before": async (input, output) => {
      if (input?.tool !== BASH) return;
      const command = output?.args?.command;
      if (typeof command !== "string" || command === "") return;
      const findings = lintCommand(command, { repoRoot: guardRoot(ctx.directory), running: [] })
        .filter((finding) => finding.severity === "fail");
      if (findings.length === 0) return;
      throw new Error(`harness-guard blocked this command: ${findings.map((finding) => `${finding.rule}: ${finding.message} Fix: ${finding.fix ?? "see the rule"}`).join("; ")}`);
    },
  });

export default HarnessGuardPlugin;