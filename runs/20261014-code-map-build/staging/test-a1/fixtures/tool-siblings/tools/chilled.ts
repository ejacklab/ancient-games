import { Effect } from "../../effect-runtime";
import { validateParcel, chillParcel } from "../support";


// Keep the same steps at a different line offset.

export const execute = Effect.fn("Chilled.execute")(function* (parcel: string) {
  const checked = validateParcel(parcel);
  const prepared = chillParcel(checked);
  return yield* Effect.succeed(prepared);
});
