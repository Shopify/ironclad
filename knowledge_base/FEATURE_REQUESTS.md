# Ironclad MCP Feature Requests
## User-Submitted Enhancement Requests

**Last Updated**: January 13, 2026  
**Total Requests**: 0  
**Status**: Active collection

---

## 📋 How Feature Requests Work

When the MCP encounters a query it cannot fulfill, it will:

1. ✅ Explain what's not available and why
2. ✅ Suggest current alternatives
3. ✅ Ask if you'd like to log a feature request
4. ✅ Collect details and append to this document
5. ✅ Check for similar existing requests (to avoid duplicates)

---

## 🎯 Request Categories

Requests are automatically categorized as:

- **🔍 Search & Filtering** - New search capabilities
- **📊 Analytics & Reporting** - Trending, comparisons, exports
- **📄 Document Operations** - PDF reading, clause extraction
- **⚙️ Workflow Enhancements** - Workflow management features
- **🔗 Integration** - Third-party integrations
- **💡 Other** - Miscellaneous enhancements

---

## 📈 Most Requested Features

_(Automatically updated as requests are logged)_

| Rank | Feature | Votes | Category | Status |
|------|---------|-------|----------|--------|
| - | _(No requests yet)_ | - | - | - |

---

## 🗂️ All Feature Requests

### 🔍 Search & Filtering

_(No requests yet in this category)_

---

### 📊 Analytics & Reporting

_(No requests yet in this category)_

---

### 📄 Document Operations

_(No requests yet in this category)_

---

### ⚙️ Workflow Enhancements

_(No requests yet in this category)_

---

### 🔗 Integration

_(No requests yet in this category)_

---

### 💡 Other

_(No requests yet in this category)_

---

## 📝 Request Format

Each request includes:
- **Request ID** - Unique identifier (FR-YYYYMMDD-NNN)
- **Date** - When request was logged
- **User** - Email of requester (from IRONCLAD_USER_EMAIL)
- **Category** - Auto-detected category
- **Description** - What the user was trying to do
- **Original Query** - Exact query user asked
- **Current Alternative** - What they can do instead
- **Status** - Planning / In Progress / Completed / Declined
- **Votes** - Number of users who want this (deduplicated)
- **Related Requests** - Similar requests
- **Notes** - Admin notes on feasibility, timeline, etc.

---

## 🔧 For Admins: Processing Requests

### Weekly Review Process

1. **Review new requests** - Check what was logged this week
2. **Deduplicate** - Merge similar requests and increment vote count
3. **Categorize** - Verify auto-categorization is correct
4. **Assess feasibility** - Can this be built? API limitations?
5. **Update roadmap** - Add to Phase 2/3 if prioritized
6. **Respond to users** - Update status and notes
7. **Commit to GitHub** - Push updated FEATURE_REQUESTS.md

### Status Definitions

- **📥 New** - Just logged, not yet reviewed
- **📋 Planning** - Under consideration for Phase 2/3
- **🔨 In Progress** - Currently being built
- **✅ Completed** - Built and available (move to roadmap)
- **⚠️ On Hold** - Blocked by API/external dependency
- **❌ Declined** - Not feasible or out of scope

---

## 🎯 Request Guidelines

**Good Feature Requests**:
- ✅ Specific and actionable
- ✅ Describes the goal, not just the feature
- ✅ Explains use case or frequency
- ✅ Not already in Phase 2/3 roadmap

**Example Good Request**:
> **Goal**: Quickly identify contracts with auto-renewal clauses
> **Use Case**: Monthly audit to catch contracts that might auto-renew
> **Frequency**: Monthly (critical for compliance)
> **Proposed Feature**: "Find contracts with auto-renewal clauses"

**Not-So-Good Request**:
> "Make search faster"  
> _(Too vague - search is already fast, or is this about a specific type of search?)_

---

## 📊 Voting on Existing Requests

If the MCP detects your request is similar to an existing one, it will:
1. Show you the existing request
2. Ask if this is what you want
3. If yes, increment the vote count
4. Record your email (deduplicated)

