# AI Routing Guide for Ironclad MCP
## When to Use MCP vs. Ironclad UI

**Last Updated**: January 13, 2026  
**Version**: 2.1 (Added Feature Roadmap)  
**Status**: Critical - Must Follow Exactly

---

## 📋 Using This Guide with the Feature Roadmap

**IMPORTANT**: When a user asks about a feature that isn't available:

1. **Check `FEATURE_ROADMAP.md`** to see if it's planned
2. **Tell the user** what phase it's in:
   - ✅ "This is available now..." (Phase 1)
   - ⚠️ "This is planned for Phase 2..." (with timeline and alternative)
   - 🔮 "This is being considered for Phase 3..." (with alternative)
   - ❌ "This isn't planned..." (with alternative)
3. **Always provide an alternative** (usually Ironclad UI)

**Example Response**:
> "Clause extraction (searching within PDFs) is planned for Phase 2 (Q2 2026). Currently, you can:
> 1. Use `search_contracts` with query='indemnity' to search metadata
> 2. Use Ironclad UI to view and search PDFs directly
> 
> Would you like me to search contract metadata instead?"

---

## 🚨 CRITICAL: Unreliable Operations - ALWAYS Redirect to UI

These operations are **BLOCKED** in Phase 1 because they produce unreliable or partial data.  
**NEVER** attempt to produce results for these queries - always redirect immediately.

### ❌ BLOCK: Date-Filtered Exports

**Trigger Words**: ANY combination of:
- Date terms: "in December", "from [date] to [date]", "Q4 2024", "last month", "2025", "between", "during"
- Export terms: "export", "download", "CSV", "generate report", "create report"

**Examples of BLOCKED Queries**:
- ❌ "Export Plus Agreements from December 2025"
- ❌ "Download contracts completed in Q4"
- ❌ "CSV of agreements signed last year"
- ❌ "Generate report for 2024 contracts"
- ❌ "Create export of contracts between Jan 1 and March 31"

**Why Blocked**:
- API doesn't support date filtering
- Client-side filtering requires scanning 40,000+ records
- Results are incomplete/unreliable (only finds 5-10 out of hundreds)
- Ironclad UI does this in 10 seconds with accurate results

**Response Template**:
```
I understand you want to export [contract type] from [date range].

⚠️ Date-filtered exports require the Ironclad UI because the API doesn't 
support server-side date filtering. Attempting this via the MCP would 
produce incomplete and unreliable results.

Please use Ironclad directly:
1. Go to Ironclad → Records
2. Filter by [record type]
3. Filter by [date field]: [start date] to [end date]
4. Click "Export" → CSV

This will complete in ~10 seconds with accurate results.

I can help with:
- Total [record type] count (instant)
- Find specific contracts by company name
- Get details for a known contract ID

Would you like me to help with one of these instead?
```

---

### ❌ BLOCK: Date-Filtered Counts

**Trigger Words**: ANY combination of:
- Count terms: "how many", "count", "number of", "total"
- Date terms: "in December", "from [date]", "Q4 2024", "last month", "2025", "completed in", "signed between"

**Examples of BLOCKED Queries**:
- ❌ "How many Plus Agreements in December 2025?"
- ❌ "Count contracts from Q4 2024"
- ❌ "Agreements completed in 2025"
- ❌ "How many signed between Jan and March?"
- ❌ "Count last month's Plus Agreements"

**Why Blocked**:
- Takes 20-30 seconds minimum
- Results may be incomplete due to pagination limits
- Ironclad UI does this instantly with filters

**Response Template**:
```
I understand you want to count [contract type] [date filter].

⚠️ Date-filtered counts require the Ironclad UI due to API limitations 
that cause slow scans and potentially incomplete results.

Please use Ironclad directly:
1. Go to Ironclad → Records
2. Filter by [record type]
3. Filter by [date field]: [start date] to [end date]
4. View the count at the top of the results

I can help with:
- Total [record type] count (instant, no date filter)
- Find specific contracts by company
- Get details for a known contract ID

Would you like the total [record type] count instead?
```

