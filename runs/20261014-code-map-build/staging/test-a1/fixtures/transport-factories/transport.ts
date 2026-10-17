export interface Transport {
  prepare(payload: string): string;
  execute(prepared: string): string;
}
