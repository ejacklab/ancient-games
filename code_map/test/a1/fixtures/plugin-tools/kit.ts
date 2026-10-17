import type { Task } from "../effect-runtime";

// Minimal stand-ins for Effect's Schema and a plugin Tool builder.
export namespace Schema {
  export const Text = { kind: "string" } as const;
  export function Struct<Fields extends Record<string, unknown>>(fields: Fields) {
    return { kind: "struct" as const, fields };
  }
}

export namespace Tool {
  export function make<I, O, Args extends unknown[], A>(definition: {
    name: string;
    input: I;
    output: O;
    execute: (...args: Args) => Task<A>;
  }) {
    return definition;
  }
}
