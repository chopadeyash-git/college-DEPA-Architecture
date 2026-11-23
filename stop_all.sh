#!/usr/bin/env bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "=========================================================="
echo " STOPPING ALL DEPA SERVICES & NODES"
echo "=========================================================="

# Stop by ports
PORTS=(8095 8081 8082 3000 3001 3002 3003)

for port in "${PORTS[@]}"; do
  PIDS=$(lsof -sTCP:LISTEN -ti :"$port" 2>/dev/null || true)
  if [ -n "$PIDS" ]; then
    for pid in $PIDS; do
      echo "Stopping process $pid listening on Port $port..."
      kill -9 "$pid" 2>/dev/null || true
    done
    echo "Port $port is now released."
  else
    echo "Port $port is already free."
  fi
done

# If .running_pids.json exists, cleanup any remaining
if [ -f "$ROOT_DIR/.running_pids.json" ]; then
  rm -f "$ROOT_DIR/.running_pids.json"
fi

echo ""
echo "All DEPA services have been cleanly stopped."
