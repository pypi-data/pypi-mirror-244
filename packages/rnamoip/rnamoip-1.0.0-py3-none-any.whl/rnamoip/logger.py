
import logging
from logging import Logger
import sys


def get_logger() -> Logger:
    return logging.getLogger()


def init(file_name: str, level: int = logging.INFO):
    logging.basicConfig(
        filename=file_name,
        filemode='w',
        format='%(asctime)s %(levelname)s: %(message)s',
        level=level,
        force=True,
    )

    logger = get_logger()
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(level)
    logger.addHandler(streamHandler)
