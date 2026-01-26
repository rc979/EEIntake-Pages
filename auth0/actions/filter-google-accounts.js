/**
 * Auth0 Post-Login Action: Filter Google Accounts
 * 
 * This action filters which Google accounts can log in based on:
 * - Allowed email domains (e.g., @yourcompany.com)
 * - Specific allowed email addresses
 * 
 * SETUP INSTRUCTIONS:
 * 1. Go to Auth0 Dashboard → Actions → Flows → Login
 * 2. Click "+" → "Build Custom"
 * 3. Name it: "Filter Google Accounts"
 * 4. Copy the code from this file into the Action editor
 * 5. Update the allowedDomains and allowedEmails arrays below
 * 6. Click "Deploy"
 * 7. Drag the action into the Login flow (between Start and Complete)
 * 8. Click "Apply"
 */

exports.onExecutePostLogin = async (event, api) => {
  // ============================================
  // CONFIGURATION: Update these arrays
  // ============================================
  
  // Allowed email domains (users from these domains can log in)
  const allowedDomains = [
    'yourcompany.com',
    'example.com'
    // Add more domains as needed
  ];
  
  // Specific allowed emails (can be from any domain)
  const allowedEmails = [
    'specialuser@gmail.com',
    'contractor@external.com'
    // Add more specific emails as needed
  ];
  
  // ============================================
  // FILTERING LOGIC (no changes needed below)
  // ============================================
  
  const email = (event.user.email || '').toLowerCase();
  
  if (!email) {
    api.access.deny('Email address required');
    return;
  }
  
  // Check if email is in allowed list
  if (allowedEmails.includes(email)) {
    api.access.allow();
    return;
  }
  
  // Check if email domain is allowed
  const emailDomain = email.split('@')[1];
  if (emailDomain && allowedDomains.includes(emailDomain)) {
    api.access.allow();
    return;
  }
  
  // Deny access if not in allowlist
  api.access.deny('Access denied. Your email is not authorized to access this site.');
};
