# Multi-Tenancy & Access Control

When building SaaS (Software as a Service) platforms, your application serves multiple customers (tenants). You must ensure strict data isolation so Tenant A can never see Tenant B's data.

## 1. Multi-Tenancy Models

1. **Database per Tenant**: Highest isolation, highest cost.
2. **Schema per Tenant**: Medium isolation, medium cost (One DB, many schemas).
3. **Shared Schema, Shared DB (Row-Level Security)**: Lowest infrastructure cost, highest complexity. Data is isolated using a `tenant_id` column.

## 2. PostgreSQL Row-Level Security (RLS)

If you use the Shared Schema model, relying entirely on Java developers to always add `WHERE tenant_id = X` is extremely dangerous. One missed WHERE clause leaks data. 
PostgreSQL RLS enforces isolation at the database kernel level.

### SQL Configuration
```sql
-- 1. Enable RLS on the table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 2. Create the isolation policy
CREATE POLICY tenant_isolation_policy ON orders
    USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- 3. Force RLS for table owners too (optional)
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
```

### Spring Boot Integration
To make this work, the Java application must inject the `tenant_id` into the PostgreSQL session right before the query executes.

```java
// Using Hibernate StatementInspector to prepend the SET command
public class TenantStatementInspector implements StatementInspector {
    @Override
    public String inspect(String sql) {
        String tenantId = TenantContext.getCurrentTenant();
        if (tenantId != null) {
            // IMPORTANT: Validate tenantId to prevent SQL injection!
            // Ensure it's a valid UUID before concatenating into SQL.
            String validated = UUID.fromString(tenantId).toString();
            return "SET LOCAL app.current_tenant = '" + validated + "'; " + sql;
        }
        return sql;
    }
}
```

---

## 3. Access Control: RBAC vs ABAC

### Role-Based Access Control (RBAC)
Permissions are tied to static roles.
- *Example*: "Admins can delete orders."
- *Implementation*: `@PreAuthorize("hasRole('ADMIN')")`
- *Pros*: Fast, simple, standard.
- *Cons*: Fails when rules become dynamic.

### Attribute-Based Access Control (ABAC)
Permissions are evaluated dynamically based on the attributes of the User, the Resource, and the Environment.
- *Example*: "Users can only delete orders IF they own the order AND the order status is 'PENDING' AND it is during business hours."
- *Implementation*: Delegated to a dedicated security service using SpEL.

```java
// In the Controller/Service
@PreAuthorize("@securityLogic.canDeleteOrder(authentication, #order)")
public void deleteOrder(Order order) { ... }

// In the Security Logic Component
@Component("securityLogic")
public class SecurityLogic {
    public boolean canDeleteOrder(Authentication auth, Order order) {
        String currentUserId = extractUserId(auth);
        
        return order.getOwnerId().equals(currentUserId) 
            && order.getStatus().equals("PENDING")
            && isBusinessHours();
    }
}
```
