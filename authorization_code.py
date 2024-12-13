import webbrowser
# Set up Upstox API parameters
api_key = 'bf7ba9b6-1cc2-4ba1-ac42-e9d66d23540a'
redirect_uri = 'http://localhost:8080'  # Localhost redirect URI
login_url = f"https://api.upstox.com/v2/login/authorization/dialog?client_id={api_key}&redirect_uri={redirect_uri}&response_type=code"

# Open the login URL in a web browser
webbrowser.open(login_url)