---

### ❌ BLOCK: Trending & Analytics Queries

**Trigger Words**:
- Trending: "trends", "over time", "trending", "growth", "decline"
- Comparisons: "compare", "vs", "Q3 to Q4", "year over year"
- Aggregations: "breakdown", "by type", "by status", "average", "median"
- Future-looking: "expiring in", "renewing in", "next 30 days", "upcoming"
- Analytics: "analysis", "analytics", "report", "dashboard"

**Examples of BLOCKED Queries**:
- ❌ "Show me contract trends over 2024"
- ❌ "Contracts expiring in the next 30 days"
- ❌ "Compare Q3 to Q4 Plus Agreements"
- ❌ "Status breakdown for all contracts"
- ❌ "Average contract value by type"
- ❌ "Growth in Plus Agreements this year"
- ❌ "Analyze contract renewal patterns"

**Why Blocked**:
- Requires date filtering (unreliable)
- Requires aggregations across large datasets
- Results would be incomplete/misleading
- Ironclad has purpose-built analytics for this

**Response Template**:
```
I understand you want [trending/analytics insight].

⚠️ Trending and analytics queries require the Ironclad UI, which has 
purpose-built reporting features for reliable analysis across date ranges.

Please use Ironclad directly:
1. Go to Ironclad → Analytics (or Reports)
2. Use date range filters and visualization tools
3. Export results if needed

The MCP is designed for quick lookups and instant queries without date filtering.

I can help with:
- Search contracts by counterparty (instant)
- Get specific contract details (instant)
- Total counts by type (instant, no dates)

Would you like help with a specific contract lookup instead?
```

---

### ❌ BLOCK: Edit/Update Operations

**Trigger Words**:
- "edit", "update", "change", "modify", "set", "delete"
- "rename", "correct", "fix", "adjust"

**Examples of BLOCKED Queries**:
- ❌ "Edit renewal date for IC-5701"
- ❌ "Update status to Active"
- ❌ "Change counterparty name in IC-121057"
- ❌ "Modify expiration date"

**Why Blocked**:
- MCP is read-only (Phase 1 design decision)
- Safety: edits require validation and audit trail
- Ironclad UI has proper controls and validation

**Response Template**:
```
I understand you want to [edit/update] [field] for [contract].

⚠️ The Ironclad MCP is read-only. Editing contracts requires the 
Ironclad UI for validation, audit trail, and proper authorization.

Please use Ironclad directly:
1. Search for [contract ID] in Ironclad
2. Open the contract
3. Use the "Edit" button to make changes
4. Changes will be properly validated and logged

I can help you:
- Look up the current value of [field] in [contract]
- Find the contract you want to edit

Would you like me to show you the current contract details?
```

---

## ✅ USE MCP: Fast & Reliable Operations

These operations complete in < 5 seconds with 100% reliability.

### ✅ Contract Lookup by ID

**Trigger Patterns**:
- "Find contract IC-[number]"
- "Get details for IC-[number]"
- "Show me IC-[number]"
- "What are the terms of IC-[number]?"
- Just the ID: "IC-5701" or "5701"

**Tool**: `get_contract_details`

**Examples**:
- ✅ "Find contract IC-5701"
- ✅ "Get details for IC-121057"
- ✅ "Show me IC-95582"
- ✅ "What are the terms of IC-5701?"
- ✅ "IC-116482"

**Expected Time**: < 1 second

---

### ✅ Search by Counterparty

**Trigger Patterns**:
- "Find contracts with [company]"
- "Do we have agreement with [company]"
- "Search for [company] contracts"
- "Contracts with [company]"
- "Show me agreements with [company]"

**Tool**: `search_contracts` with `counterparty` parameter

**Examples**:
- ✅ "Find contracts with Zoom"
- ✅ "Do we have agreement with Troon Golf"
- ✅ "Search for Gold Standard contracts"
- ✅ "Contracts with COSMONET"
- ✅ "Show me agreements with ELC"

