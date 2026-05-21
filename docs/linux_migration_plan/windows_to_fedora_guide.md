# Windows → Fedora Linux: Complete Beginner's Translation Guide

> **For:** Windows 11 power users switching to Fedora Workstation 42
> **Philosophy:** Everything you know from Windows has a Linux equivalent — often better.

---

## 1. The Big Picture: How Linux Is Different

```
WINDOWS WORLD                          LINUX WORLD
─────────────────────                  ─────────────────────
One company (Microsoft)         →      Community + Companies (Red Hat/Fedora)
Registry + scattered configs    →      Text files you can read & edit
"Install wizard" (.exe/.msi)    →      Package manager (like an App Store in terminal)
Restart for everything          →      Almost never need to restart
Drives: C:\, D:\, E:\           →      One tree: / (everything branches from root)
File Explorer                   →      Nautilus (Files)
cmd / PowerShell                →      Bash / Zsh (terminal)
Task Manager                    →      System Monitor / btop / htop
Windows Update                  →      dnf upgrade (you control when)
```

---

## 2. File System: The #1 Thing That Will Confuse You

### Windows: Drive Letters
```
C:\                    ← System drive
D:\                    ← Second drive
C:\Users\johny\        ← Your stuff
C:\Program Files\      ← Apps installed here
```

### Linux: One Tree, Everything Is a Folder
```
/                      ← "Root" = the top of everything (like C:\)
/home/harry/           ← Your stuff (like C:\Users\johny\)
/usr/                  ← System programs (like C:\Program Files\)
/etc/                  ← All config files (like Windows Registry, but readable!)
/tmp/                  ← Temporary files (auto-cleaned)
/mnt/shared/           ← Your NTFS shared drive (like S:\ in Windows)
/dev/                  ← Hardware devices (your NVMe, USB, etc.)
/var/                  ← Logs, databases, variable data
/opt/                  ← Optional/third-party software
```

### Quick Mapping Table

