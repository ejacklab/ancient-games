import { Context, type Task } from "../effect-runtime";

export interface SettlementPort {
  readonly settle: (amount: number) => Task<number>;
}
export class Settlement extends Context.Service<Settlement, SettlementPort>()("@app/Settlement") {}

export interface ReceiptPort {
  readonly fetchReceipt: () => Task<string>;
}
export class Receipt extends Context.Service<Receipt, ReceiptPort>()("@app/Receipt") {}
