import { Effect } from "../effect-runtime";
import { Capacity } from "./contract";

export const scheduleJob = Effect.fn("Queue.schedule")(function* () {
  const capacity = yield* Capacity.Service;

  return yield* capacity.reserve(4);
});
