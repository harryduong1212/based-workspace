# Service Communication & Saga Patterns

`resilience-and-patterns.md` introduces Saga and the Outbox. This document goes deeper on **inter-service communication choices** (sync vs async, REST vs gRPC vs Kafka) and on **Saga implementation** at production scale — including the AI-orchestrator-specific variant where one of the "services" is an LLM.

## 1. The Communication Decision Matrix

| Style | Latency | Coupling | Use for |
| ----- | ------- | -------- | ------- |
| **REST/HTTP-JSON** | Low (1-50ms) | Tight (client knows endpoint shape) | Public APIs, CRUD, simple synchronous flows |
| **gRPC** | Lower (1-20ms) | Tight, but typed via .proto | High-volume internal RPC; multi-language teams |
| **Kafka events** | Async (10-1000ms) | Loose (consumers decide schema usage) | Event-sourced flows; multiple consumers; replay needs |
| **RabbitMQ** | Async (10-100ms) | Medium (queue per consumer pattern) | Task queues; per-message guarantees; classic worker pools |
| **WebSocket / SSE** | Streaming | N/A | User-facing streaming UX |

**The senior call:** there is no "best" — you pick per **flow**. A single product mixes all five. The pattern is *not* "we're an event-driven shop"; it's *"this command is sync REST because the user blocks; this side-effect is Kafka because three other services need it; this RPC is gRPC because we send 10K/s and JSON overhead matters."*

## 2. Synchronous Pitfalls

The temptation to make everything sync is real — sync code is easier to reason about. The cost: **tight coupling and cascading failures**.

### The cascading failure cliff
Service A → B → C → D, all sync. C goes down. B's threads block on the C call. A's threads block on the B call. **Now A can't even serve requests that don't need C.**

