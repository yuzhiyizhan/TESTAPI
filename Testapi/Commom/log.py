import logging
import os
import time
from Testapi.config.config import LOG_PATH
from Testapi.config.config import LOG_NAME
from loguru import logger


# @logger.catch
def Log(log):
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    logger.add(
        LOG_NAME, level='INFO', rotation='2028 MB'
    )
    logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}{log}')
    # logging.basicConfig(filename=LOG_NAME, level=logging.INFO)
    # logging.info(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}{log}')
