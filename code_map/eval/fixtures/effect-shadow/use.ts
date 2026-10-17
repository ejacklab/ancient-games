import { Effect } from "./effect";
import { RelayService } from "./api";
export const deliverRelay = Effect.fn("DeliverRelay")(function* () {
  const service = yield* RelayService;
  return service.deliver(1);
});