**Expected Time**: < 2 seconds  
**Note**: Default limit is 20 results. If user wants more, they can ask for "all" or specify a limit.

---

### ✅ Quick Counts (No Dates)

**Trigger Patterns**:
- "How many [record type] total?"
- "Count [record type]"
- "Number of [record type]"
- "Total [record type]"
- "How many contracts with [company]?" (combines count + counterparty)

**Tool**: `count_contracts`

**Examples**:
- ✅ "How many Plus Agreements total?"
- ✅ "Count CCS for Enterprise contracts"
- ✅ "How many contracts with Zoom?"
- ✅ "Total Procurement Agreements"
- ✅ "Number of Plus Agreements"

**Expected Time**: < 1 second

**CRITICAL**: If the query includes ANY date reference, this becomes BLOCKED (see above).

---

### ✅ List Attachments

**Trigger Patterns**:
- "List attachments for IC-[number]"
- "What PDFs does IC-[number] have?"
- "Does IC-[number] have a signed copy?"
- "Show me documents for IC-[number]"
- "Attachments for IC-[number]"

**Tool**: `get_contract_attachments`

**Examples**:
- ✅ "List attachments for IC-5701"
- ✅ "What PDFs does IC-121057 have?"
- ✅ "Does IC-5701 have a signed copy?"
- ✅ "Show me documents for IC-95582"

**Expected Time**: < 2 seconds

---

### ✅ Extract Counterparty Address

**Trigger Patterns**:
- "Get [company]'s address from IC-[number]"
- "Extract counterparty address for IC-[number]"
- "What's the address in IC-[number]?"
- "Address for IC-[number]"

**Tool**: `extract_counterparty_address`

**Examples**:
- ✅ "Get Gold Standard's address from IC-5701"
- ✅ "Extract counterparty address for IC-121057"
- ✅ "What's the address in IC-95582?"
- ✅ "Address for IC-116482"

**Expected Time**: < 5 seconds  
**Note**: AI extraction may not be 100% reliable. Document failures gracefully.

---

### ✅ General Keyword Search

**Trigger Patterns**:
- "Show me some [record type]"
- "Search for contracts with '[keyword]'"
- "Find [record type]"
- "Browse [record type]"

**Tool**: `search_contracts` with `query` parameter

**Examples**:
- ✅ "Show me some Plus Agreements"
- ✅ "Find procurement agreements"
- ✅ "Browse CCS contracts"
- ✅ "Search for contracts with 'GDPR'" (searches metadata only)
  - **Note**: Searching *within* PDFs (clause extraction) is planned for Phase 2. See `FEATURE_ROADMAP.md`.

**Expected Time**: < 2 seconds  
**Note**: Defaults to 10-20 results

---

### ✅ Workflow Search

**Trigger Patterns**:
- "Active workflows for [type]"
- "What contracts are in workflow?"
- "Show me pending [company] contracts"
- "Workflows for [type]"
- "Contracts in approval" / "Contracts in review"
- "In-progress contracts"
- "Contracts waiting for signature" / "Contracts in sign stage"

**Tool**: `search_workflows`

**Stage Filtering**:
- "In approval" / "In review" → Use `stage='Review'` (capitalized!)
- "Waiting for signature" / "Pending signature" → Use `stage='Sign'` (capitalized!)
- "Draft contracts" → Use `stage='Draft'` (capitalized!)
- No stage mentioned → Don't use stage parameter

**IMPORTANT**: Stage values are capitalized: `Review`, `Sign`, `Draft` (not lowercase)

**Examples**:
- ✅ "Active workflows for Plus Agreements" → No stage filter
- ✅ "What contracts are in workflow?" → No stage filter
- ✅ "Show me pending Zoom contracts" → counterparty='Zoom'
- ✅ "Workflows for Procurement Agreements" → record_type='procurementAgreement'
- ✅ "Contracts in approval" → **stage='review'** (CRITICAL)
- ✅ "Plus Agreements waiting for signature" → record_type='plusAgreement', stage='sign'

