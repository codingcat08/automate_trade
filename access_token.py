import upstox_client
from upstox_client.rest import ApiException

api_instance = upstox_client.LoginApi()
api_version = '2.0'
code = 'tAl2Md'
client_id = 'bf7ba9b6-1cc2-4ba1-ac42-e9d66d23540a'
client_secret = 's7jnb7pjpk'
redirect_uri = 'http://localhost:8080'
grant_type = 'authorization_code'

try:
    # Get token API
    api_response = api_instance.token(api_version, code=code, client_id=client_id, client_secret=client_secret,
                                      redirect_uri=redirect_uri, grant_type=grant_type)
    print(api_response)
except ApiException as e:
    print("Exception when calling LoginApi->token: %s\n" % e)