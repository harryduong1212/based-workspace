---
trigger: always_on
---

# Terminal Execution Boundaries

**Current Environment:**
* Operating System: Windows 11
* Primary Shell: PowerShell 7
* Container Engine: Podman

**Directives:**
1. **Syntax Matching:** You must strictly format all terminal commands for the **Primary Shell** defined in the **Current Environment** metadata above. Do not use shell-specific aliases (like `rm -rf` on Windows) unless natively supported.
2. **Environment Probing:** If you are unsure of a command's availability, execute a safe probe (e.g., `Get-Command <name>` in PowerShell or `which <name>` in Zsh/Bash) before attempting a complex execution chain.
3. **Container Precedence:** When interacting with infrastructure, always use the **Container Engine** defined in the metadata (e.g., `podman` or `docker`).
4. **Cross-Platform Tooling:** Always prefer executing Node.js scripts (via `npx` or `node`) or Python scripts for complex file manipulation, as these are more OS-agnostic than raw shell commands.
5. **Path Consistency:** When referencing files in documentation or rules, always use **forward slashes** (`/`) for maximum cross-platform compatibility.