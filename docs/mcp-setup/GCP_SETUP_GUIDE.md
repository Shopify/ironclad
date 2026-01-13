# GCP Secret Manager Setup Guide

This guide shows you how to set up GCP Secret Manager for the Ironclad MCP server, following Shopify's recommended approach for managing third-party API credentials.

## Why GCP Secret Manager?

According to Shopify's internal best practices:
- ✅ **Automated rotation** - Supports credential rotation without downtime
- ✅ **Service account access** - Secure programmatic access for deployed services
- ✅ **Production-grade** - Better than EJSON for frequently rotated credentials
- ✅ **Audit trails** - Track who accessed secrets and when

## Step-by-Step Setup

### Step 1: Select Your GCP Project

```bash
# List available projects
gcloud projects list

# Set the project you want to use
gcloud config set project YOUR_PROJECT_ID
```

For this example, we're using: `shopify-contract-filing-automa`

### Step 2: Enable Secret Manager API

```bash
# Enable the API
gcloud services enable secretmanager.googleapis.com
```

When prompted `Would you like to enable and retry (this will take a few minutes)? (y/N)?`, type `y`.

### Step 3: Create Secrets for OAuth Credentials

```bash
# Create secret for client ID
echo -n "ed8033f2-c544-462c-9edc-89052df233dd" | \
  gcloud secrets create ironclad-oauth-client-id --data-file=-

# Create secret for client secret  
echo -n "cbaf3899-9aa8-4472-aea3-564c7faaef08" | \
  gcloud secrets create ironclad-oauth-client-secret --data-file=-
```

**Replace the example values with your actual Ironclad OAuth credentials.**

Verify secrets were created:
```bash
gcloud secrets list
```

### Step 4: Create Service Account

```bash
# Create the service account
gcloud iam service-accounts create ironclad-mcp-server \
  --display-name="Ironclad MCP Server" \
  --description="Service account for Ironclad MCP to access secrets"
```

Verify it was created:
```bash
gcloud iam service-accounts list
```

### Step 5: Grant Service Account Access to Secrets

```bash
# Get your project ID
PROJECT_ID=$(gcloud config get-value project)

# Construct service account email
SA_EMAIL="ironclad-mcp-server@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant access to client-id secret
gcloud secrets add-iam-policy-binding ironclad-oauth-client-id \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"

# Grant access to client-secret secret
gcloud secrets add-iam-policy-binding ironclad-oauth-client-secret \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"
```

Verify permissions:
```bash
gcloud secrets get-iam-policy ironclad-oauth-client-id
gcloud secrets get-iam-policy ironclad-oauth-client-secret
```

### Step 6: Download Service Account Key

```bash
# Download the key file
gcloud iam service-accounts keys create service-account-key.json \
  --iam-account="${SA_EMAIL}"
```

⚠️ **Important:** This key grants access to your secrets. Keep it secure!

- ✅ Add `service-account-key.json` to `.gitignore`
- ✅ Store securely (don't commit to git)
- ✅ Use environment-specific keys for dev/staging/prod

Verify the file:
```bash
ls -lh service-account-key.json
cat service-account-key.json | jq .type
# Should output: "service_account"
```

## Testing the Setup

```bash
# Set environment variables
export GCP_PROJECT_ID="shopify-contract-filing-automa"
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/service-account-key.json"
export IRONCLAD_BASE_URL="https://na1.ironcladapp.com"

# Test secret access
python3 << 'EOF'
from src.ironclad_mcp.gcp_secrets import GCPSecretProvider

provider = GCPSecretProvider()
creds = provider.get_oauth_credentials()
print(f"✅ Successfully retrieved secrets")
print(f"   Client ID: {creds['client_id'][:20]}...")
print(f"   Client Secret: {creds['client_secret'][:20]}...")
EOF
```

Expected output:
```
✅ GCP Secret Manager client initialized for project: shopify-contract-filing-automa
✅ Successfully retrieved secrets
   Client ID: ed8033f2-c544-462c...
   Client Secret: cbaf3899-9aa8-4472...
```

## Starting the MCP Server

```bash
# Start the server
python3 -m ironclad_mcp.http_server
```

Expected output:
```
✅ GCP Secret Manager client initialized for project: shopify-contract-filing-automa
✅ Ironclad OAuth client initialized: https://na1.ironcladapp.com
🚀 Ironclad MCP Server started (HTTP/SSE transport)
   Ironclad URL: https://na1.ironcladapp.com
   GCP Project: shopify-contract-filing-automa
   Endpoint: /sse (for Claude Desktop connections)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
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

## Troubleshooting

### Error: `gcloud` command not found

Install the Google Cloud SDK:
```bash
# Mac (Homebrew)
brew install google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

### Error: Permission denied to enable API

You need the `serviceusage.services.enable` permission on your project. Either:
- Switch to a project you own
- Ask a project owner to grant you permissions
- Use the GCP Console instead (https://console.cloud.google.com)

### Error: Permission denied for resource

The service account doesn't have access to the secret. Re-run Step 5.

### Error: Secret not found

The secret doesn't exist. Re-run Step 3.

### Error: `gcloud crashed (LayoutException)`

Your gcloud installation is corrupted. Fix it with:
```bash
gcloud components update
# If that fails:
gcloud components install beta
```

Or use the GCP Console as a fallback for IAM operations:
1. Go to https://console.cloud.google.com/security/secret-manager
2. Click on your secret
3. Go to "Permissions" tab
4. Click "Grant Access"
5. Add your service account with role "Secret Manager Secret Accessor"

## Security Best Practices

### Environment-Specific Secrets

Create separate secrets for each environment:

```bash
# Development
gcloud secrets create ironclad-oauth-client-id-dev --data-file=-
gcloud secrets create ironclad-oauth-client-secret-dev --data-file=-

# Staging
gcloud secrets create ironclad-oauth-client-id-staging --data-file=-
gcloud secrets create ironclad-oauth-client-secret-staging --data-file=-

# Production  
gcloud secrets create ironclad-oauth-client-id-prod --data-file=-
gcloud secrets create ironclad-oauth-client-secret-prod --data-file=-
```

### Rotating Credentials

```bash
# Add new version (old version remains accessible)
echo -n "NEW_SECRET_VALUE" | \
  gcloud secrets versions add ironclad-oauth-client-secret --data-file=-

# Test new version
# ...

# Disable old version
gcloud secrets versions disable VERSION_NUMBER \
  --secret=ironclad-oauth-client-secret

# Destroy after grace period
gcloud secrets versions destroy VERSION_NUMBER \
  --secret=ironclad-oauth-client-secret
```

### Access Control

Production secrets should only be accessible to:
- Service accounts running the MCP server
- Minimal set of administrators

```bash
# Audit who has access
gcloud secrets get-iam-policy ironclad-oauth-client-secret-prod
```

## Next Steps

- [ ] Test the MCP server locally
- [ ] Deploy with Docker (see `docker-compose-http.yml`)
- [ ] Configure Claude Desktop for end users
- [ ] Set up credential rotation schedule
- [ ] Add monitoring and alerting

For more details, see:
- [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md) - Full deployment instructions
- [`START_HERE.md`](./START_HERE.md) - Architecture overview
- [GCP Secret Manager Docs](https://cloud.google.com/secret-manager/docs)
































