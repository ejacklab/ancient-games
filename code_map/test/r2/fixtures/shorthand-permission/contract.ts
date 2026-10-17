import { Context, type Task } from "../effect-runtime";

export interface Request { readonly resource: string }

export interface Interface {
  readonly assert: (input: Request) => Task<boolean>;
  readonly ask: (prompt: string) => Task<string>;
}

export class Permission extends Context.Service<Permission, Interface>()("@app/Permission") {}
