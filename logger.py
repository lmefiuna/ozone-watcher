import os
import logging
os.chdir(os.path.dirname(__file__))

logger = logging.getLogger("ozonewatch")
logging.basicConfig(filename='./log', encoding='utf-8', level=logging.INFO)
