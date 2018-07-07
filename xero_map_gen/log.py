import os
import logging
import coloredlogs

from . import PKG_NAME

ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.setLevel(logging.DEBUG)
PKG_LOGGER = logging.getLogger(PKG_NAME)

def setup_logging(log_file, stream_log_level, file_log_level):
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(file_log_level)
        ROOT_LOGGER.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_log_level)
    if os.name != 'nt':
        stream_handler.setFormatter(coloredlogs.ColoredFormatter())
    stream_handler.addFilter(coloredlogs.HostNameFilter())
    stream_handler.addFilter(coloredlogs.ProgramNameFilter())
    # TODO: maybe process quiet differently so that it does not add a stream handler
    ROOT_LOGGER.addHandler(stream_handler)
    logging.info("stream log level: %s", stream_handler.level)
    if not log_file:
        logging.info("file log level: %s", file_handler.level)
