import { billForCrate } from "./caller";

declare function test(name: string, body: () => void): void;

test("prices a crate", () => {
  billForCrate(6);
});
