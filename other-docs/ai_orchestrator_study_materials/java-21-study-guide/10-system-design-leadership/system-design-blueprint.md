# The Senior System Design Blueprint

Do not just start drawing boxes in an interview. A Senior Engineer follows a rigid methodology to handle ambiguity.

## The 5-Step System Design Blueprint

### Step 1: Requirements Clarification (3-5 mins)
Never assume. Ask clarifying questions to narrow the scope.
- **Functional**: What exactly does the system do? ("Can users upload images, or just text?", "Do we need full-text search?")
- **Non-Functional**: Scale? Latency? Consistency vs. Availability (CAP Theorem)? ("Are we prioritizing high availability (eventual consistency) or strong consistency (banking)?")

### Step 2: Back-of-the-Envelope Estimation (3-5 mins)
Show you understand scale.
- 10M Daily Active Users (DAU).
- Assume 10 requests per user per day = 100M requests / day.
- 100M / 86,400 seconds = **~1,150 QPS (Queries Per Second) average**.
- Peak QPS is usually 2x to 3x average = **~3,000 QPS**.
- Storage: 10M DAU * 1MB data per day = **10TB / day**.

### Step 3: High-Level API & Data Model (5-10 mins)
- Define the core REST/GraphQL endpoints: `POST /v1/chat/messages`
- Define the core database tables: "I'll use PostgreSQL for user profiles (ACID) and Cassandra for the chat messages (high write throughput)."

### Step 4: High-Level Architecture (10 mins)
Draw the boxes: `Client -> Load Balancer -> API Gateway -> Microservices -> Cache -> Database`.

### Step 5: Deep Dive & Trade-offs (15 mins)
The interviewer will probe specific areas. Be ready to discuss:
- **Bottlenecks**: "The DB will become a bottleneck. We'll introduce Redis as a read-through cache."
- **Single Points of Failure**: "We need multiple Availability Zones (AZs)."
- **Data Partitioning**: "We'll shard the Cassandra cluster by `tenant_id`."

---

## Fully Worked Example: Multi-Tenant AI Chatbot Platform

### 1. Requirements
- SaaS platform for 1,000 businesses (tenants). Each business uploads their own documents.
- Customers of the business chat with an AI widget on their website.
- Strong isolation: Tenant A's AI cannot leak Tenant B's data.

### 2. Key Architectural Decisions (The Deep Dive)
- **Data Isolation**: We must use Row-Level Security (RLS) in PostgreSQL for configuration data, and strictly partition the Vector Database (e.g., Pinecone namespaces or pgvector RLS) by `tenant_id`.
- **Ingestion Pipeline**: When a tenant uploads a PDF, an async worker (RabbitMQ) chunks the text, calls an embedding model, and saves to the Vector DB.
- **Query Flow**:
  1. Client sends message via WebSocket to API Gateway.
  2. Gateway routes to ChatService.
  3. ChatService generates embedding for the query.
  4. ChatService queries Vector DB **filtered by tenant_id** (CRITICAL).
  5. ChatService constructs a prompt: `System Prompt + Retrieved Context + User Query`.
  6. ChatService calls LLM (e.g., GPT-4o) using Spring AI with `stream()`.
  7. Stream is pushed back over WebSocket to the client.
- **Cost Tracking**: Every LLM call returns token usage. We must publish a `TokenUsageEvent` to Kafka/RabbitMQ, aggregated by a Billing Service to charge the tenant.
