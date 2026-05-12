#!/usr/bin/env bash
# Zero-state bootstrap for based-workspace.
#
# Brings the host from "fresh clone" to "Control Panel ready to run":
#   1. Verifies Python 3.11+ and Node 20+ exist (prints install hint if not).
#   2. Creates ./.venv and installs services/control_panel/requirements.txt.
#   3. Installs the Next.js frontend node_modules (services/control_panel/web).
#   4. Prints the two commands the user runs next (backend + frontend).
#
# Everything else (Podman, Postgres, n8n, MCP servers, recipes, connectors)
# is installed *through* the Features page once the Control Panel is up.
#
# This script is intentionally read-only on the host: it never installs
# system packages, never runs sudo, never modifies anything outside the
# repo's working tree.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# ---- terminal helpers -----------------------------------------------------

if [[ -t 1 ]]; then
    BOLD=$'\033[1m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RED=$'\033[31m'; RESET=$'\033[0m'
else
    BOLD=""; GREEN=""; YELLOW=""; RED=""; RESET=""
fi

say()  { printf '%s==> %s%s\n' "$BOLD"   "$*" "$RESET"; }
ok()   { printf '%s✓%s   %s\n'  "$GREEN" "$RESET" "$*"; }
warn() { printf '%s!%s   %s\n'  "$YELLOW" "$RESET" "$*"; }
fail() { printf '%s✗%s   %s\n'  "$RED"   "$RESET" "$*" >&2; }

# ---- prerequisites --------------------------------------------------------

check_python() {
    say "Checking Python"
    if ! command -v python3 >/dev/null 2>&1; then
        fail "python3 not found on PATH"
        echo "    Fedora:  sudo dnf install -y python3.11 python3.11-venv"
        echo "    Debian:  sudo apt install -y python3.11 python3.11-venv"
        echo "    Arch:    sudo pacman -S --noconfirm python"
        return 1
    fi
    local version
    version="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
    local major minor
    IFS='.' read -r major minor <<< "$version"
    if (( major < 3 )) || (( major == 3 && minor < 11 )); then
        fail "Python $version is too old; need 3.11+"
        return 1
    fi
    ok "Python $version"
}

check_node() {
    say "Checking Node.js (for the Control Panel frontend)"
    if ! command -v node >/dev/null 2>&1; then
        warn "node not found on PATH — backend will still work, but the UI needs it"
        echo "    Fedora:  sudo dnf install -y nodejs npm"
        echo "    Debian:  sudo apt install -y nodejs npm"
        echo "    Arch:    sudo pacman -S --noconfirm nodejs npm"
        return 0  # not fatal — backend alone is useful
    fi
    local version
    version="$(node --version | sed 's/^v//')"
    local major
    major="${version%%.*}"
    if (( major < 20 )); then
        warn "Node $version is older than 20 — Next.js may complain"
    else
        ok "Node $version"
    fi
}

# ---- backend --------------------------------------------------------------

setup_venv() {
    say "Preparing Python virtualenv at .venv/"
    if [[ ! -d .venv ]]; then
        python3 -m venv .venv
        ok "Created .venv/"
    else
        ok ".venv/ already exists"
    fi

    # shellcheck source=/dev/null
    source .venv/bin/activate

    say "Installing Control Panel dependencies"
    pip install --quiet --upgrade pip wheel
    pip install --quiet -r services/control_panel/requirements.txt
    ok "Backend deps installed"
}

# ---- frontend -------------------------------------------------------------

setup_frontend() {
    if ! command -v npm >/dev/null 2>&1; then
        warn "Skipping frontend setup (npm missing)"
        return 0
    fi
    say "Installing Control Panel frontend dependencies"
    if [[ -d services/control_panel/web/node_modules ]]; then
        ok "node_modules already present — skipping (delete to force reinstall)"
    else
        (cd services/control_panel/web && npm install --silent)
        ok "Frontend deps installed"
    fi
}

# ---- .env / .mcp.json bootstrap ------------------------------------------

setup_env_files() {
    say "Bootstrapping config files"
    if [[ ! -f .env && -f .env.example ]]; then
        cp .env.example .env
        ok "Created .env from .env.example (review and fill in values)"
    elif [[ -f .env ]]; then
        ok ".env already exists"
    fi
    if [[ ! -f .mcp.json && -f .mcp.json.example ]]; then
        cp .mcp.json.example .mcp.json
        ok "Created .mcp.json from .mcp.json.example"
    elif [[ -f .mcp.json ]]; then
        ok ".mcp.json already exists"
    fi
}

# ---- main -----------------------------------------------------------------

main() {
    say "based-workspace bootstrap"
    check_python || exit 1
    check_node
    setup_venv
    setup_frontend
    setup_env_files
    cat <<MSG

${BOLD}Bootstrap complete.${RESET}

Open two terminals, then run:

  ${GREEN}# terminal 1 — Control Panel backend (FastAPI on http://localhost:8765)${RESET}
  source .venv/bin/activate
  python -m services.control_panel

  ${GREEN}# terminal 2 — Control Panel frontend (Next.js on http://localhost:3000)${RESET}
  cd services/control_panel/web
  npm run dev

Then open ${BOLD}http://localhost:3000/features${RESET} — the wizard handles Podman,
Postgres, n8n, Qdrant, llama-swap, MCP servers, recipes, and connectors from
there. ${BOLD}This script never installs system packages or runs sudo.${RESET}
MSG
}

main "$@"
