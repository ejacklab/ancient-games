import { Effect } from "../effect-runtime";
import { ParcelDesk } from "./port";

export function receiptDigits(parcel: string) {
  return parcel.length + 17;
}

export const deskLayer = Effect.fn("ParcelDesk.layer")(function* () {
  const prefix = "sealed/";

  const seal = Effect.fn("ParcelDesk.seal")(function* (parcel: string) {
    const digits = receiptDigits(prefix + parcel);
    return yield* Effect.succeed(digits);
  });

  return ParcelDesk.of({ seal });
});
