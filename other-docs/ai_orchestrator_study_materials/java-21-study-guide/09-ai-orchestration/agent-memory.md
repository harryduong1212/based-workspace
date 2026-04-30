# Agent Memory: Short-Term, Long-Term, Episodic, Procedural

A stateless LLM is a goldfish: every conversation starts from zero. **Memory** is what turns an LLM into an assistant that knows your preferences, recalls last week's decisions, and learns from past mistakes. Memory in agentic systems decomposes into four tiers — confusing them is one of the most common architectural mistakes.

## 1. The Four Tiers

| Tier | What it stores | Storage tech | Read pattern |
| ---- | -------------- | ------------ | ------------ |
| **Short-term** (working memory) | Current conversation turns | LLM context window | Always — stuffed into every call |
| **Long-term** (semantic memory) | Facts about the user/world | Vector DB + relational | Retrieved by relevance |
| **Episodic** | Past conversation summaries / events | Vector DB or graph DB | Retrieved by relevance or recency |
| **Procedural** | Learned tool-use patterns / playbooks | Prompt library + few-shot examples | Injected when matching scenario |

A production agent uses all four — usually built incrementally in that order.

## 2. Short-Term Memory (the Context Window)

The conversation so far. This is the only "memory" most apps have.

### The naïve approach — and why it breaks

```java
List<Message> history = conversationStore.findByConversationId(id);
ChatResponse resp = chatModel.call(new Prompt(history));
```

This works for the first 10 turns, then breaks because:
1. **Token cost grows linearly with turn count** — turn 30 of a conversation costs 30× turn 1.
2. **Latency grows** — TTFT degrades as input grows.
3. **You hit the context window limit** — typically 128K-1M tokens, depending on the model. Long-running conversations *will* exceed this.

### Sliding window
Keep only the last N turns. Loses old context, but predictable cost.
```java
List<Message> recent = history.stream().skip(Math.max(0, history.size() - 20)).toList();
```
Use when context older than a few minutes is genuinely irrelevant (most chat-style apps).

### Rolling summary + recent turns (the production pattern)
Periodically (every 10 turns, or when input exceeds a threshold), have the LLM **summarize** the older turns into a paragraph, replace those turns with the summary, keep the recent N turns verbatim.

```
[summary so far]: User is troubleshooting a production deployment;
                  has shared logs showing OOM errors; ruled out memory leaks.
[turn N-3]: ...
[turn N-2]: ...
[turn N-1]: ...
[turn N  ]: <new user message>
```

The summary itself is a prompt:
```java
String summarize = """
    Summarize this conversation. Preserve:
    - The user's stated goals and constraints
    - Any decisions or conclusions reached
    - Key facts (names, numbers, identifiers)
    Drop:
    - Pleasantries
    - Verbatim text that was already summarized in earlier checkpoints
    
    Conversation: {{turns}}
    """;
```

Rules of thumb:
- Summarize at ~70% of context window, not 95% (leave headroom for the response).
- Re-summarize the *whole history* periodically, not just the new turns — otherwise summaries-of-summaries decay quickly.
- Store the original turns separately for audit/debugging — never throw them away.

## 3. Long-Term Memory (Facts About the User)

Persistent knowledge that survives across conversations: the user's name, preferences, integrations, prior decisions.

### What goes here
- *"User prefers metric units."*
- *"User's primary work email is alice@acme.com."*
- *"User runs a Java 21 + Spring Boot 3 stack."*

### What does NOT go here
- The full conversation history (too noisy).
- Anything personal the user didn't explicitly choose to remember (consent boundary — see Section 7).

### Storage shape

```sql
CREATE TABLE memory_facts (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    content TEXT NOT NULL,                  -- "User prefers Markdown over HTML in summaries"
    embedding vector(1536),
    source_type TEXT,                       -- 'user-stated', 'inferred', 'admin'
    source_conversation_id UUID,
    created_at TIMESTAMPTZ NOT NULL,
    last_accessed_at TIMESTAMPTZ,
    confidence REAL                         -- 0.0–1.0
);

CREATE INDEX ON memory_facts (user_id, tenant_id);
CREATE INDEX ON memory_facts USING hnsw (embedding vector_cosine_ops);
```

### Write path — extract facts from conversations
```java
String extractor = """
    From the conversation below, extract facts about the user that should be remembered
    long-term. Output JSON: [{"fact": "...", "confidence": 0.0-1.0}].
    
    Only include facts that are:
    - Explicitly stated by the user (high confidence)
    - About the user's preferences, identity, environment, or goals
    - Likely useful in future conversations
    
    Skip transient task details.
    """;
```
Run async, after each conversation. **Do not** run on every turn — too expensive, too noisy.

### Read path — retrieve relevant facts
At conversation start, embed the user's first message, vector-search the user's `memory_facts`, inject the top 3-5 into the system prompt as "things you know about this user".

### Conflict resolution
Two facts can disagree (*"User prefers Python"* vs *"User just switched to Rust"*). Strategies:
- **Recency-weighted retrieval** — multiply similarity score by `0.95^age_in_weeks`.
- **Explicit conflict resolution prompt** — ask a cheap LLM to merge contradictions periodically.
- **Confidence decay** — facts not re-accessed for N weeks get confidence-decayed; below threshold, archived.

