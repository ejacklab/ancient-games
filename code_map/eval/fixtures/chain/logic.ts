export function start() { return middle(); }
export function middle() { return leaf() + leaf(); }
export function leaf() { return 1; }
export function recursive() { return recursive(); }
export function dynamic(fn: () => number) { return fn(); }
export function external() { return Math.random(); }
