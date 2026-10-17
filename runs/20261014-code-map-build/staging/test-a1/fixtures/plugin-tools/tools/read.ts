import { Effect } from "../../effect-runtime";
import { Schema, Tool } from "../kit";
import { checkPermission } from "../permission";
import { readFile } from "../files";

export const Input = Schema.Struct({ path: Schema.Text });
export const Output = Schema.Struct({ content: Schema.Text });

export const tool = Tool.make({
  name: "read",
  input: Input,
  output: Output,
  execute: Effect.fn("ReadTool.execute")(function* (input: { path: string }) {
    const allowed = yield* checkPermission(input.path);
    const content = yield* readFile(input.path);
    return { allowed, content };
  }),
});