Mitigations (compose them):
- **Timeouts at every hop** (with budget propagation: if A allocates a 2s budget, B has < 2s, C has < (2s − B's overhead)).
- **Bulkheads** isolating thread pools per downstream.
- **Circuit breakers** opening before cascades start.
- **Async wherever the user doesn't actually have to wait.**

### The synchronous-fan-out fallacy
A single user request fans out to 5 sync downstreams in parallel. Latency = max of 5 (assuming parallelism). Failure rate = 1 − (1 − p)^5. With p=1% per service, the aggregate failure rate is **5%**. With 10 services it's 10%. Sync fan-out doesn't scale.

The fix is structured: fan out concurrently with a deadline, return partial results when possible, log+continue rather than fail-all. Java 21's `StructuredTaskScope` is the right primitive (see `multithreading.md`).

## 3. Async / Event-Driven Patterns

### Pub-sub via Kafka (the default for "fanout to many consumers")

```
OrderService → "order.created" → Kafka topic
                                  ├── BillingService consumes
                                  ├── InventoryService consumes
                                  ├── EmailService consumes
                                  └── AnalyticsService consumes
```

**Why Kafka and not RabbitMQ here:**
- Persistent log: new consumers can replay history.
- Native fan-out: one publish, N consumer groups.
- Compaction: ideal for "current state of entity X" tables.

### Task queues via RabbitMQ (the default for "one job, one worker")

```
EmbeddingJobProducer → RabbitMQ "embed.queue" → 10 worker pods
                                                (one of them processes each msg)
```

**Why RabbitMQ:**
- Per-message ack semantics; failed jobs go to a Dead Letter Queue (DLQ).
- Priority queues; classic worker pool ergonomics.
- Smaller operational footprint than Kafka.

A common mistake is using Kafka for what is really a task queue (single consumer, ack semantics, retry logic). Kafka can do it (with manual offset management) but it's awkward — RabbitMQ or AWS SQS is simpler for that shape.

## 4. The Saga Pattern, Redux

A Saga is a sequence of local transactions across services with **compensating transactions** for rollback. Rehearsing the canonical example: an OrderSaga for an e-commerce checkout.

```
1. OrderService.createOrder()         → if fails, abort
2. PaymentService.charge()            → if fails, OrderService.cancelOrder()
3. InventoryService.reserve()         → if fails, PaymentService.refund() + OrderService.cancelOrder()
4. ShippingService.scheduleDelivery() → if fails, InventoryService.unreserve() + ...
```

Two implementation styles, restated:

### Choreography (event-driven)
Each service listens to events and emits its own. No central coordinator.
- ✅ Decentralized, no single point of failure.
- ❌ Hard to trace the overall flow ("ping-pong"); compensation order is implicit.
- **Best for:** workflows with ≤ 4 steps and minimal compensation logic.

### Orchestration (command-driven)
A central **Saga Orchestrator** sends commands to each service and tracks the saga's state.
- ✅ Clear central state machine; easier to debug; explicit compensation order.
- ❌ Orchestrator is a bottleneck and SPOF; can become a "god service".
- **Best for:** workflows with > 4 steps, complex compensation, or human-in-the-loop steps.

For most production AI orchestrators, **default to orchestration**. The debuggability win is large.

## 5. Saga Orchestrator: Production Implementation

A production Saga Orchestrator is **not** a `for` loop. It's a state machine persisted in a database, surviving restarts, retries, and crashes.

### Saga state in Postgres

```sql
CREATE TABLE saga_instances (
    id UUID PRIMARY KEY,
    saga_type TEXT NOT NULL,
    state TEXT NOT NULL,            -- 'STARTED', 'STEP_2_PENDING', 'COMPENSATING', 'COMPLETED', 'FAILED'
    payload JSONB,                  -- the running input/output state
    current_step INT,
    completed_steps JSONB,          -- [{step:1, status:'OK'}, ...]
    started_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    next_action_at TIMESTAMPTZ      -- for retries
);
```

### Step-driver loop (one polling worker per node)

```java
@Scheduled(fixedDelay = 1000)
public void drive() {
    List<SagaInstance> due = repo.findDue(Instant.now(), 32);  // batch
    for (SagaInstance s : due) {
        executor.submit(() -> advance(s));
    }
}

void advance(SagaInstance s) {
    SagaDefinition def = definitions.get(s.sagaType());
    Step step = def.stepAt(s.currentStep());
    try {
        StepResult r = step.execute(s.payload());
        s.appendCompletedStep(r);
        s.advanceStep();
        if (s.isComplete()) s.setState("COMPLETED");
    } catch (RetryableException e) {
        s.setNextActionAt(Instant.now().plus(backoff(s)));
    } catch (Exception e) {
        s.setState("COMPENSATING");
    }
    repo.save(s);                                              // single-row UPDATE; idempotent
}
```

Three properties this pattern guarantees:

1. **Crash-safe.** If the orchestrator dies mid-step, on restart it resumes from `current_step`.
2. **Idempotent.** Each step's `execute()` must dedupe by saga ID — so a re-driven step doesn't double-effect.
3. **Auditable.** `completed_steps` is the full audit trail; users with support questions can be answered with one query.

### Compensation
On `COMPENSATING`, walk `completed_steps` in **reverse**, calling each step's `compensate(payload)`. Same crash-safety + idempotency rules apply.

## 6. The Outbox Pattern (Restated, With AI Twist)

The dual-write problem (`save to DB AND emit Kafka event` is not atomic) is solved by Outbox: write the event to an `outbox` table inside the same DB transaction, then a separate process (Debezium CDC or a Kafka Connect sink) tails the WAL and publishes events.

In an AI orchestrator, the Outbox pattern matters even more because **LLM calls are dual-write generators by nature**:
- Update conversation in DB.
- Publish `TokenUsageEvent` for billing.
- Publish `MemoryFactExtractionTask` for async memory write.

Without Outbox: any of those three could be lost on a crash. With Outbox: all three are atomic with the conversation update.

```
┌────────────┐   tx { UPDATE conversation; INSERT outbox(events) }
│ ChatService│──────────────────────────────────────────┐
└────────────┘                                          │
                                                        ▼
                                              ┌──────────────────┐
                                              │ Postgres + WAL   │
                                              └─────────┬────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────┐
                                              │ Debezium / Kafka │
                                              │     Connect      │
                                              └─────────┬────────┘
                                                        │
                              ┌─────────────────────────┼─────────────────┐
                              ▼                         ▼                 ▼
                       BillingService          MemoryWriter       AnalyticsService
```

## 7. AI-Specific Saga: The "Inference Pipeline"

A novel pattern in AI orchestrators: a Saga where one of the steps is an LLM call.

```
1. Receive document upload.
2. PARSE — extract text from PDF.
3. CHUNK — split into chunks.
4. EMBED — call embedding API.   ← external, can fail/rate-limit
5. STORE — write to vector DB.
6. INDEX — refresh search index.
7. NOTIFY — emit `document.ingested` event.
```

LLM steps add unique failure modes:
- **Rate-limit (429)** → retry with exponential backoff, but with a much longer ceiling than internal services (LLMs recover in minutes, not seconds).
- **Quota exhaustion (402-style)** → don't retry; mark the saga as failed with a billing-actionable error.
- **Timeout** → may have partially succeeded server-side. Use idempotency keys so re-tries don't double-charge.
- **Mid-stream failure** → already paid for partial output. Log token cost; consider it a sunk cost on retry.

The Saga's retry policy must distinguish these: a generic "5 retries with exponential backoff" wastes money on unretryable failures.

## 8. The "What Goes Where" Cheat Sheet for AI Systems

| Concern | Mechanism |
| ------- | --------- |
| User submits chat message | Sync HTTP (the user is waiting). |
| Token usage event | Outbox → Kafka. |
| Memory fact extraction | Outbox → Kafka → async worker. |
| Document ingestion | Saga (orchestration) — multi-step, compensable. |
| Re-embedding on doc update | Async task queue (RabbitMQ / SQS). |
| Streaming response to user | SSE (or WebSocket if bidirectional). |
| Inter-microservice low-latency RPC | gRPC if Java↔Java in scale; HTTP otherwise. |
| Cache invalidation on doc change | Event-driven (`document.updated` Kafka topic). |

## 9. Operational Concerns Senior Interviews Probe

1. **Idempotency keys everywhere.** Every command must accept one. Otherwise retries duplicate effects.
2. **Schema evolution for events.** Use a registry (Confluent Schema Registry, Apicurio). Backwards-compatible changes only; consumers may be days behind.
3. **Dead Letter Queues.** Every consumer needs a DLQ + an alert + a runbook for draining it. Most teams forget the runbook until the DLQ has 100K messages.
4. **End-to-end correlation IDs.** From user request → 5 microservices → Kafka events → another service. Every span must carry the trace context (see `observability.md`).
5. **Backpressure on async workers.** Without a cap on concurrent jobs per worker, a queue burst → thread explosion → OOM. Use a bounded executor.

---

## References
- [Chris Richardson — *Microservices Patterns* (book)](https://microservices.io/book)
- [Chris Richardson — Saga pattern](https://microservices.io/patterns/data/saga.html)
- [Chris Richardson — Transactional Outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html)
- [Confluent — *Building event-driven microservices with Kafka*](https://www.confluent.io/blog/event-driven-microservices-with-confluent-cloud-and-spring-cloud-stream/)
- [Debezium — Outbox event router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
- [gRPC vs REST trade-offs — Google Cloud blog](https://cloud.google.com/blog/products/api-management/understanding-grpc-openapi-and-rest-and-when-to-use-them)
- [Camunda / Temporal — Saga orchestration as a managed product](https://temporal.io/) (worth knowing as an alternative to building your own orchestrator)
