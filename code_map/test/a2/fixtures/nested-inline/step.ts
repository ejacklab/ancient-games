import { Effect, Stream, type Task } from "./runtime";

export interface Call { readonly id: string }
export interface Outcome { readonly id: string; readonly ok: boolean }
export interface Input {
  readonly events: Stream.Source<Call>;
  readonly run: (call: Call) => Task<Outcome>;
}

export const publish = Effect.fn("Bus.publish")(function* (event: Call) {
  return event.id;
});

export const store = Effect.fn("Store.save")(function* (outcome: Outcome) {
  return outcome.ok;
});

export function source(input: Input): Stream.Source<Call> {
  return input.events;
}

export const attempt = Effect.fn("Step.attempt")(function* (input: Input) {
  const executeTool = (call: Call) => {
    return input.run(call);
  };
  const stream = input.events;
  const fibers: boolean[] = [];
  yield* Stream.runForEach(stream, (event) =>
    Effect.gen(function* () {
      yield* publish(event);
      fibers.push(
        yield* Effect.uninterruptibleMask((restore) =>
          restore(
            executeTool(event),
          ).pipe(
            Effect.flatMap(store),
          ),
        ),
      );
    }),
  );
  const providerStream = source(input).pipe(
    Stream.runForEach((update) => Effect.gen(function* () {
      yield* publish(update);
      yield* Effect.uninterruptibleMask((restoreNext) =>
        restoreNext(
          executeTool(update),
        ),
      );
    })),
  );
  yield* providerStream;
  return fibers;
});
