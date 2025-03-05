# upload_env_variables
Python repository
Avoid PyDrive2 and pydrive due to authentication issues

Private environment data is stored in a private data directory on Google Drive.
The file names in Google Drive correspond to the environment variable names,
and the file contents correspond to the environment variable values.

download_private_data_files.py
downloads the files from Google Drive into a local private data directory

upload_private_data_files.py
uploads the files from a local private data directory into Google Drive
