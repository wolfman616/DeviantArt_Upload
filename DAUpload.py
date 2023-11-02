import argparse
import os
import requests
import winreg
import sys

parser = argparse.ArgumentParser(description="Upload and publish a file to DeviantArt stash.")
parser.add_argument("--title", required=True, help="Title of the submission")
parser.add_argument("--artist_comments", help="Additional comments by the artist")
parser.add_argument("--tags_csv", help="CSV string of tags for the submission (e.g., 'tag1,tag2,tag3')")
parser.add_argument("--is_dirty", action="store_true", help="Is the submission currently being edited")
parser.add_argument("--mature", choices=["yes", "no"], default="no", help="Set mature status (yes or no, default is no)")
parser.add_argument("--mature_level", choices=["strict", "moderate"], default=None, help="Mature level of the submission (optional)")
parser.add_argument("--mature_classification_csv", default=None, help="CSV string of mature classification values (e.g., 'nudity,gore,language') (optional)")
parser.add_argument("--file", required=True, help="Path to the file to upload")

# Check for the -h option, and if present, display the help message and exit
if "-h" in sys.argv or "--help" in sys.argv:
    parser.print_help()
    sys.exit(0)
    
registry_key = r'Software\_MW'

# Define the value names for Deviantart Code, Client Secret and Client ID
deviantart_code_name = 'DeviantartCode'
deviantart_client_id_name = 'deviantartClientID'
deviantart_client_secret_name = 'deviantartClientSecret'
deviantart_access_token_name = 'deviantartAccessToken'

# Initialize variables
deviantart_code = ""
deviantart_client_id = ""
deviantart_client_secret = ""
deviantart_access_token = ""

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

# Define your API endpoints and access token
upload_url = "https://www.deviantart.com/api/v1/oauth2/stash/submit"
publish_url = "https://www.deviantart.com/api/v1/oauth2/stash/publish"
access_token = "6e35d533b6584606680a963ea60c390b7bff8ef2551488c727"

item_id = None  # Initialize item_id as None

def upload_to_deviantart(title, artist_comments, tags, is_dirty, file_path, is_mature="no"):
    if tags:
        tags_list = tags.split(',')
    # Upload the file to DeviantArt
    params = {
        "title": title,
        "artist_comments": artist_comments,
        "is_dirty": is_dirty,
        "is_mature": is_mature  # Set "is_mature" parameter to "no" by default
    }
    # Add tags to the parameters with numerical indices
    if tags:
        for index, tag in enumerate(tags.split(',')):
            params[f"tags[{index}]"] = tag
    
    files = {
        "test": (os.path.basename(file_path), open(file_path, "rb"), "image/png")
    }

    headers = {
        "Authorization": f"Bearer {deviantart_access_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"  # Replace with your User Agent
    }

    response = requests.post(upload_url, data=params, files=files, headers=headers)

    if response.status_code == 200:
        data = response.json()
        item_id = data.get("itemid")
        print("Upload successful. Item ID:", item_id)
        return item_id
    else:
        if "invalid_token" in response.text:
            print("Bad token: The access token is invalid or expired. You need to refresh it.")
        else:
            print("Upload failed. Status code:", response.status_code)
            print(response.text)
        #here is where a bad token will be shown in the response inlcuding "{"error":"invalid_token","error_description":"Expired oAuth2 user token. The client should request a new one with an access code or a refresh token.","status":"error"}"


def publish_to_deviantart(item_id, is_mature="no", mature_level=None, mature_classification_csv=None):
    # Define your publish parameters here, including the "Mature" status
    publish_params = {
        "itemid": item_id,
        "is_mature": is_mature,
        "agree_submission": "1",
        "agree_tos": "1",
        "allow_free_download": "0",
    }

    if mature_classification_csv:
        mature_classifications = mature_classification_csv.split(',')
        for index, classification in enumerate(mature_classifications):
            publish_params[f"mature_classification[{index}]"] = classification

    headers = {
        "Authorization": f"Bearer {deviantart_access_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"  # Replace with your User Agent    
    }
    # Make the publish request to DeviantArt
    publish_response = requests.post(publish_url, data=publish_params, headers=headers)

    if publish_response.status_code == 200:
        publish_data = publish_response.json()
        print("Publish successful. Deviation URL:", publish_data.get("url"))
    else:
        print("Publish failed. Status code:", publish_response.status_code)
        print(publish_response.text)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.mature == "yes" and args.mature_level is None:
        parser.error("If 'mature' is 'yes', 'mature_level' is required.")
    
    # Convert the CSV string of tags to a list
    if args.tags_csv:
        tags_list = args.tags_csv.split(',')

    item_id = upload_to_deviantart(args.title, args.artist_comments, args.tags_csv, args.is_dirty, args.file, args.mature)

    if item_id is not None:
        publish_to_deviantart(item_id, args.mature, args.mature_level, args.mature_classification_csv)
    else:
        print("WARNING: No ID")



