"""
Ironclad API Client with pagination, date filtering, and search capabilities
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

import httpx

from .date_utils import DateParser

logger = logging.getLogger(__name__)


class IroncladClient:
    """Client for interacting with Ironclad API"""
    
    def __init__(
        self,
        base_url: str,
        access_token: str,
        user_email: str,
        timeout: int = 120
    ):
        """
        Initialize the Ironclad client
        
        Args:
            base_url: Base URL for Ironclad API (e.g., https://na1.ironcladapp.com)
            access_token: OAuth access token
            user_email: Email address for user impersonation (X-As-User-Email header)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self.user_email = user_email
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-As-User-Email": user_email
            }
        )
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.client.aclose()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def search_records(
        self,
        query: Optional[str] = None,
        record_type: Optional[str] = None,
        counterparty: Optional[str] = None,
        status_filter: Optional[str] = None,
        parent_record_id: Optional[str] = None,
        page_size: int = 100,
        page: int = 0
    ) -> Dict:
        """
        Search for records using Ironclad's Records API
        
        Per Ironclad Support (Jan 2026):
        - Use 'types' query param for record type filtering
        - Use 'filter' param with syntax: (Equals([field], "value"))
        - Use 'page' and 'pageSize' for pagination (max pageSize: 100)
        - Date filtering NOT supported - must filter client-side
        
        Args:
            query: Free-text search query (searches in name field)
            record_type: Type of record (e.g., 'plusAgreement')
            counterparty: Counterparty company name
            status_filter: Workflow status filter (e.g., 'Active')
            parent_record_id: Search for child contracts with this parent ID
            page_size: Number of results per page (max 100)
            page: Page number (0-indexed)
        
        Returns:
            Dict with 'total' (count) and 'records' (list)
        """
        url = f"{self.base_url}/public/api/v1/records"
        
        # Build parameters
        params = {
            "page": page,
            "pageSize": min(page_size, 100)  # Max 100 per Ironclad
        }
        
        # Add record type filter using 'types' param (per Ironclad docs)
        if record_type:
            params["types"] = record_type
        
        # Build filter expressions (must wrap entire expression in parentheses)
        filters = []
        
        if parent_record_id:
            filters.append(f'Equals([parentRecordID], "{parent_record_id}")')
        
        if query:
            filters.append(f'Contains([name], "{query}")')
        
        if counterparty:
            # Use Contains for partial matching (case-insensitive per Ironclad)
            filters.append(f'Contains([counterpartyName], "{counterparty}")')
        
        if status_filter:
            filters.append(f'Equals([workflowStatus], "{status_filter}")')
        
        # Combine filters with AND and wrap in parentheses
        if filters:
            if len(filters) == 1:
                params["filter"] = f'({filters[0]})'
            else:
                params["filter"] = f'(And({", ".join(filters)}))'
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # API returns 'count' and 'list', normalize to 'total' and 'records'
            return {
                "total": data.get("count", 0),
                "records": data.get("list", [])
            }
        except httpx.HTTPError as e:
            logger.error(f"Error searching records: {e}")
            raise
    
    async def get_record(self, record_id: str) -> Dict:
        """
        Get a single record by ID
        
        Args:
            record_id: The record ID (ironcladId or UUID)
        
        Returns:
            Dict containing record data
        """
        url = f"{self.base_url}/public/api/v1/records/{record_id}"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching record {record_id}: {e}")
            raise
    
    async def count_records(
        self,
        query: Optional[str] = None,
        record_type: Optional[str] = None,
        counterparty: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> int:
        """
        Count records matching search criteria (fast, no date filtering)
        
        Args:
            query: Free-text search query
            record_type: Type of record (e.g., 'plusAgreement')
            counterparty: Counterparty company name
            status_filter: Workflow status filter (e.g., 'Active')
        
        Returns:
            Total count of matching records
        """
        result = await self.search_records(
            query=query,
            record_type=record_type,
            counterparty=counterparty,
            status_filter=status_filter,
            page_size=1,
            page=0
        )
        return result.get("total", 0)
    
    async def fetch_all_records(
        self,
        record_type: Optional[str] = None,
        query: Optional[str] = None,
        counterparty: Optional[str] = None,
        status_filter: Optional[str] = None,
        date_field: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        progress_callback=None
    ) -> List[Dict]:
        """
        Fetch ALL records and filter by date client-side (SLOW for large datasets)
        
        This method is necessary because Ironclad's API doesn't support
        server-side date filtering on the /records endpoint.
        
        Args:
            record_type: Type of record to fetch
            query: Free-text search query
            counterparty: Counterparty company name
            status_filter: Workflow status filter
            date_field: Date field to filter on (e.g., 'effectiveDate')
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format
            progress_callback: Optional callback function for progress updates
        
        Returns:
            List of records matching the criteria
        """
        # Parse dates if provided (using consistent date parser)
        date_from_obj = None
        date_to_obj = None
        
        if date_field and (date_from or date_to):
            try:
                date_from_obj, date_to_obj = DateParser.parse_date_range(date_from, date_to)
                logger.info(f"Date filtering: {date_field} from {date_from_obj} to {date_to_obj}")
            except ValueError as e:
                raise ValueError(f"Date parsing error: {e}")
        
        # Fetch all records in batches
        all_records = []
        page = 0
        page_size = 100  # Maximum allowed by API per Ironclad
        start_time = datetime.now()
        timeout_seconds = 120  # 2 minute timeout
        
        # Get total count first
        first_batch = await self.search_records(
            query=query,
            record_type=record_type,
            counterparty=counterparty,
            status_filter=status_filter,
            page_size=page_size,
            page=0
        )
        
        total_records = first_batch.get("total", 0)
        logger.info(f"Total records to scan: {total_records}")
        
        if progress_callback:
            progress_callback(f"Total records to scan: {total_records}")
        
        # Process first batch
        records = first_batch.get("records", [])
        all_records.extend(records)
        page += 1
        
        # Calculate total pages needed
        total_pages = (total_records + page_size - 1) // page_size
        
        # Fetch remaining batches
        while page < total_pages:
            # Check timeout
            elapsed = (datetime.now() - start_time).total_seconds()
            records_scanned = page * page_size
            if elapsed > timeout_seconds:
                logger.warning(f"Timeout after {elapsed:.1f}s. Scanned {records_scanned}/{total_records} records.")
                if progress_callback:
                    progress_callback(
                        f"⚠️ Timeout after {elapsed:.1f}s. Scanned {records_scanned}/{total_records} records. "
                        f"Found {len(all_records)} so far."
                    )
                break
            
            # Progress update
            if progress_callback and records_scanned % 1000 == 0:
                progress_callback(f"Scanned {records_scanned}/{total_records} records ({elapsed:.1f}s)...")
            
            # Fetch next batch
            batch = await self.search_records(
                query=query,
                record_type=record_type,
                counterparty=counterparty,
                status_filter=status_filter,
                page_size=page_size,
                page=page
            )
            
            records = batch.get("records", [])
            if not records:
                break
            
            all_records.extend(records)
            page += 1
            
            # Small delay to avoid overwhelming API
            await asyncio.sleep(0.05)
        
        logger.info(f"Fetched {len(all_records)} total records in {(datetime.now() - start_time).total_seconds():.1f}s")
        
        # Filter by date if specified
        if date_field and date_from_obj and date_to_obj:
            filtered = []
            for record in all_records:
                # Get the date field value from properties (per Ironclad API structure)
                props = record.get("properties", {})
                date_field_obj = props.get(date_field, {})
                date_value = date_field_obj.get("value") if isinstance(date_field_obj, dict) else None
                
                if not date_value:
                    continue
                
                try:
                    # Parse the date from the record (using consistent date parser)
                    record_date = DateParser.parse_date(date_value)
                    
                    # Check if date is in range
                    if date_from_obj <= record_date <= date_to_obj:
                        filtered.append(record)
                except Exception as e:
                    logger.warning(f"Error parsing date for record: {e}")
                    continue
            
            logger.info(f"Date filtering: {len(filtered)}/{len(all_records)} records match date range")
            return filtered
        
        return all_records
    
    async def get_record_attachments(self, record_id: str) -> Dict:
        """
        Get attachments for a record
        
        Args:
            record_id: The record ID (ironcladId or UUID)
        
        Returns:
            Dict containing attachment information
        """
        record = await self.get_record(record_id)
        return record.get("attachments", {})
    
    async def download_attachment(self, record_id: str, attachment_id: str) -> bytes:
        """
        Download an attachment file
        
        Args:
            record_id: The record ID
            attachment_id: The attachment ID
        
        Returns:
            Bytes of the attachment file
        """
        url = f"{self.base_url}/public/api/v1/records/{record_id}/attachments/{attachment_id}"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.content
        except httpx.HTTPError as e:
            logger.error(f"Error downloading attachment: {e}")
            raise
    
    # ========== Workflow Methods ==========
    
    async def search_workflows(
        self,
        query: Optional[str] = None,
        record_type: Optional[str] = None,
        counterparty: Optional[str] = None,
        stage: Optional[str] = None,
        page: int = 0,
        page_size: int = 100
    ) -> Dict:
        """
        Search for workflows (in-progress contracts)
        
        Args:
            query: Search query for workflow name
            record_type: Filter by record/workflow type
            counterparty: Filter by counterparty name
            stage: Filter by workflow stage (e.g., 'review', 'sign', 'draft')
            page: Page number (0-indexed)
            page_size: Number of results per page (max 100)
        
        Returns:
            Dict with 'total' count and 'workflows' list
        """
        url = f"{self.base_url}/public/api/v1/workflows"
        params = {
            "page": page,
            "pageSize": min(page_size, 100)
        }
        
        # Build filter expressions
        filters = []
        if record_type:
            params["types"] = record_type
        if query:
            filters.append(f'Contains([name], "{query}")')
        if counterparty:
            filters.append(f'Contains([counterpartyName], "{counterparty}")')
        if stage:
            # Stage filter - use exact match for stage name
            # API uses 'step' field (e.g., 'Sign', 'Review', 'Draft')
            filters.append(f'Equals([step], "{stage}")')
        
        if filters:
            if len(filters) == 1:
                params["filter"] = f'({filters[0]})'
            else:
                params["filter"] = f'(And({", ".join(filters)}))'
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "total": data.get("count", 0),
                "workflows": data.get("list", [])
            }
        except httpx.HTTPError as e:
            logger.error(f"Error searching workflows: {e}")
            raise
    
    async def get_workflow(self, workflow_id: str) -> Dict:
        """
        Get a specific workflow by ID
        
        Args:
            workflow_id: The workflow ID (UUID or Ironclad ID like IC-60730)
        
        Returns:
            Dict containing workflow data
        """
        import sys
        print(f"\n🔍 get_workflow called with: {workflow_id}", file=sys.stderr, flush=True)
        
        # If it looks like an Ironclad ID (IC-xxxxx), we need to get it directly
        # The API should accept ironcladId directly in the path
        if workflow_id.upper().startswith("IC-"):
            # Try using ironcladId directly
            url = f"{self.base_url}/public/api/v1/workflows/{workflow_id}"
            print(f"   Using IC- ID path: {url}", file=sys.stderr, flush=True)
        else:
            # Use UUID directly
            url = f"{self.base_url}/public/api/v1/workflows/{workflow_id}"
            print(f"   Using UUID path: {url}", file=sys.stderr, flush=True)
        
        try:
            print(f"   Making request...", file=sys.stderr, flush=True)
            response = await self.client.get(url)
            print(f"   Response status: {response.status_code}", file=sys.stderr, flush=True)
            response.raise_for_status()
            data = response.json()
            print(f"   ✅ Success! Got workflow: {data.get('ironcladId', data.get('id'))}", file=sys.stderr, flush=True)
            return data
        except httpx.HTTPError as e:
            print(f"   ❌ HTTP Error: {e}", file=sys.stderr, flush=True)
            # If direct lookup fails and it's an IC- ID, try searching
            if workflow_id.upper().startswith("IC-"):
                print(f"   Direct lookup failed, trying search...", file=sys.stderr, flush=True)
                logger.info(f"Direct lookup failed for {workflow_id}, trying search...")
                try:
                    # Search by filtering on ironcladId field
                    search_url = f"{self.base_url}/public/api/v1/workflows"
                    params = {
                        "filter": f'(Equals([ironcladId], "{workflow_id}"))',
                        "pageSize": 1
                    }
                    print(f"   Search params: {params}", file=sys.stderr, flush=True)
                    search_response = await self.client.get(search_url, params=params)
                    search_response.raise_for_status()
                    data = search_response.json()
                    workflows = data.get("list", [])
                    print(f"   Search found {len(workflows)} workflow(s)", file=sys.stderr, flush=True)
                    if workflows:
                        # Found it via search, now get full details with the UUID
                        uuid = workflows[0].get("id")
                        print(f"   Fetching by UUID: {uuid}", file=sys.stderr, flush=True)
                        return await self.get_workflow(uuid)
                    else:
                        print(f"   ❌ No workflows found in search", file=sys.stderr, flush=True)
                        raise ValueError(f"Workflow {workflow_id} not found in search")
                except Exception as search_error:
                    print(f"   ❌ Search failed: {search_error}", file=sys.stderr, flush=True)
                    logger.error(f"Search also failed: {search_error}")
                    raise ValueError(f"Workflow {workflow_id} not found (search failed: {search_error})")
            else:
                print(f"   ❌ Non-IC ID failed, re-raising error", file=sys.stderr, flush=True)
                logger.error(f"Error getting workflow: {e}")
                raise
    
    async def count_workflows(
        self,
        query: Optional[str] = None,
        record_type: Optional[str] = None,
        counterparty: Optional[str] = None
    ) -> int:
        """
        Count workflows matching criteria
        
        Args:
            query: Search query
            record_type: Filter by workflow type
            counterparty: Filter by counterparty
        
        Returns:
            Total count of matching workflows
        """
        result = await self.search_workflows(
            query=query,
            record_type=record_type,
            counterparty=counterparty,
            page=0,
            page_size=1  # We only need the count
        )
        return result.get("total", 0)
