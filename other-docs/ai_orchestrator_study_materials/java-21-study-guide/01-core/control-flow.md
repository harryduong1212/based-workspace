# Control Flow & Pattern Matching

Java provides standard control flow statements along with powerful modern enhancements introduced in recent versions.

## Standard Control Flow
- **Decision Making**: `if`, `else if`, `else`
- **Looping**: `for`, `enhanced for-each`, `while`, `do-while`
- **Branching**: `break`, `continue`, `return`

---

## Modern Enhancements (Java 14 - Java 21)

### Switch Expressions (Java 14)
Switch statements were upgraded to act as expressions (returning a value) and use arrow (`->`) syntax, eliminating the need for `break` statements to prevent fall-through.

```java
String dayType = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Weekday";
    case SATURDAY, SUNDAY -> "Weekend";
    default -> throw new IllegalArgumentException("Invalid day: " + day);
};
```
If a block is needed, the `yield` keyword is used to return a value:
```java
int result = switch (mode) {
    case "A" -> 1;
    case "B" -> {
        System.out.println("Processing B");
        yield 2;
    }
    default -> 0;
};
```

### Pattern Matching for `instanceof` (Java 16)
Eliminates the need for explicit casting after an `instanceof` check.

```java
// Old way
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// Java 16+ way
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

### Pattern Matching for `switch` (Java 21)
Allows `switch` expressions and statements to test objects against a number of patterns, each with a specific action.

```java
String format(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("int %d", i);
        case Long l    -> String.format("long %d", l);
        case Double d  -> String.format("double %f", d);
        case String s  -> String.format("String %s", s);
        case null      -> "null";
        default        -> obj.toString();
    };
}
```

### Record Patterns (Java 21)
Allows deconstructing record values directly within pattern matching.

```java
record Point(int x, int y) {}

void printPoint(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        System.out.println("X: " + x + ", Y: " + y);
    }
}
```