| Windows Path | Linux Path | What It Is |
|---|---|---|
| `C:\` | `/` | System root |
| `C:\Users\johny\` | `/home/harry/` (or `~`) | Your home folder |
| `C:\Users\johny\Desktop\` | `~/Desktop/` | Desktop |
| `C:\Users\johny\Documents\` | `~/Documents/` | Documents |
| `C:\Users\johny\Downloads\` | `~/Downloads/` | Downloads |
| `C:\Users\johny\.ssh\` | `~/.ssh/` | SSH keys |
| `C:\Program Files\` | `/usr/bin/` + `/usr/lib/` | Installed programs |
| `C:\ProgramData\` | `/etc/` + `/var/` | System-wide config & data |
| `C:\Windows\System32\` | `/usr/sbin/` | System utilities |
| `%APPDATA%\` | `~/.config/` | Per-user app settings |
| `%LOCALAPPDATA%\` | `~/.local/share/` | Per-user app data |
| `%TEMP%\` | `/tmp/` | Temporary files |
| `D:\` or `E:\` | `/mnt/shared/` | Other drives (you choose the mount point) |

### The `~` Shortcut
In Linux, `~` always means "my home directory". So `~/WORKSPACE` = `/home/harry/WORKSPACE`.

### Hidden Files
- **Windows:** Files with "Hidden" attribute
- **Linux:** Any file/folder starting with `.` (dot) is hidden. Example: `.ssh`, `.config`, `.gitconfig`
- To see hidden files: `ls -a` or press `Ctrl+H` in Files

---

## 3. Path Separators

| | Windows | Linux |
|---|---|---|
| **Separator** | `\` (backslash) | `/` (forward slash) |
| **Example** | `C:\Users\johny\file.txt` | `/home/harry/file.txt` |

> 💡 You already use `/` in Git and web URLs. Linux just uses it everywhere.

---

## 4. The Terminal: Your New Best Friend

### Windows → Linux Command Translation

| What You Want | Windows (PowerShell) | Linux (Bash) |
|---|---|---|
| **List files** | `dir` / `Get-ChildItem` | `ls` / `ls -la` (with details) |
| **Change directory** | `cd C:\Users` | `cd /home` |
| **Print current dir** | `pwd` / `Get-Location` | `pwd` |
| **Create folder** | `mkdir test` | `mkdir test` ← Same! |
| **Create file** | `New-Item file.txt` | `touch file.txt` |
| **Copy file** | `Copy-Item a.txt b.txt` | `cp a.txt b.txt` |
| **Move/rename** | `Move-Item old new` | `mv old new` |
| **Delete file** | `Remove-Item file.txt` | `rm file.txt` |
| **Delete folder** | `Remove-Item -Recurse dir` | `rm -rf dir` |
| **View file** | `Get-Content file.txt` | `cat file.txt` |
| **Search in files** | `Select-String "hello" *.txt` | `grep "hello" *.txt` |
| **Find a file** | `Get-ChildItem -Recurse -Filter "*.log"` | `find / -name "*.log"` |
| **View running processes** | `Get-Process` | `ps aux` / `htop` |
| **Kill a process** | `Stop-Process -Name app` | `kill <PID>` / `killall app` |
| **Check disk space** | `Get-PSDrive` | `df -h` |
| **Check folder size** | `(Get-ChildItem -Recurse \| Measure Length -Sum)` | `du -sh folder/` |
| **Download a file** | `Invoke-WebRequest -Uri URL -OutFile file` | `curl -O URL` / `wget URL` |
| **Clear screen** | `cls` / `Clear-Host` | `clear` |
| **View command history** | `Get-History` | `history` |
| **Pipe output** | `command1 \| command2` | `command1 \| command2` ← Same! |
| **Run as admin** | `Start-Process -Verb RunAs` | `sudo command` |
| **Environment variables** | `$env:PATH` | `$PATH` / `echo $PATH` |
| **Set env variable** | `$env:MY_VAR = "value"` | `export MY_VAR="value"` |

### Terminal Shortcuts (Same in Most Terminals!)

| Shortcut | Action |
|---|---|
| `Ctrl+C` | Cancel/stop current command |
| `Ctrl+L` | Clear screen |
| `Ctrl+R` | Search command history |
| `Tab` | Auto-complete file/folder names |
| `Tab Tab` | Show all possible completions |
| `↑` / `↓` | Scroll through previous commands |
| `Ctrl+A` | Jump to start of line |
| `Ctrl+E` | Jump to end of line |

---

## 5. Installing Software: The Biggest Upgrade

### Windows Way (What You're Used To)
1. Google the app → Download .exe → Run installer → Click Next 10 times → Done

### Linux Way (Fedora with `dnf`)
```bash
sudo dnf install obs-studio    # Done. That's it. One command.
```

### Full Comparison

| Action | Windows | Fedora Linux |
|---|---|---|
| **Install an app** | Download .exe, run wizard | `sudo dnf install <app>` |
| **Uninstall an app** | Control Panel → Programs | `sudo dnf remove <app>` |
| **Update all apps** | Windows Update (when it feels like it) | `sudo dnf upgrade` |
| **Search for an app** | Google / Microsoft Store | `dnf search <keyword>` |
| **List installed apps** | `winget list` | `dnf list installed` |
| **See app info** | Right-click → Properties | `dnf info <app>` |

### Three Ways to Install Software on Fedora

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOW TO INSTALL APPS                          │
├─────────────┬──────────────────┬────────────────────────────────┤
│ Method      │ Best For         │ Example                        │
├─────────────┼──────────────────┼────────────────────────────────┤
│ dnf         │ System apps,     │ sudo dnf install git           │
│ (built-in)  │ dev tools,       │ sudo dnf install obs-studio    │
│             │ CLI utilities    │ sudo dnf install btop          │
├─────────────┼──────────────────┼────────────────────────────────┤
│ Flatpak     │ Desktop apps     │ flatpak install flathub        │
│ (app store) │ (GUI apps)       │   com.spotify.Client           │
│             │ sandboxed/safe   │ flatpak install flathub        │
│             │                  │   com.slack.Slack              │
├─────────────┼──────────────────┼────────────────────────────────┤
│ RPM / .rpm  │ Vendor-provided  │ Like downloading a .exe from   │
│ (manual)    │ packages (rare)  │ a website. Use only when dnf   │
│             │                  │ and Flatpak don't have it.     │
└─────────────┴──────────────────┴────────────────────────────────┘
```

> 💡 **Think of `dnf` as `winget` on steroids** — it handles dependencies, updates, and security automatically.

---

## 6. System Settings & Configuration

