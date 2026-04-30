# Multi-Agent Patterns (Beyond ReAct)

ReAct (covered in `agentic-patterns.md`) is one agent in a Thought-Action-Observation loop. **Multi-agent** systems decompose work across *several* specialized LLMs/prompts that hand off, supervise, or vote. This pattern is the basis of nearly every "AI assistant that does real work" in production today.

The naive instinct is to have *one* god-agent with 30 tools. It fails: the LLM picks wrong tools, hallucinates intermediate state, and becomes uncontrollable past 5 turns. **The senior insight is the same as in microservices: decompose by responsibility.**

## 1. The Four Canonical Patterns

| Pattern | Topology | Best for |
| ------- | -------- | -------- |
| **Supervisor** | Star (one orchestrator → many specialists) | Tasks with clear sub-roles (researcher, coder, reviewer) |
| **Hierarchical** | Tree of supervisors-of-supervisors | Large workflows with nested decomposition |
| **Swarm** | Peer-to-peer with dynamic handoff | Customer-support-style routing where any agent may resolve or hand off |
| **Plan-and-Execute** | Planner produces a plan; executor runs it | Long-horizon tasks where you want a checkable plan first |

## 2. Supervisor Pattern (the Default Choice)

A **supervisor agent** receives the user's request, decides which specialist to invoke, passes its output back to the user (or to the next specialist), and decides when the task is done. Specialists are pure functions: prompt + tools, no orchestration logic.

```
            ┌─────────────┐
            │ Supervisor  │ ← user message
            └──────┬──────┘
       ┌──────────┼──────────┐
       ▼          ▼          ▼
  ┌────────┐ ┌────────┐ ┌────────┐
  │Research│ │ Coder  │ │Reviewer│
  └────────┘ └────────┘ └────────┘
```

### Spring AI sketch — supervisor with three specialists

```java
@Service
public class SupervisorAgent {
    private final ChatClient chatClient;
    private final ResearchAgent research;
    private final CoderAgent    coder;
    private final ReviewerAgent reviewer;

    public String run(String userTask) {
        Map<String, Function<String, String>> registry = Map.of(
            "research", research::run,
            "code",     coder::run,
            "review",   reviewer::run
        );

        String state = userTask;
        for (int step = 0; step < 8; step++) {                     // hard cap
            SupervisorDecision d = chatClient.prompt()
                .system("You are an orchestrator. Decide which specialist to call next, " +
                        "or finish. Specialists: research, code, review. " +
                        "Respond with a JSON: {\"action\":\"finish|research|code|review\"," +
                        "\"input\":\"...\",\"reason\":\"...\"}")
                .user("Current state:\n" + state)
                .call().entity(SupervisorDecision.class);
            if ("finish".equals(d.action())) return d.input();
            String specialistOutput = registry.get(d.action()).apply(d.input());
            state += "\n[" + d.action() + "] " + specialistOutput;
        }
        throw new IllegalStateException("Supervisor exceeded step budget");
    }

    record SupervisorDecision(String action, String input, String reason) {}
}
```

**Three rules that keep this working in production:**
1. **Hard step cap** (`step < 8`). Without it, a stuck supervisor loops until you OOM your context window or your wallet.
2. **Structured output** for the supervisor's decision. Free-text "let's call research next" parses 90% of the time and fails 10% — unacceptable. Use JSON schema enforcement.
3. **Append-only state.** Each specialist's output appends to the running state. Don't try to mutate or summarize mid-run; let the supervisor decide when to compact.

## 3. Hierarchical Pattern

Same as Supervisor, but each "specialist" is itself a Supervisor with its own pool. Useful when one branch of work is itself complex.

```
                Top-level Supervisor
                ┌────────┴────────┐
            Research-Sup       Coder-Sup
            ┌─────┴─────┐      ┌────┴────┐
       Search-A  Search-B    Plan-Coder  Test-Coder
```

This is rarely worth the complexity. **Default to flat Supervisor** unless one specialist's responsibility legitimately decomposes.

## 4. Swarm Pattern (Customer-Support Style)

No supervisor. Each agent has a `handoff()` tool that transfers control to a peer. The current agent can choose to (a) handle the request, (b) call its own tools, or (c) hand off.

```
User → BillingAgent → handoff() → TechnicalSupportAgent → resolves
```

Pros:
- No central bottleneck.
- Specialists "feel" closer to a real org chart, easier for non-engineers to reason about.

Cons:
- Routing decisions are distributed; debugging "why did it end up at the wrong agent?" is harder.
- Easy to introduce **infinite handoff loops** (BillingAgent hands to Tech, Tech hands back).

