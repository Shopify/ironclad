# Ironclad MCP Feature Roadmap
## What's Available Now and What's Coming

**Last Updated**: January 13, 2026

---

## 🎯 How to Use This Document

**For AI Assistants**: When a user asks about a feature that isn't currently available, check this roadmap and inform them:
- ✅ **Phase 1 (Current)**: "This is available now. Let me help you with that..."
- ⚠️ **Phase 2 (Planned)**: "This is planned for Phase 2. Currently, please use [alternative]..."
- 🔮 **Phase 3 (Future)**: "This is being considered for a future release. Currently, please use [alternative]..."
- ❌ **Not Planned**: "This isn't in the current roadmap. Please use [alternative]..."

---

## ✅ Phase 1: Current Capabilities (LIVE)

### Contract Search & Retrieval
- ✅ **Search by counterparty**: "Find contracts with Zoom"
- ✅ **Search by contract type**: "Show me Plus Agreements"
- ✅ **Search by keywords**: "Find contracts mentioning 'GDPR'"
- ✅ **Get contract details**: "Show me details for IC-95582"
- ✅ **List attachments**: "What documents are attached to IC-5701?"
- ✅ **Contract families**: Automatically detects amendments and parent contracts

### Workflow Management
- ✅ **Search workflows**: "What contracts are in workflow?"
- ✅ **Filter by stage**: "Contracts in approval" (filters for Review stage)
- ✅ **Filter by type**: "Active workflows for Plus Agreements"
- ✅ **Get workflow details**: "Get workflow details for IC-60730"
- ✅ **View participants**: See who's involved in each workflow
- ✅ **View approvals**: See approval status and approvers

### Counts & Totals
- ✅ **Count by type**: "How many Plus Agreements total?"
- ✅ **Count by counterparty**: "How many Zoom contracts do we have?"
- ✅ **Count workflows**: "How many contracts are in workflow?"

### Known Limitations (Phase 1)
- ❌ **No date filtering**: Cannot filter by date ranges (API limitation)
- ❌ **No trending/analytics**: Cannot show trends over time
- ❌ **No contract editing**: Read-only access
- ❌ **No bulk exports with date filters**: Cannot export "all contracts from 2024"
- ❌ **No clause extraction**: Cannot search within contract text/PDFs
- ❌ **No address extraction**: Does not parse address fields

---

## ⚠️ Phase 2: Planned Features (IN DEVELOPMENT)

### Clause Extraction & AI Reading
**Status**: Research phase  
**Expected**: Q2 2026 (pending API capabilities)

**What's Coming**:
- 🔮 **Clause search**: "Find all contracts with indemnity clauses"
- 🔮 **AI-powered Q&A**: "Do we have the right to use [Counterparty's] logo in advertising?"
- 🔮 **Obligation extraction**: "Tell me about our indemnity obligations with Microsoft"
- 🔮 **Risk identification**: "Which contracts have unlimited liability?"
- 🔮 **Trademark rights**: "What trademark usage rights do we have from partners?"

**Requirements**:
- Access to contract PDFs/attachments via API
- PDF text extraction capabilities
- AI model fine-tuned for contract clause identification

**User Response When Asked**:
> "Clause extraction and AI reading of contract PDFs is planned for Phase 2 (Q2 2026). Currently, please:
> 1. Use the Ironclad UI to view contract PDFs directly
> 2. Search for keywords in contract metadata using the MCP
> 3. Use `get_contract_details` to see if specific terms are mentioned in contract summaries"

---

### Date-Filtered Analytics (CONDITIONAL)
**Status**: Under review (see `PHASE_2_TRENDING_ANALYSIS_DESIGN.md`)  
**Expected**: TBD (depends on Ironclad API enhancements)

**What's Being Considered**:
- ⚠️ **Monthly counts**: "How many Plus Agreements in December 2025?" (20-30 sec)
- ⚠️ **Quarterly comparisons**: "Compare Q3 to Q4 Plus Agreements" (30-60 sec)
- ⚠️ **AI-driven insights**: "Why did Q4 Plus contracts spike?" (60+ sec)

**Current Decision**: **NOT BUILDING YET**

**Why**:
1. Ironclad API doesn't support server-side date filtering
2. Client-side filtering requires scanning 40,000+ records (20-30 seconds minimum)
3. Results may be incomplete/unreliable
4. Ironclad UI already does this perfectly in ~10 seconds

**Will only build if**:
- Ironclad adds server-side date filtering to API
- Users strongly prefer MCP (slow) over UI redirect (fast)
- We can provide AI-driven insights beyond raw data

**User Response When Asked**:
> "Date-filtered analytics (trends, comparisons, date ranges) are being evaluated for Phase 2, but currently all such queries are redirected to the Ironclad UI because:
> - The Ironclad UI is **faster** (10 sec vs. 20-30 sec)
> - The Ironclad UI is **more reliable** (complete data)
> - The Ironclad UI has **better visualizations** (charts, graphs)
>
> Please use Ironclad → Records → Filter by date range for instant results."

---

## 🔮 Phase 3: Future Considerations

### Contract Comparison
**Status**: Idea phase  
**Expected**: Q3-Q4 2026

**What's Being Considered**:
- 🔮 **Side-by-side comparison**: "Compare contract IC-5701 with IC-95582"
- 🔮 **Clause differences**: "What clauses differ between these NDAs?"
- 🔮 **Term changes**: "What changed between the original and amendment?"

**User Response When Asked**:
> "Contract comparison is being considered for Phase 3. Currently, please use the Ironclad UI to view contracts side-by-side."

