import type { Transport } from "./transport";

export const queueTransport = (name: string): Transport => ({
  prepare(payload) { return `ENQUEUE ${name} ${payload}`; },
  execute(prepared) { return `queued ${prepared}`; },
});
