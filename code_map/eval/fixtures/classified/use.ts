import { calculate as leftCalculation } from "./implementations/left";
import { calculate as rightCalculation } from "./implementations/right";
export function useCalculations() { return leftCalculation(2) + rightCalculation(3); }