| Windows | Fedora Linux | How to Open |
|---|---|---|
| **Settings app** | GNOME Settings | Click top-right corner → ⚙️ Settings |
| **Control Panel** | GNOME Settings + terminal | Most things in Settings GUI |
| **Task Manager** | System Monitor / `btop` | `gnome-system-monitor` or `btop` in terminal |
| **Device Manager** | `lspci` / `lsusb` | Terminal commands |
| **Registry Editor** | Config files in `/etc/` | `sudo nano /etc/<config-file>` |
| **Disk Management** | GNOME Disks / `lsblk` | `gnome-disks` or `lsblk` |
| **Event Viewer** | `journalctl` | `journalctl -xe` (recent errors) |
| **Environment Variables** | `~/.bashrc` or `~/.zshrc` | `nano ~/.bashrc` → add `export VAR=value` |
| **Windows Defender** | SELinux + Firewalld | Built-in, always running, no antivirus needed |
| **UAC ("Allow this app")** | `sudo` (type password once) | You control everything with `sudo` |
| **Services (services.msc)** | `systemctl` | `systemctl status <service>` |
| **Display Settings** | Settings → Displays | Same — Settings → Displays |
| **Sound Settings** | Settings → Sound | Same — Settings → Sound |
| **Network Settings** | Settings → Network | Same — Settings → Network |
| **Bluetooth** | Settings → Bluetooth | Same — Settings → Bluetooth |

---

## 7. User Permissions: `sudo` = "Run as Administrator"

In Windows, you right-click → "Run as Administrator."
In Linux, you type `sudo` before the command:

```bash
# Normal user (reading, coding, browsing — 99% of your time)
ls ~/WORKSPACE
cat /etc/hostname
git pull

# Admin required (installing, system changes — you type your password)
sudo dnf install git        # Install software
sudo nano /etc/fstab        # Edit system config
sudo reboot                 # Restart the system
```

> 💡 **Linux philosophy:** You never run as admin by default.
> You only elevate when needed, and it asks for YOUR password (not a separate admin password).

---

## 8. Desktop Environment: GNOME vs Windows 11

### Keyboard Shortcuts You'll Use Daily

| Action | Windows 11 | Fedora (GNOME) |
|---|---|---|
| **Open app launcher** | `Win` key | `Super` key (same key!) |
| **Search for anything** | `Win` → type | `Super` → type ← Identical! |
| **Switch windows** | `Alt+Tab` | `Alt+Tab` ← Same! |
| **Switch workspaces** | `Ctrl+Win+←/→` | `Super+Alt+←/→` or swipe up |
| **Snap window left/right** | `Win+←/→` | `Super+←/→` ← Same! |
| **Screenshot** | `Win+Shift+S` | `Print Screen` → select area |
| **File manager** | `Win+E` | `Super` → type "Files" |
| **Lock screen** | `Win+L` | `Super+L` ← Same! |
| **Close window** | `Alt+F4` | `Alt+F4` ← Same! |
| **Show desktop** | `Win+D` | `Super+D` |
| **Open terminal** | `Win+X` → Terminal | `Ctrl+Alt+T` |
| **Minimize window** | `Win+↓` | `Super+H` (or click title bar) |
| **Full screen** | `F11` | `F11` / `Super+↑` |

### Visual Comparison

```
WINDOWS 11                             FEDORA GNOME
───────────                            ───────────
Taskbar (bottom)                →      Top Bar (top) + Dash (left, hover mode)
Start Menu                      →      Activities Overview (press Super)
System Tray (right)             →      Top-right corner (click for menu)
Action Center                   →      Notification panel (top-right click)
Widgets                         →      GNOME Extensions (install what you want)
Virtual Desktops                →      Workspaces (swipe up or Super key)
Right-click Desktop             →      Right-click Desktop ← Same!
```

---

## 9. Things That Exist in Windows but NOT in Linux

