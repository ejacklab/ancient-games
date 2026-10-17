export function scopeEntry() { return scopeMiddle(); }
export function scopeMiddle() { return scopeEnd(); }
export function scopeEnd() { return 1; }
export function scopeUnrelated() { return 9; }
