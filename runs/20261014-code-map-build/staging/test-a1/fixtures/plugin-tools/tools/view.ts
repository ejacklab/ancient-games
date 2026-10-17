import { Effect } from "../../effect-runtime";
import { Schema, Tool } from "../kit";
import { checkPermission } from "../permission";
import { readFile } from "../files";

// A second reading tool: shows a file with a header.
export const Input = Schema.Struct({ path: Schema.Text, header: Schema.Text });
export const Output = Schema.Struct({ shown: Schema.Text });

export const tool = Tool.make({
  name: "view",
  input: Input,
  output: Output,
  execute: Effect.fn("ViewTool.execute")(function* (input: { path: string; header: string }) {
    const allowed = yield* checkPermission(input.path);
    const shown = yield* readFile(`${input.header}:${input.path}`);
    return { allowed, shown };
  }),
});
