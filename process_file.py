# import argparse
import re
from logger import logger

# parser = argparse.ArgumentParser()
# parser.add_argument("filepath")
# args = parser.parse_args()

# FILEPATH = args.filepath


LATITUDE_IDENTIFIER = "lat ="
DATE_FORMAT = "%b %d, %Y %I:%M %p"

# Asuncion coordinates
TARGET_LATITUDE = -25.5
TARGET_LONGITUDE = -57.5

# Measurement in Asuncion in Dobson Units


# 360 bins centered on 179.5  W  to 179.5  E
LONGITUDES_INDEXES = [num / 10 for num in range(-1795, 1796, 10)]


def process_file(filepath: str):
    target_measurement_dobson_units = None

    logger.info(f"Processing {filepath}")
    with open(filepath, "rt") as f:
        logger.info("Getting reading date and time from header 1st line")
        header_line_1 = f.readline()
        pattern = r"\s+Day:\s+\d+ (\b[A-Za-z]+\s+\d{1,2}, \d{4}\b).*LECT: (\d{2}:\d{2} [ap]m)"
        match = re.search(pattern, header_line_1)

        if match:
            date = match.group(1)
            time = match.group(2)

            logger.info(f"Found date {date} and time {time}")
        else:
            # print(
            #     f"No date and time match found in file {filepath}.\nHeader line value: {header_line_1}")
            # input("Press enter to continue. ")
            logger.warning(
                f"No date and time match found.\nHeader line value: {header_line_1}")
            print("No match found.")

        logger.info("Skipping remaining header lines")
        for i in range(2):
            f.readline()

        latitude_data = ""
        latitude = None

        while True:
            line = f.readline()
            if not line:
                break
            original_line = line
            line = line.rstrip().replace("\n", "")[1:]

            if LATITUDE_IDENTIFIER in line:
                logger.info("Last line of latitude data reached")
                line = line.split(LATITUDE_IDENTIFIER)
                latitude_data += line[0].rstrip()
                latitude = float(line[1].strip())

                if latitude == TARGET_LATITUDE:
                    logger.info(f"Found matching latitude {latitude}")

                    longitudes = [int(latitude_data[i:i+3])
                                  for i in range(0, len(latitude_data), 3)]

                    for i in range(360):
                        if LONGITUDES_INDEXES[i] == TARGET_LONGITUDE:
                            # print(i)
                            target_measurement_dobson_units = longitudes[i]
                    #         print(f"{LONGITUDES_INDEXES[i]}\t{longitudes[i]}")
                    # print(longitudes[int(abs(-179.5-TARGET_LONGITUDE))])
                    break
                else:
                    logger.debug(
                        f"Latitude {latitude} does not match target latitude {TARGET_LATITUDE}")
                latitude_data = ""
                latitude = None
            else:
                latitude_data += line

    if target_measurement_dobson_units is not None:
        return target_measurement_dobson_units, date.replace("  ", " "), time
    else:
        logger.error(
            f"No measurement found for target {TARGET_LATITUDE},{TARGET_LONGITUDE}")
        return None


if __name__ == "__main__":
    import os
    import pandas as pd
    from datetime import datetime as dt
    df = pd.DataFrame(columns=["timestamp", "UV", "OZONE"])
    FILES_PATH = "./data"
    

    contents = os.listdir(FILES_PATH)
    files = [item for item in contents if not os.path.isdir(
        os.path.join(FILES_PATH, item))]

    for file in files:
        measurement, date, time = process_file(os.path.join(FILES_PATH, file))
        timestamp = int(dt.strptime(f"{date} {time}", DATE_FORMAT).timestamp())

        if measurement == 0:
            continue

        df.loc[len(df)] = [timestamp, 0, measurement]
        print(measurement, timestamp)
    print(df)
    df.to_csv("./ozone_readings.csv", index=False)
