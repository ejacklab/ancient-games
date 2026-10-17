import { Effect } from "../effect-runtime";
import { Permission } from "./contract";

export const reconcileAccount = Effect.fn("Account.reconcile")(function* () {
  const permission = yield* Permission.Service;
  const account = "escrow";

  return yield* permission.assert({ account });
});
