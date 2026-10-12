# Your slice: context windows and effective context, by model family

1. **Advertised context windows**, from official docs: Gemini (3.x Pro and Flash), Claude (Opus and Sonnet 4.x/5.x),
   OpenAI GPT (5.x/6.x), DeepSeek, Qwen and MiniMax.
2. **Effective context: where accuracy drops before the window is full.** Look for RULER, NoLiMa, LongBench v2,
   "lost in the middle", Chroma's "context rot" and Fiction.LiveBench. Give the token length at which each model
   family's measured accuracy falls, with the benchmark's numbers.
3. **When retrieval beats loading everything into context.** Anthropic's figure is about 200K tokens (V-F8). Find
   newer figures from long-context-versus-RAG studies, 2024–2026.

These numbers are the basis for how large an index that every session reads at start may be, for each agent type.
