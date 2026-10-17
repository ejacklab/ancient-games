export const Effect = {
  fn(_name: string) {
    return function wrap(body: (value: number) => Generator<never, number, unknown>) {
      return (value: number): number => body(value).next().value as number;
    };
  },
};
export const Service = {
  of: <T>(implementation: T): T => implementation,
};
