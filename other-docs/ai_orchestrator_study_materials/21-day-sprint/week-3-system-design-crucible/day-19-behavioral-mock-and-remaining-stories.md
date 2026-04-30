# Day 19 — Behavioral Mock + Remaining 4 STAR Stories

> **Timebox: ~3 hours.** Behavioral mock (45m) → Mock review (30m) → Remaining 4 STAR stories (75m) → Interviewer Q&A bank (30m).
> The interviewer Q&A bank ("questions you ask them") is the most *underprepared* part of every interview. Senior candidates lose offers by asking generic questions.

---

## 1. Behavioral Mock (45 min)

Pick **6 of the 8 must-have STAR prompts** at random. Have a friend/peer read them to you, or use a timer + your phone's voice memo to simulate. Answer each in **2 minutes max**, then immediately move to the next. No self-correction mid-mock.

The 8 prompts (you've drafted 4 on Day 17; today you'll perform-mock all 8):
1. Pushback / conflict.
2. Mentorship.
3. Failure (production incident).
4. Ambiguity.
5. Leadership across functions.
6. Hardest performance bug.
7. Tech debt vs feature trade-off.
8. Evaluating & introducing new tech.

### Mock review (30 min)

Listen back to the recordings. Score each story on the 4 dimensions:
| Dimension                | Pass / Fail | Why |
| ------------------------ | ----------- | --- |
| Under 2 minutes spoken   |             |     |
| "I" not "we"             |             |     |
| Concrete tech named      |             |     |
| Quantified results       |             |     |

Any "Fail" → schedule a rewrite for tonight's deliverables.

---

## 2. Remaining 4 STAR Stories (75 min)

Draft the **4 you didn't do on Day 17**:
5. **Leadership** — leading a cross-functional team to a deadline.
6. **Performance** — the hardest bug or perf bottleneck you've tracked down. *Senior gold.*
7. **Tech debt** — how you balance shipping features vs paying down debt.
8. **New tech evaluation** — how you evaluated and introduced a new technology (e.g. Spring AI, n8n, pgvector — perfectly aligned with the role).

Same template as Day 17. Same rules: "I" not "we", numbers in Result, ~2 minutes spoken.

### A senior trick: story reuse

A single big project can be reframed for 3-5 different prompts:
- Same Black Friday rewrite story → "Failure" (the prod incident that triggered it), "Leadership" (rallying the team), "Performance" (the latency win), "New tech" (introducing CDC).

Draft *one master narrative* per major project. Then prep "angles" — 30-second variants tilted toward each prompt. This is a force-multiplier for prep time.

---

## 3. Interviewer Q&A Bank (30 min) — *Don't skip this*

Most candidates ask "what's the team culture like?" — which signals zero. The reverse-interview is your last chance to demonstrate seniority.

Build a **bank of 10 questions** in Obsidian. Categories:

**About the role's actual technical surface (highest signal):**
- "What does the inference path look like end-to-end? Where's the current bottleneck?"
- "How do you handle multi-tenant isolation in your vector DB today?"
- "What's your evaluation/eval-set story for prompt regressions when you ship a new system prompt?"
- "Are you on Spring AI / Langchain4j / something custom? What's the migration story if you wanted to switch LLM providers?"

**About engineering culture (medium signal):**
- "What's the post-mortem process? Can you share an example of a recent one?"
- "How does the team decide what to build next? Roadmap vs bottoms-up?"
- "What's the on-call cadence and the most common page reason?"

**About the role's growth & expectation (high signal for staff candidates):**
- "What does success in this role look like at 6 months? At 18 months?"
- "What's the highest-impact piece of work the previous person in this role shipped?"
- "What's the biggest gap on the team that someone joining now could close?"

**Save 1-2 question slots for things you actually want to know.** The interviewer can tell when you're reading a script.

---

## 4. Day 19 Deliverables

- [ ] 45-min mock recorded with 6 randomized prompts.
- [ ] Story scorecard, with rewrites scheduled for failed stories.
- [ ] All 8 STAR stories drafted in Obsidian.
- [ ] Master-narrative + angle map (which projects map to which prompts).
- [ ] 10-question interviewer Q&A bank.
- [ ] Pick the *3 questions* you'd ask in a 45-min round, and the *5 questions* for a 60-min loop. Mark them.

## 5. References

- [Gayle Laakmann McDowell — *Cracking the Coding Interview* — behavioral chapter](http://www.crackingthecodinginterview.com/) (still the canonical text).
- [The Pragmatic Engineer — *Reverse-interviewing your interviewer*](https://blog.pragmaticengineer.com/reverse-interviewing/).
- [Charity Majors — *On the merits of being qualified*](https://charity.wtf/2020/12/13/on-the-merits-of-being-qualified/) (great framing for the staff/lead interview).
- [Yossi Kreinin — *I'd interview for staff this way*](https://yosefk.com/blog/) (search his archive for staff interview posts).
