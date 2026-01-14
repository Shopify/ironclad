#!/usr/bin/env python3
"""
Lookup Record Information - Discovery Helper Script

Usage:
    python3 scripts/lookup_record_info.py IC-12345

This script helps discover API field names and values for Ironclad contracts.
Use it when filling out the knowledge base CSV templates.
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ironclad_mcp.ironclad_client import IroncladClient

# Set up environment
os.environ["GCP_PROJECT_ID"] = "shopify-contract-filing-automa"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(project_root / "service-account-key.json")
os.environ["IRONCLAD_BASE_URL"] = "https://na1.ironcladapp.com"
os.environ["IRONCLAD_USER_EMAIL"] = os.getenv("IRONCLAD_USER_EMAIL", "grant.jackman@shopify.com")

async def lookup_record(ironclad_id: str):
    """Look up record and display all relevant information."""
    
    client = IroncladClient()
    
    print("=" * 80)
    print(f"LOOKING UP: {ironclad_id}")
    print("=" * 80)
    
    try:
        results = await client.search_records(ironclad_id=ironclad_id)
        
        if not results:
            print(f"❌ Contract {ironclad_id} not found or no access")
            print("\nPossible reasons:")
            print("  • ID doesn't exist")
            print("  • No permission to access")
            print("  • Typo in Ironclad ID")
            return
        
        record = results[0]
        
        # Top-level information
        print(f"\n📋 RECORD INFORMATION")
        print("-" * 80)
        print(f"Ironclad ID:     {record.get('ironcladId')}")
        print(f"Name:            {record.get('name')}")
        print(f"Type (API):      {record.get('type')}")
        print(f"Record ID:       {record.get('id')}")
        print(f"Last Updated:    {record.get('lastUpdated')}")
        
        # CSV-ready output for record_types_template.csv
        props = record.get("properties", {})
        document_type = props.get("documentType", {}).get("value", "N/A")
        
        print(f"\n📝 FOR record_types_template.csv:")
        print("-" * 80)
        print(f"[YOUR PRACTICE AREA],{record.get('name', '').split(' with ')[0] if ' with ' in record.get('name', '') else 'UNKNOWN'},{record.get('type')},{document_type},{ironclad_id},Confirmed,")
        
        # Key properties
        print(f"\n📊 KEY PROPERTIES")
        print("-" * 80)
        
        key_fields = {
            "counterpartyName": "Counterparty Name",
            "status": "Status",
            "effectiveDate": "Effective Date",
            "agreementRenewalDate": "Agreement Renewal Date",
            "documentType": "Document Type",
            "templateType": "Template Type",
        }
        
        for api_field, display_name in key_fields.items():
            if api_field in props:
                value = props[api_field].get("value", "N/A")
                field_type = props[api_field].get("type", "unknown")
                print(f"  {display_name:25s}: {value} (type: {field_type})")
        
        # Term-related fields
        print(f"\n📅 TERM & RENEWAL FIELDS")
        print("-" * 80)
        
        term_fields = {}
        for key, value in props.items():
            if any(term in key.lower() for term in ["term", "renewal", "notice"]):
                term_fields[key] = value
        
        if term_fields:
            for api_field, value_obj in sorted(term_fields.items()):
                value = value_obj.get("value", "N/A")
                field_type = value_obj.get("type", "unknown")
                print(f"  {api_field:50s}: {value} ({field_type})")
        else:
            print("  (No term/renewal fields found)")
        
        # All properties (condensed view)
        print(f"\n📚 ALL PROPERTIES (first 50)")
        print("-" * 80)
        print(f"Total properties: {len(props)}")
        print()
        
        for i, (key, value_obj) in enumerate(sorted(props.items())[:50]):
            value = value_obj.get("value", "")
            field_type = value_obj.get("type", "unknown")
            
            # Truncate long values
            value_str = str(value)[:50]
            if len(str(value)) > 50:
                value_str += "..."
            
            print(f"  {key:50s}: {value_str:50s} ({field_type})")
        
        if len(props) > 50:
            print(f"\n  ... and {len(props) - 50} more properties")
        
        # Export full JSON for reference
        export_path = project_root / f"exports/{ironclad_id}_full_data.json"
        export_path.parent.mkdir(exist_ok=True)
        
        with open(export_path, 'w') as f:
            json.dump(record, f, indent=2)
        
        print(f"\n💾 Full record data exported to:")
        print(f"   {export_path}")
        
        print("\n" + "=" * 80)
        print("✅ LOOKUP COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error looking up record: {e}")
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/lookup_record_info.py IC-12345")
        print("\nThis script helps discover API field names and values.")
        print("Use it when filling out knowledge base CSV templates.")
        sys.exit(1)
    
    ironclad_id = sys.argv[1]
    
    # Validate format
    if not ironclad_id.startswith("IC-"):
        print(f"⚠️  Warning: '{ironclad_id}' doesn't look like an Ironclad ID")
        print("   Expected format: IC-12345")
        print("   Trying anyway...")
        print()
    
    asyncio.run(lookup_record(ironclad_id))

if __name__ == "__main__":
    main()


