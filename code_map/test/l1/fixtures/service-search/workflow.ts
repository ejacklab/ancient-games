import { Effect } from "../effect-runtime";

export const archiveParcel = Effect.fn("Archive.store")(function* () {
  return "stored";
});

/** archive parcel via the delayed vault. */
export const queuedDispatch = Effect.fn("Dispatch.queue")(function* () {
  return "queued";
});

export const auditDispatch = Effect.fn("Dispatch.audit")(function* () {
  return "archive parcel retention ledger";
});
