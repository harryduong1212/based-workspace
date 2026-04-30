# Agentic Patterns & Semantic Caching

Orchestrating AI is more than just RAG; it involves creating autonomous agents that can reason and execute workflows.

## 1. Agent Design: The ReAct Pattern

**ReAct = Reasoning + Acting**
Instead of just asking an LLM for an answer, you prompt the LLM to follow a strict cognitive loop. This drastically reduces hallucinations and improves complex problem-solving.

1. **Thought:** The model analyzes the current state.
2. **Action:** The model executes a specific tool (e.g., Database Query).
3. **Observation:** The system returns the result of the tool back to the model.
4. **Thought:** The model analyzes the observation...
*(Loop continues until the model determines it has the final answer)*

### Example Flow
1. **Thought:** "I need to check if we have enough stock of SKU A123."
2. **Action:** Call tool `checkStock(sku='A123')`
3. **Observation:** "Result: 0 items in stock."
4. **Thought:** "The item is out of stock. I need to notify the user and suggest an alternative."
5. **Action:** Call tool `findAlternatives(sku='A123')`

---

## 2. n8n Orchestration

While Spring Boot handles the heavy backend tools, **n8n** is brilliant for visually orchestrating the workflow of AI tasks.

### The Integration Pattern
1. **Webhook Node (n8n)**: Receives a trigger from an external system (e.g., a Zendesk ticket).
2. **HTTP Node (n8n)**: Calls your Spring Boot API to fetch structured database data.
3. **AI Agent Node (n8n)**: Processes the data and decides what to do.
4. **Wait Node (n8n)**: Halts the workflow. Sends a Slack message with a button ("Approve Refund?"). The workflow resumes only when a human clicks the webhook link in Slack (Human-in-the-loop).

---

## 3. Semantic Caching

LLM API calls are slow (2-5 seconds) and expensive. Traditional caching (exact string matching) fails because users ask the same question in different ways.

### The Solution
Instead of caching the exact text, cache the **Embedding** of the text.

1. User A asks: `"How do I reset my password?"`
2. You generate an embedding array for that string.
3. You query Redis (or pgvector) for existing embeddings. No match found.
4. You execute the expensive LLM call and cache the result, along with User A's embedding.
5. User B asks: `"I forgot my password, how to reset?"`
6. You generate the embedding. You query Redis.
7. **HIT!** The cosine similarity between User A's embedding and User B's embedding is `0.98`.
8. You return the cached answer instantly. Cost = $0. Latency = 10ms.
