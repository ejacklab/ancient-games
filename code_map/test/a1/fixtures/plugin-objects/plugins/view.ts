import { Effect, FileAccess, Schema, type Context } from "../kit";

export const name = "view"
export const Input = Schema.Struct({ path: Schema.Text, line: Schema.Text })
export const Plugin = {
  id: "app.tool.view",
  effect: Effect.fn("ViewTool.Plugin")(function* (ctx: Context) {
    const access = yield* FileAccess.Service
    yield* ctx.tool.transform((editor) => editor.add({ name, input: Input, execute: (input, context) => Effect.gen(function* () {
      const shown = yield* access.read(input.path);
      return `${input.line}:${shown}`;
    }) }))
  }),
}
