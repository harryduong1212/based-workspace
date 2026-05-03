# Syncthing Setup — Fedora ↔ Samsung Galaxy Tab S9+

> Reference doc for syncing study materials between the Fedora laptop and Android tablet via Syncthing. Covers initial setup, common operations, and troubleshooting.

---

## Current Configuration

### Devices

| Device | Name | Device ID | OS |
|--------|------|-----------|-----|
| Laptop | `fedora` | `IXMTBBB-BFG3GWC-2ZRVCWC-24PLTXO-EMMKW7P-DVJPXX6-ZQH6UN5-DHOBUQU` | Fedora Linux |
| Tablet | `SM-X816B` | `XQVYE5Z-3YSEIZJ-PI3KNKI-EJPGXOX-N6SBOOD-YRTW2KX-O4PAH3E-V5V4LQT` | Android (Samsung Galaxy Tab S9+) |

### Shared Folders

| Folder ID | Label | Laptop Path | Tablet Path |
|-----------|-------|-------------|-------------|
| `study-materials` | Java 21 Study Materials | `/home/harry/Workspace/Personal/Vibe/based-workspace/other-docs/ai_orchestrator_study_materials` | `/storage/emulated/0/Documents/StudyMaterials` |

### What Gets Synced

```
ai_orchestrator_study_materials/
├── 21-day-sprint/          ← 21-day study sprint schedule
│   ├── week-1-foundations/
│   ├── week-2-security-and-ai/
│   └── week-3-mastery/
└── java-21-study-guide/    ← 10-module study guide (27 files)
    ├── 01-core/
    ├── 02-collections/
    ├── 03-concurrency/
    ├── 04-jvm/
    ├── 05-ecosystem/
    ├── 06-microservices/
    ├── 07-security-and-identity/
    ├── 08-infrastructure/
    ├── 09-ai-orchestration/
    └── 10-system-design-leadership/
```

---

## Access Points

| What | URL / Location |
|------|----------------|
| Syncthing Web UI (Laptop) | http://127.0.0.1:8384/ |
| Syncthing API Key | `ExPzAkMHESUAHsHWHMXL6qR4buD6snWA` |
| Config file (Laptop) | `~/.local/state/syncthing/config.xml` |
| Systemd service | `syncthing.service` (user-level) |

---

## Common Operations

### Check Syncthing Status

```bash
systemctl --user status syncthing.service
```

### Start / Stop / Restart

```bash
# Start
systemctl --user start syncthing.service

# Stop
systemctl --user stop syncthing.service

# Restart
systemctl --user restart syncthing.service
```

### Force Rescan (After Editing Files)

Syncthing watches for file changes automatically (via `fsWatcherEnabled`), but if you want to force a rescan:

```bash
# Via API
curl -s -X POST \
  -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  http://127.0.0.1:8384/rest/db/scan?folder=study-materials

# Or just open the Web UI and click "Rescan All"
```

### Check Folder Sync Status

```bash
curl -s -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  http://127.0.0.1:8384/rest/db/status?folder=study-materials | python3 -m json.tool
```

### Check Device Connection

```bash
curl -s -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  http://127.0.0.1:8384/rest/system/connections | python3 -c "
import json, sys
data = json.load(sys.stdin)
for did, info in data.get('connections', {}).items():
    print(f'{did[:7]}... connected={info[\"connected\"]} type={info.get(\"type\",\"?\")}')
"
```

---

## Adding a New Shared Folder

If you want to sync a new folder (e.g., a new study topic):

```bash
# 1. Add the folder via API
curl -s -X POST \
  -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-new-folder",
    "label": "My New Folder",
    "path": "/home/harry/path/to/folder",
    "type": "sendreceive",
    "rescanIntervalS": 60,
    "fsWatcherEnabled": true,
    "fsWatcherDelayS": 10,
    "devices": [
      {"deviceID": "XQVYE5Z-3YSEIZJ-PI3KNKI-EJPGXOX-N6SBOOD-YRTW2KX-O4PAH3E-V5V4LQT"}
    ]
  }' \
  http://127.0.0.1:8384/rest/config/folders

# 2. On the tablet: accept the folder share notification in Syncthing-Fork
```

Or just use the Web UI at http://127.0.0.1:8384/ → **"+ Add Folder"**.

---

## Fresh Install (From Scratch)

If you need to set everything up again on a new Fedora install:

### Step 1: Install Syncthing

```bash
sudo dnf install -y syncthing
```

### Step 2: Enable & Start as User Service

```bash
systemctl --user enable syncthing.service
systemctl --user start syncthing.service
```

This starts Syncthing automatically on login. No root needed.

### Step 3: Open Web UI & Configure

