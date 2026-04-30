# Microservices: Resilience & Distributed Patterns

When transitioning from monoliths to microservices, the network becomes your biggest enemy. You must design for failure.

## 1. Resilience Patterns (Resilience4j)

### Circuit Breaker
Prevents a service from repeatedly calling a failing downstream service, preventing resource exhaustion and cascading failures.
- **CLOSED**: Traffic flows normally. If the failure rate (e.g., 50% over 10 calls) exceeds the threshold, it trips.
- **OPEN**: All calls fail fast instantly (`CallNotPermittedException`). The downstream service is given time to recover.
- **HALF-OPEN**: After a wait duration, a limited number of test calls are permitted. If they succeed, the circuit closes. If they fail, it opens again.

### Bulkhead
Isolates resources so that a failure in one part of the system doesn't bring down the whole system (named after ship compartments).
- *Example*: ThreadPool Bulkhead allocates only 10 threads to Service A and 10 to Service B. If Service A hangs, it won't consume Service B's threads.

---

## 2. Distributed Transactions

In microservices, you cannot use standard ACID database transactions across multiple services. You must use eventually consistent patterns.

### The Saga Pattern
A sequence of local transactions where each updates data within a single service. If a local transaction fails, the Saga executes **Compensating Transactions** to undo the previous successful steps.

**Two implementation styles:**
1. **Choreography (Event-Driven)**: Services publish domain events. Other services listen and react. 
   - *Pros*: Decentralized, no single point of failure.
   - *Cons*: Hard to track the overall flow ("ping-pong" effect). Best for simple workflows (2-4 steps).
2. **Orchestration (Command-Driven)**: A central Coordinator (Orchestrator) tells participating services what local transactions to execute.
   - *Pros*: Clear central logic, easy to track state.
   - *Cons*: The orchestrator can become a god-service. Best for complex workflows.

---

## 3. The Transactional Outbox Pattern

**The Problem (Dual-Write Failure)**: 
Your service needs to save an Order to the database AND publish an "OrderCreated" event to Kafka. 
- If you save to DB, then publish to Kafka, Kafka might be down (event lost, DB updated).
- If you publish to Kafka, then save to DB, the DB might violate a constraint (event published, DB empty).

**The Solution**:
1. Within a **single database transaction**, save the Order to the `orders` table AND insert a JSON event into an `outbox` table. Because it's a single transaction, it's atomic (both succeed or both fail).
2. A separate background process (like **Debezium CDC** - Change Data Capture) constantly reads the transaction log of the database and publishes the events from the `outbox` table to Kafka with guarantees.
