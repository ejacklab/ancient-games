import { describe, expect, test } from "bun:test";
import { matchAnswer, selectPath, collectLimitReasons, type Expectation } from "../../eval/matcher.ts";
import { validateCaseFile } from "../../eval/case-file.ts";
import { requirementLines } from "../../eval/requirements.ts";

const emptyExpect: Expectation = { includes: [], excludes: [], equals: [], ambiguous: null, limitReasons: [] };
const answer = {
  ambiguous: true, limits: [{ reason: "dynamic" }], links: [{ to: { file: "a.ts", line: 4 } }],
  chain: { down: [{ link: { to: { file: "first.ts", line: 1 } }, children: [
    { link: { to: { file: "second.ts", line: 2 } }, children: [
      { link: { to: { file: "third.ts", line: 3 } }, children: [], stop: { reason: "depth" } },
    ] },
  ] }] },
};

describe("case matcher", () => {
  test("includes requires both file and line; excludes rejects that location", () => {
    const location = { path: "links[].to", file: "a.ts", line: 4 };
    expect(matchAnswer(answer, { ...emptyExpect, includes: [location] })).toEqual([]);
    expect(matchAnswer(answer, { ...emptyExpect, includes: [{ ...location, line: 5 }] })).toHaveLength(1);
    expect(matchAnswer(answer, { ...emptyExpect, excludes: [location] })).toHaveLength(1);
    expect(matchAnswer(answer, { ...emptyExpect, excludes: [{ ...location, file: "b.ts" }] })).toEqual([]);
  });
  test("text includes/excludes match file:line places in both directions", () => {
    const location = { path: "matches[]", file: "chain/logic.ts", line: 3 };
    const text = "leaf — chain/logic.ts:3\n";
    expect(matchAnswer(text, { ...emptyExpect, includes: [location] })).toEqual([]);
    expect(matchAnswer(text, { ...emptyExpect, excludes: [location] })).toHaveLength(1);
    for (const other of ["chain/logic.ts:30", "chain/logic.ts:4", "other/chain/logic.ts:3", "chain/logicXts:3", ""]) {
      expect(matchAnswer(other, { ...emptyExpect, includes: [location] })).toHaveLength(1);
      expect(matchAnswer(other, { ...emptyExpect, excludes: [location] })).toEqual([]);
    }
    expect(matchAnswer("(chain/logic.ts:3)", { ...emptyExpect, includes: [location] })).toEqual([]);
  });
  test("equals distinguishes deep arrays, absent, null and empty selections", () => {
    expect(matchAnswer(answer, { ...emptyExpect, equals: [{ path: "links[].to.line", value: [4] }] })).toEqual([]);
    expect(matchAnswer(answer, { ...emptyExpect, equals: [{ path: "links[].to.line", value: 4 }] })).toHaveLength(1);
    expect(matchAnswer({}, { ...emptyExpect, equals: [{ path: "missing", value: null }] })).toHaveLength(1);
    expect(matchAnswer({ value: null }, { ...emptyExpect, equals: [{ path: "value", value: null }] })).toEqual([]);
    expect(matchAnswer({}, { ...emptyExpect, equals: [{ path: "links[].to", value: [] }] })).toEqual([]);
  });
  test("shapes allow extra object fields and unordered arrays with exact membership", () => {
    const check = { ...emptyExpect, shapes: [{ path: "links", value: [
      { from: { line: 1 }, candidates: [{ line: 2 }, { line: 3 }] },
      { from: { line: 4 }, candidates: [] },
    ] }] };
    const allowed = { links: [
      { from: { line: 4, endLine: 4 }, candidates: [], declaration: { line: 9 } },
      { from: { line: 1, name: "holder" }, candidates: [{ line: 3, testFake: true }, { line: 2 }] },
    ] };
    expect(matchAnswer(allowed, check)).toEqual([]);
    const wrong = structuredClone(allowed); wrong.links[1]!.candidates[0]!.line = 2;
    expect(matchAnswer(wrong, check)).toHaveLength(1);
    expect(matchAnswer({ links: [...allowed.links, allowed.links[0]] }, check)).toHaveLength(1);
    expect(matchAnswer({ links: allowed.links.slice(1) }, check)).toHaveLength(1);
    expect(matchAnswer({}, { ...emptyExpect, shapes: [{ path: "links", value: [] }] })).toHaveLength(1);
    expect(matchAnswer({ links: [] }, { ...emptyExpect, shapes: [{ path: "links", value: [] }] })).toEqual([]);
    // A broad shape must not take the only item compatible with a narrower one.
    expect(matchAnswer({ links: [{ line: 1 }, { line: 2 }] }, {
      ...emptyExpect, shapes: [{ path: "links", value: [{}, { line: 1 }] }],
    })).toEqual([]);
    expect(matchAnswer({ links: [{ line: 2 }, { line: 2 }] }, {
      ...emptyExpect, shapes: [{ path: "links", value: [{}, { line: 1 }] }],
    })).toHaveLength(1);
    expect(matchAnswer({ value: null }, { ...emptyExpect, shapes: [{ path: "value", value: null }] })).toEqual([]);
    expect(matchAnswer({}, { ...emptyExpect, shapes: [{ path: "value", value: null }] })).toHaveLength(1);
    expect(matchAnswer({ value: {} }, { ...emptyExpect, shapes: [{ path: "value", value: { name: "holder" } }] })).toHaveLength(1);
  });
  test("exact limit reasons allow a branch reason to be repeated in the summary, but no other reason", () => {
    const check = { ...emptyExpect, exactLimitReasons: ["depth"] };
    expect(matchAnswer({ limits: [], chain: { stop: { reason: "depth", text: "at depth" } } }, check)).toEqual([]);
    expect(matchAnswer({ limits: [{ reason: "depth" }], chain: { stop: { reason: "depth" } } }, check)).toEqual([]);
    expect(matchAnswer({ limits: [{ reason: "depth" }, { reason: "dynamic" }] }, check)).toHaveLength(1);
    expect(matchAnswer({ limits: [] }, check)).toHaveLength(1);
    expect(matchAnswer({ limits: [{ reason: "dynamic" }] }, { ...emptyExpect, exactLimitReasons: [] })).toHaveLength(1);
  });
  test("ambiguous null skips, booleans check explicitly, missing false is not false", () => {
    expect(matchAnswer(answer, emptyExpect)).toEqual([]);
    expect(matchAnswer(answer, { ...emptyExpect, ambiguous: true })).toEqual([]);
    expect(matchAnswer(answer, { ...emptyExpect, ambiguous: false })).toHaveLength(1);
    expect(matchAnswer({}, { ...emptyExpect, ambiguous: false })).toHaveLength(1);
  });
  test("[] walks arrays, children visits all descendants, and missing fields do not invent values", () => {
    expect(selectPath(answer, "chain.down[].children[].link.to.file")).toEqual(["second.ts", "third.ts"]);
    expect(selectPath(answer, "chain.down[].children.link.to.line")).toEqual([2, 3]);
    expect(selectPath(answer, "chain.down[].children[].children[].link.to.file")).toEqual(["third.ts"]);
    expect(selectPath(answer, "links.to")).toEqual([]);
    expect(selectPath(answer, "missing[].value")).toEqual([]);
    expect(selectPath(answer, "chain.down[].children[].absent")).toEqual([]);
    expect(() => selectPath(answer, "links[0].to")).toThrow("Invalid expectation path");
  });
  test("limitReasons is confined to limits and stop, including deep branches", () => {
    expect(collectLimitReasons(answer)).toEqual(["dynamic", "depth"]);
    expect(matchAnswer(answer, { ...emptyExpect, limitReasons: ["depth", "dynamic"] })).toEqual([]);
    expect(matchAnswer(answer, { ...emptyExpect, limitReasons: ["seen"] })).toHaveLength(1);
    expect(collectLimitReasons({ candidates: [{ reason: "seen" }] })).toEqual([]);
  });
});

