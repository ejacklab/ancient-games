export interface MissingService {
  missing(): number;
}
export function useMissing(service: MissingService) {
  return service.missing();
}
