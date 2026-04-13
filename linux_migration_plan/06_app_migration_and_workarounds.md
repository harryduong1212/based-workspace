# Phase 6: App Migration, Backend Tools & Incompatibility Workarounds

> **Generated:** 2026-04-12 20:55

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
{
  "extensions.gallery": {
    "serviceUrl": "https://marketplace.visualstudio.com/_apis/public/gallery",
    "itemUrl": "https://marketplace.visualstudio.com/items"
  }
}

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

## 6.2 Daily Applications (Matched to Your Windows Setup)

> Apps below are sourced from your actual `winget list` audit on 2026-04-12.
> Only apps you currently use on Windows are included.

### Browsers

| Application | Install Command | Notes |
|---|---|---|
| **Google Chrome** | See below | Your primary browser |
| **Microsoft Edge** | `flatpak install flathub com.microsoft.Edge` | Available if needed |

```bash
# Add Google Chrome repository
sudo dnf install -y fedora-workstation-repositories
sudo dnf config-manager --set-enabled google-chrome

# Install Chrome
sudo dnf install -y google-chrome-stable
```

### Communication & Meetings

| Application | Windows Status | Linux Install | Notes |
|---|---|---|---|
| **Microsoft Teams** | ✅ Installed | `flatpak install flathub com.microsoft.Teams` | Full feature parity on Linux |
| **Cisco Webex** | ✅ Installed | `flatpak install flathub com.cisco.Webex` | Video/screen share works |
| **Discord** | ✅ Installed | `flatpak install flathub com.discordapp.Discord` | Voice/video works |

### Productivity

| Application | Windows Status | Linux Install | Notes |
|---|---|---|---|
| **Obsidian** | Replaces Notion | `flatpak install flathub md.obsidian.Obsidian` | Local-first, Markdown-based, works perfectly on Linux |
| **LibreOffice** | N/A | Pre-installed on Fedora | Replaces MS Office for local editing |
| **OneDrive** | ✅ Installed | `sudo dnf install onedrive` (CLI sync) | Or use onedrive.live.com in browser |

> 💡 **Why Obsidian over Notion?**
> - **Offline-first** — all notes are local Markdown files (no cloud dependency)
> - **Cross-platform** — native Linux app, identical on all OSes
> - **Git-friendly** — your notes are just `.md` files, version-control them like code
> - **Plugin ecosystem** — 1500+ community plugins
> - **Free** for personal use
> - Your notes live in `~/Documents/Obsidian/` — easy to back up and sync

### AI & Dev Tools

| Application | Windows Status | Linux Install | Notes |
|---|---|---|---|
| **LM Studio** | ✅ Installed (v0.4.8) | Download AppImage from lmstudio.ai | Native Linux support |
| **Postman** | ✅ Installed | `flatpak install flathub com.getpostman.Postman` | API testing |
| **Google Cloud SDK** | ✅ Installed | `sudo dnf install google-cloud-cli` | Or install via gcloud script |
| **MCP Inspector** | ✅ Container | Already in Podman setup (Phase 4) | Port 6274/6277 |

```bash
# Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

### Creative & Media

| Application | Windows Status | Linux Install | Notes |
|---|---|---|---|
| **OBS Studio** | ✅ Installed | `sudo dnf install obs-studio` | Already in 6.1 above |

### Vietnamese Keyboard Setup (Replaces EVKey with VnKey-style Input)

> On Linux, the closest equivalent to VnKey/UniKey is **ibus-unikey** — same engine,
> same Telex/VNI support, native GNOME integration.

```bash
# Install ibus-unikey (VnKey/UniKey engine for Linux)
sudo dnf install -y ibus-unikey
ibus restart

# Then configure:
# Settings → Keyboard → Input Sources → "+" → Vietnamese → Vietnamese (Unikey)
# Switch between EN/VI with: Super+Space
```

**Configuration tips:**
- Right-click the keyboard icon in the top bar → **Preferences** to access Unikey settings
- Supports Telex, VNI, and VIQR input methods (same as Windows VnKey)
- Works in all apps including Chrome, VS Code, IntelliJ, and terminal

---

## 6.3 Terminal & Shell Setup

```bash
# Install modern terminal tools
sudo dnf install -y \
    zsh \
    tmux \
    ripgrep \
    fd-find \
    bat \
    eza \
    fzf \
    jq \
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

