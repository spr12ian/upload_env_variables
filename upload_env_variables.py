import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_private_data_directory_id() -> str:
    private_data_directory_id = os.getenv("PRIVATE_DATA_DIRECTORY_ID")
    if not private_data_directory_id:
        raise ValueError(
            "Private data directory id not found. Please set the PRIVATE_DATA_DIRECTORY_ID environment variable."
        )
    return private_data_directory_id


def upload_file_to_google_drive(file_path: str, drive_folder_id: str):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({"parents": [{"id": drive_folder_id}]})
    file.SetContentFile(file_path)
    file.Upload()
    print(
        f"File '{file_path}' has been uploaded to Google Drive folder with ID '{drive_folder_id}'."
    )


def list_txt_files(directory: str):
    txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    return txt_files


private_data_directory_id = get_private_data_directory_id()

# Upload all .txt files in the current directory (except requirements.txt) to the Google Drive folder
current_directory = os.getcwd()
txt_files = list_txt_files(current_directory)
print("List of .txt files in the current directory:")
for txt_file in txt_files:
    if txt_file == "requirements.txt":
        continue
    print(txt_file)
    upload_file_to_google_drive(txt_file, private_data_directory_id)
