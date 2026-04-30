# Day 20 — Capstone Polish + Light Coding Mock #3 + `#weak` Sweep

> **Timebox: ~2.5 hours.** `#weak` sweep (60m) → Light coding (45m) → Capstone polish (30m) → Logistics & rest plan (15m).
> Tomorrow is the final dry-run. Today is your last chance to **close gaps**, not open new ones. Resist the urge to learn anything new.

---

## 1. `#weak` Sweep (60 min)

Open Obsidian. Search for every note tagged `#weak`. List them in order from "most likely to come up tomorrow" to "least".

For each, do **20 minutes max**:
1. Re-read the deep-dive doc.
2. Re-answer the relevant day's recall questions.
3. *Write* (don't read) a 100-word summary of the topic in your own words.

If a topic still feels weak after 20 minutes, **stop**. You're at diminishing returns. In an interview, if pressed on it, you'll fall back to: "I don't have deep production experience with X, but conceptually it works as Y, and I'd reach for Z resources to learn it." That's a perfectly senior answer — *not knowing everything is fine, knowing how to learn is the signal.*

**Hard rule: don't tag *new* topics `#weak` today.** Today is closure. New gaps go into a "post-sprint backlog" Obsidian note.

---

## 2. Light Coding Mock #3 (45 min)

Two **Easy** problems, 20 minutes each, no Hard. The point is to **arrive at Day 21 confident**, not exhausted. Pick problems that re-use this sprint's patterns:
- Hash-map + array: [Valid Anagram (#242)](https://leetcode.com/problems/valid-anagram/).
- Two pointers: [Two Sum II (#167)](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/).
- Tree recursion: [Symmetric Tree (#101)](https://leetcode.com/problems/symmetric-tree/).
- BFS: [Number of Islands (#200)](https://leetcode.com/problems/number-of-islands/) — re-do without notes; target <8 minutes.

Any solve under 15 minutes = win. **If you struggle at "Easy" today, you're sleep-deprived, not ill-prepared.** Treat it as a signal: sleep at 10pm tonight.

---

## 3. Capstone Polish (30 min)

Open the capstone write-up (multi-tenant chatbot + enterprise-search variant). **Read it from top to bottom out loud.** Anywhere you stumble or feel unsure → mark with `[?]`. Fix the top 3 `[?]`s.

Specifically check that you can:
- State the QPS / storage estimate without looking.
- Explain the tenant isolation enforcement layer (RLS) in 30 seconds.
- Defend your vector DB choice in 30 seconds (why pgvector vs Pinecone vs Qdrant).
- Identify three failure modes the design tolerates.

This artifact is what you bring to the system-design round and what you reference in behavioral stories ("when I designed our chatbot platform...").

---

## 4. Logistics & Rest Plan (15 min)

A surprising number of senior offers are lost to logistics and fatigue, not technical gaps.

### Tomorrow's logistics (Day 21 dry-run)

- [ ] Quiet, lit room.
- [ ] Whiteboard (or large paper + markers) for system design.
- [ ] Webcam + recording set up if you're going to record.
- [ ] Water bottle. Snack within reach.
- [ ] Phone on Do Not Disturb.

### For real interviews (after Day 21)

- [ ] Confirm exact timezone / time / format with recruiter.
- [ ] Test video software 30 min before. (Zoom updates are a leading cause of late starts.)
- [ ] Eat 1.5 hours before. Not less, not more.
- [ ] **Sleep 7+ hours**. There is no version of cramming the night before that beats sleeping.

### Post-sprint plan (write down, even briefly)

What's the *one thing* you'll keep doing weekly after the sprint to retain what you've built?
- 2 LeetCode Mediums per week + an Anki deck made from `#review/` tags?
- One 30-min system design write-up per week?
- One paragraph weekly: "what shipped in AI infra this week and what does it imply for my work?"

---

## 5. Day 20 Deliverables

- [ ] `#weak` topics swept; remaining gaps documented in a "post-sprint backlog" note.
- [ ] Two Easy problems re-solved comfortably.
- [ ] Capstone document with `[?]` cleared.
- [ ] Tomorrow's logistics list completed.
- [ ] Post-sprint maintenance plan written down (even one bullet).

## 6. References

- [Cal Newport — *Deep Work*](https://www.calnewport.com/books/deep-work/) — the chapter on deliberate practice is directly relevant to how you should approach Day 21.
- [Andy Matuschak — *Why books don't work*](https://andymatuschak.org/books/) — explains why your active-recall approach is correct.
