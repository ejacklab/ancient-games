// A minimal Effect-like stand-in. Nothing here is run by the tests; it only has to type-check.
export interface Task<A> {
  [Symbol.iterator](): Generator<unknown, A, unknown>;
  pipe<B>(next: (self: Task<A>) => B): B;
}

export function task<A>(body: () => Generator<unknown, A, unknown>): Task<A> {
  const self: Task<A> = {
    [Symbol.iterator]: body,
    pipe<B>(next: (self: Task<A>) => B): B { return next(self); },
  };
  return self;
}

export namespace Effect {
  export function fn(_label: string) {
    return <Args extends unknown[], A>(body: (...args: Args) => Generator<unknown, A, unknown>) => body;
  }
  export function gen<A>(body: () => Generator<unknown, A, unknown>): Task<A> {
    return task(body);
  }
  export function uninterruptibleMask<A>(body: (restore: <B>(effect: Task<B>) => Task<B>) => Task<A>): Task<A> {
    return body((effect) => effect);
  }
  export function flatMap<A, B>(next: (value: A) => Generator<unknown, B, unknown>) {
    return (self: Task<A>): Task<B> => task(function* () { return yield* next(yield* self); });
  }
}

export namespace Stream {
  export interface Source<A> {
    readonly items: readonly A[];
    pipe<B>(next: (self: Source<A>) => B): B;
  }
  // Data-first, or as an operator for pipe, like Effect's dual APIs.
  export function runForEach<A, B>(each: (item: A) => Task<B>): (source: Source<A>) => Task<void>;
  export function runForEach<A, B>(source: Source<A>, each: (item: A) => Task<B>): Task<void>;
  export function runForEach<A, B>(
    first: Source<A> | ((item: A) => Task<B>), second?: (item: A) => Task<B>,
  ): Task<void> | ((source: Source<A>) => Task<void>) {
    const drain = (source: Source<A>, each: (item: A) => Task<B>): Task<void> =>
      task(function* () { for (const item of source.items) yield* each(item); });
    if (typeof first === "function") return (source: Source<A>) => drain(source, first);
    return drain(first, second!);
  }
}
