import { Effect } from "../effect-runtime";

export const readFile = Effect.fn("Files.read")(function* (path: string) {
  return yield* Effect.succeed(`contents of ${path}`);
});

export const writeFile = Effect.fn("Files.write")(function* (path: string, content: string) {
  return yield* Effect.succeed(`${content.length} bytes to ${path}`);
});
