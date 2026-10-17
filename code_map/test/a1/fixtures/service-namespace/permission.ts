import { Context, Effect, type Task } from "../effect-runtime";

export type Request = { action: string; path: string };

export interface Interface {
  readonly assert: (request: Request) => Task<boolean>;
}

export class Service extends Context.Service<Service, Interface>()("@app/Permission") {}

export const layer = Effect.fn("Permission.layer")(function* () {
  const assert = Effect.fn("Permission.assert")(function* (request: Request) {
    return yield* Effect.succeed(request.action === "read" || !request.path.startsWith("/etc"));
  });

  return Service.of({ assert });
});
