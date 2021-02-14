import requests
from zipfile import ZipFile
from pathlib import Path

class google_drive_downloader():
    # credit: converted to class from https://stackoverflow.com/a/39225039 

    def __init__(self, cwd_path=None, data_path=None):
        """
        data_path: root directory of where to extract data
        """

        if cwd_path is None:
            # By default, we will assume '.' data
            self.cwd_path = Path('.').absolute()
        else:
            self.cwd_path = cwd_path.absolute()

        if data_path is None:
            # By default, we will assume ./data
            self.data_path = self.cwd_path / 'data'
        else:
            self.data_path = data_path.absolute()

        if not self.data_path.exists():
            self.data_path.mkdir()

        self.zip_fname = self.cwd_path / 'tmp_download_from_gdrive.zip'

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(self, response):
        CHUNK_SIZE = 32768

        with open(self.zip_fname, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    def download_as_zip(self, gdrive_id):
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()

        response = session.get(URL, params = { 'id' : gdrive_id }, stream = True)
        token = self.get_confirm_token(response)

        if token:
            params = { 'id' : gdrive_id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)

        self.save_response_content(response)    


    def unzip_to_data_path(self):
        """Extract data to data path"""
        with ZipFile(self.zip_fname, 'r') as zf:
            zf.extractall(path=self.data_path)

    def remove_archive_subfolder(self, archive_subfolder):
        """
        Move: /data_path/unwanted_folder/train -> /data_path/train
        """
        # Create path with unwanted_folder
        move_up_path = self.data_path / archive_subfolder

        # Move all directories
        for folder in move_up_path.iterdir():
            if folder.is_dir():
                new_folder = folder.parent.parent / folder.name
                folder.rename(new_folder)


        # Delete the unwanted_folder directory
        move_up_path.rmdir()

    def print_data_path_contents(self):
        print(f"data_path:{self.data_path}")
        print("directory list:")
        # print data_path contents
        for folder in self.data_path.iterdir():
            print(folder)

    def import_gdrive_dataset(self, gdrive_id, archive_subfolder=None):
        """
           1. downloads the data from the specified gdrive_id as a zip 
           2. extracts the downloaded data to the specified data_path
           3. deletes the temporary zip file
        """
        self.download_as_zip(gdrive_id)
        self.unzip_to_data_path()

        # Delete the temporary file (using Path)
        self.zip_fname.unlink()

        if archive_subfolder is not None:
            self.remove_archive_subfolder(archive_subfolder)

        # Display result
        self.print_data_path_contents()


# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) is not 4:
#         print("Usage (google_drive_downloader): python data_utils.py google_drive_downloader drive_file_id destination_file_path")
#     else:

#         fn_name = sys.argv[1]

#         if fn_name == 'google_drive_downloader':
#             # TAKE ID FROM SHAREABLE LINK
#             file_id = sys.argv[2]
#             # DESTINATION FILE ON YOUR DISK
#             archive_subfolder = sys.argv[3]

#             gdd = google_drive_downloader()
#             gdd.import_gdrive_dataset(gdrive_id='1iYaNijLmzsrMlAdMoUEhhJuo-5bkeAuj', archive_subfolder='segmentation_data')
