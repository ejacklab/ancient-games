import type { Transport } from "./transport";

export const httpTransport = (base: string): Transport => ({
  prepare: (payload) => `POST ${base} ${payload}`,
  execute: (prepared) => `sent ${prepared}`,
});
