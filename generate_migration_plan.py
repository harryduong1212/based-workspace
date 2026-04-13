#!/usr/bin/env python3
"""
Strategic Migration Plan Generator
===================================
Dynamically detects current system hardware and generates 7 detailed
Markdown (.md) files containing the complete, step-by-step implementation
plan for migrating from Windows to Linux while preserving gaming.

Usage:
    python generate_migration_plan.py [--output-dir <path>]
"""

import os
import sys
import json
import platform
import pathlib
import argparse
import subprocess
import datetime
from textwrap import dedent

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
DEFAULT_OUTPUT_DIR = "linux_migration_plan"
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


# ─────────────────────────────────────────────
# System Detection Utilities
# ─────────────────────────────────────────────
def _run_ps(command: str) -> str:
    """Run a PowerShell command and return trimmed stdout."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True, text=True, timeout=15,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def detect_system_info() -> dict:
    """Collect comprehensive system information via PowerShell/WMI."""
    info = {
        "hostname": platform.node(),
        "os": platform.platform(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "generated_at": TIMESTAMP,
    }

    # CPU
    cpu_raw = _run_ps(
        "Get-CimInstance Win32_Processor | "
        "Select-Object Name, NumberOfCores, NumberOfLogicalProcessors | "
        "ConvertTo-Json"
    )
    try:
        cpu = json.loads(cpu_raw)
        if isinstance(cpu, list):
            cpu = cpu[0]
        info["cpu_name"] = cpu.get("Name", "Unknown")
        info["cpu_cores"] = cpu.get("NumberOfCores", "?")
        info["cpu_threads"] = cpu.get("NumberOfLogicalProcessors", "?")
    except Exception:
        info["cpu_name"] = "Unknown"
        info["cpu_cores"] = "?"
        info["cpu_threads"] = "?"

    # RAM
    ram_raw = _run_ps(
        "(Get-CimInstance Win32_PhysicalMemory | "
        "Measure-Object Capacity -Sum).Sum / 1GB"
    )
    try:
        info["ram_gb"] = round(float(ram_raw))
    except Exception:
        info["ram_gb"] = "?"

    # GPU(s)
    gpu_raw = _run_ps(
        "Get-CimInstance Win32_VideoController | "
        "Select-Object Name, @{N='VRAM_GB';E={[math]::Round($_.AdapterRAM/1GB,2)}} | "
        "ConvertTo-Json"
    )
    try:
        gpus = json.loads(gpu_raw)
        if isinstance(gpus, dict):
            gpus = [gpus]
        info["gpus"] = [
            {"name": g.get("Name", "Unknown"), "vram_gb": g.get("VRAM_GB", "?")}
            for g in gpus
        ]
    except Exception:
        info["gpus"] = [{"name": "Unknown", "vram_gb": "?"}]

    # Disks
    disk_raw = _run_ps(
        "Get-CimInstance Win32_DiskDrive | "
        "Select-Object Model, @{N='SizeGB';E={[math]::Round($_.Size/1GB,2)}}, "
        "DeviceID | ConvertTo-Json"
    )
    try:
        disks = json.loads(disk_raw)
        if isinstance(disks, dict):
            disks = [disks]
        info["disks"] = [
            {"model": d.get("Model", "Unknown"), "size_gb": d.get("SizeGB", "?")}
            for d in disks
        ]
    except Exception:
        info["disks"] = []

    # Partitions
    part_raw = _run_ps(
        "Get-Partition | Select-Object DiskNumber, PartitionNumber, DriveLetter, "
        "@{N='SizeGB';E={[math]::Round($_.Size/1GB,2)}}, Type | ConvertTo-Json"
    )
    try:
        parts = json.loads(part_raw)
        if isinstance(parts, dict):
            parts = [parts]
        info["partitions"] = parts
    except Exception:
        info["partitions"] = []

    # BitLocker
    bl_raw = _run_ps(
        "Get-BitLockerVolume -ErrorAction SilentlyContinue | "
        "Select-Object MountPoint, ProtectionStatus | ConvertTo-Json"
    )
    try:
        bl = json.loads(bl_raw)
        if isinstance(bl, dict):
            bl = [bl]
        info["bitlocker"] = bl
    except Exception:
        info["bitlocker"] = []

    # Podman
    podman_containers = _run_ps("podman ps -a --format '{{.Names}}' 2>$null")
    podman_volumes = _run_ps("podman volume ls --format '{{.Name}}' 2>$null")
    podman_images = _run_ps("podman images --format '{{.Repository}}:{{.Tag}}' 2>$null")
    info["podman"] = {
        "containers": [c for c in podman_containers.splitlines() if c.strip()],
        "volumes": [v for v in podman_volumes.splitlines() if v.strip()],
        "images": [i for i in podman_images.splitlines() if i.strip()],
    }

    return info


# ─────────────────────────────────────────────
# Markdown Generators (7 files)
# ─────────────────────────────────────────────

def generate_01_backup(info: dict) -> str:
    """Phase 1: Backup & Fallback Strategy"""
    disk_table_rows = ""
    disks = info.get("disks", [])
    for i, d in enumerate(disks):
        disk_table_rows += f"| Disk {i} | {d['model']} | {d['size_gb']} GB |\n"

    disk0_size = disks[0].get("size_gb", "?") if len(disks) > 0 else "?"
    disk1_size = disks[1].get("size_gb", "?") if len(disks) > 1 else "?"

    return dedent(f"""\
    # Phase 1: Comprehensive Backup & Fallback Strategy (No USB Required)

    > **Generated:** {info['generated_at']}
    > **System:** {info['hostname']} — {info['os']}

    ---

    ## 1.1 Why This Matters

    Repartitioning a drive is a **destructive operation**. If power fails mid-resize,
    or a partition table write goes wrong, you lose everything on that drive.
    A full disk image is your insurance policy.

    ---

    ## 1.2 Your Current Drives

    | Drive | Model | Size |
    |-------|-------|------|
    {disk_table_rows}
    ---

    ## 1.3 Pre-Backup: Disable Windows Safety Features

    Open **PowerShell as Administrator** and run:

    ```powershell
    # Disable Fast Startup (prevents NTFS hibernation lock)
    powercfg /h off

    # Suspend BitLocker if active (prevents encryption lock during resize)
    Suspend-BitLocker -MountPoint C: -RebootCount 0

    # Verify Fast Startup is off
    powercfg /a
    ```

    > Warning: **Fast Startup** makes Windows "hibernate" instead of shutting down.
    > If Linux tries to mount the drive while Windows is hibernated, it will
    > corrupt the NTFS filesystem. **Always disable this before dual-booting.**

    ---

    ## 1.4 USB-Free Disk Imaging Options

    | Method | Tool | Bootable USB Needed? | Restore Without USB? | Best For |
    |---|---|---|---|---|
    | **Option A** | `wbadmin` (built-in) | No | Yes (Windows Recovery) | Disk 0 (Windows) |
    | **Option B** | Macrium Reflect Free | No | Needs rescue media | Full disk images |
    | **Option C** | DISM (built-in) | No | Yes (from WinRE) | Windows partition only |

    ### Option A: Windows Built-in `wbadmin` (Recommended)

    ```powershell
    # Run PowerShell as Administrator

    # 1. Create a full system image to an external drive (E:)
    wbadmin start backup -backupTarget:E: -include:C: -allCritical -quiet

    # 2. Also back up Disk 1 data (H: and I:)
    wbadmin start backup -backupTarget:E: -include:H:,I: -quiet
    ```

    **To restore:** Boot into Windows Recovery Environment
    (Settings -> Recovery -> Advanced Startup) -> Troubleshoot ->
    System Image Recovery -> Select the backup on E:

    ### Option B: Macrium Reflect Free (GUI)

    1. Download from https://www.macrium.com/reflectfree
    2. Create full disk images of both Disk 0 and Disk 1
    3. Save to external drive
    4. **Bonus:** Can create a rescue partition on your existing drive

    ### Prepare External Storage

    You need an external drive with enough space for both disk images:
    - Disk 0: ~{disk0_size} GB (used space, compressed ~40-60%)
    - Disk 1: ~{disk1_size} GB (used space, compressed ~40-60%)

    ---

    ## 1.5 Supplementary: File-Level Backup

    In addition to the full disk image, copy critical files manually:

    ```powershell
    # Create a backup manifest
    $backupDest = "E:\\Migration_Backup"  # Your external drive
    New-Item -ItemType Directory -Path $backupDest -Force

    # Workspace (CRITICAL - your code repos)
    Copy-Item -Path "H:\\WORKSPACE" -Destination "$backupDest\\WORKSPACE" -Recurse -Force

    # Personal files from I:
    Copy-Item -Path "I:\\Harry" -Destination "$backupDest\\Harry" -Recurse -Force

    # Learning materials
    Copy-Item -Path "H:\\Learning" -Destination "$backupDest\\Learning" -Recurse -Force

    # SSH keys and Git config
    Copy-Item -Path "$env:USERPROFILE\\.ssh" -Destination "$backupDest\\.ssh" -Recurse -Force
    Copy-Item -Path "$env:USERPROFILE\\.gitconfig" -Destination "$backupDest\\.gitconfig" -Force

    # VS Code / Antigravity settings
    Copy-Item -Path "$env:APPDATA\\Code\\User\\settings.json" -Destination "$backupDest\\vscode_settings.json" -Force
    Copy-Item -Path "$env:APPDATA\\Code\\User\\keybindings.json" -Destination "$backupDest\\vscode_keybindings.json" -Force

    # Browser bookmarks (Chrome)
    Copy-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Bookmarks" -Destination "$backupDest\\chrome_bookmarks.json" -Force

    # Podman configuration
    if (Test-Path "$env:APPDATA\\containers") {{
        Copy-Item -Path "$env:APPDATA\\containers" -Destination "$backupDest\\podman-config" -Recurse -Force
    }}
    ```

    ---

    ## 1.6 UEFI Settings Snapshot

    Before making changes, take photos of your BIOS/UEFI settings:

    1. Restart -> Enter BIOS (`F2` / `Del`)
    2. Photograph:
       - **Boot Order** screen
       - **Secure Boot** status
       - **SATA/NVMe** mode (AHCI vs RAID)
       - **TPM** settings
    3. Save photos to your phone or external drive

    ---

    ## 1.7 Emergency Rollback Procedure

    If the migration fails at any point:

    1. Boot into Windows Recovery Environment (no USB needed)
    2. Troubleshoot -> System Image Recovery
    3. Select the backup from your external drive
    4. Restore -> Reboot -> Everything is exactly as it was

    > Estimated restore time: 30-45 minutes per drive depending on data size.

    ---

    ## 1.8 Checklist

    - [ ] Fast Startup disabled
    - [ ] BitLocker suspended (if applicable)
    - [ ] External drive ready with sufficient space
    - [ ] Disk 0 image created (wbadmin or Macrium)
    - [ ] Disk 1 image created (wbadmin or Macrium)
    - [ ] H:\\WORKSPACE backed up to external drive
    - [ ] I:\\Harry personal files backed up
    - [ ] Critical files backed up (SSH keys, Git config, bookmarks)
    - [ ] UEFI settings photographed
    - [ ] Steam games on I:\\ moved to C:\\ or noted for re-download
    """)


def generate_02_distro_comparison(info: dict) -> str:
    """Phase 2: Linux Distribution Comparison"""
    gpu_names = ", ".join(g["name"] for g in info.get("gpus", []))

    return dedent(f"""\
    # Phase 2: Linux Distribution Comparison & App Compatibility

    > **Generated:** {info['generated_at']}
    > **Your GPU(s):** {gpu_names}
    > **Your CPU:** {info.get('cpu_name', 'Unknown')}

    ---

    ## 2.1 Distribution Comparison Matrix

    | Criteria | Fedora 42 | Ubuntu 24.04 LTS | Debian 13 | Arch Linux | Linux Mint 22 |
    |---|---|---|---|---|---|
    | **Target Audience** | Modern developers | Beginners/Enterprise | Servers/Stability | Power users | Windows converts |
    | **Release Cycle** | ~6 months | 2 years (LTS) | ~2 years | Rolling release | Follows Ubuntu |
    | **Kernel Version** | ⭐ Latest stable | HWE (recent) | Conservative | ⭐ Bleeding edge | HWE |
    | **Podman Support** | ⭐ Built-in, latest | Manual install | Outdated packages | ⭐ Latest (AUR) | Manual install |
    | **NVIDIA RTX 4060** | ⭐ RPM Fusion (easy) | ubuntu-drivers (easy) | Manual (hard) | nvidia-dkms (medium) | Driver Manager (easy) |
    | **AMD Radeon 890M** | ⭐ Latest mesa | Good | Outdated mesa | ⭐ Latest mesa | Good |
    | **AMD Ryzen AI** | ⭐ Best kernel support | Good | Poor (old kernel) | ⭐ Best via AUR | Moderate |
    | **4K / HiDPI** | ⭐ Wayland-first (GNOME) | Good (X11 default) | Poor scaling | Depends on DE | Poor scaling |
    | **Wayland** | ⭐ Default | Optional | Experimental | Depends on DE | Not default |
    | **Package Manager** | dnf (fast) | apt (familiar) | apt (stable) | pacman (fast) | apt (familiar) |
    | **Flatpak** | ⭐ Pre-installed | Manual | Manual | Manual | Pre-installed |
    | **Community/Docs** | Excellent | ⭐ Largest | Good | ⭐ Arch Wiki | Good |
    | **Stability** | Very stable | ⭐ Rock solid | ⭐ Rock solid | User-dependent | Very stable |
    | **Corporate Backing** | Red Hat (IBM) | Canonical | Community | Community | Community |

    ---

    ## 2.2 Application Compatibility by Distro

    | Application | Fedora | Ubuntu | Debian | Arch | Mint | Install Method |
    |---|---|---|---|---|---|---|
    | **Google Antigravity** | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | RPM repo / .deb |
    | **VS Code** | ✅ | ✅ | ✅ | ✅ | ✅ | Official repo (all distros) |
    | **IntelliJ IDEA** | ✅ | ✅ | ✅ | ✅ | ✅ | Toolbox / Flatpak / Snap |
    | **OBS Studio** | ✅ | ✅ | ⚠️ old | ✅ | ✅ | RPM Fusion / PPA / Flatpak |
    | **Podman** | ⭐ | ✅ | ⚠️ old | ✅ | ✅ | Package manager |
    | **Podman Compose** | ⭐ | ✅ | ⚠️ | ✅ | ✅ | pip / package manager |
    | **Node.js 18+** | ✅ | ✅ | ⚠️ old | ✅ | ✅ | nvm recommended |
    | **Python 3.12+** | ✅ | ✅ | ⚠️ 3.11 | ✅ | ✅ | Pre-installed |
    | **Docker** | ✅ | ✅ | ✅ | ✅ | ✅ | Official repo |
    | **PostgreSQL 16** | ✅ | ✅ | ✅ | ✅ | ✅ | Containerized anyway |
    | **n8n** | ✅ | ✅ | ✅ | ✅ | ✅ | Containerized |
    | **Chrome** | ✅ | ✅ | ✅ | ✅ | ✅ | Google RPM/deb repo |
    | **Firefox** | ⭐ | ✅ | ✅ | ✅ | ✅ | Pre-installed |
    | **Slack** | ✅ | ✅ | ✅ | ✅ | ✅ | Flatpak |
    | **Discord** | ✅ | ✅ | ✅ | ✅ | ✅ | Flatpak |
    | **Spotify** | ✅ | ✅ | ✅ | ✅ | ✅ | Flatpak |

    **Legend:** ⭐ = Best-in-class | ✅ = Works well | ⚠️ = Works but limited/outdated

    ---

    ## 2.3 Apps That Do NOT Fit on ANY Linux Distro

    These applications have **no native Linux version** and cannot be simply installed:

    | Application | Why It Doesn't Fit | Best Workaround | Quality of Workaround |
    |---|---|---|---|
    | **Adobe Photoshop** | Proprietary, Windows/macOS only | GIMP + Krita, or boot into Windows | 🟡 Functional but different UX |
    | **Adobe Premiere Pro** | Proprietary, Windows/macOS only | Kdenlive / DaVinci Resolve (free) | 🟢 DaVinci Resolve is excellent |
    | **Adobe Illustrator** | Proprietary, Windows/macOS only | Inkscape | 🟡 Capable but learning curve |
    | **Microsoft Office** | No native desktop version | LibreOffice / Office 365 Web | 🟢 Web version is near-identical |
    | **NVIDIA GeForce Experience** | Windows-only companion app | `nvidia-smi` + `nvtop` + MangoHud | 🟢 Better for devs actually |
    | **iCloud (desktop)** | Windows/macOS only | icloud.com web interface | 🟡 Limited but functional |
    | **iTunes** | Windows/macOS only | Rhythmbox / Apple Music web | 🟡 Web player works |
    | **Notion (official desktop)** | No official Linux build | `notion-app-enhanced` (community Electron) or web | 🟢 Web version is full-featured |
    | **PowerToys** | Windows-only utilities | GNOME Extensions equivalents | 🟢 Many equivalents exist |
    | **Windows Terminal** | Windows-only | GNOME Terminal / Wezterm / Alacritty | 🟢 Equal or better |

    ---

    ## 2.4 Final Recommendation

    ### 🏆 **Fedora Workstation 42**

    **Why Fedora wins for your setup:**

    1. **Podman is a Fedora project** — Red Hat created Podman, so it's always the latest
       version with full rootless container support out of the box
    2. **Best NVIDIA + AMD hybrid GPU support** — RPM Fusion provides easy `akmod-nvidia`
       that auto-rebuilds on kernel updates (critical for your RTX 4060 + Radeon 890M)
    3. **Wayland-first** — Your 4K display gets crisp rendering in Antigravity, IntelliJ,
       and all Electron apps without manual configuration
    4. **Latest kernel** — Best support for your AMD Ryzen AI 9 HX 370's NPU and
       power management features
    5. **Antigravity has an official RPM repository** — One-command install
    6. **BTRFS by default** — Filesystem snapshots let you roll back system changes,
       acting as a safety net during post-install configuration

    ---

    ## 2.5 Checklist

    - [ ] Reviewed distro comparison matrix
    - [ ] Identified incompatible apps and acceptable workarounds
    - [ ] Confirmed Fedora Workstation 42 as target distro
    - [ ] Downloaded Fedora 42 ISO from https://fedoraproject.org/workstation/download
    """)


def generate_03_partitioning(info: dict) -> str:
    """Phase 3: Drive Partitioning & Dual-Boot Setup"""
    disk0 = info.get("disks", [{}])[0] if info.get("disks") else {"model": "Unknown", "size_gb": "?"}
    disk1 = info.get("disks", [{}])[1] if len(info.get("disks", [])) > 1 else {"model": "Unknown", "size_gb": "?"}
    ram_gb = info.get("ram_gb", 32)
    swap_size = ram_gb + 2 if isinstance(ram_gb, (int, float)) else 34

    return dedent(f"""\
    # Phase 3: Drive Partitioning & Dual-Boot Setup

    > **Generated:** {info['generated_at']}
    > **Disk 0:** {disk0['model']} ({disk0['size_gb']} GB) — Windows
    > **Disk 1:** {disk1['model']} ({disk1['size_gb']} GB) — Linux + Shared

    ---

    ## 3.1 Strategy Overview

    ```
    ┌─────────────────────────────────────────────────────────┐
    │  DISK 0 — {disk0['model']}                              │
    │  ► NO CHANGES — Remains 100% Windows Gaming             │
    │  ┌──────┬───────────────────────────┬──────┬──────┐     │
    │  │ EFI  │     Windows C: (924 GB)   │ Rec  │ Rec  │     │
    │  │250MB │     NTFS — DO NOT TOUCH   │780MB │730MB │     │
    │  └──────┴───────────────────────────┴──────┴──────┘     │
    └─────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │  DISK 1 — {disk1['model']}                                      │
    │  ► REPARTITIONED for Linux + Shared Storage                     │
    │  ┌───────┬──────────┬──────────┬─────────┬──────────────────┐   │
    │  │ EFI   │  / root  │  /home   │  swap   │   /mnt/shared    │   │
    │  │512 MB │ 150 GB   │ 200 GB   │ {swap_size} GB  │   ~548 GB       │   │
    │  │FAT32  │ BTRFS    │ BTRFS    │ swap   │   NTFS           │   │
    │  └───────┴──────────┴──────────┴─────────┴──────────────────┘   │
    └─────────────────────────────────────────────────────────────────┘
    ```

    > ⚠️ **CRITICAL:** Do NOT modify Disk 0 at all. Windows stays untouched.
    > All Linux partitions go on Disk 1. This isolates risk completely.

    ---

    ## 3.2 Partition Details

    | # | Mount Point | Size | Filesystem | Purpose |
    |---|---|---|---|---|
    | 1 | `/boot/efi` | 512 MB | FAT32 | Linux EFI System Partition (separate from Windows EFI) |
    | 2 | `/` | 150 GB | BTRFS | Linux root filesystem (OS, packages, configs) |
    | 3 | `/home` | 200 GB | BTRFS | User data, dotfiles, dev environments |
    | 4 | `[swap]` | {swap_size} GB | Linux Swap | Hibernate + memory overflow (RAM size + 2 GB) |
    | 5 | `/mnt/shared` | ~548 GB | NTFS | Cross-OS shared files (readable by both Windows & Linux) |

    ### Why BTRFS?

    - **Snapshots:** Take instant snapshots before risky changes (like driver updates)
    - **Compression:** Transparent zstd compression saves 20-30% disk space
    - **Rollback:** If a system update breaks something, roll back in seconds
    - **Fedora default:** Fully supported and tested

    ### Why Separate `/home`?

    - If you ever need to reinstall Fedora, your files and configs survive
    - Easier to manage backups of system vs. personal data
    - Can be resized independently

    ---

    ## 3.3 Current Disk 1 Partitions (Will Be Replaced)

    > **⚠️ Back up everything on these partitions BEFORE proceeding:**

    | Partition | Drive Letter | Size | Action |
    |---|---|---|---|
    | System (250 MB) | — | 0.25 GB | Delete |
    | Reserved (16 MB) | — | 0.02 GB | Delete |
    | H: (Basic) | H: | 366.56 GB | **BACKUP then Delete** |
    | I: (Basic) | I: | 562.73 GB | **BACKUP then Delete** |
    | Recovery | — | 1.95 GB | Delete |

    ---

    ## 3.4 Partitioning During Fedora Installation

    During the Fedora installer (Anaconda):

    1. Select **"Custom"** partitioning (not automatic)
    2. Select **Disk 1** only (⚠️ do NOT select Disk 0)
    3. Click **"Delete All"** on Disk 1 (after confirming backup!)
    4. Create partitions in this order:

    ```
    # Partition 1: EFI
    Mount Point: /boot/efi
    Size:        512 MiB
    Filesystem:  EFI System Partition (FAT32)

    # Partition 2: Root
    Mount Point: /
    Size:        150 GiB
    Filesystem:  BTRFS

    # Partition 3: Home
    Mount Point: /home
    Size:        200 GiB
    Filesystem:  BTRFS

    # Partition 4: Swap
    Mount Point: (swap)
    Size:        {swap_size} GiB
    Filesystem:  Linux Swap

    # Partition 5: Shared
    Mount Point: /mnt/shared
    Size:        (remaining space, ~548 GiB)
    Filesystem:  NTFS (or leave blank and format after install)
    ```

    5. Click **"Done"** → Review changes → **"Accept Changes"**

    ---

    ## 3.5 GRUB Bootloader Configuration

    The Fedora installer will install GRUB to Disk 1's EFI partition.

    ### Post-install: Set Boot Order in BIOS

    1. Restart → Enter BIOS (`F2` / `Del`)
    2. Set **Disk 1** as the first boot device
    3. GRUB will appear on every boot with both Fedora and Windows options

    ### Post-install: Verify Windows Detection

    ```bash
    # Ensure GRUB detects Windows
    sudo grub2-mkconfig -o /boot/grub2/grub.cfg

    # Check Windows appears in the boot menu
    grep -i "windows" /boot/grub2/grub.cfg
    # Should output: "Windows Boot Manager (on /dev/nvmeXnXpX)"
    ```

    ---

    ## 3.6 Cross-Compatible Shared Folder Structure

    After installation, create this structure on the NTFS shared partition:

    ```bash
    # From Linux:
    sudo mkdir -p /mnt/shared/{{Documents,Downloads,Media/{{Music,Videos,Pictures}},Learning,Projects/exports,Backups}}

    # Set permissions for your user
    sudo chown -R $(whoami):$(whoami) /mnt/shared/
    ```

    **Resulting structure (accessible from both Windows and Linux):**

    ```
    /mnt/shared/                    (Linux)
    I:\\                             (Windows — after assigning drive letter)
    ├── Documents/                  # Shared documents, PDFs, notes
    ├── Downloads/                  # Cross-OS download landing zone
    ├── Media/
    │   ├── Music/                  # Music library (both OSes)
    │   ├── Videos/                 # Video files, screen recordings
    │   └── Pictures/               # Photos, screenshots
    ├── Learning/                   # Courses, tutorials, reference material
    ├── Projects/
    │   └── exports/                # Podman volume exports, DB dumps
    └── Backups/                    # Clonezilla images, config snapshots
    ```

    > ⚠️ **NEVER place these on the shared NTFS drive:**
    > - Git repositories (NTFS lacks case-sensitivity)
    > - Podman/Docker volumes (NTFS lacks Linux permissions)
    > - Node.js `node_modules` (symlinks break on NTFS)
    > - Python virtual environments (shebangs break)

    ---

    ## 3.7 Auto-Mount Configuration (fstab)

    After Fedora installation, configure automatic mounting:

    ```bash
    # Find the UUID of your NTFS shared partition
    sudo blkid | grep ntfs

    # Add to /etc/fstab (replace UUID with your actual UUID)
    echo "UUID=XXXX-XXXX /mnt/shared ntfs-3g defaults,uid=$(id -u),gid=$(id -g),dmask=022,fmask=133 0 0" | sudo tee -a /etc/fstab

    # Test the mount
    sudo mount -a
    df -h /mnt/shared
    ```

    ---

    ## 3.8 Accessing Shared Drive from Windows

    After installing Linux and creating the shared partition:

    1. Boot into Windows
    2. Open **Disk Management** (`diskmgmt.msc`)
    3. Find the NTFS partition on Disk 1
    4. Right-click → **Change Drive Letter** → Assign `S:` (for "Shared")

    ---

    ## 3.9 Checklist

    - [ ] All data on Disk 1 (H: and I:) backed up to external drive
    - [ ] Fedora ISO downloaded and verified (checksum)
    - [ ] Bootable USB created with Rufus
    - [ ] Custom partitioning applied during install
    - [ ] GRUB installed to Disk 1 EFI
    - [ ] BIOS boot order updated (Disk 1 first)
    - [ ] Windows detected in GRUB menu
    - [ ] Shared NTFS partition mounted and accessible
    - [ ] Folder structure created on shared drive
    """)


def generate_04_podman_migration(info: dict) -> str:
    """Phase 4: Podman Zero-Data-Loss Migration"""
    containers = info.get("podman", {}).get("containers", [])
    volumes = info.get("podman", {}).get("volumes", [])
    images = info.get("podman", {}).get("images", [])

    container_status = "**No active containers detected.**" if not containers else "\n".join(f"- `{c}`" for c in containers)
    volume_status = "**No named volumes detected.**" if not volumes else "\n".join(f"- `{v}`" for v in volumes)
    image_status = "**No images detected.**" if not images else "\n".join(f"- `{i}`" for i in images)

    return dedent(f"""\
    # Phase 4: Podman Zero-Data-Loss Migration

    > **Generated:** {info['generated_at']}
    > **Focus:** Oracle Database container and volume preservation

    ---

    ## 4.1 Current Podman Inventory

    ### Containers
    {container_status}

    ### Volumes
    {volume_status}

    ### Images
    {image_status}

    > 💡 If containers/volumes appear empty, they may be running inside WSL2.
    > Check with: `wsl -d podman-machine-default podman ps -a`

    ---

    ## 4.2 Pre-Migration: Full Inventory Snapshot

    Run these commands **before** migration day to capture everything:

    ```powershell
    # Create export directory on shared drive
    New-Item -ItemType Directory -Path "I:\\Projects\\exports\\podman" -Force
    $exportDir = "I:\\Projects\\exports\\podman"

    # Snapshot all Podman state
    podman ps -a --format json | Out-File "$exportDir\\containers.json" -Encoding utf8
    podman images --format json | Out-File "$exportDir\\images.json" -Encoding utf8
    podman volume ls --format json | Out-File "$exportDir\\volumes.json" -Encoding utf8
    podman network ls --format json | Out-File "$exportDir\\networks.json" -Encoding utf8

    # Inspect every container for recreation commands
    foreach ($container in (podman ps -a --format "{{{{.Names}}}}")) {{
        podman inspect $container | Out-File "$exportDir\\inspect_$container.json" -Encoding utf8
        Write-Host "Inspected: $container"
    }}
    ```

    ---

    ## 4.3 Export Procedure (Windows Side)

    ### Step 1: Stop All Containers Gracefully

    ```powershell
    # Graceful shutdown with 30-second timeout
    podman stop --all --timeout 30

    # Verify everything is stopped
    podman ps
    # Should show no running containers
    ```

    ### Step 2: Export Container Images

    ```powershell
    # Commit running state to images (preserves any runtime changes)
    foreach ($container in (podman ps -a --format "{{{{.Names}}}}")) {{
        podman commit $container "${{container}}-backup:latest"
        Write-Host "Committed: $container"
    }}

    # Save ALL images to tar files
    foreach ($image in (podman images --format "{{{{.Repository}}}}:{{{{.Tag}}}}" | Where-Object {{ $_ -ne "<none>:<none>" }})) {{
        $safeName = $image -replace '[/:]', '_'
        podman save -o "I:\\Projects\\exports\\podman\\image_$safeName.tar" $image
        Write-Host "Saved image: $image"
    }}
    ```

    ### Step 3: Export ALL Named Volumes (Critical for Oracle)

    ```powershell
    # Export each volume to a tar file
    foreach ($vol in (podman volume ls --format "{{{{.Name}}}}")) {{
        podman volume export $vol --output "I:\\Projects\\exports\\podman\\vol_$vol.tar"
        Write-Host "Exported volume: $vol"

        # Also record volume metadata
        podman volume inspect $vol | Out-File "I:\\Projects\\exports\\podman\\vol_${{vol}}_inspect.json" -Encoding utf8
    }}
    ```

    > ⚠️ **ORACLE DATABASE SPECIFIC:**
    > The Oracle data volume typically contains the datafiles, control files,
    > and redo logs. The `podman volume export` command captures ALL of this
    > as a complete tar archive, preserving the byte-perfect state.

    ### Step 4: Export Podman Networks

    ```powershell
    foreach ($net in (podman network ls --format "{{{{.Name}}}}" | Where-Object {{ $_ -ne "podman" }})) {{
        podman network inspect $net | Out-File "I:\\Projects\\exports\\podman\\net_$net.json" -Encoding utf8
        Write-Host "Exported network config: $net"
    }}
    ```

    ### Step 5: Verify Export Integrity

    ```powershell
    # List all exported files with sizes
    Get-ChildItem "I:\\Projects\\exports\\podman" | Format-Table Name, Length -AutoSize

    # Verify tar files are valid
    foreach ($tar in (Get-ChildItem "I:\\Projects\\exports\\podman\\*.tar")) {{
        $testResult = tar -tf $tar.FullName 2>&1 | Select-Object -First 3
        if ($LASTEXITCODE -eq 0) {{
            Write-Host "✅ Valid: $($tar.Name)"
        }} else {{
            Write-Host "❌ CORRUPT: $($tar.Name) — RE-EXPORT THIS FILE"
        }}
    }}
    ```

    ---

    ## 4.4 Import Procedure (Linux Side)

    ### Step 1: Verify Podman is Installed

    ```bash
    # Fedora comes with Podman pre-installed
    podman --version
    podman info | head -20
    ```

    ### Step 2: Load Container Images

    ```bash
    EXPORT_DIR="/mnt/shared/Projects/exports/podman"

    # Load all saved images
    for img_tar in "$EXPORT_DIR"/image_*.tar; do
        echo "Loading: $(basename $img_tar)"
        podman load -i "$img_tar"
    done

    # Verify images loaded
    podman images
    ```

    ### Step 3: Recreate and Import Volumes

    ```bash
    # Import all volumes
    for vol_tar in "$EXPORT_DIR"/vol_*.tar; do
        vol_name=$(basename "$vol_tar" .tar | sed 's/^vol_//')
        echo "Creating volume: $vol_name"
        podman volume create "$vol_name"
        podman volume import "$vol_name" "$vol_tar"
        echo "✅ Imported: $vol_name"
    done

    # Verify volumes
    podman volume ls
    ```

    ### Step 4: Fix Oracle UID/GID Permissions (CRITICAL)

    ```bash
    # Oracle Database runs as UID 54321 (oracle) inside the container.
    # Windows WSL2 uses different UID mappings than native Linux.
    # This command fixes ownership so Oracle can read its datafiles.

    podman unshare chown -R 54321:54321 \\
        ~/.local/share/containers/storage/volumes/oracle_data_vol/_data

    # Verify the fix
    podman unshare ls -la \\
        ~/.local/share/containers/storage/volumes/oracle_data_vol/_data
    # All files should show oracle:oinstall (54321:54321)
    ```

    > 🚨 **If you skip this step, Oracle will fail with:**
    > - `ORA-00221: error on write to control file`
    > - `Permission denied` errors
    > - Container exits immediately after start

    ### Step 5: Recreate Networks

    ```bash
    # Recreate custom networks from exported configs
    for net_json in "$EXPORT_DIR"/net_*.json; do
        net_name=$(basename "$net_json" .json | sed 's/^net_//')
        echo "Creating network: $net_name"
        podman network create "$net_name" 2>/dev/null || echo "Network exists"
    done
    ```

    ### Step 6: Recreate Containers

    ```bash
    # Use the inspect JSON files to reconstruct podman run commands
    # Example for Oracle DB:
    podman run -d \\
        --name oracle-db-container \\
        -p 1521:1521 \\
        -p 5500:5500 \\
        -v oracle_data_vol:/opt/oracle/oradata \\
        -e ORACLE_PWD=YourSecurePassword \\
        oracle-db-backup:latest

    # For based-workspace infrastructure (postgres + n8n):
    # Use your existing docker-compose.yaml
    cd /path/to/based-workspace/infrastructure/core
    podman compose --env-file ../../.env -f docker-compose.yaml up -d
    ```

    ---

    ## 4.5 Oracle Database Validation

    ```bash
    # Wait for Oracle to fully initialize (can take 60-120 seconds)
    echo "Waiting for Oracle to start..."
    sleep 90

    # Check container health
    podman logs oracle-db-container --tail 50

    # Test database connectivity
    podman exec -it oracle-db-container sqlplus / as sysdba <<'EOF'
    -- Check instance status
    SELECT INSTANCE_NAME, STATUS, DATABASE_STATUS FROM V$INSTANCE;

    -- Check datafile integrity
    SELECT FILE#, STATUS, NAME FROM V$DATAFILE;

    -- Count user tables (verify data survived)
    SELECT COUNT(*) AS total_tables FROM DBA_TABLES WHERE OWNER NOT IN ('SYS','SYSTEM');

    -- Check for corruption
    SELECT * FROM V$DATABASE_BLOCK_CORRUPTION;

    EXIT;
    EOF
    ```

    ### Expected Output
    - Instance STATUS: `OPEN`
    - DATABASE_STATUS: `ACTIVE`
    - All datafiles STATUS: `ONLINE`
    - Block corruption: **0 rows** (no corruption)

    ---

    ## 4.6 Troubleshooting

    | Symptom | Cause | Fix |
    |---|---|---|
    | `ORA-00221` | Wrong file permissions | `podman unshare chown -R 54321:54321 <volume_path>` |
    | `Permission denied` | UID mismatch | Same as above |
    | Container won't start | Missing volume | Check `podman volume ls` and re-import |
    | `ORA-01157` | Missing datafile | Verify tar export was complete |
    | Network errors | Missing network | `podman network create <name>` |
    | Image not found | Failed load | Re-run `podman load -i <tar>` |

    ---

    ## 4.7 Checklist

    - [ ] Pre-migration inventory snapshot taken (JSON files)
    - [ ] All containers stopped gracefully
    - [ ] All containers committed to backup images
    - [ ] All images saved as .tar files
    - [ ] All volumes exported as .tar files
    - [ ] All network configs exported
    - [ ] Export integrity verified (tar -tf)
    - [ ] Images loaded on Linux
    - [ ] Volumes created and imported on Linux
    - [ ] Oracle UID/GID permissions fixed
    - [ ] Networks recreated on Linux
    - [ ] Containers recreated on Linux
    - [ ] Oracle instance status: OPEN
    - [ ] Oracle datafiles: all ONLINE
    - [ ] Oracle block corruption check: 0 rows
    """)


def generate_05_linux_install(info: dict) -> str:
    """Phase 5: Linux Installation & Post-Boot Sequence"""
    return dedent(f"""\
    # Phase 5: Fedora Installation & Immediate Post-Boot Sequence

    > **Generated:** {info['generated_at']}
    > **Target OS:** Fedora Workstation 42
    > **Priority:** Install Google Antigravity BEFORE other app configuration

    ---

    ## 5.1 Installation Media Preparation

    ### Download Fedora 42

    1. Visit: https://fedoraproject.org/workstation/download
    2. Download the **x86_64 ISO** (~2.2 GB)
    3. Verify checksum:
       ```powershell
       # In Windows PowerShell:
       Get-FileHash Fedora-Workstation-Live-x86_64-42.iso -Algorithm SHA256
       # Compare with checksum on download page
       ```

    ### Create Bootable USB

    1. Download Rufus: https://rufus.ie
    2. Insert USB drive (≥ 4 GB)
    3. Open Rufus:
       - Device: Your USB drive
       - Boot selection: The Fedora ISO
       - Partition scheme: **GPT**
       - Target system: **UEFI (non CSM)**
       - File system: FAT32
    4. Click **START** → Wait for completion

    ---

    ## 5.2 BIOS/UEFI Configuration

    Before booting from USB:

    1. Restart → Enter BIOS (`F2` / `Del` / `F12` depending on laptop)
    2. **Disable Secure Boot** (temporarily — can re-enable later)
    3. Set USB as first boot device
    4. Save & Exit

    ---

    ## 5.3 Fedora Installation

    1. Boot from USB → Select **"Start Fedora Workstation Live"**
    2. Click **"Install to Hard Drive"**
    3. **Language:** English (or your preference)
    4. **Keyboard:** Your layout
    5. **Installation Destination:**
       - Select **Disk 1 ONLY** (⚠️ do NOT select Disk 0)
       - Choose **"Custom"** partitioning
       - Apply the partition layout from Phase 3
    6. **User Creation:**
       - Full Name: Your name
       - Username: `harry` (or your preference)
       - Password: Strong password
       - Check **"Make this user administrator"**
    7. Click **"Begin Installation"**
    8. Wait for completion (~10-15 minutes)
    9. Click **"Finish Installation"** → Reboot
    10. Remove USB drive when prompted

    ---

    ## 5.4 First Boot Configuration

    After rebooting into Fedora for the first time:

    1. Complete the **GNOME Welcome** wizard
    2. Connect to WiFi/Ethernet
    3. Skip online accounts (configure later)
    4. Enable **Location Services** if desired
    5. Click **"Start Using Fedora"**

    ---

    ## 5.5 Immediate Post-Boot Sequence

    > **Execute these steps in exact order. Do NOT skip or reorder.**

    ### Step 1: Full System Update

    ```bash
    # Update all packages to latest versions
    sudo dnf upgrade --refresh -y

    # Reboot to apply kernel updates
    sudo reboot
    ```

    ### Step 2: Enable RPM Fusion Repositories

    ```bash
    # RPM Fusion provides NVIDIA drivers, multimedia codecs, and more
    sudo dnf install -y \\
        https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \\
        https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

    # Verify
    dnf repolist | grep rpmfusion
    ```

    ### Step 3: Install NVIDIA Drivers

    ```bash
    # Install NVIDIA proprietary drivers (for RTX 4060)
    sudo dnf install -y akmod-nvidia xorg-x11-drv-nvidia-cuda

    # Force build kernel modules
    sudo akmods --force

    # Regenerate initramfs
    sudo dracut --force

    # Reboot to load new driver
    sudo reboot

    # After reboot — verify NVIDIA is working
    nvidia-smi
    # Should display: NVIDIA GeForce RTX 4060 Laptop GPU
    ```

    ### Step 4: ⭐ INSTALL GOOGLE ANTIGRAVITY (Priority!)

    ```bash
    # Add the Antigravity RPM repository
    sudo tee /etc/yum.repos.d/antigravity.repo << 'EOL'
    [antigravity-rpm]
    name=Antigravity RPM Repository
    baseurl=https://us-central1-yum.pkg.dev/projects/antigravity-auto-updater-dev/antigravity-rpm
    enabled=1
    gpgcheck=0
    EOL

    # Refresh package cache and install
    sudo dnf makecache
    sudo dnf install -y antigravity

    # Verify installation
    antigravity --version

    # Launch Antigravity
    antigravity
    ```

    > 🎉 **Antigravity is now installed!** Continue with the remaining setup below.

    ### Step 5: Configure Antigravity

    ```bash
    # Fix 4K/HiDPI rendering (if text appears blurry)
    # Open Antigravity → Help → Edit Custom VM Options → Add:
    # -Dawt.toolkit.name=WLToolkit
    # Then restart Antigravity

    # Enable VS Code Marketplace extensions:
    # Open Antigravity → Settings (JSON) → Add:
    ```

    ```json
    {{
      "extensions.gallery": {{
        "serviceUrl": "https://marketplace.visualstudio.com/_apis/public/gallery",
        "itemUrl": "https://marketplace.visualstudio.com/items"
      }}
    }}
    ```

    ```bash
    # Install "Antigravity Settings Sync" extension
    # Use it to pull your VS Code settings from Windows
    ```

    ### Step 6: Mount Shared NTFS Partition

    ```bash
    # Create mount point
    sudo mkdir -p /mnt/shared

    # Find the UUID of your NTFS partition
    sudo blkid | grep ntfs
    # Example output: /dev/nvme1n1p5: UUID="ABCD1234" TYPE="ntfs"

    # Add to fstab for automatic mounting
    NTFS_UUID=$(sudo blkid -s UUID -o value /dev/nvme1n1p5)
    echo "UUID=$NTFS_UUID /mnt/shared ntfs-3g defaults,uid=$(id -u),gid=$(id -g),dmask=022,fmask=133 0 0" | sudo tee -a /etc/fstab

    # Mount immediately
    sudo mount -a

    # Verify
    ls /mnt/shared/
    df -h /mnt/shared
    ```

    ### Step 7: Install Essential Development Tools

    ```bash
    sudo dnf install -y \\
        git curl wget unzip tar \\
        python3 python3-pip python3-venv \\
        nodejs npm \\
        podman podman-compose \\
        htop btop nvtop \\
        gnome-tweaks gnome-extensions-app \\
        wl-clipboard \\
        fontconfig google-noto-fonts-common \\
        make gcc gcc-c++ kernel-devel

    # Install nvm for Node.js version management (optional)
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
    source ~/.bashrc
    nvm install --lts
    ```

    ### Step 8: Configure Git

    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    git config --global core.editor "antigravity --wait"
    git config --global init.defaultBranch main

    # Copy SSH keys from backup
    cp -r /mnt/shared/Backups/.ssh ~/.ssh
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/id_*
    chmod 644 ~/.ssh/*.pub
    ```

    ### Step 9: Verify GRUB Detects Windows

    ```bash
    # Update GRUB configuration
    sudo grub2-mkconfig -o /boot/grub2/grub.cfg

    # Verify Windows is listed
    grep -i "windows" /boot/grub2/grub.cfg
    # Expected: menuentry 'Windows Boot Manager (on /dev/nvmeXnXpX)'
    ```

    ---

    ## 5.6 Verification Dashboard

    Run this all-in-one check after completing the sequence:

    ```bash
    echo "═══════════════════════════════════════"
    echo "  Post-Boot Verification Dashboard"
    echo "═══════════════════════════════════════"
    echo ""
    echo "OS:           $(cat /etc/fedora-release)"
    echo "Kernel:       $(uname -r)"
    echo "NVIDIA:       $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'NOT DETECTED')"
    echo "Antigravity:  $(antigravity --version 2>/dev/null || echo 'NOT INSTALLED')"
    echo "Podman:       $(podman --version)"
    echo "Git:          $(git --version)"
    echo "Python:       $(python3 --version)"
    echo "Node.js:      $(node --version 2>/dev/null || echo 'NOT INSTALLED')"
    echo "Shared Drive: $(df -h /mnt/shared --output=avail 2>/dev/null | tail -1 || echo 'NOT MOUNTED')"
    echo "Windows Boot: $(grep -c 'Windows' /boot/grub2/grub.cfg 2>/dev/null || echo '0') entries found"
    echo ""
    echo "═══════════════════════════════════════"
    ```

    ---

    ## 5.7 Checklist

    - [ ] Fedora ISO downloaded and verified
    - [ ] Bootable USB created with Rufus
    - [ ] Secure Boot disabled in BIOS
    - [ ] Fedora installed with custom partitions on Disk 1
    - [ ] First boot wizard completed
    - [ ] System fully updated (`dnf upgrade`)
    - [ ] RPM Fusion enabled
    - [ ] NVIDIA drivers installed and verified (`nvidia-smi`)
    - [ ] **Google Antigravity installed and launched**
    - [ ] Antigravity 4K fix applied
    - [ ] VS Code Marketplace enabled in Antigravity
    - [ ] Shared NTFS partition mounted
    - [ ] Dev tools installed (Git, Python, Node, Podman)
    - [ ] Git configured with SSH keys
    - [ ] Windows detected in GRUB menu
    """)


def generate_06_app_migration(info: dict) -> str:
    """Phase 6: App Migration & Incompatibility Workarounds"""
    return dedent(f"""\
    # Phase 6: App Migration, Backend Tools & Incompatibility Workarounds

    > **Generated:** {info['generated_at']}

    ---

    ## 6.1 Backend Development Tools

    ### Google Antigravity (Already Installed in Phase 5)

    Configuration checklist:

    ```bash
    # 1. HiDPI/4K Fix (if needed)
    # Antigravity → Help → Edit Custom VM Options → Add:
    -Dawt.toolkit.name=WLToolkit

    # 2. Enable VS Code Marketplace
    # settings.json:
    {{
      "extensions.gallery": {{
        "serviceUrl": "https://marketplace.visualstudio.com/_apis/public/gallery",
        "itemUrl": "https://marketplace.visualstudio.com/items"
      }}
    }}

    # 3. Sync Settings from Windows
    # Install "Antigravity Settings Sync" → Pull cloud settings

    # 4. Install key extensions:
    # - Python
    # - ESLint / Prettier
    # - GitLens
    # - Docker / Podman
    # - Remote SSH
    # - Thunder Client (REST API)
    ```

    ---

    ### VS Code (Supplementary — if needed alongside Antigravity)

    ```bash
    # Add Microsoft VS Code repository
    sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
    sudo tee /etc/yum.repos.d/vscode.repo << 'EOL'
    [code]
    name=Visual Studio Code
    baseurl=https://packages.microsoft.com/yumrepos/vscode
    enabled=1
    gpgcheck=1
    gpgkey=https://packages.microsoft.com/keys/microsoft.asc
    EOL

    # Install
    sudo dnf install -y code

    # Fix 4K rendering
    # Same as Antigravity: Add to VM options
    ```

    ---

    ### IntelliJ IDEA

    ```bash
    # Option A: JetBrains Toolbox (Recommended — manages updates)
    curl -fsSL https://raw.githubusercontent.com/nagygergo/jetbrains-toolbox-install/master/jetbrains-toolbox.sh | bash
    # Then open Toolbox → Install IntelliJ IDEA

    # Option B: Flatpak
    flatpak install flathub com.jetbrains.IntelliJ-IDEA-Ultimate -y

    # Option C: Direct download
    # Visit: https://www.jetbrains.com/idea/download/?section=linux
    ```

    **Post-install configuration:**

    ```bash
    # Fix 4K/Wayland rendering
    # IntelliJ → Help → Edit Custom VM Options → Add:
    -Dawt.toolkit.name=WLToolkit

    # Import settings from Windows:
    # File → Manage IDE Settings → Import Settings → Select exported zip
    ```

    > 💡 **Export your IntelliJ settings on Windows first:**
    > File → Manage IDE Settings → Export Settings → Save to shared drive

    ---

    ### OBS Studio

    ```bash
    # Install from RPM Fusion (best integration)
    sudo dnf install -y obs-studio

    # OR via Flatpak (sandboxed)
    flatpak install flathub com.obsproject.Studio -y
    ```

    **Fedora OBS advantages:**
    - PipeWire integration for Wayland screen capture (no XComposite needed)
    - NVIDIA NVENC hardware encoding works out of the box
    - No additional plugins needed for screen recording

    **Import OBS settings from Windows:**
    ```bash
    # Copy from Windows backup:
    cp -r /mnt/shared/Backups/obs-studio ~/.config/obs-studio
    ```

    ---

    ### Podman & Container Infrastructure

    ```bash
    # Already installed in Phase 5, verify:
    podman --version
    podman-compose --version

    # Configure rootless containers
    sudo loginctl enable-linger $(whoami)

    # Test with a simple container
    podman run --rm hello-world
    ```

    ---

    ## 6.2 Daily Applications

    | Application | Install Command | Notes |
    |---|---|---|
    | **Firefox** | Pre-installed | Default browser on Fedora |
    | **Chrome** | See below | Google RPM repo |
    | **Slack** | `flatpak install flathub com.slack.Slack` | Desktop notifications work |
    | **Discord** | `flatpak install flathub com.discordapp.Discord` | Voice/video works |
    | **Spotify** | `flatpak install flathub com.spotify.Client` | Wayland native |
    | **Zoom** | `flatpak install flathub us.zoom.Zoom` | Screen sharing works |
    | **Telegram** | `flatpak install flathub org.telegram.desktop` | Native Linux app |
    | **VLC** | `sudo dnf install vlc` | Plays everything |
    | **GIMP** | `sudo dnf install gimp` | Photoshop alternative |
    | **LibreOffice** | Pre-installed | MS Office alternative |
    | **Thunderbird** | `sudo dnf install thunderbird` | Email client |
    | **FileZilla** | `sudo dnf install filezilla` | FTP client |
    | **Postman** | `flatpak install flathub com.getpostman.Postman` | API testing |

    ### Google Chrome Installation

    ```bash
    # Add Google Chrome repository
    sudo dnf install -y fedora-workstation-repositories
    sudo dnf config-manager --set-enabled google-chrome

    # Install Chrome
    sudo dnf install -y google-chrome-stable
    ```

    ---

    ## 6.3 Terminal & Shell Setup

    ```bash
    # Install modern terminal tools
    sudo dnf install -y \\
        zsh \\
        tmux \\
        ripgrep \\
        fd-find \\
        bat \\
        eza \\
        fzf \\
        jq \\
        yq

    # Optional: Install Oh My Zsh
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

    # Install Starship prompt (cross-shell)
    curl -sS https://starship.rs/install.sh | sh
    ```

    ---

    ## 6.4 PowerShell on Linux (for compatibility)

    ```bash
    # Microsoft provides PowerShell for Linux
    sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
    curl https://packages.microsoft.com/config/rhel/9/prod.repo | sudo tee /etc/yum.repos.d/microsoft-prod.repo
    sudo dnf install -y powershell

    # Launch: pwsh
    pwsh --version
    ```

    > 💡 This lets you run your existing PowerShell scripts during the transition period.

    ---

    ## 6.5 Completely Incompatible Apps & Workarounds

    | Application | Issue | Recommended Workaround | Setup Command |
    |---|---|---|---|
    | **Adobe Photoshop** | No Linux version, Wine unreliable | **GIMP** (free) or **Photopea.com** (web) | `sudo dnf install gimp` |
    | **Adobe Premiere Pro** | No Linux version | **DaVinci Resolve** (free, professional) | Download from blackmagicdesign.com |
    | **Adobe Illustrator** | No Linux version | **Inkscape** (free, SVG-native) | `sudo dnf install inkscape` |
    | **Microsoft Office** | No native Linux desktop | **LibreOffice** or **Office 365 Web** | Pre-installed / browser |
    | **Microsoft Outlook** | No native Linux | **Thunderbird** or Outlook Web | `sudo dnf install thunderbird` |
    | **Nvidia GeForce Exp.** | Windows-only | `nvidia-smi` + `nvtop` | `sudo dnf install nvtop` |
    | **iCloud Desktop** | Windows/macOS only | **icloud.com** in browser | N/A |
    | **iTunes Desktop** | Windows/macOS only | **Apple Music Web** or **Rhythmbox** | `sudo dnf install rhythmbox` |
    | **Notion Desktop** | No official Linux build | **notion-app-enhanced** or **Web** | `npm i -g notion-enhancer` |
    | **PowerToys** | Windows-only utilities | **GNOME Extensions** ecosystem | `sudo dnf install gnome-extensions-app` |
    | **Windows Terminal** | Windows-only | **GNOME Terminal** / **Wezterm** | Pre-installed / `dnf install wezterm` |
    | **Task Manager** | Windows-only | **GNOME System Monitor** + `btop` | `sudo dnf install btop` |

    ---

    ## 6.6 Bulk Installation Script

    Run this to install everything at once:

    ```bash
    #!/bin/bash
    echo "═══════════════════════════════════════"
    echo "  Installing all applications..."
    echo "═══════════════════════════════════════"

    # DNF packages
    sudo dnf install -y \\
        obs-studio vlc gimp inkscape thunderbird filezilla \\
        zsh tmux ripgrep fd-find bat eza fzf jq yq \\
        htop btop nvtop \\
        gnome-tweaks gnome-extensions-app

    # Chrome
    sudo dnf install -y fedora-workstation-repositories
    sudo dnf config-manager --set-enabled google-chrome
    sudo dnf install -y google-chrome-stable

    # Flatpak apps
    flatpak install -y flathub \\
        com.slack.Slack \\
        com.discordapp.Discord \\
        com.spotify.Client \\
        us.zoom.Zoom \\
        org.telegram.desktop \\
        com.getpostman.Postman

    echo ""
    echo "✅ All applications installed!"
    echo "═══════════════════════════════════════"
    ```

    ---

    ## 6.7 Checklist

    - [ ] Google Antigravity configured (4K fix, Marketplace, settings sync)
    - [ ] IntelliJ IDEA installed and configured
    - [ ] OBS Studio installed
    - [ ] VS Code installed (if needed alongside Antigravity)
    - [ ] Chrome installed
    - [ ] Flatpak apps installed (Slack, Discord, Spotify, etc.)
    - [ ] Terminal tools installed (zsh, tmux, ripgrep, etc.)
    - [ ] Git configured with SSH keys
    - [ ] Podman verified working
    - [ ] Incompatible app workarounds documented and alternatives installed
    """)


def generate_07_master_checklist(info: dict) -> str:
    """Phase 7: Master Migration Checklist & Verification"""
    return dedent(f"""\
    # Phase 7: Master Migration Checklist & Post-Migration Verification

    > **Generated:** {info['generated_at']}
    > **System:** {info.get('cpu_name', 'Unknown')} / {info.get('ram_gb', '?')} GB RAM
    > **Migration Path:** Windows 11 → Fedora Workstation 42 (dual-boot)

    ---

    ## 7.1 Pre-Migration Checklist

    ### Backup & Preparation
    - [ ] Fast Startup disabled in Windows
    - [ ] BitLocker suspended (if applicable)
    - [ ] UEFI/BIOS settings photographed
    - [ ] Clonezilla USB created
    - [ ] External drive ready (sufficient space for both disk images)
    - [ ] **Disk 0 full image created** (Clonezilla)
    - [ ] **Disk 1 full image created** (Clonezilla)
    - [ ] Images verified (checksum integrity)
    - [ ] Critical files backed up (SSH keys, Git config, browser bookmarks)
    - [ ] Podman inventory snapshot taken
    - [ ] Podman images saved as .tar
    - [ ] Podman volumes exported as .tar
    - [ ] IntelliJ settings exported
    - [ ] VS Code / Antigravity settings synced to cloud
    - [ ] OBS settings backed up

    ### Preparation Complete?
    **→ Only proceed to installation when ALL items above are checked.**

    ---

    ## 7.2 Installation Checklist

    - [ ] Fedora 42 ISO downloaded and checksum verified
    - [ ] Bootable USB created (Rufus, GPT/UEFI mode)
    - [ ] Secure Boot disabled in BIOS
    - [ ] Booted from Fedora USB
    - [ ] **Custom partitioning on Disk 1 ONLY**
    - [ ] Partitions created: EFI (512MB), / (150GB), /home (200GB), swap ({info.get('ram_gb', 32)}+2 GB), shared (NTFS)
    - [ ] User account created (with admin privileges)
    - [ ] Installation completed
    - [ ] USB removed and system rebooted

    ---

    ## 7.3 Post-Boot Sequence Checklist

    Execute in exact order:

    - [ ] GNOME welcome wizard completed
    - [ ] Network connected
    - [ ] `sudo dnf upgrade --refresh -y` → Reboot
    - [ ] RPM Fusion repositories enabled
    - [ ] NVIDIA drivers installed (`akmod-nvidia`) → Reboot
    - [ ] `nvidia-smi` shows RTX 4060 ✓
    - [ ] **Google Antigravity installed via RPM repo** ✓
    - [ ] Antigravity 4K fix applied ✓
    - [ ] VS Code Marketplace enabled ✓
    - [ ] Shared NTFS partition mounted at `/mnt/shared` ✓
    - [ ] Development tools installed (Git, Python, Node, Podman)
    - [ ] Git configured with SSH keys

    ---

    ## 7.4 App Migration Checklist

    - [ ] IntelliJ IDEA installed (Toolbox / Flatpak)
    - [ ] IntelliJ 4K fix applied
    - [ ] IntelliJ settings imported from backup
    - [ ] OBS Studio installed
    - [ ] OBS settings restored from backup
    - [ ] Chrome installed
    - [ ] Flatpak apps installed (Slack, Discord, Spotify)
    - [ ] Terminal tools installed (zsh, tmux, ripgrep, etc.)

    ---

    ## 7.5 Container Migration Checklist

    - [ ] Podman images loaded from .tar
    - [ ] Podman volumes imported from .tar
    - [ ] Oracle UID/GID permissions fixed (`podman unshare chown`)
    - [ ] Networks recreated
    - [ ] Containers recreated and started
    - [ ] Oracle DB instance status: OPEN
    - [ ] Oracle datafiles: all ONLINE
    - [ ] Oracle corruption check: 0 rows
    - [ ] based-workspace infrastructure running (postgres + n8n)

    ---

    ## 7.6 Dual-Boot Verification

    - [ ] GRUB menu shows Fedora as default
    - [ ] GRUB menu shows Windows Boot Manager
    - [ ] Can boot into Windows successfully
    - [ ] Can boot back into Fedora successfully
    - [ ] Windows gaming works normally
    - [ ] Shared NTFS drive accessible from Windows
    - [ ] Shared NTFS drive accessible from Linux

    ---

    ## 7.7 Final Verification Script

    Run this comprehensive check after completing everything:

    ```bash
    #!/bin/bash
    echo "╔═══════════════════════════════════════════════════╗"
    echo "║     MIGRATION VERIFICATION DASHBOARD             ║"
    echo "╠═══════════════════════════════════════════════════╣"

    # System
    printf "║ %-20s %s\\n" "OS:" "$(cat /etc/fedora-release)"
    printf "║ %-20s %s\\n" "Kernel:" "$(uname -r)"
    printf "║ %-20s %s\\n" "Desktop:" "$XDG_CURRENT_DESKTOP ($XDG_SESSION_TYPE)"

    # Hardware
    printf "║ %-20s %s\\n" "CPU:" "$(lscpu | grep 'Model name' | sed 's/.*: *//')"
    printf "║ %-20s %s\\n" "RAM:" "$(free -h | awk '/Mem/{{print $2}}')"

    # GPU
    if command -v nvidia-smi &>/dev/null; then
        printf "║ %-20s %s\\n" "NVIDIA GPU:" "$(nvidia-smi --query-gpu=name --format=csv,noheader)"
        echo "║  ✅ NVIDIA driver loaded"
    else
        echo "║  ❌ NVIDIA driver NOT detected"
    fi

    # Applications
    echo "║"
    echo "║ Applications:"
    for app in antigravity code idea obs podman git python3 node; do
        if command -v $app &>/dev/null; then
            ver=$($app --version 2>/dev/null | head -1)
            printf "║   ✅ %-15s %s\\n" "$app" "$ver"
        else
            printf "║   ❌ %-15s NOT FOUND\\n" "$app"
        fi
    done

    # Storage
    echo "║"
    echo "║ Storage:"
    if mountpoint -q /mnt/shared 2>/dev/null; then
        avail=$(df -h /mnt/shared --output=avail | tail -1 | tr -d ' ')
        printf "║   ✅ Shared drive:   %s available\\n" "$avail"
    else
        echo "║   ❌ Shared drive NOT mounted"
    fi

    # Boot
    echo "║"
    echo "║ Dual-Boot:"
    win_entries=$(grep -c "Windows" /boot/grub2/grub.cfg 2>/dev/null || echo 0)
    if [ "$win_entries" -gt 0 ]; then
        printf "║   ✅ Windows Boot:   %s entries in GRUB\\n" "$win_entries"
    else
        echo "║   ❌ Windows NOT detected in GRUB"
    fi

    # Containers
    echo "║"
    echo "║ Containers:"
    pod_containers=$(podman ps -a --format "{{{{.Names}}}}" 2>/dev/null | wc -l)
    pod_volumes=$(podman volume ls --format "{{{{.Name}}}}" 2>/dev/null | wc -l)
    pod_images=$(podman images --format "{{{{.Repository}}}}" 2>/dev/null | wc -l)
    printf "║   Containers: %s | Volumes: %s | Images: %s\\n" "$pod_containers" "$pod_volumes" "$pod_images"

    echo "║"
    echo "╚═══════════════════════════════════════════════════╝"
    ```

    ---

    ## 7.8 Troubleshooting Quick Reference

    | Issue | Solution |
    |---|---|
    | Black screen after NVIDIA install | Boot with `nomodeset` kernel param, reinstall drivers |
    | Blurry text in Antigravity/IntelliJ | Add `-Dawt.toolkit.name=WLToolkit` to VM options |
    | Shared drive not mounting | Check `/etc/fstab` UUID, install `ntfs-3g` |
    | Windows not in GRUB | Run `sudo grub2-mkconfig -o /boot/grub2/grub.cfg` |
    | Podman permission denied | `podman unshare chown` or check SELinux with `ausearch -m avc` |
    | No sound | Install PipeWire: `sudo dnf install pipewire wireplumber` |
    | WiFi not working | Check: `sudo dnf install kernel-modules-extra` |
    | Flatpak apps not opening | Run: `flatpak repair` |

    ---

    ## 7.9 Estimated Timeline

    | Phase | Duration | Cumulative |
    |---|---|---|
    | Phase 1: Backup | 1-2 hours | 1-2 hours |
    | Phase 2: Distro selection | 15 minutes | ~2 hours |
    | Phase 3: Partitioning (during install) | 30 minutes | ~2.5 hours |
    | Phase 4: Podman export (Windows) | 30-60 minutes | ~3.5 hours |
    | Phase 5: Linux install + post-boot | 1-2 hours | ~5.5 hours |
    | Phase 6: App setup | 1-2 hours | ~7.5 hours |
    | Phase 4 (cont.): Podman import + Oracle verify | 30-60 minutes | ~8.5 hours |
    | Phase 7: Verification | 30 minutes | **~9 hours total** |

    > 💡 **Pro tip:** Set aside a full day (weekend) for the migration.
    > Don't rush it. Having the Clonezilla backup means you can always roll back.
    """)


# ─────────────────────────────────────────────
# Main Script
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive Linux migration plan as Markdown files."
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for generated files (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--skip-detect",
        action="store_true",
        help="Skip system detection (use placeholder values)"
    )
    args = parser.parse_args()

    # Banner
    print("╔═══════════════════════════════════════════════════════╗")
    print("║  Strategic Migration Plan Generator                  ║")
    print("║  Windows → Linux (Fedora) with Gaming Preservation   ║")
    print("╠═══════════════════════════════════════════════════════╣")

    # Detect system
    if args.skip_detect:
        print("║  ⚠️  Skipping system detection (using defaults)      ║")
        info = {
            "hostname": "unknown", "os": platform.platform(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "generated_at": TIMESTAMP,
            "cpu_name": "Unknown CPU", "cpu_cores": "?", "cpu_threads": "?",
            "ram_gb": 32, "gpus": [{"name": "Unknown GPU", "vram_gb": "?"}],
            "disks": [
                {"model": "Disk 0", "size_gb": "?"},
                {"model": "Disk 1", "size_gb": "?"}
            ],
            "partitions": [], "bitlocker": [],
            "podman": {"containers": [], "volumes": [], "images": []},
        }
    else:
        print("║  🔍 Detecting system hardware...                     ║")
        info = detect_system_info()
        print(f"║  ✅ CPU: {info.get('cpu_name', 'Unknown')[:42]:<42} ║")
        print(f"║  ✅ RAM: {info.get('ram_gb', '?')} GB{' ' * 36}║")
        gpu_str = ", ".join(g["name"][:30] for g in info.get("gpus", []))
        print(f"║  ✅ GPU: {gpu_str[:42]:<42} ║")
        disk_count = len(info.get("disks", []))
        print(f"║  ✅ Disks: {disk_count} detected{' ' * 33}║")

    print("╠═══════════════════════════════════════════════════════╣")

    # Create output directory
    output_path = pathlib.Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Copy static beginner guide if it exists alongside this script
    beginner_guide_src = pathlib.Path(__file__).parent / "linux_migration_plan" / "00_windows_to_linux_guide.md"
    if beginner_guide_src.exists():
        import shutil
        dest = output_path / "00_windows_to_linux_guide.md"
        try:
            if beginner_guide_src.resolve() != dest.resolve():
                shutil.copy2(beginner_guide_src, dest)
                print(f"║  📖 Copied:  00_windows_to_linux_guide.md            ║")
            else:
                print(f"║  📖 Exists:  00_windows_to_linux_guide.md            ║")
        except (PermissionError, OSError):
            print(f"║  📖 Exists:  00_windows_to_linux_guide.md            ║")

    # Generate all 7 dynamic files
    files = {
        "01_backup_and_fallback_strategy.md": generate_01_backup,
        "02_linux_distribution_comparison.md": generate_02_distro_comparison,
        "03_drive_partitioning_and_dual_boot.md": generate_03_partitioning,
        "04_podman_zero_data_loss_migration.md": generate_04_podman_migration,
        "05_linux_installation_and_post_boot.md": generate_05_linux_install,
        "06_app_migration_and_workarounds.md": generate_06_app_migration,
        "07_master_checklist_and_verification.md": generate_07_master_checklist,
    }

    for filename, generator_fn in files.items():
        filepath = output_path / filename
        content = generator_fn(info)
        filepath.write_text(content, encoding="utf-8")
        print(f"║  📄 Created: {filename:<39} ║")

    # Save system info as JSON for reference
    info_path = output_path / "system_info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, default=str)
    print(f"║  📋 Created: system_info.json{' ' * 23}║")

    # Summary
    print("╠═══════════════════════════════════════════════════════╣")
    total = len(files) + 1
    print(f"║  ✅ Generated {total} files in: {str(output_path)[:24]:<24} ║")
    print("║                                                       ║")
    print("║  Start reading from 01_backup_and_fallback_strategy   ║")
    print("║  and follow each phase in order.                      ║")
    print("╚═══════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
