import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import HarnessGuardPlugin from "../src/plugins/opencode.ts";

const secret = "SECRET-PLANT-7f3a9c";
let folder: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

describe("opencode plugin", () => {
  test("plugin: bash codex exec without a stdin redirect throws with the trap id", async () => {
    const plugin = await HarnessGuardPlugin({ directory: folder });
    await expect(plugin["tool.execute.before"]({ tool: "bash" }, { args: { command: "codex exec task" } })).rejects.toThrow("trap:codex-stdin");
  });

  test.each(["echo clean", "codex exec task </dev/null", "codex exec --help", "opencode run task"])(
    "plugin: clean bash command %s does not throw",
    async (command: string) => {
      const plugin = await HarnessGuardPlugin({ directory: folder });
      await plugin["tool.execute.before"]({ tool: "bash" }, { args: { command } });
    },
  );

  test("plugin: a non-bash tool does not lint a command-shaped argument", async () => {
    const plugin = await HarnessGuardPlugin({ directory: folder });
    await plugin["tool.execute.before"]({ tool: "read" }, { args: { command: "codex exec task" } });
  });

  test("plugin: paths are checked against the git root of the supplied directory", async () => {
    execFileSync("git", ["init", "--quiet", folder], { cwd: folder });
    const nested = path.join(folder, "nested");
    fs.mkdirSync(nested);
    const plugin = await HarnessGuardPlugin({ directory: nested });
    await plugin["tool.execute.before"]({ tool: "bash" }, { args: { command: `opencode run ${path.join(folder, "input.md")}` } });
    const outside = path.join(path.dirname(folder), "outside-hg-repo.md");
    await expect(plugin["tool.execute.before"]({ tool: "bash" }, { args: { command: `opencode run ${outside}` } })).rejects.toThrow("trap:opencode-outside-repo");
  });

  test("plugin: a denied prompt is absent from the error and guard state", async () => {
    const plugin = await HarnessGuardPlugin({ directory: folder });
    let caught: unknown;
    try {
      await plugin["tool.execute.before"]({ tool: "bash" }, { args: { command: `codex exec '${secret}'` } });
    } catch (error) { caught = error; }
    expect(caught).toBeInstanceOf(Error);
    expect(String(caught)).toContain("trap:codex-stdin");
    expect(String(caught)).not.toContain(secret);
    const state = path.join(folder, ".harness-guard");
    if (fs.existsSync(state)) {
      for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
        const file = path.join(state, name);
        expect(name).not.toContain(secret);
        if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
      }
    }
  });
});
