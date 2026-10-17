import { Effect, FileAccess, Permission, Schema, type Context } from "../kit";

export const name = "write"
export const Input = Schema.Struct({ path: Schema.Text, content: Schema.Text })
export const Plugin = {
  id: "app.tool.write",
  effect: Effect.fn("WriteTool.Plugin")(function* (ctx: Context) {
    const access = yield* FileAccess.Service
    const permission = yield* Permission.Service
    yield* ctx.tool.transform((editor) => editor.add({ name, input: Input, execute: (input, context) => Effect.gen(function* () {
      yield* permission.assert(input.path, context.session);
      return yield* access.write(input.path, input.content);
    }) }))
  }),
}
