# Ironclad MCP Deployment Guide

This guide walks you through deploying the Ironclad MCP server for your organization using GCP Secret Manager.

## Prerequisites

- Google Cloud Platform account with a project
- `gcloud` CLI installed and configured
- Ironclad OAuth credentials (client ID and secret)
- Docker and Docker Compose installed (for deployment)

## Step 1: Select or Create GCP Project

```bash
# List your projects
gcloud projects list

# Select the project you want to use
gcloud config set project YOUR_PROJECT_ID
```

For this setup, we're using: `shopify-contract-filing-automa`

## Step 2: Enable Secret Manager API

```bash
# Enable the Secret Manager API for your project
gcloud services enable secretmanager.googleapis.com
```

When prompted, type `y` to enable the API.

## Step 3: Store OAuth Credentials in GCP Secret Manager

```bash
# Create secrets for Ironclad OAuth credentials
echo -n "YOUR_CLIENT_ID" | gcloud secrets create ironclad-oauth-client-id --data-file=-

echo -n "YOUR_CLIENT_SECRET" | gcloud secrets create ironclad-oauth-client-secret --data-file=-
```

Replace `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` with your actual Ironclad OAuth credentials.

**Example:**
```bash
echo -n "ed8033f2-c544-462c-9edc-89052df233dd" | gcloud secrets create ironclad-oauth-client-id --data-file=-

echo -n "cbaf3899-9aa8-4472-aea3-564c7faaef08" | gcloud secrets create ironclad-oauth-client-secret --data-file=-
```

## Step 4: Create Service Account for MCP Server

```bash
# Create a service account
gcloud iam service-accounts create ironclad-mcp-server \
  --display-name="Ironclad MCP Server" \
  --description="Service account for Ironclad MCP to access secrets"
```

## Step 5: Grant Service Account Access to Secrets

```bash
# Get your project ID
export PROJECT_ID=$(gcloud config get-value project)

# Create service account email
export SA_EMAIL="ironclad-mcp-server@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant access to client ID secret
gcloud secrets add-iam-policy-binding ironclad-oauth-client-id \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"

# Grant access to client secret
gcloud secrets add-iam-policy-binding ironclad-oauth-client-secret \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"
```

## Step 6: Download Service Account Key

```bash
# Download the service account key
gcloud iam service-accounts keys create service-account-key.json \
  --iam-account="${SA_EMAIL}"

# Verify the key was created
ls -lh service-account-key.json
```

⚠️ **Security Note:** This key file grants access to your secrets. Keep it secure and never commit it to version control.

## Step 7: Configure Environment Variables

Create a `.env` file:

```bash
cat > .env << EOF
# GCP Configuration
GCP_PROJECT_ID=shopify-contract-filing-automa
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

# Ironclad Configuration
IRONCLAD_BASE_URL=https://na1.ironcladapp.com

# Server Configuration
PORT=8000
EOF
```

## Step 8: Test Locally

```bash
# Install dependencies
python3 -m pip install google-cloud-secret-manager

# Test the server
export GCP_PROJECT_ID="shopify-contract-filing-automa"
export GOOGLE_APPLICATION_CREDENTIALS="./service-account-key.json"
export IRONCLAD_BASE_URL="https://na1.ironcladapp.com"

python3 -m ironclad_mcp.http_server
```

You should see:
```
✅ GCP Secret Manager client initialized for project: shopify-contract-filing-automa
✅ Ironclad OAuth client initialized: https://na1.ironcladapp.com
🚀 Ironclad MCP Server started (HTTP/SSE transport)
   Ironclad URL: https://na1.ironcladapp.com
   GCP Project: shopify-contract-filing-automa
   Endpoint: /sse (for Claude Desktop connections)
```

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ironclad-mcp",
  "version": "2.0.0",
  "transport": "sse"
}
```

## Step 9: Deploy with Docker Compose

```bash
# Build and start the service
docker-compose -f docker-compose-http.yml up --build -d

# Check logs
docker-compose -f docker-compose-http.yml logs -f

# Test the deployed service
curl http://localhost:8000/health
```

## Step 10: Configure Claude Desktop (End Users)

End users need to add this to their Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "ironclad-mcp": {
      "type": "streamable-http",
      "url": "http://YOUR_SERVER_URL:8000/sse",
      "headers": {
        "X-User-Email": "user@shopify.com"
      }
    }
  }
}
```

Replace:
- `YOUR_SERVER_URL` with your MCP server's hostname or IP
- `user@shopify.com` with the user's actual email

## Security Considerations

### For Production Deployment:

1. **Authentication**: Integrate with Shopify's authentication system (IAP, Okta, etc.) to validate X-User-Email headers

2. **Network Security**: Deploy behind a firewall or VPN

3. **Secret Rotation**: Regularly rotate OAuth credentials:
   ```bash
   # Add new version
   echo -n "NEW_SECRET" | gcloud secrets versions add ironclad-oauth-client-secret --data-file=-
   
   # Disable old version
   gcloud secrets versions disable VERSION_NUMBER --secret=ironclad-oauth-client-secret
   ```

4. **Access Control**: Limit service account permissions to only the necessary secrets

5. **Monitoring**: Set up logging and monitoring for:
   - API call patterns
   - Authentication failures
   - Secret access attempts

## Troubleshooting

### Error: Permission denied for secret access

**Solution:** Verify service account has `roles/secretmanager.secretAccessor` role:
```bash
gcloud secrets get-iam-policy ironclad-oauth-client-id
```

### Error: GCP_PROJECT_ID not set

**Solution:** Export the environment variable:
```bash
export GCP_PROJECT_ID="your-project-id"
```

### Error: Service account key not found

**Solution:** Verify the key file exists and the path is correct:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/service-account-key.json"
```

## Next Steps

- **Add authentication**: Integrate with Shopify's auth system
- **Deploy to Cloud Run**: For automatic scaling and managed infrastructure
- **Set up monitoring**: Track usage and errors
- **Configure alerts**: Get notified of issues

---

For questions or issues, refer to:
- [GCP Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Ironclad API Documentation](https://developer.ironcladapp.com)
































