# Phase 4: Podman Zero-Data-Loss Migration

> **Generated:** 2026-04-12 20:55
> **Focus:** Oracle Database container and volume preservation

---

## 4.1 Current Podman Inventory

### Containers
- `antigravity-manager`
- `bsd-postgres`
- `oracle19`
- `based-workspace-postgres`
- `n8n-atom`
- `mcp-inspector`
- `wfm-activemq`

### Volumes
- `infrastructure_advanced_antigravity_data`
- `infrastructure-ai_based-workspace-ollama-data`
- `infrastructure-webui_open-webui-data`
- `wfm-bsd_oracle-data`
- `wfm-bsd_activemq-data`
- `wfm-bsd_postgres-data`
- `infrastructure-core_based-workspace-postgres-data`
- `infrastructure-core_based-workspace-n8n-data`
- `n8n-atom-quickstart_n8n-atom-data`
- `n8n-atom-quickstart_based-workspace-postgres-data`
- `infrastructure-core-quickstart_based-workspace-postgres-data`
- `infrastructure-core-quickstart_n8n-atom-data`

### Images
- `docker.io/based-workspace/n8n-atom:latest`
- `docker.io/library/infrastructure-core-mcp-inspector:latest`
- `docker.io/based-workspace/mcp-inspector:latest`
- `docker.io/library/infrastructure-core-n8n-atom:latest`
- `docker.io/ollama/ollama:latest`
- `ghcr.io/open-webui/open-webui:main`
- `docker.n8n.io/n8nio/n8n:latest`
- `docker.io/library/node:22-alpine`
- `docker.io/library/node:22-bookworm-slim`
- `docker.io/library/node:22-bookworm`
- `docker.io/library/node:24-slim`
- `docker.io/lbjlaq/antigravity-manager:latest`
- `docker.io/library/postgres:latest`
- `ghcr.io/modelcontextprotocol/inspector:latest`
- `docker.io/pgvector/pgvector:pg16`
- `docker.io/library/postgres:16-alpine`
- `docker.io/atom8n/n8n:fork`
- `docker.io/n8nio/base:22.21.1`
- `docker.io/apache/activemq-classic:latest`
- `dockerregistry.mgm-tp.com/com.mgmtp.lidl.wfm/wfm-oracle-db:19.18.0`

> 💡 If containers/volumes appear empty, they may be running inside WSL2.
> Check with: `wsl -d podman-machine-default podman ps -a`

---

## 4.2 Pre-Migration: Full Inventory Snapshot

Run these commands **before** migration day to capture everything:

```powershell
# Create export directory on shared drive
New-Item -ItemType Directory -Path "C:\Backups\exports\podman" -Force
$exportDir = "C:\Backups\exports\podman"

# Snapshot all Podman state
podman ps -a --format json | Out-File "$exportDir\containers.json" -Encoding utf8
podman images --format json | Out-File "$exportDir\images.json" -Encoding utf8
podman volume ls --format json | Out-File "$exportDir\volumes.json" -Encoding utf8
podman network ls --format json | Out-File "$exportDir\networks.json" -Encoding utf8

# Inspect every container for recreation commands
foreach ($container in (podman ps -a --format "{{.Names}}")) {
    podman inspect $container | Out-File "$exportDir\inspect_$container.json" -Encoding utf8
    Write-Host "Inspected: $container"
}
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
foreach ($container in (podman ps -a --format "{{.Names}}")) {
    podman commit $container "${container}-backup:latest"
    Write-Host "Committed: $container"
}

# Save only images used by containers and their committed backups
$imagesToSave = (podman ps -a --format "{{.Image}}") + (podman ps -a --format "{{.Names}}-backup:latest")
foreach ($image in ($imagesToSave | Select-Object -Unique | Where-Object { $_ -ne "<none>:<none>" -and $_ -match "\w" })) {
    $safeName = $image -replace '[/:]', '_'
    podman save -o "C:\Backups\exports\podman\image_$safeName.tar" $image
    Write-Host "Saved image: $image"
}
```

### Step 3: Export ALL Named Volumes (Critical for Oracle)

```powershell
# Export each volume to a tar file (using an alpine container because remote volume export fails on Windows)
foreach ($vol in (podman volume ls --format "{{.Name}}")) {
    podman run --rm -v "${vol}:/volume_data:ro" -v "C:\Backups\exports\podman:/backup" docker.io/library/alpine tar -cf "/backup/vol_${vol}.tar" -C /volume_data .
    Write-Host "Exported volume: $vol"

    # Also record volume metadata
    podman volume inspect $vol | Out-File "C:\Backups\exports\podman\vol_${vol}_inspect.json" -Encoding utf8
}
```

> ⚠️ **ORACLE DATABASE SPECIFIC:**
> The Oracle data volume typically contains the datafiles, control files,
> and redo logs. The alpine `tar` command captures ALL of this
> as a complete archive, preserving the byte-perfect state.

### Step 4: Export Podman Networks

```powershell
foreach ($net in (podman network ls --format "{{.Name}}" | Where-Object { $_ -ne "podman" })) {
    podman network inspect $net | Out-File "C:\Backups\exports\podman\net_$net.json" -Encoding utf8
    Write-Host "Exported network config: $net"
}
```

### Step 5: Verify Export Integrity

```powershell
# List all exported files with sizes
Get-ChildItem "C:\Backups\exports\podman" | Format-Table Name, Length -AutoSize

# Verify tar files are valid
foreach ($tar in (Get-ChildItem "C:\Backups\exports\podman\*.tar")) {
    $testResult = tar -tf $tar.FullName 2>&1 | Select-Object -First 3
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Valid: $($tar.Name)"
    } else {
        Write-Host "❌ CORRUPT: $($tar.Name) — RE-EXPORT THIS FILE"
    }
}
```

### Step 6: Cleanup Local Backup Images (Optional)

Once the export is verified, you can delete the temporary `-backup:latest` images created during the commit step to free up space on Windows:

```powershell
foreach ($image in (podman images --format "{{.Repository}}:{{.Tag}}" | Where-Object { $_ -like "*-backup:latest" })) {
    podman rmi $image
    Write-Host "Removed temporary backup image: $image"
}
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

podman unshare chown -R 54321:54321 \
    ~/.local/share/containers/storage/volumes/oracle_data_vol/_data

# Verify the fix
podman unshare ls -la \
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
podman run -d \
    --name oracle-db-container \
    -p 1521:1521 \
    -p 5500:5500 \
    -v oracle_data_vol:/opt/oracle/oradata \
    -e ORACLE_PWD=YourSecurePassword \
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
