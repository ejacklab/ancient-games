import { Effect } from "../effect-runtime";
import { Steps } from "./steps";

export const runStep = Effect.fn("runStep")(function* (label: string) {
  const steps = yield* Steps.make(3);
  return yield* steps.attempt(label);
});