**Expected Time**: < 2 seconds

**IMPORTANT**: The API uses stage names like 'review', 'sign', 'draft' (lowercase). Use these exact values.

---

### ✅ Workflow Details

**Trigger Patterns**:
- "Get workflow details for [ID]"
- "Show me workflow [ID]"
- "What's the status of [ID]?"
- "Who's reviewing [ID]?"

**Tool**: `get_workflow_details`

**Examples**:
- ✅ "Get workflow details for IC-125001"
- ✅ "What's the status of IC-125001?"
- ✅ "Who's reviewing the ACME contract?"

**Expected Time**: < 2 seconds  
**Note**: Returns participants, approvals, stage, status, recent activity

---

### ✅ Marketing Rights Queries

**Trigger Patterns**:
- "Can we use [merchant]'s logo?"
- "Marketing rights for [merchant]"
- "Can we use [merchant] in our marketing?"
- "Logo usage rights for [company]"
- "What are the marketing rights for IC-[number]?"
- "Can [vendor] use Shopify's logo?"

**Tool**: `get_contract_details`

**Response Logic**:

**For Plus Agreements, Plus Large Agreements, CCS for Enterprise**:

Check the `Marketing Rights` metadata field in the contract details:

1. **If "Standard"**:
   ```
   ✅ **Marketing Rights**: Standard
   
   Shopify can use [merchant]'s name and logo in marketing materials without 
   requiring explicit consent for each use.
   ```

2. **If "Meet in the Middle"**:
   ```
   ⚠️ **Marketing Rights**: Meet in the Middle
   
   Shopify requires explicit consent from [merchant] before using their name 
   or logo in marketing materials. Please reach out to the merchant for approval 
   before each use.
   ```

3. **If "Other"**:
   ```
   📄 **Marketing Rights**: Other (Bespoke Arrangement)
   
   This contract has custom marketing rights terms. Please review the contract 
   in Ironclad to understand the specific rights granted:
   
   1. Open Ironclad → Search for IC-[number]
   2. Review the Marketing Rights section of the contract
   3. Look for clauses about logo usage, brand usage, or publicity rights
   
   [Link to contract in Ironclad]
   ```

4. **If field is empty or not present**:
   ```
   ⚠️ Marketing Rights information is not recorded in metadata.
   
   Please review the contract in Ironclad:
   1. Open Ironclad → Search for IC-[number]
   2. Look for Marketing Rights or Publicity Rights clauses
   ```

**For Procurement Agreements and Other Record Types**:

Marketing rights metadata is only captured for Plus Agreements. For vendor contracts:

```
⚠️ Marketing rights for vendor use of Shopify's name/logo are not captured 
in contract metadata.

To determine if [vendor] can use Shopify's branding:
1. Open Ironclad → Search for IC-[number]
2. Review the contract for:
   - "Publicity Rights" clauses
   - "Marketing" or "Brand Usage" sections
   - "Confidentiality" restrictions
   - "Use of Marks" or "Trademark License" clauses

📍 **Note**: Contract reading/clause extraction is planned for Phase 2 (Q2 2026), 
which will make these queries instant.

Would you like me to help you find the contract ID if you don't have it?
```

**Examples**:
- ✅ "Can we use Fast-Fix Jewelry's logo?" → Get contract details, check Marketing Rights field
- ✅ "Marketing rights for IC-120483" → Get contract details, return Marketing Rights value
- ✅ "What are the marketing rights for Gold Standard?" → Search for contract first, then get details
- ✅ "Can Zoom use Shopify's logo in their materials?" → Get contract, inform that field doesn't exist for Procurement

**Expected Time**: < 2 seconds (for lookup) + manual contract review if "Other"

**Special Note for Phase 2**: When contract reading is available, the MCP will be able to 
automatically extract marketing/publicity rights clauses from any contract type.

---

## 🎯 Decision Tree

Use this flowchart to determine routing:

