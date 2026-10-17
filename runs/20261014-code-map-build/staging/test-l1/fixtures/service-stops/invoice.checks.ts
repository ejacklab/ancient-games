import { submitInvoice } from "./workflow";

declare function test(name: string, body: () => unknown): void;
test("submits an invoice", () => submitInvoice(12));
