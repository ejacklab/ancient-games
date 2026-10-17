import { Effect } from "../effect-runtime";

export const checkPermission = Effect.fn("Permission.check")(function* (path: string) {
  return yield* Effect.succeed(!path.startsWith("/etc"));
});