```
User Query
│
├─ Contains date + export? → ❌ BLOCK → Redirect to UI
│
├─ Contains date + count? → ❌ BLOCK → Redirect to UI
│
├─ Contains "trend"/"analytics"/"expiring in"? → ❌ BLOCK → Redirect to UI
│
├─ Contains "edit"/"update"/"change"? → ❌ BLOCK → Redirect to UI
│
├─ Has contract ID (IC-xxxxx) + completed? → ✅ USE MCP → get_contract_details
│
├─ Has contract ID (IC-xxxxx) + in progress/workflow? → ✅ USE MCP → get_workflow_details
│
├─ Contains "workflow"/"in progress"/"pending"/"approval"? → ✅ USE MCP → search_workflows
│
├─ Has company name + "pending"/"workflow"? → ✅ USE MCP → search_workflows
│
├─ Has company name? → ✅ USE MCP → search_contracts (counterparty)
│
├─ Says "how many" without date? → ✅ USE MCP → count_contracts
│
├─ Says "attachments"? → ✅ USE MCP → get_contract_attachments
│
├─ Says "address"? → ✅ USE MCP → extract_counterparty_address
│
├─ Says "marketing rights"/"logo"/"branding"? → ✅ USE MCP → get_contract_details + interpret Marketing Rights field
│
└─ General search/keyword? → ✅ USE MCP → search_contracts (query)
```

---

## 🧪 Test Your Understanding

### Should These Use MCP or Redirect to UI?

1. "How many Plus Agreements in December 2025?" → **❌ BLOCK** (date + count)
2. "Find contracts with Zoom" → **✅ USE MCP** (counterparty search)
3. "Export Plus Agreements from Q4" → **❌ BLOCK** (date + export)
4. "Get details for IC-5701" → **✅ USE MCP** (contract ID lookup)
5. "Show me contract trends over 2024" → **❌ BLOCK** (trending/analytics)
6. "How many Plus Agreements total?" → **✅ USE MCP** (count, no date)
7. "Contracts expiring in 30 days" → **❌ BLOCK** (future-looking/date)
8. "Active workflows for Plus Agreements" → **✅ USE MCP** (workflow search) **UPDATED!**
9. "Update renewal date for IC-121057" → **❌ BLOCK** (edit operation)
10. "List attachments for IC-95582" → **✅ USE MCP** (attachments)
11. "What contracts are in approval?" → **✅ USE MCP** (workflow search) **NEW!**
12. "Show me pending Zoom contracts" → **✅ USE MCP** (workflow search) **NEW!**

---

## 📊 Success Metrics

**Phase 1 is working correctly when**:

- ✅ 100% of date-filtered exports redirect to UI
- ✅ 100% of date-filtered counts redirect to UI
- ✅ 100% of trending queries redirect to UI
- ✅ 100% of edit queries redirect to UI
- ✅ 100% of workflow queries use MCP workflow tools **UPDATED!**
- ✅ 100% of simple lookups use MCP and complete in < 5 seconds
- ✅ 0% of partial/incomplete results provided to users

**If you see any of these, routing is BROKEN**:
- ❌ MCP attempts to produce date-filtered export
- ❌ MCP produces "estimate" or "partial" count for date query
- ❌ MCP attempts trending analysis
- ❌ MCP redirects workflow queries to UI (should use workflow tools)
- ❌ User gets incomplete data without warning

---

## 🗺️ Feature Roadmap & "Not Available" Responses

When a user asks about a feature that's not currently available, **always check `FEATURE_ROADMAP.md`** and inform them about:
1. Whether it's planned (Phase 2, 3, or not planned)
2. When it might be available
3. Why it's not currently available
4. Alternative approaches they can use now

### Common "Not Available" Questions

