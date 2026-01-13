# 🔍 Ironclad API Discovery - Field Names & Filtering

## ✅ BREAKTHROUGH: API Response Format

###Wrong Field Names (What We Expected)
- `total` → ❌ Doesn't exist
- `records` → ❌ Doesn't exist

### ✅ Correct Field Names (What API Returns)
- `count` → Total number of matching records
- `list` → Array of record objects

**Fix Applied**: Updated `ironclad_client.py` to normalize API responses

---

## 📊 API Capabilities Discovered

### ✅ What Works
1. **GET `/records`** - Returns all records
   - Total: 107,673 records
   - Default page size: 20
   - Returns: `{count: number, list: array, page: number, pageSize: number}`

2. **GET `/records/{id}`** - Direct lookup by ID
   - Works perfectly
   - Returns full record details

3. **Pagination**
   - `page` parameter works
   - `limit` parameter is IGNORED (always returns 20)

### ❌ What Doesn't Work
1. **Query Parameters for Filtering**
   - `?type=plusAddenda` → IGNORED (returns all types)
   - `?counterpartyName=Zoom` → IGNORED (returns all)
   - `?limit=100` → IGNORED (always returns 20)

2. **Filter Expressions**
   - `?filter=Equals([type], "plusAddenda")` → 400 Bad Request
   - `?filter=Equals(type, "plusAddenda")` → 400 Bad Request ("unknown")
   - `?filter=type=plusAddenda` → 400 Bad Request ("unknown")

---

## 📝 Record Structure Discoveries

### Top-Level Fields
```json
{
  "id": "uuid",
  "ironcladId": "IC-12345",
  "type": "plusAddenda",
  "name": "Agreement title",
  "lastUpdated": "timestamp",
  "properties": {...},
  "attachments": {...},
  "source": "...",
  "links": {...},
  "childIds": [...]
}
```

### Properties Structure
Properties are nested objects with `type` and `value`:
```json
{
  "counterpartyName": {
    "type": "string",
    "value": "FLOWER POWER PTY LTD"
  },
  "effectiveDate": {
    "type": "date",
    "value": "2025-12-31"
  }
}
```

### Record Types (Observed)
Plus-related types:
- `plusAddenda`
- `plusAmendingAgreement`
- `plusRenewal`

Other types:
- `alliancePartnerLoi`
- `consultantAgreement`
- `nDA`
- `partnerCoMarketingAddendum`
- `procurementAgreement`
- `strategic`
- `imported`
- (many more...)

**Update**: Found IC-5701 with type `plusAgreement` (camelCase). **Known to have 40,000+ Plus Agreements in system**, but sampling first 500 records found only 5 (1%), indicating records are sorted in unknown order.

⚠️ **This makes client-side filtering unreliable** - must scan ALL 107,673 records to get accurate counts.

Related types also exist:
- `plusAddenda` - Change orders/addenda to Plus Agreements
- `plusAmendingAgreement` - Amendments
- `plusRenewal` - Renewals

---

## 🤔 Questions for Ironclad Support

1. **How to filter `/records` endpoint?**
   - Query parameters are ignored
   - Filter expressions return 400 errors
   - Is there a working filter syntax?

2. **Is there a search endpoint that supports filtering?**
   - `/records/search` → 403 Forbidden (missing scopes)
   - What scopes are needed for search?

3. **How to paginate efficiently?**
   - `limit` parameter is ignored
   - Fixed 20 records per page
   - Is there a way to increase page size?

4. **What are the correct type values for "Plus Agreements"?**
   - User asks about "Plus Agreement"
   - We see: `plusAddenda`, `plusAmendingAgreement`, `plusRenewal`
   - Are these the correct types, or is there a parent type?

---

## 🚀 Current Status

**What's Fixed**:
- ✅ Field name normalization (`count`/`list` → `total`/`records`)
- ✅ User impersonation header working
- ✅ Direct ID lookups working

**What's Blocked**:
- ❌ Filtering by type
- ❌ Filtering by counterparty
- ❌ Searching by keywords
- ❌ Counting specific record types
- ❌ Date-filtered queries (requires filtering first)

**Impact**:
- Can't answer "How many Plus Agreements?" (Known: 40,000+, but API can't tell us)
- Can't answer "Find contracts with Zoom"
- Can't reliably sample or estimate (unknown sort order)
- MCP limited to lookups by known IDs only
- **Both a performance issue AND an accuracy issue**

