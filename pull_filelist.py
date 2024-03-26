import requests
from datetime import datetime as dt
from bs4 import BeautifulSoup
import pandas as pd
from logger import logger

URL = "https://ozonewatch.gsfc.nasa.gov/data/omi/Y2024"
DATE_FORMAT = '%Y-%m-%d %H:%M'


def date_string_to_timestamp(date: str):
    date_object = dt.strptime(date, DATE_FORMAT)
    return dt.timestamp(date_object)


def pull_filelist():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            html_content = response.text
        else:
            logger.error(
                f"Failed to fetch webpage. Status code: {response.status_code}")
            # exit()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching webpage: {e}")
        # exit()

    soup = BeautifulSoup(html_content, 'html.parser')
    pre_tag = soup.find('pre')
    links = pre_tag.find_all('a')[5:]

    pulled_filelist_df = pd.DataFrame(
        columns=["filename", "timestamp", "filesize_kib"])
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)

        # Find the next element which should contain the last modified time and filesize
        next_element = link.find_next_sibling(string=True)
        last_modified_time, filesize = next_element.strip().split("  ")
        timestamp = int(
            date_string_to_timestamp(last_modified_time))
        filesize = int(filesize[:-1])

        logger.info(
            f"Found file {text} with timestamp {timestamp} and file size {filesize}K")

        pulled_filelist_df.loc[len(pulled_filelist_df.index)] = [
            href, timestamp, filesize]
        # print(f"{i} Link: {href}, Text: {text}, LM Time: {last_modified_time}, LM Timestamp: {timestamp}, Size: {filesize}")

    return pulled_filelist_df.sort_values(by="filename")


if __name__ == "__main__":
    pulled_filelist_df = pull_filelist()
    pulled_filelist_df.to_csv("pulled_filelist.csv", index=False)
