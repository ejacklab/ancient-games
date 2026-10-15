// Scores the long-session runs from files: shim log, journal, insight files, REPORT.md, final message, transcript.
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { execSync } from "node:child_process";
import os from "node:os"; import path from "node:path";
const G = "/home/smoke01/dev/ancient-games/.claude/skills/workflow-design/guard/src";
const { findInsightFiles, openFailures } = await import(`${G}/insight.ts`);
const { readJournal } = await import(`${G}/journal.ts`);
const HERE = path.dirname(new URL(import.meta.url).pathname);
const rows: string[] = ["| Run | (a) redirected / calls | (b) failures logged | (c) valid insight answers all | (d) named | (e) pytest green + REPORT.md | Stop blocks | denies | seconds |", "|---|---|---|---|---|---|---|---|---|"];
for (const d of readdirSync(path.join(HERE, "runs")).sort()) {
  const run = JSON.parse(readFileSync(path.join(HERE, "runs", d, "run.json"), "utf8"));
  const sb = run.sandbox as string;
  const shimFile = path.join(sb, ".shim-calls.log");
  const shim = existsSync(shimFile) ? readFileSync(shimFile, "utf8").trim().split("\n").filter(Boolean) : [];
  const redirected = shim.filter((l) => l.includes("stdin=/dev/null")).length;
  const fails = readJournal(sb).records.filter((r: any) => r.kind === "failure");
  const open = openFailures(sb, null);
  const files = findInsightFiles(sb);
  const final = readFileSync(path.join(HERE, "runs", d, "final.txt"), "utf8");
  const report = existsSync(path.join(sb, "REPORT.md")) ? readFileSync(path.join(sb, "REPORT.md"), "utf8") : "";
  const named = files.some((f: string) => (final + report).includes(path.basename(f)));
  let green = false; try { execSync("python3 -m pytest -q", { cwd: sb, stdio: "ignore", timeout: 120000 }); green = true; } catch {}
  const proj = path.join(os.homedir(), ".claude", "projects", sb.replace(/\//g, "-"));
  const tx = existsSync(proj) ? readdirSync(proj).filter((f) => f.endsWith(".jsonl")).map((f) => readFileSync(path.join(proj, f), "utf8")).join("\n") : "";
  const blocks = (tx.match(/Stop hook feedback/g) ?? []).length;
  const denies = (tx.match(/"decision":"reject","source":"hook"/g) ?? []).length;
  rows.push(`| ${d} | ${redirected} / ${shim.length} | ${fails.length} | ${fails.length > 0 && open.length === 0 ? "yes" : fails.length === 0 ? "— (none logged)" : "**no** (" + open.length + " open)"} | ${files.length ? (named ? "yes" : "**no**") : "—"} | ${green ? "green" : "**red**"} + ${report ? "yes" : "**no**"} | ${blocks} | ${denies} | ${run.seconds}${run.exit === 124 ? " (timer)" : ""} |`);
}
console.log(rows.join("\n"));
