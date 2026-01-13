# Feature Request System - Quick Start
## Everything You Need to Know in 5 Minutes

**Last Updated**: January 13, 2026

---

## ✅ YES, This Is Fully Implemented!

You asked:
> "Is it possible to have such a doc? When the mcp detects from a user based on their question that the mcp is not capable of completing the task - it asks the user if they would like to make it a feature request, the mcp then logs it in the central doc."

**Answer**: ✅ **Yes! It's ready to use.**

---

## 🎯 How It Works (User Perspective)

```
User: "Find contracts with auto-renewal clauses"

MCP: "❌ Clause extraction isn't available yet.
     Would you like to log a feature request?"

User: "Yes"

MCP: "Why do you need this feature?"

User: "Monthly compliance audits"

MCP: "✅ Feature request FR-20260115-003 logged!
     You'll be notified when it's built."
```

**That's it!** The request is automatically saved to `FEATURE_REQUESTS.md`.

---

## 📄 Key Files

| File | What It Does |
|------|--------------|
| **knowledge_base/FEATURE_REQUESTS.md** | Central log of all requests |
| **knowledge_base/AI_ROUTING_GUIDE.md** | Instructions for MCP on how to collect requests |
| **GITHUB_DEPLOYMENT_GUIDE.md** | How to deploy docs to GitHub |
| **FEATURE_REQUEST_SYSTEM_COMPLETE.md** | Full implementation details |

---

## 🚀 Deployment (3 Steps)

### Step 1: Deploy to GitHub (5 minutes)

```bash
# Create repo
gh repo create your-org/ironclad-mcp-docs --private

# Clone and setup
git clone git@github.com:your-org/ironclad-mcp-docs.git
cd ironclad-mcp-docs
mkdir -p docs/feedback

# Copy docs
cp /Users/grantjackman/Documents/Ironclad-mcp/knowledge_base/FEATURE_REQUESTS.md docs/feedback/

# Commit
git add .
git commit -m "Add feature request tracking"
git push
```

### Step 2: Restart MCP Server (1 minute)

```bash
# Quit Cursor completely
# Restart Cursor
# Wait for MCP to load (~10 seconds)
```

### Step 3: Test It (2 minutes)

Ask Claude:
```
"Find all contracts with indemnity clauses"
```

Expected response:
- ✅ Explains clause extraction is Phase 2
- ✅ Offers to log feature request
- ✅ Collects details if you say yes
- ✅ Saves to FEATURE_REQUESTS.md

---

## 📋 What Gets Logged

```markdown
#### FR-20260115-001: Title
**Status**: 📥 New
**Category**: 📄 Document Operations
**Date**: 2026-01-15
**User**: your.email@shopify.com
**Votes**: 1

**Original Query**: "Find indemnity clauses"
**Use Case**: Monthly compliance audits
**Frequency**: Monthly
```

---

## 🔄 Weekly Maintenance (10 minutes)

### Every Monday:

1. **Pull latest**:
   ```bash
   cd /Users/grantjackman/Documents/Ironclad-mcp
   ```

2. **Check new requests**:
   ```bash
   grep "Status.*📥 New" knowledge_base/FEATURE_REQUESTS.md
   ```

3. **Review and update**:
   - Deduplicate similar requests
   - Update statuses (Planning/In Progress/Completed)
   - Add to roadmap if prioritized

4. **Sync to GitHub**:
   ```bash
   cd /path/to/github/repo
   cp /Users/grantjackman/Documents/Ironclad-mcp/knowledge_base/FEATURE_REQUESTS.md docs/feedback/
   git add docs/feedback/
   git commit -m "Update feature requests - $(date +%Y-%m-%d)"
   git push
   ```

**Done!** Takes ~10 minutes per week.

---

## 💡 Key Features

### Auto-Detect Duplicates
```
User: "Find indemnity clauses"
MCP: "I found FR-20260110-001 (12 votes) for clause extraction.
     Would you like to add your vote?"
```

### Auto-Categorize
- 🔍 Search & Filtering
- 📊 Analytics & Reporting
- 📄 Document Operations
- ⚙️ Workflow Enhancements
- 🔗 Integration
- 💡 Other

