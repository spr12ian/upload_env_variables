import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def authenticate_service_account():
    # Define the scope
    scopes = ["https://www.googleapis.com/auth/drive"]

    # Path to your service account JSON file
    SERVICE_ACCOUNT_FILE = get_private_data_service_account_file()

    # Load the service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=scopes
    )
    return credentials

def get_private_data_directory_id() -> str:
    private_data_directory_id = os.getenv("PRIVATE_DATA_DIRECTORY_ID")
    if not private_data_directory_id:
        raise ValueError(
            "Private data directory id not found. Please set the PRIVATE_DATA_DIRECTORY_ID environment variable."
        )
    return private_data_directory_id

def get_private_data_service_account_file() -> str:
    service_account_file = os.getenv("PRIVATE_DATA_SERVICE_ACCOUNT_FILE")
    if not service_account_file:
        raise ValueError(
            "Private data service account file not found. Please set the PRIVATE_DATA_SERVICE_ACCOUNT_FILE environment variable."
        )
    return service_account_file

def upload_file_to_google_drive(file_path, folder_id):
    credentials = authenticate_service_account()
    service = build("drive", "v3", credentials=credentials)

    file_name = os.path.basename(file_path)

    # Search for the file in the specified folder
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])

    if items:
        # File exists, update it
        file_id = items[0]['id']
        media = MediaFileUpload(file_path, resumable=True)
        updated_file = service.files().update(fileId=file_id, media_body=media).execute()
        print(f"File '{file_path}' updated successfully on Google Drive. File ID: {updated_file.get('id')}")
    else:
        # File does not exist, create it
        file_metadata = {
            "name": file_name,
            "parents": [folder_id],
        }
        media = MediaFileUpload(file_path, resumable=True)
        new_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f"File '{file_path}' uploaded successfully to Google Drive. File ID: {new_file.get('id')}")


TEST_FILE = "_private_data/TEST_FILE.txt"

# Set your target Google Drive folder ID
TARGET_FOLDER_ID = get_private_data_directory_id()

# Upload a test file
upload_file_to_google_drive(TEST_FILE, TARGET_FOLDER_ID)