# GitHub Actions Guide — CI/CD for Java Developers

> This guide explains the CI/CD pipeline that automatically builds and publishes n8n-atom Docker images. It's written for developers with backend experience but limited DevOps knowledge.

---

## What is CI/CD?

**CI (Continuous Integration)** and **CD (Continuous Delivery/Deployment)** automate the process of building, testing, and publishing your code.

| Concept | What it does | Java equivalent |
|---|---|---|
| **CI** | Automatically build & test on every push | Jenkins running `mvn test` on every commit |
| **CD** | Automatically publish/deploy after CI passes | Jenkins running `mvn deploy` to Nexus |

In our case:
- **CI**: Build n8n-atom from source inside a GitHub runner
- **CD**: Push the built Docker image to GitHub Container Registry (GHCR)

---

## GitHub Actions Concepts

### Workflow, Job, Step — The Hierarchy

```
Workflow (.yml file)
 └── Job (runs on a virtual machine)
      └── Step 1: Checkout code
      └── Step 2: Build
      └── Step 3: Test
      └── Step 4: Publish
```

| GitHub Actions Term | Java/Backend Equivalent |
|---|---|
| **Workflow** (`.yml` file) | Like a Jenkinsfile or `pom.xml` build lifecycle |
| **Job** | Like a Maven module build — runs independently |
| **Step** | Like a Maven goal (`compile`, `test`, `package`) |
| **Runner** | Like a Jenkins agent — the machine that executes the build |
| **Action** | Like a Maven plugin — reusable, pre-built build logic |
| **Trigger** (`on:`) | Like a Git webhook / post-commit hook |
| **Secret** | Like `settings.xml` credentials |
| **Artifact** | Like a `.jar` / `.war` file produced by the build |

### How Triggers Work

```yaml
on:
  push:
    branches: [master]     # Run when code is pushed to master
    tags: ['v*']           # Run when a tag like v1.0.0 is created
  workflow_dispatch:       # Allow manual trigger from GitHub UI
```

This is similar to configuring a Jenkins pipeline to trigger on SCM changes. The `workflow_dispatch` is like manually clicking "Build Now" in Jenkins.

---

## Our Workflow — Annotated

Here's the complete workflow for publishing the n8n-atom Docker image, with detailed comments:

