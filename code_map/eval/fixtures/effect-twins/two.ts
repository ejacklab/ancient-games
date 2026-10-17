import { Effect } from "./effect";
export const relayStep = Effect.fn("RelayStep")(function* () {
  return 2;
});
