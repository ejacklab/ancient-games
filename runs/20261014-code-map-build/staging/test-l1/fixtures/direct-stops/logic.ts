export function entry(value: number): number { return middle(value); }
export function middle(value: number): number { return leaf(value); }
export function leaf(value: number): number { return value + 1; }

export function loopA(value: number): number { return loopB(value); }
export function loopB(value: number): number { return loopA(value); }

export function isolated(): number { return 9; }
