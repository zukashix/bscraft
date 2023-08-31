# Common utilities for BSCraft Launcher
# Author: zukashix

# import required modules
import requests
import uuid
import psutil
import os
import shutil

# define web headers

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# function to check internet connection
def checkInternet() -> bool:
    try:
        requests.get('https://updater.braxtonelmer.com/', timeout=10, headers=headers)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def getRam() -> int: # function to get ram in mb
    return int(psutil.virtual_memory().total / (1024**2))

# function to download a file using url 
def downloadFile(file_url, file_loc, callback = None):
    r = requests.get(file_url, stream = True, headers=headers, verify=False)

    if callback != None:
        callback["setMax"](int(r.headers.get('content-length', 0)))
        downloadedSize = 0

    with open(file_loc, 'wb') as ufile:
        for chunk in r.iter_content(chunk_size=1024):

        # Writing one chunk at a time to file (No excessive memory usage on large-size files)
            if chunk:
                ufile.write(chunk)
                ufile.flush()

                if callback != None:
                    downloadedSize += len(chunk)
                    callback["setProgress"](downloadedSize)


def generate_offline_uuid(username):
    # Generate a UUID version 3 using the username and Minecraft's UUID namespace
    namespace = uuid.UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d')
    uuid_str = uuid.uuid3(namespace, username).hex

    # Insert hyphens at the correct positions to match the UUID format
    formatted_uuid = f"{uuid_str[:8]}-{uuid_str[8:12]}-4{uuid_str[13:16]}-a{uuid_str[16:19]}-{uuid_str[19:]}"

    return formatted_uuid


def copy_folder_contents(source_folder, destination_folder):
    # Iterate through all the files and folders in the source folder
    for root, dirs, files in os.walk(source_folder):
        # Create the corresponding folder structure in the destination folder
        dest_root = os.path.join(destination_folder, os.path.relpath(root, source_folder))
        os.makedirs(dest_root, exist_ok=True)

        # Copy files to the destination folder, overwriting any existing files
        for file in files:
            source_path = os.path.join(root, file)
            dest_path = os.path.join(dest_root, file)
            shutil.copy2(source_path, dest_path)  # copy2 preserves metadata (timestamps, etc.)
