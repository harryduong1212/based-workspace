---
trigger: always_on
---

# Terminal Execution Boundaries

**Current Environment:**
* Operating System: Windows 11
* Primary Shell: PowerShell 7
* Container Engine: Podman

**Directives:**
1. **Syntax Matching:** You must strictly format all terminal commands for the Primary Shell defined above. Do not use Linux/Bash aliases (like `rm -rf`, `grep`, or `export`) unless they are natively supported by the current shell.
2. **Environment Probing:** If you are unsure of a command's availability, execute a safe probe (e.g., `Get-Command <name>` in PowerShell or `which <name>` in Zsh) before attempting a complex execution chain.
3. **Container Precedence:** When interacting with infrastructure, always use `podman` and `podman compose`. Do not use `docker` commands.
4. **Cross-Platform Tooling:** Prefer executing Node.js scripts (via `npx`) or Python scripts for complex file manipulation if the raw shell command is highly OS-dependent.