# Auth0 Configuration

This directory contains Auth0 configuration files and Action code for reference and version control.

## Deployment Options

You can deploy Auth0 Actions in two ways:

1. **Auth0 CLI** (Recommended) - Deploy Actions programmatically from your repo
2. **Auth0 Dashboard** (Manual) - Copy/paste code into the dashboard

Both methods are documented below.

## Files

- `actions/filter-google-accounts.js` - Post-Login Action to filter Google accounts by email domain or specific emails

## How to Deploy Auth0 Actions

### Option 1: Using Auth0 CLI (Recommended)

#### Install Auth0 CLI

```bash
# macOS/Linux
brew tap auth0/auth0-cli
brew install auth0-cli

# Or using npm
npm install -g @auth0/auth0-cli

# Or using curl (macOS/Linux)
curl -sSfL https://raw.githubusercontent.com/auth0/auth0-cli/main/install.sh | sh
```

#### Authenticate

```bash
auth0 login
```

This will open your browser to authenticate with Auth0.

#### Deploy an Action

```bash
# Deploy the filter-google-accounts action
cd auth0/actions
auth0 actions deploy filter-google-accounts.js

# Or deploy interactively (will prompt for file)
auth0 actions deploy
```

#### List Actions

```bash
auth0 actions list
```

#### Attach Action to Login Flow

After deploying, you still need to attach it to the Login flow:

1. Go to **Auth0 Dashboard** → **Actions** → **Flows** → **Login**
2. Drag your deployed Action into the flow (between **Start** and **Complete**)
3. Click **Apply**

#### Update an Existing Action

```bash
# Update the action code
auth0 actions update <action-id> --code filter-google-accounts.js
```

---

### Option 2: Using Auth0 Dashboard (Manual)

#### 1. Create the Action in Auth0 Dashboard

1. Go to **Auth0 Dashboard** → **Actions** → **Flows**
2. Click **Login** flow
3. Click **+** (Add Action) → **Build Custom**
4. Name it (e.g., "Filter Google Accounts")
5. Click **Create**

#### 2. Copy Code from This Repo

1. Open the Action file from `auth0/actions/` in this repo
2. Copy the entire code
3. Paste it into the Auth0 Action editor
4. Update the configuration arrays (allowedDomains, allowedEmails) with your values

#### 3. Deploy and Attach

1. Click **Deploy** (top right)
2. Go back to **Actions** → **Flows** → **Login**
3. Drag your Action into the flow (between **Start** and **Complete**)
4. Click **Apply**

## Current Actions

### Filter Google Accounts

**Purpose:** Restrict Google login to specific email domains or individual email addresses.

**Configuration:**
- Edit `auth0/actions/filter-google-accounts.js`
- Update `allowedDomains` array with allowed email domains
- Update `allowedEmails` array with specific allowed email addresses
- Copy the updated code to Auth0 Dashboard

**How it works:**
- Checks if user's email matches any in `allowedEmails` → Allow
- Checks if user's email domain matches any in `allowedDomains` → Allow
- Otherwise → Deny with error message

## Auth0 Dashboard Links

- **Actions:** https://manage.auth0.com/#/actions/flows
- **Users:** https://manage.auth0.com/#/users
- **Applications:** https://manage.auth0.com/#/applications
- **Connections:** https://manage.auth0.com/#/connections

## Environment Variables (Netlify)

The Netlify Auth0 extension automatically creates these environment variables:
- `AUTH0_DOMAIN` - Your Auth0 tenant domain
- `AUTH0_CLIENT_ID` - Your Auth0 application client ID
- `AUTH0_AUDIENCE` - Your Auth0 API audience

These are available in Netlify Functions but not in static HTML (which is why we hardcode them in `docs/index.html`).
