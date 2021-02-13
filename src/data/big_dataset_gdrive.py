import subprocess

def gdrive_download(FILE_ID, FILENAME):
    return subprocess.call("./src/scripts/gdrive-download.sh", FILE_ID, FILENAME)

def gdrive_unzip(FILENAME):
    return subprocess.call("./src/scripts/gdrive-unzip.sh", FILENAME)