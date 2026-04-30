# Java Database Connectivity (JDBC)

JDBC is an API that enables Java applications to interact with relational databases. It serves as the bridge between the application layer and the physical data layer.

![JDBC Architecture](../assets/images/java_database_connectivity_jdbc_Untitled.png)

## 1. Architecture

The JDBC architecture consists of two main layers:
1. **JDBC API**: The interface between the Java application and JDBC.
2. **JDBC Driver**: The interface between JDBC and the database. Each Database Management System (DBMS) requires its own specific driver (e.g., PostgreSQL driver, MySQL Connector/J).

### Drivers and Dialects
- The **Driver** handles connection configuration and network communication with the DBMS.
- A **Dialect** defines the specific variant of SQL supported by the database. In Hibernate 6+ (Spring Boot 3), dialect detection is **automatic** — you no longer need to specify version-specific classes like the legacy `MySQL8Dialect` or `PostgreSQL95Dialect`. Simply configure your `DataSource` and Hibernate resolves the correct dialect from database metadata at startup.

---

## 2. Setting Up a Connection

### 2.1 Dependencies
Instead of manually downloading `.jar` files, modern Java applications use build tools like Maven or Gradle to manage driver dependencies.

```xml
<!-- Maven Example for PostgreSQL -->
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.6.0</version>
</dependency>
```

### 2.2 Establishing the Connection
You need three primary components:
1. **URL**: The path to the database (e.g., `jdbc:postgresql://localhost:5432/mydb`).
2. **Username**: Database user.
3. **Password**: User's password.

**Using `DriverManager`**
```java
String url = "jdbc:postgresql://localhost:5432/mydb";
try (Connection conn = DriverManager.getConnection(url, "user", "password")) {
    // Execute queries
} catch (SQLException e) {
    e.printStackTrace();
}
```

**Using `DataSource` (Preferred in Enterprise Apps)**
`DataSource` is preferred because it can be integrated with connection pooling (like **HikariCP**, the default in Spring Boot), significantly improving performance by reusing connections.

> [!TIP]
> **HikariCP Sizing Formula**: The widely accepted formula for optimal pool size is: `connections = ((core_count * 2) + effective_spindle_count)`. For modern SSDs, the spindle count is often treated as 1. A pool size of 10-20 is usually sufficient for high-throughput applications.

```java
PGSimpleDataSource dataSource = new PGSimpleDataSource();
dataSource.setUrl("jdbc:postgresql://localhost:5432/mydb");
dataSource.setUser("user");
dataSource.setPassword("password");

try (Connection conn = dataSource.getConnection()) {
    // Execute queries
}
```

*Note: Always use `try-with-resources` to ensure the `Connection` is closed and resources are released back to the pool.*

---

## 3. Transactions

A transaction is a sequence of operations performed as a single logical unit of work. It ensures data integrity based on ACID properties.

### Managing Transactions via JDBC
```java
try (Connection conn = dataSource.getConnection()) {
    // 1. Disable Auto-Commit to start the transaction
    conn.setAutoCommit(false);

    try {
        // Execute updates/inserts
        // ...

        // 2. Commit if everything succeeds
        conn.commit();
    } catch (SQLException ex) {
        // 3. Rollback if an error occurs
        conn.rollback();
    }
}
```

### Savepoints
Savepoints allow you to rollback a portion of a transaction rather than the entire transaction.
```java
Savepoint sp = conn.setSavepoint("savepoint-one");
// Execute more queries...
conn.rollback(sp); // Rolls back to "savepoint-one"
conn.commit();
```

---

## 4. Transaction Isolation Levels

Isolation levels dictate how changes made by one transaction become visible to other concurrent transactions.