**Example**:
> "I found a similar request (FR-20260115-001) asking for clause extraction. This has 5 votes from other users. Would you like to add your vote to this request?"

---

## 🔍 Searching This Document

Admins can search for requests by:
```bash
# Find all requests from a user
grep "grant.jackman@shopify.com" FEATURE_REQUESTS.md

# Find requests by category
grep "### 📊 Analytics" -A 50 FEATURE_REQUESTS.md

# Find high-priority requests (5+ votes)
grep "Votes: [5-9]" FEATURE_REQUESTS.md
grep "Votes: [0-9][0-9]" FEATURE_REQUESTS.md
```

---

## 🚀 GitHub Integration

### Initial Setup

```bash
# In your GitHub repo
mkdir docs/
cp /path/to/Ironclad-mcp/knowledge_base/*.md docs/
cp /path/to/Ironclad-mcp/*.md docs/
git add docs/
git commit -m "Add Ironclad MCP documentation"
git push
```

### Weekly Update Workflow

```bash
# After reviewing requests
cd /path/to/github/repo
cp /path/to/Ironclad-mcp/knowledge_base/FEATURE_REQUESTS.md docs/
git add docs/FEATURE_REQUESTS.md
git commit -m "Update feature requests - Week of $(date +%Y-%m-%d)"
git push
```

### Automate (Optional)

Add to `.github/workflows/update-requests.yml`:
```yaml
name: Update Feature Requests
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Copy from MCP server
        run: |
          # Add logic to pull from MCP server
          cp /path/to/FEATURE_REQUESTS.md docs/
      - name: Commit and push
        run: |
          git config user.name "Feature Request Bot"
          git config user.email "bot@example.com"
          git add docs/FEATURE_REQUESTS.md
          git commit -m "Automated feature request update" || exit 0
          git push
```

---

## 📧 Notification Options

### Email Digest (Weekly)

You can set up a weekly email digest of new requests:

```bash
# Add to crontab
0 9 * * 1 /path/to/scripts/email_feature_requests.sh
```

Script sends email with:
- New requests this week
- Top requested features
- Requests needing review

---

## 🎯 Success Metrics

Track:
- **Request volume** - How many per week?
- **Category distribution** - What do users want most?
- **Implementation rate** - % of requests that get built
- **Time to resolution** - Days from request to implementation
- **User engagement** - Are users logging requests?

---

## 📝 Example Request Entry

```markdown
#### FR-20260115-001: Clause Extraction for Indemnity Clauses
**Status**: 📋 Planning (Phase 2)  
**Category**: 📄 Document Operations  
**Date**: 2026-01-15  
**User**: grant.jackman@shopify.com  
**Votes**: 5 (3 unique users)

**Original Query**:
> "Find all contracts with indemnity clauses"

**Description**:
User wants to search within contract PDFs for specific legal clauses like indemnity, liability, and termination. Use case is for legal compliance audits and risk assessment.

**Current Alternative**:
1. Use `search_contracts` with query='indemnity' (searches metadata only)
2. Use Ironclad UI → Records → Search within PDFs

**Roadmap Status**:
✅ Added to Phase 2 roadmap (Q2 2026)

**Requirements**:
- PDF text extraction API
- AI model for clause identification
- Support for multiple clause types

**Related Requests**:
- FR-20260116-003: Trademark clause search
- FR-20260120-007: Liability cap extraction

**Admin Notes**:
High priority - 5 votes in first week. Requires Ironclad API enhancement for PDF access. Timeline: Q2 2026 pending API availability.

**Voters**:
1. grant.jackman@shopify.com (2026-01-15)
2. jane.doe@shopify.com (2026-01-16)
3. john.smith@shopify.com (2026-01-18)
```

---

## 🔗 Related Documents

- **FEATURE_ROADMAP.md** - Official roadmap (Phase 1/2/3)
- **AI_ROUTING_GUIDE.md** - When to offer feature requests
- **PHASE_2_TRENDING_ANALYSIS_DESIGN.md** - Analytics design docs

---

**This document is automatically updated by the MCP when users log feature requests.**

---

_Last manual review: January 13, 2026_  
_Next review: January 20, 2026_
