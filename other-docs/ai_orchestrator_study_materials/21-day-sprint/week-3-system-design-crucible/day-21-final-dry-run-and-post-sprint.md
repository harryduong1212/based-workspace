# Day 21 — Final Dry-Run + Post-Sprint Plan

> **Timebox: ~3 hours.** Full mock loop (2h) → Debrief (45m) → Post-sprint plan finalization (15m).
> Today simulates a real onsite back-to-back. Then you stop. Real interviews start tomorrow.

---

## 1. The Full Mock Loop (2 hours, all in one sitting)

Replicate a senior interview onsite. **No breaks longer than 5 minutes between rounds.**

| Slot         | Round                        | Duration |
| ------------ | ---------------------------- | -------- |
| 0:00 – 0:45  | Coding (1 Medium + 1 Hard)   | 45 min   |
| 0:45 – 0:50  | 5-min reset                  |          |
| 0:50 – 1:35  | System design                | 45 min   |
| 1:35 – 1:40  | 5-min reset                  |          |
| 1:40 – 2:00  | Behavioral (3 prompts × ~6m) | 20 min   |

**Coding round:** Pick problems blind from a category you haven't drilled today. Recommended: one combo Medium ([Word Break #139](https://leetcode.com/problems/word-break/), [Daily Temperatures #739](https://leetcode.com/problems/daily-temperatures/), [Course Schedule #207](https://leetcode.com/problems/course-schedule/)) + one Hard you haven't seen ([LRU Cache #146](https://leetcode.com/problems/lru-cache/), [Trapping Rain Water #42](https://leetcode.com/problems/trapping-rain-water/)).

**System design round:** Use a **third** prompt — neither Day 15's chatbot nor Day 18's enterprise search. Suggested: *"Design a real-time AI agent that watches a user's calendar, email, and Slack, and proactively suggests actions ('reply to this email', 'reschedule this meeting'). Privacy and consent are first-class."* This forces you to think about: consent gates, async event ingestion, ranking proactive suggestions, human-in-the-loop, false-positive cost.

**Behavioral round:** 3 random STAR prompts from your bank, 6 minutes each (longer than 2-minute story format, because the interviewer asks follow-ups).

---

## 2. Debrief (45 min) — *the most valuable part of the entire sprint*

Watch / listen to your recordings. Open Obsidian.

### For coding
- **Time-to-first-line-of-code:** how many minutes did you spend understanding the problem before typing? Senior baseline: 5-8 minutes. Less = you're rushing; more = you're stalling.
- **Edge cases stated upfront:** count them. Senior baseline: 3-5.
- **Big-O stated *before* submitting:** yes/no.
- **Clarifying questions you asked the (imaginary) interviewer:** ≥2 is good.

### For system design
- **Did you stick to the 5-step blueprint, or jump straight to boxes?** Skipping requirements is the most common senior mistake.
- **How many minutes did you spend on the deep-dive section?** Senior baseline: ≥40% of total time. If you compressed it to 5 minutes, you wasted the slot in earlier steps.
- **Did you propose at least 2 explicit trade-offs and pick a side?** Senior signal.
- **Did you mention operational concerns (rollout, SLO, on-call, cost telemetry)?**

### For behavioral
- **Average story length:** under 2.5 min spoken? More = you're rambling; less = you're under-detailing.
- **"I" vs "we" ratio:** senior baseline is "I" by ~2:1.
- **Numbers in Result:** every story should have at least one quantified outcome.

### Output: a 1-page "Day 21 verdict" note

Sections:
1. **Strengths** — 3 things you can confidently rely on tomorrow.
2. **Compensations** — 3 known weaknesses + your specific in-interview compensation strategy ("if asked about HNSW tuning, anchor on `m` and `ef_search`, then admit limited prod experience").
3. **Hard nos** — what you would *not* claim under direct questioning.

This note is the artifact you re-read 30 minutes before each real interview.

---

## 3. Post-Sprint Plan Finalization (15 min)

You won't keep doing 2.5h/day after this. But you will atrophy fast without maintenance. Pick **one** weekly habit you can sustain:

- **Option A — *Coding*:** 2 LeetCode Mediums per week, one from a weak category. 1h/week.
- **Option B — *System design*:** one 60-min mock + 30-min write-up per week. 1.5h/week.
- **Option C — *Reading*:** one paper per week from `arxiv.org/list/cs.CL/recent` or one engineering blog post (Anthropic, OpenAI, ByteByteGo, Pragmatic Engineer). 30m/week.
- **Option D — *Anki*:** convert your `#review/` tagged notes into 200 flashcards; 5-minute daily review. 35min/week.

Recommendation: **A + C** — keeps coding sharp without burnout, keeps you current on a fast-moving field.

Set a recurring calendar block. Treat it like a meeting with yourself.

---

## 4. Day 21 Deliverables

- [ ] Full 2h mock loop completed and recorded.
- [ ] Debrief note produced — Strengths / Compensations / Hard nos.
- [ ] Post-sprint maintenance plan in calendar (recurring block, named).
- [ ] **Stop.** No more new material. Sleep 8+ hours. Revisit your debrief 30 min before each real interview.

---

## 5. Closing Reflection

Sprint completed. What you should now have:

1. **A tight ~150-line Obsidian per topic** with your own words — not the syllabus's. Owning the explanation in your own framing is the senior signal.
2. **One capstone document** (multi-tenant chatbot + variants) you can defend in 60 minutes.
3. **8 STAR stories** drilled to 2-minute speaking time, plus a 10-question interviewer Q&A bank.
4. **A debriefed map of your interview fingerprint** — the specific patterns of mistakes you make under pressure, and your in-interview compensations.

The 21 days don't make you a senior AI orchestrator. They make you **legible** as one to an interviewer. The work is real either way.

Good luck.

## 6. References

- [Marc Brackett — *Permission to Feel*](https://marcbrackett.com/permission-to-feel/) (the chapter on regulating performance anxiety is genuinely useful for interview week).
- [Lara Hogan — *Negotiating offers*](https://larahogan.me/blog/job-negotiation-guide/) — when the offers come.
- [Levels.fyi](https://levels.fyi) — calibrate your offer.