> Only listing apps you **actually have installed** on Windows that won't work on Linux.

| Application | Issue | Action |
|---|---|---|
| **Adobe Photoshop 2024** | No Linux version | **GIMP** (`sudo dnf install gimp`) or **Photopea.com** (web, very close to PS) |
| **Overwolf** | Windows-only (gaming) | Stays on Windows gaming partition |
| **Delta Force** | Windows-only (Garena) | Stays on Windows gaming partition |
| **VALORANT / LoL** | Vanguard anti-cheat blocks Linux | **Must play on Windows** — dual-boot |

### Apps That Work Better on Linux (no workaround needed)

| Application | Windows Version | Linux Version | Why It's Better |
|---|---|---|---|
| **Podman** | Runs in WSL2 VM | Native, rootless | No VM overhead, faster startup |
| **Git** | Git for Windows (emulated) | Native | Native filesystem, faster operations |
| **Node.js / Python** | Native | Native | Identical experience |
| **SSH** | OpenSSH client | OpenSSH (native) | Built into the OS, first-class |
| **Teams** | Electron app | Flatpak | Same performance |
| **Discord** | Electron app | Flatpak | Same performance |

---

## 6.6 Why You Don't Need Kaspersky (or Any Antivirus) on Linux

> This section explains the **fundamental architectural reasons** why Linux doesn't need
> third-party antivirus, so you can make an informed decision.

### The Short Answer

Linux wasn't designed to need antivirus. Its security model is **built into the kernel**, not bolted on as an afterthought. Installing Kaspersky on Linux would be like wearing a life jacket in your living room — it won't hurt, but it serves no purpose, and it slows you down.

### 5 Reasons Linux Is Inherently Secure

#### 1. You Never Run as Admin

| Windows | Linux |
|---|---|
| Many apps silently run with admin rights | **Nothing** runs as root unless you explicitly `sudo` |
| Malware can elevate via UAC bypass | Malware cannot escalate — it's trapped in your user space |
| Installers write to `C:\Program Files\` freely | Software can only write to `~` (your home) without `sudo` |

**Impact:** Even if you download something malicious, it **cannot** modify system files, install drivers, or infect other users. It's jailed in your home directory with no access to the kernel.

#### 2. No .exe Files = No Attack Vector

| Windows | Linux |
|---|---|
| Downloaded `.exe` files run when double-clicked | Downloaded files are **not executable by default** |
| Email attachments can auto-execute | You must manually `chmod +x` a file before it can run |
| Drive-by downloads via browser | Browser downloads land as inert data files |

**Impact:** The #1 malware delivery method on Windows (tricking users into running .exe) simply doesn't work. Linux files have no execute permission until you explicitly grant it.

#### 3. SELinux — Mandatory Access Control (Fedora's Secret Weapon)

Fedora ships with **SELinux** enabled by default. This is a kernel-level security layer that goes beyond traditional permissions:

```
Traditional Permissions:     "User X can read file Y"
SELinux:                     "Process A running as context B can ONLY access 
                              file C of type D using operation E"
