import type { Transport } from "./transport";

export const httpTransport: Transport = {
  prepare(payload) { return `POST ${payload}`; },
};

export class QueueTransport implements Transport {
  prepare(payload: string) { return `ENQUEUE ${payload}`; }
}

export function fileTransport(directory: string): Transport {
  return {
    prepare(payload) { return `${directory}/${payload}`; },
  };
}
