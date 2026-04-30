# Caching & Messaging Architectures

In high-throughput senior-level backend systems, the database cannot handle all the load, and synchronous HTTP calls often lead to cascading failures. We use Caching and Asynchronous Messaging to solve this.

## 1. Advanced Caching Strategies

### Multi-Level Caching (L1 + L2)
Using a remote cache (like Redis) still incurs network latency. A multi-level cache solves this by putting an ultra-fast local cache in front of the remote cache.
- **L1 (Local)**: Caffeine (In-memory, JVM-bound, nanosecond latency).
- **L2 (Remote)**: Redis (Distributed, millisecond latency).
- *Flow*: Application → Check Caffeine → Check Redis → Check Database.

### The Cache Stampede Problem
If a highly requested, expensive cache key expires, thousands of concurrent threads might miss the cache simultaneously and hit the database, instantly crashing it.
- **Fix (Spring Boot)**: Use `@Cacheable(sync = true)`.
- *How it works*: It locks the cache key. The first thread calculates the value and populates the cache. The other threads wait for the first thread to finish and then read from the newly populated cache.

### Eviction Policies
When the cache is full, how do we remove items?
- **LRU (Least Recently Used)**: Removes the item that hasn't been accessed for the longest time.
- **LFU (Least Frequently Used)**: Removes the item accessed the fewest times.
- **TTL (Time to Live)**: Absolute expiration (e.g., expires after 1 hour).
- **TTI (Time to Idle)**: Sliding expiration (e.g., expires if not accessed for 30 minutes).

---

## 2. Reliable Messaging (RabbitMQ)

In a distributed system, messages fail. Network glitches, database locks, or bad data can cause consumers to throw exceptions. You cannot simply discard these messages.

### The Dead-Letter Exchange (DLX) Retry Pipeline
A standard enterprise pattern for handling failures in RabbitMQ without blocking the main queue.

1. **Main Queue**: Consumer pulls a message. If processing fails (e.g., DB is down), the consumer explicitly `nacks` (negative-acknowledges) the message with `requeue=false`.
2. **Dead Letter Exchange**: The Main Queue is configured with an `x-dead-letter-exchange` routing to a **Retry Queue**.
3. **Retry Queue (TTL)**: This queue has NO consumers. It has a Time-To-Live (TTL) of, say, 5 minutes.
4. **Back to Main**: The Retry Queue has its own `x-dead-letter-exchange` pointing *back* to the Main Queue! Once the 5-minute TTL expires, the message is automatically pushed back to the Main Queue for another attempt.
5. **Poison Pill Handling**: After a certain number of retries (tracked via message headers), the consumer routes the message to a **Parking Lot Queue** for manual human intervention.

### Idempotent Consumers
Because networks can duplicate messages (at-least-once delivery), your consumer MUST be idempotent (processing the same message twice has the exact same effect as processing it once).
- **Implementation**: Store the `message_id` in a database table *within the same transaction* as your business logic. If the `message_id` already exists, discard the duplicate.
