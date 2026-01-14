#!/bin/bash
# Ironclad MCP Server - Restart Script

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🔄 Restarting Ironclad MCP Server..."
echo ""

# Stop existing server
"$PROJECT_DIR/scripts/stop_server.sh"

echo ""
sleep 1

# Start fresh server
"$PROJECT_DIR/scripts/start_server.sh"




