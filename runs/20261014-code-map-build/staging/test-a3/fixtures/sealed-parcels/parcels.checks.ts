import { Effect } from "../effect-runtime";
import { ParcelDesk } from "./port";
import { receiptDigits } from "./live";
import { dispatchParcel, relayParcel } from "./workflow";

declare function test(name: string, body: () => void): void;
declare function it(name: string, body: () => void): void;
declare function describe(name: string, body: () => void): void;

const fakeDesk = ParcelDesk.of({
  seal: () => Effect.succeed(301),
});

test("submits a sealed parcel", () => {
  const task = relayParcel("amber-72");
  task.next();
  task.next(fakeDesk);
});

describe("evening parcels", () => {
  it("queues a second parcel", () => {
    const task = dispatchParcel("blue-19");
    task.next();
    task.next(fakeDesk);
  });
});

test("hashes receipt directly", () => {
  receiptDigits("direct-88");
});

export function notATest() {
  receiptDigits("setup-only");
}
