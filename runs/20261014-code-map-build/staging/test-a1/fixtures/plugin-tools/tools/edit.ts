import { Effect } from "../../effect-runtime";
import { Schema, Tool } from "../kit";
import { checkPermission } from "../permission";
import { writeFile } from "../files";


// A second writing tool: replaces text, at a different line offset.
export const Input = Schema.Struct({ path: Schema.Text, replacement: Schema.Text });
export const Output = Schema.Struct({ edited: Schema.Text });

export const tool = Tool.make({
  name: "edit",
  input: Input,
  output: Output,
  execute: Effect.fn("EditTool.execute")(function* (input: { path: string; replacement: string }) {
    const allowed = yield* checkPermission(input.path);
    const edited = yield* writeFile(input.path, input.replacement);
    return { allowed, edited };
  }),
});
