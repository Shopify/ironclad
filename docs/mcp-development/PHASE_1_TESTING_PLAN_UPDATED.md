# Phase 1 Testing Plan - Ironclad MCP (Updated)
## Post-Testing Revisions - January 12, 2026

**Purpose**: Validate Phase 1 tools work reliably and AI routes queries appropriately  
**Target**: < 5 seconds per operation, 100% reliability  
**Version**: 2.0 (Post-Testing Updates)

---

## 🚨 Changes from Version 1.0

### Removed from Phase 1:
- ❌ **Test Suite 6: Workflow Search** - Workflows API not available with current permissions
- ❌ **Test 4.2.1: Version History** - Requires workflows API (Phase 2 research)

### Updated Tests:
- ✅ **Test 7.4**: Changed from "Shopify Plus" to "GDPR" keyword
- ✅ **Test 2.1**: Updated success criteria to clarify default limit behavior

### New Blocking Rules Added to AI Routing:
- ❌ Date-filtered exports (Tests 9.1-9.5) must ALWAYS redirect
- ❌ Date-filtered counts (Tests 8.1-8.5) must ALWAYS redirect
- ❌ Trending/analytics (Tests 11.1-11.5) must ALWAYS redirect
- ❌ Workflow queries must redirect (no API access)
- ❌ Edit operations must redirect (read-only design)

---

## ✅ Positive Tests (Should Use MCP)

### Test Suite 1: Contract Lookup by ID

**Expected Tool**: `get_contract_details`  
**Expected Time**: < 1 second

| # | Query | Expected Behavior | Status |
|---|-------|-------------------|--------|
| 1.1 | "Find contract IC-5701" | Returns full contract details | ✅ Pass |
| 1.2 | "Get details for IC-121057" | Returns contract or "not found" | ✅ Pass |
| 1.3 | "Show me IC-95582" | Returns contract details | ✅ Pass |
| 1.4 | "What are the terms of IC-5701?" | Returns contract with term details | ⚠️ Missing Transaction Fee field (KB update needed) |
| 1.5 | "IC-116482" | Recognizes ID and fetches details | ✅ Pass |

**Success Criteria**:
- ✅ Returns in < 1 second
- ✅ Provides complete contract data (see KB updates for field names)
- ✅ Handles non-existent IDs gracefully
- ✅ Works with or without "IC-" prefix

**KB Updates Needed**:
- Add "Transaction Fee" field for Plus/Plus Large agreements
- Map "Variable Platform Fee" → display as "D2C Variable Platform Fee"

---

### Test Suite 2: Search by Counterparty

**Expected Tool**: `search_contracts`  
**Expected Time**: < 2 seconds

| # | Query | Expected Behavior | Status |
|---|-------|-------------------|--------|
| 2.1 | "Find contracts with Zoom" | Returns Zoom contracts (default 20) | ✅ Pass (39 total found, showed 20) |
| 2.2 | "Do we have agreement with Troon Golf" | Returns yes/no with contracts | ✅ Pass |
| 2.3 | "Search for Gold Standard contracts" | Returns Gold Standard contracts | ✅ Pass |
| 2.4 | "Contracts with COSMONET" | Returns COSMONET contracts | ✅ Pass |
| 2.5 | "Show me agreements with ELC" | Returns ELC contracts | ✅ Pass |

**Success Criteria**:
- ✅ Returns relevant results in < 2 seconds
- ✅ Partial name matching works (e.g., "Zoom" finds "Zoom Video Communications, Inc.")
- ✅ Returns 0 results for non-existent companies
- ✅ Defaults to 20 results (should mention "Showing 20 results, set limit for more")

**Updated**: Test 2.1 clarified that showing 20 out of 39 is expected behavior with default limit.

---

### Test Suite 3: Quick Counts (No Dates)

**Expected Tool**: `count_contracts`  
**Expected Time**: < 1 second

| # | Query | Expected Behavior | Status |
|---|-------|-------------------|--------|
| 3.1 | "How many Plus Agreements total?" | Returns total count | ✅ Pass |
| 3.1.1 | "How many Plus Large Agreements?" | Returns total count | ✅ Pass |
| 3.2 | "Count CCS for Enterprise contracts" | Returns CCS count | ✅ Pass |
| 3.3 | "How many contracts with Zoom?" | Returns Zoom contract count | ✅ Pass |
| 3.4 | "Total Procurement Agreements" | Returns procurement count | ✅ Pass |
| 3.5 | "Number of Plus Agreements" | Returns count | ✅ Pass |

