import { unitStamp as actualStamp, paddedStamp } from "./amounts";

declare function test(name: string, body: () => void): void;
declare function it(name: string, body: () => void): void;
declare function describe(name: string, body: () => void): void;

function unitStamp() { return -9; }

test("same spelling but another function", () => { unitStamp(); });

test("two calls are one test case", () => {
  actualStamp(2);
  actualStamp(7);
});

it("walks through a helper", () => {
  paddedStamp(4);
});

describe("ledger group", () => {
  test("nested ledger case", () => {
    actualStamp(6);
  });
});

export function setupLedger() { actualStamp(100); }
