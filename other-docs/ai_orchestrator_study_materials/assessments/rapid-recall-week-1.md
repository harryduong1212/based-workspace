# Rapid Recall — Week 1 (Days 1–5)

> **Format:** punchy single-line Q&A. Read the question, **answer aloud or in your head**, then scroll to the answer. Goal: last-minute drilling, not deep study.
> **Pacing:** ~30 seconds per card. Whole file in 30–40 minutes.
> **If you miss a card:** tag the topic `#weak` in Obsidian and revisit the relevant day's syllabus.

---

## Topic: Arrays & JVM Internals (Day 1)

**Q1.** What's the time/space target for Two Sum, and why is it not just `O(n²)` brute force?
**A.** `O(n)` time, `O(n)` space using a HashMap of `value → index`. Trade space for time: at each `i`, ask "have I already seen `target - nums[i]`?".

**Q2.** Name the three JVM subsystems and one job each.
**A.** Class Loader (loads `.class` files via delegation hierarchy), Runtime Data Areas (Stack/Heap/Method Area memory), Execution Engine (interpreter + JIT).

**Q3.** What does `OutOfMemoryError: GC overhead limit exceeded` specifically mean (vs. plain `Java heap space`)?
**A.** JVM is spending >98% CPU on GC but reclaiming <2% of heap. Symptom of a leak or unbounded collection — not just "memory is full".

**Q4.** Why is the first ~30 seconds after deploy slower than steady state?
**A.** JIT tiered compilation: code starts interpreted (Tier 0), gets profiled (Tiers 1–3), eventually fully optimized by C2 (Tier 4). The "warm-up" phase.

**Q5.** What is a TLAB and what bottleneck does it eliminate?
**A.** Thread-Local Allocation Buffer — a small per-thread chunk of Eden. Lets allocation be effectively lock-free instead of contending on a shared heap pointer.

**Q6.** What is Escape Analysis, and what is its visible effect?
**A.** JIT analysis of whether an object outlives its method. If not, the object is *scalar-replaced* onto the stack — heap allocation skipped, GC skipped.

**Q7.** When would you choose GraalVM AOT (native image) over JVM JIT?
**A.** Cold-start sensitive workloads (Lambda, Cloud Run scale-to-zero), small memory footprint. Trade off: lose JIT's steady-state optimizations.

**Q8.** Best Time to Buy/Sell Stock — what's the invariant the running `maxProfit` maintains?
**A.** After processing index `i`, `maxProfit` is the best profit achievable selling at any `j ≤ i` given the running min seen so far.

---

## Topic: Linked Lists & Virtual Threads (Day 2)

**Q9.** Reverse a linked list iteratively — what's the *one* state you must save before flipping a pointer?
**A.** `next = curr.next` — otherwise you lose the rest of the list when you do `curr.next = prev`.

**Q10.** Why is `synchronized` an anti-pattern with virtual threads, but `ReentrantLock` is fine?
**A.** `synchronized` *pins* the virtual thread to its OS carrier — defeats unmounting. `ReentrantLock` allows the VT to unmount during blocking I/O inside the critical section.

**Q11.** Roughly how many platform threads can you have on a typical box, and why?
**A.** ~10K. Each platform thread has a ~1MB stack mapped 1:1 to an OS thread. Hits both memory and OS-thread limits past that.

**Q12.** What's the JVM flag to detect virtual-thread pinning in production?
**A.** `-Djdk.tracePinnedThreads=full` (or `=short`). Logs a stack each time a VT is pinned.

**Q13.** What does `StructuredTaskScope.ShutdownOnFailure` do that `CompletableFuture.allOf` doesn't?
**A.** Cancels sibling subtasks the moment one fails. Plain `allOf` waits for all, even after one has thrown.

**Q14.** A teammate says "virtual threads make my image-resize service scale better." Right or wrong?
**A.** Wrong. VTs help *blocking* workloads only. CPU-bound work still saturates cores; use `ForkJoinPool` sized to cores.

**Q15.** Merge Two Sorted Lists — what's the *one trick* that simplifies the boundary case?
**A.** Dummy head node. `dummy.next` is the real head; you append to `tail` without an `if first?` branch.

---

## Topic: Trees & Database Optimization (Day 3)

**Q16.** Maximum depth of a binary tree — write the recurrence.
**A.** `depth(node) = 1 + max(depth(left), depth(right))`. Base case: `null → 0`.

**Q17.** HikariCP optimal pool size formula?
**A.** `connections ≈ (cores × 2) + spindles`. Modern SSDs: spindles ≈ 1. Almost always 10–20, *not* hundreds.

**Q18.** What's the N+1 query problem, and name three Hibernate fixes.
**A.** Loading `N` parents then lazily loading each one's children = `N+1` queries. Fixes: `@EntityGraph` (JOIN FETCH), `@BatchSize` (IN clause batches), `@Fetch(SUBSELECT)`.

**Q19.** B-Tree left-prefix rule — composite index on `(tenant, status, created_at)`. Which queries hit it?
**A.** Hit: `WHERE tenant=X`, `WHERE tenant=X AND status=Y`. Miss: `WHERE status=Y` alone (no leading `tenant`).

