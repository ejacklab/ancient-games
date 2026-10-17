import { Effect } from "../../effect-runtime";
import { Schema, Tool } from "../kit";
import { checkPermission } from "../permission";
import { writeFile } from "../files";

export const Input = Schema.Struct({ path: Schema.Text, content: Schema.Text });
export const Output = Schema.Struct({ written: Schema.Text });

export const tool = Tool.make({
  name: "write",
  input: Input,
  output: Output,
  execute: Effect.fn("WriteTool.execute")(function* (input: { path: string; content: string }) {
    const allowed = yield* checkPermission(input.path);
    const written = yield* writeFile(input.path, input.content);
    return { allowed, written };
  }),
});