| Windows Thing | Linux Reality | Why It's Actually Fine |
|---|---|---|
| **Windows Registry** | Doesn't exist | Config is in plain text files (`/etc/`, `~/.config/`) — much easier to back up and understand |
| **Drive Letters (C:, D:)** | Doesn't exist | Everything is under `/`. Drives are "mounted" to folders like `/mnt/shared/` |
| **.exe files** | Doesn't exist | Apps come through package managers. No downloading random .exe files |
| **DLL Hell** | Doesn't exist | Package manager handles all dependencies automatically |
| **Windows Update auto-restart** | Doesn't exist | You update when YOU want. System never force-restarts |
| **Blue Screen of Death** | Extremely rare | Linux kernel panics are far less common |
| **Antivirus software** | Not needed | Linux's permission model + SELinux makes viruses nearly impossible |
| **Activation / Product Keys** | Doesn't exist | Fedora is 100% free, forever |
| **Bloatware** | Doesn't exist | Only what you install is on the system |
| **defrag (disk defragmentation)** | Not needed | BTRFS and ext4 don't fragment like NTFS |
| **"Install for all users" dialog** | Doesn't exist | `dnf` installs system-wide by default |
| **Windows Subsystem for Linux** | You ARE Linux now | No virtualization layer needed — native performance |

---

## 10. Things That Exist in Linux but NOT in Windows

| Linux Thing | What It Does | Why It's Awesome |
|---|---|---|
| **Package Manager (`dnf`)** | Installs, updates, removes ALL software from one place | Never Google for downloads again |
| **`sudo`** | Run one command as admin without switching user | Safer than "Run as Administrator" |
| **Everything is a file** | Devices, processes, configs — all accessible as files | USB drive is `/dev/sda`, CPU info is `/proc/cpuinfo` |
| **Filesystem snapshots (BTRFS)** | Instant backup of your entire system state | Break something? Roll back in 5 seconds |
| **True multi-user** | Multiple people can use the same machine simultaneously | Great for servers and shared machines |
| **Symlinks everywhere** | Like shortcuts, but more powerful | Your `based-workspace` already uses these! |
| **Cron / Systemd timers** | Schedule any task to run automatically | Like Task Scheduler but more powerful |
| **`man` pages** | Built-in documentation for every command | Type `man ls` to learn about `ls` |
| **SSH built-in** | Remote into any machine from terminal | `ssh user@server` — that's it |
| **Workspaces** | Multiple desktops built into the OS | Better than Windows virtual desktops |
| **Tiling / window management** | Advanced window arrangement | GNOME Extensions or install a tiling WM |
| **`grep`, `awk`, `sed`** | Powerful text processing in terminal | Process huge files in seconds |
| **Pipes (`\|`)** | Chain commands together | `cat log.txt \| grep ERROR \| wc -l` (count errors) |
| **Native containers (Podman)** | Run containers without extra software | No Docker Desktop needed — Podman is built in |

---

## 11. File Extensions & Executables

| Windows | Linux | Notes |
|---|---|---|
| `.exe` | No extension needed | Files are executable via permissions, not extensions |
| `.msi` | `.rpm` | Fedora's package format (rarely install manually) |
| `.bat` / `.ps1` | `.sh` | Shell scripts |
| `.dll` | `.so` | Shared libraries |
| `.lnk` (shortcuts) | Symlinks (`ln -s`) | `ln -s /real/path /shortcut/path` |
| `.zip` | `.tar.gz`, `.zip` | `tar -xzf file.tar.gz` or `unzip file.zip` |
| `.docx` | `.odt` (LibreOffice) | LibreOffice opens .docx too |

### Making a Script Executable

```bash
# Windows: just double-click the .bat file

# Linux: you need to mark it as executable first
chmod +x my_script.sh     # Make it runnable (one time only)
./my_script.sh             # Run it
```

---

## 12. Services & Background Processes

| Windows | Linux (`systemctl`) | Example |
|---|---|---|
| `services.msc` | `systemctl list-units` | See all services |
| Start a service | `sudo systemctl start <name>` | `sudo systemctl start postgresql` |
| Stop a service | `sudo systemctl stop <name>` | `sudo systemctl stop postgresql` |
| Auto-start on boot | `sudo systemctl enable <name>` | `sudo systemctl enable podman` |
| Disable auto-start | `sudo systemctl disable <name>` | `sudo systemctl disable bluetooth` |
| Check service status | `sudo systemctl status <name>` | `sudo systemctl status sshd` |
| View service logs | `journalctl -u <name>` | `journalctl -u podman` |

---

## 13. Networking

