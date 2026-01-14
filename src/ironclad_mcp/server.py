"""
Main MCP server for Ironclad integration
"""
import asyncio
import os
import json
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
from .ironclad_client import IroncladClient
from .auth import IroncladOAuthClient
from .gcp_secrets import GCPSecretProvider


# Initialize MCP server
app = Server("ironclad-mcp")

# Global client instance (initialized on first use)
_ironclad_client = None
_oauth_client = None

# Knowledge base directory
KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent.parent / "knowledge_base"


async def get_client() -> IroncladClient:
    """Get or create the Ironclad client"""
    global _ironclad_client, _oauth_client
    
    if _ironclad_client is None:
        # Get OAuth credentials from GCP Secret Manager
        secret_provider = GCPSecretProvider()
        creds = secret_provider.get_oauth_credentials()
        
        # Initialize OAuth client
        base_url = os.getenv("IRONCLAD_BASE_URL", "https://na1.ironcladapp.com")
        _oauth_client = IroncladOAuthClient(
            base_url=base_url,
            client_id=creds["client_id"],
            client_secret=creds["client_secret"]
        )
        
        # Get access token
        access_token = await _oauth_client.get_access_token()
        
        # Get user email for impersonation
        user_email = os.getenv("IRONCLAD_USER_EMAIL")
        if not user_email:
            raise ValueError("IRONCLAD_USER_EMAIL environment variable must be set")
        
        # Initialize Ironclad client
        timeout = int(os.getenv("IRONCLAD_API_TIMEOUT", "120"))
        _ironclad_client = IroncladClient(
            base_url=base_url,
            access_token=access_token,
            user_email=user_email,
            timeout=timeout
        )
    
    return _ironclad_client


