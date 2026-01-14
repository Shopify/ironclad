#!/bin/bash
# Ironclad MCP Server - Stop Script

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$PROJECT_DIR/.server.pid"

echo -e "${YELLOW}🛑 Stopping Ironclad MCP Server${NC}"

# Stop server from PID file
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Killing server with PID $PID..."
        kill -9 "$PID" 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Server stopped"
    else
        echo "PID $PID not running"
    fi
    rm -f "$PID_FILE"
else
    echo "No PID file found"
fi

# Kill any orphaned processes
ORPHANED_PIDS=$(ps aux | grep "ironclad_mcp.http_server" | grep -v grep | awk '{print $2}')
if [ -n "$ORPHANED_PIDS" ]; then
    echo "Killing orphaned processes: $ORPHANED_PIDS"
    echo "$ORPHANED_PIDS" | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Orphaned processes killed"
fi

echo -e "${GREEN}✅ All servers stopped${NC}"




