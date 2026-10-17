import { submitLedger } from "./ledger";

declare const Bun: { write(path: URL, value: string): Promise<number> };
declare function test(name: string, body: () => void): void;


await Bun.write(new URL("./test-file-ran.marker", import.meta.url), "test file executed");

test("submits an adjusted ledger", () => {
  submitLedger();
});
