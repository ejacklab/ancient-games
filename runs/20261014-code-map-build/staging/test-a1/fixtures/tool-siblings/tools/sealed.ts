import { Effect } from "../../effect-runtime";
import { validateParcel, sealParcel } from "../support";

// Each tool implements the same callable shape through a constant.
export const execute = Effect.fn("Sealed.execute")(function* (parcel: string) {
  const checked = validateParcel(parcel);
  const prepared = sealParcel(checked);
  return yield* Effect.succeed(prepared);
});
