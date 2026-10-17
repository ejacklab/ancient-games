export function routeRoot() {
  routeA();
  routeShared();
}
export function routeA() { return routeShared(); }
export function routeShared() { return routeLeaf(); }
export function routeLeaf() { return routeTail(); }
export function routeTail() { return 1; }