**Success Criteria**:
- ✅ Returns exact count in < 1 second
- ✅ Handles record type variations ("Plus Agreement" vs "plusAgreement")
- ✅ Combines with counterparty filter correctly
- ✅ Returns "0" for non-existent types

---

### Test Suite 4: Attachments

**Expected Tool**: `get_contract_attachments`  
**Expected Time**: < 2 seconds

| # | Query | Expected Behavior | Status |
|---|-------|-------------------|--------|
| 4.1 | "List attachments for IC-5701" | Returns attachment list | ✅ Pass |
| 4.2 | "What PDFs does IC-121057 have?" | Returns PDF metadata | ✅ Pass |
| 4.2.1 | "How many versions of the agreement for ELC?" | ⚠️ **PHASE 2** - Requires workflows API | ⚠️ Not available in Phase 1 |
| 4.3 | "Does IC-5701 have a signed copy?" | Returns yes/no with details | ✅ Pass |
| 4.4 | "Show me documents for IC-95582" | Returns document list | ✅ Pass |
| 4.5 | "Attachments for IC-116482" | Returns attachments | ✅ Pass |

**Success Criteria**:
- ✅ Returns attachment metadata in < 2 seconds
- ✅ Shows attachment types (signedCopy, amendment, etc.)
- ✅ Includes file sizes and upload dates
- ✅ Handles contracts with no attachments

**Updated**: Test 4.2.1 moved to Phase 2 research (version history requires workflows API).

---

### Test Suite 5: Address Extraction

**Expected Tool**: `extract_counterparty_address`  
**Expected Time**: < 5 seconds