| User Request | Status | Response | Alternative |
|-------------|--------|----------|-------------|
| "Find contracts with indemnity clauses" | 🔮 Phase 2 (Q2 2026) | "Clause extraction is planned for Phase 2..." | Search metadata or use Ironclad UI |
| "Show me trends over 2024" | ⚠️ On Hold | "Date analytics are under review..." | Use Ironclad UI (faster, more reliable) |
| "Compare IC-5701 with IC-95582" | 🔮 Phase 3 | "Contract comparison is being considered..." | Get details for each separately |
| "Export all December 2025 contracts" | ⚠️ On Hold | "Date-filtered exports require Ironclad UI..." | Use Ironclad UI export |
| "Update renewal date for IC-5701" | ❌ Not Planned | "Contract editing isn't planned..." | Use Ironclad UI editing |
| "Notify me when IC-5701 is signed" | ❌ Not Planned | "Notifications aren't supported..." | Use Ironclad notification settings |

### Response Template for Unavailable Features

```markdown
[Feature name] is [status from roadmap].

📍 **What's Available Now**: [current alternatives]
🔮 **What's Coming**: [if planned, mention phase and timeline]
💡 **Alternative**: [suggest Ironclad UI or workaround]

Would you like me to [suggest alternative action]?
```

**Examples**:

**For Clause Extraction**:
> "Searching within contract PDFs (clause extraction) is planned for Phase 2 (Q2 2026). 
> 
> Currently, you can:
> 1. Use `search_contracts` with query='indemnity' to search contract metadata
> 2. Use Ironclad UI to view and search PDFs directly
> 
> Would you like me to search contract metadata instead?"

**For Trending Analysis**:
> "Date-filtered trending analysis is under evaluation for Phase 2. Currently, all trending queries redirect to Ironclad UI because:
> - Ironclad UI is **faster** (10 sec vs 20-30 sec)
> - Ironclad UI is **more reliable** (complete data)
> - Ironclad UI has **better visualizations** (charts, graphs)
> 
> Use: Ironclad → Records → Filter by date range → Analytics"

**For Contract Editing**:
> "Contract editing is not planned for the MCP due to security and compliance requirements.
> 
> To update contract fields:
> 1. Open Ironclad → Search for IC-5701
> 2. Click 'Edit' button
> 3. Update the field
> 4. Save changes
> 
> This ensures proper audit trails and approvals."

### Key Principle

**Always be transparent about limitations** and **always provide a working alternative**.

Better to say "This is planned for Q2 2026, but here's how to do it now..." than to attempt something that produces incomplete/unreliable results.

---

## 💡 Feature Request Collection

### When to Offer Feature Requests

After explaining that a feature isn't available and suggesting alternatives, **always offer to log a feature request** if:

1. ✅ The feature is **not** in Phase 2/3 roadmap
2. ✅ The user's request is **specific and actionable**
3. ✅ The feature seems **reasonable and useful**
4. ❌ **Don't offer** if already in roadmap (just mention the phase/timeline)
5. ❌ **Don't offer** if fundamentally impossible or out of scope

### Feature Request Workflow

**Step 1: Detect Unavailable Feature**

When you can't fulfill a request, check `FEATURE_ROADMAP.md`:
- If in Phase 2/3: Tell user the phase and timeline
- If not planned or not in roadmap: Offer to log feature request

**Step 2: Explain and Suggest Alternatives**

> "❌ [Feature] isn't currently available because [reason].
> 
> **Current alternatives**:
> 1. [Alternative 1]
> 2. [Alternative 2]
> 
> Would you like to [use alternative 1], or would you like me to log this as a feature request?"

**Step 3: Check for Similar Requests**

Before creating a new request, **always search `FEATURE_REQUESTS.md`** for similar requests:

```markdown
# Search for keywords from user's query
# Example: User asks "Find contracts with auto-renewal clauses"
# Search for: "auto-renewal", "renewal clause", "clause extraction"
```

If similar request exists:
> "✅ I found a similar feature request (**FR-20260115-001: Clause Extraction**) that has 5 votes from other users.
> 
> This request asks for: [brief description]
> 
> Would you like to add your vote to this existing request?"

If no similar request:
> "I don't see any similar requests. Would you like me to create a new feature request?"

**Step 4: Collect Details** (if user says yes)

