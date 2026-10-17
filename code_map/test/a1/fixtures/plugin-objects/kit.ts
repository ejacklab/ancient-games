import { Context as Services, Effect as Base, type Task } from "../effect-runtime";

// Minimal stand-ins for Effect.gen, Schema, a plugin context and two services.
export namespace Effect {
  export const fn = Base.fn;
  export function gen<A>(body: () => Task<A>): Task<A> { return body(); }
}

export namespace Schema {
  export const Text = { kind: "string" } as const;
  export function Struct<Fields extends Record<string, unknown>>(fields: Fields) {
    return { kind: "struct" as const, fields };
  }
}

export type ToolDefinition = {
  name: string;
  input: unknown;
  execute: (input: any, context: { session: string }) => Task<unknown>;
};
export type Editor = { add(definition: ToolDefinition): Editor };
export type Context = { tool: { transform(change: (editor: Editor) => Editor): Task<void> } };

export class FileAccess extends Services.Service<FileAccess, {
  read(path: string): Task<string>;
  write(path: string, content: string): Task<void>;
}>()("FileAccess") {}

export class Permission extends Services.Service<Permission, {
  assert(path: string, session: string): Task<void>;
}>()("Permission") {}
