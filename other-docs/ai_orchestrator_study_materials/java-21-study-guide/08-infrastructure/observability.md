# Cloud Deployment & Observability

When running a distributed architecture, it is impossible to debug issues by looking at a single log file. You must track requests as they jump across network boundaries.

## 1. Cloud Run & Cloud SQL Proxy

If deploying to GCP (Google Cloud Platform), the modern stack utilizes **Cloud Run** and **Cloud SQL**.

### Cloud Run
- Serverless container orchestration. It scales to zero when there is no traffic, and scales up to 1000s of instances instantly.
- Best paired with Spring Boot 3 Native Images (GraalVM) to eliminate JVM cold-start penalties.

### Cloud SQL Proxy
- **Security Rule**: Never expose your database to the public internet.
- The Proxy runs as a sidecar container next to your application.
- Your app connects to `localhost:5432` without SSL.
- The Proxy authenticates via IAM, encrypts the traffic, and establishes a secure TLS tunnel to the Cloud SQL database instance.

---

## 2. Distributed Tracing & Observability

### The Correlation ID (Trace ID)
To track a request across 5 different microservices, we inject a unique `X-Request-ID` or `traceparent` (W3C standard) header at the API Gateway.

### Mapped Diagnostic Context (MDC)
SLF4J (the logging facade for Logback) provides the MDC. It is a ThreadLocal map.
When a request enters your Spring application, a Servlet Filter grabs the Header and puts it into the MDC.

```java
@Component
public class CorrelationIdFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain) {
        String correlationId = request.getHeader("X-Request-ID");
        if (correlationId == null) {
            correlationId = UUID.randomUUID().toString();
        }
        
        // Put it in the MDC
        MDC.put("correlationId", correlationId);
        
        try {
            chain.doFilter(request, response);
        } finally {
            // ALWAYS clear ThreadLocals in the finally block to prevent memory leaks in thread pools!
            MDC.remove("correlationId");
        }
    }
}
```

### Logback Configuration
You then update your `logback-spring.xml` to automatically print this variable on every single log line.
```xml
<!-- Notice the %X{correlationId} -->
<pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] [%X{correlationId}] %-5level %logger{36} - %msg%n</pattern>
```

### Propagating the ID Downstream
When Service A calls Service B using a `RestTemplate` or `WebClient`, it must attach the Correlation ID from the MDC into the outgoing HTTP Headers. (Libraries like Micrometer Tracing handle this automatically).

When you search Datadog, Splunk, or ELK for that Correlation ID, you will see the exact timeline of logs across the Gateway, Service A, Service B, and the Database.
