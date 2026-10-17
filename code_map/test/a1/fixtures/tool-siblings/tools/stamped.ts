import { Effect } from "../../effect-runtime";
import { validateParcel, stampParcel } from "../support";


export const execute = Effect.fn("Stamped.execute")(function* (parcel: string) {
  const checked = validateParcel(parcel);
  const prepared = stampParcel(checked);
  return yield* Effect.succeed(prepared);
});
