import { Effect } from "../../effect-runtime";
import { Depot } from "../port";

// The caller is outside module/, but the helper is called only within it.
export const intakeCrate = Effect.fn("Depot.intakeCrate")(function* (label: string) {
  const depot = yield* Depot.Service;
  const accepted = yield* depot.acceptCrate(label);
  if (!accepted) {
    return "rejected";
  } else {
    yield* depot.recordCrate(label);
  }
  return yield* localReceipt(label);
});

export const localReceipt = Effect.fn("Depot.localReceipt")(function* (label: string) {
  return yield* Effect.succeed(`receipt:${label}`);
});

export const unusedIntake = Effect.fn("Depot.unusedIntake")(function* () {
  return yield* Effect.succeed("unused");
});
