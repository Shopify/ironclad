#!/bin/bash
# Ironclad MCP Server - Status Check

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$PROJECT_DIR/.server.pid"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}📊 Ironclad MCP Server Status${NC}"
echo ""

# Check PID file
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "PID File: $PID_FILE"
    echo "Recorded PID: $PID"
    
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "Status: ${GREEN}RUNNING ✓${NC}"
        
        # Check health endpoint
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo -e "Health Check: ${GREEN}PASSED ✓${NC}"
            curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo ""
        else
            echo -e "Health Check: ${RED}FAILED ✗${NC}"
        fi
    else
        echo -e "Status: ${RED}NOT RUNNING (stale PID file)${NC}"
    fi
else
    echo "PID File: Not found"
    echo -e "Status: ${RED}NOT RUNNING${NC}"
fi

# Check for any orphaned processes
echo ""
echo "All ironclad_mcp processes:"
ps aux | grep "ironclad_mcp.http_server" | grep -v grep || echo "  None found"




