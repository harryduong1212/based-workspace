# 🗺️ Master Migration Roadmap & Progress Tracker

> **How to use this tracker:**  
> Keep this file open during your migration. Every time you finish a phase, check the box `[x]`. This ensures you never lose track of what state you are in.

---

## 📍 Current Status

You are currently **PREPARING FOR MIGRATION (Windows)**. \
Next step: **Phase 1: Backup & Fallback Strategy**.

---

## 🛤️ The Migration Path

### 🟩 Step 1: Preparation (Do these in Windows right now)
- [ ] **Phase 0:** Read `00_windows_to_linux_guide.md` to mentally prepare for the differences.
- [x] **Phase 1:** Read and execute `01_backup_and_fallback_strategy.md` to disable Fast Startup and upload your data to Google Drive.
- [x] **Phase 2:** Read `02_linux_distribution_comparison.md` (Optional - just to review why we chose Fedora).
- [x] **Phase 4 (Part 1):** Read `04_podman_zero_data_loss_migration.md` and run the *Windows Side Export Procedure* to save your containers.
- [ ] **Phase 8:** Save `08_windows_rebuild_blueprint.md` to your Google Drive just in case you ever need to rebuild Windows.

### 🟧 Step 2: The Point of No Return (Installing Linux)
- [x] **Phase 3:** Review `03_drive_partitioning_and_dual_boot.md` so you understand what we are going to do to your drives.
- [ ] **Phase 5 (Part 1):** Follow `05_linux_installation_and_post_boot.md` to boot the Fedora USB, wipe Disk 1, and install Fedora.

### 🟦 Step 3: Landing in Linux (Do these in Fedora)
- [ ] **Phase 5 (Part 2):** Run the post-boot scripts in `05_linux_installation_and_post_boot.md` to install drivers and mount your shared drive.
- [ ] **Phase 6:** Run the single bulk install script in `06_app_migration_and_workarounds.md` to restore all your daily apps.
- [ ] **Phase 4 (Part 2):** Run the *Linux Side Import Procedure* in `04_podman_zero_data_loss_migration.md` to restore your databases and N8N.
- [ ] **Phase 7:** Go through `07_master_checklist_and_verification.md` to verify your entire system is perfectly configured.

---

### 🚨 Emergency / Lost?
* If you haven't rebooted with the Fedora USB yet: **You are in Step 1**. (No data has changed).
* If you are in the Fedora installer: **You are in Step 2**.
* If you are looking at the GNOME Desktop (Fedora): **You are in Step 3**.