```

**What this means in practice:**
- Even if an attacker gains root access, SELinux **still blocks** unauthorized actions
- Each process is confined to its own security domain
- A compromised web browser **cannot** access your SSH keys, even though they're readable by your user
- Container processes (Podman) are automatically sandboxed via SELinux policies

> **Windows has nothing equivalent.** Windows Defender is reactive (scans for known threats).
> SELinux is proactive (prevents all unauthorized behavior, even from unknown threats).

#### 4. Package Manager = Verified Software Supply Chain

| Windows | Linux (Fedora) |
|---|---|
| Download .exe from random websites | `sudo dnf install <app>` from signed, verified repos |
| No signature verification by default | **Every package is GPG-signed** and verified before install |
| No dependency management | All dependencies managed and audited |
| Updates are per-app (each app updates itself) | One command updates **everything**: `sudo dnf upgrade` |

**Impact:** You never need to Google for downloads. Every package in Fedora's repos has been reviewed, signed, and can be audited by anyone. Supply chain attacks (fake downloads, trojanized installers) are practically impossible.

#### 5. Market Share = No Target

| OS | Desktop Market Share | Malware Written For It |
|---|---|---|
| Windows | ~72% | ~95% of all malware |
| macOS | ~16% | ~4% |
| Linux Desktop | ~4% | < 0.5% |

Malware authors target Windows because the ROI is highest. Writing malware for Linux is hard (permissions, SELinux, diverse distros) and targets a tiny audience. It's simply not worth it.

### What Linux DOES Have Instead of Antivirus

| Layer | Tool | What It Does |
|---|---|---|
| **Kernel-level** | SELinux | Mandatory access control — process sandboxing |
| **Network** | Firewalld | Built-in firewall (enabled by default on Fedora) |
| **Updates** | `dnf-automatic` | Auto-security-patches (optional, recommended) |
| **Containers** | Podman rootless | Containers are isolated from the host by default |
| **File integrity** | AIDE | Detects unauthorized file changes (optional) |
| **Audit** | `auditd` | Logs every system call for forensics (built-in) |

```bash
# Verify your security stack is active:
getenforce                    # Should output: Enforcing
sudo firewall-cmd --state     # Should output: running
sudo systemctl status auditd  # Should output: active (running)
```

### The Verdict

| Criteria | Kaspersky on Windows | Linux Without Antivirus |
|---|---|---|
| Protection model | **Reactive** — scans for known signatures | **Proactive** — prevents unauthorized actions |
| Performance impact | 5-15% CPU/RAM overhead | Zero overhead (built into kernel) |
| Update dependency | Must update virus definitions daily | Kernel security is always active |
| False positives | Frequent (blocks legit dev tools) | None (no scanner running) |
| Cost | $30-60/year | Free (included with OS) |

> **Bottom line:** On Linux, you ARE the antivirus. The OS enforces that programs can only
> do what you explicitly allow. Kaspersky would add CPU overhead and occasionally block
> your development tools (Podman, npm, pip) with zero additional security benefit.

---

## 6.7 Bulk Installation Script

Run this to install everything at once:

```bash
#!/bin/bash
echo "═══════════════════════════════════════"
echo "  Installing all applications..."
echo "  (Matched to your Windows setup)"
echo "═══════════════════════════════════════"

# ---- DNF packages ----
sudo dnf install -y \
    obs-studio gimp \
    zsh tmux ripgrep fd-find bat eza fzf jq yq \
    htop btop nvtop \
    gnome-tweaks gnome-extensions-app \
    ibus-unikey

# ---- Google Chrome ----
sudo dnf install -y fedora-workstation-repositories
sudo dnf config-manager --set-enabled google-chrome
sudo dnf install -y google-chrome-stable

# ---- Flatpak apps (your actual daily apps) ----
flatpak install -y flathub \
    com.microsoft.Teams \
    com.cisco.Webex \
    com.discordapp.Discord \
    com.getpostman.Postman \
    md.obsidian.Obsidian

# ---- LM Studio (AppImage) ----
echo "📥 Download LM Studio manually from: https://lmstudio.ai"

# ---- Google Cloud SDK ----
curl https://sdk.cloud.google.com | bash

echo ""
echo "✅ All applications installed!"
echo "═══════════════════════════════════════"
```

---

## 6.8 Checklist

- [ ] Google Antigravity configured (4K fix, Marketplace, settings sync)
- [ ] IntelliJ IDEA installed and configured
- [ ] OBS Studio installed
- [ ] VS Code installed (if needed alongside Antigravity)
- [ ] Google Chrome installed
- [ ] Microsoft Teams installed (Flatpak)
- [ ] Cisco Webex installed (Flatpak)
- [ ] Discord installed (Flatpak)
- [ ] Obsidian installed (Flatpak)
- [ ] Postman installed (Flatpak)
- [ ] LM Studio installed (AppImage)
- [ ] Vietnamese keyboard set up (ibus-unikey)
- [ ] Terminal tools installed (zsh, tmux, ripgrep, etc.)
- [ ] Google Cloud SDK installed
- [ ] Git configured with SSH keys
- [ ] Podman verified working
- [ ] SELinux verified enforcing (`getenforce`)
- [ ] Firewalld verified running
