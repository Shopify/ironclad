"""
Vault integration for retrieving user identity and Ironclad credentials
"""
import os
import hvac
from typing import Dict, Optional


class VaultCredentialProvider:
    """Manages Vault authentication and retrieves user-specific credentials"""
    
    def __init__(self):
        self.vault_addr = os.getenv("VAULT_ADDR")
        self.vault_token = os.getenv("VAULT_TOKEN")
        self.vault_namespace = os.getenv("VAULT_NAMESPACE")
        
        if not self.vault_addr or not self.vault_token:
            raise ValueError(
                "VAULT_ADDR and VAULT_TOKEN environment variables must be set. "
                "Please configure your Vault credentials."
            )
        
        # Initialize Vault client
        self.client = hvac.Client(
            url=self.vault_addr,
            token=self.vault_token,
            namespace=self.vault_namespace
        )
        
        if not self.client.is_authenticated():
            raise ValueError(
                "Failed to authenticate with Vault. "
                "Please check your VAULT_TOKEN is valid."
            )
        
        # Get user identity from token
        self.user_identity = self._get_token_identity()
    
    def _get_token_identity(self) -> Dict:
        """
        Look up the identity associated with this Vault token
        Returns user information including username, email, entity_id, etc.
        """
        try:
            # Look up the token to get metadata
            token_info = self.client.auth.token.lookup_self()
            
            identity = {
                'display_name': token_info['data'].get('display_name'),
                'entity_id': token_info['data'].get('entity_id'),
                'metadata': token_info['data'].get('meta', {}),
                'policies': token_info['data'].get('policies', [])
            }
            
            # If we have an entity_id, get more detailed identity info
            if identity['entity_id']:
                try:
                    entity_info = self.client.secrets.identity.read_entity(
                        entity_id=identity['entity_id']
                    )
                    
                    # Get aliases (these contain username/email)
                    aliases = entity_info['data'].get('aliases', [])
                    if aliases:
                        identity['username'] = aliases[0].get('name')
                        identity['alias_metadata'] = aliases[0].get('metadata', {})
                    
                    # Get entity metadata (might contain email, etc.)
                    identity['entity_metadata'] = entity_info['data'].get('metadata', {})
                except Exception:
                    # Entity lookup might not be available, continue with what we have
                    pass
            
            return identity
            
        except Exception as e:
            raise ValueError(f"Could not determine user identity from Vault token: {e}")
    
    def get_user_email(self) -> str:
        """
        Get the user's email address for Ironclad API calls.
        This is used in the x-as-user-email header.
        """
        # Try to get email from Vault user data first
        user_data = self.get_user_ironclad_data()
        if user_data and 'email' in user_data:
            return user_data['email']
        
        # Fall back to identity metadata
        if self.user_identity.get('entity_metadata', {}).get('email'):
            return self.user_identity['entity_metadata']['email']
        
        # Try username if it looks like an email
        username = self.user_identity.get('username', '')
        if '@' in username:
            return username
        
        # Last resort: use display name if it looks like an email
        display_name = self.user_identity.get('display_name', '')
        if '@' in display_name:
            return display_name
        
        raise ValueError(
            f"Could not determine email for user. "
            f"Please ensure your Ironclad email is stored in Vault at: "
            f"secret/ironclad/users/<your_identifier>"
        )
    
    def get_user_identifier(self) -> str:
        """Get a consistent user identifier for Vault path lookups"""
        # Priority order for identifier
        if self.user_identity.get('entity_metadata', {}).get('email'):
            return self.user_identity['entity_metadata']['email']
        
        if self.user_identity.get('username'):
            return self.user_identity['username']
        
        if self.user_identity.get('display_name'):
            return self.user_identity['display_name']
        
        if self.user_identity.get('entity_id'):
            return self.user_identity['entity_id']
        
        raise ValueError("Could not determine user identifier from Vault token")
    
    def get_user_ironclad_data(self) -> Optional[Dict]:
        """
        Retrieve user's Ironclad-specific data from Vault.
        This might include their Ironclad email, user ID, or preferences.
        """
        user_id = self.get_user_identifier()
        
        # Try multiple possible paths where user data might be stored
        possible_paths = [
            f"ironclad/users/{user_id}",
            f"users/{user_id}/ironclad",
            f"ironclad/entities/{self.user_identity.get('entity_id')}",
        ]
        
        for path in possible_paths:
            if not path:
                continue
            
            try:
                # Try KV v2 (most common)
                secret = self.client.secrets.kv.v2.read_secret_version(path=path)
                return secret['data']['data']
            except Exception:
                # Try KV v1
                try:
                    secret = self.client.secrets.kv.v1.read_secret(path=path)
                    return secret['data']
                except Exception:
                    continue
        
        # No user-specific data found, which is OK - we'll use identity data
        return None
    
    def get_oauth_credentials(self) -> Dict[str, str]:
        """
        Get the company-wide Ironclad OAuth credentials from Vault.
        These are shared across all users.
        """
        # Path for shared company credentials
        oauth_path = os.getenv(
            "VAULT_IRONCLAD_OAUTH_PATH",
            "ironclad/oauth"
        )
        
        try:
            # Try KV v2
            secret = self.client.secrets.kv.v2.read_secret_version(path=oauth_path)
            data = secret['data']['data']
        except Exception:
            # Try KV v1
            try:
                secret = self.client.secrets.kv.v1.read_secret(path=oauth_path)
                data = secret['data']
            except Exception as e:
                raise ValueError(
                    f"Could not find Ironclad OAuth credentials in Vault at path: {oauth_path}. "
                    f"Error: {e}"
                )
        
        # Validate required fields
        if 'client_id' not in data or 'client_secret' not in data:
            raise ValueError(
                f"Ironclad OAuth credentials at {oauth_path} must contain "
                "'client_id' and 'client_secret' fields"
            )
        
        return data
















































