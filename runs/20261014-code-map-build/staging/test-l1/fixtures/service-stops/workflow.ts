import { Effect } from "../effect-runtime";
import { Receipt, Settlement } from "./port";

export const submitInvoice = Effect.fn("Invoice.submit")(function* (amount: number) {
  const settlement = yield* Settlement.Service;
  return yield* settlement.settle(amount);
});

export const missingReceipt = Effect.fn("Invoice.receipt")(function* () {
  const receipt = yield* Receipt.Service;
  return yield* receipt.fetchReceipt();
});

export const chooseRoute = Effect.fn("Invoice.route")(function* (routes: Record<string, () => number>, key: string) {
  return routes[key]();
});

export const applyCallback = Effect.fn("Invoice.callback")(function* (callback: () => number) {
  return callback();
});

export const roundInvoice = Effect.fn("Invoice.round")(function* (amount: number) {
  return Math.abs(amount);
});

export const idleInvoice = Effect.fn("Invoice.idle")(function* () {
  return 0;
});
