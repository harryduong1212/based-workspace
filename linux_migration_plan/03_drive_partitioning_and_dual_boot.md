# Phase 3: Drive Partitioning & Dual-Boot Setup

> **Generated:** 2026-04-12 20:55
> **Disk 0:** SAMSUNG MZVL21T0HDLU-00BT7 (953.86 GB) — Windows
> **Disk 1:** WDC WDS100T2B0C-00PXH0 (931.51 GB) — Linux + Shared

---

## 3.1 Strategy Overview

```
┌─────────────────────────────────────────────────────────┐
│  DISK 0 — SAMSUNG MZVL21T0HDLU-00BT7                              │
│  ► NO CHANGES — Remains 100% Windows Gaming             │
│  ┌──────┬───────────────────────────┬──────┬──────┐     │
│  │ EFI  │     Windows C: (924 GB)   │ Rec  │ Rec  │     │
│  │250MB │     NTFS — DO NOT TOUCH   │780MB │730MB │     │
│  └──────┴───────────────────────────┴──────┴──────┘     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  DISK 1 — WDC WDS100T2B0C-00PXH0                                      │
│  ► REPARTITIONED for Linux + Shared Storage                     │
│  ┌───────┬──────────┬──────────┬─────────┬──────────────────┐   │
│  │ EFI   │  / root  │  /home   │  swap   │   /mnt/shared    │   │
│  │512 MB │ 150 GB   │ 200 GB   │ 34 GB  │   ~548 GB       │   │
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
| 4 | `[swap]` | 34 GB | Linux Swap | Hibernate + memory overflow (RAM size + 2 GB) |
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
Size:        34 GiB
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
sudo mkdir -p /mnt/shared/{Documents,Downloads,Media/{Music,Videos,Pictures},Learning,Projects/exports,Backups}

# Set permissions for your user
sudo chown -R $(whoami):$(whoami) /mnt/shared/
```

**Resulting structure (accessible from both Windows and Linux):**

```
/mnt/shared/                    (Linux)
I:\                             (Windows — after assigning drive letter)
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

- [x] All data on Disk 1 (H: and I:) backed up to external drive
- [ ] Fedora ISO downloaded and verified (checksum)
- [ ] Bootable USB created with Rufus
- [ ] Custom partitioning applied during install
- [ ] GRUB installed to Disk 1 EFI
- [ ] BIOS boot order updated (Disk 1 first)
- [ ] Windows detected in GRUB menu
- [ ] Shared NTFS partition mounted and accessible
- [ ] Folder structure created on shared drive
