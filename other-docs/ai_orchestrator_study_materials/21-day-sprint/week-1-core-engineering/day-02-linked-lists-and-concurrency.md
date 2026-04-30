# Day 2 — Linked Lists & Concurrency (Virtual Threads)

> **Timebox: ~2.5 hours.** DSA practice (60m) → Deep-dive read (60m) → Recall & write-up (30m).
> Concurrency is dense — if the read overruns 60m, finish it tomorrow morning before Day 3 instead of cutting recall.

---

## 1. Algorithmic Canvas — Linked Lists

The reason linked lists keep showing up in interviews isn't because they're useful (in production Java you'd reach for `ArrayDeque` or `ArrayList`). They're a *pointer manipulation litmus test*. Master two techniques and you cover ~80% of LL problems: **dummy head** and **slow/fast (Floyd's) pointers**.

### Problem 1 — [Reverse Linked List (LC #206)](https://leetcode.com/problems/reverse-linked-list/) — *Easy*

**Target:** `O(n)` time, `O(1)` space — iterative, three-pointer reversal.
**Key insight:** at each node, you must remember the *next* pointer before you overwrite the link, otherwise you lose the rest of the list.

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    while (curr != null) {
        ListNode next = curr.next;  // 1. remember
        curr.next = prev;           // 2. flip
        prev = curr;                // 3. advance prev
        curr = next;                // 4. advance curr
    }
    return prev;
}
```

**Pattern visual — three-pointer walk:**

```mermaid
graph LR
    P[prev] -.-> C[curr] --> N[next]
    style P fill:#444,color:#fff
    style C fill:#a55,color:#fff
    style N fill:#555,color:#fff
```
*Each tick: save `next`, flip `curr.next = prev`, then `prev = curr; curr = next`.*

**Follow-ups:**
- [Reverse Linked List II (LC #92)](https://leetcode.com/problems/reverse-linked-list-ii/) — reverse only between positions `m` and `n`. **Use a dummy head** to simplify the boundary case.
- [Reverse Nodes in k-Group (LC #25)](https://leetcode.com/problems/reverse-nodes-in-k-group/) — same trick applied to chunks. *Hard*, but a classic.
- [Linked List Cycle (LC #141)](https://leetcode.com/problems/linked-list-cycle/) — Floyd's tortoise/hare; covers the *other* fundamental LL trick.

---

### Problem 2 — [Merge Two Sorted Lists (LC #21)](https://leetcode.com/problems/merge-two-sorted-lists/) — *Easy*

**Target:** `O(n + m)` time, `O(1)` extra space — iterative with a **dummy head**.
**Key insight:** allocate one sentinel node so you never have to special-case "is this the first node we're appending?". The real list is `dummy.next`.

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0);
    ListNode tail  = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) { tail.next = l1; l1 = l1.next; }
        else                  { tail.next = l2; l2 = l2.next; }
        tail = tail.next;
    }
    tail.next = (l1 != null) ? l1 : l2;  // splice the remainder
    return dummy.next;
}
```

**Why the dummy matters:** without it, you'd need an `if (head == null) head = ...; else tail.next = ...;` branch on every iteration. The dummy collapses two cases into one — the same trick you'll use in *every* "build a list as you go" problem.

**Follow-ups:**
- [Merge K Sorted Lists (LC #23)](https://leetcode.com/problems/merge-k-sorted-lists/) — *Hard*. Either heap-of-heads (`O(N log k)`) or pairwise merge. Day 12 (heaps) revisits this.
- [Add Two Numbers (LC #2)](https://leetcode.com/problems/add-two-numbers/) — same dummy-head + carry pattern.
- [Sort List (LC #148)](https://leetcode.com/problems/sort-list/) — merge sort on a linked list, `O(n log n)` time, `O(log n)` stack.

---

## 2. Engineering Deep-Dive — Multithreading & Virtual Threads

**Read:** [multithreading.md](../../java-21-study-guide/03-concurrency/multithreading.md)

This is *the* differentiator topic for an AI orchestration role: a single chatbot request fans out to embedding calls, vector search, LLM calls, tool calls — all I/O-bound and blocking. Virtual Threads (Project Loom) are why you don't need WebFlux for this.

### 5 extraction targets

1. The **6-state thread lifecycle** (New → Runnable → Running → Blocked/Waiting → Timed-Waiting → Terminated). Be able to name a transition trigger for each edge.
2. **Why platform threads don't scale**: 1:1 OS-thread mapping → ~1MB stack per thread → ~10K concurrent threads ceiling on a normal box.
3. **Mount/unmount mechanics of virtual threads**: when a VT performs blocking I/O, the JVM unmounts it from its **carrier thread** (a real OS thread in the ForkJoinPool), freeing the carrier for another VT. *This is what makes blocking code cheap.*
4. **The Pinning trap**: `synchronized` blocks (and native code, and old JNI calls) prevent unmounting. The VT stays glued to its carrier — and now you've recreated the platform-thread bottleneck. **Fix: `ReentrantLock`.**
5. **Structured Concurrency** (`StructuredTaskScope`): treats N concurrent subtasks as one unit of work. `ShutdownOnFailure` cancels siblings if one fails — this is the right primitive for a RAG pipeline that fans out to *embed + vector-search + cache-check* in parallel.

### Recall questions (close the doc)

1. Your service uses `Executors.newVirtualThreadPerTaskExecutor()` and benchmarks great in isolation. In production it falls over at 200 RPS. Top suspect (give the JVM diagnostic flag too)? *(→ Pinning. Run with `-Djdk.tracePinnedThreads=full` to log every pin event.)*
2. Why is `synchronized (cache) { jdbc.query(...) }` a virtual-thread anti-pattern, but `lock.lock(); try { jdbc.query(...) } finally { lock.unlock(); }` is not?
3. You fan out 3 subtasks: `embed()`, `vectorSearch()`, `getUserPrefs()`. The third throws. With `StructuredTaskScope.ShutdownOnFailure`, what happens to the other two's threads, and why is this superior to plain `CompletableFuture.allOf`?
4. A teammate says: "Virtual threads make my CPU-bound image-resize handler scale better." Right or wrong, and why? *(→ Wrong. VTs help only with **blocking** workloads. CPU-bound work still needs `ForkJoinPool` sized to cores.)*
5. Pre-Loom, `Thread.sleep(1)` inside a critical section made the carrier thread useless for 1ms. On a virtual thread, what happens and at what cost?

---

## 3. Day 2 Deliverables

- [ ] `sprint/day02/ReverseLinkedList.java` — iterative + recursive solutions, 3-line big-O comment, `// Trade-off:` note explaining when recursion's stack risk matters.
- [ ] `sprint/day02/MergeTwoSortedLists.java` — dummy-head solution, 3-line big-O comment.
- [ ] **Obsidian note (200 words):** *"Why production rarely uses `LinkedList<E>`"* — pointer-chasing cache misses, `ArrayDeque` as the better fit, and one historical case where a real linked list *was* the right answer (e.g. LRU cache combined with a HashMap).
- [ ] **Obsidian note (250 words):** *"Virtual threads in one diagram"* — explain mount/unmount to a teammate using one drawing. Include the pinning trap as a footnote.
- [ ] **Code experiment:** spin up 10,000 virtual threads, each doing `Thread.sleep(Duration.ofSeconds(1))`. Measure wall time. Repeat with `Executors.newFixedThreadPool(200)`. Record the numbers in your Obsidian note.
- [ ] **Spaced-repetition tags:** `#review/day-02`, `#topic/linked-lists`, `#topic/concurrency`. Revisit on Day 9 and Day 16.

---

## 4. References & Further Reading

**Linked lists / pointer technique**
- [NeetCode — Linked List roadmap](https://neetcode.io/roadmap)
- [LeetCode editorial — Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/editorial/)

**Virtual threads & structured concurrency**
- [JEP 444 — Virtual Threads (Final, Java 21)](https://openjdk.org/jeps/444)
- [JEP 453 — Structured Concurrency (Preview)](https://openjdk.org/jeps/453)
- [Inside Java — *Virtual Threads: Why You Should Care*](https://inside.java/2023/05/22/podcast-031/)
- [Netflix Tech Blog — Java 21 Virtual Threads in production](https://netflixtechblog.com/java-21-virtual-threads-dive-in-e4e0dccc1991)
- [Martin Fowler — The LMAX Architecture (Mechanical Sympathy)](https://martinfowler.com/articles/lmax.html)
