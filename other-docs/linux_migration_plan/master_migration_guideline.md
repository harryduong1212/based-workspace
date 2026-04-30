# Master Migration Guideline (Windows → Fedora)

This is the consolidated checklist and flow used to successfully migrate from Windows 11 to Fedora 43 Workstation.

---

## 1. Pre-Migration Backups (Windows)
- [x] Push all code to Bitbucket / GitHub.
- [x] Export `.env` files from local workspaces.
- [x] Snapshot current Podman data (export database dumps or verify volume location on the `workspace` drive).
- [x] Create Windows 11 Bootable USB (Fallback).
- [x] Create Fedora 43 Live USB.
- [x] Extract system `system_info.json` (captured all apps, drivers, partitions).

## 2. Drive Strategy & Partitioning
Fedora is installed on the primary SSD replacing Windows. The secondary SSD (with `WORKSPACE` and `Games`) was kept intact as NTFS and subsequently remounted in Fedora to ensure zero data loss.

| Drive | Mount Point in Fedora | Filesystem | Content |
|---|---|---|---|
| **Disk 0** (~1TB) | `/` (root), `/home` | BTRFS | Fedora OS, Flatpaks, Home directory, Podman containers |
| **Disk 1** (~1TB) | `/mnt/shared`, `/mnt/games` | NTFS / ext4 | WORKSPACE, Games |

## 3. Installation Flow
- [x] Boot from Fedora Live USB.
- [x] Select Automatic Partitioning for Disk 0 ONLY (overwriting Windows). BTRFS is used by default.
- [x] Connect to Wi-Fi.
- [x] Complete installation and reboot.

## 4. Post-Boot Configuration
- Configure BTRFS subvolumes / snapshots (optional, highly recommended for recovery).
- Modify `/etc/fstab` to automatically mount the secondary data drive (`WORKSPACE`).
  - Example setup for NTFS drive: `UUID=XXXXX /mnt/shared ntfs-3g defaults,uid=1000,gid=1000,dmask=022,fmask=133 0 0`
- Point the symlinks for `~/Workspace` to `/mnt/shared/WORKSPACE`.

## 5. Environment Restoration

### 5.1 Restoring Podman Volumes
*(Note: Full Podman volume raw copy was deemed unnecessary. Instead, recreate the structure and map the shared drive.)*
- Install podman: `sudo dnf install podman podman-compose`
- Re-run the `docker-compose.yml` for all infrastructure layers which points volume mounts to the persisted `~/Workspace` codebase.
- Re-import database dumps (`oracle19`, `postgres`) if necessary.

### 5.2 Restoring Apps
- Follow the `fedora_rebuild_blueprint.md` to reinstall all required tools natively via DNF and Sandboxed via Flatpak.

> [!CAUTION] 
> **Uninstallation Warning:** When removing packages, carefully review the `dnf` or `flatpak` transaction. Removing dependencies might unintentionally break other tools. Always check what "dependent packages" will be removed before confirming `Y`. (See the Vulkan / Howdy incident).

## 6. Verification
- Validate `zsh` is default terminal.
- Test Java 21 native execution (SDKMAN).
- Test Podman networks (`podman network ls`).
- Test Cisco AnyConnect network VPN connects successfully.
- Verify IntelliJ opens natively and fetches Maven dependencies securely via corp proxy.
