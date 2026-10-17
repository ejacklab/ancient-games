import { Effect } from "../effect-runtime";
import { Permission, type Request } from "./contract";

// The returned object carries references, not method bodies.
export const permissionLayer = Effect.fn("Permission.layer")(function* () {
  const prefix = "draft/";

  const assert = Effect.fn("Permission.assert")(function* (input: Request) {
    return yield* Effect.succeed(input.resource.startsWith(prefix));
  });

  const ask = Effect.fn("Permission.ask")(function* (prompt: string) {
    return yield* Effect.succeed(`question: ${prompt}`);
  });

  return Permission.of({ assert, ask });
});
