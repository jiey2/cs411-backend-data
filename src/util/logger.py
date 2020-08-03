import logging
import os
import sys

from src.configs.configs import NORMAL_LOGGER

formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")


def get_logger(name, log_file, level=logging.DEBUG, format=True):

    # output to both console and file
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')

    if format:
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# mkdir if not exist
if not os.path.exists(os.path.dirname(NORMAL_LOGGER)):
    os.mkdir(os.path.dirname(NORMAL_LOGGER))

log = get_logger('normal', os.path.abspath(NORMAL_LOGGER))
