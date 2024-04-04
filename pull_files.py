import os
import requests
import pandas as pd
from pull_filelist import URL, pull_filelist
from logger import logger
os.chdir(os.path.dirname(__file__))

DATA_FOLDER_PATH = "./data"


def download_file(source_url: str, output_file_path: str) -> bool:
    try:
        response = requests.get(source_url)
        if response.status_code == 200:
            with open(output_file_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"File downloaded successfully to: {output_file_path}")
            print(f"File downloaded successfully to: {output_file_path}")
            return True
        else:
            logger.error(
                f"Failed to download file. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
        return False
    except Exception:
        return False


def pull_files(pulled_filelist_df: pd.DataFrame):
    if not os.path.isdir(DATA_FOLDER_PATH):
        os.mkdir(DATA_FOLDER_PATH)
    # pulled_filelist_df = pull_filelist()

    downloaded_files_df = pd.DataFrame(
        columns=["filename", "timestamp", "filesize_kib"])

    for index, row in pulled_filelist_df.iterrows():
        filename = row['filename']
        timestamp = row['timestamp']
        filesize = row['filesize_kib']
        logger.info(f"Processing file {filename}")

        download_new_file = False

        if os.path.isfile(f"{DATA_FOLDER_PATH}/{filename}"):
            existing_timestamp = os.path.getmtime(
                f"{DATA_FOLDER_PATH}/{filename}")
            logger.info(f"File {filename} already exists")

            # TODO: compare filesizes
            if timestamp != existing_timestamp:
                logger.info(
                    f"File {filename} has different timestamp {timestamp}, previous timestamp is {existing_timestamp}")
                download_new_file = True
        else:
            download_new_file = True

        if download_new_file:
            downloaded = False
            MAX_RETRIES = 5
            for i in range(MAX_RETRIES):
                if download_file(f"{URL}/{filename}", f"{DATA_FOLDER_PATH}/{filename}"):
                    os.utime(f"{DATA_FOLDER_PATH}/{filename}",
                             (timestamp, timestamp))
                    downloaded_files_df.loc[len(downloaded_files_df.index)] = [
                        filename, timestamp, filesize]
                    downloaded = True
                    break
            if not downloaded:
                logger.error(f"Could not download file {filename}")

    return downloaded_files_df


if __name__ == "__main__":
    pulled_filelist = pull_filelist()
    downloaded_files = pull_files(pulled_filelist)
    print(pulled_filelist)
    print(downloaded_files)
    # logger.info(f"Pulling files into {DATA_FOLDER_PATH}")
