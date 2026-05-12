#!/usr/bin/env bash
# Install the project's git hooks into .git/hooks/.
# Pre-commit hook runs gitleaks against the staged diff (fast).
# Idempotent — safe to re-run.
#
# Usage: ./scripts/install-git-hooks.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOK="$REPO_ROOT/.git/hooks/pre-commit"

# 1. Install gitleaks to ~/.local/bin if missing.
if ! command -v gitleaks >/dev/null 2>&1; then
  echo "gitleaks not found — installing to ~/.local/bin..."
  mkdir -p "$HOME/.local/bin"
  VERSION="8.30.0"
  ARCH="$(uname -m)"
  case "$ARCH" in
    x86_64) ARCH="x64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *) echo "unsupported arch: $ARCH" >&2; exit 1 ;;
  esac
  URL="https://github.com/gitleaks/gitleaks/releases/download/v${VERSION}/gitleaks_${VERSION}_linux_${ARCH}.tar.gz"
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  echo "  fetching $URL"
  curl -fsSL "$URL" -o "$TMP/gitleaks.tgz"
  tar -xzf "$TMP/gitleaks.tgz" -C "$TMP" gitleaks
  install -m 0755 "$TMP/gitleaks" "$HOME/.local/bin/gitleaks"
  echo "  installed: $(gitleaks version 2>&1 | head -1)"
fi

# 2. Write the pre-commit hook.
cat >"$HOOK" <<'EOF'
#!/usr/bin/env bash
# Auto-installed by scripts/install-git-hooks.sh — block commits containing secrets.
# Bypass with `git commit --no-verify` (don't, unless you're really sure).
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks protect --staged --redact -v --config "$REPO/.gitleaks.toml" || {
    echo ""
    echo "✗ gitleaks blocked this commit. Review findings above."
    echo "  If a finding is a known false-positive, add an allowlist entry to .gitleaks.toml."
    exit 1
  }
else
  echo "warning: gitleaks not installed — re-run scripts/install-git-hooks.sh"
fi
EOF
chmod +x "$HOOK"

echo "installed: $HOOK"
