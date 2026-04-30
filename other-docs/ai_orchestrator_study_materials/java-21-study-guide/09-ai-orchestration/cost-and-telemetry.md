# Cost Tracking, Token Telemetry & Caching

LLM bills are the surprise line item that ends careers. A poorly-architected AI orchestrator can burn six figures of vendor credit in a weekend. The senior signal is showing you've designed for **cost as a first-class concern**, alongside latency and correctness.

## 1. The Cost Equation

```
cost_per_request = (prompt_tokens × prompt_price) + (completion_tokens × completion_price)
                 - prompt_cached_tokens × discount
```

Approximate late-2025 pricing per 1M tokens (always re-check):

| Model | Prompt $/1M | Completion $/1M | Cached prompt $/1M |
| ----- | ----------- | --------------- | ------------------ |
| GPT-4o | $2.50 | $10.00 | $1.25 (50% off) |
| GPT-4o-mini | $0.15 | $0.60 | $0.075 |
| Claude 3.5 Sonnet | $3.00 | $15.00 | $0.30 (90% off, manual) |
| Claude 3.5 Haiku | $0.80 | $4.00 | $0.08 |
| Embedding (3-small) | $0.02 | n/a | n/a |

**The non-obvious math:** completion tokens cost 4-5× prompt tokens. A request with a 3K-token system prompt and a 200-token answer is *more* prompt-cost than completion-cost. Caching the system prompt collapses prompt cost by 50–90%.

## 2. Token Counting in Java

You cannot trust the model to tell you tokens before sending — you'd be sending the request to find out. Use the provider's tokenizer locally:

- **OpenAI:** [`com.knuddels:jtokkit`](https://github.com/knuddels/jtokkit) implements `cl100k_base` / `o200k_base` BPE.
- **Anthropic:** no public tokenizer; use the `count_tokens` API endpoint (it's free) or estimate at ~4 chars per token.

```java
Encoding enc = Encodings.newDefaultEncodingRegistry().getEncoding(EncodingType.O200K_BASE).orElseThrow();
int tokens = enc.countTokens(prompt);
if (tokens > tenantConfig.maxPromptTokens()) {
    throw new TokenBudgetExceededException("prompt=" + tokens + " > limit=" + tenantConfig.maxPromptTokens());
}
```

Pre-flight token checks let you reject doomed requests *before* spending API credits — particularly important for user-uploaded content where a malicious user could paste a 500K-token document.

## 3. The TokenUsageEvent Pipeline

Every LLM response includes a `usage` object: `{prompt_tokens, completion_tokens, total_tokens}`. Capture it on **every call** and publish to a usage event bus.

```java
record TokenUsageEvent(
    Instant timestamp,
    String  tenantId,
    String  userId,
    String  conversationId,
    String  model,
    int     promptTokens,
    int     completionTokens,
    int     cachedPromptTokens,
    BigDecimal estimatedCostUsd,
    String  feature       // "chat", "summarize", "embedding", "rerank"
) {}

@Service
public class LlmCallTracker {
    private final KafkaTemplate<String, TokenUsageEvent> kafka;

    public ChatResponse track(ChatModel model, Prompt prompt, RequestContext ctx) {
        ChatResponse resp = model.call(prompt);
        Usage u = resp.getMetadata().getUsage();
        kafka.send("token.usage", ctx.tenantId(), new TokenUsageEvent(
            Instant.now(), ctx.tenantId(), ctx.userId(), ctx.conversationId(),
            ctx.model(), (int) u.getPromptTokens(), (int) u.getCompletionTokens(),
            (int) u.getCachedTokens(), pricer.cost(ctx.model(), u), ctx.feature()
        ));
        return resp;
    }
}
```

Downstream consumers:
- **Aggregation** (Kafka Streams / Flink) → per-tenant daily totals → billing.
- **Real-time monitoring** → alert when a tenant crosses 80% of daily quota.
- **Cost analytics** → which feature drove yesterday's $4K spike?

**Don't write usage events directly to Postgres.** Volume is high, and the write must never block the user request. Kafka (or a similar bus) gives you decoupling and replayability for free.

## 4. Prompt Caching (The 80% Cost Saving)

LLM providers charge less for **previously-seen prompt prefixes**. Two flavors:

### Anthropic — explicit caching (90% discount)
You annotate which prompt segments to cache. Cache lifetime: 5 minutes (refreshed on hit).
```java
// Pseudocode — Anthropic Java SDK
MessageRequest req = MessageRequest.builder()
    .system(List.of(
        SystemMessage.of(longSystemPrompt).withCacheControl(CacheControl.EPHEMERAL)
    ))
    .messages(...)
    .build();
```
Use for: long system prompts, RAG context that's reused across many turns of a conversation, persona definitions.

### OpenAI — automatic caching (50% discount)
No annotation. The system caches automatically when prompt prefix > 1024 tokens and is reused within ~10 minutes.
- Cache hit = tokens count toward `prompt_tokens_cached` in the usage object.
- **The trick:** *order matters*. Put stable content (system prompt, RAG context) **first**, dynamic content (user message, recent turns) **last**. Reordering invalidates the cache.

### When caching pays off
- High-volume conversations with the same system prompt: **2–5× cost reduction**.
- One-off requests: zero benefit (no reuse window).
- RAG with frequently-rotating context: minimal benefit (cache misses dominate).

## 5. Response Caching (Semantic Cache)

Covered in detail in `agentic-patterns.md` (Day 12). Recap:
- Hash the **embedding** of the user query, not the raw string.
- On cosine similarity > ~0.95 to a cached query, return the cached response.
- Latency: 2-5s → 10ms. Cost: $0.

The caveat: **invalidation**. Cached answers tied to documents must be evicted when those documents change. Tag each cached entry with the source `document_id`s; on doc update, evict by tag.

## 6. Model Routing & Fallback Chains

Don't always use the most capable model. Pattern: **start cheap, escalate on confidence drop**.

```java
ChatResponse cheap = haikuModel.call(prompt);
if (confidenceScore(cheap) < 0.7) {
    return sonnetModel.call(prompt);   // re-do with capable model
}
return cheap;
```

Where `confidenceScore` comes from:
- Self-evaluation: ask the cheap model to rate its own confidence (noisy but cheap).
- Heuristic: short answers, hedge phrases ("I think", "possibly"), or refusal-shaped outputs trigger escalation.
- Tool-failure signals: if the cheap model picked a wrong tool, retry with the capable one.

**Provider fallback** is also a cost+resilience lever:
```
primary: Claude 3.5 Sonnet
   ↓ (on 429 / 503 / timeout)
fallback: GPT-4o
   ↓ (on cascade failure)
fallback: cached previous similar response (degraded UX)
```
Build this with Resilience4j circuit breakers (one per provider).

## 7. Per-Tenant Budgets and Throttling

You **must** enforce per-tenant limits or one customer's bug will cost you another customer's contract.

| Limit | Granularity | Enforcement point |
| ----- | ----------- | ----------------- |
| Tokens per minute | Sliding window | API gateway / sidecar |
| Tokens per day | Calendar day | After-the-fact + warn at 80%, block at 100% |
| Concurrent requests | Live count | Per-tenant Bulkhead (Resilience4j) |
| Cost per day | Computed | Aggregation layer + circuit breaker |

The implementation surface depends on tier: per-minute is rate-limit middleware (Bucket4j, Redis-backed sliding window); per-day is async (the user blocks only after the daily aggregation has updated, which is fine).

```java
// Sliding-window rate limit with Bucket4j + Redis
@Component
public class TenantTokenLimiter {
    Bucket bucket(String tenantId, long capacityPerMinute) {
        Bandwidth limit = Bandwidth.simple(capacityPerMinute, Duration.ofMinutes(1));
        return Bucket.builder().addLimit(limit).build();   // back this with Redis for HA
    }
}
```

## 8. Observability for Cost

The four dashboards every AI orchestrator needs:

1. **Spend per tenant per day** (top-N) — instantly identifies anomalies.
2. **Spend per feature** (`chat`, `summarize`, `embed`, `rerank`) — tells you which feature is the cost driver, hence the optimization target.
3. **Cache hit rate** (prompt + response) — declining hit rate = degraded efficiency, often after a system prompt change.
4. **Tokens per request distribution** (P50, P95, P99) — a P99 spike often means a bug (loop, runaway context).

Anomaly alerts: tenant spending > 3× their 7-day moving average → page on-call. Single-request token usage > $1 (configurable) → log and inspect.

## 9. Common Cost Footguns

1. **Unbounded conversation memory.** Token cost grows quadratically with conversation length. Fix: rolling summary + recent-N-turns (see `agent-memory.md`).
2. **Re-embedding on every read.** Embeddings should be computed once, stored, reused. Catastrophic if buried in a hot path.
3. **Re-ranker called on every chunk.** Re-rank only the top-K from vector search, not the entire corpus.
4. **Multi-agent runs without step caps** — see `multi-agent-patterns.md`.
5. **Streaming clients that don't propagate cancellation upstream** — user closes browser, LLM keeps generating, you keep paying. See `llm-streaming.md`.
6. **Test/staging environments without rate limits.** A bug in CI can rack up thousands in a night.
7. **Dev keys in code** — accidental commit + GitHub scrape = burned credits. Use secrets management; rotate on suspicion.

## 10. The Senior Architecture Signal

In a system design interview, when asked "how do you handle cost?", a senior answer covers:

1. **Pre-flight token check** — reject before spending.
2. **TokenUsageEvent on every call** — measure to manage.
3. **Prompt caching** for stable prefixes.
4. **Semantic response caching** for repeated queries.
5. **Model routing** — cheap default, escalate when needed.
6. **Per-tenant budgets** with quota enforcement at the gateway.
7. **Per-feature cost dashboards** to identify optimization targets.
8. **Stripe metering integration** so customers see their usage and you bill correctly.

You don't have to design all eight in 30 seconds. You have to *name* them and identify which 2-3 you'd build first.

---

## References
- [OpenAI — Pricing & token counting (`tiktoken`)](https://platform.openai.com/docs/guides/text-generation/managing-tokens)
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching)
- [Anthropic — Prompt caching guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [`jtokkit` — Java tokenizer for OpenAI models](https://github.com/knuddels/jtokkit)
- [Bucket4j — Java rate-limiting library](https://bucket4j.com/)
- [Stripe Metering API](https://stripe.com/docs/billing/subscriptions/usage-based) (when you need to bill customers per-token)
- [Helicone, Langfuse — third-party LLM observability](https://www.helicone.ai/) — useful if you don't want to build the dashboards yourself.
