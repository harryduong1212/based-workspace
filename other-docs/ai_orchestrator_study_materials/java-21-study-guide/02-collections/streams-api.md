# Streams API (Java 8+)

The Streams API provides a functional, declarative approach to processing sequences of elements. It is one of the most heavily tested topics in any Java interview.

## 1. What is a Stream?

A Stream is a **pipeline** of operations that processes data from a source (Collection, array, I/O channel) without modifying the source. Streams are:
- **Lazy**: Intermediate operations are not executed until a terminal operation is invoked.
- **Single-use**: A stream can only be consumed once. To re-process, create a new stream.
- **Potentially parallel**: Can transparently switch to multi-threaded processing.

### Creating Streams
```java
// From a Collection
List<String> names = List.of("Harry", "Alice", "Bob");
Stream<String> stream = names.stream();

// From static factory methods
Stream<String> of = Stream.of("A", "B", "C");
IntStream range = IntStream.range(1, 100);     // 1 to 99
IntStream rangeClosed = IntStream.rangeClosed(1, 100); // 1 to 100

// From other sources
Stream<String> lines = Files.lines(Path.of("data.txt"));
Stream<Integer> generated = Stream.iterate(0, n -> n + 2).limit(10); // 0,2,4,...,18
```

---

## 2. Stream Pipeline Structure

Every stream pipeline consists of three stages:

```
Source → Intermediate Operation(s) → Terminal Operation
```

- **Intermediate operations** return a new Stream (lazy, chainable).
- **Terminal operations** produce a result or side-effect and consume the stream.

---

## 3. Key Intermediate Operations

| Operation | Description | Example |
| --- | --- | --- |
| `filter(Predicate)` | Keeps elements matching the predicate | `.filter(s -> s.length() > 3)` |
| `map(Function)` | Transforms each element | `.map(String::toUpperCase)` |
| `flatMap(Function)` | Flattens nested structures (Stream of Streams → single Stream) | `.flatMap(list -> list.stream())` |
| `distinct()` | Removes duplicates (uses `equals()`) | `.distinct()` |
| `sorted()` | Sorts elements (natural order or custom Comparator) | `.sorted(Comparator.reverseOrder())` |
| `peek(Consumer)` | Performs an action on each element without modifying (debugging) | `.peek(System.out::println)` |
| `limit(n)` | Truncates to first N elements | `.limit(5)` |
| `skip(n)` | Skips first N elements | `.skip(2)` |

### `map` vs `flatMap`
```java
// map: 1-to-1 transformation
List<String> upper = names.stream()
    .map(String::toUpperCase)
    .toList(); // [HARRY, ALICE, BOB]

// flatMap: 1-to-many (flatten nested lists)
List<List<String>> nested = List.of(List.of("A", "B"), List.of("C", "D"));
List<String> flat = nested.stream()
    .flatMap(Collection::stream)
    .toList(); // [A, B, C, D]
```

---

## 4. Key Terminal Operations

| Operation | Description | Return Type |
| --- | --- | --- |
| `collect(Collector)` | Mutable reduction into a container | Varies (List, Map, etc.) |
| `toList()` | Collects into an unmodifiable List (Java 16+) | `List<T>` |
| `forEach(Consumer)` | Performs action on each element | `void` |
| `reduce(identity, accumulator)` | Reduces elements to a single value | `T` or `Optional<T>` |
| `count()` | Counts elements | `long` |
| `findFirst()` / `findAny()` | Returns first/any element | `Optional<T>` |
| `anyMatch()` / `allMatch()` / `noneMatch()` | Boolean checks against a predicate | `boolean` |
| `min()` / `max()` | Finds min/max by Comparator | `Optional<T>` |

### `reduce` Example
```java
// Sum all integers
int sum = IntStream.rangeClosed(1, 100)
    .reduce(0, Integer::sum); // 5050

// Concatenate strings
String joined = names.stream()
    .reduce("", (a, b) -> a + ", " + b); // ", Harry, Alice, Bob"
```

