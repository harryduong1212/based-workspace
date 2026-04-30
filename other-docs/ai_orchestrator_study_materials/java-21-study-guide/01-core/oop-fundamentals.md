# OOP Fundamentals & Design Principles

Object-Oriented Programming is the foundation of Java. While these concepts may seem basic, Senior-level interviews test deep understanding of *when* and *why* to apply each principle, not just definitions.

## 1. The Four Pillars of OOP

### Encapsulation
Bundling data (fields) and the methods that operate on that data into a single unit (class), while restricting direct access to internal state.

```java
public class BankAccount {
    private BigDecimal balance; // Hidden internal state

    public BankAccount(BigDecimal initialBalance) {
        this.balance = initialBalance;
    }

    // Controlled access via methods (invariants enforced)
    public void deposit(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Deposit must be positive");
        }
        this.balance = this.balance.add(amount);
    }

    public BigDecimal getBalance() {
        return balance; // Read-only exposure
    }
}
```

> **Why it matters**: Encapsulation protects invariants. If `balance` were public, any code could set it to a negative value, breaking business rules.

### Inheritance
A mechanism where a new class (subclass) acquires the properties and behaviors of an existing class (superclass). Java supports **single inheritance** for classes but **multiple inheritance for interfaces**.

```java
public class Animal {
    protected String name;
    public void speak() { System.out.println("..."); }
}

public class Dog extends Animal {
    @Override
    public void speak() { System.out.println("Woof!"); }
}
```

> **Modern Guidance**: Favor **composition over inheritance** (Item 18, Effective Java). Inheritance creates tight coupling. Use it for "is-a" relationships (Dog *is an* Animal), not for code reuse.

### Polymorphism
The ability of a single interface to represent different underlying forms (types).

- **Compile-time (Static)**: Method overloading — same name, different parameter types.
- **Runtime (Dynamic)**: Method overriding — a subclass provides its own implementation of a superclass method. The JVM determines which method to call at runtime based on the actual object type.

```java
Animal animal = new Dog(); // Reference type: Animal, Object type: Dog
animal.speak(); // "Woof!" — Runtime polymorphism (dynamic dispatch)
```

### Abstraction
Hiding complex implementation details and exposing only the essential interface. Achieved via:
- **Abstract Classes**: Can have both abstract methods (no body) and concrete methods. Cannot be instantiated.
- **Interfaces**: Define a contract (what to do, not how). Since Java 8, interfaces can have `default` and `static` methods.

```java
// Abstract class — partial implementation
public abstract class PaymentProcessor {
    // Template Method Pattern
    public final void processPayment(BigDecimal amount) {
        validate(amount);
        execute(amount);     // Abstract — each subclass implements differently
        sendConfirmation();
    }

    protected abstract void execute(BigDecimal amount);

    private void validate(BigDecimal amount) { /* common validation */ }
    private void sendConfirmation() { /* common notification */ }
}
```

---

## 2. Abstract Class vs Interface

| Feature | Abstract Class | Interface |
| --- | --- | --- |
| Instantiation | Cannot be instantiated | Cannot be instantiated |
| Constructors | ✅ Can have constructors | ❌ No constructors |
| State (Fields) | ✅ Instance fields allowed | ❌ Only `public static final` constants |
| Method Types | Abstract + concrete methods | Abstract + `default` + `static` + `private` (Java 9+) |
| Inheritance | Single inheritance only | Multiple interfaces allowed |
| Access Modifiers | All modifiers allowed | Methods are `public` by default |
| **Use When** | Sharing state or partial implementation among related classes | Defining a contract for unrelated classes |

> **Interview Answer**: "Use an abstract class when you want to share code and state among closely related classes. Use an interface when you want to define a capability that can be mixed into unrelated classes (like `Comparable`, `Serializable`)."

---

## 3. The `equals()` / `hashCode()` Contract

This is a **classic** Senior Java interview question. Violating this contract causes silent, catastrophic bugs in `HashMap`, `HashSet`, and other hash-based collections.

