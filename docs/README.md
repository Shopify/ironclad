# Ironclad MCP Documentation
## Query Ironclad Contracts Through Claude Desktop

**Last Updated**: January 13, 2026

---

## 🎯 What is the Ironclad MCP?

The **Ironclad Model Context Protocol (MCP)** enables Shopify employees to query Ironclad contract data directly through Claude Desktop in Cursor, without leaving their development environment.

**What you can do:**
- ✅ Search contracts by counterparty, type, or keywords
- ✅ Get contract details and view attachments
- ✅ Search and track active workflows
- ✅ Count contracts and analyze data
- ✅ Automatically detect contract families and amendments

**What you can't do (yet):**
- ❌ Edit or create contracts (security/compliance - use Ironclad UI)
- ❌ Date-filtered trending analysis (API limitations - use Ironclad UI)
- ❌ Search within PDF clauses (planned for Phase 2)

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Add MCP Configuration

Open your Cursor MCP config file:
```
~/.cursor/mcp.json
```

Add this configuration:
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

**Replace:**
- `YOUR_SERVER_URL` - Get this from #ironclad-for-plus or your admin
- `your.email@shopify.com` - Use your actual Shopify email

### Step 2: Restart Cursor

Quit Cursor completely (Cmd+Q) and restart.

### Step 3: Start Querying!

Open Claude in Cursor and try:
```
"Find contracts with Zoom"
```

**That's it!** ✅

For detailed setup instructions, see [mcp-setup/QUICK_START.md](mcp-setup/QUICK_START.md)

---

## 📚 Documentation

### For End Users

| Document | Description |
|----------|-------------|
| **[Quick Start](mcp-setup/QUICK_START.md)** | 10-minute setup guide |
| **[Feature Roadmap](mcp-usage/FEATURE_ROADMAP.md)** | What's available and what's coming |
| **[AI Routing Guide](mcp-usage/AI_ROUTING_GUIDE.md)** | How the MCP works internally |
| **[Knowledge Base](mcp-usage/SHOPIFY_IRONCLAD_KNOWLEDGE_BASE.md)** | Ironclad-specific info |

### For Administrators

| Document | Description |
|----------|-------------|
| **[GCP Setup Guide](mcp-setup/GCP_SETUP_GUIDE.md)** | Configure GCP Secret Manager |
| **[Deployment Guide](mcp-setup/DEPLOYMENT_GUIDE.md)** | Production deployment |

### For Developers

| Document | Description |
|----------|-------------|
| **[API Discovery](mcp-development/API_DISCOVERY.md)** | Ironclad API documentation |
| **[Testing Plan](mcp-development/PHASE_1_TESTING_PLAN_UPDATED.md)** | Test scenarios and results |
| **[Phase 2 Design](mcp-development/PHASE_2_TRENDING_ANALYSIS_DESIGN.md)** | Future feature design |

### Feature Requests & Feedback

| Document | Description |
|----------|-------------|
| **[Feature Requests](mcp-feedback/FEATURE_REQUESTS.md)** | User-submitted enhancement ideas |
| **[Quick Roadmap](mcp-feedback/QUICK_ROADMAP_REFERENCE.md)** | One-page roadmap overview |
| **[Request Quick Start](mcp-feedback/FEATURE_REQUESTS_QUICK_START.md)** | How feature requests work |

---

## 💡 Example Queries

### Search Contracts
```
"Find contracts with Zoom"
"Show me Plus Agreements"
"Search for contracts mentioning 'GDPR'"
```

### Get Contract Details
```
"Show me details for IC-95582"
"Get contract IC-5701 with attachments"
"What's the status of IC-124986?"
```

### Workflow Management
```
"What contracts are in workflow?"
"Active workflows for Plus Agreements"
"Show me contracts in approval"
"Get workflow details for IC-60730"
```

### Counts & Totals
```
"How many Plus Agreements total?"
"Count Zoom contracts"
"How many workflows are active?"
```

---

## 📊 Current Status

### ✅ Phase 1 - LIVE (January 2026)

