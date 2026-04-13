# Phase 5: Fedora Installation & Immediate Post-Boot Sequence

> **Generated:** 2026-04-12 20:55
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
sudo dnf install -y \
    https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
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
{
  "extensions.gallery": {
    "serviceUrl": "https://marketplace.visualstudio.com/_apis/public/gallery",
    "itemUrl": "https://marketplace.visualstudio.com/items"
  }
}
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
sudo dnf install -y \
    git curl wget unzip tar \
    python3 python3-pip python3-venv \
    nodejs npm \
    podman podman-compose \
    htop btop nvtop \
    gnome-tweaks gnome-extensions-app \
    wl-clipboard \
    fontconfig google-noto-fonts-common \
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