---

### Bulk Operations
**Status**: Idea phase  
**Expected**: TBD

**What's Being Considered**:
- 🔮 **Multi-contract export**: "Export all Zoom contracts"
- 🔮 **Batch analysis**: "Analyze payment terms across all Plus Agreements"
- 🔮 **Bulk metadata extraction**: "List all renewal dates for active contracts"

**Requirements**:
- Reliable pagination (API limit: 100 records/page)
- Performance optimization (40,000+ contracts to scan)
- Clear progress indicators for long-running operations

**User Response When Asked**:
> "Bulk operations are being considered for a future release. Currently, please use the Ironclad UI's export functionality for bulk data."

---

### Advanced Search
**Status**: Idea phase  
**Expected**: TBD

**What's Being Considered**:
- 🔮 **Boolean operators**: "Contracts with Zoom AND (status='active' OR renewalDate > 2025)"
- 🔮 **Saved searches**: "Run my saved search 'Expiring Q1'"
- 🔮 **Fuzzy matching**: "Find contracts with companies similar to 'Mikrosoft'"

**User Response When Asked**:
> "Advanced search is being considered for a future release. Currently, the MCP supports basic keyword, counterparty, and contract type searches."

---

## ❌ Not Planned (Use Ironclad UI)

### Contract Editing & Creation
**Status**: Not planned  
**Reason**: Security, compliance, and audit requirements

**What Won't Be Added**:
- ❌ Create new contracts
- ❌ Update contract fields
- ❌ Upload attachments
- ❌ Change workflow stages
- ❌ Approve/reject contracts
- ❌ Send for signature

**User Response When Asked**:
> "Contract editing and creation are not planned for the MCP due to security and compliance requirements. Please use the Ironclad UI for all editing operations:
> - Create contracts: Ironclad → New Contract
> - Edit fields: Ironclad → Contract Details → Edit
> - Upload documents: Ironclad → Attachments → Upload
> - Workflow actions: Ironclad → Workflow → [Action]"

---

### Real-Time Notifications
**Status**: Not planned  
**Reason**: MCP architecture (pull-based, not push-based)

**What Won't Be Added**:
- ❌ "Notify me when IC-5701 is signed"
- ❌ "Alert me when contracts are expiring"
- ❌ "Watch for new Plus Agreements"

**User Response When Asked**:
> "Real-time notifications are not supported by the MCP architecture. Please use Ironclad's built-in notification features:
> - Ironclad → Settings → Notifications
> - Set up email alerts for contract events"

---

## 📊 Feature Request Process

### How to Request a New Feature

If a user asks for something not on this roadmap:

**Step 1: Acknowledge**
> "That's not currently available or planned. Let me see if there's an alternative..."

**Step 2: Suggest Alternative**
> "You can accomplish this by:
> 1. [Alternative approach using current features]
> 2. [Ironclad UI workflow]
> 3. [Workaround if applicable]"

**Step 3: Offer to Log Request** (if appropriate)
> "Would you like me to log this as a feature request? If so, I'll note:
> - What you're trying to accomplish
> - Your proposed feature
> - How often you'd use it"

---

## 🔗 Related Documents

- **AI_ROUTING_GUIDE.md** - When to use MCP vs. redirect to Ironclad UI
- **PHASE_2_TRENDING_ANALYSIS_DESIGN.md** - Detailed design for Phase 2 analytics
- **TEST_RESULTS_ACTION_PLAN.md** - Phase 1 test results and limitations
- **README.md** - Current feature list and setup guide

---

## 🎯 Quick Reference: Common "Not Available" Responses

### "Show me trends over 2024"
> "Trending analysis is under evaluation for Phase 2. Currently, Ironclad UI provides faster and more reliable trending with visual charts. Use: Ironclad → Records → Filter by date → View analytics."

### "Find contracts with indemnity clauses"
> "Clause extraction is planned for Phase 2 (Q2 2026). Currently, use `search_contracts` with query='indemnity' to search contract metadata, or use Ironclad UI to search within PDFs."

### "Export all contracts from December 2025"
> "Date-filtered exports are not currently available due to API limitations. Use Ironclad UI for instant date-filtered exports: Ironclad → Records → Filter by date range → Export."

### "Compare IC-5701 with IC-95582"
> "Contract comparison is being considered for Phase 3. Currently, use `get_contract_details` for each contract individually and compare manually."

### "Update the renewal date for IC-5701"
> "Contract editing is not planned for the MCP due to security requirements. Use Ironclad UI: Ironclad → IC-5701 → Edit → Update renewal date."

### "Notify me when IC-5701 is signed"
> "Real-time notifications are not supported by MCP architecture. Use Ironclad → Settings → Notifications to set up email alerts."

---

## 📅 Roadmap Timeline

| Phase | Status | Timeline | Focus |
|-------|--------|----------|-------|
| **Phase 1** | ✅ **LIVE** | Jan 2026 | Search, retrieval, workflows, basic counts |
| **Phase 2A** | 🔬 Research | Q2 2026 | Clause extraction, AI reading |
| **Phase 2B** | ⚠️ On Hold | TBD | Date analytics (pending API fix) |
| **Phase 3** | 💡 Ideas | Q3-Q4 2026 | Comparison, bulk ops, advanced search |

---

**Key Principle**: **The MCP should complement Ironclad UI, not replace it.** When Ironclad UI does something better (faster, more reliable, better UX), we redirect users there.

**User Trust is Critical**: It's better to redirect to a fast, reliable UI than provide slow or potentially incomplete data through the MCP.
