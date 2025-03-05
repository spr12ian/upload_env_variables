import os

PRIVATE_DATA_DIRECTORY = "_private_data"

private_data_keys=[
    "GITHUB_USER_EMAIL",
    "GITHUB_USER_NAME",
    "NVIDIA_OPENAI_API_KEY",
    "PRIVATE_DATA_DIRECTORY_ID",
    "PRIVATE_DATA_SERVICE_ACCOUNT_FILE",
]

for key in private_data_keys:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"{key} not found in environment variables")
    path=f"{PRIVATE_DATA_DIRECTORY}/{key}.txt"
    with open(path, "w") as f:
        f.write(value)

env_vars = os.environ

for key, value in env_vars.items():
    if key not in private_data_keys:
        print(f"{key}: {value}")