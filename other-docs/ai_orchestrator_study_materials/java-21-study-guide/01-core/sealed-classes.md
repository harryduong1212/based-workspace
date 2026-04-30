# Sealed Classes & Interfaces (Java 17)

Sealed classes and interfaces restrict which classes can extend or implement them, providing precise control over inheritance hierarchies. They are a **finalized feature since Java 17** and are a critical complement to Pattern Matching and Records.

## 1. Why Sealed Classes Matter

In traditional Java, you had two extremes:
- `final` classes — cannot be extended at all.
- Open classes — can be extended by anyone, anywhere.

Sealed classes sit in the middle: **controlled extensibility**. You explicitly declare which classes are allowed to inherit.

## 2. Syntax

```java
// The sealed parent declares its permitted subtypes
public sealed interface Shape permits Circle, Rectangle, Triangle {}

// Each permitted subtype MUST be one of: final, sealed, or non-sealed
public record Circle(double radius) implements Shape {}                // final (records are implicitly final)
public final class Rectangle implements Shape {                        // explicitly final
    private final double width, height;
    public Rectangle(double width, double height) { this.width = width; this.height = height; }
    public double width() { return width; }
    public double height() { return height; }
}
public non-sealed class Triangle implements Shape {                    // open for further extension
    private final double base, height;
    public Triangle(double base, double height) { this.base = base; this.height = height; }
    public double base() { return base; }
    public double height() { return height; }
}
```

### Rules for Permitted Subtypes
- Must be declared in the same module (or same file if unnamed module).
- Each subtype must explicitly extend/implement the sealed parent.
- Each subtype must be one of: `final`, `sealed`, or `non-sealed`.

## 3. The Killer Feature: Exhaustive Switch (No `default` Needed!)

When combined with **Pattern Matching for `switch`** (Java 21), sealed types enable **exhaustive switches** — the compiler knows all possible subtypes, so `default` is unnecessary:

```java
double area(Shape shape) {
    return switch (shape) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t  -> 0.5 * t.base() * t.height();
        // No default needed! The compiler verifies all cases are covered.
    };
}
```

> **Why this matters**: If you later add a new permitted subtype (e.g., `Hexagon`), the compiler will **immediately flag every switch** that doesn't handle it. This is compile-time safety that open class hierarchies can never provide.

## 4. Sealed Classes vs. Enums

| Feature | Sealed Classes | Enums |
| --- | --- | --- |
| Instances | Multiple instances per type | Fixed set of singleton instances |
| Data | Each subtype can carry different data | All values share the same fields |
| Hierarchy | Can have deep inheritance trees | Flat (no sub-enums) |
| Use Case | Domain modeling (shapes, events, AST nodes) | Fixed constants (days, statuses) |

## 5. Real-World Example: Domain Events

Sealed types are ideal for modeling a **closed set of domain events** in an event-driven architecture:

```java
public sealed interface OrderEvent permits OrderCreated, OrderShipped, OrderCancelled {
    String orderId();
    Instant timestamp();
}

public record OrderCreated(String orderId, Instant timestamp, BigDecimal total) implements OrderEvent {}
public record OrderShipped(String orderId, Instant timestamp, String trackingNumber) implements OrderEvent {}
public record OrderCancelled(String orderId, Instant timestamp, String reason) implements OrderEvent {}

// Exhaustive handler — compiler ensures no event type is missed
String handleEvent(OrderEvent event) {
    return switch (event) {
        case OrderCreated e  -> "Order %s created: $%s".formatted(e.orderId(), e.total());
        case OrderShipped e  -> "Order %s shipped: %s".formatted(e.orderId(), e.trackingNumber());
        case OrderCancelled e -> "Order %s cancelled: %s".formatted(e.orderId(), e.reason());
    };
}
```

> **Interview Tip**: When asked about Java 21 features, presenting Sealed Classes + Records + Pattern Matching as a unified trio for domain modeling shows deep understanding. This pattern replaces the Visitor pattern with far less boilerplate.
