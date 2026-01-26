#!/bin/bash
# Deploy Auth0 Actions using Auth0 CLI
# Usage: ./deploy-action.sh <action-name>
# Example: ./deploy-action.sh filter-google-accounts

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <action-name>"
    echo "Example: $0 filter-google-accounts"
    exit 1
fi

ACTION_NAME="$1"
ACTION_FILE="actions/${ACTION_NAME}.js"

if [ ! -f "$ACTION_FILE" ]; then
    echo "Error: Action file not found: $ACTION_FILE"
    exit 1
fi

echo "Deploying Auth0 Action: $ACTION_NAME"
echo "File: $ACTION_FILE"
echo ""

# Check if auth0 CLI is installed
if ! command -v auth0 &> /dev/null; then
    echo "Error: Auth0 CLI not found. Install it with:"
    echo "  brew install auth0-cli"
    echo "  or"
    echo "  npm install -g @auth0/auth0-cli"
    exit 1
fi

# Deploy the action
auth0 actions deploy "$ACTION_FILE"

echo ""
echo "✅ Action deployed successfully!"
echo ""
echo "Next steps:"
echo "1. Go to Auth0 Dashboard → Actions → Flows → Login"
echo "2. Drag your deployed Action into the flow"
echo "3. Click Apply"