```yaml
# File: .github/workflows/docker-publish.yml
# Location: In the harryduong1212/n8n-atom repository

name: Build & Publish Docker Image

# ┌─────────────────────────────────────────────────────────┐
# │ TRIGGERS — When does this workflow run?                 │
# └─────────────────────────────────────────────────────────┘
on:
  push:
    branches: [master]     # Auto-run when you push to master
    tags: ['v*']           # Auto-run when you create a version tag
  workflow_dispatch:       # Manual trigger button in GitHub UI
                           # (useful for testing without pushing code)

# ┌─────────────────────────────────────────────────────────┐
# │ ENVIRONMENT — Shared variables across all jobs          │
# └─────────────────────────────────────────────────────────┘
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  # ↑ This resolves to "harryduong1212/n8n-atom" automatically.
  # github.repository is a built-in variable provided by GitHub.

# ┌─────────────────────────────────────────────────────────┐
# │ JOBS — The actual work                                  │
# └─────────────────────────────────────────────────────────┘
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    # ↑ This job runs on a fresh Ubuntu VM provided by GitHub (free tier).
    # It's like a Jenkins agent — temporary, clean, and disposable.

    permissions:
      contents: read       # Can read your repo code
      packages: write      # Can push images to GHCR
      # ↑ These are like IAM roles. Without 'packages: write',
      # the push to GHCR would fail with a 403 Forbidden.

    steps:
      # ── Step 1: Get the source code ──
      - name: Checkout
        uses: actions/checkout@v4
        # ↑ "uses" means "run this pre-built Action" — like using a Maven plugin.
        # actions/checkout clones your repo into the runner's workspace.
        # Without this, the runner has an empty directory.

      # ── Step 2: Enable ARM64 builds ──
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
        # ↑ QEMU is a CPU emulator. This step installs it so we can
        # build ARM64 images on an AMD64 runner.
        #
        # WHY: Your friend's M4/M5 MacBook has an ARM64 CPU.
        # Without this, the image would only work on Intel/AMD machines.
        #
        # ANALOGY: It's like installing a JVM that can run both x86
        # and ARM bytecode — cross-compilation for containers.

      # ── Step 3: Enable multi-platform Docker builds ──
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        # ↑ Buildx extends Docker with multi-platform build support.
        # Standard docker build can only build for the host architecture.
        # Buildx + QEMU can build for ANY architecture.
        #
        # ANALOGY: It's like adding the maven-cross-compile plugin to
        # build both Java 11 and Java 17 artifacts in one build.

      # ── Step 4: Authenticate with GHCR ──
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
        # ↑ GITHUB_TOKEN is AUTOMATIC — you don't need to create it!
        # GitHub generates a short-lived token for each workflow run
        # that has permissions to push to your account's GHCR.
        #
        # ANALOGY: It's like Maven's settings.xml where your Nexus
        # credentials are stored, but managed automatically by GitHub.

      # ── Step 5: Generate image tags and labels ──
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=raw,value=latest,enable=${{ github.ref == format('refs/heads/{0}', 'master') }}
            type=semver,pattern={{version}}
            type=sha,prefix=
        # ↑ This generates smart tags:
        #   - "latest" when pushing to master
        #   - "1.0.0" when you create a v1.0.0 tag
        #   - "abc1234" (short SHA) for every build
        #
        # ANALOGY: Like Maven's version management — SNAPSHOT for
        # development, release version for tagged builds.

      # ── Step 6: Build from source ──
      - name: Build n8n-atom from source
        run: |
          sudo corepack enable
          corepack prepare pnpm@10.22.0 --activate
          export NODE_OPTIONS='--max-old-space-size=4096'
          export LEFTHOOK=0 HUSKY=0
          if [ -f scripts/prepare.mjs ]; then
            mv scripts/prepare.mjs scripts/prepare.mjs.bak
          fi
          echo "console.log('Prepare skipped (CI build)')" > scripts/prepare.mjs
          pnpm install --frozen-lockfile --ignore-scripts
          pnpm run build:n8n
        # ↑ This is the SAME build process as your local script
        # (build_n8n_atom.py), but running directly on the GitHub
        # runner instead of inside a container.
        #
        # The runner already has Node.js installed, so we don't
        # need a container-in-a-container.

      # ── Step 7: Build & push the Docker image ──
      - name: Build & Push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./docker/images/n8n/Dockerfile
          platforms: linux/amd64,linux/arm64
          # ↑ Build for BOTH architectures:
          #   - amd64: Your Windows PC, Intel Macs, most servers
          #   - arm64: M1/M2/M3/M4/M5 MacBooks, AWS Graviton
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          # ↑ GitHub Actions cache — reuses unchanged Docker layers
          # between builds. This can cut build time from 20min to 5min.
          #
          # ANALOGY: Like Maven's local repository (~/.m2/repository)
          # caching downloaded dependencies between builds.
```

---

## MCP Inspector Workflow

The MCP Inspector workflow is simpler because the build is smaller:

```yaml
# File: .github/workflows/docker-publish.yml
# Location: In the harryduong1212/mcp-inspector-atom8n repository

name: Build & Publish MCP Inspector

on:
  push:
    branches: [main]
    tags: ['v*']
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=raw,value=latest,enable=${{ github.ref == format('refs/heads/{0}', 'main') }}
            type=semver,pattern={{version}}
            type=sha,prefix=

      - name: Build from source
        run: |
          npm install --ignore-scripts
          npm run build

      - name: Build & Push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Multi-Arch Images Explained

### The Problem

Your Windows PC has an **AMD64** (also called x86_64) processor. Your friend's M4 MacBook has an **ARM64** (also called aarch64) processor. They are fundamentally different instruction sets — like speaking different languages.

A Docker image compiled for AMD64 **cannot run natively** on ARM64. It would need to use **Rosetta emulation** (slow and sometimes crashes).

### The Solution: Multi-Arch Manifests

When we build with `platforms: linux/amd64,linux/arm64`, Docker creates:

```
ghcr.io/harryduong1212/n8n-atom:latest
├── linux/amd64  →  Image A (for Intel/AMD machines)
└── linux/arm64  →  Image B (for Apple Silicon Macs)
```

When someone runs `docker pull`, the engine automatically selects the correct variant for their CPU. Your friend doesn't need to know or care — it just works.

> **Java analogy**: It's like publishing a multi-release JAR (`MANIFEST.MF` with `Multi-Release: true`) that contains both Java 11 and Java 17 class files. The JVM picks the right version automatically.

### How QEMU Makes This Possible

The GitHub runner has an AMD64 CPU. To build ARM64 images, it uses **QEMU** — a CPU instruction translator that converts ARM64 instructions to AMD64 in real-time.

```
GitHub Runner (AMD64 CPU)
 └── QEMU ARM64 emulator
      └── Docker build (compiling npm packages for ARM64)
