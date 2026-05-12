#!/usr/bin/env bash
# Run the MCP Inspector Atom on the host (NOT in a container) so it can read
# host config files like ~/.cursor/mcp.json and ~/.gemini/antigravity/mcp_config.json.
# Per the upstream readme: https://github.com/khanh-atom/mcp-inspector-atom8n
#
#   ./scripts/mcp-inspector.sh start    # idempotent — leaves a PID file for stop
#   ./scripts/mcp-inspector.sh stop
#   ./scripts/mcp-inspector.sh status
#   ./scripts/mcp-inspector.sh logs     # follow logs

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="${XDG_RUNTIME_DIR:-/tmp}/based-workspace-mcp-inspector"
mkdir -p "$RUN_DIR"
PID_FILE="$RUN_DIR/pid"
LOG_FILE="$RUN_DIR/log"

is_running() {
  [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

cmd_start() {
  if is_running; then
    echo "already running (pid $(cat "$PID_FILE"))"
    echo "  ui: http://localhost:6274"
    return 0
  fi
  if ss -ltn 2>/dev/null | grep -qE ':(6274|6277)\b'; then
    echo "port 6274 or 6277 occupied by another process — investigate before starting" >&2
    return 1
  fi
  cd "$REPO_ROOT"
  # setsid detaches into a new session so SIGHUP from the parent shell can't kill it.
  setsid nohup ./scripts/with-env.sh npm exec -y @atom8n/inspector@latest >"$LOG_FILE" 2>&1 < /dev/null &
  echo $! >"$PID_FILE"
  disown 2>/dev/null || true
  sleep 6
  if is_running; then
    echo "started (pid $(cat "$PID_FILE"))"
    echo "  ui:  http://localhost:6274"
    echo "  log: $LOG_FILE"
  else
    echo "failed to start — see $LOG_FILE" >&2
    rm -f "$PID_FILE"
    return 1
  fi
}

cmd_stop() {
  if ! is_running; then
    echo "not running"
    rm -f "$PID_FILE"
    return 0
  fi
  PID="$(cat "$PID_FILE")"
  # The npm wrapper spawns several node children; kill the whole process group.
  pkill -P "$PID" 2>/dev/null || true
  kill "$PID" 2>/dev/null || true
  # Also nuke any lingering inspector children (npm exec orphans them on SIGTERM)
  pkill -f '@atom8n/inspector' 2>/dev/null || true
  rm -f "$PID_FILE"
  echo "stopped"
}

cmd_status() {
  if is_running; then
    echo "running (pid $(cat "$PID_FILE"))"
    echo "  ui: http://localhost:6274"
  else
    echo "not running"
  fi
}

cmd_logs() { tail -F "$LOG_FILE"; }

case "${1:-}" in
  start)  cmd_start ;;
  stop)   cmd_stop ;;
  status) cmd_status ;;
  logs)   cmd_logs ;;
  restart) cmd_stop; cmd_start ;;
  *) echo "usage: $0 {start|stop|status|logs|restart}" >&2; exit 2 ;;
esac
