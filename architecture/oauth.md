## OAuth2 Flow (Salesforce)

1. Client requests authorization code
2. Salesforce returns authorization code
3. Exchange code for access_token + refresh_token
4. Use access_token for API calls
5. Refresh token when expired

Auth URL:
https://login.salesforce.com/services/oauth2/token
