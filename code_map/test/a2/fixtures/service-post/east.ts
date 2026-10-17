import { Effect } from "../effect-runtime";


// reconcile violet parcel
export const reconcileParcel = Effect.fn("East.reconcile")(function* () {
  return "violet dispatch receipt";
});