| **Isolation Level** | **Description** | **JDBC Constant** |
| --- | --- | --- |
| **Read Uncommitted** | Allows reading uncommitted data (Dirty reads). | `Connection.TRANSACTION_READ_UNCOMMITTED` |
| **Read Committed** | Prevents dirty reads. Data must be committed to be read. | `Connection.TRANSACTION_READ_COMMITTED` |
| **Repeatable Read** | Prevents non-repeatable reads. Ensures multiple reads return the same data. | `Connection.TRANSACTION_REPEATABLE_READ` |
| **Serializable** | Strictest level. Prevents phantom reads. Transactions act sequentially. | `Connection.TRANSACTION_SERIALIZABLE` |

```java
connection.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED);
```

---

## 5. Database Optimization & Performance (Hibernate/JPA context)

When using an ORM like Hibernate over JDBC, several critical performance traps exist.

### 5.1 The N+1 Query Problem
Fetching a collection of entities, and then lazily loading a relationship for each entity results in 1 initial query + N additional queries.

**Detection & Fixes**:
1. **`@EntityGraph`**: Overrides lazy loading for specific queries to use a SQL `JOIN FETCH`.
   ```java
   @EntityGraph(attributePaths = {"items"})
   List<Order> findByStatus(String status);
   ```
2. **`@BatchSize`**: Instead of fetching relationships 1-by-1, it fetches them in batches using an `IN (...)` clause.
   ```java
   @Entity
   @BatchSize(size = 50)
   public class Order { ... }
   ```
3. **`@Fetch(FetchMode.SUBSELECT)`**: Fetches all collections for all currently loaded parent entities using a single sub-query.

### 5.2 Hibernate 2nd-Level Cache
The 1st-level cache is scoped to the `EntityManager`/`Session`. The 2nd-level cache (L2) is scoped to the `SessionFactory` and shared across sessions.
- **Entity Cache**: Caches the actual entity data.
- **Collection Cache**: Caches only the IDs of the entities in a collection. You MUST also cache the target entity to avoid N+1.
- **Query Cache**: Caches the IDs returned by a specific query.

### 5.3 Advanced PostgreSQL Optimization

**PostgreSQL Query Planner (`EXPLAIN ANALYZE`)**
Always prefix slow queries with `EXPLAIN (ANALYZE, BUFFERS)` to see actual execution times and memory hits. Look out for **Sequential Scans** (full table scans) on large tables and the join algorithms used:
- **Nested Loop**: Fast for small datasets.
- **Hash Join**: Creates a hash table of the smaller table, scans the larger. Good for unindexed large sets.
- **Merge Join**: Fast if both sets are already sorted.

**B-Tree Left-Prefix Rule**
If a composite index is created on `(company_id, status, created_at)`:
- `WHERE company_id = X AND status = Y` → **Uses index**
- `WHERE status = Y` → **FULL TABLE SCAN** (Misses the prefix!)

**Advanced Index Types**
- **GIN (Generalized Inverted Index)**: Crucial for full-text search (`tsvector`), JSONB containment (`@>`), and array operations.
- **GiST**: Optimized for geometric data and proximity queries (e.g., PostGIS).
- **BRIN**: Ideal for huge time-series tables where data is naturally ordered (extremely small footprint).

**Partial & Covering Indexes**
```sql
-- Partial Index: Incredibly fast and small, only indexes specific rows
CREATE INDEX idx_active_users ON users(status) WHERE status = 'ACTIVE';

-- Covering Index: No heap fetch required if we only SELECT the INCLUDE columns
CREATE INDEX idx_status_covering ON users(status) INCLUDE (name, email);
```

### 5.4 Zero-Downtime Schema Migrations (Liquibase)
When applying schema changes to a live DB, locking is the enemy.
- **Expand and Contract Pattern**: Never rename a column in one step. 
  1. Add new column.
  2. Deploy code that writes to both, reads from old.
  3. Backfill data.
  4. Deploy code that reads from new.
  5. Drop old column.
- **Index Creation**: Standard `CREATE INDEX` blocks writes. Always use `CREATE INDEX CONCURRENTLY` in PostgreSQL to build the index in the background without locking the table.
