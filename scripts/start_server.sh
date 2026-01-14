#!/bin/bash
# Ironclad MCP Server - Start Script with Automatic Cleanup
# This script ensures only one server instance runs at a time

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$PROJECT_DIR/.server.pid"
LOG_FILE="${LOG_FILE:-/tmp/ironclad-mcp.log}"

echo -e "${YELLOW}🔧 Ironclad MCP Server Startup${NC}"
echo "Project: $PROJECT_DIR"
echo "Log: $LOG_FILE"
echo ""

# Step 1: Kill any existing server processes
echo -e "${YELLOW}Step 1: Checking for existing server processes...${NC}"
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "  Found server with PID $OLD_PID (from PID file)"
        kill -9 "$OLD_PID" 2>/dev/null || true
        echo -e "  ${GREEN}✓${NC} Killed old server"
    fi
    rm -f "$PID_FILE"
fi

# Kill any other ironclad_mcp.http_server processes
ORPHANED_PIDS=$(ps aux | grep "ironclad_mcp.http_server" | grep -v grep | awk '{print $2}')
if [ -n "$ORPHANED_PIDS" ]; then
    echo "  Found orphaned server processes: $ORPHANED_PIDS"
    echo "$ORPHANED_PIDS" | xargs kill -9 2>/dev/null || true
    echo -e "  ${GREEN}✓${NC} Killed orphaned servers"
else
    echo -e "  ${GREEN}✓${NC} No old processes found"
fi

# Step 2: Clear Python bytecode cache
echo -e "\n${YELLOW}Step 2: Clearing Python bytecode cache...${NC}"
cd "$PROJECT_DIR"
find ./src -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find ./src -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "  ${GREEN}✓${NC} Cache cleared"

# Step 3: Validate environment
echo -e "\n${YELLOW}Step 3: Validating environment...${NC}"
if [ ! -f "$PROJECT_DIR/service-account-key.json" ]; then
    echo -e "${RED}❌ Error: service-account-key.json not found${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Service account key exists"

# Step 4: Set environment variables
echo -e "\n${YELLOW}Step 4: Setting environment variables...${NC}"
export GCP_PROJECT_ID="shopify-contract-filing-automa"
export GOOGLE_APPLICATION_CREDENTIALS="$PROJECT_DIR/service-account-key.json"
export IRONCLAD_BASE_URL="https://na1.ironcladapp.com"
export IRONCLAD_API_TIMEOUT="120"
export PYTHONPATH="$PROJECT_DIR/src"
echo -e "  ${GREEN}✓${NC} Environment configured"

# Step 5: Start the server
echo -e "\n${YELLOW}Step 5: Starting server...${NC}"
rm -f "$LOG_FILE"

cd "$PROJECT_DIR"
python3 -u -m ironclad_mcp.http_server >> "$LOG_FILE" 2>&1 &
NEW_PID=$!

# Save PID
echo "$NEW_PID" > "$PID_FILE"

# Wait a moment for startup
sleep 3

# Check if server is running
if ps -p "$NEW_PID" > /dev/null 2>&1; then
    # Test health endpoint
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Server started successfully!${NC}"
        echo "   PID: $NEW_PID"
        echo "   Health: http://localhost:8000/health"
        echo "   Logs: tail -f $LOG_FILE"
        echo ""
        echo -e "${GREEN}To stop: ./scripts/stop_server.sh${NC}"
        exit 0
    else
        echo -e "${RED}❌ Server started but health check failed${NC}"
        echo "Check logs: tail -f $LOG_FILE"
        exit 1
    fi
else
    echo -e "${RED}❌ Server failed to start${NC}"
    echo "Check logs: tail -f $LOG_FILE"
    exit 1
fi




