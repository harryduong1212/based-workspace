# Behavioral Mastery (The STAR Framework)

Interviews for Senior/Lead roles heavily weight behavioral questions. A brilliant coder who fails the behavioral interview will not get an offer. Seniority isn't just coding; it's navigating ambiguity, leading teams, and learning from failure.

## 1. The Anatomy of a Perfect STAR Story

Your story should be exactly 2 minutes long. 

- **Situation (15%)**: Context. "At Company X, our legacy monolith was struggling to process 10,000 orders/minute during peak sales, causing database deadlocks."
- **Task (10%)**: Your goal. "As the lead backend engineer, I was tasked with redesigning the checkout flow to ensure zero dropped orders during the Black Friday event, with only 3 weeks to go."
- **Action (60%)**: **Use "I", not "We" - highlight YOUR technical decisions.** 
  "First, I analyzed the PostgreSQL locks and realized the bottleneck was synchronous inventory deduction. I decoupled the flow by introducing RabbitMQ. I implemented a Transactional Outbox pattern where the checkout simply inserted an event into an `outbox` table in the same local transaction as the order creation. I wrote a Debezium CDC pipeline to reliably publish these to RabbitMQ, where a separate pool of workers processed the inventory deduction asynchronously with a retry DLQ."
- **Result (15%)**: **Quantify everything.** "As a result, we successfully handled 25,000 orders/minute with zero deadlocks. Average checkout latency dropped from 2.5s to 300ms, and we captured an additional $2M in revenue during the sale."

---

## 2. The 8 Must-Have Stories

Write one detailed STAR story for each of these prompts before your interview. *Pro Tip: You can reuse a single massive project for multiple prompts by focusing on different angles.*

1. **Pushback/Conflict**: When did you disagree with product/management on a technical decision? How did you resolve it? *(Focus on data-driven persuasion, not ego)*.
2. **Mentorship**: How did you level up a junior developer who was struggling? *(Focus on empathy and pair-programming)*.
3. **Failure**: Tell me about a time you brought down production. *(Focus heavily on the post-mortem, the fix, and the systemic CI/CD change you introduced to prevent it happening again)*.
4. **Ambiguity**: A time you were given a vague requirement and had to deliver.
5. **Leadership**: Leading a cross-functional team across a finish line.
6. **Performance**: The hardest bug or performance bottleneck you've tracked down.
7. **Tech Debt**: How do you balance shipping features vs. paying down tech debt?
8. **New Tech Evaluation**: How you evaluated and introduced a new technology (e.g., Spring AI, n8n, or pgvector) to the stack.
