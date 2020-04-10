import logging
import os
import time
from Testapi.config.config import LOG_PATH
from Testapi.config.config import LOG_NAME


def Log(log):
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    logging.basicConfig(filename=LOG_NAME, level=logging.INFO)
    logging.info(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}{log}')