describe("case-file boundary", () => {
  function suite() {
    return { project: ["tsconfig.json"], root: ".", tests: [], cases: [
      { id: "case", requirement: "A2", line: requirementLines.A2[0] as string, args: ["find", "x"], expect: emptyExpect },
    ] };
  }
  test("validates exact Fails-if identity and rejects invalid predicates and duplicate ids", () => {
    expect(validateCaseFile(suite()).cases[0]!.line).toBe(requirementLines.A2[0]);
    const wrongLine = suite(); wrongLine.cases[0]!.line = "a made up check";
    expect(() => validateCaseFile(wrongLine)).toThrow("Unknown Fails-if line");
    const duplicate = suite(); duplicate.cases.push(duplicate.cases[0]!);
    expect(() => validateCaseFile(duplicate)).toThrow("duplicate case");
    const invalid = suite(); invalid.cases[0]!.expect = { ...emptyExpect, includes: [{ path: "links[2]", file: "a.ts", line: 1 }] };
    expect(() => validateCaseFile(invalid)).toThrow("Invalid expectation path");
    expect(() => validateCaseFile({ ...suite(), tests: null })).toThrow();
  });
  test("validates optional shape paths and exact limit reason lists", () => {
    const valid = suite();
    valid.cases[0]!.expect = { ...emptyExpect, shapes: [{ path: "links[].to", value: [{ line: 1 }] }], exactLimitReasons: ["depth"] };
    expect(validateCaseFile(valid).cases[0]!.expect).toEqual(valid.cases[0]!.expect);
    for (const shapes of [null, {}, [{ value: [] }], [{ path: "links[0]", value: [] }], [{ path: "links" }]]) {
      const invalid = suite(); invalid.cases[0]!.expect = { ...emptyExpect, shapes } as any;
      expect(() => validateCaseFile(invalid)).toThrow();
    }
    const invalid = suite(); invalid.cases[0]!.expect = { ...emptyExpect, exactLimitReasons: [1] } as any;
    expect(() => validateCaseFile(invalid)).toThrow("Invalid exact limit reasons");
  });
});
