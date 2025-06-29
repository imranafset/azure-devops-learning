from msgraph.graph_service_client import GraphServiceClient
from azure.identity import ClientSecretCredential
from msgraph.generated.models.user import User
from msgraph.generated.models.password_profile import PasswordProfile
import asyncio
import os # Import the os module to access environment variables

# To initialize your graph_client, see https://learn.microsoft.com/en-us/graph/sdks/create-client?from=snippets&tabs=python

# It's best practice to get these from environment variables, especially in Jenkins.
# The Jenkins pipeline will inject these values into the environment.
tenant_id = os.environ.get("tenant_id")
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")

# --- IMPORTANT VALIDATION ---
# Add a check to ensure environment variables are present
if not all([tenant_id, client_id, client_secret]):
    raise ValueError("Missing one or more required environment variables: tenant_id, client_id, client_secret. Ensure they are set in Jenkins.")


scopes = ['https://graph.microsoft.com/.default']

# azure.identity
# The ClientSecretCredential constructor expects keyword arguments.
# You had it as positional arguments, which is incorrect.
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

graph_client = GraphServiceClient(credential, scopes)

async def create_user():
    try:
        print("Creating user request...")
        request_body = User(
            account_enabled=True,
            display_name="Kumar Ramaswamy",
            mail_nickname="KumarS",
            # Ensure this UPN matches your tenant's domain, e.g., "youruser@yourtenant.onmicrosoft.com"
            user_principal_name="kumars@imrankhan7210yahoo.onmicrosoft.com",
            password_profile=PasswordProfile(
                force_change_password_next_sign_in=True,
                # Consider generating a stronger, random password in a real scenario
                password="password@543215s",
            ),
        )

        print("Sending request to Microsoft Graph...")
        result = await graph_client.users.post(request_body)
        print("User created successfully!")
        return result
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")
        # Re-raise the exception so Jenkins knows the step failed
        raise

if __name__ == "__main__":
    try:
        result = asyncio.run(create_user())
        print(result)
    except Exception as e:
        # Catch and print any top-level exceptions from asyncio.run
        print(f"Pipeline execution failed: {e}")
        # Exit with a non-zero status code to indicate failure to Jenkins
        exit(1)