**Q20.** `@Transactional(readOnly = true)` — what does it actually do under the hood?
**A.** Hibernate flush mode goes to MANUAL (no dirty checking). Postgres executes `SET TRANSACTION READ ONLY`, allowing safe routing to read replicas.

**Q21.** When would you reach for a GIN index? A BRIN index?
**A.** GIN: JSONB containment, full-text search (`tsvector`), array operations. BRIN: huge time-series tables where data is naturally ordered (tiny footprint).

**Q22.** What single Postgres clause makes index creation non-blocking on a live table?
**A.** `CREATE INDEX CONCURRENTLY ...`. Builds in the background without write-locking the table.

**Q23.** Outline the Expand-and-Contract pattern for a column rename.
**A.** (1) Add new column. (2) Deploy code that writes both, reads old. (3) Backfill data. (4) Deploy code that reads new. (5) Drop old column.

---

## Topic: Graphs & Spring Internals (Day 4)

**Q24.** Number of Islands — why mark `grid[r][c] = '0'` instead of using a `boolean[][] visited`?
**A.** Saves `O(m·n)` extra space. Trade-off: destructive to input — state aloud in interview.

**Q25.** Clone Graph — what's the bug if you register `visited.put(node, copy)` *after* recursing into neighbors?
**A.** Infinite loop on any cyclic graph: the recursion sees `node` un-cached and re-enters indefinitely.

**Q26.** Spring bean lifecycle — name the 8 phases in order.
**A.** BeanDefinition parse → BeanFactoryPostProcessor → instantiation → DI → @PostConstruct → init → BeanPostProcessor (AOP wrap) → destruction.

**Q27.** What's the `@Transactional` self-invocation trap?
**A.** Calling `this.savedToDatabase()` from another method in the same class bypasses the AOP proxy → no transaction. Same root cause as `@Async` on internal calls.

**Q28.** When does Spring use a JDK Dynamic Proxy vs CGLIB?
**A.** JDK Dynamic Proxy if the bean implements an interface (proxies the interface). CGLIB otherwise (subclasses the class). CGLIB is the default in Spring Boot.

**Q29.** Which `@Transactional` propagation level lets you persist an audit log even if the surrounding transaction rolls back?
**A.** `REQUIRES_NEW`. Suspends the outer transaction, opens a fresh independent one. Audit commits even if outer rolls back.

**Q30.** Why does `private @Transactional` *never* work?
**A.** AOP proxies (both JDK Dynamic and CGLIB) cannot intercept private methods — they can't be overridden / proxied.

---

## Topic: Sliding Window & Microservices Resilience (Day 5)

**Q31.** Sliding window template — what's the invariant after the inner `while` loop?
**A.** The window `[left, right]` is *valid* (satisfies the problem's constraint). Record the answer here.

**Q32.** Longest Substring Without Repeating Characters — how do you advance `left` when you hit a duplicate?
**A.** Jump to `lastSeen.get(char) + 1`, **never** decrement. Otherwise you'd re-process characters and lose `O(n)`.

**Q33.** Circuit breaker states — name them and what triggers each transition.
**A.** CLOSED → OPEN when failure rate exceeds threshold. OPEN → HALF-OPEN after wait duration. HALF-OPEN → CLOSED on test-call success, → OPEN on failure.

**Q34.** Bulkhead vs Circuit Breaker — what's the distinction?
**A.** Bulkhead *isolates resources* (separate thread pools per downstream); CB *stops calls* to a known-bad downstream. They compose.

**Q35.** Saga choreography vs orchestration — when would you pick orchestration?
**A.** Workflows >4 steps, complex compensation order, observability matters. Centralized state machine wins for debuggability.

**Q36.** What's the dual-write problem?
**A.** Need to write to DB *and* publish to Kafka atomically. Neither order is safe: DB-then-Kafka can lose events; Kafka-then-DB can publish events for failed writes.

**Q37.** Outbox + CDC — explain the two-step solution in one sentence each.
**A.** (1) In one DB transaction, write the entity *and* an event row to an `outbox` table. (2) Debezium tails the WAL and publishes outbox events to Kafka — guaranteed atomic with the original write.

**Q38.** Why is `@Scheduled` polling of the outbox table inferior to Debezium CDC?
**A.** Polling latency + table-scan load. Debezium reads the WAL directly — no polling, near-zero latency, no extra load on the OLTP table.

---

## Cross-cutting bonus

**Q39.** Senior signal: "show me your `O(1)` space optimization for Climbing Stairs / House Robber." What's the trick?
**A.** Drop the full `dp[]` array; keep only the last 2 values (`prev1`, `prev2`). The recurrence only depends on those two anyway.

**Q40.** A teammate: "I'll wrap this outbound HTTP call in `@Retryable(maxAttempts=5, backoff=@Backoff(delay=2000))`." What's wrong in a 4-microservice chain?
**A.** Retry storms compound: 5×5×5×5 = 625 retries possible per user request. Add jitter, cap end-to-end retry budget, distinguish retryable from unretryable failures.

---

**Score yourself:** count cards you got right within ~10s.
- 35–40: solid; spend Day-of-interview prep on scenario drills, not recall.
- 28–34: re-read the lowest-scoring topic's syllabus deep-dive.
- <28: this is normal mid-sprint; tag the misses `#weak` and re-do this file in 3 days.
