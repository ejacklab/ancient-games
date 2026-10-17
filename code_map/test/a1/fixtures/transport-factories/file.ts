import type { Transport } from "./transport";

export const fileTransport = (directory: string): Transport => {
  // The returned object is built in a nested helper.
  const build = (): Transport => ({
    prepare: (payload) => `${directory}/${payload}`,
    execute: (prepared) => `wrote ${prepared}`,
  });
  return build();
};
