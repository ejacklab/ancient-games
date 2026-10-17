import { dispatchTicket } from "./module/workflow";

export function receiveTicket(ticket: string) {
  return dispatchTicket(ticket);
}
