import { Effect } from "../effect-runtime";
import { Permission } from "./contract";

export const approveDraft = Effect.fn("Draft.approve")(function* (resource: string) {
  const permission = yield* Permission.Service;
  const allowed = yield* permission.assert({ resource });
  yield* permission.ask("publish draft?");
  return allowed;
});

export const approveBatch = Effect.fn("Batch.approve")(function* () {
  const permission = yield* Permission.Service;
  yield* permission.assert({ resource: "draft/first" });

  // A property access need not share its receiver's source line.
  yield* permission
    .assert({ resource: "draft/second" });
});