Open http://127.0.0.1:8384/ in your browser.

### Step 4: Add the Study Materials Folder

Via Web UI: Click **"+ Add Folder"** →
- **Folder Label**: `Java 21 Study Materials`
- **Folder ID**: `study-materials`
- **Folder Path**: `/home/harry/Workspace/Personal/Vibe/based-workspace/other-docs/ai_orchestrator_study_materials`
- Check **"Watch for Changes"**

### Step 5: Pair with Tablet

1. On the tablet, open Syncthing-Fork → **Device ID** (find it in Settings or the main screen)
2. On the laptop Web UI → **"+ Add Remote Device"** → paste the tablet's Device ID
3. On the tablet, accept the pairing request
4. On the laptop, click the folder → **Edit** → **Sharing** tab → check the tablet device
5. On the tablet, accept the folder share

### Step 6: Set Up Obsidian on Tablet

1. Install **Obsidian** from Play Store
2. Open Obsidian → **"Open folder as vault"**
3. Navigate to `/Documents/StudyMaterials`

---

## Tablet-Side Setup (Syncthing-Fork + Obsidian)

### Install Apps

1. **Syncthing-Fork** — Play Store (official Syncthing Android app is discontinued)
2. **Obsidian** — Play Store (free)

### Syncthing-Fork Settings (Recommended)

- **Run on startup**: Enable (Settings → Run on system startup)
- **Sync only on Wi-Fi**: Enable (Settings → Sync only on Wi-Fi) — saves mobile data
- **Battery optimization**: Exclude Syncthing-Fork from battery optimization so it syncs in the background

### Obsidian Vault Setup

1. Open Obsidian → Create vault → **"Open folder as vault"**
2. Navigate to the Syncthing folder: `Documents/StudyMaterials`
3. The vault will contain both `21-day-sprint/` and `java-21-study-guide/`

---

## Troubleshooting

### Devices Connected But Folder Shows "Unshared"

The folder is not shared with the device. Fix via API:

```bash
# 1. Get current folder config
curl -s -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  http://127.0.0.1:8384/rest/config/folders/study-materials > /tmp/fc.json

# 2. Add device to folder
python3 -c "
import json
with open('/tmp/fc.json') as f: config = json.load(f)
tablet = {'deviceID': 'XQVYE5Z-3YSEIZJ-PI3KNKI-EJPGXOX-N6SBOOD-YRTW2KX-O4PAH3E-V5V4LQT', 'introducedBy': '', 'encryptionPassword': ''}
ids = [d['deviceID'] for d in config.get('devices', [])]
if tablet['deviceID'] not in ids: config['devices'].append(tablet)
with open('/tmp/fc.json', 'w') as f: json.dump(config, f)
print('Done')
"

# 3. Apply
curl -s -X PUT \
  -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  -H "Content-Type: application/json" \
  -d @/tmp/fc.json \
  http://127.0.0.1:8384/rest/config/folders/study-materials

# 4. Restart to re-announce
curl -s -X POST -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  http://127.0.0.1:8384/rest/system/restart
```

### Tablet Not Receiving Folder Share Notification

1. Restart Syncthing on laptop: `systemctl --user restart syncthing.service`
2. On tablet: pull down to refresh in Syncthing-Fork
3. On tablet: open Syncthing-Fork → **Web GUI** (in menu) — check for banner at top
4. Verify both devices are on the same network

### Sync Seems Stuck

```bash
# Check for errors
curl -s -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  http://127.0.0.1:8384/rest/system/error | python3 -m json.tool

# Check folder errors
curl -s -H "X-API-Key: ExPzAkMHESUAHsHWHMXL6qR4buD6snWA" \
  http://127.0.0.1:8384/rest/folder/errors?folder=study-materials | python3 -m json.tool
```

### Conflict Files

If the same file is edited on both devices simultaneously, Syncthing creates a `.sync-conflict-*` file. Resolve manually:

```bash
# Find conflict files
find /home/harry/Workspace/Personal/Vibe/based-workspace/other-docs/ai_orchestrator_study_materials \
  -name "*.sync-conflict-*" -type f
```

### Reset Syncthing Completely

```bash
systemctl --user stop syncthing.service
systemctl --user disable syncthing.service
rm -rf ~/.local/state/syncthing/
# Then follow "Fresh Install" steps above
```

---

## Security Notes

- Syncthing uses **TLS encryption** for all connections — data is encrypted in transit
- Device pairing requires **mutual acceptance** — both sides must approve
- The API key (`ExPzAkMHESUAHsHWHMXL6qR4buD6snWA`) is local-only (bound to `127.0.0.1`)
- Consider setting a **Web UI password** at http://127.0.0.1:8384/ → Actions → Settings → GUI
