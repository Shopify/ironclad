#!/bin/bash

# Sync Ironclad MCP Documentation to GitHub
# Usage: ./scripts/sync-to-github.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Ironclad MCP Documentation Sync${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Configuration
MCP_DIR="/Users/grantjackman/Documents/Ironclad-mcp"
GITHUB_DIR="/Users/grantjackman/Documents/ironclad-github"

# Check if directories exist
if [ ! -d "$MCP_DIR" ]; then
    echo -e "${RED}❌ MCP directory not found: $MCP_DIR${NC}"
    exit 1
fi

if [ ! -d "$GITHUB_DIR" ]; then
    echo -e "${RED}❌ GitHub directory not found: $GITHUB_DIR${NC}"
    exit 1
fi

# Check if GITHUB_TOKEN is set (optional)
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  GITHUB_TOKEN not set. Push may require manual authentication.${NC}"
    echo ""
fi

echo -e "${GREEN}📦 Syncing documentation files...${NC}"
echo ""

# Copy setup docs
echo "  → Copying setup documentation..."
cp "$MCP_DIR/QUICK_START.md" "$GITHUB_DIR/docs/mcp-setup/" 2>/dev/null || true
cp "$MCP_DIR/GCP_SETUP_GUIDE.md" "$GITHUB_DIR/docs/mcp-setup/" 2>/dev/null || true
cp "$MCP_DIR/DEPLOYMENT_GUIDE.md" "$GITHUB_DIR/docs/mcp-setup/" 2>/dev/null || true

# Copy usage docs
echo "  → Copying usage documentation..."
cp "$MCP_DIR/knowledge_base/AI_ROUTING_GUIDE.md" "$GITHUB_DIR/docs/mcp-usage/" 2>/dev/null || true
cp "$MCP_DIR/knowledge_base/FEATURE_ROADMAP.md" "$GITHUB_DIR/docs/mcp-usage/" 2>/dev/null || true
cp "$MCP_DIR/knowledge_base/SHOPIFY_IRONCLAD_KNOWLEDGE_BASE.md" "$GITHUB_DIR/docs/mcp-usage/" 2>/dev/null || true

# Copy development docs
echo "  → Copying development documentation..."
cp "$MCP_DIR/API_DISCOVERY.md" "$GITHUB_DIR/docs/mcp-development/" 2>/dev/null || true
cp "$MCP_DIR/PHASE_2_TRENDING_ANALYSIS_DESIGN.md" "$GITHUB_DIR/docs/mcp-development/" 2>/dev/null || true
cp "$MCP_DIR/PHASE_1_TESTING_PLAN_UPDATED.md" "$GITHUB_DIR/docs/mcp-development/" 2>/dev/null || true

# Copy feedback docs
echo "  → Copying feedback documentation..."
cp "$MCP_DIR/knowledge_base/FEATURE_REQUESTS.md" "$GITHUB_DIR/docs/mcp-feedback/" 2>/dev/null || true
cp "$MCP_DIR/FEATURE_REQUESTS_QUICK_START.md" "$GITHUB_DIR/docs/mcp-feedback/" 2>/dev/null || true
cp "$MCP_DIR/QUICK_ROADMAP_REFERENCE.md" "$GITHUB_DIR/docs/mcp-feedback/" 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ Files synced successfully!${NC}"
echo ""

# Check for changes
cd "$GITHUB_DIR"

if [ -n "$(git status --porcelain)" ]; then
    echo -e "${BLUE}📝 Changes detected:${NC}"
    git status --short
    echo ""
    
    # Stage all changes
    echo -e "${GREEN}📦 Staging changes...${NC}"
    git add docs/
    
    # Create commit with timestamp
    COMMIT_MSG="Update MCP documentation - $(date +%Y-%m-%d)"
    echo -e "${GREEN}💾 Creating commit...${NC}"
    echo "   Message: $COMMIT_MSG"
    git commit -m "$COMMIT_MSG" -m "Auto-synced from /Users/grantjackman/Documents/Ironclad-mcp"
    echo ""
    
    # Push to GitHub
    echo -e "${GREEN}🚀 Pushing to GitHub...${NC}"
    if git push origin main; then
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✅ Documentation synced to GitHub!${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo "View at: https://github.com/Shopify/ironclad/tree/main/docs"
    else
        echo ""
        echo -e "${RED}========================================${NC}"
        echo -e "${RED}  ❌ Push failed${NC}"
        echo -e "${RED}========================================${NC}"
        echo ""
        echo -e "${YELLOW}You may need to:${NC}"
        echo "1. Set GITHUB_TOKEN environment variable"
        echo "2. Or push manually: cd $GITHUB_DIR && git push origin main"
        exit 1
    fi
else
    echo -e "${BLUE}ℹ️  No changes to sync${NC}"
    echo ""
    echo "Documentation is already up to date!"
fi

echo ""
echo -e "${GREEN}Done!${NC}"
