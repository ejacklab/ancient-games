import { Context, type Task } from "../effect-runtime";

export interface LedgerPort {
  readonly settle: () => Task<number>;
}
export class Ledger extends Context.Service<Ledger, LedgerPort>()("@app/Ledger") {}
