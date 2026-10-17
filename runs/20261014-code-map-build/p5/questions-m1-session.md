Q1 (where defined). Where is the SessionRunner service defined, and where is its `drain` implemented?
Q2 (where defined). Where is the maximum-steps prompt defined, and where is it applied?
Q3 (what calls X, through injected services). What calls `SessionRunner.drain`?
Q4 (what calls X). What calls `SessionStep.attempt`?
Q5 (what X calls). What does `SessionStep.attempt` call?
Q6 (call chain, down, three or more levels). From SessionExecution down to a tool's own execute function
Q7 (call chain, up, three or more levels). From `SessionRunnerRetry.policy` up to the session runner
Q8 (which tests reach X). Which tests reach `SessionRunnerRetry.policy`?
Q9 (steps and decisions of one flow). How does `SessionStep.attempt` decide its outcome after the stream ends?
Q10 (difference between siblings). How do the Retry and Continue step outcomes differ?
