# Day 17 — Coding Mock #2 + Behavioral STAR Drafting (4 of 8)

> **Timebox: ~3 hours.** Coding mock (60m, hard stop) → Mock review (30m) → Behavioral STAR drafting (75m) → Reflection (15m).
> Behavioral interviews fail more senior candidates than coding interviews. Don't underestimate this half of the day.

---

## 1. Coding Mock #2 (60 min)

Pick **two more unseen problems**, with the difficulty bar slightly higher than Day 14:
- 1 Medium that combines patterns (e.g. graph + DP, sliding window + monotonic deque).
- 1 Hard.

**Suggested problems** (don't read past the title — pick blind):
- Medium combos: [Course Schedule (#207)](https://leetcode.com/problems/course-schedule/), [Word Break (#139)](https://leetcode.com/problems/word-break/), [Decode Ways (#91)](https://leetcode.com/problems/decode-ways/), [Longest Increasing Subsequence (#300)](https://leetcode.com/problems/longest-increasing-subsequence/).
- Hard: [LRU Cache (#146)](https://leetcode.com/problems/lru-cache/), [Edit Distance (#72)](https://leetcode.com/problems/edit-distance/), [Median of Two Sorted Arrays (#4)](https://leetcode.com/problems/median-of-two-sorted-arrays/), [Sliding Window Maximum (#239)](https://leetcode.com/problems/sliding-window-maximum/).

**Mock protocol:** same as Day 14 — narrate aloud, set a hard 60m timer, state Big-O before submitting, stop at 60m.

### Mock review (30 min)

Same postmortem template as Day 14, tagged `#mock/day-17`. Compare the two postmortems side-by-side: are you making the *same* class of mistake? (e.g. always rushing to code without writing examples first; always missing one edge case category). That pattern is your **interview fingerprint** — knowing it lets you compensate consciously on Day 21.

---

## 2. Behavioral STAR Drafting (75 min)

**Read first:** [behavioral-mastery.md](../../java-21-study-guide/10-system-design-leadership/behavioral-mastery.md) — 10 minutes.

Then draft **4 of the 8 must-have stories**. Pick the ones that map *most easily* to your real experience (you'll do the harder ones on Day 19):

1. **Pushback / conflict** — disagreed with product/management on a technical call.
2. **Mentorship** — leveled up a junior dev who was struggling.
3. **Failure** — brought down production. *Heavy on the post-mortem and systemic prevention.*
4. **Ambiguity** — vague requirement → shipped product.

### STAR template — keep each story to ~2 minutes spoken

```
SITUATION (15%, ~20 sec)
   Context. Company / scale / specific problem.
   "At Company X, our legacy monolith was struggling to process 10K orders/min during peak."

TASK (10%, ~15 sec)
   Your goal. Constraint (deadline, scope).
   "As lead backend engineer, I was tasked with redesigning the checkout flow with 3 weeks until Black Friday."

ACTION (60%, ~75 sec) — USE "I" NOT "WE"
   Your specific technical decisions. Walk through 2-3 concrete actions, name the technologies.
   "I analyzed the PG locks, identified synchronous inventory deduction as the bottleneck, and decoupled it via RabbitMQ + Outbox + Debezium CDC."

RESULT (15%, ~15 sec) — QUANTIFY
   Numbers. Business impact. What you learned.
   "We handled 25K orders/min with zero deadlocks; checkout latency 2.5s → 300ms; captured $2M in additional Black Friday revenue."
```

### Drafting rules

- **One story per problem.** Don't multi-purpose a single story across 4 prompts on first draft (you can later — but draft separately first).
- **"I" not "we".** Senior interviewers are listening for ownership. Even on team projects, frame your specific actions with "I".
- **Numbers everywhere in Result.** "Latency dropped" → no. "p99 latency dropped from 850ms to 120ms" → yes.
- **Failure stories are 80% post-mortem.** The interviewer wants to know how you *prevented recurrence*, not just what broke.

---

## 3. Day 17 Deliverables

- [ ] Two-problem coding mock completed under 60m.
- [ ] Two postmortem notes tagged `#mock/day-17` + side-by-side comparison with Day 14 postmortems.
- [ ] Four STAR stories drafted (Pushback, Mentorship, Failure, Ambiguity), 2 minutes spoken-time each.
- [ ] **Speak each story aloud once**, ideally recorded. Note: any place you fumble = needs a rewrite, not a re-read.
- [ ] Reflection (100 words): what's my interview fingerprint? What's my compensation strategy?

## 4. References

- [Amazon Leadership Principles + STAR](https://www.amazon.jobs/content/en/our-workplace/leadership-principles) (the OG of structured behavioral interviews).
- [Lara Hogan — *Negotiation* and managing up (free posts)](https://larahogan.me/blog/).
- [Camille Fournier — *The Manager's Path*](https://www.oreilly.com/library/view/the-managers-path/9781491973882/) (relevant even for ICs aiming at staff/lead).
- [Gergely Orosz — *Senior Engineer Interview Guide*](https://blog.pragmaticengineer.com/preparing-for-the-senior-engineer-interview/) (free version).
