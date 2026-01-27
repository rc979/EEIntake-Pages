#!/bin/bash
# Deploy Auth0 Action via Management API
# This bypasses CLI authentication issues

set -e

ACTION_FILE="actions/filter-google-accounts.js"
TENANT="dev-etm8p8yhx6s75syc.us.auth0.com"

if [ ! -f "$ACTION_FILE" ]; then
    echo "Error: Action file not found: $ACTION_FILE"
    exit 1
fi

echo "Deploying Auth0 Action via Management API..."
echo ""

# Read the action code
ACTION_CODE=$(cat "$ACTION_FILE")

# Create JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "name": "Filter Google Accounts",
  "supported_triggers": [{"id": "post-login", "version": "v3"}],
  "code": $(jq -Rs . <<< "$ACTION_CODE")
}
EOF
)

echo "Creating action via Auth0 Management API..."
echo "Note: You'll need a Management API token"
echo ""
echo "To get a token, run:"
echo "  auth0 api tokens create"
echo ""
echo "Or visit: https://manage.auth0.com/#/apis/management/explorer"
echo ""
echo "Then set AUTH0_MGMT_TOKEN environment variable and run this script again."

if [ -z "$AUTH0_MGMT_TOKEN" ]; then
    echo ""
    echo "Attempting to get token from auth0 CLI..."
    export PATH="$HOME/bin:$PATH"
    
    # Try to get token from CLI
    if command -v auth0 &> /dev/null; then
        echo "Trying to use auth0 CLI to get token..."
        # This might work if CLI is authenticated
        TOKEN=$(auth0 api tokens create --json 2>/dev/null | jq -r '.access_token' 2>/dev/null || echo "")
        
        if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
            AUTH0_MGMT_TOKEN="$TOKEN"
        fi
    fi
fi

if [ -z "$AUTH0_MGMT_TOKEN" ]; then
    echo ""
    echo "ERROR: AUTH0_MGMT_TOKEN not set"
    echo ""
    echo "Quick fix: Use the Auth0 Dashboard instead:"
    echo "1. Go to https://manage.auth0.com/#/actions/flows"
    echo "2. Click Login flow → + → Build Custom"
    echo "3. Name: 'Filter Google Accounts'"
    echo "4. Copy code from $ACTION_FILE"
    echo "5. Deploy and attach to flow"
    exit 1
fi

# Deploy via API
RESPONSE=$(curl -s -X POST \
  "https://${TENANT}/api/v2/actions/actions" \
  -H "Authorization: Bearer $AUTH0_MGMT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

ACTION_ID=$(echo "$RESPONSE" | jq -r '.id // empty')

if [ -z "$ACTION_ID" ] || [ "$ACTION_ID" == "null" ]; then
    echo "Error deploying action:"
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
    exit 1
fi

echo "✅ Action deployed successfully!"
echo "Action ID: $ACTION_ID"
echo ""
echo "Next: Attach it to the Login flow in Auth0 Dashboard:"
echo "https://manage.auth0.com/#/actions/flows/login"
