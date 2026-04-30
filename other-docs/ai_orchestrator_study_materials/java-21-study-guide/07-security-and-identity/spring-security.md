# Spring Security Internals

Spring Security is a powerful, highly customizable authentication and access-control framework. Under the hood, it operates entirely on Servlet Filters.

## 1. The Filter Chain Architecture

When a request enters a Spring Boot application, it hits the `DelegatingFilterProxy`, which delegates to the `FilterChainProxy`. This proxy contains a list of `SecurityFilterChain` objects.

**Standard Order of Execution**:
1. `CorsFilter` (Handles Cross-Origin Requests).
2. `CsrfFilter` (Handles Cross-Site Request Forgery — usually disabled for stateless APIs).
3. `AuthenticationFilter` (e.g., `BearerTokenAuthenticationFilter` for JWTs). Extracts the token and authenticates the user.
4. `ExceptionTranslationFilter` (Wraps the authorization check. Catches `AccessDeniedException` → HTTP 403 Forbidden, `AuthenticationException` → HTTP 401 Unauthorized).
5. `AuthorizationFilter` (The very last filter). Checks if the authenticated user has the required roles/permissions to access the specific endpoint. Exceptions thrown here bubble up to `ExceptionTranslationFilter`.

---

## 2. Resource Server Configuration

When building a stateless REST API that consumes JWTs, you configure Spring Boot as an OAuth2 Resource Server.

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            // 1. Disable CSRF for stateless APIs
            .csrf(AbstractHttpConfigurer::disable)
            // 2. Enforce stateless session creation (No JSESSIONID)
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            // 3. Define Endpoint Access
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasAuthority("SCOPE_admin")
                .anyRequest().authenticated()
            )
            // 4. Enable JWT Bearer Token validation
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter()))
            )
            .build();
    }

    // 5. Customizing Role mapping
    @Bean
    public JwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
        // By default, Spring expects scopes to be prefixed with "SCOPE_".
        // We can change this to read a custom "roles" claim and prefix with "ROLE_"
        grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");
        grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");

        JwtAuthenticationConverter jwtAuthenticationConverter = new JwtAuthenticationConverter();
        jwtAuthenticationConverter.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);
        return jwtAuthenticationConverter;
    }
}
```

## 3. Method-Level Security (`@PreAuthorize`)

Instead of configuring all URLs in the `SecurityFilterChain`, it is often better to secure methods directly using SpEL (Spring Expression Language).

> **Prerequisite**: You must add `@EnableMethodSecurity` to your `@Configuration` class for `@PreAuthorize` to work. *(In Spring Security 6, this replaced the older `@EnableGlobalMethodSecurity`.)*

```java
@Service
public class OrderService {

    // Simple Role Check
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteOrder(String id) { ... }

    // Advanced Attribute-Based Check (ABAC)
    // Ensures the user can only access the order if they own it.
    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.claims['user_id']")
    public Order getOrder(String orderId, String userId) { ... }
}
```
