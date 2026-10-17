import type { Answer, ChainStep, Limit, Link, Node, Step, TestCase } from "./answer.ts";

const place = (node: { file: string; line: number }) => `${node.file}:${node.line}`;

function nodeLine(node: Node): string {
  return `${node.name} (${node.kind}) ${place(node)}`;
}

function linkLine(link: Link): string {
  const target = link.to ? nodeLine(link.to) : `no implementation: ${link.reason ?? "unresolved"}`;
  const parts = [`${nodeLine(link.from)} ${link.kind} -> ${target}`, `at ${place(link.site)}`, link.resolution];
  if (link.declaration) parts.push(`declared at ${place(link.declaration)}`);
  if (link.via === "implementation-lookup") parts.push("via implementation lookup");
  for (const candidate of link.candidates) {
    parts.push(`candidate ${nodeLine(candidate)}${candidate.testFake ? " [test fake]" : ""}`);
  }
  return parts.join("; ");
}

function limitLine(limit: Limit): string {
  const where = limit.at ? ` at ${place(limit.at)}` : "";
  const text = limit.text ? `: ${limit.text}` : "";
  const ref = limit.ref ? ` (first shown at ${place(limit.ref)})` : "";
  return `limit ${limit.reason}${where}${ref}${text}`;
}

function chainLines(steps: ChainStep[], indent: string): string[] {
  const lines: string[] = [];
  for (const step of steps) {
    lines.push(`${indent}level ${step.level} ${linkLine(step.link)}${step.stop ? ` [stop ${limitLine(step.stop)}]` : ""}`);
    lines.push(...chainLines(step.children, `${indent}  `));
  }
  return lines;
}

function stepLines(step: Step, indent: string): string[] {
  const lines = [`${indent}${step.kind} ${place(step.at)}: ${step.text.split("\n")[0]}`];
  for (const child of step.children ?? []) lines.push(...stepLines(child, `${indent}  `));
  return lines;
}

function testLines(test: TestCase, indent: string): string[] {
  const lines = [`${indent}${test.name} (${place(test)}) through fake: ${test.throughFake}`];
  test.path.forEach((link, index) => lines.push(`${indent}  ${index + 1}. ${linkLine(link)}`));
  return lines;
}

export function renderText(answer: Answer): string {
  const lines: string[] = [`${answer.command} ${answer.query.join(" ")}`.trim()];
  if (answer.matches) {
    lines.push(answer.matches.length ? `${answer.matches.length} match(es):` : "no matches");
    for (const match of answer.matches) lines.push(`  ${nodeLine(match)}`);
    if (answer.ambiguous) lines.push("  ambiguous: more than one place matches; run chain on the one that fits and name the others");
  }
  for (const link of answer.links ?? []) lines.push(linkLine(link));
  if (answer.chain) {
    lines.push("up:");
    lines.push(...chainLines(answer.chain.up, "  "));
    lines.push("down:");
    lines.push(...chainLines(answer.chain.down, "  "));
  }
  if (answer.tests) {
    lines.push(`${answer.tests.label} (static links, not execution coverage): ${answer.tests.count} test(s)`);
    for (const test of answer.tests.tests) lines.push(...testLines(test, "  "));
    for (const test of answer.tests.undecided) lines.push(...testLines(test, "  undecided "));
  }
  if (answer.map) {
    lines.push(`definitions: ${answer.map.definitions.length}`);
    for (const definition of answer.map.definitions) lines.push(`  ${nodeLine(definition)}`);
    lines.push(`links: ${answer.map.links.length}`);
    for (const link of answer.map.links) lines.push(`  ${linkLine(link)}`);
    lines.push(`entries: ${answer.map.entries.length}`);
    for (const entry of answer.map.entries) {
      lines.push(`  ${nodeLine(entry.fn)}`);
      for (const step of entry.fn ? entry.steps : []) lines.push(...stepLines(step, "    "));
    }
    if (answer.map.siblings) {
      lines.push(`siblings: ${answer.map.siblings.members.join(", ")}`);
      for (const row of answer.map.siblings.rows) {
        lines.push(`  ${row.concern} [${row.status}]`);
        for (const cell of row.cells) lines.push(`    ${cell.member} ${place(cell.at)}: ${cell.text}`);
      }
    }
  }
  if (answer.empty) lines.push(`empty: ${answer.empty} (nothing was found by this analysis; this is not proof of absence)`);
  for (const limit of answer.limits) lines.push(limitLine(limit));
  return lines.join("\n");
}