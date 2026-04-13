# Phase 1: Manual Data Preservation & Preparation

> **System:** Harry — Windows-11-10.0.26200-SP0

---

## 1.1 Pre-Migration: Disable Windows Safety Features

Before you do anything with Linux, you **must** disable Windows Fast Startup. 

Open **PowerShell as Administrator** and run:

```powershell
# Disable Fast Startup (prevents NTFS hibernation lock)
powercfg /h off

# Verify Fast Startup is off
powercfg /a
```

> Warning: **Fast Startup** makes Windows "hibernate" instead of shutting down.
> If Linux tries to mount the drive while Windows is hibernated, it will
> corrupt the NTFS filesystem. **Always disable this before dual-booting.**

---

## 1.2 Manual Google Drive Backup Checklist

Since you are managing backups manually via Google Drive, please ensure the following critical directories and files are uploaded **before** you repartition Disk 1.

> [!CAUTION]
> **Disk 1 (H: and I:) will be completely wiped during the Linux installation.** 
> Your Windows drive (Disk 0 / C:) will remain untouched, but back up thoroughly to be safe.

### Folders to Upload to Google Drive

- [ ] **`H:\WORKSPACE\`** (Your code repos, including based-workspace)
- [ ] **`H:\Learning\`** (University materials)
- [ ] **`I:\Harry\`** (Personal photos, software, files)
- [ ] **`%USERPROFILE%\.ssh\`** (Critical: your SSH keys)
- [ ] **`%USERPROFILE%\.gitconfig`** (Global Git settings)
- [ ] **`H:\WORKSPACE\Personal\.gitconfig-personal`** (Your personal Git include)

### Settings to Manually Export/Sync

- [ ] **IntelliJ Settings:** File -> Manage IDE Settings -> Export Settings (upload zip)
- [ ] **Chrome Bookmarks:** Bookmark Manager -> Export Bookmarks
- [ ] **Podman Data:** (See Phase 4 for container export commands)

---

## 1.3 Move Steam Games (Optional)

You have 7 Steam games installed on `I:\SteamLibrary`. Since `I:` will be wiped:
- If you have space on `C:\` (~924 GB capacity), move them using the Steam settings (Settings -> Storage -> Move).
- Otherwise, you will need to re-download them later.

---

## 1.4 UEFI Settings Snapshot

Before making system changes, take photos of your BIOS/UEFI settings:

1. Restart -> Enter BIOS (`F2` / `Del`)
2. Photograph:
   - **Boot Order** screen
   - **Secure Boot** status
   - **SATA/NVMe** mode (AHCI vs RAID)
   - **TPM** settings
3. Save photos to your phone or Google Drive.

---

## 1.5 Readiness Checklist

- [ ] Fast Startup disabled (`powercfg /h off`)
- [ ] All code (`H:\WORKSPACE`) uploaded to Google Drive
- [ ] All personal files (`I:\Harry`) uploaded to Google Drive
- [ ] SSH keys and Git configs uploaded to Google Drive
- [ ] Settings (IntelliJ, Chrome) exported and uploaded
- [ ] Games moved to `C:\` or deleted
- [ ] UEFI settings photographed
