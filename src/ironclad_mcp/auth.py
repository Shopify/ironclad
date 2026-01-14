"""
OAuth authentication for Ironclad API
"""
import os
import httpx
from typing import Optional, Dict
from datetime import datetime, timedelta


class IroncladOAuthClient:
    """Handles OAuth token management for Ironclad API"""
    
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f"{base_url}/oauth/token"
        
        # Token cache
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
    
    async def get_access_token(self) -> str:
        """
        Get a valid access token, refreshing if necessary.
        Tokens are valid for 6 hours.
        """
        # Check if we have a valid cached token
        if self._access_token and self._token_expires_at:
            # Add 5 minute buffer before expiration
            if datetime.now() < (self._token_expires_at - timedelta(minutes=5)):
                return self._access_token
        
        # Request new token
        return await self._request_new_token()
    
    async def _request_new_token(self) -> str:
        """Request a new access token using client credentials grant"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    # Request Ironclad scopes in the correct format
                    "scope": "public.records.readRecords public.records.readSchemas public.records.readAttachments public.workflows.readWorkflows public.workflows.readApprovals public.workflows.readDocuments"
                }
            )
            
            if response.status_code != 200:
                raise Exception(
                    f"Failed to obtain OAuth token: {response.status_code} - {response.text}"
                )
            
            token_data = response.json()
            
            self._access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 21600)  # Default 6 hours
            self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            return self._access_token








