import winreg
import requests
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import threading
import winreg

registry_key = r'Software\_MW'
value_name = 'DeviantartCode'
registry_key = r'Software\_MW'
# Initialize variables for Deviantart Code and Client ID
deviantart_code = ""
deviantart_client_id = ""
deviantart_client_secret = ""
deviantart_access_token = ""
# Define the value names for Deviantart Code and Client ID
deviantart_code_name = 'DeviantartCode'
deviantart_client_id_name = 'deviantartClientID'
deviantart_client_secret_name = 'deviantartClientSecret'
deviantart_access_token_name = 'deviantartAccessToken'
deviantart_refresh_token_name = 'deviantartRefreshToken'


try:
    # Open the Registry key
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_READ) as key:
        # Try to read the Deviantart Code value
        try:
            deviantart_code, _ = winreg.QueryValueEx(key, deviantart_code_name)
        except FileNotFoundError:
            print(f"Registry value '{deviantart_code_name}' not found in '{registry_key}'.")

        # Try to read the Deviantart Client ID value
        try:
            deviantart_client_id, _ = winreg.QueryValueEx(key, deviantart_client_id_name)
        except FileNotFoundError:
            print(f"Registry value '{deviantart_client_id_name}' not found in '{registry_key}'.")

        try:
            deviantart_client_secret, _ = winreg.QueryValueEx(key, deviantart_client_secret_name)
        except FileNotFoundError:
            print(f"Registry value '{deviantart_client_secret_name}' not found in '{registry_key}'.")

        try:
            deviantart_access_token, _ = winreg.QueryValueEx(key, deviantart_access_token_name)
        except FileNotFoundError:
            print(f"Registry value '{deviantart_access_token_name}' not found in '{registry_key}'.")
        try:
            deviantart_refresh_token, _ = winreg.QueryValueEx(key, deviantart_refresh_token_name)
        except FileNotFoundError:
            print(f"Registry value '{deviantart_refresh_token_name}' not found in '{registry_key}'.")

except FileNotFoundError:
    print(f"Registry key '{registry_key}' not found.")
except PermissionError:
    print(f"Permission error: Unable to open the registry key.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Print Deviantart Code and Client ID
if deviantart_code:
    print(f"Deviantart Code: {deviantart_code}")
else:
    print("No Deviantart Code")

if deviantart_client_id:
    print(f"Deviantart Client ID: {deviantart_client_id}")
else:
    print("No Deviantart Client ID")

if deviantart_client_secret:
    print(f"Deviantart Secret: {deviantart_client_secret}")
else:
    print("No Deviantart Secret")


if deviantart_access_token:
    print(f"Deviantart access token: {deviantart_access_token}")
else:
    print("No Deviantart access token")


if deviantart_refresh_token:
    print(f"Deviantart Refresh token: {deviantart_refresh_token}")
else:
    print("No Deviantart refresh token")


# Define the URL for user authorization
authorization_url = "https://www.deviantart.com/oauth2/authorize"

# Set the required query-string parameters
params = {
    "response_type": "code",
    "client_id": deviantart_client_id,  # Replace with your actual client ID
    "redirect_uri": "http://localhost",  # Change to your preferred redirect URI
    "scope": "stash publish",  # You may need to specify the required scope(s)
}

# Create the full authorization URL
full_authorization_url = f"{authorization_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

# Print the authorization URL (for debugging purposes)
print("Authorization URL:", full_authorization_url)

# Open the URL in a web browser to let the user authorize your application
webbrowser.open(full_authorization_url)

# Inform the user that the script is running
print("Waiting for user authorization...")

# Define the redirect URI and port for your local server
redirect_uri = "http://localhost"
port = 80

# Define the URL for token retrieval
token_url = "https://www.deviantart.com/oauth2/token"

# Create a dictionary to store the authorization code
authorization_code = None

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_code
        params = parse_qs(self.path[self.path.find('?')+1:])
        if 'code' in params:
            authorization_code = params['code'][0]
            print("Authorization code received:", authorization_code)  # Print the code

            # Save the code to the Windows Registry
            try:
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_key) as key:
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, authorization_code)
                print(f'Successfully saved Deviantart code in the Registry.')
            except Exception as e:
                print(f'Failed to save Deviantart code in the Registry: {str(e)}')

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Authorization successful. You can close this window now.')
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Invalid request. Please close this window and try again.')

# Create a flag to signal the server to stop
server_stopped = False

# Start the local HTTP server to capture the authorization code in a separate thread
def start_server():
    server = HTTPServer(('localhost', port), AuthHandler)
    while not server_stopped:
        server.handle_request()

server_thread = threading.Thread(target=start_server)
server_thread.start()

try:
    # Wait until the user has authorized the application
    while authorization_code is None:
        pass

    # Stop the server and finish the thread
    server_stopped = True
    server_thread.join()
except KeyboardInterrupt:
    pass
    # Continue with the rest of your script (token retrieval and registry key update)
try:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_key) as key:
        winreg.SetValueEx(key, deviantart_code_name, 0, winreg.REG_SZ, authorization_code)
    print(f'Successfully saved Deviantart Code in the Registry.')
except Exception as e:
    print(f'Failed to save Deviantart Code in the Registry: {str(e)}')
    pass
