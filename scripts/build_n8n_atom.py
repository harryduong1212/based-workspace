import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


# =============================================================================
# Platform Helpers
# =============================================================================

def posix_volume_path(p: Path) -> str:
    """Convert any OS path to a format suitable for container volume mounts.

    On Windows, Docker/Podman expect either a Linux-style path (e.g., /c/Users/...)
    or a Windows-style path with forward slashes. We use the resolved absolute path
    which both Podman and Docker handle correctly on Windows.

    On macOS/Linux, the resolved POSIX path is already correct.
    """
    resolved = p.resolve()
    return str(resolved)


def get_volume_suffix() -> str:
    """On SELinux-enabled Linux (Fedora, RHEL), add :Z for proper labeling.

    SELinux (Security-Enhanced Linux) restricts which processes can access which
    files. When you mount a host directory into a container, SELinux may block the
    container from reading/writing those files. The ':Z' suffix tells the container
    engine to automatically relabel the files so the container can access them.

    Think of it like Java's SecurityManager — but enforced at the OS level.
    """
    if sys.platform == "linux":
        try:
            result = subprocess.run(
                ["getenforce"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip() in (
                "Enforcing",
                "Permissive",
            ):
                return ":Z"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    return ""


def detect_engine(preferred: str | None = None) -> str:
    """Auto-detect container engine. Podman is preferred on all platforms.

    Args:
        preferred: If set, try this engine first (from --engine flag).
    """
    engines = ["podman", "docker"]

    if preferred:
        preferred = preferred.lower()
        if preferred not in engines:
            print(f"❌ Unknown engine: {preferred}. Choose 'podman' or 'docker'.")
            sys.exit(1)
        # Move preferred to front
        engines = [preferred] + [e for e in engines if e != preferred]

    for engine in engines:
        try:
            subprocess.run(
                [engine, "--version"],
                capture_output=True,
                check=True,
                timeout=10,
            )
            return engine
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # Platform-specific help
    help_msg = {
        "win32": "Install Podman Desktop: https://podman-desktop.io/\n   Or Docker Desktop: https://docs.docker.com/desktop/install/windows-install/",
        "darwin": "Install via Homebrew: brew install podman\n   Then run: podman machine init && podman machine start\n   Or install Docker Desktop: brew install --cask docker",
        "linux": "Install via package manager:\n   Ubuntu/Debian: sudo apt-get install podman\n   Fedora: sudo dnf install podman",
    }
    platform_help = help_msg.get(sys.platform, "Install Podman or Docker for your OS.")

    print(f"❌ Error: Neither Podman nor Docker is installed.\n\n💡 {platform_help}")
    sys.exit(1)


def build_volume_mount(host_path: Path, container_path: str) -> str:
    """Build a volume mount string with optional SELinux suffix."""
    suffix = get_volume_suffix()
    return f"{posix_volume_path(host_path)}:{container_path}{suffix}"


# =============================================================================
# Builders
# =============================================================================

def build_mcp_inspector(engine: str):
    """Compile mcp-inspector-atom8n via ephemeral container."""
    print("🚀 Building mcp-inspector-atom8n via Ephemeral Container...")
    target_dir = WORKSPACE_ROOT / "external" / "mcp-inspector-atom8n"

    if not target_dir.exists():
        print(f"❌ Source directory not found: {target_dir}")
        print("💡 Did you initialize submodules? Run: git submodule update --init --recursive")
        sys.exit(1)

    volume = build_volume_mount(target_dir, "/app")

    cmd = [
        engine, "run", "--rm",
        "-v", volume,
        "-w", "/app",
        "docker.io/node:22-bookworm",
        "bash", "-c", "npm install --ignore-scripts && npm run build",
    ]

    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("❌ Failed to build mcp-inspector-atom8n.")
        sys.exit(result.returncode)
    print("✅ Successfully built mcp-inspector-atom8n.")


def build_n8n_atom(engine: str, args: argparse.Namespace) -> None:
    """Build n8n-atom using an ephemeral container with tar-based export.

    The key insight: pnpm creates symlinks that break when written to a
    Windows host via Docker/Podman volume mounts. To avoid this, we:
    1. Build everything inside a Linux container (as before).
    2. Create a DEREFERENCED tar archive inside the container.
    3. Keep the archive as a single file on the host to bypass Windows MAX_PATH limits.
    4. Extract the tar directly inside the final Docker image.
    """
    target_dir = WORKSPACE_ROOT / "external" / "n8n-atom"
    build_context_dir = target_dir / "build_context"
    tar_path = target_dir / "compiled.tar"

    # FAST PATH: If build context already exists, skip compilation
    if (build_context_dir / "compiled.tar").exists() and not args.clean:
        print("\n⚡ Existing build context detected! Skipping full compilation...")
        stage_docker_assets(target_dir)
        return

    print("\n🚀 Building n8n-atom via Ephemeral Container...")
    print("⚠️  This step might take several minutes. Please be patient...")
    cache_volume = "vibe-pnpm-store"

    if not target_dir.exists():
        print(f"❌ Source directory not found: {target_dir}")
        print("💡 Did you initialize submodules? Run: git submodule update --init --recursive")
        sys.exit(1)

    # Restore any package.json files modified by a previous build's pre-deploy cleanup.
    # Must run on the HOST because n8n-atom is a git submodule (.git is outside the mount).
    print("🔄 Restoring clean source state (host-side git checkout)...")
    subprocess.run(["git", "checkout", "--", "."], cwd=target_dir, capture_output=True)

    workspace_volume = "vibe-n8n-workspace"
    out_volume = build_volume_mount(target_dir, "/out")

    # Architecture: Git Archive -> Persistent Linux Volume
    # We use git archive on the host (where git correctly parses submodules) 
    # to generated a perfectly clean tar stream of tracked files.
    # We pipe this to the persistent Linux container where the build runs.
    # The final compiled.tar is copied to /out (the Windows mount).
    print("\n--- SYNCING SOURCE TO LINUX FS (Git Archive) ---")
    # Step 1: Clean /build, preserving node_modules and turbo cache
    clean_cmd = [
        engine, "run", "--rm",
        "-v", f"{workspace_volume}:/build",
        "docker.io/node:22-bookworm",
        "sh", "-c",
        "mkdir -p /build && find /build -mindepth 1 -maxdepth 1 ! -name node_modules ! -name .turbo -exec rm -rf {} +"
    ]
    result1 = subprocess.run(clean_cmd)
    if result1.returncode != 0:
        sys.exit(result1.returncode)

    # Step 2: Extract clean git tree into /build
    tar_cmd = f"git -C \"{target_dir.absolute()}\" archive --format=tar HEAD | {engine} run -i --rm -v {workspace_volume}:/build docker.io/node:22-bookworm tar xf - -C /build"
    result2 = subprocess.run(tar_cmd, shell=True)
    if result2.returncode != 0:
        sys.exit(result2.returncode)

    build_script = (
        "set -e && "
        "command -v pnpm >/dev/null || (corepack enable && corepack prepare pnpm@10.22.0 --activate) && "
        "pnpm config set store-dir /pnpm-store && "
        "export npm_config_loglevel=notice && "
        "export NODE_OPTIONS='--max-old-space-size=4096' && "
        "export LEFTHOOK=0 HUSKY=0 CI=true && "
        "cd /build && "
        "echo '--- STARTING INSTALL ---' && "
        "pnpm install --frozen-lockfile && "
        "echo '--- REBUILDING NATIVE MODULES ---' && "
        "pnpm rebuild sqlite3 && "
        "echo '--- STARTING BUILD ---' && "
        "pnpm run build:n8n && "
        "echo '--- CREATING PORTABLE ARCHIVE (Linux FS) ---' && "
        "tar chf /tmp/compiled.tar -C /build/compiled . && "
        "echo '--- COPYING ARCHIVE TO HOST ---' && "
        "rm -f /out/compiled.tar /out/pnpm-lock.yaml && "
        "cp /tmp/compiled.tar /out/compiled.tar && "
        "cp /build/pnpm-lock.yaml /out/pnpm-lock.yaml && "
        "echo '--- ARCHIVE READY ---' && "
        "ls -lh /out/compiled.tar"
    )

    cmd = [
        engine, "run", "--rm",
        "-v", f"{cache_volume}:/pnpm-store",
        "-v", f"{workspace_volume}:/build",
        "-v", out_volume,
        "-w", "/build",
        "docker.io/node:22-bookworm",
        "sh", "-c", build_script,
    ]

    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ Failed to build n8n-atom. Exit Code: {result.returncode}")
        if sys.platform == "win32":
            print("💡 Windows tips: If OOM, increase WSL2 memory in .wslconfig")
        sys.exit(result.returncode)

    # Stage assets for the Docker build context
    stage_docker_assets(target_dir)

    print("\n✅ Build artifacts ready in build_context/")
    print("💡 Next step: podman compose up --build")


def stage_docker_assets(target_dir: Path):
    """Prepare a minimal 'build_context' directory for Docker/Podman."""
    build_context_dir = target_dir / "build_context"
    tar_src = target_dir / "compiled.tar"
    tar_dst = build_context_dir / "compiled.tar"
    entrypoint_src = target_dir / "docker" / "images" / "n8n" / "docker-entrypoint.sh"
    entrypoint_dst = build_context_dir / "docker-entrypoint.sh"

    print("📦 Staging Docker build context...")
    
    # Create clean directory
    if build_context_dir.exists():
        shutil.rmtree(build_context_dir, ignore_errors=True)
    build_context_dir.mkdir(parents=True, exist_ok=True)

    # Copy tar archive
    if tar_src.exists():
        print(f"  🚚 Moving {tar_src.name} to build_context/")
        shutil.move(str(tar_src), str(tar_dst))
    elif not tar_dst.exists():
        print("  ❌ Error: compiled.tar not found! Re-run build with --clean")
        sys.exit(1)

    # Check for lockfile sync
    lockfile = target_dir / "pnpm-lock.yaml"
    if lockfile.exists():
        print(f"  🚚 Lockfile safely synced to host!")

    # Copy entrypoint
    if entrypoint_src.exists():
        print(f"  📄 Copying {entrypoint_src.name}")
        shutil.copy2(entrypoint_src, entrypoint_dst)

    # Create minimal .dockerignore
    (build_context_dir / ".dockerignore").write_text("*.log\n.env\n")


def clean_build_artifacts(engine: str, args: argparse.Namespace):
    """Remove compiled output and node_modules to force a clean rebuild.

    Scope is determined by the build target flags:
      --n8n --clean   → clean n8n only
      --mcp --clean   → clean mcp only
      --all --clean   → clean both
      --clean (bare)  → clean both
    """
    print("🧹 Cleaning build artifacts...")

    clean_n8n = args.all or args.n8n or (not args.n8n and not args.mcp)
    clean_mcp = args.all or args.mcp or (not args.n8n and not args.mcp)

    dirs_to_clean = []

    if clean_n8n:
        dirs_to_clean.extend([
            WORKSPACE_ROOT / "external" / "n8n-atom" / "build_context",
            WORKSPACE_ROOT / "external" / "n8n-atom" / "node_modules",
        ])

    if clean_mcp:
        dirs_to_clean.extend([
            WORKSPACE_ROOT / "external" / "mcp-inspector-atom8n" / "node_modules",
            WORKSPACE_ROOT / "external" / "mcp-inspector-atom8n" / "client" / "dist",
            WORKSPACE_ROOT / "external" / "mcp-inspector-atom8n" / "server" / "build",
            WORKSPACE_ROOT / "external" / "mcp-inspector-atom8n" / "cli" / "build",
        ])

    for d in dirs_to_clean:
        if d.exists():
            print(f"  🗑️  Removing {d.relative_to(WORKSPACE_ROOT)}...")
            shutil.rmtree(d, ignore_errors=True)

    if clean_n8n:
        # Clean up tar archive if present
        tar_file = WORKSPACE_ROOT / "external" / "n8n-atom" / "compiled.tar"
        if tar_file.exists():
            print(f"  🗑️  Removing {tar_file.relative_to(WORKSPACE_ROOT)}...")
            tar_file.unlink()
        # Clean pnpm cache and workspace volumes
        for vol in ["vibe-pnpm-store", "vibe-n8n-workspace"]:
            print(f"  🗑️  Removing volume {vol}...")
            subprocess.run([engine, "volume", "rm", "-f", vol], capture_output=True)

    print("✅ Clean complete. Ready for a fresh build.")


# =============================================================================
# Verification
# =============================================================================

def verify_build(n8n_dir: Path, mcp_dir: Path):
    """Check if the build artifacts exist for final deployment."""
    print("\n🔍 Verifying n8n-atom build integrity...")
    n8n_context = n8n_dir / "build_context"

    n8n_checks = [
        (n8n_context, "Build Context Directory"),
        (n8n_context / "compiled.tar", "n8n Portable Archive"),
        (n8n_context / "docker-entrypoint.sh", "Docker Entrypoint"),
    ]

    n8n_passed = True
    for path, label in n8n_checks:
        if path.exists():
            print(f"  ✅ {label}: FOUND")
        else:
            print(f"  ❌ {label}: MISSING")
            n8n_passed = False

    print("\n🔍 Verifying mcp-inspector build integrity...")
    mcp_checks = [
        (mcp_dir / "client" / "dist", "MCP Client (dist)"),
        (mcp_dir / "server" / "build", "MCP Server (build)"),
        (mcp_dir / "cli" / "build", "MCP CLI (build)"),
    ]

    mcp_passed = True
    for path, label in mcp_checks:
        if path.exists():
            print(f"  ✅ {label}: FOUND")
        else:
            print(f"  ❌ {label}: MISSING")
            mcp_passed = False

    if n8n_passed and mcp_passed:
        print("\n✨ All builds are healthy and ready for deployment!")
    else:
        print("\n⚠️ Build is incomplete. Please check the logs above.")
        sys.exit(1)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Multi-OS Builder for n8n-atom & MCP Inspector",
        epilog=(
            "Examples:\n"
            "  python build_n8n_atom.py --all          Build everything\n"
            "  python build_n8n_atom.py --n8n           Build only n8n-atom\n"
            "  python build_n8n_atom.py --mcp           Build only MCP Inspector\n"
            "  python build_n8n_atom.py --check         Verify existing build\n"
            "  python build_n8n_atom.py --clean --all   Clean rebuild\n"
            "  python build_n8n_atom.py --engine docker  Force Docker engine\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--n8n", action="store_true", help="Build only n8n-atom")
    parser.add_argument("--mcp", action="store_true", help="Build only mcp-inspector-atom8n")
    parser.add_argument("--check", action="store_true", help="Verify existing build integrity")
    parser.add_argument("--all", action="store_true", help="Build both (default)")
    parser.add_argument("--clean", action="store_true", help="Wipe compiled output before rebuilding")
    parser.add_argument(
        "--engine",
        choices=["podman", "docker"],
        default=None,
        help="Override container engine auto-detection (default: try podman first)",
    )

    args = parser.parse_args()

    # Default to all if nothing specified
    if not (args.n8n or args.mcp or args.check):
        args.all = True

    engine = detect_engine(args.engine)
    print(f"🔧 Detected container engine: {engine.upper()}")
    print(f"🖥️  Platform: {sys.platform}")

    if args.check:
        verify_build(
            WORKSPACE_ROOT / "external" / "n8n-atom",
            WORKSPACE_ROOT / "external" / "mcp-inspector-atom8n",
        )
        return

    if args.clean:
        clean_build_artifacts(engine, args)

    if args.all or args.mcp:
        build_mcp_inspector(engine)

    if args.all or args.n8n:
        build_n8n_atom(engine, args)

    # Final check after building
    verify_build(
        WORKSPACE_ROOT / "external" / "n8n-atom",
        WORKSPACE_ROOT / "external" / "mcp-inspector-atom8n",
    )

    print("\n🎉 Compilation process finished!")
    print("▶️  You can now start the dev stack:")
    print(f"   {engine} compose -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d --build")


if __name__ == "__main__":
    main()
