# Day 16 — Spaced Review + Week 1 Deep-Dive

> **Timebox: ~2.5 hours.** Spaced-review pass on tagged topics (90m) → Capstone write-up iteration (30m) → Light DSA refresher (30m).
> This is a **deliberate slow day** sandwiched between Day 15's heavy mock and Day 17's coding+behavioral. Use it. Don't stack new material.

---

## 1. Spaced Review (90 min) — Touch every Week 1 topic in 90 minutes

The goal is *active recall*, not passive re-reading. Set a 10-minute timer per topic.

For each Week 1 topic, do the following without opening the syllabus:
1. **Whiteboard the structure** (memory diagram, lifecycle, etc.) on paper.
2. **Re-derive the canonical insight** (e.g. for arrays: "single-pass with hash map trades space for time").
3. **Answer the 5 recall questions from the day file.** Score yourself.
4. **Only then** open the doc to verify. Note any gaps.

| 10-min slot | Topic | Day file | Syllabus reference |
| ----------- | ----- | -------- | ------------------ |
| 0:00–0:10   | Arrays + JVM | Day 1 | [jvm-architecture.md](../../java-21-study-guide/04-jvm/jvm-architecture.md) |
| 0:10–0:20   | Linked Lists + Virtual Threads | Day 2 | [multithreading.md](../../java-21-study-guide/03-concurrency/multithreading.md) |
| 0:20–0:30   | Trees + JDBC/Hibernate | Day 3 | [jdbc.md](../../java-21-study-guide/05-ecosystem/jdbc.md) |
| 0:30–0:40   | Graphs + Spring internals | Day 4 | [spring-framework.md](../../java-21-study-guide/05-ecosystem/spring-framework.md) |
| 0:40–0:50   | Sliding Window + Microservice resilience | Day 5 | [resilience-and-patterns.md](../../java-21-study-guide/06-microservices/resilience-and-patterns.md) |
| 0:50–1:00   | OAuth + JWT | Day 6 | [oauth2-and-jwt.md](../../java-21-study-guide/07-security-and-identity/oauth2-and-jwt.md) |
| 1:00–1:10   | Multi-tenancy + RLS | Day 7 | [multi-tenancy.md](../../java-21-study-guide/07-security-and-identity/multi-tenancy.md) |
| 1:10–1:20   | Containers + JVM container flags | Day 8 | [containerization.md](../../java-21-study-guide/08-infrastructure/containerization.md) |
| 1:20–1:30   | Observability + correlation IDs | Day 9 | [observability.md](../../java-21-study-guide/08-infrastructure/observability.md) |

**Rule:** if a topic stays at <80% confidence, tag it `#weak` *again* and reschedule for Day 20.

---

## 2. Capstone Iteration (30 min)

Open your Day 15 capstone write-up. **Add or fix one weakness** identified in Day 15's self-review:
- Add the missing Mermaid diagram of async ingestion.
- Add the missing per-tenant cost-tracking section.
- Add a "trade-offs considered and rejected" section (e.g. "Why not Pinecone? Why not LlamaIndex on top of Elasticsearch?").

Don't try to perfect it. One fix per day adds up.

---

## 3. Light DSA Refresher (30 min)

Pick **two patterns from Week 1 that you nailed easily** (not weak ones). Do **one Easy** of each, *under a 10-minute timer*. The point is to keep muscle memory warm without burnout. Suggestions:
- Arrays: [Contains Duplicate (#217)](https://leetcode.com/problems/contains-duplicate/).
- Linked List: [Middle of Linked List (#876)](https://leetcode.com/problems/middle-of-the-linked-list/).
- Trees: [Same Tree (#100)](https://leetcode.com/problems/same-tree/).
- BFS: [Number of Islands (#200)](https://leetcode.com/problems/number-of-islands/) — re-do, target <8 minutes.

If a "should be easy" problem takes you >10 minutes, that's a *signal*, not a tragedy — tag the topic `#weak` and revisit Day 20.

---

## 4. Day 16 Deliverables

- [ ] Spaced-review scorecard for all 9 Week 1 topics, with `#weak` tags applied.
- [ ] One concrete improvement to the capstone write-up.
- [ ] Two warm-up Easy problems re-solved under 10m each.
- [ ] Mid-week reflection (100 words): am I ahead, on-track, or behind on the sprint? What's the one thing slipping?

## 5. References

- [Andrew C. Smith — *The spacing effect for engineers*](https://andymatuschak.org/spaced-repetition/) — a 2-minute primer on why this day matters.
- [Anki](https://apps.ankiweb.net/) — if you want to convert your `#review/...` tags into a flashcard deck for ongoing recall after the sprint.
