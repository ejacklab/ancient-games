import { Effect, Service } from "../support";

const deepest = (value: number): number => {
  // lunar ledger reconciliation
  const description = "copper orchard receipt";
  return value + description.length;
};

const svc = {
  get: (value: number): number => {
    return deepest(value);
  },
};

const get = function (value: number): number {
  return svc.get(value);
};

const service = Service.of({ get });

const compute = Effect.fn("Compute")(function* (value: number) {
  return service.get(value);
});

export const submit = (value: number): number => {
  if (value < 0) return 0;
  return compute(value);
};
