Q1 (where defined). Where is the permission rule evaluation defined, and what happens when no rule matches?
Q2 (where defined). Where is the Permission service (ask, assert, reply) declared and implemented?
Q3 (what calls X, through injected services). What calls `Permission.assert`?
Q4 (what calls X). What calls the tool runtime's `execute` (`tool/runtime.ts`)?
Q5 (what X calls). What does `Permission.assert` call?
Q6 (call chain, down, three or more levels). From the write tool down to agent resolution
Q7 (call chain, up, three or more levels). From `Permission.assert` in the write tool up to the session step
Q8 (which tests reach X). Which tests reach `Permission.reply`?
Q9 (steps and decisions of one flow). What does `Permission.reply` do?
Q10 (difference between siblings). How do the read and write tools differ in their permission checks?