### The Contract
1. **Reflexive**: `x.equals(x)` must be `true`.
2. **Symmetric**: If `x.equals(y)`, then `y.equals(x)`.
3. **Transitive**: If `x.equals(y)` and `y.equals(z)`, then `x.equals(z)`.
4. **Consistent**: Multiple calls return the same result (if objects haven't changed).
5. **Non-null**: `x.equals(null)` must be `false`.
6. **hashCode rule**: If `x.equals(y)`, then `x.hashCode() == y.hashCode()`. (The reverse is NOT required.)

### Correct Implementation
```java
public class Employee {
    private final String id;
    private final String name;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Employee employee = (Employee) o;
        return Objects.equals(id, employee.id); // Equality based on business key
    }

    @Override
    public int hashCode() {
        return Objects.hash(id); // MUST use the same fields as equals()
    }
}
```

> **Why Records are great**: `record Employee(String id, String name) {}` automatically generates correct `equals()` and `hashCode()` based on all components.

---

## 4. SOLID Principles (Interview Must-Know)

### S — Single Responsibility Principle (SRP)
A class should have **one reason to change** — one responsibility.

```java
// BAD: This class does validation, persistence, AND email
public class UserService {
    public void createUser(User user) {
        validate(user);
        userRepository.save(user);
        emailService.sendWelcome(user);
    }
}

// GOOD: Each class has one job
public class UserValidator { public void validate(User user) { ... } }
public class UserRepository { public void save(User user) { ... } }
public class WelcomeEmailService { public void send(User user) { ... } }
```

### O — Open/Closed Principle (OCP)
Classes should be **open for extension, closed for modification**. Add new behavior by adding new code, not changing existing code.

```java
// Using Strategy Pattern (OCP-compliant)
public interface DiscountStrategy {
    BigDecimal apply(BigDecimal price);
}

public class SeasonalDiscount implements DiscountStrategy {
    public BigDecimal apply(BigDecimal price) { return price.multiply(new BigDecimal("0.80")); }
}

public class LoyaltyDiscount implements DiscountStrategy {
    public BigDecimal apply(BigDecimal price) { return price.multiply(new BigDecimal("0.90")); }
}

// Adding a new discount type requires ZERO changes to existing code
```

### L — Liskov Substitution Principle (LSP)
Subtypes must be substitutable for their base types without altering correctness. If `Dog extends Animal`, then `Dog` must behave correctly everywhere `Animal` is expected.

### I — Interface Segregation Principle (ISP)
Clients should not be forced to depend on interfaces they do not use. Prefer many small, focused interfaces over one large "fat" interface.

### D — Dependency Inversion Principle (DIP)
High-level modules should depend on **abstractions**, not concrete implementations. This is the principle behind Spring's Dependency Injection.

```java
// BAD: High-level depends on low-level concrete class
public class OrderService {
    private PostgresOrderRepo repo = new PostgresOrderRepo(); // Tight coupling!
}

// GOOD: Depend on abstraction
public class OrderService {
    private final OrderRepository repo; // Interface
    public OrderService(OrderRepository repo) { this.repo = repo; } // Injected
}
```

---

## 5. Composition Over Inheritance

When you need to reuse behavior, prefer **composing objects** (has-a) over extending classes (is-a).

```java
// Inheritance approach (fragile — breaks if ArrayList internals change)
public class InstrumentedSet<E> extends HashSet<E> {
    private int addCount = 0;

    @Override
    public boolean add(E e) {
        addCount++;
        return super.add(e); // Depends on HashSet internal behavior
    }
}

// Composition approach (robust — delegates explicitly)
public class InstrumentedSet<E> implements Set<E> {
    private final Set<E> delegate; // Wrapped set
    private int addCount = 0;

    public InstrumentedSet(Set<E> delegate) { this.delegate = delegate; }

    @Override
    public boolean add(E e) {
        addCount++;
        return delegate.add(e); // Clear delegation
    }

    // Delegate all other Set methods to the inner set...
}
```

> **Interview Tip**: This is the **Decorator Pattern** from GoF. Spring uses this extensively (e.g., `TransactionAwareDataSourceProxy` wrapping a `DataSource`).
