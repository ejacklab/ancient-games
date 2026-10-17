import { submitLedger } from "./caller";

declare function test(name: string, body: () => void): void;

test("submits a private ledger", () => {
  submitLedger(3);
});
