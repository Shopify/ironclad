# Shopify Ironclad Knowledge Base
## Complete Reference for Ironclad MCP

**Last Updated**: 2026-01-15  
**Version**: 1.1 (Added Marketing Rights)  
**Status**: Production

---

## 🎯 Purpose

This document provides the Ironclad MCP with essential context about Shopify's contract organization, terminology, and search strategies. Use this to understand user queries and translate them into correct API calls.

---

## 📋 Table of Contents

1. [Contract Organization](#contract-organization)
2. [Marketing Rights in Merchant Contracts](#marketing-rights-in-merchant-contracts)
3. [Record Types by Practice Area](#record-types-by-practice-area)
4. [Search Strategies](#search-strategies)
5. [Critical Fields Reference](#critical-fields-reference)
6. [Contract Families & Relationships](#contract-families--relationships)
7. [Common Queries & Examples](#common-queries--examples)

---

## Contract Organization

### Practice Area → Record Type → Document Type

Shopify organizes contracts in a three-tier hierarchy:

```
Practice Area (business categorization, context only)
  └─ Record Type (Ironclad template/workflow)
      └─ Document Type (specific template variant)
```

**Example**:
```
Revenue
  └─ Plus Agreement (Record Type: plusAgreement)
      ├─ Standard Plus Agreement
      ├─ Multi-Brand Agreement
      ├─ High Store Volume Agreement
      └─ NPO Agreement
```

---

## Marketing Rights in Merchant Contracts

**Context**: Shopify often needs to use merchant names and logos in marketing materials (case studies, success stories, testimonials, etc.). The marketing rights granted by merchants are captured in Plus Agreement metadata.

### Marketing Rights Field Values

**Applies To**: Plus Agreements, Plus Large Agreements, CCS for Enterprise

**Field Name**: `Marketing Rights` (or `marketingRights1_0e1fb205-c256-4efc-aa07-7eaf884b3dd9_string` in API)

**Possible Values**:

1. **Standard**
   - **Meaning**: Shopify can use merchant's name and logo in marketing materials without requiring explicit consent for each use
   - **Action**: ✅ Proceed with marketing use (within scope of agreement)
   - **Example Use**: "Fast-Fix Jewelry uses Shopify Plus to power their ecommerce"

2. **Meet in the Middle**
   - **Meaning**: Requires explicit consent from merchant before each use
   - **Action**: ⚠️ Contact merchant for approval before using name/logo
   - **Process**: Reach out via primary contact listed in contract

3. **Other**
   - **Meaning**: Custom/bespoke marketing rights arrangement
   - **Action**: 📄 Read the contract to understand specific terms
   - **Location**: Look for "Marketing Rights", "Publicity Rights", or "Use of Marks" sections

### Common Marketing Rights Questions

**Q**: "Can we use [merchant]'s logo in a case study?"  
**A**: Check the `Marketing Rights` field:
- **Standard** → Yes, proceed
- **Meet in the Middle** → Get approval first
- **Other** → Review contract for specifics

**Q**: "Can [vendor] use Shopify's logo in their materials?"  
**A**: Marketing rights for vendor use of Shopify's branding are **not** captured in metadata for Procurement Agreements. Must review contract manually (look for "Publicity Rights" or "Use of Marks" clauses).

### Why This Matters

- **Compliance**: Using merchant branding without proper rights could violate contract terms
- **Relationships**: Respecting marketing rights maintains good merchant relationships
- **Legal**: Trademark/IP considerations require clear documentation of usage rights

---

## Record Types by Practice Area

### 🟢 Revenue (Shopify Plus & Enterprise Contracts)

#### Plus Agreement (`plusAgreement`)
Standard Shopify Plus subscription contracts.

**Document Types**:
- **Standard Plus Agreement** (IC-5701) - Standard contracts
- **Multi-Brand Agreement** (IC-121364) - Multiple brands
- **High Store Volume Agreement** (IC-121001) - 25+ brands/stores
- **NPO Agreement** (IC-119262) - Non-profit pricing
- **Affiliate Plus Agreement** (IC-39561) - Has parentRecordID
- **MSA** (IC-14349) - Master agreement only

**Search Fields**: counterpartyName, brandName1, myShopifyUrl

---

#### Plus Large Accounts Agreement (`plusLargeAccountsAgreement`)
Large account Plus contracts.

**Document Types**:
- **Standard Plus Agreement** (IC-120483)
- **Multi-Brand Agreement** (IC-119257)
- **High Store Volume Agreement** (IC-117483)
- **MSA** (IC-17611)

**Search Fields**: counterpartyName, brandName1, myShopifyUrl

---

#### CCS for enterprise (`ccsForEnterprise`)
Enterprise-level customers (essentially Plus for Enterprise).

**Document Types**:
- **Standard CCS for enterprise Agreement** (IC-115185)
- **CCS for enterprise Amendment** (IC-104717) - Upgrade from Plus
- **Multi-Brand CCS for enterprise Agreement** (IC-105006)
- **CCS Master Subscription Agreement** - Has children

**Search Fields**: counterpartyName, brandName1, myShopifyUrl

---

#### CCS Components (`ccsComponents`)
Component-based enterprise contracts.

**Document Types**:
- **CCS Master Subscription Agreement** - MSA only
- **Shop Pay Component** (IC-116628) - Shop Pay only
- **Storefront Component** (IC-114297) - Storefront only
- **Checkout Component** - Checkout only

**Search Fields**: counterpartyName, brandName1, myShopifyUrl

---

#### Plus Renewal (`plusRenewal`)
Renewal amendments for Plus contracts.

**Document Types**:
- **Plus Renewal Amendment** (IC-121400) - Longer terms/better pricing
- **Plus TOS Amendment** (IC-120833) - TOS merchant renewals

**Search Fields**: counterpartyName

---

#### Plus Amending Agreement (`plusAmendingAgreement`)
General amendments to Plus contracts.

**Document Types**:
- **Plus Amending Agreement** (IC-116897) - General amendments
- **Automated 2024 Rate Lock Amendment** (IC-78577) - 3-year rate lock
- **2024 Rate Lock Amendment** (IC-60815) - Custom rate locks
- **Consent to Assignment** (IC-60930) - Assignment consent

**Search Fields**: counterpartyName

---

#### Plus Addenda (`plusAddenda`)
Addendums to Plus contracts.

**Document Types**:
- **Incremental Storage Fee Addendum** (IC-121285)
- **Change Order** (IC-120589) - Most common: name/address changes
- **AvaTax Addendum** (IC-771)
- **Shop Pay Conversion Addendum**
- **Additional Services Fee Addendum**

**Search Fields**: counterpartyName

---

#### Plus NDA (`plusNda`)
Non-Disclosure Agreements for potential Plus merchants.

**Document Types**:
- **Plus NDA** (IC-120692)

**Search Fields**: counterpartyName

---

### 🔵 Procurement (Vendor & Supplier Contracts)

#### Procurement Agreement (`procurementAgreement`)
Vendor/supplier contracts primarily for software, products, and services.

**Document Types**:
- **Master Services Agreement** (IC-95582) - Software vendors
- **MPA** (IC-117224) - Master Purchase Agreement for products
- **Agency Agreement** (IC-120161) - Services
- **Order Form** (IC-120977) - Has parentRecordID
- **SOW** (IC-121237) - Statement of Work, has parentRecordID
- **Recruiting Services Agreement** (IC-44303)
- **Sponsorship Agreement** (IC-120666)
- **Membership Agreement** (IC-50783)
- **Consulting Agreement** (IC-120352) - "External Workers"

**Search Fields**: counterpartyName

---

#### NDA (`NDA`)
Mutual Non-Disclosure Agreements.

**Document Types**:
- **Mutual Non-Disclosure Agreement** (IC-121309) - For vendors and partners

**Search Fields**: counterpartyName

---

### 🟣 Partnerships (Partner Program Agreements)

#### Partner Development Fund PPA Addendum (`partnerDevelopmentFundPpaAddendum`)
Partnership agreements for development funds.

**Document Types**:
- **Partner Development Fund PPA Addendum** (IC-121333)

**Note**: PPA = Partner Program Agreement (online terms, no Ironclad contract)

**Search Fields**: counterpartyName

---

#### Partner Marketing Addendum (`partnerMarketingAddendum`)
Partnership agreements for marketing funds.

**Document Types**:
- **Partner Marketing Addendum** (IC-121132)

**Search Fields**: counterpartyName

---

#### Partner Co-Marketing Addendum (`partnerCoMarketingAddendum`)
Co-marketing partnership agreements.

**Document Types**:
- **Co-Marketing Addendum to the Shopify Partner Program Agreement** (IC-121371)

**Search Fields**: counterpartyName

---

#### Other Partnership Types
- **Orders API PPA Addendum** (`ordersApiPpaAddendum`)
- **3PL Addendum to the PPA** (`3PlAddendumToThePpa`) - IC-114499
- **Flip the Base PPA Partner** (`flipTheBasePpaPartner`) - IC-120495
- **Alliance Partner LOI** (`alliancePartnerLoi`) - IC-121335
- **Strategic Product Partnership PPA Addendum** (`strategicProductPartnershipPpaAddendum`) - IC-106613
- **Strategic** (`strategic`) - Various MSA/Amendments - IC-117063
- **Sales Channel** (`salesChannel`) - Various - IC-118400

**All search by**: counterpartyName

---

## Search Strategies

### 🎯 Plus Agreements: Multiple Search Fields

**Critical Insight**: Plus Agreements can be searched by THREE different fields:

1. **Legal Business Name** (`counterpartyName`)
   - Example: "Gold Standard Media LLC"
   - Use when user provides legal entity name

2. **Brand Name** (`brandName1_af134335-06fa-4c91-954a-76b70c08adb4_string`)
   - Example: "Fast-Fix Jewelry & Watch Repairs"
   - Use when user mentions a brand or doing-business-as name

3. **Shopify URL** (`custome2e9166e97b6446f827926cdb3508de6_0e1fb205-c256-4efc-aa07-7eaf884b3dd9_string`)
   - Example: "caseboss.myshopify.com"
   - Use when user provides a myshopify.com URL

**When searching Plus Agreements, try all three fields to maximize chances of finding the contract.**

### Search by Ironclad ID (Fastest)

```python
# Direct lookup - fastest method (~0.5s)
GET /records/IC-5701
```

**When to use**: User provides specific Ironclad ID (IC-xxxxx format)

### Search by Counterparty (Fast)

```python
# Formula filter - fast (~0.5-2s)
GET /records?filter=Contains([counterpartyName], "Gold Standard")
```

**When to use**: User asks for contracts with specific company
**Note**: Partial matching works ("Gold Standard" finds "Gold Standard Media LLC")

### Search Plus by Brand/URL (Fast)

```python
# Try multiple fields for Plus contracts
Contains([brandName1_...], "Fast-Fix Jewelry")
Contains([custome2e...], "caseboss.myshopify.com")
```

**When to use**: User mentions brand name or Shopify URL for Plus contracts

---

## Critical Fields Reference

### Universal Fields (All Contracts)

| UI Name | API Field | Type | Description |
|---------|-----------|------|-------------|
| Counterparty Name | `counterpartyName` | string | Legal business name |
| Shopify Entity | `shopifyEntity_b6b03c00-e54d-4644-9b47-15c12d4809b7_string` | string | Which Shopify legal entity |
| Counterparty Contact Name | `contactNameCounterparty` | string | Primary contact name |
| Counterparty Contact Email | `counterpartyContactEmailAddress_0e1fb205-c256-4efc-aa07-7eaf884b3dd9_email` | email | Primary contact email |
| Effective Date | `effectiveDate` | date | Contract start date |
| Status | `status` | string | Active, Inactive, Expired, etc. |

### Term Fields (Most Contracts)

| UI Name | API Field | Type | Description |
|---------|-----------|------|-------------|
| Initial Term (months) | `initialTermMonths_648ebaad-410a-4699-b44d-3766a659e1f0_number` | number | Initial term length |
| Renewal Term (months) | `renewalTerm_648ebaad-410a-4699-b44d-3766a659e1f0_number` | number | Auto-renewal period |
| Agreement Renewal Date | `agreementRenewalDate` | date | Next renewal date |
| Notice for Non-Renewal | `noticeForNonRenewal_648ebaad-410a-4699-b44d-3766a659e1f0_number` | number | Days notice to cancel |

**Excluded from**: NDAs (Plus NDA, Mutual NDA)

### Revenue-Specific Fields (Plus Agreements)

| UI Name | API Field | Type | Description |
|---------|-----------|------|-------------|
| **My Shopify URL** ⭐ | `custome2e9166e97b6446f827926cdb3508de6_0e1fb205-c256-4efc-aa07-7eaf884b3dd9_string` | string | **SEARCHABLE** - Store URL |
| **Brand Name 1** ⭐ | `brandName1_af134335-06fa-4c91-954a-76b70c08adb4_string` | string | **SEARCHABLE** - Brand name |
| Minimum Platform Fee | `minimumPlatformFee_0e1fb205-c256-4efc-aa07-7eaf884b3dd9_monetaryAmount` | monetary | Minimum monthly fee |
| D2C Variable Platform Fee | `variablePlatformFee_af134335-06fa-4c91-954a-76b70c08adb4_number` | number | D2C fee % |
| B2B Variable Platform Fee | `b2BVariablePlatformFee_af134335-06fa-4c91-954a-76b70c08adb4_number` | number | B2B fee % |
| Retail Variable Platform Fee | `retailVariablePlatformFee_c8752c3e-80c4-4ba7-bc88-2c8e3c40f7d6_number` | number | Retail fee % |
| Transaction Fee | `custom948f83a18721475691fabc408560f0ae_0e1fb205-c256-4efc-aa07-7eaf884b3dd9_number` | number | Transaction fee % |
| Promo Type | `promoType_ce6836f1-59d9-4f29-8c61-c6f0ebda8707_string` | string | Promotional pricing |
| Customer Notice for Non-Renewal | `custom1d18db5e359541688df8a459b2555b6e_0e1fb205-c256-4efc-aa07-7eaf884b3dd9_number` | number | Customer notice days |

**Used by**: plusAgreement, plusLargeAccountsAgreement, ccsForEnterprise, ccsComponents

---

## Contract Families & Relationships

Some contracts have parent-child relationships via `parentRecordID`:

### Contracts with Parents (have parentRecordID)

- **Affiliate Plus Agreements** → parent is Standard Plus Agreement
- **Order Forms** → parent is governing contract (MSA/MPA/Agency Agreement)
- **SOWs** (Statements of Work) → parent is governing contract
- **Sales Orders for MSAs** → parent is the MSA

### Contracts with Children (referenced by parentRecordID)

- **MSAs** (Master Subscription Agreements) - children are Sales Orders
- **Governing Procurement Contracts** - children are Order Forms/SOWs
- **Standard Plus Agreements** - children are Affiliate Plus Agreements

**When searching for contract families, look for `parentRecordID` field in the contract properties.**

---

## Common Queries & Examples

### "Find Plus contracts with Gold Standard"
```
Strategy: search_plus_agreements("Gold Standard")
Will search:
  1. counterpartyName contains "Gold Standard"
  2. brandName1 contains "Gold Standard"
Result: IC-5701 (Gold Standard Media LLC)
```

### "Find contracts for caseboss.myshopify.com"
```
Strategy: search_plus_agreements("caseboss.myshopify.com")
Will search:
  1. counterpartyName (unlikely match)
  2. myShopifyUrl contains "caseboss.myshopify.com"
Result: Finds Plus Agreement by store URL
```

### "Find Fast-Fix Jewelry contracts"
```
Strategy: search_plus_agreements("Fast-Fix Jewelry")
Will search:
  1. counterpartyName contains "Fast-Fix"
  2. brandName1 contains "Fast-Fix Jewelry"
Result: IC-120483 (Jewelry Repair Enterprises with brand "Fast-Fix Jewelry")
```

### "Get contract IC-5701"
```
Strategy: Direct lookup
GET /records/IC-5701
Result: Immediate return (~0.5s)
```

### "Find Zoom contracts"
```
Strategy: search_records(counterparty="Zoom")
GET /records?filter=Contains([counterpartyName], "Zoom")
Result: IC-95582 (Zoom Video Communications Inc.)
```

### "Show me contracts expiring in 30 days"
```
Strategy: Fetch records, filter by agreementRenewalDate
Filter: agreementRenewalDate between today and today+30 days
Note: Requires fetching and client-side filtering
```

---

## API Limitations & Workarounds

### ❌ Cannot Enumerate by Record Type

**Problem**: `/records` list endpoint doesn't return certain record types (like plusAgreement) in pagination.

**Impact**: Cannot answer "How many Plus Agreements do we have?" via API

**Workaround**: Only support direct ID lookups for now

**Status**: Waiting for Ironclad support resolution

---

## Quick Reference: Record Type API Values

| UI Name | API Value |
|---------|-----------|
| Plus Agreement | `plusAgreement` |
| Plus Large Accounts Agreement | `plusLargeAccountsAgreement` |
| CCS for enterprise | `ccsForEnterprise` |
| CCS Components | `ccsComponents` |
| Plus Renewal | `plusRenewal` |
| Plus Amending Agreement | `plusAmendingAgreement` |
| Plus Addenda | `plusAddenda` |
| Plus NDA | `plusNda` |
| Procurement Agreement | `procurementAgreement` |
| NDA | `NDA` |
| Partner Development Fund PPA Addendum | `partnerDevelopmentFundPpaAddendum` |
| Partner Marketing Addendum | `partnerMarketingAddendum` |
| Partner Co-Marketing Addendum | `partnerCoMarketingAddendum` |
| Orders API PPA Addendum | `ordersApiPpaAddendum` |
| 3PL Addendum to the PPA | `3PlAddendumToThePpa` |
| Flip the Base PPA Partner | `flipTheBasePpaPartner` |
| Alliance Partner LOI | `alliancePartnerLoi` |
| Strategic Product Partnership PPA Addendum | `strategicProductPartnershipPpaAddendum` |
| Strategic | `strategic` |
| Sales Channel | `salesChannel` |

---

## Usage Guidelines for MCP

### When User Asks for Plus Contracts

1. **Check if they mention brand name or URL** → Use `search_plus_agreements()`
2. **If counterparty name only** → Use standard `search_records(counterparty=...)`
3. **If Ironclad ID** → Use direct lookup

### When User Asks for Procurement Contracts

1. **Use counterpartyName search** → Standard approach
2. **Check parentRecordID** → May need to fetch parent contract

### When User Asks About Terms/Renewals

1. **Fetch contract first**
2. **Extract term fields** from properties
3. **Return in user-friendly format** (e.g., "12 months" not "12")

---

## Maintenance

**To Update This Knowledge Base**:
1. Modify source CSVs in `/templates/`
2. Regenerate JSON files
3. Update this markdown document
4. Test search functionality
5. Deploy updated MCP

**Owner**: Grant Jackman  
**Review Frequency**: Quarterly or when new record types added

---

**End of Knowledge Base** 📚


