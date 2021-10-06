# connector-azure-storage

This integration enables you to deploy and manage storage accounts and blob services. This integration was integrated with version 2021-04-01 of Azure Storage.

# API Documentation Link: https://docs.microsoft.com/en-us/rest/api/storagerp/storage-accounts

# Connector Authentication:

You can get authentication token to access the Azure Storage APIs using OAuth 2.0 method.

-	On behalf of User – Delegate Permissions
Please refer https://docs.microsoft.com/en-us/rest/api/azure/#register-your-client-application-with-azure-ad for more info

1.  Make sure the following permissions are granted for the app registration:
      a.  Azure Service Management - permission user_impersonation of type Delegated.
2. The Redirect URI can direct any web application that you wish to receive responses from Azure AD. If you are not sure what to set, you can use https://localhost
3.	Copy the following URL and replace the TENANT_ID, CLIENT_ID, REDIRECT_URI with your own client ID and redirect URI, accordingly. https://login.microsoftonline.com/TENANT_ID/oauth2/v2.0/authorize?response_type=code&scope=https://management.azure.com/user_impersonation offline_access user.read&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI 
1.	Enter the link and you will be prompted to grant permissions for your Azure Service Management. You will be automatically redirected to a link with the following structure: REDIRECT_URI?code=AUTH_CODE&session_state=SESSION_STATE
2.	Copy the AUTH_CODE (without the "code=" prefix) and paste it in your instance configuration under the Authorization code parameter.
3.	Enter your client ID in the Client ID parameter field.
4.	Enter your client secret in the Client Secret parameter field.
5.	Enter your tenant ID in the Tenant ID parameter field.
6.	Enter your redirect URI in the Redirect URI parameter field. By default it is set to https://localhost
