export function routeRoot() { return 1; }
export function routeA() { return routeRoot(); }
export function routeShared() { routeA(); return routeRoot(); }
export function routeLeaf() { return routeShared(); }
export function routeTail() { return routeLeaf(); }
