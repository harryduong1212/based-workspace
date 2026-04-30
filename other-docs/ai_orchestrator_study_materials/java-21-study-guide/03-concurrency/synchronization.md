# Synchronization & Concurrent Utilities

When multiple threads access a shared resource, there is a possibility of data inconsistency due to thread interference. Synchronization mechanisms ensure thread safety.

## 1. Traditional Synchronization
Java provides the intrinsic `synchronized` keyword, which uses the monitor lock associated with an object.

### Synchronized Method
Locks the entire method. If the method is `static`, the lock is acquired on the `Class` object. If non-static, the lock is acquired on the `this` instance.

```java
class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }
}
```

### Synchronized Block
Allows finer-grained locking over specific lines of code, reducing contention.

```java
public void process() {
    // some non-critical operations
    synchronized(this) {
        // critical section
        count++;
    }
}
```

### Java Memory Model (JMM)
The JMM defines how threads interact through memory. It establishes **Happens-Before** relationships to ensure visibility and ordering of variable modifications across threads.

### Volatile Keyword
Ensures that the value of a variable is always read from main memory, not from the thread's local cache. 
- **Visibility**: Writes to a `volatile` variable establish a happens-before relationship with subsequent reads.
- **Ordering**: Prevents the compiler and CPU from reordering instructions around the volatile read/write.
- *Note*: It does not guarantee atomicity (e.g., `count++` is not safe even if `count` is volatile).

```java
private volatile boolean flag = true;
```

---

## 2. Modern `java.util.concurrent` Utilities

In modern Java, utilizing high-level constructs from `java.util.concurrent` is strongly preferred over raw `synchronized` blocks or `wait/notify`.

### Locks (`ReentrantLock` & `StampedLock`)
Provides more advanced features than `synchronized`, such as interruptible lock waits, timed waits, and fairness.

**ReentrantLock**:
```java
Lock lock = new ReentrantLock();

public void safeMethod() {
    lock.lock();
    try {
        // critical section (Safe for Virtual Threads!)
    } finally {
        lock.unlock(); // Always unlock in a finally block!
    }
}
```

**StampedLock**:
Introduces optimistic reading. It returns a "stamp" (long) that you can validate later. If no write occurred, you don't need to acquire a real read lock, drastically improving read-heavy performance.

### Concurrent Collections
Thread-safe collections that handle their own synchronization efficiently (often using lock striping or lock-free algorithms).
- `ConcurrentHashMap`
- `CopyOnWriteArrayList`
- `BlockingQueue` (e.g., `ArrayBlockingQueue`)

### Atomic Variables
Classes in `java.util.concurrent.atomic` support lock-free thread-safe programming on single variables.
- `AtomicInteger`, `AtomicLong`, `AtomicBoolean`, `AtomicReference`

```java
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet(); // Thread-safe atomic operation
```

### Synchronizers
High-level classes that facilitate coordination between threads.
- **CountDownLatch**: Allows one or more threads to wait until a set of operations performed in other threads completes.
- **CyclicBarrier**: Allows a set of threads to all wait for each other to reach a common barrier point.
- **Semaphore**: Maintains a set of permits to restrict the number of threads accessing a physical or logical resource.

---

## 3. Asynchronous Programming (`CompletableFuture`)
Introduced in Java 8, `CompletableFuture` allows building complex, non-blocking asynchronous pipelines without "callback hell."

### Composition Patterns
- **Chaining**: `thenApply()` transforms the result. `thenAccept()` consumes the result (returns void).
- **FlatMapping**: `thenCompose()` chains two dependent futures (similar to `flatMap`).
- **Zipping**: `thenCombine()` executes two independent futures concurrently and combines their results.
- **Fan-out**: `allOf()` waits for an array of futures to complete. `anyOf()` waits for the fastest future to complete.

```java
CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(() -> fetchUser(id));
CompletableFuture<Order> orderFuture = CompletableFuture.supplyAsync(() -> fetchOrder(id));

// Combining independent futures
userFuture.thenCombine(orderFuture, (user, order) -> {
    return new Invoice(user, order);
}).exceptionally(ex -> {
    // Handle error seamlessly
    log.error("Failed to build invoice", ex);
    return Invoice.fallback();
});
```
