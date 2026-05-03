# Project Reactor & Spring WebFlux

Spring WebFlux + Project Reactor were the canonical answer to "how do you scale a Java service to thousands of concurrent connections?" before Java 21. **Virtual threads changed the calculus.** This doc covers Reactor's primitives, the bugs they catch (and create), and — critically — the honest 2025 answer to *when WebFlux is still worth it*.

If you're starting a new service in 2025 with no prior reactive code, your default should be **plain Spring MVC + virtual threads**. WebFlux earns its complexity in three specific scenarios called out in §7.

---

## 1. The Two Primitives

### `Mono<T>` — 0 or 1 element
A computation that *eventually* produces one value, errors, or is empty.
```java
Mono<User> user = userRepo.findById(id);                       // 0 or 1
Mono<Void> ack  = saveAndPublish(user);                        // 0 (signal-only)
```

### `Flux<T>` — 0 to N elements
A stream of values over time.
```java
Flux<Order> orders = orderRepo.findByStatus("OPEN");            // batch
Flux<String> tokens = chatModel.stream(prompt);                 // streaming
```

Both are **publishers** in the Reactive Streams sense. Nothing happens until something subscribes. This is the most-violated rule by Java engineers new to reactive.

```java
Mono<User> mono = userRepo.findById(id);   // ← does NOTHING. No HTTP call yet.
mono.subscribe(System.out::println);       // ← NOW the call fires.
```

In Spring WebFlux, the framework subscribes for you when you return `Mono`/`Flux` from a controller. Outside controllers, **forgetting `subscribe()` is the most common silent reactive bug.**

---

## 2. The Pipeline Operators You'll Use Daily

| Operator | What it does |
| -------- | ------------ |
| `map(fn)` | Transform each element synchronously |
| `flatMap(fn)` | Transform each element into a Mono/Flux and merge — the **async chain** operator |
| `filter(p)` | Drop elements not matching |
| `zip(a, b)` | Combine two publishers' results into a tuple |
| `concatMap(fn)` | Like flatMap but **preserves order** (sequential) |
| `switchMap(fn)` | Cancel previous inner publisher when new outer arrives |
| `onErrorResume(fn)` | Recover with an alternative publisher on error |
| `retryWhen(spec)` | Retry on error with backoff/jitter |
| `timeout(duration)` | Error if no signal in time |
| `cache()` / `replay()` | Multicast the result to multiple subscribers |

### The `flatMap` rule

If your transformation returns `Mono<T>`, use `flatMap` (not `map`). Otherwise you get `Mono<Mono<T>>` — a double-wrapped publisher that almost always indicates a bug.

```java
Mono<Order> result = orderRepo.findById(id)
    .flatMap(order -> chargeService.charge(order))    // returns Mono<Receipt>
    .flatMap(receipt -> orderRepo.markPaid(id))       // returns Mono<Order>
    .timeout(Duration.ofSeconds(5))
    .onErrorResume(TimeoutException.class, e -> orderRepo.markPending(id));
```

This is the closest reactive comes to a "linear procedural" feel — read it as: *find → charge → mark paid, with a 5s budget and a timeout fallback*.

---

## 3. Hot vs Cold Publishers

A **cold** publisher restarts work for each subscriber. `Mono.fromCallable(() -> dbCall())` makes a fresh DB call per subscriber. Default in Reactor.

A **hot** publisher emits to all current subscribers, regardless of when they subscribed. Examples: `Sinks.Many.multicast()`, broker subscriptions, server-sent event streams.

**The bug to watch for:** treating a hot publisher as cold. If you `.cache()` a hot publisher, late subscribers may see stale or nothing. If you forget `.cache()` on a cold publisher used by multiple subscribers, you re-execute the source N times.

```java
// Cold — each subscriber triggers a fresh HTTP call
Mono<Quote> live = webClient.get().uri("/quote/AAPL").retrieve().bodyToMono(Quote.class);

// Cache the result for ALL subscribers (still cold, but result is shared)
Mono<Quote> shared = live.cache(Duration.ofSeconds(5));

// Hot — emits live ticks to all current subscribers
Sinks.Many<Tick> ticks = Sinks.many().multicast().onBackpressureBuffer(1024);
Flux<Tick> tickStream = ticks.asFlux();
```

---

## 4. Back-Pressure (Reactor's Real Selling Point)

This is what Reactor gives you that virtual threads alone don't: **the contract that the consumer signals demand to the producer.**

```java
upstream
    .onBackpressureBuffer(256, BufferOverflowStrategy.DROP_OLDEST)
    .subscribe(slowConsumer);
```

If `slowConsumer` falls behind, the buffer fills. At 256 items, *the oldest are dropped*. Alternatives:

