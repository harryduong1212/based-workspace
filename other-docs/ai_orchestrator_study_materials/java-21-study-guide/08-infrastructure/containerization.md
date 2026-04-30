# Containerization & Podman

In modern deployments, your Java application is shipped as an immutable container. Optimizing this container is crucial for performance and security.

## 1. The Ultimate Java Multi-Stage Containerfile

A standard `FROM eclipse-temurin:21-jdk` image can be over 400MB. For microservices, we want minimal attack surfaces and small image sizes. We achieve this using a multi-stage build and `jlink`.

> *Note: Podman uses `Containerfile` as the default filename, while Docker uses `Dockerfile`. Both are fully interchangeable in format and syntax. Use whichever matches your container engine.*

```dockerfile
# ----------------------------------------
# Stage 1: Build the app with Maven
# ----------------------------------------
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /build

# Copy POM and download dependencies FIRST (Maximizes Docker layer caching!)
COPY pom.xml .
RUN mvn dependency:go-offline

# Then copy source and build
COPY src ./src
RUN mvn clean package -DskipTests

# ----------------------------------------
# Stage 2: Create custom JRE with jlink
# ----------------------------------------
FROM eclipse-temurin:21-jdk AS jre-build
# Use jdeps to identify required modules, then link them into a custom JRE
RUN jlink \
    --add-modules java.base,java.sql,java.naming,java.management,java.instrument,java.net.http,jdk.crypto.ec \
    --strip-debug \
    --no-man-pages \
    --no-header-files \
    --compress=zip-9 \
    --output /javaruntime

# ----------------------------------------
# Stage 3: Minimal Production Image
# ----------------------------------------
FROM debian:bookworm-slim
# 1. Setup non-root user (Security Best Practice)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 2. Copy the tiny custom JRE and the Application JAR
COPY --from=jre-build /javaruntime /opt/java
COPY --from=build /build/target/*.jar /app/app.jar

USER appuser

# 3. Use JVM container awareness flags!
ENTRYPOINT ["/opt/java/bin/java", "-XX:MaxRAMPercentage=75.0", "-XX:+UseZGC", "-XX:+ZGenerational", "-jar", "/app/app.jar"]
```

### Why use `jlink`?
Standard JREs contain hundreds of modules your application will never use (like Swing or AWT GUI libraries). `jlink` strips these out, reducing the runtime size to ~40-50MB.

---

## 2. Rootless Podman Concepts

Docker runs as a daemon running as `root`. If a hacker breaks out of a Docker container, they have root access to the host machine.
Podman solves this.

### Key Differences
1. **Daemonless**: Podman does not have a background daemon.
2. **Rootless**: Podman runs entirely within the user namespace.
   - If you run Podman as the user `harry`, the container runs as `harry`.
   - Even if the container thinks it is running as `root` (UID 0 internally), it is actually mapped to `harry` on the host. 
   - A breakout results in standard user privileges, completely neutralizing the attack.

### Working with Podman
Podman is entirely compatible with Docker CLI commands.
```bash
# Set an alias
alias docker=podman

# Build and run exactly the same way
podman build -t my-app .
podman run -d -p 8080:8080 my-app
```
