# Advanced Build System Architecture

This document explains the high-performance, cross-platform build pipeline for the `n8n-atom` project.

## 🚀 The Isolated Linux Build Pipeline (Phase 3)

We have transitioned from a host-volume mount approach to an **Isolated Linux Build Pipeline** to solve persistent issues with Windows NTFS filesystem limitations (path lengths, symlink breakage, and extreme I/O lag).

### 1. Source Injection (Git Archive)
The host (Windows/macOS/Linux) acts purely as a "source publisher". The build script uses `git archive` to package a clean, tracked-only snapshot of the source code and streams it into a persistent Linux-native volume.

```bash
git archive HEAD | tar xf - -C /build
```
- **Cleanup**: Pre-existing files in `/build` are purged, while `node_modules` and `.turbo` cache are preserved for performance.
- **Reproducibility**: Only tracked files are included; local `node_modules` or temp files on the host do not interfere with the build.

### 2. Native EXT4 Caching
The compilation occurs on a native Linux filesystem (`ext4`) within a Podman/Docker volume (`vibe-n8n-workspace`). This provides:
- **Zero MAX_PATH limitations**: Linux handles deep `node_modules` paths natively.
- **Turbo speed**: Native filesystem I/O is 10x-50x faster than WSL2/9p mounts during `npm install`.
- **Native Bindings**: Native modules (`sqlite3`, `bcrypt`) are compiled against the builder container's Linux libraries, ensuring perfect runtime compatibility.

### 3. Archive & Export
Once built, the script creates a **dereferenced tar archive** (`compiled.tar`).
- **Dereferencing**: Converts all `node_modules` symlinks into real files.
- **Single Artifact**: The entire `compiled/` directory is exported as a single `.tar` file to the host. This avoids re-introducing Windows filesystem issues during the final export.

---

## 🛠️ The 3-Volume Architecture

| Volume Name | Mount Point | Purpose |
|---|---|---|
| `vibe-pnpm-store` | `/pnpm-store` | Global dependency cache for PNPM (persistent across projects). |
| `vibe-n8n-workspace` | `/build` | Workspace where source is extracted, and compilation happens. |
| **Host Volume** | `/out` | Outbound mount used to copy the final `compiled.tar` back to Windows. |

---

## 🧼 Managed Cache (The `--clean` Flag)

- **Standard Build**: Reuses `node_modules` and the `pnpm` store for sub-2-minute rebuilds.
- **`--clean` Build**: 
    1. Purges the local `compiled/` and `build_context/` folders.
    2. Deletes the `vibe-pnpm-store` and `vibe-n8n-workspace` volumes.
    3. Forces a 100% fresh, from-scratch compilation.

---

## 🛠️ Troubleshooting

### Lockfile Configuration Mismatch
If you see `ERR_PNPM_LOCKFILE_CONFIG_MISMATCH`, it means the lockfile is out of sync with an override. The builder automatically uses `--no-frozen-lockfile` to resolve this and syncs the updated lockfile back to your host.

### Postgres Login Failure
If n8n crashes on startup with `password authentication failed`, the persistent DB volume likely has a mismatched password. 
**Fix**: Reset the password in the DB container or prune the database volume (`podman compose down -v`).

---
*Last Updated: April 03, 2026*
