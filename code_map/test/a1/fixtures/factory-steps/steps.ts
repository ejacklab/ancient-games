import { Effect } from "../effect-runtime";

export namespace Steps {
  // The factory hands back an object; its methods are written here, not in a library.
  export const make = Effect.fn("Steps.make")(function* (limit: number) {
    const attempt = Effect.fn("Steps.attempt")(function* (label: string) {
      return yield* Effect.succeed(label.length <= limit);
    }); // end of attempt

    return { attempt };
  });
}
