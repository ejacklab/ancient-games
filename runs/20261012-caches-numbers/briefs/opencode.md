# Your slice: search versus grep by size, code-graph pay-off, rebuild cost

1. **When an agent does better with full-text/BM25, vector or hybrid search than with grep**, by corpus size (files
   or tokens). Earlier research: S-F4 (about 10M tokens) and V-F6 (Cursor, 1,000 or more files). Find more, especially
   for code repositories and for notes or memory corpora.
2. **When a code graph pays off:** repo size in files or symbols, the question types, and token or tool-call savings
   (see G-F7 for codegraph; find other tools: Aider repo map, Serena, Sourcegraph, Cursor indexing).
3. **Index build and rebuild cost:** seconds per 1K files or per MB, and the size on disk, for an FTS5 index, a vector
   index (local embedding models) and a code graph, from vendor docs or benchmarks.
