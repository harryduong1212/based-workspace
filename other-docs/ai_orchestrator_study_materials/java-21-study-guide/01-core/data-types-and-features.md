# Data Types & Modern Features

## Primitive Data Types

| **Data Type** | **Default Value (fields)** | **Size** | **Range** |
| --- | --- | --- | --- |
| `byte` | `0` | 8-bit signed | -128 to 127 |
| `short` | `0` | 16-bit signed | -32,768 to 32,767 |
| `int` | `0` | 32-bit signed | $-2^{31}$ to $2^{31} - 1$ |
| `long` | `0L` | 64-bit signed | $-2^{63}$ to $2^{63} - 1$ |
| `float` | `0.0f` | 32-bit IEEE 754 | Single-precision floating point |
| `double` | `0.0d` | 64-bit IEEE 754 | Double-precision floating point |
| `char` | `'\u0000'` | 16-bit Unicode | `\u0000` to `\uffff` |
| `boolean` | `false` | JVM specific | `true` or `false` |

## Reference Data Types
- Objects, Arrays, Interfaces, Enums, and Records.
- Default value for reference types is `null`.

![Data Types Diagram](../assets/images/data_types_untitled.png)

---

## Modern Java Data Structures (Java 14 - Java 21)

### Records (Java 16)
Records provide a compact syntax for declaring classes that are transparent carriers for shallowly immutable data. They automatically generate constructors, accessors, `equals()`, `hashCode()`, and `toString()`.

```java
public record User(String username, String email) {}

// Usage
var user = new User("harry", "harry@example.com");
System.out.println(user.email());
```

### Local-Variable Type Inference (`var`) (Java 10)
Allows the compiler to infer the type of a local variable.

```java
var list = new ArrayList<String>(); // Inferred as ArrayList<String>
var stream = list.stream();         // Inferred as Stream<String>
```

### Text Blocks (Java 15)
Multi-line string literals that avoid the need for most escape sequences.

```java
String json = """
    {
        "name": "Harry",
        "role": "Backend Developer"
    }
    """;
```

### String Templates (Preview in Java 21 — ⚠️ Removed in JDK 23)
Allowed string interpolation, combining literal text with embedded expressions and variables securely. This feature was previewed in Java 21 (JEP 430) and Java 22 (JEP 459), but the OpenJDK team **withdrew and removed it entirely in JDK 23** due to design concerns with the processor-centric approach.

```java
// This code compiled ONLY on Java 21/22 with --enable-preview
String name = "Harry";
String greeting = STR."Hello \{name}!";
```

> **⚠️ Interview Note**: If asked about String Templates, mention that the feature was explored but ultimately rejected. This demonstrates you track the evolution of the language. Use `String.format()` or `"... " + variable` for interpolation in production code.
