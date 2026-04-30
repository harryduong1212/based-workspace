# LLM Streaming: SSE, WebSocket, and Back-Pressure

A non-streamed LLM call returns the full response after 2–10 seconds — long enough for the user to feel like the app is broken. Streaming exposes tokens as they're generated, dropping **time-to-first-token (TTFT)** to ~300ms and *perceived* latency to near-zero. This is non-negotiable for interactive AI products.

## 1. The Three Latencies (and Which One You're Optimizing)

| Metric | What it measures | Typical target |
| ------ | ---------------- | -------------- |
| **TTFT** (time to first token) | Network + auth + LLM warmup | **< 500ms** |
| **ITL** (inter-token latency) | LLM generation throughput | < 50ms / token |
| **TTLT** (time to last token) | Total wall time | proportional to output length |

You cannot meaningfully improve TTLT — it's bounded by token count × model speed. You **can** improve TTFT (closer LLM regions, prompt caching, smaller system prompts) and you absolutely should optimize *perceived* latency by streaming.

## 2. Transport: SSE vs WebSocket

### Server-Sent Events (SSE)
- One-way: server → client.
- Built on plain HTTP/1.1 or HTTP/2; works through every proxy.
- Native browser support via `EventSource`.
- **Use for:** the standard chat-UI streaming case. **This should be the default.**

```
Content-Type: text/event-stream

data: {"delta":"Hello"}

data: {"delta":" world"}

data: [DONE]
```

### WebSocket
- Two-way, low-latency.
- Supports binary frames.
- **Use for:** voice/audio agents, collaborative editing, multi-turn streaming where the *client* also needs to push events mid-stream (e.g. user interrupts → cancel inference).

The mistake to avoid: defaulting to WebSocket "because real-time". WebSocket adds operational complexity (sticky load balancing, idle timeouts, harder observability) that SSE doesn't. Pay that cost only when you actually need bidirectional streaming.

## 3. Spring WebFlux + Virtual Threads: The Modern Pattern

Pre-Loom, you'd use Spring WebFlux's `Flux<String>` because blocking the request thread for 8 seconds while an LLM streams is unacceptable. Post-Java-21 with virtual threads, **plain Spring MVC + `SseEmitter` is competitive** — the carrier thread unmounts during the LLM read, so blocking is cheap.

### SSE with Spring MVC + virtual threads (the simpler choice for most teams)

```java
@RestController
public class ChatController {
    private final ChatModel chatModel;

    @GetMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter stream(@RequestParam String q) {
        SseEmitter emitter = new SseEmitter(60_000L);  // 60s
        Thread.startVirtualThread(() -> {
            try {
                chatModel.stream(new Prompt(q)).forEach(chunk -> {
                    try {
                        emitter.send(SseEmitter.event()
                            .data(Map.of("delta", chunk.getResult().getOutput().getContent())));
                    } catch (IOException e) {
                        // client disconnected — abort upstream cleanly
                        chunk.cancel();
                    }
                });
                emitter.send(SseEmitter.event().data("[DONE]"));
                emitter.complete();
            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        });
        return emitter;
    }
}
```

### Reactive Flux variant (if you're already on WebFlux)

```java
@GetMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<Map<String, String>>> stream(@RequestParam String q) {
    return chatModel.stream(new Prompt(q))
        .map(chunk -> ServerSentEvent.builder(
            Map.of("delta", chunk.getResult().getOutput().getContent())).build())
        .timeout(Duration.ofSeconds(60))
        .onErrorResume(e -> Flux.just(ServerSentEvent.builder(
            Map.<String, String>of("error", e.getMessage())).build()));
}
```

## 4. Back-Pressure (Where Naïve Streaming Breaks)

The bug: your LLM emits 100 tokens/sec; the client consumes 20 tokens/sec (slow network); your app buffers the gap **in memory**, unbounded. Under load, you OOM.

