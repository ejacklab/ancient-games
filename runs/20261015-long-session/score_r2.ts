// Round 2 scorer: (a)–(e) as round 1, plus (f) the agent's own failures logged, (g) every logged failure answered.
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { execSync } from "node:child_process";
import os from "node:os"; import path from "node:path";
const G = "/home/smoke01/dev/ancient-games/.claude/skills/workflow-design/guard/src";
const { findInsightFiles, openFailures } = await import(`${G}/insight.ts`);
const { readJournal } = await import(`${G}/journal.ts`);
const HERE = path.dirname(new URL(import.meta.url).pathname);
const dir = process.argv[2] ?? "runs-r2";
const out = ["| Run | (a) redirected / calls | own failures (transcript) | (f) own logged | engine logged | (g) all answered | (d) named | (e) green + REPORT | blocks | seconds |", "|---|---|---|---|---|---|---|---|---|---|"];
for (const d of readdirSync(path.join(HERE, dir)).sort()) {
  const run = JSON.parse(readFileSync(path.join(HERE, dir, d, "run.json"), "utf8")); const sb = run.sandbox as string;
  const shimF = path.join(sb, ".shim-calls.log");
  const shim = existsSync(shimF) ? readFileSync(shimF, "utf8").trim().split("\n").filter(Boolean) : [];
  const proj = path.join(os.homedir(), ".claude", "projects", sb.replace(/\//g, "-"));
  const lines = existsSync(proj) ? readdirSync(proj).filter((f) => f.endsWith(".jsonl")).flatMap((f) => readFileSync(path.join(proj, f), "utf8").split("\n")) : [];
  // ground truth: Bash calls whose result is an error, and test runs whose output shows failures with no error flag
  const bashIds = new Set<string>(); let own = 0; let blocks = 0;
  for (const l of lines) { let j: any; try { j = JSON.parse(l); } catch { continue; }
    const c = j?.message?.content; if (typeof c === "string" && c.startsWith("Stop hook feedback")) blocks++;
    if (!Array.isArray(c)) continue;
    for (const x of c) {
      if (x?.type === "tool_use" && x.name === "Bash") bashIds.add(x.id);
      if (x?.type === "tool_result" && bashIds.has(x.tool_use_id)) {
        const t = JSON.stringify(x.content ?? "");
        if (x.is_error || /\b[1-9]\d* (failed|errors?)\b/.test(t)) own++;
      } } }
  const recs = readJournal(sb).records.filter((r: any) => r.kind === "failure");
  const engine = recs.filter((r: any) => /codex|engine|R12\.1/i.test(`${r.check} ${r.input} ${r.engine}`)).length;
  const ownLogged = recs.length - engine;
  const open = openFailures(sb, null); const files = findInsightFiles(sb);
  const final = readFileSync(path.join(HERE, dir, d, "final.txt"), "utf8");
  const report = existsSync(path.join(sb, "REPORT.md")) ? readFileSync(path.join(sb, "REPORT.md"), "utf8") : "";
  const named = files.some((f: string) => (final + report).includes(path.basename(f)));
  let green = false; try { execSync("python3 -m pytest -q", { cwd: sb, stdio: "ignore", timeout: 120000 }); green = true; } catch {}
  out.push(`| ${d} | ${shim.filter((l) => l.includes("stdin=/dev/null")).length} / ${shim.length} | ${own} | ${ownLogged} | ${engine} | ${recs.length && !open.length ? "yes" : recs.length ? `**no** (${open.length} open)` : "—"} | ${files.length ? (named ? "yes" : "**no**") : "—"} | ${green ? "green" : "**red**"} + ${report ? "yes" : "**no**"} | ${blocks} | ${run.seconds}${run.exit === 124 ? " (timer)" : ""} |`);
}
console.log(out.join("\n"));
