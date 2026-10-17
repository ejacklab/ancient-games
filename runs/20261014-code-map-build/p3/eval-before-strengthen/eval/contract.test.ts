import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { validateAnswer } from "../../eval/contract.ts";
import { matchAnswer } from "../../eval/matcher.ts";
import { validateCaseFile } from "../../eval/case-file.ts";

const evalDir = resolve(import.meta.dir, "../../eval");
const suite = validateCaseFile(JSON.parse(readFileSync(resolve(evalDir, "cases/fixtures.json"), "utf8")));
const canned = (id: string): any => JSON.parse(readFileSync(resolve(evalDir, "stub/answers", id + ".json"), "utf8"));
function failures(id: string, mutate: (answer: any) => void) {
  const answer = canned(id); mutate(answer);
  const sample = suite.cases.find(sample => sample.id === id)!;
  return [...matchAnswer(answer, sample.expect), ...validateAnswer(answer, sample.args, sample.tests ?? suite.tests, resolve(evalDir, "fixtures"))];
}

describe("independent fixture checks", () => {
  for (const sample of suite.cases) test(`correct canned ${sample.id}`, () => {
    const answer = canned(sample.id);
    if (["R1", "R3"].includes(sample.requirement)) return;
    if (sample.format === "text") {
      const text = answer.matches.map((node: any) => `${node.name} — ${node.file}:${node.line}`).join("\n");
      expect(matchAnswer(text, sample.expect)).toEqual([]); return;
    }
    expect(matchAnswer(answer, sample.expect)).toEqual([]);
    expect(validateAnswer(answer, sample.args, sample.tests ?? suite.tests, resolve(evalDir, "fixtures"))).toEqual([]);
  });
  const mutations: [string, string, (answer: any) => void][] = [
    ["missing implementation", "R2-all-implementations", a => a.links[0].candidates.pop()],
    ["declaration as implementation", "R2-declaration", a => a.links[0].to = { ...a.links[0].to, file: "services/api.ts", line: 2 }],
    ["fake loses label", "R2-test-fake", a => delete a.links[0].candidates[1].testFake],
    ["fake as real", "R2-test-fake", a => a.links[0].to = a.links[0].candidates[1]],
    ["ambiguous unmarked", "R2-ambiguous", a => a.links[0].resolution = "implementation"],
    ["unresolved unmarked", "R2-unresolved", a => delete a.links[0].resolution],
    ["unresolved without reason", "R2-unresolved", a => delete a.links[0].reason],
    ["missing map location", "A1-module-siblings", a => delete a.map.definitions[0].line],
    ["map contradicts code", "A1-module-siblings", a => a.map.entries[0].steps[1].text = "return value + 9;"],
    ["missing definition", "A1-module-siblings", a => a.map.definitions.pop()],
    ["missing sibling", "A1-module-siblings", a => a.map.siblings.members.pop()],
    ["known place missing", "A2-find-known", a => a.matches = []],
    ["ambiguity treated as certainty", "A2-ambiguous-find", a => a.ambiguous = false],
    ["unnamed candidate", "A2-ambiguous-find", a => a.matches.pop()],
    ["known chain link missing", "A2-known-chain", a => a.chain.down[0].children = []],
    ["constant arrow chain missing", "A2-const-chain", a => a.chain.down = []],
    ["Effect.fn body not walked", "A2-const-chain", a => a.chain.down[0].children = []],
    ["constant function expression not walked", "A2-const-chain-through", a => a.chain.down = []],
    ["object property arrow not walked", "A2-const-chain-through", a => a.chain.down[0].children = []],
    ["constant caller missing", "A2-const-callers", a => a.links = []],
    ["constant callee missing", "A2-const-callees", a => a.links = []],
    ["Effect.fn caller loses its constant name", "A2-const-callers", a => a.links[0].from.name = "<anonymous>"],
    ["property callee loses its holder name", "A2-const-callees", a => a.links[0].to.name = "<anonymous>"],
    ["constant test path missing", "A3-const-tests", a => { a.tests.tests = []; a.tests.count = 0; }],
    ["constant test path skips Effect.fn", "A3-const-tests", a => a.tests.tests[0].path.splice(3, 1)],
    ["constant map definition missing", "A1-const-map", a => a.map.definitions.splice(3, 1)],
    ["constant map entry missing", "A1-const-map", a => a.map.entries = []],
    ["constant entry decision missing", "A1-const-map", a => a.map.entries[0].steps.shift()],
    ["constant entry steps out of source order", "A1-const-map", a => a.map.entries[0].steps.reverse()],
    ["constant comment search missing", "A2-const-find-comment", a => a.matches = []],
    ["constant string search missing", "A2-const-find-string", a => a.matches = []],
    ["missing link kind", "A2-link-kind-location", a => delete a.chain.down[0].link.kind],
    ["missing link location", "A2-link-kind-location", a => delete a.chain.down[0].link.site],
    ["duplicate function expanded", "A2-shared-once", a => delete a.chain.down[0].children[1].stop],
    ["bad seen ref", "A2-shared-once", a => a.chain.down[0].children[1].stop.ref.line = 99],
    ["depth exceeded", "A2-default-six-down", a => a.chain.down[0].level = 7],
    ["count differs", "A3-count-evidence", a => a.tests.count = 9],
    ["no test evidence", "A3-count-evidence", a => a.tests.tests[0].path = []],
    ["disconnected test evidence", "A3-count-evidence", a => a.tests.tests[0].path[1].from.line = 42],
    ["known test missing", "A3-known-path", a => a.tests.tests = []],
    ["coverage label", "A3-static-label", a => a.tests.label = "execution coverage"],
    ["fake counted without rule", "A3-fake-unset", a => { a.tests.tests = a.tests.undecided; a.tests.undecided = []; a.tests.count = 1; }],
    ["fake rule limit missing", "A3-fake-unset", a => a.limits = []],
    ["file report unasked", "A3-no-file-report", a => a.tests = { label: "static-call-path", count: 0, tests: [], undecided: [] }],
    ["whole map unasked", "A5-specific-answer", a => a.map = canned("A1-module-siblings").map],
    ["answer limits missing", "A5-specific-answer", a => delete a.limits],
    ["unknown whole-repo payload", "A5-specific-answer", a => a.repositoryDump = {}],
    ["empty proves absence", "L1-empty", a => a.empty = "nothing exists"],
    ["early branch no reason", "L1-depth-zero", a => a.limits = []],
    ["nonempty marked empty", "A5-specific-answer", a => a.empty = "none found by static analysis"],
  ];
  for (const [name, id, mutate] of mutations) test(`rejects ${name}`, () => {
    expect(failures(id, mutate).length).toBeGreaterThan(0);
  });
});

