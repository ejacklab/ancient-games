import { Effect } from "../effect-runtime";
import { Settlement } from "./port";

export function increment(amount: number) { return amount + 1; }

export const settle = Effect.fn("Settlement.settle")(function* (amount: number) {
  return increment(amount);
});

export const settlement = Settlement.of({ settle });
