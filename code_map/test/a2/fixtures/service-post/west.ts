import { Effect } from "../effect-runtime";

// reconcile violet parcel
export const reconcileParcel = Effect.fn("West.reconcile")(function* () {
  return "violet dispatch receipt";
});
