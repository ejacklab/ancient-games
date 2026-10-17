import { work as left } from "./map/siblings/left";
import { work as right } from "./map/siblings/right";
export function enter() { return left(1) + right(2); }
