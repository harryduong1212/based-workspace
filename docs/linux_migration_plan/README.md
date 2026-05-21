# Linux Migration Plan

This directory contains the authoritative documentation and blueprints generated and updated through the complete migration from Windows 11 to Fedora 43 Workstation.

## Core Documentation

1. **[Master Migration Guideline](master_migration_guideline.md)**
   The high-level flow, checklists, constraints, and data partition migration strategies used during the migration.

2. **[Windows 11 Rebuild Blueprint](windows_11_rebuild_blueprint.md)**
   An exact snapshot of the original Windows 11 state, dependencies, system architecture, and installation flows for safe regression if necessary.

3. **[Fedora 43 Rebuild Blueprint](fedora_rebuild_blueprint.md)**
   The up-to-date definitive guide for exactly reproducing the current Fedora 43 developer environment from scratch, including DNF tools, Flatpak sandboxes, Podman containers, and environment variables.

4. **[Linux Distribution Comparison](linux_distribution_comparison.md)**
   The historical analysis and rationale behind selecting Fedora over alternatives for this specific developer machine.

5. **[Windows to Fedora Translation Guide](windows_to_fedora_guide.md)**
   A comprehensive beginner's guide detailing structural comparisons, package managers, and keyboard shortcuts mapping Windows muscle memory to Fedora GNOME.

---

> **Note:** The old 15+ fragmented migration drafts (`00_...` to `14_...`) have been successfully merged, pruned of obsolete data, and retired in favor of these 5 living documents.
