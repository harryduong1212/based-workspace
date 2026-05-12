#!/usr/bin/env bash
# Start the Control Panel backend (FastAPI :8765) and frontend (Next.js :3000)
# in parallel with prefixed, line-buffered output. Ctrl-C kills both.
#
# Usage: ./scripts/dev.sh [--no-frontend | --no-backend]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WEB_DIR="$SCRIPT_DIR/services/control_panel/web"

START_BACKEND=1
START_FRONTEND=1
for arg in "$@"; do
  case "$arg" in
    --no-frontend) START_FRONTEND=0 ;;
    --no-backend)  START_BACKEND=0 ;;
    -h|--help)
      sed -n '2,8p' "$0"
      exit 0
      ;;
    *) echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done

if [[ $START_FRONTEND -eq 1 && ! -d "$WEB_DIR/node_modules" ]]; then
  echo "frontend deps missing; run './scripts/bootstrap.sh' first." >&2
  exit 1
fi

# Track child PIDs so the trap can take them all down even if one crashed.
PIDS=()

cleanup() {
  trap - INT TERM EXIT
  for pid in "${PIDS[@]:-}"; do
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      # SIGTERM the whole process group so npm/uvicorn children die too.
      kill -TERM "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
    fi
  done
  # Brief grace, then force.
  sleep 0.5
  for pid in "${PIDS[@]:-}"; do
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      kill -KILL "-$pid" 2>/dev/null || kill -KILL "$pid" 2>/dev/null || true
    fi
  done
}
trap cleanup INT TERM EXIT

# Prefix each line of a stream with a tagged, coloured label. Keeps both
# servers' logs interleaved but distinguishable.
prefix() {
  local tag="$1"
  local color="$2"
  local reset="\033[0m"
  awk -v t="$tag" -v c="$color" -v r="$reset" '{ printf "%s[%s]%s %s\n", c, t, r, $0; fflush(); }'
}

if [[ $START_BACKEND -eq 1 ]]; then
  # `setsid` puts uvicorn in its own process group so the trap can signal it
  # as a group (catches uvicorn's reload workers, asyncio threads, etc.).
  setsid "$SCRIPT_DIR/scripts/with-env.sh" python3 -m services.control_panel \
    2>&1 | prefix "backend " "\033[36m" &
  PIDS+=("$!")
fi

if [[ $START_FRONTEND -eq 1 ]]; then
  (
    cd "$WEB_DIR"
    setsid npm run dev 2>&1 | prefix "frontend" "\033[35m"
  ) &
  PIDS+=("$!")
fi

if [[ ${#PIDS[@]} -eq 0 ]]; then
  echo "nothing to start (both --no-* flags set)" >&2
  exit 2
fi

echo ""
echo "  backend:  http://127.0.0.1:8765"
echo "  frontend: http://127.0.0.1:3000"
echo "  Ctrl-C to stop both."
echo ""

# Wait for any child to exit. If one dies, fall through and the trap takes
# the other one down. `wait -n` returns when the first child finishes.
wait -n || true