// These use contract/source checks alone so unrelated case equalities cannot hide a validation gap.
describe("source relationships", () => {
  function check(id: string, mutate: (answer: any) => void) {
    const answer = canned(id); mutate(answer);
    const sample = suite.cases.find(sample => sample.id === id)!;
    return validateAnswer(answer, sample.args, sample.tests ?? suite.tests, resolve(evalDir, "fixtures"));
  }
  const mutations: [string, string, (answer: any) => void][] = [
    ["sibling text at wrong source location", "A1-module-siblings", a => a.map.siblings.rows[0].cells[0].text = "return value + 1;"],
    ["flow text at wrong source location", "A1-module-siblings", a => a.map.entries[0].steps[1].text = "return value + 9;"],
    ["chain first down link detached from query", "A2-known-chain", a => a.chain.down[0].link.from.line = 4],
    ["chain child detached from parent", "A2-known-chain", a => a.chain.down[0].children[0].link.from.line = 4],
    ["chain first up link detached from query", "A2-default-six-up", a => { a.chain.up[0].link.to.line = 8; a.chain.up[0].link.candidates[0].line = 8; }],
    ["chain up child detached from parent", "A2-default-six-up", a => { a.chain.up[0].children[0].link.to.line = 7; a.chain.up[0].children[0].link.candidates[0].line = 7; }],
    ["test path starts outside test", "A3-count-evidence", a => a.tests.tests[0].path[0].from.line = 2],
    ["test path ends at wrong function", "A3-count-evidence", a => { const last = a.tests.tests[0].path.at(-1); last.to.line = 4; last.candidates[0].line = 4; }],
    ["test path links do not join", "A3-count-evidence", a => a.tests.tests[0].path[1].from.line = 4],
    ["test site is not a call on the source line", "A3-count-evidence", a => a.tests.tests[0].path[0].site.line = 2],
    ["test site belongs to another function", "A3-count-evidence", a => a.tests.tests[0].path[1].site.line = 4],
    ["Service.of shorthand reported as a caller", "A2-const-callers", a => a.links[0].site.line = 19],
    ["object property call attributed to module", "A2-const-callees", a => { a.links[0].from.kind = "other"; a.links[0].from.line = 19; }],
    ["chain section in where response", "A5-specific-answer", a => a.chain = { up: [], down: [] }],
    ["links section in where response", "A5-specific-answer", a => a.links = []],
  ];
  for (const [name, id, mutate] of mutations) test(`rejects ${name}`, () => expect(check(id, mutate).length).toBeGreaterThan(0));
  test("trailing whitespace allowed, internal whitespace and truncation rejected", () => {
    expect(check("A1-module-siblings", a => a.map.siblings.rows[0].cells[0].text += " \t")).toEqual([]);
    expect(check("A1-module-siblings", a => a.map.siblings.rows[0].cells[0].text = "if (value<0) return 0;").length).toBeGreaterThan(0);
    expect(check("A1-module-siblings", a => a.map.siblings.rows[0].cells[0].text = "if (value < 0)").length).toBeGreaterThan(0);
  });
  test("known sibling classification cannot be unclear", () => expect(failures("A1-shared-and-varies", a => a.map.siblings.rows[0].status = "unclear").length).toBeGreaterThan(0));
  test("computed call must state dynamic limit", () => expect(failures("A2-computed-member", a => a.limits = []).length).toBeGreaterThan(0));
  test("blanket limit is rejected on complete answer", () => expect(failures("L1-no-blanket-limit", a => a.limits = [{ reason: "dynamic" }]).length).toBeGreaterThan(0));
});
