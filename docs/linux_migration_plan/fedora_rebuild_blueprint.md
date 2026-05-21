# Fedora 43 Complete System Rebuild Blueprint

> **System Snapshot Date:** 2026-04-16
> **Machine:** AMD Ryzen AI 9 HX 370 / RTX 4060 Laptop / 32 GB RAM
> **OS:** Fedora Linux 43 (Workstation Edition)
> **Purpose:** If you ever need to reinstall Fedora from scratch, follow this guide to restore your exact developer setup.

---

## 1. Hardware & System Baseline

| Component | Status/Driver Setup |
|---|---|
| **AMD Ryzen AI 9 HX 370 + 890M** | Native kernel support (Linux 6.19+) |
| **NVIDIA RTX 4060 Laptop** | Proprietary NVIDIA drivers (via RPM Fusion) |
| **Audio & Peripherals** | PipeWire handles native audio automatically |

> [!CAUTION] 
> **Uninstallation Warning:** When removing packages (like `vulkan`), carefully review the `dnf` or `flatpak` transaction. Removing dependencies might unintentionally break other tools (e.g., removing `vulkan` breaks `howdy`). Always check what "dependent packages" will be removed before confirming `Y`.

---

## 2. Package Management & Software Installation

### Native DNF Packages (System Utilities & Dev Tools)

```bash
# First, ensure your system is up to date
sudo dnf upgrade --refresh

# Install core development tools
sudo dnf install git zsh util-linux nodejs java-25-openjdk java-21-openjdk maven
```

### Flatpak Applications (Sandboxed Desktop Apps)

Most desktop apps are installed via Flatpak for isolation.

```bash
# Add Flathub if not already added
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# Installed Flatpaks:
flatpak install flathub com.discordapp.Discord
flatpak install flathub com.getpostman.Postman
flatpak install flathub com.google.Chrome
flatpak install flathub com.obsproject.Studio
flatpak install flathub md.obsidian.Obsidian
```

---

## 3. Core Development Tools

### 3.1 SDKMAN! (Java Management)
Project requires specific Java versions (Java 17/21). Use SDKMAN to avoid Fedora repository deprecation issues.

```bash
# Install SDKMAN!
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install Java versions
sdk install java 21.0.10-tem
sdk install java 25.0.2-tem

# Permanent JAVA_HOME in ~/.zshrc:
# export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
# export PATH=$JAVA_HOME/bin:$PATH
```

### 3.2 Node & Maven
- **Node.js**: v22.22.0 (Installed natively via DNF)
- **Maven**: 3.9.11 (Installed natively via DNF `sudo dnf install maven`)

#### Workspace-Specific NPM Registries (direnv)
Because NPM does not deeply resolve `.npmrc` files beyond the project root, using `direnv` is critical for gracefully separating global and work-scoped credentials (e.g., routing `mgm` workspaces to Artifactory).

1. Install direnv: `sudo dnf install -y direnv`
2. Hook it into your shell (`~/.bashrc` or `~/.zshrc`): `eval "$(direnv hook bash)"` (or `zsh`)
3. Create `.envrc` inside your isolated workspace:
   ```bash
   export NPM_CONFIG_USERCONFIG="/home/harry/Workspace/mgm/.npmrc"
   ```
4. Run `direnv allow` in that workspace. Now, any `npm` or `mvn` build inside this tree will use these credentials automatically!

### 3.3 Default Shell (ZSH)
Instead of Bash, ZSH is the default shell.
```bash
# Change default shell to zsh
chsh -s $(which zsh)
```

---

## 4. IDEs & Editors

### 4.1 IntelliJ IDEA Ultimate
**Important:** Do NOT install via Flatpak. Flatpak runs in a sandbox and will cause "restricted shell" errors (`mvn not found`, `sudo not found`).
- **Install natively:** Download from JetBrains website (`.tar.gz`) or use **JetBrains Toolbox** natively.
- **SDK Setup:** Go to **File > Project Structure > SDKs** and point to `/usr/lib/jvm/java-21-openjdk` or your SDKMAN paths.

### 4.2 SQL Workbench Integration
Create a native shortcut so it's searchable via the Super key.

```bash
# Create desktop file
nano ~/.local/share/applications/sql-workbench.desktop

# Add contents:
[Desktop Entry]
Type=Application
Terminal=false
Name=SQL Workbench
Exec=bash "/home/harry/Workspace/mgm/Config/WFM config/Workbench-Build131.2/sqlworkbench.sh"
Icon=utilities-terminal
Categories=Development;Database;

# Make executable and validate
chmod +x "/home/harry/Workspace/mgm/Config/WFM config/Workbench-Build131.2/sqlworkbench.sh"
chmod +x ~/.local/share/applications/sql-workbench.desktop
desktop-file-validate ~/.local/share/applications/sql-workbench.desktop
```

---

## 5. Podman & Container Infrastructure

Fedora natively supports Podman instead of Docker. No WSL2 overhead!

### 5.1 Installation
```bash
sudo dnf install podman podman-compose podman-desktop
# Verified versions: Podman 5.8.1, podman-compose 1.5.0
```

### 5.2 Container Reproduction
No data loss migration means you map the same directory structures.

```bash
# Recreate networks
podman network create based-workspace-net
podman network create oracle_default
podman network create wfm-bsd_default

# Recreate volumes
podman volume create wfm-bsd_oracle-data
podman volume create wfm-bsd_activemq-data
podman volume create wfm-bsd_postgres-data
podman volume create infrastructure-core_based-workspace-postgres-data
podman volume create infrastructure-core_based-workspace-n8n-data
```

*(See Windows 11 blueprint for full exact `podman run` commands, simply run them directly natively in Fedora Terminal).*

---

## 6. Tomcat Environment Fixes (`setenv.sh`)
When running Tomcat natively, the old Windows `setenv.bat` will fail. Use `setenv.sh`.
- Remove the deprecated `-XX:+UseConcMarkSweepGC`.
- Ensure all `--add-opens` flags exist for Java 16+ modularity.
- Refer to your archived `setenv.sh` for exact properties (`-Dmgm.dbconfig`, etc.).

---

## 7. Fixing the Keyring System (Auto-Unlock)
If you are repeatedly asked for a password to unlock the default keyring upon boot.

1. Ensure your login password matches the keyring password.
2. Edit PAM config: `sudo nano /etc/pam.d/gdm-password`
3. Add at the end of the `auth` section:
   `auth optional pam_gnome_keyring.so`
4. Add at the end of the `session` section:
   `session optional pam_gnome_keyring.so auto_start`
5. Remove any duplicates.

---

## 8. Cisco AnyConnect VPN Workaround
Using AnyConnect SSL-VPN requires the correct NetworkManager plugin.

```bash
# Install openconnect for GNOME
sudo dnf install NetworkManager-openconnect-gnome

# Configuration:
# 1. Settings > Network > + > Multi-protocol VPN client (openconnect)
# 2. Enter Gateway
# 3. Connect (will prompt for Single Sign-On / SAML login).
```