Ask for:
1. **Use case**: "Can you briefly describe why you need this feature?"
2. **Frequency**: "How often would you use this? (Daily/Weekly/Monthly/Occasionally)"
3. **Priority** (optional): "Is this blocking your work, or nice to have?"

**Step 5: Generate Request ID**

Format: `FR-YYYYMMDD-NNN`
- `YYYYMMDD` = Today's date
- `NNN` = Sequential number (count existing requests from today + 1)

Example: `FR-20260115-001` (first request on Jan 15, 2026)

**Step 6: Categorize**

Auto-detect category based on keywords:
- **🔍 Search & Filtering**: "search", "find", "filter", "query"
- **📊 Analytics & Reporting**: "trend", "compare", "analytics", "export", "report"
- **📄 Document Operations**: "PDF", "clause", "extract", "read", "attachment"
- **⚙️ Workflow Enhancements**: "workflow", "approval", "stage", "participant"
- **🔗 Integration**: "integrate", "sync", "API", "webhook"
- **💡 Other**: (default)

**Step 7: Format and Append**

Write to `knowledge_base/FEATURE_REQUESTS.md` in this format:

```markdown
#### FR-20260115-001: [Short descriptive title]
**Status**: 📥 New  
**Category**: [Auto-detected category]  
**Date**: YYYY-MM-DD  
**User**: [From IRONCLAD_USER_EMAIL]  
**Votes**: 1 (1 unique user)

**Original Query**:
> "[Exact query user asked]"

**Description**:
[What user was trying to accomplish]

**Use Case**:
[User's described use case]

**Frequency**: [Daily/Weekly/Monthly/Occasionally]

**Current Alternative**:
1. [Alternative you suggested]
2. [Another alternative]

**Roadmap Status**:
⚠️ Not yet in roadmap - pending review

**Admin Notes**:
_(To be filled by admin during review)_

**Voters**:
1. [user email] (YYYY-MM-DD)

---
```

**Step 8: Confirm to User**

> "✅ **Feature request logged!**
> 
> **Request ID**: FR-20260115-001  
> **Title**: Clause Extraction for Auto-Renewal Clauses  
> **Category**: Document Operations
> 
> Your request has been added to the feature request backlog and will be reviewed by the team. You can track all feature requests in the GitHub repo (link will be provided after deployment).
> 
> Is there anything else I can help you with using the current features?"

### Feature Request Template Examples

**Example 1: New Feature (Not in Roadmap)**

User asks: "Can you find contracts that auto-renew?"

**Response**:
> "❌ Searching for specific clauses within contract PDFs (like auto-renewal clauses) isn't currently available.
> 
> **Current alternatives**:
> 1. Use `search_contracts` with query='auto-renewal' to search contract metadata
> 2. Use Ironclad UI → Search within PDFs
> 
> **Note**: General clause extraction is planned for Phase 2 (Q2 2026), but auto-renewal specifically isn't on the roadmap yet.
> 
> Would you like me to:
> 1. Search contract metadata now, or
> 2. Log a feature request for auto-renewal clause detection?"

[If user says "log request":]

> "Great! To help prioritize this feature:
> 
> 1. **Use case**: Why do you need to find auto-renewal contracts?
> 2. **Frequency**: How often would you use this?"

[After user responds:]

> "✅ **Feature request logged!**
> 
> **FR-20260115-003: Auto-Renewal Clause Detection**  
> **Category**: Document Operations  
> **Votes**: 1
> 
> Your request will be reviewed by the team. Thanks for the feedback!"

**Example 2: Similar Request Exists**

User asks: "Find all contracts with indemnity clauses"

**Response**:
> "❌ Clause extraction isn't available yet. It's planned for Phase 2 (Q2 2026).
> 
> ✅ **Good news**: I found an existing feature request for this!
> 
> **FR-20260110-001: Clause Extraction (Indemnity, Liability, Termination)**  
> **Status**: Planning - Phase 2  
> **Votes**: 12 users
> 
> This request is already prioritized for Phase 2 development.
> 
> Would you like to:
> 1. Add your vote to this request (shows demand), or
> 2. Search contract metadata in the meantime?"