### Track Votes
```
**Votes**: 13 (13 unique users)

**Voters**:
1. user1@shopify.com (2026-01-15)
2. user2@shopify.com (2026-01-16)
...
```

---

## 🔍 Search Requests

### Find New Requests
```bash
grep "Status.*📥 New" knowledge_base/FEATURE_REQUESTS.md
```

### Find Popular Requests (5+ votes)
```bash
grep -E "Votes: ([5-9]|[0-9][0-9])" knowledge_base/FEATURE_REQUESTS.md
```

### Find Requests from User
```bash
grep "grant.jackman@shopify.com" knowledge_base/FEATURE_REQUESTS.md
```

### Find by Category
```bash
grep "### 📄 Document Operations" -A 100 knowledge_base/FEATURE_REQUESTS.md
```

---

## 📊 Metrics to Track

- **Total requests**: `grep -c "^#### FR-" FEATURE_REQUESTS.md`
- **New requests**: `grep -c "Status.*📥 New" FEATURE_REQUESTS.md`
- **Top requests**: Sort by vote count
- **By category**: Count per category
- **By user**: Most active requesters

---

## ✅ When to Use

### ✅ Offer Feature Request:
- User asks for something not available
- Not in Phase 2/3 roadmap
- Reasonable and useful feature
- User seems genuinely interested

### ❌ Don't Offer:
- Already in Phase 2/3 roadmap (just mention it's coming)
- Fundamentally impossible
- Out of scope (e.g., personal CRM integration)
- Security/compliance violation (e.g., edit contracts via MCP)

---

## 🎯 Examples

### Example 1: New Request

**User**: "Compare two contracts"

**MCP**: 
> "❌ Not available (Phase 3 consideration).
> Would you like to log a feature request?"

**User**: "Yes"

**MCP**: 
> "Why do you need this?"

**User**: "Renegotiation prep, monthly"

**MCP**:
> "✅ FR-20260115-007 logged!"

---

### Example 2: Existing Request

**User**: "Find liability clauses"

**MCP**:
> "❌ Not available yet.
> ✅ Found FR-20260110-001 (12 votes).
> Add your vote?"

**User**: "Yes"

**MCP**:
> "✅ Vote added! Now 13 votes."

---

### Example 3: Already in Roadmap

**User**: "Search PDFs"

**MCP**:
> "❌ Not available yet.
> ✅ Already planned for Phase 2 (Q2 2026)!
> Would you like to search metadata instead?"

[No feature request offered - already planned]

---

## 🚀 Quick Commands

```bash
# View all requests
cat knowledge_base/FEATURE_REQUESTS.md

# Find new requests
grep "Status.*📥 New" knowledge_base/FEATURE_REQUESTS.md

# Find popular requests
grep -E "Votes: ([5-9]|[0-9][0-9])" knowledge_base/FEATURE_REQUESTS.md

# Sync to GitHub
cp knowledge_base/FEATURE_REQUESTS.md /path/to/github/repo/docs/feedback/
cd /path/to/github/repo && git add . && git commit -m "Update requests" && git push
```

---

## 📚 Full Documentation

- **FEATURE_REQUESTS.md** - Central request log
- **AI_ROUTING_GUIDE.md** - Collection workflow (8 steps)
- **FEATURE_ROADMAP.md** - Official roadmap
- **GITHUB_DEPLOYMENT_GUIDE.md** - Deployment instructions
- **FEATURE_REQUEST_SYSTEM_COMPLETE.md** - Full implementation details

---

## ✅ Status

- ✅ **Fully implemented** - Ready to use
- ✅ **No code changes needed** - AI follows instructions
- ✅ **Auto-deduplication** - Prevents duplicate requests
- ✅ **Vote tracking** - Shows demand
- ✅ **GitHub ready** - Easy deployment

---

## 🎉 Bottom Line

**Your MCP now automatically collects user feedback!**

1. ✅ User asks for unavailable feature
2. ✅ MCP offers to log request
3. ✅ MCP collects details
4. ✅ MCP saves to FEATURE_REQUESTS.md
5. ✅ You review weekly
6. ✅ Sync to GitHub

**No additional development required!** 🚀
