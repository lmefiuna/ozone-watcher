import os
from logger import logger
from datetime import datetime as dt
import pandas as pd
from pull_filelist import pull_filelist
from pull_files import pull_files, DATA_FOLDER_PATH
from process_file import process_file, DATE_FORMAT
from mysql_connection import insert_row
os.chdir(os.path.dirname(__file__))

# True for downloading all files, including processed ones and attempting to load to database
compute_all = False

filelist_df = pull_filelist()
downloaded_files_df = pull_files(filelist_df)

output_df = pd.DataFrame(columns=["timestamp", "UV", "OZONE"])

if compute_all:
    logger.warning("Processing all files, including previously processed.")
    contents = os.listdir(DATA_FOLDER_PATH)
    
    files = [item for item in contents if not os.path.isdir(
        os.path.join(DATA_FOLDER_PATH, item))]
    
    for file in files:
        result = process_file(os.path.join(DATA_FOLDER_PATH, file))
        
        if result is None:
            continue
        
        measurement, date, time = result
        timestamp = int(dt.strptime(f"{date} {time}", DATE_FORMAT).timestamp())

        # ignore 0 value measurementes, acording to file format description
        if measurement == 0:
            continue

        output_df.loc[len(output_df)] = [timestamp, 0, measurement]
else:
    logger.debug("Processing only new files")
    for index, row in downloaded_files_df.iterrows():
        result = process_file(os.path.join(DATA_FOLDER_PATH, row["filename"]))
        
        if result is None:
            continue
        
        measurement, date, time = result
        timestamp = int(dt.strptime(f"{date} {time}", DATE_FORMAT).timestamp())

        # ignore 0 value measurementes, acording to file format description
        if measurement == 0:
            continue

        output_df.loc[len(output_df)] = [timestamp, 0, measurement]

# output_df.to_csv("./output_ozone_readings.csv", index=False)
for index, row in output_df.iterrows():
    insert_row(row["timestamp"], row["OZONE"])