## 4. Episodic Memory (Past Conversation Summaries)

The summary of *what happened* in past conversations, retrievable by topic.

### Use case
User: *"What did we decide about the auth migration last week?"*
Without episodic memory, the agent has no idea. With it: vector-search the user's past conversation summaries by query, inject the top 1-2 as context.

### Schema
```sql
CREATE TABLE conversation_summaries (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    conversation_id UUID NOT NULL,
    summary TEXT NOT NULL,
    embedding vector(1536),
    started_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    metadata JSONB
);
```

The summary is the same artifact you produce in Section 2 (rolling summary), persisted at conversation end.

### Graph-DB variant
For agent systems where past conversations form a *web of references* (decisions linked to people linked to projects), a graph DB (Neo4j, Memgraph) outperforms a flat vector DB. The retrieval becomes a graph traversal: "find all conversations involving Alice that mentioned the auth project".

This is over-engineering for most products. Default to vector DB; switch to graph only when query patterns demand it.

## 5. Procedural Memory (Learned Playbooks)

How the agent does *kinds* of tasks. The agent improves over time at, say, "writing a PR description" by accumulating few-shot examples of good outputs and injecting them when a similar task arises.

### Storage
A library of `(scenario, prompt_template, example_outputs[])` triples. Curated, not auto-extracted (auto-extracted procedural memory drifts toward the mediocre median).

### Read path
On a new task, classify the scenario (a small classifier LLM call), pull the matching playbook, inject as part of the system prompt.

```java
record Playbook(String scenario, String systemAddendum, List<String> fewShotExamples) {}

String classify = "Classify this user task into one of: " + scenarios + ". Just the label.";
String label = chatModel.call(classify + userTask);
Playbook pb = playbookStore.find(label);
String finalSystem = baseSystemPrompt + "\n\n" + pb.systemAddendum() +
                     "\n\nExamples:\n" + String.join("\n---\n", pb.fewShotExamples());
```

This is the slowest-evolving memory tier. It's where you encode your *team's* expertise into the agent.

## 6. Putting It All Together

A typical chat turn flow:
```
1. User message arrives.
2. Embed it.
3. Read short-term: load conversation history (apply rolling summary if oversized).
4. Read long-term: vector-search user's memory_facts.
5. Read episodic: vector-search conversation_summaries (only if query implies historical reference).
6. Read procedural: classify task, load matching playbook.
7. Assemble prompt:
   [system: baseSystem + playbook + factsAbout(user) + recentEpisode]
   [history: rolling summary + recent N turns]
   [user: new message]
8. Call LLM, stream response.
9. (Async) After response: extract new facts → memory_facts.
10. (Async) On conversation end: produce summary → conversation_summaries.
```

Steps 3-6 are concurrent (`StructuredTaskScope.ShutdownOnFailure` is the right Java 21 primitive — see `multithreading.md`).

## 7. Privacy, Consent, and the Right to Forget

**Memory amplifies the privacy stakes.** A user agreeing to chat does not, by default, agree to be remembered.

Design rules:

1. **Tell the user what you remember.** A "memories" pane where they can see and delete. Apple/OpenAI/Anthropic all do this.
2. **Don't infer sensitive attributes** (race, religion, political views, health) into long-term memory, even if mentioned in passing.
3. **Right to deletion.** A `DELETE /v1/users/{id}/memory` endpoint that purges *all* memory tiers must be built early — retrofitting is hard.
4. **Tenant-scope every fact.** If a user uses your product across two tenants, the tenants must not share memory unless explicitly granted.
5. **Audit trail.** Every memory write should record provenance (which conversation, which turn). Mandatory for GDPR/CCPA compliance.

## 8. Where Memory Goes Wrong (Real Failure Modes)

- **Stale-fact poisoning.** A user joked once *"My favorite color is blue"* — a year later, the agent injects this into every prompt. Solution: confidence decay + relevance filtering.
- **Cross-conversation leakage.** Memory written during conversation A leaks into conversation B from a different user, due to a missing user_id filter. **Cross-user integration test required.**
- **Context-window starvation.** Memory injection is so verbose it crowds out the actual conversation. Cap injected memory to ~10% of context budget.
- **Conflict-driven confusion.** Two contradictory facts both retrieved → model gets confused → degraded answer. Solution: conflict resolution at write time, not read time.
- **Token cost explosion.** Memory retrieval feels free until you measure it: 5 vector queries + N facts injected = 30% of per-turn cost. Budget accordingly.

---

## References
- [OpenAI — *Memory* feature design](https://help.openai.com/en/articles/8590148-memory-faq)
- [Anthropic — *Building Claude with memory*](https://www.anthropic.com/news/memory)
- [LangGraph — Memory primitives](https://langchain-ai.github.io/langgraph/concepts/memory/)
- [MemGPT paper — Packer et al. (2023)](https://arxiv.org/abs/2310.08560)
- [LangChain — Conversational memory patterns](https://python.langchain.com/docs/how_to/chatbots_memory/)
- [GDPR Art. 17 — Right to erasure](https://gdpr-info.eu/art-17-gdpr/) (relevant when designing the deletion API)
