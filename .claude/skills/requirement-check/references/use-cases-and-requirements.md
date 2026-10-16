# Use cases and requirements — R13

What a piece of work is built and judged against: the accepted use cases, and the requirements written where they
leave a detail unclear. Levels follow RFC 2119. The ids R13.1–R13.7 are stable: the harness requirements (R11.1 units,
R12.7 score) and the harness-guard's `register` command cite them.

**R13.1 Two lists, merged into one.** The user writes the basic use cases in one list. The AI agent writes the use
cases it suggests in a separate list. The user accepts or declines each suggestion, and the accepted list — the user's
own cases plus the suggestions the user accepted — is the one list the work is built and judged against. Its maker is
the user. A suggestion enters it only with the user's recorded decision — or, in a time-boxed run (the user gave a
time or a number of rounds), with the agent's provisional decision from the experts' advice, which the user accepts
or declines when the run ends.

**R13.2 What an accepted use case holds.** Its purpose (why it is needed), its fails-if (what makes a result wrong) and
its minimum acceptance criteria (the least that must be observed for a result to pass), each stated as an observable
outcome, never as a method. A use case missing any of the three is not accepted. This applies to the user's own cases
as well as to suggestions.

**R13.3** A result that fails an accepted use case is wrong.

**R13.4 Requirements (SHOULD exist).** A requirement is written where an accepted use case leaves a detail unclear,
and where qualities pull against each other — for example how secure and how fast — in which case it states the
target for each side, as a value or a comparison the user gives. Requirements that cut across use cases (security,
privacy, speed) SHOULD be written.

**R13.5 Who writes a requirement.** The user, or the AI agent from the vision and the accepted use cases. A suggested
requirement binds only after the user accepts it (in a time-boxed run, provisionally, as in R13.1), and an edited
requirement needs a new acceptance. Each requirement
states its purpose: the use case or vision line it serves. A requirement whose purpose cannot be named is not
accepted, including one the user asked for.

**R13.6** A result that breaks an accepted requirement is wrong, except where R13.7 applies.

**R13.7 Conflict.** When an accepted use case and an accepted requirement conflict, the use case wins. The conflict is
recorded and shown to the user, naming the use case, the requirement and the result affected; the user decides
whether the requirement is revised or the trade-off is stated in it.

Fails if: an AI suggestion is in the accepted list with no recorded decision by the user (in a time-boxed run, no
provisional decision with its reason and the experts' run folder); a provisional decision is not put to the user
when the run ends; an accepted use case lacks
its purpose, fails-if or minimum acceptance criteria; a result that fails an accepted use case is passed; a suggested
requirement binds before acceptance, or an edited one keeps its old acceptance; a requirement has no named purpose; two
qualities that pull against each other have no target for either side; a conflict between a use case and a
requirement is resolved without being recorded and shown to the user.