| Strategy | Behavior |
| -------- | -------- |
| `onBackpressureBuffer(n)` | Buffer up to `n`; error on overflow |
| `onBackpressureBuffer(n, DROP_OLDEST)` | Drop oldest when full (lossy, preserves liveness) |
| `onBackpressureBuffer(n, DROP_LATEST)` | Drop new arrivals when full |
| `onBackpressureDrop()` | Drop new arrivals immediately when consumer signals no demand |
| `onBackpressureLatest()` | Keep only the latest, drop intermediate |
| (default in many ops) | Unbounded buffer — **the OOM default** |

The default of "unbounded buffer" is what bites teams that adopt Reactor without thinking about back-pressure. **Always pick a bounded strategy explicitly at the boundaries** between fast producers and slow consumers (LLM stream → SSE client; Kafka topic → DB writer; etc.).

---

## 5. WebFlux Controller Patterns

### Reactive REST endpoint
```java
@GetMapping("/users/{id}")
public Mono<User> get(@PathVariable UUID id) {
    return userRepo.findById(id)
        .switchIfEmpty(Mono.error(new NotFoundException(id)));
}
```

### Streaming SSE
```java
@GetMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<String>> chat(@RequestParam String q) {
    return chatModel.stream(new Prompt(q))
        .map(chunk -> ServerSentEvent.builder(chunk.text()).build())
        .timeout(Duration.ofSeconds(60))
        .onErrorResume(e -> Flux.just(ServerSentEvent.builder("error: " + e.getMessage()).build()));
}
```

### Aggregating concurrent calls (the place WebFlux still shines)
```java
@GetMapping("/dashboard")
public Mono<Dashboard> dashboard(@PathVariable UUID userId) {
    Mono<User>           user    = userClient.get(userId);
    Mono<List<Order>>    orders  = orderClient.recent(userId);
    Mono<Subscription>   sub     = billingClient.current(userId);

    return Mono.zip(user, orders, sub)
        .map(t -> new Dashboard(t.getT1(), t.getT2(), t.getT3()))
        .timeout(Duration.ofSeconds(2));        // budget for the whole fan-out
}
```

Three independent HTTP calls, fanned out concurrently, with a single timeout budget. Cleaner than `CompletableFuture.allOf` and still concise with virtual threads + `StructuredTaskScope`.

---

## 6. The Common Bugs

### 6.1 Calling `.block()` on a non-blocking thread
WebFlux's event-loop threads are precious. Calling `.block()` on one of them (usually a Netty event loop) will throw or, worse, hang.

```java
// Inside a @GetMapping handler — DO NOT do this
public Mono<String> handler() {
    return Mono.just(blockingCall.block());     // crashes / hangs the event loop
}
```

This bug is *easier to make than it looks* — any sync code path you forgot to convert can introduce it. Reactor 3.6+ adds a `BlockHound` check that throws on detection; enable it in dev/test.

### 6.2 Forgetting `subscribe()` outside controllers

```java
// Background task — does NOTHING
@Scheduled(fixedDelay = 60_000)
public void refresh() {
    cacheRepo.warmCache();         // returns Mono<Void> but you never subscribe
}
```

The fix is to either subscribe explicitly or change to a synchronous return. Use `Mono.fromRunnable(...)` + `.subscribe()` with a logging consumer for fire-and-forget.

### 6.3 Lost MDC (correlation IDs) across thread boundaries

Reactor moves work between threads silently. Logback's MDC is ThreadLocal — so by default, your correlation ID disappears across an `flatMap`. Solution: use Micrometer Tracing's Reactor instrumentation, which propagates a `ContextSnapshot` across operator boundaries. Without it, distributed tracing breaks intermittently in WebFlux apps.

### 6.4 Hot publishers leaking memory
A `Sinks.Many` with no consumer accumulates messages indefinitely (depending on the strategy). Long-lived hot publishers must have explicit `dispose()` paths and bounded backpressure.

### 6.5 `Mono.fromCallable(blocking)` on the wrong scheduler
By default, the callable runs on the *subscribing* thread. For blocking code, route it to the bounded-elastic scheduler:

```java
Mono.fromCallable(() -> jdbc.query(...))
    .subscribeOn(Schedulers.boundedElastic());
```

In a virtual-thread world this matters less — but if you're on WebFlux for the operator chain alone, you still need this.

---

## 7. WebFlux vs. Plain MVC + Virtual Threads (the honest 2025 take)

For most new services, **plain Spring MVC + virtual threads is now the correct default.** The carrier thread unmounts during blocking I/O, so the per-request thread cost is negligible — eliminating WebFlux's main historical advantage.

WebFlux still earns its complexity in three specific cases:

### 7.1 Server-streamed SSE/WebSocket with operator-rich pipelines
When the response is a stream of events with complex transformations (filter, throttle, debounce, retry-with-jitter), Reactor's operator vocabulary is hard to beat. Virtual threads + a hand-coded loop work but read worse.

### 7.2 Non-trivial async composition
Fan-outs with timeouts, retries, and error fallbacks (the dashboard example in §5). Virtual threads + `StructuredTaskScope` cover the basics; Reactor's `zip` + `timeout` + `retryWhen(Retry.backoff(...).filter(...))` covers the *complicated* basics.

### 7.3 You're consuming reactive APIs anyway
If your downstream is a reactive Kafka client, R2DBC, Spring Cloud Stream, or a vendor SDK that's reactive, fighting the reactive style upstream while staying reactive downstream is wasted effort. Stay in one paradigm.

### When NOT to use WebFlux

- **Simple CRUD service** — virtual threads + Spring Data JPA is shorter, easier to debug, plenty fast.
- **Team unfamiliar with reactive** — the cognitive cost is real. Wrong-thread `block()` bugs and lost MDCs eat months of senior time.
- **Heavy use of ThreadLocal-based libraries** — anything from Spring Security's old SecurityContextHolder to Hibernate's Session uses ThreadLocal in ways Reactor crosses. Workarounds exist but the friction is constant.

A common middle ground: use `WebClient` (the reactive HTTP client) inside a *synchronous* controller running on virtual threads. You get a great HTTP client without the full reactive commitment — call `.block()` on `WebClient` results because the calling thread is virtual and unmounts cheaply.

---

## 8. Reactor for AI Orchestrator Workloads

Concrete fit assessment for the role's typical workloads:

| Workload | Reactor / WebFlux fit |
| -------- | --------------------- |
| LLM streaming response to the client | **Strong** if you also use Reactor's operators (debounce, retry); SSE works with plain MVC + virtual threads if not. |
| Vector search + LLM call composition | Mediocre — virtual threads + `StructuredTaskScope` is simpler. |
| Webhook handler ingesting and emitting Kafka | If your Kafka client is reactive, yes. If it's plain, virtual threads. |
| Background embedding worker | No — use plain JDBC/JPA + virtual threads. |
| Multi-stage Saga orchestrator | No — explicit state machine in Postgres beats reactive composition for debuggability. |

The more your code looks like *deterministic procedural pipelines that block on I/O*, the more virtual threads win. The more your code looks like *event streams with operators*, the more Reactor wins.

---

## 9. Testing Reactor Code

`StepVerifier` is non-negotiable.

```java
StepVerifier.create(userRepo.findById(id))
    .expectNextMatches(u -> u.email().equals("a@b.com"))
    .verifyComplete();

StepVerifier.create(emptyMono)
    .verifyComplete();      // expects only completion, no values

StepVerifier.create(failingMono)
    .verifyError(IllegalStateException.class);
```

For time-based operators (`timeout`, `delay`, `interval`), use `StepVerifier.withVirtualTime(() -> ...)` to advance simulated time without `Thread.sleep`.

---

## 10. Quick Reference

```java
// Convert blocking to reactive
Mono.fromCallable(() -> blockingCall())
    .subscribeOn(Schedulers.boundedElastic());

// Concurrent fan-out with timeout
Mono.zip(svcA.call(), svcB.call(), svcC.call())
    .timeout(Duration.ofSeconds(2));

// Retry with exponential backoff + jitter
.retryWhen(Retry.backoff(3, Duration.ofMillis(200))
    .jitter(0.5)
    .filter(IOException.class::isInstance));

// Error recovery
.onErrorResume(NotFoundException.class, e -> Mono.just(defaultUser));

// Bounded back-pressure
.onBackpressureBuffer(256, BufferOverflowStrategy.DROP_OLDEST);

// Cache result for late subscribers
.cache(Duration.ofSeconds(30));
```

---

## References
- [Project Reactor reference](https://projectreactor.io/docs/core/release/reference/)
- [Reactor in Spring Framework — WebFlux](https://docs.spring.io/spring-framework/reference/web-reactive.html)
- [Reactive Streams spec](https://www.reactive-streams.org/)
- [Simon Baslé — *Reactor Operators by Example*](https://spring.io/blog/2019/03/06/flight-of-the-flux-1-assembly-vs-subscription)
- [Inside Java — *Virtual Threads or Reactive: How to Choose?*](https://inside.java/2023/04/13/podcast-029/)
- Companion reads: [llm-streaming.md](../09-ai-orchestration/llm-streaming.md) (Reactor-vs-MVC for LLM streaming specifically), [multithreading.md](../03-concurrency/multithreading.md) (the virtual-thread alternative).
