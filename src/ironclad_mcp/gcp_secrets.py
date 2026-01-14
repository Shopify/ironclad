"""
GCP Secret Manager integration for Ironclad OAuth credentials
"""
from google.cloud import secretmanager
import os


class GCPSecretProvider:
    """Retrieves OAuth credentials from GCP Secret Manager"""
    
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID environment variable must be set")
        
        self.client = secretmanager.SecretManagerServiceClient()
        print(f"✅ GCP Secret Manager client initialized for project: {self.project_id}")
    
    def get_secret(self, secret_id: str, version: str = "latest") -> str:
        """Get a secret value from GCP Secret Manager"""
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version}"
        
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode('UTF-8')
        except Exception as e:
            raise ValueError(f"Could not read secret {secret_id} from GCP Secret Manager: {e}")
    
    def get_oauth_credentials(self) -> dict:
        """Get Ironclad OAuth credentials from GCP Secret Manager"""
        client_id = self.get_secret("ironclad-oauth-client-id")
        client_secret = self.get_secret("ironclad-oauth-client-secret")
        
        return {
            "client_id": client_id,
            "client_secret": client_secret
        }
































