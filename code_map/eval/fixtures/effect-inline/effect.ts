export declare const Effect: {
  gen<T>(body: () => Generator<never, T, unknown>): T;
  fn(title: string): <T>(body: () => Generator<never, T, unknown>) => () => T;
};