```

This is slower than native compilation (expect 2-3x longer builds), but it means we don't need a separate ARM64 build farm.

---

## GHCR (GitHub Container Registry)

### What is it?

GHCR is GitHub's Docker image registry — like Docker Hub, but integrated with your GitHub account and repos.

| Feature | GHCR | Maven Central / Nexus |
|---|---|---|
| **Stores** | Docker images | JAR files |
| **Auth** | GitHub token (automatic) | Username/password in settings.xml |
| **URL pattern** | `ghcr.io/owner/repo:tag` | `groupId:artifactId:version` |
| **Visibility** | Public or private | Public (Central) or private (Nexus) |

### How Authentication Works

1. GitHub automatically creates a `GITHUB_TOKEN` for each workflow run.
2. This token has permissions scoped to the current repository.
3. The `docker/login-action` uses this token to authenticate with GHCR.
4. **You don't need to create or manage any secrets** — it's fully automatic.

### Viewing Your Published Images

After the workflow runs successfully:
1. Go to your repository on GitHub
2. Click "Packages" in the right sidebar
3. Or visit: `https://github.com/harryduong1212/n8n-atom/pkgs/container/n8n-atom`

---

## Practical Cheat Sheet

### "I changed code, how do I publish a new image?"

```bash
# Option 1: Push to master (triggers automatically)
git add . && git commit -m "feat: my change" && git push

# Option 2: Create a release tag (more controlled)
git tag v1.0.0
git push origin v1.0.0
```

### "How do I trigger a rebuild manually?"

1. Go to your repo on GitHub → **Actions** tab
2. Click the workflow name ("Build & Publish Docker Image")
3. Click **"Run workflow"** dropdown → select branch → **"Run workflow"**

### "How do I see build logs?"

1. Go to **Actions** tab
2. Click the workflow run (green ✅ or red ❌)
3. Click the job name → expand each step to see logs

### "How do I roll back to a previous image?"

```bash
# List available tags
podman search ghcr.io/harryduong1212/n8n-atom --list-tags

# Use a specific SHA tag instead of "latest"
# In docker-compose.quickstart.yaml, change:
#   image: ghcr.io/harryduong1212/n8n-atom:abc1234
```

### "What if the build fails?"

1. Check the **Actions** tab for red ❌ runs
2. Expand the failed step to see the error
3. Common issues:
   - **OOM**: The GitHub runner has 7GB RAM. If the build exceeds this, it's killed.
   - **Network**: npm registry timeouts → rerun the workflow
   - **Breaking change**: The source code has a build error → fix and push again

---

## Setting Up the Workflows

### Step 1: Enable GHCR for your account

1. Go to [github.com/settings/packages](https://github.com/settings/packages)
2. Ensure "Packages" is enabled (it should be by default)

### Step 2: Add the workflow file to n8n-atom

```bash
# In your local n8n-atom fork
cd external/n8n-atom

# Create the workflow directory
mkdir -p .github/workflows

# Copy the workflow file (from the annotated example above)
# Save it as .github/workflows/docker-publish.yml

# Commit and push
git add .github/workflows/docker-publish.yml
git commit -m "ci: add Docker image publish workflow"
git push
```

### Step 3: Add the workflow file to mcp-inspector-atom8n

Same process, using the MCP Inspector workflow example above.

### Step 4: Verify

1. Go to **Actions** tab in your repo
2. You should see the workflow listed
3. It will run automatically on the next push to master/main

---

## Summary

```mermaid
graph LR
    A[Push to master] --> B[GitHub Actions]
    B --> C[Build from source]
    C --> D[Create Docker image<br/>amd64 + arm64]
    D --> E[Push to GHCR]
    E --> F[Users run:<br/>docker compose up]

    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
    style E fill:#9C27B0,color:#fff
    style F fill:#FF9800,color:#fff
```

**The complete flow:**
1. You push code to your fork → GitHub Actions triggers
2. A fresh Ubuntu VM builds n8n-atom from source
3. The compiled code is packaged into a multi-arch Docker image
4. The image is pushed to `ghcr.io/harryduong1212/n8n-atom:latest`
5. Normal users simply run `docker compose up` with the quickstart file
