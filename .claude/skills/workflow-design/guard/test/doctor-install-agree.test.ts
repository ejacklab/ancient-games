// Written by the COO after the live install (run 20261015-ts-hybrid): doctor must recognise the command install prints.
import { expect, test } from "bun:test";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { doctor } from "../src/doctor.ts";
import { installSnippet } from "../src/install.ts";

test("doctor: the command install --print gives counts as installed for claude-code", () => {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  const projectRoot = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  const snippet = installSnippet("claude-code", "/opt/skills/workflow-design/guard");
  const json = snippet.slice(snippet.indexOf("{"));
  fs.mkdirSync(path.join(home, ".claude"));
  fs.writeFileSync(path.join(home, ".claude", "settings.json"), json);
  const row = doctor({ home, projectRoot }).harnesses.find((h) => h.harness === "claude-code");
  expect(row?.guard).toBe("installed");
});

test("doctor: a settings file with an unrelated hook is absent", () => {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  const projectRoot = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  fs.mkdirSync(path.join(home, ".claude"));
  fs.writeFileSync(path.join(home, ".claude", "settings.json"),
    JSON.stringify({ hooks: { Stop: [{ hooks: [{ type: "command", command: "bun /opt/other/src/main.ts" }] }] } }));
  const row = doctor({ home, projectRoot }).harnesses.find((h) => h.harness === "claude-code");
  expect(row?.guard).toBe("absent");
});
