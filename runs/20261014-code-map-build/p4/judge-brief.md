# Brief — P4 judge: does a module map hold the known items?

You check one module map made by a code-map tool against an answer key written by a reader. The map is JSON:
`map.definitions` (each with a name, kind and location), `map.links` (calls, each with from, to, kind and
location), `map.entries` (entry functions with their steps), `map.siblings` (members and rows), and `limits`.
It is large: search it with grep or a short script (python3 or jq), do not read it whole.

## Read

- The key: KEY. Each claim has an id, a source file:line and a quote. Paths in the key start with
  `packages/<pkg>/`; paths in the map are relative to the package root.
- The map: MAP. The code, if you need it: ROOT.

## Check

For each key claim that names a definition, a call link, an entry, a test reaching a function, or a sibling
difference, decide whether the map holds it:
- **held**: the map has the item, with a location within 3 lines of the key's;
- **missed**: the map does not have it, and no limit in the map names that place;
- **limited**: the map does not have it, but a limit names that place or reason;
- **wrong**: the map has the item with a location or content that contradicts the code (check the code first);
- **n/a**: the claim is not something a map holds (for example a behaviour described in words).

Also take ten links at random from the map and check each against the code: correct or wrong.

## Return

Your final message only:
1. A table: claim id · held / missed / limited / wrong / n/a · one short note.
2. Totals per status.
3. The ten random links: link · correct or wrong · why.
