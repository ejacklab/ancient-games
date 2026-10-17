import { Effect } from "../effect-runtime";
import { ParcelDesk } from "./port";

// The report must follow the typed service member into the concrete body.
export const dispatchParcel = Effect.fn("Parcel.dispatch")(function* (parcel: string) {
  const desk = yield* ParcelDesk.Service;

  return yield* desk.seal(parcel);
});

export function relayParcel(parcel: string) {
  return dispatchParcel(parcel);
}