### Back-pressure in Reactor (`Flux`)
Reactor's reactive streams contract is back-pressure-aware **by default**. The downstream `request(n)` controls how many items the publisher emits. If your sink uses `BackpressureStrategy.BUFFER` *unbounded*, you've defeated this. Use:

```java
// Bounded buffer with overflow policy
Sinks.Many<String> sink = Sinks.many().multicast().onBackpressureBuffer(256);
// or — drop the slow consumer
Sinks.Many<String> sink = Sinks.many().multicast().directBestEffort();
```

### Back-pressure in plain SSE
`SseEmitter.send()` blocks until the buffer drains, which transitively blocks the upstream LLM consumer (no buffer growth). With virtual threads this is safe and free. **The trap:** spawning the upstream LLM read on a *separate* thread that pushes into an unbounded `LinkedBlockingQueue<String>` between threads → unbounded growth. Always use a bounded queue, and decide explicitly whether overflow blocks (apply back-pressure) or drops (lossy, but preserves liveness).

### Cancellation propagation
If the client disconnects (closed tab, mobile background), the LLM call should abort to save tokens and money.
- **Spring MVC SseEmitter:** the next `emitter.send()` after disconnect throws `IOException`. Catch it, call `chunk.cancel()` or close the LLM stream.
- **Reactor `Flux`:** subscription cancellation propagates upstream automatically — *if* the LLM client is reactive. OpenAI/Anthropic Java SDKs that use blocking `HttpClient` need an explicit `dispose()` hook.

## 5. End-of-Stream Metadata (Don't Forget Usage)

Every LLM provider emits a final event with **token counts** and **finish reason**. Your billing/cost tracker depends on this.

OpenAI streaming (with `stream_options: {include_usage: true}`):
```json
data: {"choices":[{"delta":{"content":""},"finish_reason":"stop"}], "usage":{"prompt_tokens":42,"completion_tokens":127,"total_tokens":169}}

data: [DONE]
```

Anthropic emits a `message_stop` event with usage. Both Spring AI and the official SDKs surface this — make sure your streaming handler captures the *final* chunk and publishes a `TokenUsageEvent` to your accounting pipeline. **Forgetting this is the #1 reason cost dashboards diverge from provider invoices.**

## 6. Failure Modes to Plan For

| Failure | What you see | Mitigation |
| ------- | ------------ | ---------- |
| Client disconnects mid-stream | `IOException` on `send()` | Abort upstream LLM call, log partial token count |
| Provider returns 500 mid-stream | `chunk.error` event | Send error SSE event, keep connection open or fail-fast based on UX |
| Upstream timeout | TTFT > N seconds | Circuit breaker (Resilience4j), fallback to a cheaper/faster model |
| Provider rate-limit (429) | `chunk.error` with code | Don't retry mid-stream; queue request, signal "system busy" UX |
| Network blips (TCP reset) | Partial response | If user-visible: stream a *retry* token + restart. Most don't bother and surface the error. |

## 7. Rules of Thumb

1. **Default to SSE.** Reach for WebSocket only when you need bidirectional events (voice, interruption).
2. **Always capture end-of-stream usage** — your cost tracking depends on it.
3. **Always propagate cancellation upstream** — disconnected clients shouldn't burn LLM tokens.
4. **Always bound your buffers** — between LLM and client, no unbounded queues.
5. **Java 21 + virtual threads is enough for most apps.** WebFlux only when you're already on a reactive stack or genuinely need its operators.

---

## References
- [WHATWG — *Server-Sent Events*](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [Spring docs — `SseEmitter`](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-async.html#mvc-ann-async-sse)
- [Spring AI reference — Streaming chat responses](https://docs.spring.io/spring-ai/reference/api/chatclient.html)
- [Project Reactor — Backpressure & overflow strategies](https://projectreactor.io/docs/core/release/reference/#producing.create)
- [OpenAI — Streaming + usage](https://platform.openai.com/docs/api-reference/streaming)
- [Anthropic — Streaming Messages API](https://docs.anthropic.com/en/api/messages-streaming)
