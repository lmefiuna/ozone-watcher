import argparse
from logger import logger

parser = argparse.ArgumentParser()
parser.add_argument("filepath")
args = parser.parse_args()

FILEPATH = args.filepath

logger.info(f"Processing {FILEPATH}")

LATITUDE_IDENTIFIER = "lat ="

# Asuncion coordinates
TARGET_LATITUDE = -25.5
TARGET_LONGITUDE = -57.5

# Measurement in Asuncion in Dobson Units
TARGET_MEASUREMENT_DU = None


# 360 bins centered on 179.5  W  to 179.5  E
LONGITUDES_INDEXES = [num / 10 for num in range(-1795, 1796, 10)]


with open(FILEPATH, "rt") as f:
    # skip header lines
    logger.info("Skipping header lines")
    for i in range(3):
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
                        TARGET_MEASUREMENT_DU = longitudes[i]
                #         print(f"{LONGITUDES_INDEXES[i]}\t{longitudes[i]}")
                # print(longitudes[int(abs(-179.5-TARGET_LONGITUDE))])
                break
            else:
                logger.info(
                    f"Latitude {latitude} does not match target latitude {TARGET_LATITUDE}")
            latitude_data = ""
            latitude = None
        else:
            latitude_data += line

if TARGET_MEASUREMENT_DU is not None:
    print(TARGET_MEASUREMENT_DU)
    exit(0)
else:
    exit(1)
