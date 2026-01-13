# Ironclad

This repository serves two purposes:

1. **🤖 Ironclad MCP Documentation** - Query Ironclad contracts through Claude Desktop
2. **📋 Ironclad Workflow Requests** - Request new workflows or changes to existing ones

---

## 🤖 Ironclad MCP (Model Context Protocol)

### What is it?

The Ironclad MCP enables Shopify employees to query Ironclad contract data directly through Claude Desktop in Cursor, without leaving their development environment.

**Quick examples:**
- "Find contracts with Zoom"
- "Show me details for IC-95582"
- "What contracts are in approval?"
- "How many Plus Agreements total?"

### 🚀 Quick Setup (5 Minutes)

1. **Add to your `~/.cursor/mcp.json`:**
   ```json
   {
     "mcpServers": {
       "ironclad-mcp": {
         "type": "streamable-http",
         "url": "http://YOUR_SERVER_URL:8000/sse",
         "headers": {
           "X-User-Email": "your.email@shopify.com"
         }
       }
     }
   }
   ```
   
2. **Get server URL** from `#ironclad-for-plus` or your admin
3. **Restart Cursor** (Cmd+Q and reopen)
4. **Ask Claude**: "Find contracts with Zoom"

**✅ Done!**

### 📚 Full Documentation

**👉 [Complete MCP Documentation](docs/README.md)**

**Quick links:**
- **Setup**: [Quick Start Guide](docs/mcp-setup/QUICK_START.md)
- **Usage**: [Feature Roadmap](docs/mcp-usage/FEATURE_ROADMAP.md) | [AI Routing Guide](docs/mcp-usage/AI_ROUTING_GUIDE.md)
- **Development**: [API Discovery](docs/mcp-development/API_DISCOVERY.md) | [Testing Plan](docs/mcp-development/PHASE_1_TESTING_PLAN_UPDATED.md)
- **Feedback**: [Feature Requests](docs/mcp-feedback/FEATURE_REQUESTS.md) | [Roadmap](docs/mcp-feedback/QUICK_ROADMAP_REFERENCE.md)

### Current Status

- ✅ **Phase 1 (LIVE)**: Contract search, workflow tracking, counts
- 🔮 **Phase 2 (Q2 2026)**: Clause extraction, AI reading
- 💡 **Phase 3 (Q3-Q4 2026)**: Contract comparison, bulk operations

---

## 📋 Ironclad Workflow Requests

### Overview

This repository is also dedicated to managing requests related to Ironclad development work. It serves as a centralized place for team members to propose new workflows, request changes to existing workflows, or deprecate workflows that are no longer in use.

### How to Use

To request a new workflow, propose changes, or ask for deprecation:

#### 1. Open a New Issue

- Click on the **[Issues](https://github.com/Shopify/ironclad/issues)** tab
- Select **"New Issue"**
- Choose the appropriate template (if available) and fill in the requested details

#### 2. Provide Details

- **For new workflows**: Clearly describe the business need, stakeholders, and desired outcome
- **For changes**: Reference the existing workflow and describe the changes required
- **For deprecation**: Identify the workflow and the rationale for deprecation

#### 3. Track Progress

- Your request will be reviewed by the Ironclad development team
- Discussion and status updates will occur directly within the issue

### Contributing

If you'd like to contribute directly (e.g., suggest improvements to this process), please open a pull request or discuss your ideas in an issue.

---

## 🆘 Support

### For MCP Issues
- **Plus Agreement matters**: `#ironclad-for-plus`
- **All other contract matters**: `#ironclad_support_non-plus`

### For Workflow Requests
- **Plus matters ONLY**: `#ironclad-for-plus`
- **All other workflow matters**: `#ironclad_support_non-plus`

---

## 🔗 Quick Links

| Purpose | Link |
|---------|------|
| **MCP Documentation** | [docs/README.md](docs/README.md) |
| **MCP Quick Start** | [docs/mcp-setup/QUICK_START.md](docs/mcp-setup/QUICK_START.md) |
| **Feature Requests** | [docs/mcp-feedback/FEATURE_REQUESTS.md](docs/mcp-feedback/FEATURE_REQUESTS.md) |
| **Workflow Issues** | [Issues](https://github.com/Shopify/ironclad/issues) |
| **Workflow Request Template** | [request-for-ironclad-development-work.md](request-for-ironclad-development-work.md) |

---

**Built for Shopify** 🚀
