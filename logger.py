import os
import logging
os.chdir(os.path.dirname(__file__))

LOG_FILENAME = ".log"

logger = logging.getLogger("ozonewatch")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILENAME)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
# logging.basicConfig(filename=f'./{LOG_FILENAME}', level=logging.INFO)
# print(f"Logging to {os.getcwd()}{LOG_FILENAME}")