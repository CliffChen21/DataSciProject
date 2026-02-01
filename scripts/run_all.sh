#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export PYTHONPATH="$ROOT_DIR"

# Start backend
nohup /home/codespace/.python/current/bin/python -m backend.app > "$ROOT_DIR/output/backend.log" 2>&1 &
BACKEND_PID=$!

echo "Backend started (PID: $BACKEND_PID). Logs: $ROOT_DIR/output/backend.log"

# Start frontend
cd "$ROOT_DIR/frontend"
if [ ! -d "node_modules" ]; then
  npm install
fi
npm run dev