---

## 5. Collectors (The Power Tools)

The `Collectors` utility class provides powerful reduction operations.

```java
import static java.util.stream.Collectors.*;

List<Order> orders = fetchOrders();

// Collect to a List (mutable)
List<String> nameList = names.stream().collect(toList());

// Collect to an unmodifiable List (Java 16+, preferred)
List<String> nameList2 = names.stream().toList();

// Collect to a Map
Map<String, Integer> nameLengths = names.stream()
    .collect(toMap(name -> name, String::length));

// Group By (like SQL GROUP BY)
Map<OrderStatus, List<Order>> byStatus = orders.stream()
    .collect(groupingBy(Order::status));

// Group By with aggregation (count per group)
Map<OrderStatus, Long> countByStatus = orders.stream()
    .collect(groupingBy(Order::status, counting()));

// Partition By (split into true/false groups)
Map<Boolean, List<Order>> partitioned = orders.stream()
    .collect(partitioningBy(o -> o.total().compareTo(BigDecimal.valueOf(100)) > 0));

// Joining strings
String csv = names.stream()
    .collect(joining(", ", "[", "]")); // [Harry, Alice, Bob]

// Summarizing statistics
IntSummaryStatistics stats = orders.stream()
    .collect(summarizingInt(o -> o.items().size()));
// stats.getAverage(), stats.getMax(), stats.getSum(), stats.getCount()
```

---

## 6. Optional (Companion to Streams)

`Optional<T>` is a container that may or may not contain a non-null value. It was introduced alongside Streams to handle absent values safely.

```java
// Creating Optionals
Optional<String> present = Optional.of("Hello");
Optional<String> empty = Optional.empty();
Optional<String> nullable = Optional.ofNullable(getValue()); // null-safe

// Consuming Optionals (NEVER call .get() without .isPresent()!)
String result = present
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .orElse("DEFAULT");             // "HELLO"

// orElseGet (lazy — only called if empty)
String lazy = empty.orElseGet(() -> expensiveComputation());

// orElseThrow (throw if absent)
String strict = empty.orElseThrow(() -> new NotFoundException("Not found"));

// ifPresent / ifPresentOrElse
present.ifPresentOrElse(
    value -> System.out.println("Found: " + value),
    () -> System.out.println("Not found")
);
```

> **Anti-pattern**: Never use `Optional` as a method parameter or field type. It is designed for return types only.

---

## 7. Parallel Streams

Parallel streams split the workload across the common `ForkJoinPool`.

```java
long count = names.parallelStream()
    .filter(n -> n.length() > 3)
    .count();
```

### When to Use Parallel Streams
- ✅ Large datasets (10,000+ elements).
- ✅ CPU-bound operations (no I/O, no shared mutable state).
- ✅ Stateless, associative operations (`reduce`, `collect`).

### When NOT to Use
- ❌ Small collections (overhead exceeds benefit).
- ❌ I/O-bound operations (use Virtual Threads instead!).
- ❌ Operations with side-effects or shared mutable state.
- ❌ Order-dependent operations (unless using `forEachOrdered()`).

> **Interview Tip**: If asked "when would you use parallel streams?", always mention the tradeoffs. Saying "always use parallel for performance" is a red flag. Mention Virtual Threads as the modern alternative for I/O-bound concurrency.

---

## 8. Common Pitfalls

1. **Stream reuse**: Streams are single-use. Calling a terminal operation on an already-consumed stream throws `IllegalStateException`.
2. **Infinite streams**: `Stream.iterate()` and `Stream.generate()` are infinite. Always use `limit()`.
3. **Side-effects in `peek()`**: `peek()` is for debugging. Do not rely on it for business logic; it may not execute for short-circuiting operations.
4. **`collect(toList())` vs `.toList()`**: `toList()` (Java 16+) returns an **unmodifiable** list. `collect(toList())` returns a mutable `ArrayList`.