[If user says "add vote":]

> "✅ **Vote added!**
> 
> **FR-20260110-001** now has **13 votes** (including yours).
> 
> Your feedback helps us prioritize development. Thank you!"

**Example 3: Already in Roadmap (Don't Offer Request)**

User asks: "Can you search within PDFs?"

**Response**:
> "❌ PDF search (clause extraction) isn't available yet.
> 
> ✅ **This is already planned for Phase 2 (Q2 2026)!**
> 
> **What's coming**:
> - Search for specific clauses (indemnity, liability, etc.)
> - AI-powered contract Q&A
> - Obligation and risk extraction
> 
> **Current alternatives**:
> 1. Use `search_contracts` to search contract metadata
> 2. Use Ironclad UI to view and search PDFs directly
> 
> Would you like me to search contract metadata instead?"

[Note: No feature request offered because it's already in roadmap]

### Voting on Existing Requests

If user wants to vote on an existing request:

1. **Check if they already voted** (search for their email in the request)
   - If yes: "You've already voted for this request (on [date])"
   - If no: Proceed to add vote

2. **Update vote count**: `Votes: 12 (12 unique users)` → `Votes: 13 (13 unique users)`

3. **Add voter**: Append to voters list:
   ```markdown
   **Voters**:
   ...
   13. new.user@shopify.com (2026-01-15)
   ```

4. **Confirm**:
   > "✅ Vote added! FR-20260110-001 now has **13 votes**."

### Important Rules

1. **Always search for similar requests first** - Avoid duplicates
2. **Always offer alternatives** - Feature request is not a replacement for helping now
3. **Keep it brief** - Don't make feature request process feel like a burden
4. **Be enthusiastic** - Frame as "your feedback helps us improve!"
5. **Confirm with details** - Give user the request ID and category
6. **Track user email** - For deduplication and follow-up

### When NOT to Offer Feature Requests

❌ **Don't offer if**:
- Feature is already in Phase 2/3 roadmap (just mention it's coming)
- Feature is fundamentally impossible (e.g., "predict future contract values")
- Feature is out of scope (e.g., "integrate with my personal CRM")
- User is just asking a question (e.g., "What does this field mean?")
- Feature violates security/compliance (e.g., "let me edit contracts via MCP")

✅ **Do offer if**:
- Feature is reasonable and useful
- Not in current roadmap
- User seems genuinely interested (not just exploring)
- Feature aligns with MCP goals

---

## 🔄 Version History

### v2.1 - January 13, 2026 (Feature Roadmap Update)
- **ADDED**: Feature roadmap integration (`FEATURE_ROADMAP.md`)
- **ADDED**: Guidance on responding to unavailable features
- **ADDED**: Common "not available" questions table
- **ADDED**: Response templates for Phase 2/3 features
- Updated version to 2.1

### v2.0 - January 12, 2026 (Evening Update)
- **FEATURE**: Added workflow support (search_workflows, get_workflow_details)
- **CORRECTION**: Workflows API IS available (scope: public.workflows.readWorkflows)
- Removed workflows from BLOCKED section
- Added workflows to USE MCP section
- Updated decision tree to include workflow routing
- Updated test questions to include workflows

### v1.9 - January 12, 2026 (Afternoon)
- **CRITICAL**: Added BLOCK rules for date-filtered exports (Test 9.1 failure)
- **CRITICAL**: Added BLOCK rules for trending/analytics (Tests 11.1, 11.2 failures)
- **INCORRECT**: Added BLOCK rules for workflows (later found to be available)
- Removed "create_report" tool references (deprecated)
- Updated response templates with clearer explanations
- Added decision tree and test questions

### v1.0 - Initial Version
- Basic routing guidance
- Tool descriptions
- Simple examples

---

**Remember**: It's better to redirect to Ironclad UI than to provide incomplete or unreliable results.  
**User trust is critical** - partial data is worse than no data.
