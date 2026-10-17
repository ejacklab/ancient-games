import type { Transport } from "./transport";

export function send(transport: Transport, payload: string) {
  return transport.prepare(payload);
}
