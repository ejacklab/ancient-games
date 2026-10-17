export type Task<A> = Generator<unknown, A, unknown>;

export namespace Context {
  export function Service<Self, Shape>() {
    return (_key: string) => class {
      static Service: Task<Shape>;
      static of(implementation: Shape): Shape { return implementation; }
    };
  }
}

export namespace Effect {
  export function fn(_label: string) {
    return <Args extends unknown[], A>(body: (...args: Args) => Task<A>) => body;
  }
}
