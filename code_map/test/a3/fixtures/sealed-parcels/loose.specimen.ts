import { receiptDigits } from "./live";

declare function test(name: string, body: () => void): void;

test("selected only by an explicit spec pattern", () => {
  receiptDigits("loose-46");
});