| Action | Windows | Linux |
|---|---|---|
| **See IP address** | `ipconfig` | `ip addr` (or `ip a`) |
| **Ping a server** | `ping google.com` | `ping google.com` ← Same! |
| **DNS lookup** | `nslookup domain.com` | `dig domain.com` / `nslookup domain.com` |
| **See open ports** | `netstat -an` | `ss -tulnp` |
| **Firewall** | Windows Defender Firewall | `firewall-cmd` (Firewalld) |
| **Connect to WiFi** | Settings → WiFi | Settings → WiFi ← Same GUI! |
| **VPN** | Settings → VPN | Settings → VPN / `nmcli` |
| **SSH into a server** | `ssh user@host` (PowerShell) | `ssh user@host` ← Same! |

---

## 14. Your Development Workflow: Before vs After

### Before (Windows)
```
1. Open Windows Terminal / PowerShell
2. cd H:\WORKSPACE\Personal\Vibe\based-workspace
3. code .  (or antigravity .)
4. podman compose up (through WSL2 sometimes)
5. git add, commit, push
```

### After (Fedora)
```
1. Open GNOME Terminal (Ctrl+Alt+T)
2. cd ~/WORKSPACE/Personal/Vibe/based-workspace
3. antigravity .  (or code .)
4. podman compose up  (native — no WSL2 needed, faster!)
5. git add, commit, push  ← identical!
```

> 💡 **The biggest change?** Your path uses `/` instead of `\`, and starts with `~` instead of `H:\`.
> **Everything else is basically the same.**

---

## 15. Daily Cheat Sheet (Print This!)

```
╔══════════════════════════════════════════════════════════════╗
║                FEDORA DAILY CHEAT SHEET                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  UPDATE EVERYTHING:     sudo dnf upgrade                     ║
║  INSTALL AN APP:        sudo dnf install <app>               ║
║  REMOVE AN APP:         sudo dnf remove <app>                ║
║  SEARCH FOR APP:        dnf search <keyword>                 ║
║                                                              ║
║  OPEN TERMINAL:         Ctrl + Alt + T                       ║
║  OPEN APP LAUNCHER:     Super key                            ║
║  SWITCH WINDOWS:        Alt + Tab                            ║
║  SCREENSHOT:            Print Screen                         ║
║  LOCK SCREEN:           Super + L                            ║
║                                                              ║
║  SEE DISK SPACE:        df -h                                ║
║  SEE FOLDER SIZE:       du -sh folder/                       ║
║  FIND A FILE:           find ~ -name "*.java"                ║
║  SEARCH IN FILES:       grep -r "search term" folder/        ║
║                                                              ║
║  START CONTAINERS:      podman compose up -d                 ║
║  STOP CONTAINERS:       podman compose down                  ║
║  SEE CONTAINERS:        podman ps                            ║
║                                                              ║
║  REBOOT:                sudo reboot                          ║
║  SHUTDOWN:              sudo poweroff                        ║
║  CHECK ERRORS:          journalctl -xe                       ║
║                                                              ║
║  UNDO A BAD CHANGE:     (BTRFS snapshot restore)             ║
║  HELP FOR ANY COMMAND:  man <command>  or  <command> --help  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 16. Common "Wait, How Do I..." Moments

### "Where is Control Panel?"
→ **GNOME Settings** (top-right corner → ⚙️). For deeper stuff → terminal.

### "Where is Task Manager?"
→ Press `Super`, type "System Monitor". Or open terminal and type `btop` (much better!).

### "Where do I download Chrome?"
→ `sudo dnf install google-chrome-stable` (after enabling the repo once).

### "How do I open a .zip file?"
→ Double-click it in Files (same as Windows). Or: `unzip file.zip`.

### "How do I connect a USB drive?"
→ Plug it in. It auto-mounts. Click it in the Files sidebar. No driver needed.

### "How do I change my wallpaper?"
→ Right-click desktop → "Change Background". Same as Windows!

### "What if I break something?"
→ BTRFS snapshots let you roll back. Or reinstall Fedora — your `/home` is on a separate partition, so all your files survive.

### "Can I still use PowerShell?"
→ Yes! `sudo dnf install powershell` then type `pwsh`. Your existing scripts will mostly work.

### "Where is the 'Program Files' folder?"
→ You don't need it. `dnf` puts everything in the right place automatically. To see where an app is: `which <app-name>`.

### "How do I right-click → Open Terminal here?"
→ In GNOME Files, right-click → "Open in Terminal". Identical to Windows!