**Available Now:**
- Contract search (counterparty, type, keywords)
- Contract details and attachments
- Workflow search and tracking
- Contract families and amendments
- Counts and totals (no date filtering)

**Known Limitations:**
- ❌ No date filtering (API limitation)
- ❌ No trending/analytics (use Ironclad UI)
- ❌ No contract editing (security - use Ironclad UI)
- ❌ No clause extraction (planned Phase 2)

### 🔮 Phase 2 - PLANNED (Q2 2026)

**Coming Soon:**
- Clause extraction (search within PDFs)
- AI-powered contract Q&A
- Obligation and risk identification
- Trademark and indemnity searches

### 💡 Phase 3 - FUTURE (Q3-Q4 2026)

**Being Considered:**
- Contract comparison (side-by-side)
- Bulk operations
- Advanced search features

See [Feature Roadmap](mcp-usage/FEATURE_ROADMAP.md) for details.

---

## 💬 Feature Requests

### How It Works

When you ask for something the MCP can't do, it will:
1. ✅ Explain what's not available and why
2. ✅ Suggest current alternatives
3. ✅ Ask if you'd like to log a feature request
4. ✅ Collect details and save to [FEATURE_REQUESTS.md](mcp-feedback/FEATURE_REQUESTS.md)

**Example:**
```
You: "Find contracts with indemnity clauses"

MCP: "Clause extraction isn't available yet (planned Phase 2).
     Would you like to log a feature request?"

You: "Yes"

MCP: [Collects details and logs request]
     "✅ Feature request FR-20260115-003 logged!"
```

Your feedback helps prioritize development!

See [Feature Request Quick Start](mcp-feedback/FEATURE_REQUESTS_QUICK_START.md) for details.

---

## 🆘 Support

### For MCP Issues

- **Plus Agreement matters**: `#ironclad-for-plus`
- **All other matters**: `#ironclad_support_non-plus`

### For Ironclad Workflow Requests

This repo is also used for Ironclad workflow development requests.

To request a new workflow or changes:
1. Go to [Issues](https://github.com/Shopify/ironclad/issues)
2. Click "New Issue"
3. Choose the appropriate template
4. Fill in the details

See [main README](../README.md) for workflow request process.

---

## 🔐 Security & Privacy

### User Attribution
All MCP queries are logged under your Ironclad account (via `X-User-Email` header) for audit trails.

### Credentials
- OAuth credentials stored in GCP Secret Manager
- No credentials exposed to end users
- Service accounts with minimal required permissions

### Data Access
- Read-only access to contracts
- No editing or creation capabilities
- Respects Ironclad permissions

---

## 🔗 Quick Links

### Setup
- [Quick Start Guide](mcp-setup/QUICK_START.md)
- [GCP Setup](mcp-setup/GCP_SETUP_GUIDE.md)
- [Deployment Guide](mcp-setup/DEPLOYMENT_GUIDE.md)

### Usage
- [Feature Roadmap](mcp-usage/FEATURE_ROADMAP.md)
- [AI Routing Guide](mcp-usage/AI_ROUTING_GUIDE.md)
- [Knowledge Base](mcp-usage/SHOPIFY_IRONCLAD_KNOWLEDGE_BASE.md)

### Development
- [API Discovery](mcp-development/API_DISCOVERY.md)
- [Testing Plan](mcp-development/PHASE_1_TESTING_PLAN_UPDATED.md)

### Feedback
- [Feature Requests](mcp-feedback/FEATURE_REQUESTS.md)
- [Quick Roadmap](mcp-feedback/QUICK_ROADMAP_REFERENCE.md)

---

## 📖 External Resources

- **Model Context Protocol**: https://modelcontextprotocol.io
- **Ironclad API**: https://developer.ironcladapp.com
- **GCP Secret Manager**: https://cloud.google.com/secret-manager

---

## 🎯 TL;DR

1. **Add config to `~/.cursor/mcp.json`** (get server URL from admin)
2. **Restart Cursor**
3. **Ask Claude**: "Find contracts with Zoom"
4. **Done!** ✅

For detailed setup: [Quick Start Guide](mcp-setup/QUICK_START.md)

---

**Built for Shopify by the Ironclad team** 🚀