Mitigations: a global handoff counter (max ~3 hops), and a "no-back-handoff" rule (you cannot hand off to the agent that just handed off to you).

OpenAI's [Swarm](https://github.com/openai/swarm) (experimental) and [Agents SDK](https://github.com/openai/openai-agents-python) are reference implementations.

## 5. Plan-and-Execute

The opposite of ReAct. Instead of think-act-think-act, generate **the entire plan upfront** as a structured artifact, then execute it deterministically. The user can review the plan before execution starts.

```java
record Plan(List<Step> steps) {}
record Step(String action, Map<String, Object> args) {}

Plan plan = chatClient.prompt()
    .system("Produce a plan as JSON. Each step is one tool call.")
    .user(userTask)
    .call().entity(Plan.class);

// (Optional) human-in-the-loop checkpoint here.

for (Step step : plan.steps()) {
    Object result = toolRegistry.invoke(step.action(), step.args());
    state.put(step.action(), result);
    if (shouldReplan(state)) plan = replan(state);     // optional adaptive variant
}
```

**Best for:** travel booking, multi-step data engineering jobs, long migrations. Tasks where the user wants to *review the plan* before any side effect.

**Worst for:** customer support, conversational tasks where the next step depends on the previous step's actual output (ReAct wins here).

## 6. Common Cross-Cutting Concerns

Every multi-agent system needs:

### 6.1 Step budgets
Per-agent and global. *Always* both.
- Per-agent: prevents one stuck specialist from burning the budget.
- Global: prevents the supervisor from looping forever.

### 6.2 Structured handoffs
The data passed between agents must be **typed**, not free-text. Use Java records / Pydantic models / JSON schemas. Free-text handoffs hallucinate.

### 6.3 Memory boundaries
Don't pass the entire conversation history to every specialist. Each specialist gets:
- Its own system prompt (its role).
- The minimal scoped input (the supervisor's last instruction).
- Its own tool set.

This keeps each call short, cheap, and focused. The supervisor maintains the global thread.

### 6.4 Observability
Tag every LLM call with `(trace_id, agent_name, step_number, parent_step_id)`. In a 10-step multi-agent run, *one* call hallucinates and the user sees a wrong answer. Without tags, finding the bad call is impossible.

### 6.5 Cost ceilings
A multi-agent run can issue 30 LLM calls. Per-request token budget is non-negotiable:
```java
if (totalTokensUsed > tenantTokenBudget) throw new TokenBudgetExceededException();
```
Without this, a single bad prompt can burn $50 in 60 seconds.

## 7. The Java/Spring AI Stack (as of late 2025)

Java's multi-agent frameworks lag Python (LangGraph, AutoGen, CrewAI). Two pragmatic paths:

1. **Roll your own with Spring AI primitives** — `ChatClient`, structured outputs (`.entity(MyType.class)`), `@Tool` registries. The Supervisor sketch above is ~50 lines; it's fine.
2. **Spring AI Alibaba's agent module** — early but evolving; production-grade by 2026 likely. Worth tracking.
3. **Polyglot** — Java for the data plane and tools, Python for the agent orchestration via LangGraph, communicating via gRPC or HTTP. Common in larger orgs where data engineers own the agent layer.

Don't pick a complex framework before you've shipped Supervisor in 50 lines and *needed* something more.

## 8. When Multi-Agent Is the Wrong Answer

✅ Genuine role decomposition (researcher ≠ coder ≠ reviewer have distinct prompts and tools).
✅ Long-horizon tasks where ReAct's flat loop loses coherence past 5 steps.
✅ Workflows that benefit from human review of a *plan* before execution.

❌ Simple tool calling. Use Spring AI `@Tool` directly.
❌ Latency-sensitive responses (each agent hop adds 1-3 seconds).
❌ "I want my agent to feel smart" — this is not a reason. Multi-agent adds debuggability cost without intelligence gain unless the decomposition is real.

---

## References
- [Anthropic — *Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents) (the canonical critique of over-engineered agent systems)
- [LangGraph — Multi-agent supervisors](https://langchain-ai.github.io/langgraph/tutorials/multi-agent/agent_supervisor/)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [Microsoft AutoGen — Conversational multi-agent framework](https://microsoft.github.io/autogen/)
- [CrewAI — Roles and crews](https://docs.crewai.com/)
- [ReAct paper — Yao et al. (2022)](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve paper — Wang et al. (2023)](https://arxiv.org/abs/2305.04091)
