import { Effect } from "../effect-runtime";
import { Capacity } from "./contract";

export const localLayer = Effect.fn("Capacity.local")(function* () {
  const reserve = Effect.fn("Local.reserve")(function* (units: number) {
    return yield* Effect.succeed(units + 7);
  });
  return Capacity.of({ reserve });
});


export const remoteLayer = Effect.fn("Capacity.remote")(function* () {
  const offset = 23;

  const reserve = Effect.fn("Remote.reserve")(function* (units: number) {
    return yield* Effect.succeed(units + offset);
  });
  return Capacity.of({ reserve });
});
