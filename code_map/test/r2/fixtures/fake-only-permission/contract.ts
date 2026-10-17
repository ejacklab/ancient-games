import { Context, type Task } from "../effect-runtime";

export interface Interface {
  readonly assert: (input: { readonly account: string }) => Task<boolean>;
}

export class Permission extends Context.Service<Permission, Interface>()("@app/Permission") {}
