#!/bin/bash

# Quick Local Deployment Script
# Tests the HTTP server before production deployment

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Ironclad MCP - Local Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check prerequisites
echo -e "${GREEN}Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites met${NC}"
echo ""

# Check .env file
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cat > .env << 'EOF'
GCP_PROJECT_ID=shopify-contract-filing-automa
GOOGLE_APPLICATION_CREDENTIALS=/Users/grantjackman/Documents/Ironclad-mcp/service-account-key.json
IRONCLAD_BASE_URL=https://na1.ironcladapp.com
IRONCLAD_API_TIMEOUT=120
EOF
    echo -e "${GREEN}✅ Created .env file${NC}"
else
    echo -e "${GREEN}✅ Found existing .env file${NC}"
fi

echo ""

# Build and start
echo -e "${GREEN}Building Docker image...${NC}"
docker-compose build

echo ""
echo -e "${GREEN}Starting server...${NC}"
docker-compose up -d

echo ""
echo -e "${GREEN}Waiting for server to be healthy...${NC}"
sleep 5

# Health check
MAX_RETRIES=10
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Server is healthy!${NC}"
        break
    fi
    
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
        echo -e "${RED}❌ Server failed to start${NC}"
        echo ""
        echo "Check logs:"
        docker-compose logs ironclad-mcp
        exit 1
    fi
    
    echo "  Waiting... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Server URL: http://localhost:8000/sse"
echo ""
echo "Test it with Cursor:"
echo "1. Update ~/.cursor/mcp.json:"
echo '   {
     "mcpServers": {
       "ironclad-mcp": {
         "type": "streamable-http",
         "url": "http://localhost:8000/sse",
         "headers": {
           "X-User-Email": "your.email@shopify.com"
         }
       }
     }
   }'
echo ""
echo "2. Restart Cursor"
echo "3. Ask Claude: 'Find contracts with Zoom'"
echo ""
echo "Commands:"
echo "  View logs:  docker-compose logs -f"
echo "  Stop:       docker-compose down"
echo "  Restart:    docker-compose restart"
echo ""
