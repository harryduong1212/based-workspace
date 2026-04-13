# Windows 11 Complete System Rebuild Blueprint

> **System Snapshot Date:** 2026-04-12
> **Machine:** AMD Ryzen AI 9 HX 370 / RTX 4060 Laptop / 32 GB RAM
> **OS:** Windows 11 Pro (Build 26200)
> **Purpose:** If you ever need to reinstall Windows from scratch, follow this guide to restore your exact setup.

---

## 1. Hardware & Driver Baseline

| Component | Driver Source |
|---|---|
| **AMD Ryzen AI 9 HX 370** | AMD Adrenalin (auto-detected by Windows Update) |
| **AMD Radeon 890M** | AMD Adrenalin Software |
| **NVIDIA RTX 4060 Laptop** | NVIDIA App / GeForce Experience ([nvidia.com/drivers](https://www.nvidia.com/download/index.aspx)) |
| **ASUS Laptop** | MyASUS app (Microsoft Store) + ASUS Smart Display Control |
| **Realtek Audio** | Realtek Audio Control (Microsoft Store) |
| **Logitech Peripherals** | Logitech Download Assistant (auto-installs) |

### Post-Install Driver Steps
```powershell
# 1. Run Windows Update first (gets most drivers)
# Settings → Windows Update → Check for updates (repeat until no more updates)

# 2. Install NVIDIA drivers manually for latest Game Ready version
# Download from: https://www.nvidia.com/download/index.aspx
# Select: RTX 4060 Laptop → Windows 11 → Game Ready Driver

# 3. Install MyASUS from Microsoft Store for ASUS-specific features
```

---

## 2. Windows Features to Enable

```powershell
# Run PowerShell as Administrator

# WSL2 (required for Podman)
wsl --install

# Hyper-V (if needed for Podman machine)
# Usually auto-enabled with WSL2

# Windows Sandbox (optional, for safe testing)
Enable-WindowsOptionalFeature -Online -FeatureName "Containers-DisposableClientVM" -All -NoRestart
```

---

## 3. Package Managers to Install First

### 3.1 Scoop (User-level package manager)
```powershell
# Install Scoop
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

# Add extras bucket
scoop bucket add extras

# Your installed Scoop packages:
scoop install 7zip
scoop install docker
scoop install grep
scoop install helm
scoop install kubectl
scoop install pipx
scoop install ripgrep
scoop install rustup
```

### 3.2 Chocolatey (System-level package manager)
```powershell
# Install Chocolatey (Run as Admin)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Your installed Chocolatey packages:
choco install python3 -y
choco install visualstudio2019buildtools -y
choco install visualstudio2019-workload-vctools -y
```

---

## 4. Core Development Tools

### 4.1 Languages & Runtimes

| Tool | Version | Install Method |
|---|---|---|
| **Python** | 3.13.x | `choco install python3` or [python.org](https://www.python.org/downloads/) |
| **Node.js** | 22.x | `winget install OpenJS.NodeJS.LTS` |
| **Java (Corretto 21)** | 21.0.7 | IntelliJ auto-downloads to `~/.jdks/` |
| **Rust** | via rustup | `scoop install rustup` then `rustup default stable` |

```powershell
# Verify installations
python --version      # 3.13.x
node --version        # v22.x
npm --version         # 10.x
java -version         # openjdk 21.0.7
rustup --version      # 1.28.x
```

### 4.2 Python Global Packages

```powershell
pip install graphifyy
pip install python-docx
pip install python-dotenv
pip install psycopg2-binary
pip install lxml
pip install networkx
pip install httpx
pip install firebase-admin
pip install google-cloud-firestore
pip install google-cloud-storage
pip install tree-sitter
pip install tree-sitter-java
pip install tree-sitter-javascript
pip install tree-sitter-python
pip install tree-sitter-c
pip install tree-sitter-cpp
pip install tree-sitter-c-sharp
pip install tree-sitter-go
pip install tree-sitter-kotlin
```

### 4.3 Git Configuration

```powershell
git config --global user.name "Linh Hoàng Dương"
git config --global user.email "linh.hoang.duong@mgm-tp.com"
git config --global credential.https://bitbucket.mgm-tp.com.provider bitbucket
git config --global includeif.gitdir:H:/WORKSPACE/Personal/.path .gitconfig-personal
git config --global core.editor '"C:\Users\johny\AppData\Local\Programs\Microsoft VS Code\bin\code" --wait'
```

> **Note:** You have a conditional `.gitconfig-personal` that activates for personal repos under `H:/WORKSPACE/Personal/`. Make sure to recreate this file with your personal email/signing config.

---

## 5. IDEs & Editors

### 5.1 Google Antigravity
```powershell
winget install Google.Antigravity
# Version at snapshot: 1.22.2
```

### 5.2 Visual Studio Code
```powershell
winget install Microsoft.VisualStudioCode
# Version at snapshot: 1.114.0

# Restore settings via Settings Sync (sign in with GitHub/Microsoft account)
# Extensions will auto-restore if Settings Sync was enabled
```

### 5.3 IntelliJ IDEA
```powershell
# Download from: https://www.jetbrains.com/idea/download/
# Or use JetBrains Toolbox: https://www.jetbrains.com/toolbox-app/
# Version at snapshot: 2024.3.6

# Java SDK: Amazon Corretto 21.0.7 (auto-downloads in IntelliJ)
# Location: C:\Users\johny\.jdks\corretto-21.0.7\

# User env var set:
[System.Environment]::SetEnvironmentVariable("IntelliJ IDEA", "C:\Program Files\JetBrains\IntelliJ IDEA 2024.3.6\bin;", "User")
```

---

## 6. Podman & Container Infrastructure

### 6.1 Install Podman

```powershell
winget install RedHat.Podman
winget install RedHat.Podman-Desktop
# Desktop version at snapshot: 1.18.0
```

### 6.2 Initialize Podman Machine

```powershell
# Create and start the Podman machine (WSL2 backend)
podman machine init podman-bsd-machine --cpus 12 --memory 2048 --disk-size 100
podman machine start podman-bsd-machine
podman machine set podman-bsd-machine --default
```

### 6.3 Your Containers (Exact Reproduction Commands)

#### Container 1: `oracle19` — Oracle Database 19c
```powershell
# Image: dockerregistry.mgm-tp.com/com.mgmtp.lidl.wfm/wfm-oracle-db:19.18.0
# Volume: wfm-bsd_oracle-data → /opt/oracle/oradata
# Ports: 1521→1521 (SQL*Net), 8888→5500 (EM Express)

podman volume create wfm-bsd_oracle-data
podman run -d \
    --name oracle19 \
    -p 1521:1521 \
    -p 8888:5500 \
    -v wfm-bsd_oracle-data:/opt/oracle/oradata \
    dockerregistry.mgm-tp.com/com.mgmtp.lidl.wfm/wfm-oracle-db:19.18.0
```

#### Container 2: `wfm-activemq` — ActiveMQ Classic
```powershell
# Image: docker.io/apache/activemq-classic:latest
# Volume: wfm-bsd_activemq-data

podman volume create wfm-bsd_activemq-data
podman run -d \
    --name wfm-activemq \
    -p 1099:1099 -p 1883:1883 -p 5672:5672 \
    -p 8161:8161 -p 61613-61614:61613-61614 -p 61616:61616 \
    docker.io/apache/activemq-classic:latest
```

#### Container 3: `bsd-postgres` — PostgreSQL (Work)
```powershell
# Image: docker.io/library/postgres:latest
# Volume: wfm-bsd_postgres-data
# Port: 5532→5432

podman volume create wfm-bsd_postgres-data
podman run -d \
    --name bsd-postgres \
    -p 5532:5432 \
    -v wfm-bsd_postgres-data:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=yourpassword \
    docker.io/library/postgres:latest
```

#### Container 4: `based-workspace-postgres` — PostgreSQL + pgvector
```powershell
# Image: docker.io/pgvector/pgvector:pg16
# Volume: infrastructure-core_based-workspace-postgres-data
# Port: 5432→5432

podman volume create infrastructure-core_based-workspace-postgres-data
podman run -d \
    --name based-workspace-postgres \
    -p 5432:5432 \
    -v infrastructure-core_based-workspace-postgres-data:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=yourpassword \
    --network based-workspace-net \
    docker.io/pgvector/pgvector:pg16
```

#### Container 5: `n8n-atom` — n8n Automation (Fork)
```powershell
# Image: docker.io/atom8n/n8n:fork
# Volume: infrastructure-core_based-workspace-n8n-data
# Port: 5678→5888

podman volume create infrastructure-core_based-workspace-n8n-data
podman run -d \
    --name n8n-atom \
    -p 5678:5888 \
    -v infrastructure-core_based-workspace-n8n-data:/home/node/.n8n \
    --network based-workspace-net \
    docker.io/atom8n/n8n:fork
```

#### Container 6: `mcp-inspector` — MCP Inspector
```powershell
# Image: ghcr.io/modelcontextprotocol/inspector:latest
# Ports: 6274, 6277

podman run -d \
    --name mcp-inspector \
    -p 6274:6274 -p 6277:6277 \
    ghcr.io/modelcontextprotocol/inspector:latest
```

#### Container 7: `antigravity-manager`
```powershell
# Image: docker.io/lbjlaq/antigravity-manager:latest
# Port: 8045

podman run -d \
    --name antigravity-manager \
    -p 8045:8045 \
    docker.io/lbjlaq/antigravity-manager:latest
```

### 6.4 Networks

```powershell
podman network create based-workspace-net
podman network create oracle_default
podman network create wfm-bsd_default
podman network create infrastructure-advanced_default
```

### 6.5 All Volumes Summary

| Volume Name | Used By | Purpose |
|---|---|---|
| `wfm-bsd_oracle-data` | oracle19 | Oracle 19c datafiles |
| `wfm-bsd_activemq-data` | wfm-activemq | ActiveMQ data |
| `wfm-bsd_postgres-data` | bsd-postgres | Work PostgreSQL |
| `infrastructure-core_based-workspace-postgres-data` | based-workspace-postgres | pgvector AI memory |
| `infrastructure-core_based-workspace-n8n-data` | n8n-atom | n8n workflows |
| `infrastructure_advanced_antigravity_data` | antigravity-manager | Antigravity manager data |
| `infrastructure-ai_based-workspace-ollama-data` | (ollama) | Ollama AI models |
| `infrastructure-webui_open-webui-data` | (open-webui) | Open WebUI data |
| `n8n-atom-quickstart_*` | (quickstart variants) | Quickstart n8n/postgres |
| `infrastructure-core-quickstart_*` | (quickstart variants) | Quickstart core |

> **Note:** The `based-workspace` containers can also be started via Docker Compose:
> ```powershell
> cd H:\WORKSPACE\Personal\Vibe\based-workspace
> podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d
> ```

---

## 7. Applications (Install via `winget`)

### 7.1 Developer Tools
```powershell
winget install Microsoft.PowerShell
winget install Microsoft.WindowsTerminal
winget install Microsoft.VisualStudioCode
winget install Google.Antigravity
winget install JetBrains.IntelliJIDEA.Ultimate  # or Community
winget install RedHat.Podman
winget install RedHat.Podman-Desktop
winget install Git.Git
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.13
winget install Google.CloudSDK
winget install Postman.Postman
```

### 7.2 Productivity & Communication
```powershell
winget install Notion.Notion
winget install Cisco.CiscoWebexMeetings
winget install Microsoft.Teams
winget install Discord.Discord
```

### 7.3 Media & Creative
```powershell
winget install OBSProject.OBSStudio
winget install ElementLabs.LMStudio
# Adobe Photoshop & Lightroom: Install via Adobe Creative Cloud
```

### 7.4 Gaming
```powershell
winget install Valve.Steam
winget install Guru3D.RTSS  # RivaTuner Statistics Server
# Overwolf: Download from https://www.overwolf.com
# Riot Games: Download from https://www.riotgames.com
# Delta Force: Install via Garena launcher
```

### 7.5 System Utilities
```powershell
winget install DucFabulous.UltraViewer
winget install AnyDesk.AnyDesk
winget install Cloudflare.Warp
# Kaspersky: Install from license
# Norton: Install from license
# EVKey (Vietnamese keyboard): Download from https://evkey.vn
# MSI Afterburner: Download from https://www.msi.com/Landing/afterburner
```

### 7.6 VPN & Networking
```powershell
# Cisco Secure Client (AnyConnect): Provided by your company IT
# Cloudflare WARP: Already in list above
```

---

## 8. Startup Programs

These apps launch on Windows boot:

| App | Purpose | Auto-start? |
|---|---|---|
| **Podman Desktop** | Container management | ✅ Yes |
| **OneDrive** | Cloud sync | ✅ Yes |
| **Discord** | Chat | ✅ Yes |
| **Riot Client** | Gaming (Vanguard anti-cheat) | ✅ Yes |
| **Notion** | Notes | ✅ Yes |
| **Steam** | Gaming (silent mode) | ✅ Yes |
| **Cisco Webex** | Work meetings | ✅ Yes |
| **Kaspersky** | Security | ✅ Yes |
| **Cloudflare WARP** | VPN/proxy | ✅ Yes |
| **AnyDesk** | Remote desktop | ✅ Yes |
| **EVKey** | Vietnamese keyboard | ✅ Yes |
| **MSI Afterburner** | GPU monitoring | ✅ Yes |
| **NVIDIA App** | GPU management | ✅ Yes |

---

## 9. Environment Variables (User-Level)

```powershell
# Set these after installing everything:
[System.Environment]::SetEnvironmentVariable("CARGO_HOME", "C:\Users\johny\scoop\persist\rustup\.cargo", "User")
[System.Environment]::SetEnvironmentVariable("RUSTUP_HOME", "C:\Users\johny\scoop\persist\rustup\.rustup", "User")
[System.Environment]::SetEnvironmentVariable("IntelliJ IDEA", "C:\Program Files\JetBrains\IntelliJ IDEA 2024.3.6\bin;", "User")
```

### User PATH Entries
```
C:\Users\johny\scoop\apps\rustup\current\.cargo\bin
C:\Users\johny\scoop\shims
C:\Users\johny\AppData\Local\Microsoft\WindowsApps
C:\Users\johny\AppData\Local\Programs\Microsoft VS Code\bin
C:\Program Files\JetBrains\IntelliJ IDEA 2024.3.6\bin
C:\Users\johny\AppData\Roaming\npm
C:\Users\johny\AppData\Local\Programs\Antigravity\bin
C:\Users\johny\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin
C:\Users\johny\.lmstudio\bin
C:\Users\johny\.local\bin
```

---

## 10. Disk Layout (To Recreate)

| Disk | Drive | Size | Content |
|---|---|---|---|
| **Disk 0** (Samsung NVMe 954 GB) | C: | 924 GB | Windows 11 Pro + Programs |
| **Disk 1** (WDC NVMe 932 GB) | H: | 367 GB | WORKSPACE, Learning, ISOs |
| **Disk 1** (WDC NVMe 932 GB) | I: | 563 GB | Games (Steam, Riot), Personal files |

### Folder Structure to Recreate

```
H:\
├── WORKSPACE\
│   ├── mgm\                        # Work projects (Lidl WFM, BSD)
│   ├── Old\                        # Archived projects (Almex, Citynow, Intern)
│   └── Personal\
│       ├── Vibe\based-workspace\   # AI workspace (this project!)
│       ├── aop-demo\               # Spring AOP demo
│       ├── reactive\               # Reactive programming
│       ├── webtool\                # Web tools project
│       └── ...
├── Learning\UIT\                   # University materials
├── ISO and Installer\              # Windows installers & configs
├── SteamLibrary\                   # Steam library (empty or games)
├── app\                            # App logs
├── opt\wfm\                        # WFM work tools
└── tmp\                            # Temp files

I:\
├── SteamLibrary\steamapps\         # 7 Steam games
├── Game\
│   ├── Riot Games\                 # League of Legends, VALORANT
│   ├── Delta Force\                # Delta Force (Garena)
│   └── PlayStation\                # PS Remote Play
└── Harry\
    ├── Photos\                     # Personal photos
    ├── Software\                   # Software backups
    └── Linh tinh\                  # Miscellaneous
```

---

## 11. SSH Keys

```
~\.ssh\
└── known_hosts (409 bytes)
```

> ⚠️ **No private SSH keys detected!** You may be using:
> - Credential Manager for HTTPS Git authentication
> - Windows SSH Agent with keys loaded in memory  
> - Company-managed SSH via Cisco/VPN
>
> **Before rebuilding:** Run `ssh-add -l` to check if any keys are loaded in the agent.
> If you use SSH keys for Git, make sure to back up `id_rsa` / `id_ed25519` from `~/.ssh/`.

---

## 12. Complete Rebuild Script (One-Shot)

Save this as `rebuild_windows.ps1` and run as Administrator after a fresh Windows install:

```powershell
# ============================================================
# Windows 11 Complete Rebuild Script
# Generated from system snapshot: 2026-04-12
# ============================================================

Write-Host "Step 1/8: Installing package managers..." -ForegroundColor Cyan

# Scoop
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
scoop bucket add extras
scoop install 7zip docker grep helm kubectl pipx ripgrep rustup

# Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

Write-Host "Step 2/8: Installing core developer tools..." -ForegroundColor Cyan
winget install Microsoft.PowerShell --accept-package-agreements --accept-source-agreements -e
winget install Microsoft.WindowsTerminal -e
winget install Git.Git -e
winget install Python.Python.3.13 -e
winget install OpenJS.NodeJS.LTS -e
winget install Google.CloudSDK -e

Write-Host "Step 3/8: Installing IDEs & editors..." -ForegroundColor Cyan
winget install Google.Antigravity -e
winget install Microsoft.VisualStudioCode -e
# IntelliJ: Install manually or via Toolbox

Write-Host "Step 4/8: Installing Podman..." -ForegroundColor Cyan
winget install RedHat.Podman -e
winget install RedHat.Podman-Desktop -e

Write-Host "Step 5/8: Installing productivity apps..." -ForegroundColor Cyan
winget install Notion.Notion -e
winget install Cisco.CiscoWebexMeetings -e
winget install Microsoft.Teams -e
winget install Discord.Discord -e
winget install Postman.Postman -e

Write-Host "Step 6/8: Installing media & utility apps..." -ForegroundColor Cyan
winget install OBSProject.OBSStudio -e
winget install ElementLabs.LMStudio -e
winget install Valve.Steam -e
winget install DucFabulous.UltraViewer -e
winget install AnyDesk.AnyDesk -e
winget install Cloudflare.Warp -e

Write-Host "Step 7/8: Installing Python packages..." -ForegroundColor Cyan
pip install graphifyy python-docx python-dotenv psycopg2-binary lxml networkx httpx
pip install firebase-admin google-cloud-firestore google-cloud-storage
pip install tree-sitter tree-sitter-java tree-sitter-javascript tree-sitter-python

Write-Host "Step 8/8: Configuring Git..." -ForegroundColor Cyan
git config --global user.name "Linh Hoàng Dương"
git config --global user.email "linh.hoang.duong@mgm-tp.com"
git config --global core.editor '"C:\Users\johny\AppData\Local\Programs\Microsoft VS Code\bin\code" --wait'
git config --global credential.https://bitbucket.mgm-tp.com.provider bitbucket

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Rebuild complete!" -ForegroundColor Green
Write-Host "  Manual steps remaining:" -ForegroundColor Yellow
Write-Host "  1. Install NVIDIA drivers from nvidia.com" -ForegroundColor Yellow
Write-Host "  2. Install Adobe Creative Cloud" -ForegroundColor Yellow
Write-Host "  3. Install JetBrains IntelliJ IDEA" -ForegroundColor Yellow
Write-Host "  4. Install Kaspersky from license" -ForegroundColor Yellow
Write-Host "  5. Install EVKey from evkey.vn" -ForegroundColor Yellow
Write-Host "  6. Install Cisco Secure Client from IT" -ForegroundColor Yellow
Write-Host "  7. Initialize Podman machine" -ForegroundColor Yellow
Write-Host "  8. Clone based-workspace repo" -ForegroundColor Yellow
Write-Host "  9. Restore SSH keys from backup" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green
```

---

## 13. Post-Rebuild Verification

```powershell
Write-Host "=== System Rebuild Verification ==="
@("python", "node", "npm", "git", "java", "podman", "code", "antigravity") | ForEach-Object {
    $cmd = $_
    try {
        $ver = & $cmd --version 2>&1 | Select-Object -First 1
        Write-Host "  OK  $cmd = $ver" -ForegroundColor Green
    } catch {
        Write-Host "  MISSING  $cmd" -ForegroundColor Red
    }
}
```
