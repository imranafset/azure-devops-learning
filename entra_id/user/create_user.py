from msgraph.graph_service_client import GraphServiceClient
from azure.identity import ClientSecretCredential
from msgraph.generated.models.user import User
from msgraph.generated.models.password_profile import PasswordProfile
import asyncio
# To initialize your graph_client, see https://learn.microsoft.com/en-us/graph/sdks/create-client?from=snippets&tabs=python

tenant_id = "abc"
client_id = ""
client_secret = ""

scopes = ['https://graph.microsoft.com/.default']

#azure.identity
#credential = DeviceCodeCredential(
    #tenant_id=tenant_id,
    #client_id=client_id)

credential = ClientSecretCredential(
      tenant_id,
      client_id,
      client_secret 
  ) 
graph_client = GraphServiceClient(credential, scopes)

async def create_user():
    try:
        print("Creating user request...")
        request_body = User(
            account_enabled = True,
            display_name = "Kumar Ramaswamy",
            mail_nickname = "KumarS",
            user_principal_name = "kumars@imrankhan7210yahoo.onmicrosoft.com",
            password_profile = PasswordProfile(
                force_change_password_next_sign_in = True,
                password = "password@543215s",
            ),
        )

        print("Sending request to Microsoft Graph...")
        result = await graph_client.users.post(request_body)
        print("User created successfully!")
        return result
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")
        raise

if __name__ == "__main__":
    result = asyncio.run(create_user())
    print(result)