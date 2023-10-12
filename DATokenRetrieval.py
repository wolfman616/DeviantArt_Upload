import requests
import winreg

def regreads():
    registry_key = r'Software\_MW'

    # Define the value names for Deviantart Code and Client ID
    deviantart_code_name = 'DeviantartCode'
    deviantart_client_id_name = 'deviantartClientID'
    deviantart_client_secret_name = 'deviantartClientSecret'
    deviantart_access_token_name = 'deviantartAccessToken'

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
    except FileNotFoundError:
        print(f"Registry key '{registry_key}' not found.")
    except PermissionError:
        print(f"Permission error: Unable to open the registry key.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return deviantart_client_secret, deviantart_client_id, deviantart_code, deviantart_access_token
registry_key = r'Software\_MW'

deviantart_code_name = 'DeviantartCode'
deviantart_client_id_name = 'deviantartClientID'
deviantart_client_secret_name = 'deviantartClientSecret'
deviantart_access_token_name = 'deviantartAccessToken'

# Initialize variables for Deviantart Code and Client ID
deviantart_code = ""
deviantart_client_id = ""
deviantart_client_secret = ""
deviantart_access_token = ""


# Define the token endpoint
token_url = "https://www.deviantart.com/oauth2/token"

# Define your variables for client_id, client_secret, and code

result=regreads()
deviantart_client_secret, deviantart_client_id, deviantart_code, deviantart_access_token = result
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
redirect_uri = "http://localhost"

# Define the data to send in the POST request using the variables
data = {
    "grant_type": "authorization_code",
    "client_id": deviantart_client_id,
    "client_secret": deviantart_client_secret,
    "code": deviantart_code,
    "redirect_uri": redirect_uri,
}

try:
    # Send the POST request to obtain the access token
    response = requests.post(token_url, data=data)
    response_data = response.json()

    if "access_token" in response_data:
        deviantart_access_token = response_data["access_token"]
        print(f"Access Token: {deviantart_access_token}")
        
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_key) as key:
                winreg.SetValueEx(key, deviantart_access_token_name, 0, winreg.REG_SZ, deviantart_access_token)
                print(f'Successfully saved Deviantart Client ID in the Registry.')
        except Exception as e:
            print(f'Failed to save Deviantart Client ID in the Registry: {str(e)}')
            
        
    else:
        print("Failed to obtain the access token.")

        #here is where a bad auth code is detected {"error":"invalid_request","error_description":"Incorrect authorization code.","status":"error"}
        #we will run python.exe "C:\Script\Python\DAAuthorization - Copy.py"
        #and wait 5 seconds and then re read the registry with regreads()

except Exception as e:
    print(f"An error occurred: {str(e)}")
    pass
    print(f"Deviantdssdsdart Client ID: {deviantart_access_token}")

print(response.text)