@app.list_tools()
async def list_tools():
    """Define available MCP tools"""
    return [
        Tool(
            name="search_contracts",
            description="Search for contracts in Ironclad repository by counterparty name, record type, or keywords. Returns instant results.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (keywords in contract name)"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results to return (max 100)",
                        "default": 20
                    },
                    "ironclad_id": {
                        "type": "string",
                        "description": "Filter by Ironclad ID (e.g., 'IC-95582'). Better to use get_contract_details directly for known IDs."
                    },
                    "record_type": {
                        "type": "string",
                        "description": "Filter by record type (e.g., 'plusAgreement', 'procurementAgreement', 'nDA', etc.)"
                    },
                    "counterparty": {
                        "type": "string",
                        "description": "Filter by counterparty name (e.g., 'Zoom', 'Microsoft'). Supports partial matching."
                    }
                }
            }
        ),
        Tool(
            name="get_contract_details",
            description="Get detailed information about a specific contract including all metadata, dates, values, and status. Automatically detects and reports contract families and amendments.",
            inputSchema={
                "type": "object",
                "properties": {
                    "record_id": {
                        "type": "string",
                        "description": "The Ironclad ID (e.g., 'IC-5701') or UUID record ID. Ironclad IDs are preferred and easier to use."
                    }
                },
                "required": ["record_id"]
            }
        ),
        Tool(
            name="get_contract_attachments",
            description="List all attachments (documents) for a specific contract including file names, types, sizes, and upload dates.",
            inputSchema={
                "type": "object",
                "properties": {
                    "record_id": {
                        "type": "string",
                        "description": "The Ironclad ID (e.g., 'IC-5701') or UUID record ID"
                    }
                },
                "required": ["record_id"]
            }
        ),
        Tool(
            name="count_contracts",
            description="Count contracts matching search criteria. Fast for simple counts. For date-filtered counts (e.g., 'in December 2025'), this will be slower (20-30 seconds) as the API doesn't support date filtering.",
            inputSchema={
                "type": "object",
                "properties": {
                    "record_type": {
                        "type": "string",
                        "description": "Filter by record type (e.g., 'plusAgreement')"
                    },
                    "counterparty": {
                        "type": "string",
                        "description": "Filter by counterparty name"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (keywords)"
                    }
                }
            }
        ),
        Tool(
            name="search_workflows",
            description="Search for in-progress contracts (workflows) by counterparty, type, stage, or keywords. Returns workflows that are in draft, review, or signing stages. Use stage='Review' for approval queries (note: capitalized!).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (keywords in workflow name)"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results to return (max 100)",
                        "default": 20
                    },
                    "record_type": {
                        "type": "string",
                        "description": "Filter by workflow type (e.g., 'plusAgreement', 'procurementAgreement')"
                    },
                    "counterparty": {
                        "type": "string",
                        "description": "Filter by counterparty name. Supports partial matching."
                    },
                    "stage": {
                        "type": "string",
                        "description": "Filter by workflow stage (CAPITALIZED): 'Draft', 'Review' (for approval), 'Sign' (for signature)"
                    }
                }
            }
        ),
        Tool(
            name="get_workflow_details",
            description="Get detailed information about a specific in-progress contract (workflow) including status, participants, and current stage.",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_id": {
                        "type": "string",
                        "description": "The workflow ID (UUID) or Ironclad ID (e.g., 'IC-5701')"
                    }
                },
                "required": ["workflow_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls"""
    client = await get_client()
    
    try:
        if name == "search_contracts":
            # Handle ironclad_id searches separately (more efficient lookup)
            if arguments.get("ironclad_id"):
                ironclad_id = arguments["ironclad_id"]
                search_result = await client.search_records(
                    query=ironclad_id,
                    page_size=arguments.get("limit", 20),
                    page=0
                )
                records = search_result.get("records", [])
            else:
                search_result = await client.search_records(
                    query=arguments.get("query"),
                    page_size=arguments.get("limit", 20),
                    page=0,
                    record_type=arguments.get("record_type"),
                    counterparty=arguments.get("counterparty")
                )
                records = search_result.get("records", [])
            
            if not records:
                return [TextContent(
                    type="text",
                    text="No contracts found matching your search."
                )]
            
            result_text = f"Found {len(records)} contracts:\n\n"
            for record in records:
                props = record.get('properties', {})
                counterparty_name = props.get('counterpartyName', {}).get('value', 'N/A')
                
                result_text += f"**{record.get('name', 'Unnamed Contract')}**\n"
                result_text += f"  Ironclad ID: {record.get('ironcladId', 'N/A')}\n"
                result_text += f"  Counterparty: {counterparty_name}\n"
                result_text += f"  Type: {record.get('type', 'N/A')}\n"
                result_text += f"  Record ID: {record.get('id')}\n\n"
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "get_contract_details":
            try:
                import sys
                record_id = arguments["record_id"]
                print(f"\n🎯🎯🎯 get_contract_details called with record_id={record_id}", file=sys.stderr, flush=True)
                
                # Fetch the record directly (works with both IC-5701 format and UUID)
                record = await client.get_record(record_id)
                props = record.get('properties', {})
            
                # Helper function to extract property values
                def get_prop(key):
                    prop = props.get(key, {})
                    if isinstance(prop, dict) and 'value' in prop:
                        val = prop['value']
                        # Format monetary amounts
                        if isinstance(val, dict) and 'amount' in val and 'currency' in val:
                            return f"{val['currency']} {val['amount']:,.2f}"
                        return val
                    return None
                
                result_text = f"# {record.get('name', 'Contract Details')}\n\n"
                result_text += f"**Ironclad ID:** {record.get('ironcladId', 'N/A')}\n"
                result_text += f"**Record ID:** {record.get('id')}\n"
                result_text += f"**Type:** {record.get('type', 'N/A')}\n"
                
                # Extract key contract details
                if get_prop('counterpartyName'):
                    result_text += f"**Counterparty:** {get_prop('counterpartyName')}\n"
                
                if get_prop('status'):
                    result_text += f"**Status:** {get_prop('status')}\n"
                
                if get_prop('contractValue'):
                    result_text += f"**Contract Value:** {get_prop('contractValue')}\n"
                
                if get_prop('effectiveDate'):
                    result_text += f"**Effective Date:** {get_prop('effectiveDate')}\n"
                
                # Try multiple field patterns for agreement end date
                end_date = get_prop('agreementEndDate') or get_prop('agreementEndDate_b6b03c00-e54d-4644-9b47-15c12d4809b7_date')
                if end_date:
                    result_text += f"**Agreement End Date:** {end_date}\n"
                
                if get_prop('workflowCreatedDate'):
                    result_text += f"**Created:** {get_prop('workflowCreatedDate')}\n"
                
                if record.get('lastUpdated'):
                    result_text += f"**Last Modified:** {record.get('lastUpdated')}\n"
                
                # Check for completed date in multiple possible field names
                completed_date = (get_prop('workflowCompletedDate') or 
                                get_prop('workflowProcessAttributes_workflowCompletedDate'))
                if completed_date:
                    result_text += f"**Completed:** {completed_date}\n"
                
                # Add document type and paper source
                if get_prop('documentType'):
                    result_text += f"**Document Type:** {get_prop('documentType')}\n"
                
                if get_prop('paperSource'):
                    result_text += f"**Paper Source:** {get_prop('paperSource')}\n"
                
                # Add attachments if present
                if 'attachments' in record and record['attachments']:
                    result_text += f"\n**Attachments:**\n"
                    for att_name, att_info in record['attachments'].items():
                        if isinstance(att_info, dict):
                            filename = att_info.get('filename', att_name)
                            result_text += f"  - {filename}\n"
                
                # FIRST: Extract and display term-related fields prominently
                import re
                import sys
                
                # DEBUG: Log all property keys
                print(f"\n🔍 DEBUG: Contract {record.get('ironcladId')} has {len(props)} properties", file=sys.stderr, flush=True)
                print(f"🔍 DEBUG: Property keys: {list(props.keys())[:10]}...", file=sys.stderr, flush=True)  # First 10 keys
                
                # Check for specific known term fields
                initial_term = get_prop('initialTermMonths_648ebaad-410a-4699-b44d-3766a659e1f0_number')
                renewal_term = get_prop('renewalTerm_648ebaad-410a-4699-b44d-3766a659e1f0_number')
                
                print(f"🔍 DEBUG: initial_term = {initial_term}", file=sys.stderr, flush=True)
                print(f"🔍 DEBUG: renewal_term = {renewal_term}", file=sys.stderr, flush=True)
                
                # Also check for other term-related fields
                term_keywords = ['term', 'renewal', 'duration', 'period', 'expir']
                term_fields = []
                clause_fields = []
                
                for field_key, field_value in props.items():
                    val = get_prop(field_key)
                    if val is not None and val != '' and val != []:
                        # Check if it's a term-related field
                        if any(keyword in field_key.lower() for keyword in term_keywords):
                            # Separate clause text from structured data
                            if field_key.startswith('clause_'):
                                clause_fields.append((field_key, field_value))
                            else:
                                term_fields.append((field_key, val))
                
                # Display structured term fields prominently
                if initial_term or renewal_term or term_fields:
                    result_text += f"\n**📅 Contract Terms & Renewal:**\n"
                    
                    # Display known fields first with clean labels
                    if initial_term is not None:
                        result_text += f"  - **Initial Term:** {initial_term} months\n"
                    
                    if renewal_term is not None:
                        result_text += f"  - **Renewal Term:** {renewal_term} months\n"
                    
                    # Display other term-related fields
                    for field_key, val in term_fields:
                        # Skip the fields we already displayed
                        if field_key in ['initialTermMonths_648ebaad-410a-4699-b44d-3766a659e1f0_number', 
                                         'renewalTerm_648ebaad-410a-4699-b44d-3766a659e1f0_number']:
                            continue
                        
                        # Create readable name
                        clean_name = field_key
                        # Remove UUID suffix
                        clean_name = re.sub(r'_[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}_\w+$', '', clean_name)
                        # Convert to Title Case
                        clean_name = re.sub(r'([A-Z])', r' \1', clean_name).strip()
                        clean_name = clean_name.replace('_', ' ')
                        clean_name = ' '.join(word.capitalize() for word in clean_name.split())
                        
                        # Format value with units
                        if isinstance(val, (int, float)) and 'term' in field_key.lower():
                            # Likely months
                            result_text += f"  - **{clean_name}:** {val} months\n"
                        elif isinstance(val, (int, float)) and 'days' in field_key.lower():
                            result_text += f"  - **{clean_name}:** {val} days\n"
                        else:
                            result_text += f"  - **{clean_name}:** {val}\n"
                
                # Display clause-based term information (AI-extracted text)
                if clause_fields:
                    result_text += f"\n**📜 Contract Clauses (AI-Extracted):**\n"
                    for field_key, field_value in clause_fields:
                        if isinstance(field_value, dict) and 'value' in field_value:
                            clause_data = field_value['value']
                            if isinstance(clause_data, dict) and 'clauseText' in clause_data:
                                # Format clause name
                                clause_name = field_key.replace('clause_', '').replace('-', ' ').title()
                                clause_text = clause_data['clauseText']
                                # Truncate very long clause text
                                if len(clause_text) > 300:
                                    clause_text = clause_text[:300] + "..."
                                result_text += f"  - **{clause_name}:**\n"
                                result_text += f"    {clause_text}\n\n"
                
                # DEBUG: Show sample of available property keys
                all_keys = list(props.keys())
                if len(all_keys) > 0:
                    result_text += f"\n**🔍 DEBUG - Available Properties ({len(all_keys)} total):**\n"
                    result_text += f"First 20 property keys:\n"
                    for i, key in enumerate(all_keys[:20], 1):
                        result_text += f"  {i}. `{key}`\n"
                    if len(all_keys) > 20:
                        result_text += f"  ... and {len(all_keys) - 20} more\n"
                    
                # Display all available properties (not already shown above)
                result_text += f"\n**📋 Additional Contract Properties:**\n"
                
                # Fields already displayed - skip these to avoid duplication
                displayed_fields = {
                    'counterpartyName', 'status', 'contractValue', 'effectiveDate',
                    'agreementEndDate', 'agreementEndDate_b6b03c00-e54d-4644-9b47-15c12d4809b7_date',
                    'workflowCreatedDate', 'workflowCompletedDate', 
                    'workflowProcessAttributes_workflowCompletedDate',
                    'documentType', 'paperSource'
                }
                
                # Add all term-related fields to skip list (already shown prominently)
                for field_key, _ in term_fields:
                    displayed_fields.add(field_key)
                for field_key, _ in clause_fields:
                    displayed_fields.add(field_key)
                
                # Helper to format field names for display
                def format_field_name(field_key):
                    # Remove UUID suffixes
                    import re
                    clean_key = re.sub(r'_[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}_\w+$', '', field_key)
                    # Convert camelCase to Title Case with spaces
                    clean_key = re.sub(r'([A-Z])', r' \1', clean_key).strip()
                    # Convert snake_case to spaces
                    clean_key = clean_key.replace('_', ' ')
                    # Capitalize words
                    return ' '.join(word.capitalize() for word in clean_key.split())
                
                # Collect and sort all properties
                all_properties = []
                for field_key, field_value in props.items():
                    if field_key not in displayed_fields:
                        val = get_prop(field_key)
                        if val is not None and val != '' and val != []:
                            formatted_name = format_field_name(field_key)
                            all_properties.append((formatted_name, val))
                
                # Sort alphabetically for easier scanning
                all_properties.sort(key=lambda x: x[0])
                
                # Display all properties
                if all_properties:
                    for field_label, val in all_properties:
                        # Handle lists
                        if isinstance(val, list):
                            val_str = ', '.join(str(v) for v in val)
                            result_text += f"  - {field_label}: {val_str}\n"
                        # Handle dicts
                        elif isinstance(val, dict):
                            # Skip complex nested objects, just show simple ones
                            if len(str(val)) < 100:
                                result_text += f"  - {field_label}: {val}\n"
                        else:
                            result_text += f"  - {field_label}: {val}\n"
                else:
                    result_text += "  No additional properties found.\n"
                
                return [TextContent(type="text", text=result_text)]
            
            except Exception as e:
                import traceback
                error_msg = f"❌ Error retrieving contract details: {str(e)}\n\n"
                error_msg += f"**Error Type:** {type(e).__name__}\n"
                error_msg += f"**Details:** {traceback.format_exc()}\n"
                print(f"❌ ERROR in get_contract_details: {e}", file=sys.stderr, flush=True)
                print(traceback.format_exc(), file=sys.stderr, flush=True)
                return [TextContent(type="text", text=error_msg)]
        
        elif name == "get_contract_attachments":
            record_id = arguments["record_id"]
            
            # Fetch attachments directly (works with both IC-5701 format and UUID)
            attachments = await client.get_record_attachments(record_id)
            
            if not attachments:
                return [TextContent(
                    type="text",
                    text="No attachments found for this contract."
                )]
            
            result_text = f"Found {len(attachments)} attachment(s):\n\n"
            for att in attachments:
                result_text += f"**{att.get('name', 'Unnamed File')}**\n"
                result_text += f"  ID: {att.get('id')}\n"
                result_text += f"  Type: {att.get('mimeType', 'N/A')}\n"
                result_text += f"  Size: {att.get('size', 'N/A')} bytes\n"
                result_text += f"  Uploaded: {att.get('createdAt', 'N/A')}\n\n"
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "count_contracts":
            count = await client.count_records(
                query=arguments.get("query"),
                record_type=arguments.get("record_type"),
                counterparty=arguments.get("counterparty")
            )
            
            result_text = f"Found {count:,} contracts"
            if arguments.get("record_type"):
                result_text += f" of type '{arguments['record_type']}'"
            if arguments.get("counterparty"):
                result_text += f" with counterparty '{arguments['counterparty']}'"
            result_text += "."
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "search_workflows":
            search_result = await client.search_workflows(
                query=arguments.get("query"),
                record_type=arguments.get("record_type"),
                counterparty=arguments.get("counterparty"),
                stage=arguments.get("stage"),
                page_size=arguments.get("limit", 20),
                page=0
            )
            
            workflows = search_result.get("workflows", [])
            total = search_result.get("total", 0)
            
            if not workflows:
                return [TextContent(
                    type="text",
                    text="No in-progress contracts found matching your search."
                )]
            
            result_text = f"Found {len(workflows)} in-progress contract(s)"
            if total > len(workflows):
                result_text += f" (showing {len(workflows)} of {total} total)"
            result_text += ":\n\n"
            
            for wf in workflows:
                wf_id = wf.get('ironcladId', wf.get('id'))
                wf_name = wf.get('title') or wf.get('name', 'Unnamed Workflow')
                wf_type = wf.get('type', 'N/A')
                
                # Get workflow stage and status
                # API uses 'step' for stage (e.g., 'Sign', 'Review', 'Draft')
                wf_stage = wf.get('step', 'N/A')
                wf_status = wf.get('status', 'N/A')
                
                # Get counterparty from attributes (workflows use 'attributes', not 'properties')
                attrs = wf.get('attributes', {})
                counterparty = attrs.get('counterpartyName', 'N/A')
                
                result_text += f"**{wf_id}** - {wf_name}\n"
                result_text += f"  Type: {wf_type}\n"
                result_text += f"  Stage: {wf_stage}\n"
                result_text += f"  Status: {wf_status}\n"
                result_text += f"  Counterparty: {counterparty}\n\n"
            
            return [TextContent(type="text", text=result_text)]
        
        elif name == "get_workflow_details":
            import sys
            workflow_id = arguments["workflow_id"]
            print(f"\n🎯 get_workflow_details called with workflow_id={workflow_id}", file=sys.stderr, flush=True)
            
            try:
                workflow = await client.get_workflow(workflow_id)
                print(f"✅ Successfully retrieved workflow {workflow_id}", file=sys.stderr, flush=True)
            except Exception as e:
                print(f"❌ Error retrieving workflow: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
                import traceback
                traceback.print_exc(file=sys.stderr)
                raise
            
            # Build detailed workflow information
            wf_id = workflow.get('ironcladId', workflow.get('id'))
            wf_name = workflow.get('title') or workflow.get('name', 'Unnamed Workflow')
            wf_type = workflow.get('type', 'N/A')
            # API uses 'step' for stage and 'status' for status
            wf_stage = workflow.get('step', 'N/A')
            wf_status = workflow.get('status', 'N/A')
            
            result_text = f"# {wf_name}\n\n"
            result_text += f"**Workflow ID:** {wf_id}\n"
            result_text += f"**Type:** {wf_type}\n"
            result_text += f"**Current Stage:** {wf_stage}\n"
            result_text += f"**Status:** {wf_status}\n\n"
            
            # Get attributes (workflows use 'attributes', not 'properties')
            attrs = workflow.get('attributes', {})
            
            # Key fields
            counterparty = attrs.get('counterpartyName')
            created_date = workflow.get('created', 'N/A')
            updated_date = workflow.get('lastUpdated', 'N/A')
            
            if counterparty:
                result_text += f"**Counterparty:** {counterparty}\n"
            result_text += f"**Created:** {created_date}\n"
            result_text += f"**Last Updated:** {updated_date}\n\n"
            
            # Participants
            participants = workflow.get('participants', [])
            if participants:
                result_text += "## Participants\n"
                for p in participants:
                    if isinstance(p, dict):
                        p_name = p.get('name', p.get('email', 'Unknown'))
                        p_role = p.get('role', 'N/A')
                        result_text += f"- {p_name} ({p_role})\n"
                    else:
                        # Handle string or other formats
                        result_text += f"- {str(p)}\n"
                result_text += "\n"
            
            # Approvals if present
            approvals = workflow.get('approvals', [])
            if approvals:
                result_text += "## Approvals\n"
                for approval in approvals:
                    # Handle both string and dict formats
                    if isinstance(approval, str):
                        # If it's a string, just display it
                        result_text += f"- {approval}\n"
                    elif isinstance(approval, dict):
                        # If it's a dict, extract details
                        approver = approval.get('approver', {})
                        if isinstance(approver, dict):
                            approver_name = approver.get('email', approver.get('name', 'Unknown'))
                        else:
                            approver_name = str(approver)
                        approval_status = approval.get('status', 'Pending')
                        result_text += f"- {approver_name}: {approval_status}\n"
                    else:
                        # Unknown format, just convert to string
                        result_text += f"- {str(approval)}\n"
                result_text += "\n"
            
            # Turn history / comments
            comments = workflow.get('comments', [])
            if comments:
                result_text += f"## Recent Activity ({len(comments)} comment(s))\n"
                for comment in comments[:5]:  # Show first 5
                    if isinstance(comment, dict):
                        author = comment.get('author', {})
                        if isinstance(author, dict):
                            author_name = author.get('email', author.get('name', 'Unknown'))
                        else:
                            author_name = str(author)
                        comment_text = comment.get('text', '')
                        comment_date = comment.get('createdAt', '')
                        result_text += f"- **{author_name}** ({comment_date}): {comment_text[:100]}\n"
                    else:
                        # Handle string or other formats
                        result_text += f"- {str(comment)[:100]}\n"
                if len(comments) > 5:
                    result_text += f"\n... and {len(comments) - 5} more comments\n"
                result_text += "\n"
            
            return [TextContent(type="text", text=result_text)]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        import traceback
        import sys
        error_msg = f"❌ **Error calling tool '{name}'**\n\n"
        error_msg += f"**Error Type:** {type(e).__name__}\n"
        error_msg += f"**Error Message:** {str(e)}\n\n"
        error_msg += f"**Stack Trace:**\n```\n{traceback.format_exc()}\n```\n"
        
        # Log to stderr for debugging
        print(f"\n❌ EXCEPTION in call_tool '{name}':", file=sys.stderr, flush=True)
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        
        return [TextContent(
            type="text",
            text=error_msg
        )]


@app.list_resources()
async def list_resources():
    """
    List available knowledge base resources.
    
    These resources provide context about Shopify's Ironclad instance organization.
    NOTE: This is a CONTEXT GUIDE ONLY - not an exhaustive field list.
    Many more fields exist beyond what's documented here.
    """
    return [
        Resource(
            uri="knowledge://shopify-ironclad/overview",
            name="Shopify Ironclad Knowledge Base - Overview",
            description="Complete reference guide for Shopify's contract organization. Covers 24 record types across Revenue, Procurement, and Partnerships practice areas. NOTE: Context guide only - additional fields exist beyond those documented.",
            mimeType="text/markdown"
        ),
        Resource(
            uri="knowledge://shopify-ironclad/record-types",
            name="Record Types Reference (JSON)",
            description="Machine-readable mapping of practice areas, record types, and document types. Includes search field configurations. Context guide - not exhaustive.",
            mimeType="application/json"
        ),
        Resource(
            uri="knowledge://shopify-ironclad/critical-fields",
            name="Critical Fields Reference (JSON)",
            description="Key fields used for search and display. Includes universal, term, and revenue-specific fields. Context guide - many additional fields exist per record type.",
            mimeType="application/json"
        )
    ]


@app.read_resource()
async def read_resource(uri: str):
    """
    Read and return knowledge base resources.
    
    These provide context about Shopify's contract organization but are NOT exhaustive.
    Use them as a guide to understand structure and search strategies.
    """
    if uri == "knowledge://shopify-ironclad/overview":
        kb_path = KNOWLEDGE_BASE_DIR / "SHOPIFY_IRONCLAD_KNOWLEDGE_BASE.md"
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add disclaimer at the top
            disclaimer = """
> **IMPORTANT**: This knowledge base is a CONTEXT GUIDE ONLY.
> It documents critical fields and common search patterns but is NOT exhaustive.
> Many additional fields exist for each record type beyond those listed here.
> Use this to understand organization and search strategies, not as a complete field dictionary.

---

"""
            return content + disclaimer if not content.startswith(">") else content
            
        except FileNotFoundError:
            return "Knowledge base file not found. Please ensure knowledge_base directory exists."
    
    elif uri == "knowledge://shopify-ironclad/record-types":
        kb_path = KNOWLEDGE_BASE_DIR / "record_types.json"
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Add metadata disclaimer
            if 'metadata' not in data:
                data['metadata'] = {}
            data['metadata']['disclaimer'] = "Context guide only - not an exhaustive list of all record types or document types"
            
            return json.dumps(data, indent=2)
        except FileNotFoundError:
            return json.dumps({"error": "Record types file not found"})
    
    elif uri == "knowledge://shopify-ironclad/critical-fields":
        kb_path = KNOWLEDGE_BASE_DIR / "critical_fields.json"
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Add metadata disclaimer
            if 'metadata' not in data:
                data['metadata'] = {}
            data['metadata']['disclaimer'] = "Context guide only - many additional fields exist per record type beyond those documented here"
            
            return json.dumps(data, indent=2)
        except FileNotFoundError:
            return json.dumps({"error": "Critical fields file not found"})
    
    else:
        return f"Unknown resource URI: {uri}"


def main():
    """Entry point for the MCP server"""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def run_server():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(run_server())


if __name__ == "__main__":
    main()



