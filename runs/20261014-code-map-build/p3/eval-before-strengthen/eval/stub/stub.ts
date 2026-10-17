import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { isDeepStrictEqual } from "node:util";
import { loadCaseFile } from "../case-file.ts";
import { toolArguments } from "../run.ts";

const file = await loadCaseFile(resolve(import.meta.dir, "../cases/fixtures.json"));
const args = Bun.argv.slice(2);
const matching = file.cases.filter(test => isDeepStrictEqual(toolArguments(file, test), args));
if (!matching.length) {
  console.log(JSON.stringify({ command: args[0] ?? "", limits: [], empty: "none found by static analysis" }));
} else {
  const answers = await Promise.all(matching.map(test => readFile(resolve(import.meta.dir, "answers", test.id + ".json"), "utf8")));
  const answer: unknown = JSON.parse(answers[0]!);
  // Several checks can ask the same question; breaking any of their canned files must be visible.
  if (answers.some(text => !isDeepStrictEqual(JSON.parse(text), answer))) {
    throw new Error(`Conflicting canned answers for identical command: ${matching.map(test => test.id).join(", ")}`);
  }
  if (matching[0]!.format === "text") {
    const value = answer as { matches: { name: string; file: string; line: number }[] };
    console.log(value.matches.map(node => `${node.name} — ${node.file}:${node.line}`).join("\n"));
  } else console.log(JSON.stringify(answer));
}