| # | Query | Expected Behavior | Status |
|---|-------|-------------------|--------|
| 5.1 | "Get Gold Standard's address from IC-5701" | Extracts address from PDF | ⚠️ Fail (provided contact info only) |
| 5.2 | "Extract counterparty address for IC-121057" | Returns structured address | ✅ Pass |
| 5.3 | "What's the address in IC-95582?" | Extracts and formats address | ⚠️ Fail (doesn't extract from PDF) |
| 5.4 | "Find COSMONET's address in their contract" | Searches + extracts | ✅ Pass |
| 5.5 | "Address for IC-116482" | Extracts address | ✅ Pass |

**Success Criteria**:
- ✅ Returns in < 5 seconds
- ⚠️ Provides structured address when available
- ⚠️ Handles international addresses
- ⚠️ Gracefully handles PDFs without clear address

**Note**: AI extraction is not 100% reliable. **Address extraction is NOT CRITICAL** per user feedback. No additional work required.

---

### Test Suite 6: ❌ REMOVED - Workflow Search

**Removed from Phase 1**: Workflows API is not available with current OAuth permissions.

**Tests 6.1-6.5 moved to Phase 2 Research**:
- 6.1: Active workflows for Plus Agreements
- 6.2: What contracts are in workflow?
- 6.3: Show me pending Zoom contracts
- 6.4: Workflows for Procurement Agreements
- 6.5: Contracts in approval

**Phase 2 Investigation**:
- Is there a workflow-specific OAuth scope?
- Can we access in-progress contracts?
- What's the priority for this feature?

---

### Test Suite 7: General/Keyword Search

**Expected Tool**: `search_contracts`  
**Expected Time**: < 2 seconds

| # | Query | Expected Behavior | Status |
|---|-------|-------------------|--------|
| 7.1 | "Show me some Plus Agreements" | Returns sample Plus Agreements | ✅ Pass |
| 7.2 | "Search for contracts with 'annual subscription'" | Keyword search in name | ⚠️ Partial (found similar terms) |
| 7.3 | "Find procurement agreements" | Returns procurement contracts | ✅ Pass |
| 7.4 | "Contracts mentioning GDPR" | Keyword search (compliance term) | **UPDATED TEST** - Use for Phase 2 clause extraction |
| 7.5 | "Browse CCS contracts" | Returns CCS examples | ✅ Pass |

**Success Criteria**:
- ✅ Returns relevant results in < 2 seconds
- ✅ Keyword matching works in contract names
- ✅ Defaults to 10-20 results
- ✅ Can be combined with type filter

**Updated**: Test 7.4 changed from "Shopify Plus" (too broad) to "GDPR" (specific keyword for testing).

---

## ❌ Negative Tests (Should Direct to Ironclad UI)

### Test Suite 8: Date-Filtered Counts

**Expected Behavior**: ALWAYS redirect to Ironclad UI (NOT use MCP)

| # | Query | Expected Response | Status |
|---|-------|-------------------|--------|
| 8.1 | "How many Plus Agreements in December 2025?" | Redirects to Ironclad UI | ⚠️ Partial (auth error + redirect) |
| 8.2 | "Count contracts from Q4 2024" | Redirects to Ironclad UI | ⚠️ Partial (auth error + redirect) |
| 8.3 | "Agreements completed in 2025" | Redirects to Ironclad UI | ✅ Pass |
| 8.4 | "How many signed between Jan and March?" | Redirects to Ironclad UI | Pending retest |
| 8.5 | "Count last month's Plus Agreements" | Redirects to Ironclad UI | Pending retest |

**Success Criteria**:
- ✅ AI recognizes date pattern
- ✅ Responds with Ironclad UI recommendation
- ✅ Explains API limitations briefly
- ✅ Offers alternative MCP queries (total count, specific lookup)
- ✅ **NEVER produces partial/estimated counts**

**Critical**: See AI Routing Guide for response templates.

---

### Test Suite 9: Date-Filtered Exports

**Expected Behavior**: ALWAYS redirect to Ironclad UI (NEVER produce export)

| # | Query | Expected Response | Status |
|---|-------|-------------------|--------|
| 9.1 | "Export Plus Agreements from December 2025" | Redirects to Ironclad UI | ❌ **FAIL** - Produced partial CSV (9 records) |
| 9.2 | "Download contracts completed in Q4" | Redirects to Ironclad UI | Pending retest |
| 9.3 | "CSV of agreements signed last year" | Redirects to Ironclad UI | Pending retest |
| 9.4 | "Export contracts between Jan 1 and March 31" | Redirects to Ironclad UI | Pending retest |
| 9.5 | "Generate report for 2024 contracts" | Redirects to Ironclad UI | Pending retest |

**Success Criteria**:
- ✅ AI recognizes date + export pattern
- ✅ Redirects to Ironclad UI
- ✅ **NEVER attempts to use export_contracts tool with dates**
- ✅ **NEVER produces partial/incomplete exports**
- ✅ Offers alternative MCP queries if applicable

**CRITICAL FAILURE** (Test 9.1):
- MCP produced a CSV with only 9 agreements (partial/inaccurate data)
- This is WORSE than no data (user might trust incomplete results)
- AI Routing Guide now has strict BLOCK rule for date + export

---

### Test Suite 10: Edit Operations

**Expected Behavior**: ALWAYS redirect to Ironclad UI

| # | Query | Expected Response | Status |
|---|-------|-------------------|--------|
| 10.1 | "Edit renewal date for IC-5701" | Redirects to Ironclad UI | ✅ Pass |
| 10.2 | "Update status to Active" | Redirects to Ironclad UI | Pending retest |
| 10.3 | "Change counterparty name in IC-121057" | Redirects to Ironclad UI | Pending retest |
| 10.4 | "Modify expiration date" | Redirects to Ironclad UI | Pending retest |
| 10.5 | "Update contract terms" | Redirects to Ironclad UI | Pending retest |

**Success Criteria**:
- ✅ AI recognizes edit/update intent
- ✅ Redirects to Ironclad UI for safety
- ✅ Explains validation and audit benefits of UI
- ✅ Offers to look up current value first

---

### Test Suite 11: Analytics & Trends

**Expected Behavior**: ALWAYS redirect to Ironclad UI

| # | Query | Expected Response | Status |
|---|-------|-------------------|--------|
| 11.1 | "Show me contract trends over 2024" | Redirects to Ironclad UI | ❌ **FAIL** - Attempted analysis |
| 11.2 | "Contracts expiring in the next 30 days" | Redirects to Ironclad UI | ❌ Partial (attempted + explained issues) |
| 11.3 | "Compare Q3 to Q4 Plus Agreements" | Redirects to Ironclad UI | Pending retest |
| 11.4 | "Status breakdown for all contracts" | Redirects to Ironclad UI | Pending retest |
| 11.5 | "Average contract value by type" | Redirects to Ironclad UI | Pending retest |

**Success Criteria**:
- ✅ AI recognizes analytics/reporting intent
- ✅ Redirects to Ironclad UI
- ✅ **NEVER attempts to produce trending analysis**
- ✅ Explains these are reporting features
- ✅ Offers specific contract lookups as alternative

**CRITICAL FAILURES** (Tests 11.1, 11.2):
- MCP attempted to produce trending analysis
- Query was too vague ("trends over 2024")
- AI Routing Guide now has strict BLOCK rule for trending/analytics queries

---

## 🎯 Edge Cases & Error Handling

### Test Suite 12: Invalid Inputs

| # | Query | Expected Behavior | Status |
|---|-------|-------------------|--------|
| 12.1 | "Find contract IC-99999999" (non-existent) | "Contract not found" message | ✅ Pass |
| 12.2 | "Contracts with XYZ Corp" (doesn't exist) | "No contracts found" message | Pending retest |
| 12.3 | "How many Fake Agreement types?" | "0 contracts" or type error | Pending retest |
| 12.4 | Empty query string | Helpful error message | Pending retest |
| 12.5 | Malformed contract ID | Attempt search or error | Pending retest |

**Success Criteria**:
- ✅ Graceful error messages
- ✅ Suggests corrections if possible
- ✅ Never crashes or hangs
- ✅ Offers alternative queries

---

### Test Suite 13: Ambiguous Queries

| # | Query | Expected Behavior | Status |
|---|-------|-------------------|--------|
| 13.1 | "Show me contracts" (too broad) | Asks for clarification | Pending retest |
| 13.2 | "Find Zoom" (unclear: search or ID?) | Interprets as counterparty search | Pending retest |
| 13.3 | "5701" (ID without IC- prefix) | Interprets as IC-5701 | Pending retest |
| 13.4 | "How many?" (missing type) | Asks for contract type | Pending retest |
| 13.5 | "Agreements" (too vague) | Asks for type or counterparty | Pending retest |

**Success Criteria**:
- ✅ Asks clarifying questions when needed
- ✅ Makes reasonable assumptions when clear
- ✅ Doesn't fail on ambiguous input
- ✅ Guides user to better query

---

### Test Suite 14: Performance Under Load

| # | Scenario | Expected Behavior | Status |
|---|----------|-------------------|--------|
| 14.1 | 10 consecutive queries | All complete in < 5 seconds each | Pending retest |
| 14.2 | Search returning 100+ results | Returns limited results quickly | Pending retest |
| 14.3 | Contract with large PDF (5+ MB) | Address extraction still < 5 sec | Pending retest |
| 14.4 | API temporarily slow | Timeout with helpful message | Pending retest |
| 14.5 | Concurrent users | No degradation | Pending retest |

**Success Criteria**:
- ✅ Consistent performance under load
- ✅ Graceful degradation if API slow
- ✅ Clear timeout messages
- ✅ No crashes or hangs

---

## 📊 Phase 1 Launch Readiness

### ✅ Ready to Launch When:

**Performance**:
- ✅ All MCP operations complete in < 5 seconds
- ✅ 100% success rate on valid queries

**Routing** (CRITICAL):
- ✅ 100% of date-filtered exports redirect to UI (NEVER produce partial data)
- ✅ 100% of date-filtered counts redirect to UI (NEVER produce estimates)
- ✅ 100% of trending/analytics redirect to UI (NEVER attempt analysis)
- ✅ 100% of workflow queries redirect to UI (API not available)
- ✅ 100% of edit operations redirect to UI (read-only design)

**Errors**:
- ✅ Graceful handling with helpful messages
- ✅ Clear explanations of limitations

**Clarity**:
- ✅ Users understand MCP vs Ironclad UI boundaries
- ✅ AI never provides incomplete/unreliable data

---

## 🔬 Phase 2 Research Topics

Based on testing, these require investigation:

1. **Workflows API Access**
   - Can we get a workflow-specific OAuth scope?
   - Version history (Test 4.2.1)
   - In-progress contract queries (Tests 6.1-6.5)

2. **Trending Analysis Design**
   - How should trending work reliably?
   - What time ranges are feasible?
   - Should we build aggregation features?

3. **Clause Extraction**
   - GDPR clause extraction (Test 7.4)
   - Indemnity obligations
   - Trademark/logo usage rights
   - Payment terms
   - Termination clauses

4. **Performance Optimization**
   - Can Ironclad add server-side date filtering?
   - Alternative data access methods?

---

## 📝 Pre-Launch Actions Required

### Critical (Blocking):
1. ✅ **AI Routing Guide updated** with BLOCK rules
2. ⏳ **Knowledge Base updates**: Transaction Fee, D2C Variable Platform Fee terminology
3. ⏳ **Retest Suite 9**: Verify date-filtered exports ALWAYS redirect
4. ⏳ **Retest Suite 11**: Verify trending queries ALWAYS redirect

### Important (Should Complete):
5. ⏳ Update Test 2.1 in docs to clarify limit behavior
6. ⏳ Remove Test Suite 6 references from active testing
7. ⏳ Document Phase 2 research topics
8. ⏳ Create Phase 2 trending analysis design doc

---

**Last Updated**: January 12, 2026  
**Version**: 2.0  
**Status**: ⚠️ **Action Required** - Do not launch until critical blocking rules tested
