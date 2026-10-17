import { Effect } from "../effect-runtime";
import { Ledger } from "./port";

export const submitLedger = Effect.fn("Ledger.submit")(function* () {
  const ledger = yield* Ledger.Service;
  return yield* ledger.settle();
});
