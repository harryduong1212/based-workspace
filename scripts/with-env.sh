#!/usr/bin/env bash
# Source the project-root .env, then exec the given command.
# Used as the `command` in .mcp.json so the JSON stays secret-free —
# the MCP server inherits POSTGRES_PASSWORD etc. via os.environ.
#
# Usage: ./scripts/with-env.sh <command> [args...]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

exec "$@"
