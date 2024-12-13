import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = 'eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI1TEE3TksiLCJqdGkiOiI2NzVhZDUwNDc0ZmJmZTM1MTZiOWZjMmEiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzM0MDA2MDIwLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzQwNDA4MDB9.sQ5QCNGanwEhR1r7GmB44OdHr7y9U83q_0o3_elhZ-A'
api_version = '2.0'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    # Get User Fund And Margin
    api_response = api_instance.get_profile(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)
