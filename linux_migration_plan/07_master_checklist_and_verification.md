# Phase 7: Master Migration Checklist & Post-Migration Verification

> **Generated:** 2026-04-12 20:55
> **System:** AMD Ryzen AI 9 HX 370 w/ Radeon 890M            / 32 GB RAM
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
- [ ] Partitions created: EFI (512MB), / (150GB), /home (200GB), swap (32+2 GB), shared (NTFS)
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
printf "║ %-20s %s\n" "OS:" "$(cat /etc/fedora-release)"
printf "║ %-20s %s\n" "Kernel:" "$(uname -r)"
printf "║ %-20s %s\n" "Desktop:" "$XDG_CURRENT_DESKTOP ($XDG_SESSION_TYPE)"

# Hardware
printf "║ %-20s %s\n" "CPU:" "$(lscpu | grep 'Model name' | sed 's/.*: *//')"
printf "║ %-20s %s\n" "RAM:" "$(free -h | awk '/Mem/{print $2}')"

# GPU
if command -v nvidia-smi &>/dev/null; then
    printf "║ %-20s %s\n" "NVIDIA GPU:" "$(nvidia-smi --query-gpu=name --format=csv,noheader)"
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
        printf "║   ✅ %-15s %s\n" "$app" "$ver"
    else
        printf "║   ❌ %-15s NOT FOUND\n" "$app"
    fi
done

# Storage
echo "║"
echo "║ Storage:"
if mountpoint -q /mnt/shared 2>/dev/null; then
    avail=$(df -h /mnt/shared --output=avail | tail -1 | tr -d ' ')
    printf "║   ✅ Shared drive:   %s available\n" "$avail"
else
    echo "║   ❌ Shared drive NOT mounted"
fi

# Boot
echo "║"
echo "║ Dual-Boot:"
win_entries=$(grep -c "Windows" /boot/grub2/grub.cfg 2>/dev/null || echo 0)
if [ "$win_entries" -gt 0 ]; then
    printf "║   ✅ Windows Boot:   %s entries in GRUB\n" "$win_entries"
else
    echo "║   ❌ Windows NOT detected in GRUB"
fi

# Containers
echo "║"
echo "║ Containers:"
pod_containers=$(podman ps -a --format "{{.Names}}" 2>/dev/null | wc -l)
pod_volumes=$(podman volume ls --format "{{.Name}}" 2>/dev/null | wc -l)
pod_images=$(podman images --format "{{.Repository}}" 2>/dev/null | wc -l)
printf "║   Containers: %s | Volumes: %s | Images: %s\n" "$pod_containers" "$pod_volumes" "$pod_images"

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
