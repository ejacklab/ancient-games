import { Effect, FileAccess, Schema, type Context } from "../kit";

export const name = "read"
export const Input = Schema.Struct({ path: Schema.Text })
export const Plugin = {
  id: "app.tool.read",
  effect: Effect.fn("ReadTool.Plugin")(function* (ctx: Context) {
    const access = yield* FileAccess.Service
    yield* ctx.tool.transform((editor) => editor.add({ name, input: Input, execute: (input, context) => Effect.gen(function* () {
      return yield* access.read(input.path);
    }) }))
  }),
}
